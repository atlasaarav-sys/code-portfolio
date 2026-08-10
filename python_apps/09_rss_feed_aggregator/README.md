# RSS Feed Aggregator

**Stack:** Python 3, stdlib only (`urllib.request`, `xml.etree.ElementTree`)

Fetches a list of RSS/Atom feed URLs, parses entries (handling both RSS
2.0's `<item>` and Atom's `<entry>` formats), dedupes by link, sorts by
publish date, and prints/exports a unified feed.

## Files

- `feed_parser.py` — feed fetching (`urllib.request`) + parsing for both
  RSS 2.0 and Atom, normalized to a common `FeedEntry` shape
- `aggregator.py` — fetches multiple feeds, merges + dedupes + sorts
- `main.py` — CLI: reads a list of feed URLs from a file, prints the
  aggregated, sorted result (optionally as JSON)
- `test_feed_parser.py` — parses inline RSS and Atom XML fixtures (no
  network access needed for the test) and checks the normalized output

## How to run

```bash
python main.py feeds.txt              # one feed URL per line
python main.py feeds.txt --json > out.json
```

Run tests (pure parsing logic, no network):

```bash
python -m unittest test_feed_parser.py
```

## Notes

Feed fetching (`urllib.request.urlopen`) requires network access and isn't
exercised by the test suite — the parser itself (the part with actual
logic worth testing) is tested against inline XML fixtures instead of
live feeds, so tests are deterministic and don't depend on network
availability.
