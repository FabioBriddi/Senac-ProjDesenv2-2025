from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pathlib import Path
from datetime import datetime
import csv
import codecs

from ..db import get_connection

router = APIRouter(tags=["ingestions"])

# Pasta para salvar os arquivos enviados
UPLOAD_DIR = Path(__file__).resolve().parents[1] / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# Encodings comuns em CSVs brasileiros (ordem de tentativa)
ENCODINGS_TO_TRY = ["utf-8-sig", "utf-8", "latin-1", "cp1252", "iso-8859-1"]


def detect_and_read_csv(file_path: Path) -> tuple[list[dict], str]:
    """
    Tenta ler o CSV com diferentes encodings.
    Retorna (lista de dicts, encoding usado).
    """
    for encoding in ENCODINGS_TO_TRY:
        try:
            with file_path.open("r", encoding=encoding, newline="") as f:
                # Tenta ler algumas linhas para validar o encoding
                reader = csv.DictReader(f)
                rows = list(reader)
                return rows, encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception as e:
            # Outro erro, tenta próximo encoding
            continue

    raise ValueError(
        f"Não foi possível decodificar o arquivo com os encodings: {ENCODINGS_TO_TRY}"
    )


def open_csv_with_fallback(file_path: Path):
    """
    Abre o CSV tentando múltiplos encodings.
    Retorna um file handle aberto com o encoding correto.
    """
    for encoding in ENCODINGS_TO_TRY:
        try:
            f = file_path.open("r", encoding=encoding, newline="")
            # Tenta ler o header para validar
            reader = csv.reader(f)
            header = next(reader, None)
            f.seek(0)  # Volta ao início
            if header:
                return f, encoding
            f.close()
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception:
            continue

    raise ValueError(
        f"Não foi possível decodificar o arquivo com os encodings: {ENCODINGS_TO_TRY}"
    )


# -------------------------------------------------------------------
# 1) Histórico de ingestões
# -------------------------------------------------------------------
@router.get("/")
def list_ingestions():
    """
    Lista histórico de uploads (artistas e dispositivos).
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, source_id, file_name, ingested_at, total_rows
        FROM ingestions
        ORDER BY datetime(ingested_at) DESC
        """
    )
    rows = [dict(r) for r in cur.fetchall()]

    conn.close()
    return rows


# -------------------------------------------------------------------
# 2) Upload CSV por ARTISTA -> stream_events
# -------------------------------------------------------------------
def parse_artist_csv(file_path: Path) -> tuple[list[tuple], str]:
    """
    Lê o CSV de artista (FUGA / similar) e devolve uma lista de tuplas:
    (artist_name, track_title, isrc, upc, platform, country, stream_date, streams)
    
    Também retorna o encoding detectado.
    """
    events = []

    rows, encoding_used = detect_and_read_csv(file_path)

    for row in rows:
        artist = (
            row.get("Artist Name")
            or row.get("artist_name")
            or row.get("Artist")
            or row.get("Artista")  # Português
            or ""
        )
        track = (
            row.get("Track Title")
            or row.get("Recording Name")
            or row.get("track_title")
            or row.get("Título")  # Português
            or row.get("Faixa")
            or ""
        )
        isrc = row.get("ISRC") or row.get("isrc") or ""
        upc = row.get("UPC") or row.get("upc") or ""
        platform = (
            row.get("Service")
            or row.get("Platform")
            or row.get("service")
            or row.get("Plataforma")  # Português
            or row.get("Serviço")
            or ""
        )
        country = (
            row.get("Country of Consumption")
            or row.get("Country")
            or row.get("country")
            or row.get("País")  # Português
            or ""
        )
        date_str = (
            row.get("Date")
            or row.get("Stream Date")
            or row.get("date")
            or row.get("Data")  # Português
            or ""
        )
        streams_str = (
            row.get("Streams")
            or row.get("Quantity")
            or row.get("streams")
            or row.get("Reproduções")  # Português
            or row.get("Quantidade")
            or "0"
        )

        stream_date = date_str.strip() if date_str else None

        try:
            # Remove separadores de milhar (ponto ou vírgula)
            cleaned = str(streams_str).replace(".", "").replace(",", "").strip()
            streams = int(cleaned or "0")
        except ValueError:
            streams = 0

        events.append(
            (
                artist.strip(),
                track.strip(),
                isrc.strip(),
                upc.strip(),
                platform.strip(),
                country.strip(),
                stream_date,
                streams,
            )
        )

    return events, encoding_used


