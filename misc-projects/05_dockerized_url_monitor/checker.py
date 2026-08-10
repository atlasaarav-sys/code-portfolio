"""Periodically checks a list of URLs and records results."""

import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

import models


def check_url(url, timeout=5.0):
    """Returns (status_code, latency_ms, error) -- exactly one of
    status_code or error will be meaningful."""
    start = time.perf_counter()
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            latency_ms = (time.perf_counter() - start) * 1000
            return resp.status, latency_ms, None
    except urllib.error.HTTPError as e:
        # A non-2xx response is still a completed request -- record the real
        # status code rather than treating it as a connection failure.
        latency_ms = (time.perf_counter() - start) * 1000
        return e.code, latency_ms, None
    except Exception as e:
        latency_ms = (time.perf_counter() - start) * 1000
        return None, latency_ms, str(e)


def run_check_cycle(conn, urls):
    for url in urls:
        status_code, latency_ms, error = check_url(url)
        checked_at = datetime.now(timezone.utc).isoformat()
        models.record_check(conn, url, checked_at, status_code, latency_ms, error)


def run_checker_loop(conn, urls, interval_seconds=60, stop_event=None):
    while not (stop_event and stop_event.is_set()):
        run_check_cycle(conn, urls)
        time.sleep(interval_seconds)
