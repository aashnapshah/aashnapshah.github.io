"""Process the Acknowledgements album and rebuild the gallery page.

Run: python3 tools/build-gallery.py

What it does, per photo:
- honours the EXIF orientation flag, so nothing shows up sideways
- crops extreme aspect ratios back to something that sits well in a masonry
  column, centring the crop on detected faces when there are any
- resizes to 900px on the long side and saves JPEG without EXIF, which also
  strips GPS coordinates -- these are personal photos going on a public site
- writes every photo, old and new, shuffled into gallery/index.html

The shuffle uses a fixed seed so re-running gives the same order.
"""
import pathlib
import json
import random
import re
import sys
import unicodedata
from datetime import datetime

import cv2
import numpy as np
from PIL import Image, ImageOps

ALBUM = pathlib.Path.home() / "Desktop/Acknowledgements"
FEATURED_DIR = ALBUM / "_featured"
FEATURED_LIST = pathlib.Path(__file__).resolve().parent / "gallery-featured.txt"
SCORES = pathlib.Path(__file__).resolve().parent / "photo-scores.json"
META = pathlib.Path(__file__).resolve().parent / "photo-meta.json"
REMOVE_LIST = pathlib.Path(__file__).resolve().parent / "gallery-remove.txt"

# The days worth leading with, best first. Taken from EXIF capture dates.
KEY_DATES = ["2026-05-01",   # thesis defense
             "2026-05-27",   # commencement
             "2026-05-28",   # commencement, day two
             "2026-05-02"]   # defense party
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/img/gallery/album"
PAGE = ROOT / "gallery/index.html"

LONG_SIDE = 900
QUALITY = 80
MAX_LANDSCAPE = 1.5      # anything wider gets trimmed
MIN_PORTRAIT = 0.72      # anything taller gets trimmed
SEED = 20260924
LEAD = 20          # how many photos get the big block at the top

# Automatic culling. Numbers picked off the actual distributions, not guessed:
# sharpness has a median of 641, so 70 only catches the genuinely smeared;
# 640px catches the handful whose originals were tiny to begin with.
MIN_LONG_SIDE = 640    # web copy is capped at 900, so under this the source was small
MIN_SHARPNESS = 70     # variance of the Laplacian; low means blurry
GROUP_SPARE = 4        # a crowd this size is kept even if she is not recognised,
                       # because face matching gets unreliable on small distant faces
ALWAYS_KEEP = ("milo-",)   # Milo gets in on his own merits

CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def gps(exif):
    """(lat, lon) in degrees from the EXIF GPS block, or None."""
    info = exif.get(34853)
    if not info:
        return None
    def deg(v, ref):
        d, m, sec = (float(x) for x in v)
        val = d + m / 60 + sec / 3600
        return -val if ref in ("S", "W") else val
    try:
        return round(deg(info[2], info[1]), 5), round(deg(info[4], info[3]), 5)
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        return None


