from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from typing import Optional
from io import StringIO
import csv

from ..db import get_db

router = APIRouter(tags=["reports"])


@router.get("/summary")
def summary():
    """
    Resumo geral:
    - total de artistas
    - total de linhas (faixas)
    - total de streams
    - primeira e última data encontradas
    """
    with get_db() as conn:
        cur = conn.cursor()

        cur.execute(
            "SELECT COUNT(DISTINCT artist_name) AS total_artists FROM stream_events"
        )
        total_artists = cur.fetchone()["total_artists"] or 0

        cur.execute("SELECT COUNT(*) AS total_tracks FROM stream_events")
        total_tracks = cur.fetchone()["total_tracks"] or 0

        cur.execute("SELECT SUM(streams) AS total_streams FROM stream_events")
        row = cur.fetchone()
        total_streams = row["total_streams"] or 0

        cur.execute(
            """
            SELECT stream_date
            FROM stream_events
            WHERE stream_date IS NOT NULL AND stream_date <> ''
            ORDER BY stream_date ASC
            LIMIT 1
            """
        )
        first = cur.fetchone()
        first_date = first["stream_date"] if first else None

        cur.execute(
            """
            SELECT stream_date
            FROM stream_events
            WHERE stream_date IS NOT NULL AND stream_date <> ''
            ORDER BY stream_date DESC
            LIMIT 1
            """
        )
        last = cur.fetchone()
        last_date = last["stream_date"] if last else None

    return {
        "total_artists": total_artists,
        "total_tracks": total_tracks,
        "total_streams": total_streams,
        "first_date": first_date,
        "last_date": last_date,
    }


@router.get("/top-artists")
def top_artists(limit: int = 10):
    """
    Top artistas por soma de streams.
    """
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT artist_name, SUM(streams) AS total_streams
            FROM stream_events
            GROUP BY artist_name
            ORDER BY total_streams DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = [dict(r) for r in cur.fetchall()]
    return rows


@router.get("/distributors")
def list_distributors():
    """
    Lista todas as distribuidoras disponíveis no banco.
    Útil para popular o filtro no frontend.
    """
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT DISTINCT distributor
            FROM device_daily_streams
            WHERE distributor IS NOT NULL AND distributor <> ''
            ORDER BY distributor
            """
        )
        rows = [row["distributor"] for row in cur.fetchall()]
    return rows


@router.get("/date-range")
def get_date_range():
    """
    Retorna o range de datas (day_label) disponíveis na tabela device_daily_streams.
    Útil para popular o filtro de período no frontend.
    """
    with get_db() as conn:
        cur = conn.cursor()
        
        cur.execute(
            """
            SELECT DISTINCT day_label
            FROM device_daily_streams
            WHERE day_label IS NOT NULL AND day_label <> ''
            ORDER BY day_label ASC
            """
        )
        all_dates = [row["day_label"] for row in cur.fetchall()]
        
        min_date = all_dates[0] if all_dates else None
        max_date = all_dates[-1] if all_dates else None
        
    return {
        "min_date": min_date,
        "max_date": max_date,
        "all_dates": all_dates
    }


@router.get("/streams-by-platform")
def streams_by_platform(
    distributor: Optional[str] = Query(None, description="Filtrar por distribuidora (ex: FUGA, VYDIA)"),
    date_from: Optional[str] = Query(None, description="Data inicial (day_label)"),
    date_to: Optional[str] = Query(None, description="Data final (day_label)")
):
    """
    Retorna séries de streams diários por plataforma (device),
    a partir da tabela device_daily_streams.
    """
    with get_db() as conn:
        cur = conn.cursor()

        query = """
            SELECT
                device_name,
                day_label,
                SUM(streams) AS total_streams
            FROM device_daily_streams
            WHERE 1=1
        """
        params = []

        if distributor:
            query += " AND distributor = ?"
            params.append(distributor)

        if date_from:
            query += " AND day_label >= ?"
            params.append(date_from)

        if date_to:
            query += " AND day_label <= ?"
            params.append(date_to)

        query += """
            GROUP BY device_name, day_label
            ORDER BY device_name, day_label ASC
        """

        cur.execute(query, params)
        rows = cur.fetchall()

    series_by_platform: dict[str, list[dict]] = {}

    for row in rows:
        device = row["device_name"] or ""
        date_str = row["day_label"]
        total_streams = row["total_streams"]

        if device not in series_by_platform:
            series_by_platform[device] = []
        series_by_platform[device].append(
            {
                "date": date_str,
                "streams": total_streams,
            }
        )

    result = [
        {"platform": platform, "points": points}
        for platform, points in series_by_platform.items()
    ]

    return result


@router.get("/streams-by-distributor")
def streams_by_distributor():
    """
    Retorna total de streams agrupado por distribuidora (FUGA, Vydia, The Orchard).
    """
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                distributor,
                SUM(streams) AS total_streams
            FROM device_daily_streams
            GROUP BY distributor
            ORDER BY total_streams DESC
            """
        )
        rows = [dict(r) for r in cur.fetchall()]
    return rows


# =============================================================================
# ENDPOINTS DE EXPORT CSV
# =============================================================================

@router.get("/export/platforms-csv")
def export_platforms_csv(
    distributor: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None)
):
    """
    Exporta dados de streams por plataforma em formato CSV.
    Colunas: Plataforma, Dia, Streams
    """
    with get_db() as conn:
        cur = conn.cursor()

        query = """
            SELECT
                device_name AS plataforma,
                day_label AS dia,
                SUM(streams) AS streams
            FROM device_daily_streams
            WHERE 1=1
        """
        params = []

        if distributor:
            query += " AND distributor = ?"
            params.append(distributor)

        if date_from:
            query += " AND day_label >= ?"
            params.append(date_from)

        if date_to:
            query += " AND day_label <= ?"
            params.append(date_to)

        query += """
            GROUP BY device_name, day_label
            ORDER BY device_name, day_label ASC
        """

        cur.execute(query, params)
        rows = cur.fetchall()

    # Gerar CSV
    output = StringIO()
    writer = csv.writer(output, delimiter=';')
    
    # Header
    writer.writerow(["Plataforma", "Dia", "Streams"])
    
    # Data
    for row in rows:
        writer.writerow([row["plataforma"], row["dia"], row["streams"]])
    
    output.seek(0)
    
    # Retornar como download
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=streams_por_plataforma.csv"
        }
    )


@router.get("/export/distributors-csv")
def export_distributors_csv():
    """
    Exporta dados de streams por distribuidora em formato CSV.
    """
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                distributor AS distribuidora,
                SUM(streams) AS total_streams
            FROM device_daily_streams
            GROUP BY distributor
            ORDER BY total_streams DESC
            """
        )
        rows = cur.fetchall()

    output = StringIO()
    writer = csv.writer(output, delimiter=';')
    
    writer.writerow(["Distribuidora", "Total Streams"])
    
    for row in rows:
        writer.writerow([row["distribuidora"], row["total_streams"]])
    
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=streams_por_distribuidora.csv"
        }
    )


@router.get("/export/top-artists-csv")
def export_top_artists_csv(limit: int = 100):
    """
    Exporta top artistas em formato CSV.
    """
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT artist_name, SUM(streams) AS total_streams
            FROM stream_events
            GROUP BY artist_name
            ORDER BY total_streams DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = cur.fetchall()

    output = StringIO()
    writer = csv.writer(output, delimiter=';')
    
    writer.writerow(["Artista", "Total Streams"])
    
    for row in rows:
        writer.writerow([row["artist_name"], row["total_streams"]])
    
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=top_artistas.csv"
        }
    )
