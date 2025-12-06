import sqlite3

conn = sqlite3.connect("app/music_insights.db")
conn.execute("""
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
""")
conn.execute("CREATE INDEX IF NOT EXISTS idx_api_connectors_name ON api_connectors (name)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_api_connectors_active ON api_connectors (is_active)")
conn.commit()
conn.close()
print("Tabela criada!")