def slug(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


def faces(img):
    """Face boxes in image pixel coordinates, detected on a downscaled copy."""
    small = img.convert("L")
    scale = 420 / max(small.size)
    if scale < 1:
        small = small.resize((max(1, int(small.width * scale)), max(1, int(small.height * scale))))
    else:
        scale = 1
    found = CASCADE.detectMultiScale(np.array(small), scaleFactor=1.12, minNeighbors=6, minSize=(24, 24))
    return [(x / scale, y / scale, w / scale, h / scale) for x, y, w, h in found]


def crop(img):
    """Trim only the extreme ratios, keeping the subject in frame."""
    w, h = img.size
    ratio = w / h
    if MIN_PORTRAIT <= ratio <= MAX_LANDSCAPE:
        return img

    boxes = faces(img)
    if ratio > MAX_LANDSCAPE:                      # too wide: choose an x window
        new_w = int(h * MAX_LANDSCAPE)
        if boxes:
            centre = sum(x + bw / 2 for x, _, bw, _ in boxes) / len(boxes)
        else:
            centre = w / 2
        left = int(min(max(0, centre - new_w / 2), w - new_w))
        return img.crop((left, 0, left + new_w, h))

    new_h = int(w / MIN_PORTRAIT)                  # too tall: choose a y window
    if boxes:
        centre = sum(y + bh / 2 for _, y, _, bh in boxes) / len(boxes)
    else:
        centre = h * 0.42                          # people sit above centre more often than below
    top = int(min(max(0, centre - new_h / 2), h - new_h))
    return img.crop((0, top, w, top + new_h))


FORCE = "--force" in sys.argv


def process():
    """Resize the album into OUT, writing only what is missing.

    Deliberately not delete-everything-then-rewrite: rewriting all 354 files on
    every run produced a pile of macOS " 2" / " 3" duplicate-conflict copies.
    Pass --force to regenerate anyway, after changing the crop or size settings.
    """
    OUT.mkdir(parents=True, exist_ok=True)

    sources = sorted(p for p in ALBUM.rglob("*")
                     if p.is_file() and not p.name.startswith(".")
                     and p.suffix.lower() in (".jpg", ".jpeg", ".png"))
    written, seen, meta = [], set(), {}
    for src in sources:
        folder = src.parent.name
        stem = slug(src.stem)
        name = stem if folder in (ALBUM.name, FEATURED_DIR.name) else f"{slug(folder)}-{stem}"
        n = 2
        while name in seen:
            name, n = f"{name}-{n}", n + 1
        seen.add(name)

        try:
            with Image.open(src) as probe:
                ex = probe._getexif() or {}
            taken = str(ex.get(36867) or ex.get(306) or "")
            entry = {}
            if taken:
                entry["date"] = taken[:10].replace(":", "-")
                entry["taken"] = taken
            here = gps(ex)
            if here:
                entry["lat"], entry["lon"] = here
            if entry:
                meta[f"{name}.jpg"] = entry
        except Exception:
            pass

        dest = OUT / f"{name}.jpg"
        if dest.exists() and not FORCE:
            with Image.open(dest) as done:
                written.append((f"/assets/img/gallery/album/{name}.jpg", folder, done.width, done.height))
            continue
        try:
            img = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        except Exception as e:
            print("  skipped", src.name, e)
            continue
        img = crop(img)
        img.thumbnail((LONG_SIDE, LONG_SIDE), Image.LANCZOS)
        # no exif= argument, so orientation, timestamps and GPS are all dropped
        img.save(dest, "JPEG", quality=QUALITY, optimize=True, progressive=True)
        written.append((f"/assets/img/gallery/album/{name}.jpg", folder, img.width, img.height))

    # anything in OUT that no longer corresponds to a source photo, including
    # the " 2" / " 3" duplicate-conflict copies, goes
    wanted = {f"{n}.jpg" for n in seen}
    for stale in OUT.glob("*.jpg"):
        if stale.name not in wanted:
            stale.unlink()
            print("  pruned", stale.name)
    META.write_text(json.dumps(meta, indent=1, sort_keys=True))
    return written


def existing_entries():
    """Keep the professional photos, and keep the alt text they already have."""
    html = PAGE.read_text()
    out = []
    for m in re.finditer(r'<img src="(/assets/img/gallery/[^"/]+)" alt="([^"]*)"', html):
        src = m.group(1)
        with Image.open(ROOT / src.lstrip("/")) as im:
            w, h = ImageOps.exif_transpose(im).size
        out.append((src, m.group(2), w, h))
    return out


ALT = {
    "Family": "Family photo",
    "Friends": "With friends",
    "Cousins": "With cousins",
    "Milo": "Milo",
    "Science": "In the lab",
}


def featured_order():
    """Filenames to pull to the top, most important first.

    Two ways to say so, and you can use either or both:
      1. drop photos into ~/Desktop/Acknowledgements/_featured/
      2. list filenames in tools/gallery-featured.txt, one per line, best first
    The text file wins on ordering, since a folder has no meaningful order.
    """
    listed, big = [], set()
    if FEATURED_LIST.exists():
        for line in FEATURED_LIST.read_text().splitlines():
            line = line.split("#")[0].strip()
            if not line:
                continue
            large = line.startswith("*")
            name = slug(pathlib.Path(line.lstrip("*").strip()).stem)
            listed.append(name)
            if large:
                big.add(name)
    foldered = sorted(slug(f.stem) for f in FEATURED_DIR.glob("*")
                      if f.is_file() and not f.name.startswith("."))
    rank = {name: i for i, name in enumerate(listed)}
    for name in foldered:
        rank.setdefault(name, len(rank))
    return rank, big


def dhash(path, size=8):
    """64-bit perceptual hash: compares each pixel with its right-hand neighbour.

    Near-identical shots (burst frames, a re-save, the same photo twice) land on
    the same or a very close hash, which exact file hashing would miss.
    """
    with Image.open(path) as im:
        im = im.convert("L").resize((size + 1, size), Image.LANCZOS)
        px = list(im.getdata())
    bits = 0
    for row in range(size):
        for col in range(size):
            i = row * (size + 1) + col
            bits = (bits << 1) | int(px[i] > px[i + 1])
    return bits


def seconds_apart(a, b, meta):
    """Gap between two shots, or a huge number if either lacks a timestamp.

    Burst frames of one moment can differ enough in pixels to survive a hash
    comparison; taken seconds apart, they are still the same photo twice.
    """
    fmt = "%Y:%m:%d %H:%M:%S"
    try:
        ta = datetime.strptime(meta[pathlib.Path(a).name]["taken"][:19], fmt)
        tb = datetime.strptime(meta[pathlib.Path(b).name]["taken"][:19], fmt)
    except (KeyError, ValueError):
        return 1e9
    return abs((ta - tb).total_seconds())


def dedupe(srcs, scores, meta, protected=()):
    """Drop near-identical photos, keeping the sharpest of each group.

    A photo you picked by hand always wins its group -- you chose that frame,
    and a sharpness score has no business overruling that.
    """
    hashes = {src: dhash(ROOT / src.lstrip("/")) for src in srcs}
    keep, groups = [], []
    for src in srcs:
        h = hashes[src]
        for g in groups:
            distance = bin(h ^ hashes[g[0]]).count("1")
            if distance <= 8 or (distance <= 16 and seconds_apart(src, g[0], meta) <= 180):
                g.append(src)
                break
        else:
            groups.append([src])
    dropped = 0
    for g in groups:
        chosen = [s for s in g if pathlib.Path(s).stem in protected]
        if chosen:
            keep.extend(chosen)
            dropped += len(g) - len(chosen)
        else:
            keep.append(max(g, key=lambda s: scores.get(pathlib.Path(s).name, {}).get("sharpness", 0)))
            dropped += len(g) - 1
    return keep, dropped


def removed():
    """Photos to leave out of the gallery entirely, one filename per line."""
    if not REMOVE_LIST.exists():
        return set()
    out = set()
    for line in REMOVE_LIST.read_text().splitlines():
        line = line.split("#")[0].strip()
        if line:
            out.add(slug(pathlib.Path(line).stem))
    return out


album = process()
rank, big = featured_order()
scores = json.loads(SCORES.read_text()) if SCORES.exists() else {}
meta = json.loads(META.read_text()) if META.exists() else {}


def key_of(src):
    return pathlib.Path(src).stem


gone = removed()


def cull(entries):
    """Drop the unusable and the ones she is not in.

    Kept regardless: anything featured by hand, anything in ALWAYS_KEEP, and
    any photo with a crowd in it -- recognition gets unreliable once faces are
    small and half-turned, and she is usually somewhere in a group shot.
    """
    keep, reasons = [], {"blurry": 0, "low-res": 0, "not her": 0}
    for e in entries:
        name = pathlib.Path(e[0]).name
        v = scores.get(name, {})
        if pathlib.Path(e[0]).stem in rank or name.startswith(ALWAYS_KEEP):
            keep.append(e)
            continue
        if max(e[2], e[3]) < MIN_LONG_SIDE:
            reasons["low-res"] += 1
            continue
        if v.get("sharpness", 1e9) < MIN_SHARPNESS:
            reasons["blurry"] += 1
            continue
        if not v.get("is_me") and v.get("faces", 0) < GROUP_SPARE:
            reasons["not her"] += 1
            continue
        keep.append(e)
    return keep, reasons
album_entries = [(src, ALT.get(folder, "Photo"), w, h) for src, folder, w, h in album
                 if pathlib.Path(src).stem not in gone]
album_entries, culled = cull(album_entries)
kept_srcs, duplicates = dedupe([e[0] for e in album_entries], scores, meta, protected=set(rank))
kept_srcs = set(kept_srcs)
album_entries = [e for e in album_entries if e[0] in kept_srcs]

professional = existing_entries()          # posters, awards, conferences
entries = professional + album_entries

featured = sorted((e for e in entries if key_of(e[0]) in rank),
                  key=lambda e: rank[key_of(e[0])])
taken = {key_of(e[0]) for e in featured}


def quality(e):
    """Close-up and sharp beats distant and soft."""
    v = scores.get(pathlib.Path(e[0]).name, {})
    return (v.get("prominence", 0) * 6) + min(v.get("sharpness", 0) / 400, 1.5)


# Priority order:
#   1. anything named in gallery-featured.txt / dropped in _featured
#   2. the professional photos -- lab, posters, conferences
#   3. album photos you are in, the most flattering first
#   4. everything else
# The top LEAD of that order go in the lead block. This is not fussiness about
# where things sit: a CSS multi-column layout fills column 1 top to bottom
# before starting column 2, so putting a photo "first" in the grid buries it
# down the left edge rather than showing it first. The lead block is its own
# row-wise element, so order there is the order you actually see.
pro = [e for e in professional if key_of(e[0]) not in taken]
with_me = [e for e in album_entries
           if key_of(e[0]) not in taken
           and scores.get(pathlib.Path(e[0]).name, {}).get("is_me")]
in_me = {key_of(e[0]) for e in with_me}
others = [e for e in album_entries
          if key_of(e[0]) not in taken and key_of(e[0]) not in in_me]
with_me.sort(key=quality, reverse=True)

# Photos from the days that matter, defense first, then commencement, then the
# party -- inside each day the most flattering shot leads.
key = []
for day in KEY_DATES:
    same_day = [e for e in album_entries
                if meta.get(pathlib.Path(e[0]).name, {}).get("date") == day
                and key_of(e[0]) not in taken]
    same_day.sort(key=quality, reverse=True)
    key += same_day
on_key_day = {key_of(e[0]) for e in key}

ranked = key + [e for e in pro if key_of(e[0]) not in on_key_day] + \
    [e for e in with_me if key_of(e[0]) not in on_key_day]
featured += ranked[:max(0, LEAD - len(featured))]
promoted = {key_of(e[0]) for e in featured}

rest = [e for e in ranked if key_of(e[0]) not in promoted] + \
    [e for e in others if key_of(e[0]) not in on_key_day]
random.Random(SEED).shuffle(others)

# width/height are required: the gallery is a CSS multi-column layout, and a
# lazy image with no intrinsic size collapses to nothing until it loads, which
# breaks every column but the first.
def figure(e, eager=False):
    src, alt, w, h = e
    load = "" if eager else ' loading="lazy"'
    cls = ' class="is-big"' if pathlib.Path(src).stem in big else ""
    return f'<figure{cls}><img src="{src}" alt="{alt}" width="{w}" height="{h}"{load}></figure>'


# Featured photos get their own block above the grid. They cannot simply go
# first in the main grid: CSS multi-column fills column 1 top to bottom before
# starting column 2, so "first" would mean "top of the left column", not "top
# of the page".
blocks = ""
if featured:
    strip = "\n".join("            " + figure(e, eager=i < 4) for i, e in enumerate(featured))
    blocks += f'          <div class="gallery gallery--featured" data-layout="justified" data-row-height="300" data-big-height="560">\n{strip}\n          </div>\n'
grid = "\n".join("            " + figure(e) for e in rest)
blocks += f'          <div class="gallery" data-min="150">\n{grid}\n          </div>'

html = PAGE.read_text()
pattern = re.compile(r"(<!-- gallery:start -->\n).*?([ \t]*<!-- gallery:end -->)", re.S)
if not pattern.search(html):
    raise SystemExit("gallery/index.html has no <!-- gallery:start --> markers")
PAGE.write_text(pattern.sub(lambda m: m.group(1) + blocks + "\n" + m.group(2), html, count=1))

print(f"processed {len(album)} album photos")
print(f"  culled: {culled['low-res']} low-res, {culled['blurry']} blurry, "
      f"{culled['not her']} without you; {duplicates} duplicates; {len(gone)} by hand")
print(f"  {len(key)} from key dates; {len(featured)} in the lead block, {len(rest)} in the grid")
