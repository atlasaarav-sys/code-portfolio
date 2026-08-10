# REST API — Notes CRUD

**Stack:** Python, Flask, SQLite, `pytest`-style tests via `unittest`

A small but complete REST API: full CRUD (Create/Read/Update/Delete) on a
`notes` resource, backed by SQLite, with proper HTTP status codes
(201/200/204/404/400), JSON error responses, and a test suite that
exercises the API through Flask's test client (no server process needed
to run tests).

## Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/notes` | Create a note (`{"title": "...", "body": "..."}`) -> 201 |
| `GET` | `/notes` | List all notes, optional `?q=` substring filter on title |
| `GET` | `/notes/<id>` | Fetch one note -> 200 or 404 |
| `PUT` | `/notes/<id>` | Replace a note's title/body -> 200 or 404 |
| `DELETE` | `/notes/<id>` | Delete a note -> 204 or 404 |

## Files

- `app.py` — Flask app + route handlers
- `models.py` — SQLite schema + data access functions (parameterized
  queries throughout)
- `tests/test_api.py` — full CRUD lifecycle test + edge cases (404 on
  missing note, 400 on malformed body)

## How to run

```bash
pip install flask
python app.py
```

```bash
curl -X POST localhost:5000/notes -H "Content-Type: application/json" -d '{"title":"Buy milk","body":"2%"}'
curl localhost:5000/notes
curl localhost:5000/notes/1
curl -X PUT localhost:5000/notes/1 -H "Content-Type: application/json" -d '{"title":"Buy milk","body":"whole milk"}'
curl -X DELETE localhost:5000/notes/1
```

Run tests:

```bash
python -m unittest tests/test_api.py
```

## Notes

`notes.db` is created next to `app.py` at runtime and is gitignored — it's
local state, not source content. Tests use an in-memory SQLite database
(`:memory:`), so they never touch the real data file.
