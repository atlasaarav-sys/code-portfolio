# URL Shortener Service

**Stack:** Python 3, `http.server` + `sqlite3` (stdlib only, no Flask/Django)

A small REST API: `POST /shorten` with a JSON body to create a short code,
`GET /<code>` to redirect to the original URL, `GET /stats/<code>` for hit
counts. Persists to SQLite so short links survive a restart.

## Files

- `shortener_server.py` — `http.server.BaseHTTPRequestHandler` subclass
  implementing the three routes + SQLite storage
- `test_shortener.py` — starts the server on a background thread on an
  ephemeral port and drives it with real HTTP requests (`urllib`)

## How to run

```bash
python shortener_server.py --port 8080
```

Then, from another terminal:

```bash
curl -X POST http://localhost:8080/shorten -d '{"url": "https://example.com/very/long/path"}'
# -> {"code": "a1b2c3", "short_url": "http://localhost:8080/a1b2c3"}

curl -i http://localhost:8080/a1b2c3
# -> 302 redirect to https://example.com/very/long/path

curl http://localhost:8080/stats/a1b2c3
# -> {"url": "...", "hits": 1, "created": "..."}
```

Run tests (spins up the server itself, no manual steps needed):

```bash
python -m unittest test_shortener.py
```

## Notes

Short codes are 6-character base62, generated from a counter + salt
hashed with SHA-256 (deterministic-but-unpredictable, not random —
avoids a collision-retry loop). `shortener.db` is created next to the
script at runtime and gitignored.
