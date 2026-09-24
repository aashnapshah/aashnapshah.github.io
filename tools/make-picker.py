"""Build a local page for choosing which photos lead the gallery.

Run: python3 tools/make-picker.py
Then open http://localhost:4173/tools/pick-featured.html

Tick the photos you want up top, drag them into the order you want, press Copy,
and paste into tools/gallery-featured.txt. Then re-run build-gallery.py.

Photos are pre-sorted so the likely candidates come first: crimson regalia
(graduation and defense robes are Harvard crimson, which is easy to spot by
colour), then shots you are in, then the sharpest close-ups. The regalia ones
start pre-ticked -- untick anything that is not what you wanted.
"""
import colorsys
import json
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALBUM = ROOT / "assets/img/gallery/album"
SCORES = ROOT / "tools/photo-scores.json"
OUT = ROOT / "tools/pick-featured.html"
FEATURED = ROOT / "tools/gallery-featured.txt"
REMOVED = ROOT / "tools/gallery-remove.txt"


def read_list(path):
    if not path.exists():
        return []
    out = []
    for line in path.read_text().splitlines():
        line = line.split("#")[0].strip()
        if line:
            out.append(line)
    return out

scores = json.loads(SCORES.read_text()) if SCORES.exists() else {}


def crimson(path):
    """Fraction of the frame that is Harvard-crimson -- i.e. academic regalia."""
    with Image.open(path) as im:
        im = im.convert("RGB").resize((64, 64), Image.BILINEAR)
        px = list(im.getdata())
    hits = 0
    for r, g, b in px:
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        deg = h * 360
        if (deg >= 340 or deg <= 12) and s >= 0.42 and 0.12 <= v <= 0.75:
            hits += 1
    return hits / len(px)


photos = sorted(ALBUM.glob("*.jpg"))
rows = []
for p in photos:
    v = scores.get(p.name, {})
    rows.append({
        "name": p.name,
        "me": v.get("is_me", False),
        "regalia": round(crimson(p), 4),
        "quality": v.get("prominence", 0) * 6 + min(v.get("sharpness", 0) / 400, 1.5),
    })

rows.sort(key=lambda r: (-r["regalia"] * 3 - (1 if r["me"] else 0) - r["quality"] * 0.2))

# carry over whatever is already chosen, so nothing has to be redone
current = read_list(FEATURED)
order = [c.lstrip("*").strip() for c in current]
bigs = {c.lstrip("*").strip() for c in current if c.startswith("*")}
gone = set(read_list(REMOVED))

def card(r):
    state = []
    if r["name"] in order:
        state.append("on")
    if r["name"] in bigs:
        state.append("big")
    if r["name"] in gone:
        state.append("gone")
    return (
        '<figure class="{cls}" data-name="{n}">'
        '<img src="../assets/img/gallery/album/{n}" loading=lazy>'
        '<div class=btns>'
        '<button class=f title="feature">&#9733;</button>'
        '<button class=b title="show big">&#8599;</button>'
        '<button class=x title="remove">&#10005;</button>'
        '</div><figcaption>{me}{n}</figcaption></figure>'
    ).format(cls=" ".join(state), n=r["name"], me="you &middot; " if r["me"] else "")


cards = "\n".join(card(r) for r in rows)

