"""Stamp the stylesheet and script links with a content hash.

Run: python3 tools/stamp-assets.py   (after changing CSS or JS)

Why: index.html gets revalidated on reload but /assets/css/style.css does not,
so a browser happily pairs new HTML with a stylesheet from an hour ago. That
looked like broken layout several times over. A hash in the query string means
the URL changes whenever the file does, so a stale copy can never be reused.
"""
import hashlib
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ("index.html", "gallery/index.html", "404.html")
ASSETS = ("/assets/css/style.css", "/assets/js/gallery.js")

versions = {}
for path in ASSETS:
    f = ROOT / path.lstrip("/")
    if f.exists():
        versions[path] = hashlib.sha1(f.read_bytes()).hexdigest()[:8]

for name in PAGES:
    page = ROOT / name
    if not page.exists():
        continue
    html = page.read_text()
    original = html
    for path, ver in versions.items():
        html = re.sub(re.escape(path) + r"(\?v=[0-9a-f]+)?", f"{path}?v={ver}", html)
    if html != original:
        page.write_text(html)
        print(f"stamped {name}")

for path, ver in versions.items():
    print(f"  {path} -> {ver}")
