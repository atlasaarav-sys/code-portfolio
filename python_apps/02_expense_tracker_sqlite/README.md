# Expense Tracker (SQLite)

**Stack:** Python 3, `sqlite3` (stdlib)

CLI expense tracker backed by a real SQLite database: add expenses with a
category and date, list/filter them, and generate a monthly summary report
grouped by category.

## Files

- `expense_tracker.py` — CLI (`add`, `list`, `report`, `delete`) + all
  SQLite access (schema creation, parameterized queries)
- `test_expense_tracker.py` — unit tests against a temp database

## How to run

```bash
python expense_tracker.py add 42.50 groceries --date 2026-01-15 --note "weekly shop"
python expense_tracker.py add 15.00 transport --date 2026-01-16
python expense_tracker.py list
python expense_tracker.py report --month 2026-01
python expense_tracker.py delete 1
```

Run tests:

```bash
python -m unittest test_expense_tracker.py
```

## Notes

Database file defaults to `expenses.db` next to the script (gitignored —
it's local user data, not source content). All queries are parameterized
(`?` placeholders) — no string-formatted SQL.
