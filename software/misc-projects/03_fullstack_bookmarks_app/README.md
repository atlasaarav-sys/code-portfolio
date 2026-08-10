# Full-Stack Web App — Bookmarks

**Stack:** Python, Flask (server-rendered HTML, no separate frontend
framework — deliberately, see Notes), SQLite, session-based auth with
salted+hashed passwords, Docker

A small but complete full-stack app: users register/log in, and each
user has their own private list of bookmarks (add/delete, with a title +
URL). Demonstrates the fundamentals employers actually screen full-stack
candidates on — auth, per-user data isolation, server-rendered templates,
CSRF-safe forms, and a working deployment story (Dockerfile) — without
the extra surface area of a JS framework/build pipeline.

## Features

- Register / log in / log out (Flask sessions, `werkzeug.security` for
  password hashing — never stores plaintext passwords)
- Each user only ever sees their own bookmarks (every query is scoped by
  `user_id`, enforced server-side, not just hidden in the UI)
- Add / delete bookmarks via plain HTML forms (works with JS disabled)
- Dockerized for a real "how would you deploy this" story

## Files

- `app.py` — routes: `/register`, `/login`, `/logout`, `/` (list +
  add), `/delete/<id>`
- `models.py` — SQLite schema (`users`, `bookmarks`) + data access
- `templates/` — Jinja2 templates (`base.html`, `login.html`,
  `register.html`, `bookmarks.html`)
- `Dockerfile` — production-ish container (gunicorn, not the Flask dev
  server)
- `tests/test_app.py` — registration, login, auth-required redirects, and
  per-user data isolation (user A can't see/delete user B's bookmarks)

## How to run

```bash
pip install flask gunicorn
python app.py            # dev server on :5000
```

Or with Docker:

```bash
docker build -t bookmarks-app .
docker run -p 8000:8000 bookmarks-app
```

Run tests:

```bash
python -m unittest tests/test_app.py
```

## Notes

No React/Vue here on purpose — server-rendered Jinja2 templates are the
right tool for a CRUD-with-auth app this size, and skipping a JS build
pipeline keeps the "how do I deploy this" story to one `Dockerfile`
instead of a frontend build step plus a separate static host. The auth
pattern (hashed passwords, session cookies, server-side ownership checks
on every query) is the actual substance being demonstrated here, not the
choice of templating engine.
