from pathlib import Path
from contextlib import contextmanager
import sqlite3
from datetime import datetime

# Banco em app\music_insights.db
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
    # A pasta app já existe, mas não custa garantir
    DB_PATH.parent.mkdir(exist_ok=True)

    with get_db() as conn:
        cur = conn.cursor()

        # Usuários (simples, só pra não quebrar auth)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
            """
        )

        # Fontes (origens) de dados
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

        # Ingestões (uploads)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS ingestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER NOT NULL,
                file_name TEXT NOT NULL,
                ingested_at TEXT NOT NULL,
                total_rows INTEGER NOT NULL,
                FOREIGN KEY (source_id) REFERENCES sources(id)
            )
            """
        )

        # Detalhamento de streams (ESTA É A TABELA QUE OS RELATÓRIOS USAM)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS stream_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingestion_id INTEGER NOT NULL,
                artist_name TEXT NOT NULL,
                track_title TEXT,
                isrc TEXT,
                upc TEXT,
                platform TEXT,
                country TEXT,
                stream_date TEXT,
                streams INTEGER,
                FOREIGN KEY (ingestion_id) REFERENCES ingestions(id)
            )
            """
        )

        # Seed de fontes, se ainda não houver nada
        cur.execute("SELECT COUNT(*) AS cnt FROM sources")
        count = cur.fetchone()["cnt"]

        if count == 0:
            cur.executemany(
                """
                INSERT INTO sources (name, type, description, is_active)
                VALUES (?, ?, ?, ?)
                """,
                [
                    (
                        "FUGA - Analytics streams by asset",
                        "csv",
                        "Uploads CSV de streams por artista (FUGA)",
                        1,
                    ),
                    (
                        "Device logs",
                        "csv",
                        "Uploads CSV de dispositivos / players",
                        1,
                    ),
                ],
            )
