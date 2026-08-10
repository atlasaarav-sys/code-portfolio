"""SQLite storage for URL check results."""

import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    checked_at TEXT NOT NULL,
    status_code INTEGER,
    latency_ms REAL,
    error TEXT
)
"""


def get_connection(db_path):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    conn.commit()
    return conn


def record_check(conn, url, checked_at, status_code=None, latency_ms=None, error=None):
    conn.execute(
        "INSERT INTO checks (url, checked_at, status_code, latency_ms, error) VALUES (?, ?, ?, ?, ?)",
        (url, checked_at, status_code, latency_ms, error),
    )
    conn.commit()


def latest_check_per_url(conn, urls):
    results = {}
    for url in urls:
        row = conn.execute(
            "SELECT * FROM checks WHERE url = ? ORDER BY id DESC LIMIT 1", (url,)
        ).fetchone()
        results[url] = dict(row) if row else None
    return results
