import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import models
from checker import check_url, run_check_cycle


class FakeResponse:
    def __init__(self, status):
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class TestChecker(unittest.TestCase):
    def test_check_url_success(self):
        with patch("urllib.request.urlopen", return_value=FakeResponse(200)):
            status, latency, error = check_url("https://example.com")
        self.assertEqual(status, 200)
        self.assertIsNone(error)
        self.assertGreaterEqual(latency, 0)

    def test_check_url_connection_error(self):
        with patch("urllib.request.urlopen", side_effect=OSError("connection refused")):
            status, latency, error = check_url("https://unreachable.example.com")
        self.assertIsNone(status)
        self.assertIn("connection refused", error)

    def test_run_check_cycle_records_results(self):
        conn = models.get_connection(":memory:")
        with patch("urllib.request.urlopen", return_value=FakeResponse(200)):
            run_check_cycle(conn, ["https://example.com", "https://example.org"])

        results = models.latest_check_per_url(conn, ["https://example.com", "https://example.org"])
        self.assertEqual(results["https://example.com"]["status_code"], 200)
        self.assertEqual(results["https://example.org"]["status_code"], 200)

    def test_latest_check_returns_none_for_unchecked_url(self):
        conn = models.get_connection(":memory:")
        results = models.latest_check_per_url(conn, ["https://never-checked.example.com"])
        self.assertIsNone(results["https://never-checked.example.com"])


if __name__ == "__main__":
    unittest.main()
