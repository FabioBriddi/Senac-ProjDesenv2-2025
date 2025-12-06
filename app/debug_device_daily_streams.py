from pathlib import Path
import sqlite3

# Caminho do banco: app\music_insights.db
DB_PATH = Path(__file__).resolve().parent / "music_insights.db"

def main():
    print(f"Usando banco em: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Mostra os primeiros registros salvos na tabela de dispositivos
    print("\n=== PRIMEIROS REGISTROS EM device_daily_streams ===\n")
    try:
        cur.execute(
            """
            SELECT
                ingestion_id,
                distributor,
                device_name,
                day_label,
                streams
            FROM device_daily_streams
            ORDER BY ingestion_id, device_name, day_label
            LIMIT 50
            """
        )
    except sqlite3.OperationalError as e:
        print(f"Erro ao consultar device_daily_streams: {e}")
        conn.close()
        return

    rows = cur.fetchall()
    if not rows:
        print("Nenhum registro encontrado em device_daily_streams.")
    else:
        for r in rows:
            print(
                f"ingestion={r['ingestion_id']}, "
                f"dist={r['distributor']}, "
                f"device={r['device_name']}, "
                f"dia={r['day_label']}, "
                f"streams={r['streams']}"
            )

    conn.close()


if __name__ == "__main__":
    main()
