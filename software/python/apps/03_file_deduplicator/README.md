# File Deduplicator

**Stack:** Python 3, stdlib only (`hashlib`, `pathlib`)

Finds duplicate files under a directory by content hash (not filename) —
two-phase for speed: group by file size first (cheap), only hash files
that share a size with at least one other file (expensive but now on a
much smaller set). Defaults to a dry-run report; `--delete` actually
removes duplicates, keeping the first file found in each group.

## Files

- `dedup.py` — the two-phase dedup logic + CLI
- `test_dedup.py` — unit tests using `tempfile`-created fixture files

## How to run

```bash
python dedup.py /path/to/folder              # dry-run report
python dedup.py /path/to/folder --delete      # actually delete duplicates (keeps first found per group)
```

Run tests:

```bash
python -m unittest test_dedup.py
```

## Notes

Size-first grouping means a folder with 10,000 all-different-size files
never gets hashed at all — the expensive SHA-256 pass only runs on files
that already collide on size, which is where duplicates could actually be.
