"""Minimal REST URL shortener service, stdlib only."""

import argparse
import hashlib
import json
import sqlite3
import string
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_DB = Path(__file__).parent / "shortener.db"
BASE62 = string.digits + string.ascii_lowercase + string.ascii_uppercase


def get_connection(db_path=DEFAULT_DB):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS links (
            code TEXT PRIMARY KEY,
            url TEXT NOT NULL,
            created TEXT NOT NULL,
            hits INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    return conn


def generate_code(url: str, counter: int, length: int = 6) -> str:
    digest = hashlib.sha256(f"{url}:{counter}:{time.time()}".encode()).digest()
    n = int.from_bytes(digest[:8], "big")
    code_chars = []
    for _ in range(length):
        code_chars.append(BASE62[n % 62])
        n //= 62
    return "".join(code_chars)


class ShortenerHandler(BaseHTTPRequestHandler):
    conn: sqlite3.Connection = None  # set by main()
    counter = [0]

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/shorten":
            self._send_json(404, {"error": "not found"})
            return

        length = int(self.headers.get("Content-Length", 0))
        try:
            data = json.loads(self.rfile.read(length))
            url = data["url"]
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError("invalid URL")
        except (json.JSONDecodeError, KeyError, ValueError):
            self._send_json(400, {"error": "expected JSON body with a valid 'url' field"})
            return

        ShortenerHandler.counter[0] += 1
        code = generate_code(url, ShortenerHandler.counter[0])

        self.conn.execute(
            "INSERT INTO links (code, url, created, hits) VALUES (?, ?, ?, 0)",
            (code, url, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())),
        )
        self.conn.commit()

        host = self.headers.get("Host", "localhost")
        self._send_json(201, {"code": code, "short_url": f"http://{host}/{code}"})

    def do_GET(self):
        if self.path.startswith("/stats/"):
            code = self.path[len("/stats/"):]
            row = self.conn.execute("SELECT url, hits, created FROM links WHERE code = ?", (code,)).fetchone()
            if not row:
                self._send_json(404, {"error": "unknown code"})
                return
            self._send_json(200, {"url": row[0], "hits": row[1], "created": row[2]})
            return

        code = self.path.lstrip("/")
        if not code:
            self._send_json(200, {"status": "ok", "message": "URL shortener running"})
            return

        row = self.conn.execute("SELECT url FROM links WHERE code = ?", (code,)).fetchone()
        if not row:
            self._send_json(404, {"error": "unknown code"})
            return

        self.conn.execute("UPDATE links SET hits = hits + 1 WHERE code = ?", (code,))
        self.conn.commit()

        self.send_response(302)
        self.send_header("Location", row[0])
        self.end_headers()

    def log_message(self, format, *args):
        pass  # keep test/demo output quiet


def run_server(port: int, db_path=DEFAULT_DB):
    ShortenerHandler.conn = get_connection(db_path)
    server = ThreadingHTTPServer(("localhost", port), ShortenerHandler)
    print(f"URL shortener listening on http://localhost:{port}")
    return server


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    server = run_server(args.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
