"""SQLite schema + data access for the bookmarks app."""

import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""


def get_connection(db_path):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def create_user(conn, username, password_hash):
    cur = conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
    conn.commit()
    return cur.lastrowid


def get_user_by_username(conn, username):
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    return dict(row) if row else None


def get_user_by_id(conn, user_id):
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return dict(row) if row else None


def add_bookmark(conn, user_id, title, url):
    cur = conn.execute("INSERT INTO bookmarks (user_id, title, url) VALUES (?, ?, ?)", (user_id, title, url))
    conn.commit()
    return cur.lastrowid


def list_bookmarks(conn, user_id):
    rows = conn.execute("SELECT * FROM bookmarks WHERE user_id = ?", (user_id,)).fetchall()
    return [dict(row) for row in rows]


def delete_bookmark(conn, user_id, bookmark_id):
    # Scoped by user_id, not just id -- this is what prevents user A from
    # deleting user B's bookmark by guessing/incrementing an ID.
    cur = conn.execute("DELETE FROM bookmarks WHERE id = ? AND user_id = ?", (bookmark_id, user_id))
    conn.commit()
    return cur.rowcount > 0
