import json
import os
import sys
import threading
import unittest
import urllib.request
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import models
from status_server import StatusHandler


class TestStatusServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = models.get_connection(":memory:")
        cls.urls = ["https://example.com", "https://broken.example.com"]

        models.record_check(cls.conn, cls.urls[0], datetime.now(timezone.utc).isoformat(), 200, 42.5, None)
        models.record_check(cls.conn, cls.urls[1], datetime.now(timezone.utc).isoformat(), None, 5000.0, "timed out")

        StatusHandler.conn = cls.conn
        StatusHandler.urls = cls.urls

        cls.server = ThreadingHTTPServer(("localhost", 0), StatusHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()

    def test_json_api_returns_latest_status_per_url(self):
        with urllib.request.urlopen(f"http://localhost:{self.port}/api/status") as resp:
            data = json.loads(resp.read())

        self.assertEqual(data["https://example.com"]["status_code"], 200)
        self.assertEqual(data["https://broken.example.com"]["error"], "timed out")

    def test_html_status_page_renders(self):
        with urllib.request.urlopen(f"http://localhost:{self.port}/") as resp:
            html = resp.read().decode()

        self.assertIn("example.com", html)
        self.assertIn("URL Monitor", html)
        self.assertIn("timed out", html)  # error surfaced, not silently dropped


if __name__ == "__main__":
    unittest.main()
