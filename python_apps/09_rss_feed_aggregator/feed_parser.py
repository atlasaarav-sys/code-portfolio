"""Fetches and parses RSS 2.0 / Atom feeds into a normalized shape."""

import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass

ATOM_NS = "{http://www.w3.org/2005/Atom}"


@dataclass
class FeedEntry:
    title: str
    link: str
    published: str  # raw string as given by the feed; not parsed to datetime to avoid a dependency
    source_feed: str = ""


def fetch(url: str, timeout: float = 10.0) -> str:
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_feed(xml_text: str, source_feed: str = "") -> list[FeedEntry]:
    root = ET.fromstring(xml_text)

    if root.tag == f"{ATOM_NS}feed":
        return _parse_atom(root, source_feed)
    return _parse_rss(root, source_feed)


def _parse_rss(root: ET.Element, source_feed: str) -> list[FeedEntry]:
    entries = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        published = (item.findtext("pubDate") or "").strip()
        entries.append(FeedEntry(title, link, published, source_feed))
    return entries


def _parse_atom(root: ET.Element, source_feed: str) -> list[FeedEntry]:
    entries = []
    for entry in root.findall(f"{ATOM_NS}entry"):
        title = (entry.findtext(f"{ATOM_NS}title") or "").strip()
        link_el = entry.find(f"{ATOM_NS}link")
        link = link_el.get("href", "") if link_el is not None else ""
        published = (entry.findtext(f"{ATOM_NS}published") or entry.findtext(f"{ATOM_NS}updated") or "").strip()
        entries.append(FeedEntry(title, link, published, source_feed))
    return entries
