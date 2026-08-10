"""A hand-written subset-of-Markdown -> HTML converter (no external deps)."""

import html
import re

INLINE_PATTERNS = [
    (re.compile(r"\*\*(.+?)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"\*(.+?)\*"), r"<em>\1</em>"),
    (re.compile(r"`(.+?)`"), r"<code>\1</code>"),
    (re.compile(r"\[(.+?)\]\((.+?)\)"), r'<a href="\2">\1</a>'),
]


def render_inline(text: str) -> str:
    text = html.escape(text, quote=False)
    # html.escape turns '&' in "&amp;" pattern-safe, but we still want our
    # own markup below to use raw <>, so escape first then apply patterns.
    for pattern, repl in INLINE_PATTERNS:
        text = pattern.sub(repl, text)
    return text


def convert(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    html_parts = []
    i = 0
    in_list = None  # "ul" or "ol" or None
    in_blockquote = False

    def close_list():
        nonlocal in_list
        if in_list:
            html_parts.append(f"</{in_list}>")
            in_list = None

    def close_blockquote():
        nonlocal in_blockquote
        if in_blockquote:
            html_parts.append("</blockquote>")
            in_blockquote = False

    while i < len(lines):
        line = lines[i]

        # Fenced code block
        if line.strip().startswith("```"):
            close_list()
            close_blockquote()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            code = html.escape("\n".join(code_lines))
            html_parts.append(f"<pre><code>{code}</code></pre>")
            i += 1
            continue

        # Horizontal rule
        if re.match(r"^-{3,}$", line.strip()):
            close_list()
            close_blockquote()
            html_parts.append("<hr>")
            i += 1
            continue

        # Headings
        heading_match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading_match:
            close_list()
            close_blockquote()
            level = len(heading_match.group(1))
            html_parts.append(f"<h{level}>{render_inline(heading_match.group(2))}</h{level}>")
            i += 1
            continue

        # Blockquote
        if line.startswith(">"):
            if not in_blockquote:
                close_list()
                html_parts.append("<blockquote>")
                in_blockquote = True
            content = line.lstrip(">").strip()
            html_parts.append(f"<p>{render_inline(content)}</p>")
            i += 1
            continue
        else:
            close_blockquote()

        # Unordered list
        ul_match = re.match(r"^[-*]\s+(.*)$", line)
        if ul_match:
            if in_list != "ul":
                close_list()
                html_parts.append("<ul>")
                in_list = "ul"
            html_parts.append(f"<li>{render_inline(ul_match.group(1))}</li>")
            i += 1
            continue

        # Ordered list
        ol_match = re.match(r"^\d+\.\s+(.*)$", line)
        if ol_match:
            if in_list != "ol":
                close_list()
                html_parts.append("<ol>")
                in_list = "ol"
            html_parts.append(f"<li>{render_inline(ol_match.group(1))}</li>")
            i += 1
            continue

        close_list()

        # Blank line -> paragraph break (no-op, just skip)
        if line.strip() == "":
            i += 1
            continue

        # Paragraph: collect until blank line or a block-starting line
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() != "" and not re.match(
            r"^(#{1,6}\s|[-*]\s|\d+\.\s|>|```|-{3,}$)", lines[i]
        ):
            para_lines.append(lines[i])
            i += 1
        html_parts.append(f"<p>{render_inline(' '.join(para_lines))}</p>")

    close_list()
    close_blockquote()
    return "\n".join(html_parts)
