import unittest

from feed_parser import parse_feed
from aggregator import dedupe_and_sort

RSS_SAMPLE = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
  <title>Example RSS Feed</title>
  <item>
    <title>First Post</title>
    <link>https://example.com/first</link>
    <pubDate>Mon, 05 Jan 2026 10:00:00 GMT</pubDate>
  </item>
  <item>
    <title>Second Post</title>
    <link>https://example.com/second</link>
    <pubDate>Tue, 06 Jan 2026 10:00:00 GMT</pubDate>
  </item>
</channel>
</rss>
"""

ATOM_SAMPLE = """<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example Atom Feed</title>
  <entry>
    <title>Atom Entry One</title>
    <link href="https://example.com/atom-one"/>
    <published>2026-01-07T10:00:00Z</published>
  </entry>
</feed>
"""


class TestFeedParser(unittest.TestCase):
    def test_parse_rss(self):
        entries = parse_feed(RSS_SAMPLE, source_feed="rss.xml")
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].title, "First Post")
        self.assertEqual(entries[0].link, "https://example.com/first")
        self.assertEqual(entries[0].source_feed, "rss.xml")

    def test_parse_atom(self):
        entries = parse_feed(ATOM_SAMPLE, source_feed="atom.xml")
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].title, "Atom Entry One")
        self.assertEqual(entries[0].link, "https://example.com/atom-one")

    def test_dedupe_by_link(self):
        entries = parse_feed(RSS_SAMPLE) + parse_feed(RSS_SAMPLE)  # simulate duplicate fetch
        deduped = dedupe_and_sort(entries)
        self.assertEqual(len(deduped), 2)

    def test_sort_by_published_descending(self):
        entries = parse_feed(RSS_SAMPLE)
        sorted_entries = dedupe_and_sort(entries)
        self.assertEqual(sorted_entries[0].title, "Second Post")  # later date first


if __name__ == "__main__":
    unittest.main()
