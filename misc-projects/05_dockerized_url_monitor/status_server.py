"""HTTP status page + JSON API, with the checker running as a background thread."""

import argparse
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import models
from checker import run_checker_loop
from config import get_monitored_urls

DB_PATH = os.path.join(os.path.dirname(__file__), "monitor.db")


class StatusHandler(BaseHTTPRequestHandler):
    conn = None
    urls = []

    def do_GET(self):
        if self.path == "/api/status":
            self._send_json()
        elif self.path == "/" or self.path == "":
            self._send_html()
        else:
            self.send_response(404)
            self.end_headers()

    def _send_json(self):
        statuses = models.latest_check_per_url(self.conn, self.urls)
        body = json.dumps(statuses, indent=2).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self):
        statuses = models.latest_check_per_url(self.conn, self.urls)
        rows = []
        for url, check in statuses.items():
            if check is None:
                rows.append(f"<tr><td>{url}</td><td colspan='3'>no data yet</td></tr>")
                continue
            ok = check["status_code"] and 200 <= check["status_code"] < 400
            color = "green" if ok else "red"
            status_text = check["status_code"] or f"ERROR: {check['error']}"
            rows.append(
                f"<tr><td>{url}</td><td style='color:{color}'>{status_text}</td>"
                f"<td>{check['latency_ms']:.0f} ms</td><td>{check['checked_at']}</td></tr>"
            )

        html = f"""<!doctype html><html><head><title>URL Monitor</title>
<style>body{{font-family:sans-serif;margin:40px}}table{{border-collapse:collapse}}
td,th{{padding:8px;border-bottom:1px solid #ddd}}</style></head><body>
<h1>URL Monitor</h1>
<table><tr><th>URL</th><th>Status</th><th>Latency</th><th>Checked at</th></tr>
{''.join(rows)}</table></body></html>"""

        body = html.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--interval", type=int, default=60, help="seconds between check cycles")
    args = parser.parse_args()

    conn = models.get_connection(DB_PATH)
    urls = get_monitored_urls()

    StatusHandler.conn = conn
    StatusHandler.urls = urls

    checker_thread = threading.Thread(
        target=run_checker_loop, args=(conn, urls, args.interval), daemon=True
    )
    checker_thread.start()

    server = ThreadingHTTPServer(("0.0.0.0", args.port), StatusHandler)
    print(f"Status page on http://localhost:{args.port}, checking {len(urls)} URL(s) every {args.interval}s")
    server.serve_forever()


if __name__ == "__main__":
    main()
