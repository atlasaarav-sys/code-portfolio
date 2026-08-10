"""URLs to monitor. Edit this list or override via the MONITOR_URLS env var
(comma-separated) at container run time.
"""

import os

DEFAULT_URLS = [
    "https://www.google.com",
    "https://github.com",
    "https://httpbin.org/status/200",
]


def get_monitored_urls():
    env_value = os.environ.get("MONITOR_URLS")
    if env_value:
        return [u.strip() for u in env_value.split(",") if u.strip()]
    return DEFAULT_URLS
