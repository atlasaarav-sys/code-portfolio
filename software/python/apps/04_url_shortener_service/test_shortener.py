import http.client
import json
import threading
import unittest
import urllib.error
import urllib.request

from shortener_server import run_server


class TestShortenerService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = run_server(port=0, db_path=":memory:")  # ephemeral port
        cls.port = cls.server.server_address[1]
        cls.base_url = f"http://localhost:{cls.port}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()

    def shorten(self, url):
        req = urllib.request.Request(
            f"{self.base_url}/shorten",
            data=json.dumps({"url": url}).encode(),
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())

    def raw_get(self, path):
        """GET without following redirects, using http.client directly."""
        conn = http.client.HTTPConnection("localhost", self.port)
        conn.request("GET", path)
        resp = conn.getresponse()
        status, headers, body = resp.status, dict(resp.getheaders()), resp.read()
        conn.close()
        return status, headers, body

    def test_shorten_and_redirect(self):
        result = self.shorten("https://example.com/some/long/path")
        self.assertIn("code", result)

        status, headers, _ = self.raw_get(f"/{result['code']}")
        self.assertEqual(status, 302)
        self.assertEqual(headers["Location"], "https://example.com/some/long/path")

    def test_unknown_code_404(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(f"{self.base_url}/doesnotexist")
        self.assertEqual(ctx.exception.code, 404)

    def test_stats_tracks_hits(self):
        result = self.shorten("https://example.com/stats-test")
        code = result["code"]

        for _ in range(3):
            self.raw_get(f"/{code}")

        with urllib.request.urlopen(f"{self.base_url}/stats/{code}") as resp:
            stats = json.loads(resp.read())
        self.assertEqual(stats["hits"], 3)

    def test_invalid_url_returns_400(self):
        req = urllib.request.Request(
            f"{self.base_url}/shorten",
            data=json.dumps({"url": "not-a-url"}).encode(),
            method="POST",
        )
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req)
        self.assertEqual(ctx.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
