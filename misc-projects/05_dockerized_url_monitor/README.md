# Dockerized URL Health Monitor + CI/CD

**Stack:** Python, `http.server` + `urllib` (stdlib only), SQLite, Docker,
GitHub Actions

A small uptime monitor: periodically checks a configurable list of URLs,
records status code + latency to SQLite, and serves a live status page —
containerized, with a GitHub Actions workflow that runs the test suite and
builds the Docker image on every push. This is the "DevOps awareness"
entry in the misc-projects set: the point isn't the monitor itself, it's
having a real, working CI/CD pipeline attached to it.

## What it does

- `checker.py` — background loop: `GET`/`HEAD`s each configured URL,
  records `(url, timestamp, status_code, latency_ms, error)` to SQLite
- `status_server.py` — `http.server`-based status page (`/`) showing the
  latest check per URL plus a JSON API (`/api/status`) for scripting
- `Dockerfile` — runs both the checker loop and status server in one
  container (checker as a background thread inside the server process,
  simplest correct option for a single-container demo)
- `.github/workflows/ci.yml` (at the repo root, scoped to this project via
  a `paths:` filter) — on every push touching this project: installs deps,
  runs the test suite, then builds the Docker image to confirm it still
  builds cleanly

## Files

- `checker.py`, `status_server.py`, `models.py`, `config.py`
- `Dockerfile`, `requirements.txt` (stdlib only, so this file only pins
  the Python version constraint — no third-party packages needed)
- `tests/test_checker.py`, `tests/test_status_server.py`

## How to run

```bash
pip install -r requirements.txt
python status_server.py --port 8080   # runs the checker loop + status page together
```

Or with Docker:

```bash
docker build -t url-monitor .
docker run -p 8080:8080 url-monitor
```

Then visit `http://localhost:8080` for the status page or
`http://localhost:8080/api/status` for JSON.

Run tests:

```bash
python -m unittest discover tests
```

## CI/CD pipeline

See [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) at the
repo root. It triggers on pushes/PRs touching
`misc-projects/05_dockerized_url_monitor/**`, and runs two jobs: `test`
(Python 3.12, `python -m unittest discover tests`) and `docker-build`
(builds the image with `docker build .`, doesn't push anywhere — proving
the image builds is the point for a portfolio pipeline, not standing up a
registry).

## Notes

The checker records failures (timeouts, connection errors, non-2xx
status) as real rows rather than skipping them — an uptime monitor that
silently drops failed checks defeats its own purpose.
