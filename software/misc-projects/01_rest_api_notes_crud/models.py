"""SQLite schema + data access for the notes CRUD API."""

import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL DEFAULT ''
)
"""


def get_connection(db_path):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    conn.commit()
    return conn


def create_note(conn, title, body):
    cur = conn.execute("INSERT INTO notes (title, body) VALUES (?, ?)", (title, body))
    conn.commit()
    return cur.lastrowid


def list_notes(conn, query=None):
    if query:
        rows = conn.execute("SELECT * FROM notes WHERE title LIKE ?", (f"%{query}%",)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM notes").fetchall()
    return [dict(row) for row in rows]


def get_note(conn, note_id):
    row = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    return dict(row) if row else None


def update_note(conn, note_id, title, body):
    cur = conn.execute("UPDATE notes SET title = ?, body = ? WHERE id = ?", (title, body, note_id))
    conn.commit()
    return cur.rowcount > 0


def delete_note(conn, note_id):
    cur = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    return cur.rowcount > 0