@router.post("/upload/artist")
async def upload_artist(file: UploadFile = File(...)):
    """
    Upload de CSV por artista.
    Salva o arquivo em uploads/ e grava os registros em stream_events.
    """
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Envie um arquivo CSV")

    # Nome seguro com timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    safe_name = f"{timestamp}_{file.filename}"
    dest_path = UPLOAD_DIR / safe_name

    # Salvar o arquivo físico
    content = await file.read()
    dest_path.write_bytes(content)

    # Ler o CSV e montar os eventos
    try:
        events, encoding_used = parse_artist_csv(dest_path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    total_rows = len(events)

    conn = get_connection()
    cur = conn.cursor()

    # 1 = fonte CSV artistas (ajuste se usar outro id na tabela sources)
    source_id = 1

    # Registrar a ingestão
    cur.execute(
        """
        INSERT INTO ingestions (source_id, file_name, ingested_at, total_rows)
        VALUES (?, ?, ?, ?)
        """,
        (source_id, safe_name, datetime.now().isoformat(), total_rows),
    )
    ingestion_id = cur.lastrowid

    # Inserir detalhamento em stream_events
    if events:
        cur.executemany(
            """
            INSERT INTO stream_events (
                ingestion_id,
                artist_name,
                track_title,
                isrc,
                upc,
                service,
                country,
                stream_date,
                streams
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    ingestion_id,
                    e[0],  # artist_name
                    e[1],  # track_title
                    e[2],  # isrc
                    e[3],  # upc
                    e[4],  # service (plataforma)
                    e[5],  # country
                    e[6],  # stream_date
                    e[7],  # streams
                )
                for e in events
            ],
        )

    conn.commit()
    conn.close()

    return {
        "status": "ok",
        "ingestion_id": ingestion_id,
        "rows_inserted": total_rows,
        "encoding_detected": encoding_used,
    }


# -------------------------------------------------------------------
# 3) Upload CSV por DISPOSITIVO -> device_daily_streams
# -------------------------------------------------------------------
@router.post("/upload/device")
async def upload_device(
    distributor: str = Form(...),  # "FUGA", "Vydia" ou "The Orchard"
    file: UploadFile = File(...),
):
    """
    Upload de CSV por dispositivo.

    - Primeira coluna = nome do dispositivo
    - Demais colunas = dias do período

    Os dados vão para a tabela device_daily_streams.
    """
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Envie um arquivo CSV.")

    # Salvar o arquivo
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    saved_name = f"{timestamp}_{file.filename}"
    saved_path = UPLOAD_DIR / saved_name

    contents = await file.read()
    saved_path.write_bytes(contents)

    conn = get_connection()
    cur = conn.cursor()

    # 2 = "Uploads CSV (dispositivos)" na tabela sources
    source_id = 2

    ingested_at = datetime.now().isoformat()
    cur.execute(
        """
        INSERT INTO ingestions (source_id, file_name, ingested_at, total_rows)
        VALUES (?, ?, ?, 0)
        """,
        (source_id, saved_name, ingested_at),
    )
    ingestion_id = cur.lastrowid

    try:
        total_points, encoding_used = insert_device_data_from_csv(
            conn=conn,
            csv_path=saved_path,
            ingestion_id=ingestion_id,
            distributor=distributor,
        )
    except Exception as e:
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=400, detail=f"Erro ao processar CSV: {e}")

    conn.commit()
    conn.close()

    return {
        "message": "Upload de dispositivos processado com sucesso.",
        "ingestion_id": ingestion_id,
        "file_name": saved_name,
        "distributor": distributor,
        "total_points": total_points,
        "encoding_detected": encoding_used,
    }


def insert_device_data_from_csv(
    conn, csv_path: Path, ingestion_id: int, distributor: str
) -> tuple[int, str]:
    """
    Lê um CSV em que:
      - a primeira coluna = nome do dispositivo
      - as demais colunas = dias do período
    e grava em device_daily_streams.

    Retorna (total_points_inserted, encoding_used).
    """
    cur = conn.cursor()

    # Detecta encoding e abre arquivo
    f, encoding_used = open_csv_with_fallback(csv_path)

    try:
        reader = csv.reader(f)

        # Cabeçalho
        header = next(reader, None)
        if not header or len(header) < 2:
            raise ValueError(
                "Cabeçalho do CSV inválido. Esperado: [device, dia1, dia2, ...]."
            )

        day_labels = header[1:]
        rows_to_insert = []

        for row in reader:
            if not row or len(row) < 2:
                continue

            device_name = row[0].strip()
            if not device_name:
                continue

            for idx, day_label in enumerate(day_labels, start=1):
                if idx >= len(row):
                    continue

                raw_val = row[idx].strip()
                if not raw_val:
                    continue

                try:
                    # Remove separadores de milhar
                    streams = int(
                        raw_val.replace(".", "").replace(",", "").strip()
                    )
                except ValueError:
                    # Se tiver texto estranho na célula, ignora
                    continue

                rows_to_insert.append(
                    (
                        ingestion_id,
                        distributor,
                        device_name,
                        day_label.strip(),
                        streams,
                    )
                )

        if rows_to_insert:
            cur.executemany(
                """
                INSERT INTO device_daily_streams (
                    ingestion_id,
                    distributor,
                    device_name,
                    day_label,
                    streams
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                rows_to_insert,
            )

        # Atualiza total_rows na tabela ingestions
        total_stream_points = len(rows_to_insert)
        cur.execute(
            "UPDATE ingestions SET total_rows = ? WHERE id = ?",
            (total_stream_points, ingestion_id),
        )

        return total_stream_points, encoding_used

    finally:
        f.close()


# -------------------------------------------------------------------
# 4) Deletar uma ingestão (e seus dados relacionados)
# -------------------------------------------------------------------
@router.delete("/{ingestion_id}")
def delete_ingestion(ingestion_id: int):
    """
    Remove uma ingestão e todos os dados associados.
    Útil para corrigir uploads errados.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Verifica se existe
    cur.execute("SELECT id, source_id FROM ingestions WHERE id = ?", (ingestion_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Ingestão não encontrada")

    source_id = row["source_id"]

    # Remove dados relacionados baseado na fonte
    if source_id == 1:  # Artistas
        cur.execute(
            "DELETE FROM stream_events WHERE ingestion_id = ?", (ingestion_id,)
        )
    elif source_id == 2:  # Dispositivos
        cur.execute(
            "DELETE FROM device_daily_streams WHERE ingestion_id = ?", (ingestion_id,)
        )

    # Remove a ingestão
    cur.execute("DELETE FROM ingestions WHERE id = ?", (ingestion_id,))

    conn.commit()
    conn.close()

    return {"status": "ok", "deleted_ingestion_id": ingestion_id}
