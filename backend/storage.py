from pathlib import Path
import sqlite3

DB_FILE = Path(__file__).resolve().parent / "history.db"


def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        score REAL,
        label TEXT,
        pinyin TEXT,
        created_at TEXT
    )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_history_created ON history(created_at)")
    conn.commit()
    conn.close()



def save_record(record):
    conn = get_conn()
    conn.execute(
        """
        INSERT INTO history
        (text, score, label, pinyin, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            record["text"],
            record["score"],
            record["label"],
            record["pinyin"],
            record["created_at"],
        ),
    )
    conn.commit()
    conn.close()


def get_history(limit: int = 20):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM history ORDER BY created_at DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]