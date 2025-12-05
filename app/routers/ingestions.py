from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from datetime import datetime
import csv

from ..db import get_db

router = APIRouter(tags=["ingestions"])

# Pasta para salvar os arquivos enviados
UPLOAD_DIR = Path(__file__).resolve().parents[1] / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


@router.get("/")
def list_ingestions():
    """Lista histórico de uploads."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, source_id, file_name, ingested_at, total_rows
            FROM ingestions
            ORDER BY datetime(ingested_at) DESC
            """
        )
        rows = [dict(r) for r in cur.fetchall()]
    return rows


def parse_artist_csv(file_path: Path):
    """
    Lê o CSV de artista (FUGA / similar) e devolve uma lista de tuplas:
    (artist_name, track_title, isrc, upc, platform, country, stream_date, streams)
    """
    events = []

    with file_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            artist = (
                row.get("Artist Name")
                or row.get("artist_name")
                or row.get("Artist")
                or ""
            )
            track = (
                row.get("Track Title")
                or row.get("Recording Name")
                or row.get("track_title")
                or ""
            )
            isrc = row.get("ISRC") or row.get("isrc") or ""
            upc = row.get("UPC") or row.get("upc") or ""
            platform = (
                row.get("Service")
                or row.get("Platform")
                or row.get("service")
                or ""
            )
            country = (
                row.get("Country of Consumption")
                or row.get("Country")
                or row.get("country")
                or ""
            )
            date_str = (
                row.get("Date")
                or row.get("Stream Date")
                or row.get("date")
                or ""
            )
            streams_str = (
                row.get("Streams")
                or row.get("Quantity")
                or row.get("streams")
                or "0"
            )

            # Normalização simples – mantém como veio, só tira espaços
            stream_date = date_str.strip() if date_str else None

            try:
                streams = int(str(streams_str).replace(",", "").strip() or "0")
            except ValueError:
                streams = 0

            events.append(
                (
                    artist,
                    track,
                    isrc,
                    upc,
                    platform,
                    country,
                    stream_date,
                    streams,
                )
            )

    return events


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
    events = parse_artist_csv(dest_path)
    total_rows = len(events)

    with get_db() as conn:
        cur = conn.cursor()

        # 1 = fonte CSV FUGA
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
                    platform,
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
                        e[4],  # platform
                        e[5],  # country
                        e[6],  # stream_date
                        e[7],  # streams
                    )
                    for e in events
                ],
            )

    return {
        "status": "ok",
        "ingestion_id": ingestion_id,
        "rows_inserted": total_rows,
    }
