# CLI Tool — Git Changelog Generator

**Stack:** Python 3, stdlib only (`subprocess`, `re`, `argparse`)

Generates a grouped `CHANGELOG.md` from git history by parsing Conventional
Commits (`feat:`, `fix:`, `docs:`, etc.) out of `git log` — the actual
annoyance this solves: writing a changelog by hand before a release, or
re-reading `git log` trying to remember what changed.

## What it does

1. Runs `git log` between two refs (default: last tag -> `HEAD`, or a
   full range you specify) and parses each commit's subject line.
2. Buckets commits by [Conventional Commits](https://www.conventionalcommits.org/)
   type (`feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `other`).
3. Renders a Markdown changelog grouped by type, each entry linking to its
   commit hash, in the same format GitHub/GitLab release notes typically
   use.

## Files

- `changelog.py` — git log parsing + Conventional Commit categorization +
  Markdown rendering, plus the CLI entry point
- `tests/test_changelog.py` — tests the parsing/categorization logic
  against literal commit-line fixtures (no real git repo required, so
  tests are deterministic)

## How to run

```bash
# From inside any git repo:
python /path/to/changelog.py --from v1.0.0 --to HEAD --output CHANGELOG.md

# Or just the last N commits, no tag needed:
python /path/to/changelog.py --last 20
```

Run tests:

```bash
python -m unittest tests/test_changelog.py
```

## Notes

Commits that don't follow the `type: subject` or `type(scope): subject`
convention land in an "Other" bucket rather than being dropped — a real
repo's history is never 100% conventional, and silently discarding
non-conforming commits would make the changelog wrong in exactly the way
you wouldn't notice.
