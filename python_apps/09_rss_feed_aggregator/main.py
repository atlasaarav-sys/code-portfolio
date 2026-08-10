import argparse
import json
from dataclasses import asdict

from aggregator import aggregate


def main():
    parser = argparse.ArgumentParser(description="Aggregate RSS/Atom feeds")
    parser.add_argument("feed_list_file", help="text file, one feed URL per line")
    parser.add_argument("--json", action="store_true", help="output as JSON instead of plain text")
    args = parser.parse_args()

    with open(args.feed_list_file) as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    entries = aggregate(urls)

    if args.json:
        print(json.dumps([asdict(e) for e in entries], indent=2))
    else:
        for e in entries:
            print(f"[{e.published}] {e.title}")
            print(f"  {e.link}")


if __name__ == "__main__":
    main()
