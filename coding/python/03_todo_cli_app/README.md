# 03 — Todo CLI App

**Language:** Python 3
**Level:** Advanced (for this track — first "real" application)

## What this demonstrates

- Structuring a small application (`argparse` subcommands, a persistence
  layer, separate module for data model)
- JSON file persistence across runs
- `dataclasses`, type hints, `pathlib`
- Basic unit tests with `unittest`

## Files

- `todo.py` — CLI entry point (add/list/done/remove/clear via subcommands)
- `storage.py` — load/save tasks to `tasks.json` (created at runtime, not
  committed — see `.gitignore`)
- `test_todo.py` — unit tests for the task model and storage layer

## How to run

```bash
python todo.py add "Buy groceries"
python todo.py add "Finish portfolio" --priority high
python todo.py list
python todo.py done 1
python todo.py remove 2
python todo.py list --all
```

Run tests:

```bash
python -m unittest test_todo.py
```

## Notes

`tasks.json` is created next to the script on first run and is
gitignored — each user gets their own local task list.
