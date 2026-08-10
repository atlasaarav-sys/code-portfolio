"""Fetch multiple feeds, merge, dedupe by link, sort by published date string."""

from feed_parser import fetch, parse_feed, FeedEntry


def aggregate(feed_urls: list[str]) -> list[FeedEntry]:
    all_entries: list[FeedEntry] = []
    for url in feed_urls:
        try:
            xml_text = fetch(url)
            all_entries.extend(parse_feed(xml_text, source_feed=url))
        except Exception as e:
            print(f"Warning: failed to fetch/parse {url}: {e}")

    return dedupe_and_sort(all_entries)


def dedupe_and_sort(entries: list[FeedEntry]) -> list[FeedEntry]:
    seen_links = set()
    deduped = []
    for entry in entries:
        if entry.link and entry.link in seen_links:
            continue
        seen_links.add(entry.link)
        deduped.append(entry)

    # String-sort on `published` works for RFC822/ISO8601 format feeds
    # commonly enough for a demo; a real aggregator would parse to datetime.
    deduped.sort(key=lambda e: e.published, reverse=True)
    return deduped
