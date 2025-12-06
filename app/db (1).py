from pathlib import Path
from contextlib import contextmanager
import sqlite3
from datetime import datetime

# Banco em app/music_insights.db
DB_PATH = Path(__file__).resolve().parent / "music_insights.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Tabela de fontes (sources)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            description TEXT,
            is_active INTEGER NOT NULL DEFAULT 1
        )
        """
    )

    # Tabela de ingestions
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS ingestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER NOT NULL,
            file_name TEXT NOT NULL,
            ingested_at TEXT NOT NULL,
            total_rows INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (source_id) REFERENCES sources(id)
        )
        """
    )

    # Tabela de eventos de stream por artista
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS stream_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingestion_id INTEGER NOT NULL,
            artist_name TEXT NOT NULL,
            track_title TEXT,
            isrc TEXT,
            upc TEXT,
            service TEXT,
            country TEXT,
            stream_date TEXT,
            streams INTEGER NOT NULL,
            FOREIGN KEY (ingestion_id) REFERENCES ingestions(id)
        )
        """
    )

    # Tabela de dados diários por dispositivo
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS device_daily_streams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingestion_id INTEGER NOT NULL,
            distributor TEXT NOT NULL,
            device_name TEXT NOT NULL,
            day_label TEXT NOT NULL,
            streams INTEGER NOT NULL,
            FOREIGN KEY (ingestion_id) REFERENCES ingestions(id)
        )
        """
    )

    # =========================================================================
    # NOVA TABELA: Conectores de API
    # =========================================================================
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS api_connectors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            base_url TEXT,
            auth_type TEXT NOT NULL DEFAULT 'api_key',
            api_key TEXT,
            api_secret TEXT,
            client_id TEXT,
            client_secret TEXT,
            token_url TEXT,
            additional_headers TEXT,
            is_active INTEGER NOT NULL DEFAULT 1,
            last_sync_at TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            notes TEXT
        )
        """
    )

    # =========================================================================
    # ÍNDICES PARA PERFORMANCE
    # =========================================================================

    # Índices para stream_events
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_stream_events_artist ON stream_events (artist_name)"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_stream_events_date ON stream_events (stream_date)"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_stream_events_service ON stream_events (service)"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_stream_events_country ON stream_events (country)"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_stream_events_ingestion ON stream_events (ingestion_id)"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_stream_events_artist_date ON stream_events (artist_name, stream_date)"
    )

    # Índices para device_daily_streams
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_device_streams_device ON device_daily_streams (device_name)"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_device_streams_day ON device_daily_streams (day_label)"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_device_streams_distributor ON device_daily_streams (distributor)"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_device_streams_ingestion ON device_daily_streams (ingestion_id)"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_device_streams_device_day ON device_daily_streams (device_name, day_label)"
    )

    # Índice para ingestions
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_ingestions_date ON ingestions (ingested_at)"
    )

    # Índice para api_connectors
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_api_connectors_name ON api_connectors (name)"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_api_connectors_active ON api_connectors (is_active)"
    )

    # =========================================================================
    # POPULAR TABELA SOURCES SE ESTIVER VAZIA
    # =========================================================================
    cur.execute("SELECT COUNT(*) AS cnt FROM sources")
    row = cur.fetchone()
    total_sources = row[0] if row else 0

    if total_sources == 0:
        cur.executemany(
            """
            INSERT INTO sources (name, type, description, is_active)
            VALUES (?, ?, ?, ?)
            """,
            [
                ("Uploads CSV (artistas)", "csv", "Uploads manuais de arquivos CSV de streams por artista", 1),
                ("Uploads CSV (dispositivos)", "csv", "Uploads manuais de arquivos CSV de streams por dispositivo", 1),
            ],
        )

    conn.commit()
    conn.close()


def rebuild_indexes():
    """
    Função utilitária para reconstruir índices.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("REINDEX")
    conn.commit()
    conn.close()


def vacuum_db():
    """
    Compacta o banco de dados SQLite.
    """
    conn = get_connection()
    conn.execute("VACUUM")
    conn.close()