OUT.write_text("""<!doctype html><meta charset=utf-8><title>Pick featured photos</title>
<style>
body{font:14px/1.5 -apple-system,sans-serif;margin:0;background:#faf9f7;color:#222}
header{position:sticky;top:0;background:#fffe;backdrop-filter:blur(8px);border-bottom:1px solid #e6e6e3;padding:1rem 1.5rem;z-index:5}
h1{font-size:1.1rem;margin:0 0 .35rem}p{margin:0;color:#666;max-width:78ch;font-size:13px}
.bar{display:flex;gap:.6rem;align-items:center;margin-top:.7rem;flex-wrap:wrap}
button{font:500 13px/1 inherit;padding:.5rem .9rem;border-radius:999px;border:1px solid #d5d5d0;background:#fff;cursor:pointer}
button.primary{background:#a51c30;border-color:#a51c30;color:#fff}
b{color:#a51c30}
textarea{width:100%;height:110px;margin-top:.6rem;font:12px/1.5 ui-monospace,Menlo,monospace;border:1px solid #e0e0dc;border-radius:8px;padding:.6rem;display:none}
textarea.show{display:block}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:.8rem;padding:1.2rem 1.5rem}
figure{position:relative;margin:0;border-radius:10px;overflow:hidden;border:2px solid transparent;background:#fff}
figure.on{border-color:#a51c30}
figure.big{border-color:#0a7d53;border-width:3px}
figure.gone{opacity:.32;border-color:#999;border-style:dashed}
figure img{width:100%;aspect-ratio:1;object-fit:cover;display:block}
figcaption{font-size:10px;color:#777;padding:.3rem .4rem;word-break:break-all}
.btns{position:absolute;top:6px;left:6px;display:flex;gap:4px}
.btns button{padding:0;width:26px;height:26px;border-radius:7px;font-size:13px;line-height:1;opacity:.82}
.btns button:hover{opacity:1}
figure.on .f{background:#a51c30;color:#fff;border-color:#a51c30}
figure.big .b{background:#0a7d53;color:#fff;border-color:#0a7d53}
figure.gone .x{background:#444;color:#fff;border-color:#444}
.n{font-weight:600;color:#a51c30}
</style>
<header>
<h1>Choose what the gallery does with each photo</h1>
<p><b>&#9733;</b> feature it in the block at the top &mdash; click order is display order.
<b>&#8599;</b> show it big, on a row of its own (features it too).
<b>&#10005;</b> drop it from the gallery entirely.
Sorted with the likely graduation and defense shots first, by how much Harvard crimson is in frame.
Your current choices are already loaded.</p>
<div class="bar">
  <span><span class="n" id="cf">0</span> featured &middot; <span class="n" id="cb">0</span> big &middot; <span class="n" id="cx">0</span> removed</span>
  <button class="primary" id="copyf">Copy featured list</button>
  <button id="copyx">Copy removed list</button>
  <button id="show">Show both</button>
</div>
<textarea id="outf" readonly></textarea>
<textarea id="outx" readonly></textarea>
</header>
<div class="grid">
""" + cards + """
</div>
<script>
var NL = String.fromCharCode(10);
var order = ORDER_JSON;
var bigs = new Set(BIGS_JSON);
var gone = new Set(GONE_JSON);

function featuredLines(){
  return order.map(function(n){ return (bigs.has(n) ? "*" : "") + n; });
}
function render(){
  document.getElementById("cf").textContent = order.length;
  document.getElementById("cb").textContent = bigs.size;
  document.getElementById("cx").textContent = gone.size;
  document.getElementById("outf").value = featuredLines().join(NL);
  document.getElementById("outx").value = Array.from(gone).join(NL);
}
function sync(fig){
  var n = fig.dataset.name;
  fig.classList.toggle("on", order.indexOf(n) >= 0);
  fig.classList.toggle("big", bigs.has(n));
  fig.classList.toggle("gone", gone.has(n));
}
document.querySelector(".grid").addEventListener("click", function(e){
  var btn = e.target.closest("button");
  if(!btn) return;
  var fig = e.target.closest("figure");
  var n = fig.dataset.name;
  if(btn.classList.contains("f")){
    var i = order.indexOf(n);
    if(i >= 0){ order.splice(i,1); bigs.delete(n); } else { order.push(n); gone.delete(n); }
  } else if(btn.classList.contains("b")){
    if(bigs.has(n)) bigs.delete(n);
    else { bigs.add(n); if(order.indexOf(n) < 0) order.push(n); gone.delete(n); }
  } else {
    if(gone.has(n)) gone.delete(n);
    else {
      gone.add(n); bigs.delete(n);
      var j = order.indexOf(n); if(j >= 0) order.splice(j,1);
    }
  }
  sync(fig);
  render();
});
function copy(text, btn, label){
  navigator.clipboard.writeText(text).then(function(){
    btn.textContent = "Copied";
    setTimeout(function(){ btn.textContent = label; }, 1200);
  });
}
document.getElementById("copyf").onclick = function(){
  copy(featuredLines().join(NL), this, "Copy featured list");
};
document.getElementById("copyx").onclick = function(){
  copy(Array.from(gone).join(NL), this, "Copy removed list");
};
document.getElementById("show").onclick = function(){
  document.getElementById("outf").classList.toggle("show");
  document.getElementById("outx").classList.toggle("show");
};
render();
</script>
""".replace("ORDER_JSON", json.dumps(order))
   .replace("BIGS_JSON", json.dumps(sorted(bigs)))
   .replace("GONE_JSON", json.dumps(sorted(gone))))

print(f"wrote {OUT.relative_to(ROOT)}: {len(rows)} photos, "
      f"{len(order)} featured, {len(bigs)} big, {len(gone)} removed")
