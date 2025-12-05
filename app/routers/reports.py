from fastapi import APIRouter
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


@router.get("/streams-by-platform")
def streams_by_platform():
    """
    Streams agregadas por plataforma (service).
    """
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT platform, SUM(streams) AS total_streams
            FROM stream_events
            GROUP BY platform
            ORDER BY total_streams DESC
            """
        )
        rows = [dict(r) for r in cur.fetchall()]
    return rows
