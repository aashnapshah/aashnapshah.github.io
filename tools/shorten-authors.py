"""Shorten long author lists on aashna-shah.com.

Run: python3 tools/shorten-authors.py

What it does
- Rewrites each `.pub-item__authors` line to: first two … me … last two.
- Keeps the full list, markup and all, in `data-authors`, so nothing is lost.
- Only shortens when that hides at least three names. Short lists stay whole.
- Safe to rerun: it reads the full list back out of `data-authors`.

Adding a paper: paste the full author list into index.html as usual, then
rerun this.
"""

import html
import pathlib
import re

ME = "Aashna P. Shah"
GAP = "…"
MIN_HIDDEN = 3          # below this, shortening is not worth the gap

AUTHORS_RE = re.compile(
    r'<div class="pub-item__authors"(?P<attrs>[^>]*)>(?P<body>.*?)</div>', re.S
)
STORED_RE = re.compile(r'\s*data-authors="(?P<full>[^"]*)"')


def shorten(full):
    """Return the shortened author list, or the full one if it is short."""
    authors = full.split(", ")
    keep = {0, 1, len(authors) - 2, len(authors) - 1}
    keep |= {i for i, a in enumerate(authors) if ME in a}
    keep = sorted(i for i in keep if 0 <= i < len(authors))
    if len(authors) - len(keep) < MIN_HIDDEN:
        return full

    # Names are separated by a comma; a gap gets a space on both sides, so the
    # ellipsis reads as a break rather than as another name.
    out, previous = "", None
    for i in keep:
        if previous is None:
            pass
        elif i > previous + 1:
            out += f" {GAP} "
        else:
            out += ", "
        out += authors[i]
        previous = i
    return out


def rewrite(match):
    attrs, body = match.group("attrs"), match.group("body")
    # A previous run stored the full list; prefer it over the shortened body.
    stored = STORED_RE.search(attrs)
    full = html.unescape(stored.group("full")) if stored else body
    attrs = STORED_RE.sub("", attrs)

    short = shorten(full)
    if short == full:
        return f'<div class="pub-item__authors"{attrs}>{full}</div>'
    kept = html.escape(full, quote=True)
    return f'<div class="pub-item__authors"{attrs} data-authors="{kept}">{short}</div>'


site = pathlib.Path(__file__).resolve().parent.parent / "index.html"
page = site.read_text()
page, count = AUTHORS_RE.subn(rewrite, page)
site.write_text(page)
print(f"rewrote {count} author lists")
