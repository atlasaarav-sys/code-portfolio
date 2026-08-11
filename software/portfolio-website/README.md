# Personal Portfolio Website

**Stack:** Single-file HTML/CSS/JS — no build step, no framework, no
dependencies beyond a Google Fonts import (Inter + Space Grotesk).

A dark-themed, minimalistic personal portfolio site with three sections
(Home, About, Projects) and a link out to GitHub.

## Files

- `index.html` — the entire site (markup, styles, and behavior in one file)

## How to run

Just open `index.html` in a browser — no server or build step needed.

```bash
# macOS
open index.html
# Windows
start index.html
# Linux
xdg-open index.html
```

## Deployment

[`.github/workflows/deploy-pages.yml`](../../.github/workflows/deploy-pages.yml)
at the repo root deploys this folder to GitHub Pages automatically on
every push to `main` that touches it, at `https://<username>.github.io/<repo>/`.

## What's in it

- **Home** — name, tagline, one-line hook, contact info, and a prominent
  "View my GitHub" button.
- **About** — degree, a short narrative, technical skills grouped into 5
  categories, and a compact work-experience timeline.
- **Projects** — a 2-column card grid (1-column on mobile) featuring the
  four most recent/impressive projects, each linking directly to its
  folder in this repo on GitHub.
- Sticky nav with smooth-scroll section links and a mobile hamburger menu.
- Scroll-triggered fade/slide-in via `IntersectionObserver`, disabled
  automatically for users with `prefers-reduced-motion: reduce`.

## Notes

- `nav` intentionally uses a solid near-opaque background instead of
  `backdrop-filter: blur()` — a `backdrop-filter` on an ancestor creates a
  new [containing block](https://developer.mozilla.org/en-US/docs/Web/CSS/Containing_block)
  for any `position: fixed` descendant, which broke the mobile menu's
  full-viewport sizing (it was ending up sized relative to the ~60px nav
  bar instead of the screen) — caught and fixed while testing the mobile
  menu in a real browser, not just assumed to work.
- GitHub project links point at
  `github.com/atlasaarav-sys/code-portfolio` — update the username in
  `index.html` if the repo or account changes.
- Live GitHub API fetching for pinned repos was left out on purpose: it's
  optional per the brief, and hardcoded cards mean the site never breaks
  or shows stale/rate-limited data if GitHub's API is unavailable.
