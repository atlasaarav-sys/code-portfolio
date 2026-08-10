# Markdown Static Site Generator

**Stack:** Python 3, stdlib only (no `markdown` package — the converter is
hand-written)

Converts a folder of `.md` files (with optional `key: value` front matter)
into a small styled HTML site: one page per Markdown file plus an
auto-generated index page listing them all.

## Files

- `md_to_html.py` — a from-scratch Markdown-subset converter: headings
  (`#`-`######`), paragraphs, bold/italic, inline code, fenced code
  blocks, links, unordered/ordered lists, blockquotes, horizontal rules
- `site_generator.py` — walks a content directory, parses front matter
  (`---\nkey: value\n---`), renders each page through an HTML template,
  and writes an `index.html` linking all pages
- `content/` — a few example `.md` pages to build from

## How to run

```bash
python site_generator.py content/ output/
```

Then open `output/index.html`.

## Notes

This is a genuine subset of Markdown (no tables, no nested lists, no
reference-style links) — it covers what you'd actually write for a
personal blog/docs site, not the full CommonMark spec.
