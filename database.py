import json
import sqlite3

DB_PATH = "results.db"


def init_db():
    """Létrehozza a results táblát, ha még nem létezik."""
    connection = sqlite3.connect(DB_PATH)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            verdict TEXT NOT NULL,
            stats TEXT NOT NULL,
            checked_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    connection.close()

def save_result(ip: str, verdict: str, stats: dict):
    """Új sorként elmenti az eredményt."""
    connection = sqlite3.connect(DB_PATH)
    connection.execute(
        "INSERT INTO results (ip, verdict, stats) VALUES (?, ?, ?)",
        (ip, verdict, json.dumps(stats)),
    )
    connection.commit()
    connection.close()

def get_latest_result(ip: str):
    """Visszaadja az IP legfrissebb eredményét, vagy None-t."""
    connection = sqlite3.connect(DB_PATH)
    row = connection.execute(
        "SELECT ip, verdict, stats, checked_at FROM results WHERE ip = ? ORDER BY id DESC LIMIT 1",
        (ip,),
    ).fetchone()
    connection.close()

    if row is None:
        return None

    return {
        "ip": row[0],
        "verdict": row[1],
        "stats": json.loads(row[2]),
        "checked_at": row[3],
    }