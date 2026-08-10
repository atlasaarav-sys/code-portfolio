"""Walks a content directory of .md files, converts each to HTML, and
writes a small static site with an auto-generated index.
"""

import argparse
import re
from pathlib import Path

from md_to_html import convert

PAGE_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  body {{ font-family: -apple-system, sans-serif; max-width: 720px; margin: 40px auto; padding: 0 16px; line-height: 1.6; }}
  code {{ background: #f2f2f2; padding: 2px 5px; border-radius: 3px; }}
  pre code {{ display: block; padding: 12px; overflow-x: auto; }}
  a {{ color: #0969da; }}
  nav a {{ margin-right: 12px; }}
</style>
</head>
<body>
<nav><a href="index.html">Home</a></nav>
<h1>{title}</h1>
{body}
</body>
</html>
"""

INDEX_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  body {{ font-family: -apple-system, sans-serif; max-width: 720px; margin: 40px auto; padding: 0 16px; line-height: 1.6; }}
  li {{ margin: 8px 0; }}
</style>
</head>
<body>
<h1>{title}</h1>
<ul>
{links}
</ul>
</body>
</html>
"""


def parse_front_matter(text: str) -> tuple[dict, str]:
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not match:
        return {}, text
    meta = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta, match.group(2)


def build_site(content_dir: Path, output_dir: Path, site_title: str = "My Site"):
    output_dir.mkdir(parents=True, exist_ok=True)
    pages = []

    for md_path in sorted(content_dir.glob("*.md")):
        text = md_path.read_text(encoding="utf-8")
        meta, body_md = parse_front_matter(text)
        title = meta.get("title", md_path.stem.replace("_", " ").title())

        body_html = convert(body_md)
        page_html = PAGE_TEMPLATE.format(title=title, body=body_html)

        out_path = output_dir / (md_path.stem + ".html")
        out_path.write_text(page_html, encoding="utf-8")
        pages.append((title, out_path.name, meta.get("date", "")))

    links = "\n".join(
        f'  <li><a href="{filename}">{title}</a>{f" — {date}" if date else ""}</li>'
        for title, filename, date in pages
    )
    index_html = INDEX_TEMPLATE.format(title=site_title, links=links)
    (output_dir / "index.html").write_text(index_html, encoding="utf-8")

    return pages


def main():
    parser = argparse.ArgumentParser(description="Build a static site from a folder of Markdown files")
    parser.add_argument("content_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--title", default="My Site")
    args = parser.parse_args()

    pages = build_site(args.content_dir, args.output_dir, args.title)
    print(f"Built {len(pages)} page(s) into {args.output_dir}/")
    for title, filename, _ in pages:
        print(f"  {filename}  ({title})")


if __name__ == "__main__":
    main()
