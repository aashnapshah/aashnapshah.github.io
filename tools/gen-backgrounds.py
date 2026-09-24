"""Generate the background artwork for aashna-shah.com.

Run: python3 tools/gen-backgrounds.py

What this produces
- The hero wash: two soft crimson radial gradients behind the top of the page.
- The motif field: six static illustrations in a layer behind the page,
  each centred on a section transition, where the margins are quiet (the
  script at the bottom of index.html places them). Each spans the page.

Visual language
- a few continuous lines, never a chart
- warm grey for context, crimson for the one meaningful signal
- the reading column stays clear; each motif fades toward it (CSS mask)
- no axes, labels, or diagram furniture

Six themes, each a complete drawing sized for one side margin, alternating
left and right down the page. They were previously drawn as pairs split
across the reading column, but 760px of text sits between the halves and the
eye will not bridge that -- it read as fragments of lines at the edges rather
than one picture.
  posterior      Bayesian updating on one baseline: a wide prior sharpening
                 into a tight crimson posterior (About)
  trajectories   the reference interval climbing (into Research)
  clusters       three patient clusters, stacked (down Publications)
  interval       the same interval, falling (into Talks)
  trace          one heartbeat: P wave, QRS complex, T wave (into Experience)
  network        inputs to output, one path lit (into Community)

Each block replaces the content between matching bg markers in index.html,
so rerunning this script is safe.
"""

import math
import pathlib
import re


MARGIN_W = 300   # canvas width; CSS scales this to the real gutter

T = "var(--text)"
A = "var(--accent)"
NS = (
    'vector-effect="non-scaling-stroke" fill="none" '
    'stroke-linecap="round" stroke-linejoin="round"'
)


# ---------------------------------------------------------------- helpers


def fmt(v):
    """Compact number formatting for path data."""
    return f"{v:.1f}".rstrip("0").rstrip(".")


def svg(css_class, width, height, body, defs=""):
    """Wrap a decorative SVG. Each motif keeps its own aspect ratio."""
    defs = f"<defs>{defs}</defs>" if defs else ""
    return (
        f'<svg class="{css_class}" viewBox="0 0 {width} {height}" '
        f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true" '
        f'focusable="false">{defs}{body}</svg>'
    )


def line(d, color=T, opacity=".10", width="1.3", signal=False, index=0):
    """One line in the shared system.

    pathLength normalises every path to 1 so the draw-in animation takes the
    same time whatever the length; index staggers the start (see the CSS).
    """
    modifier = " art-line--signal" if signal else ""
    return (
        f'<path class="art-line{modifier}" style="--i:{index}" pathLength="1" '
        f'd="{d}" {NS} stroke="{color}" stroke-opacity="{opacity}" '
        f'stroke-width="{width}"/>'
    )


def smooth(points):
    """Catmull-Rom spline through the points, as cubic Bezier path data."""
    pts = [points[0]] + list(points) + [points[-1]]
    out = [f"M{fmt(pts[1][0])} {fmt(pts[1][1])}"]
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        out.append(
            f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} "
            f"{fmt(p2[0])} {fmt(p2[1])}"
        )
    return " ".join(out)


def gaussian(x0, x1, mu, sigma, baseline, height, n=96):
    """A bell curve drawn on a baseline, sampled densely near the peak."""
    pts = []
    for k in range(n + 1):
        t = k / n
        # Warp the samples toward the peak so narrow curves stay smooth.
        u = 2 * t - 1
        x = mu + math.copysign(abs(u) ** 1.35, u) * max(mu - x0, x1 - mu)
        x = min(max(x, x0), x1)
        y = baseline - height * math.exp(-((x - mu) ** 2) / (2 * sigma**2))
        pts.append((x, y))
    # Keep the sample list monotone in x after clamping.
    pts = sorted(set(pts))
    return smooth(pts)


def dots(circles, fill=T, opacity=".17", signal=False):
    """A group of nodes."""
    modifier = " art-nodes--signal" if signal else ""
    body = "".join(
        f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{r}"/>' for x, y, r in circles
    )
    return f'<g class="art-nodes{modifier}" fill="{fill}" fill-opacity="{opacity}">{body}</g>'


def hollow(circles, stroke=T, opacity=".18"):
    """Open nodes: page-coloured discs with a thin outline."""
    body = "".join(
        f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{r}"/>' for x, y, r in circles
    )
    return (
        f'<g class="art-nodes" fill="var(--bg)" stroke="{stroke}" '
        f'stroke-opacity="{opacity}" stroke-width="1.5">{body}</g>'
    )


def cluster(cx, cy, scale=1.0, index=0):
    """One patient cluster, drawn as nested density contours.

    Four closed rings of the same irregular outline at shrinking sizes, so
    they nest the way contour levels do. The inner two are crimson: that is
    where the cluster is densest. No scatter points, just the contours.
    """
    rx, ry = 150 * scale, 112 * scale
    # One irregular outline, reused at every level so the rings stay nested.
    wobble = [1.00, 0.92, 1.07, 0.96, 1.05, 0.94, 1.03, 0.98, 1.06, 0.93]
    angles = [math.radians(d) for d in range(0, 360, 36)]

    def ring(factor):
        return [
            (cx + rx * factor * wobble[k] * math.cos(a),
             cy + ry * factor * wobble[k] * math.sin(a))
            for k, a in enumerate(angles)
        ]

    # (size, colour, opacity, stroke width), outermost first
    levels = [
        (1.00, T, ".07", "1.3"),
        (0.76, T, ".11", "1.5"),
        (0.52, A, ".17", "1.9"),
        (0.29, A, ".34", "2.4"),
    ]
    body = ""
    for i, (factor, colour, opacity, width) in enumerate(levels):
        points = ring(factor)
        body += line(
            smooth(points + points[:2]), colour, opacity, width,
            signal=colour == A, index=index + i,
        )
    return body


def fit(body, top, bottom, pad=24):
    """Centre a drawing in its own box.

    Takes the drawing's vertical extent and returns (height, body) with the
    body shifted so there is equal space above and below. Motifs are centred
    on a divider line by their box, so the box has to hug the drawing.
    """
    height = bottom - top + 2 * pad
    return fmt(height), f'<g transform="translate(0 {fmt(pad - top)})">{body}</g>'


def motif(name, width, height, body, anchor=None, side="right"):
    """One SVG in the background field, spanning the main area.

    anchor is a section id, and the page script centres the motif on the
    divider line above that section, where the margins are quiet. Pass
    (section id, "middle") to centre it inside the section, or
    (section id, "start") to begin it at the section's top edge. Without an
    anchor the script centres it in the About section.

    side is "left" or "right"; CSS pins the motif to that margin.

    Each motif carries a whisper of crimson wash behind the line work, so the
    art sits on warm paper rather than flat white. Keep it very low: it stacks
    with the hero wash at the top of the page.
    """
    if not anchor:
        data = ' data-hero=""'
    elif isinstance(anchor, tuple):
        data = f' data-section="{anchor[0]}" data-align="{anchor[1]}"'
    else:
        data = f' data-section="{anchor}"'

    defs = (
        f'<radialGradient id="wash-{name}" cx=".5" cy=".5" r=".62">'
        f'<stop offset="0" stop-color="{A}" stop-opacity=".03"/>'
        f'<stop offset="1" stop-color="{A}" stop-opacity="0"/>'
        f'</radialGradient>'
    )
    wash = f'<rect width="{width}" height="{height}" fill="url(#wash-{name})"/>'

    out = svg(f"motif motif--{name} motif--{side}", width, height, wash + body, defs)
    return out.replace("<svg ", f'<svg preserveAspectRatio="none"{data} ', 1)


def posterior(peak=64, anchor="research", side="right"):
    """Bayesian updating along one baseline: a wide prior narrowing to a posterior.

    Five distributions in one margin, the wide low prior first and each one
    after it narrower and taller, ending in the crimson posterior.
    """
    W = MARGIN_W
    # (mean, spread, colour, opacity, stroke width), prior first
    curves = [
        (52, 30, T, ".10", "1.5"),
        (104, 22, T, ".13", "1.55"),
        (152, 16, T, ".16", "1.6"),
        (196, 11, T, ".21", "1.7"),
        (238, 7.5, A, ".40", "2.6"),
    ]
    heights = [peak * (30 / s) ** 0.5 for _, s, _, _, _ in curves]

    pad = 24
    H = max(heights) + 2 * pad
    base = H - pad

    body = line(f"M0 {fmt(base)} H{W}", T, ".075", "1.2", index=0)
    for i, ((mu, s, colour, opacity, width), h) in enumerate(zip(curves, heights)):
        x0, x1 = max(0, mu - 4 * s), min(W, mu + 4 * s)
        body += line(
            gaussian(x0, x1, mu, s, base, h), colour, opacity, width,
            signal=colour == A, index=i + 1,
        )
    return motif("posterior", W, fmt(H), body, anchor=anchor, side=side)


def clusters(side="left"):
    """Three patient clusters down the margin, faintly linked."""
    W = MARGIN_W
    scale = 0.52
    first, second, third = (96, 92), (196, 246), (104, 400)
    body = cluster(*first, scale=scale, index=0)
    body += cluster(*second, scale=scale, index=2)
    body += cluster(*third, scale=scale, index=4)
    body += line(
        smooth([(126, 150), (158, 186), (178, 212)]), T, ".065", "1.3", index=6,
    )
    body += line(
        smooth([(176, 300), (148, 336), (124, 360)]), T, ".065", "1.3", index=7,
    )
    ry = 112 * scale
    H, body = fit(body, first[1] - ry - 18, third[1] + ry + 18)
    return motif("clusters", W, H, body, anchor=("publications", "start"), side=side)


def envelope(rising):
    """A personal reference interval inside the population one.

    A wandering centre line, a wide grey envelope, a narrow crimson envelope,
    and a row of measurements. One point sits outside the personal band but
    inside the population one: normal for the population, abnormal for the
    person.

    Both longitudinal motifs come from this one shape so they stay
    consistent: rising=True mirrors it vertically so it climbs instead of
    falling.
    """
    W = MARGIN_W

    def centre(x):
        y = 150 + 240 * x / W + 16 * math.sin(x / 22) + 7 * math.sin(x / 10 + 1.3)
        return 540 - y if rising else y

    xs = list(range(0, W + 1, 6))

    def band(offset):
        return smooth([(x, centre(x) + offset) for x in xs])

    body = (
        line(band(-70), T, ".075", "1.5", index=0)
        + line(band(70), T, ".075", "1.5", index=1)
        + line(band(-22), A, ".26", "2.2", signal=True, index=2)
        + line(band(22), A, ".26", "2.2", signal=True, index=3)
    )
    samples = [(26, -8), (68, 6), (110, -12), (152, 4), (194, 10), (236, -6), (278, 8)]
    body += hollow([(x, centre(x) + dy, 3) for x, dy in samples], T, ".2")
    outlier_x = 216
    outlier = centre(outlier_x) - 50
    body += dots([(outlier_x, outlier, 3.4)], A, ".48", signal=True)

    top = min(min(centre(x) for x in xs) - 74, outlier - 4)
    return fit(body, top, max(centre(x) for x in xs) + 74)


def trajectories(side="left"):
    """The reference interval, climbing."""
    H, body = envelope(rising=True)
    return motif("trajectories", MARGIN_W, H, body, anchor="research", side=side)


def interval(side="right"):
    """The same interval, falling."""
    H, body = envelope(rising=False)
    return motif("interval", MARGIN_W, H, body, anchor="talks", side=side)


def trace(side="left"):
    """One heartbeat in the margin: P wave, QRS complex, T wave."""
    W = MARGIN_W
    base = 200
    signal = (
        f"M0 {base} H40 C52 {base} 56 182 68 182 C80 182 84 {base} 96 {base} "
        f"H128 C138 {base} 141 196 145 188 L151 176 L160 240 L171 110 L182 226 L190 {base} "
        f"H222 C234 {base} 238 178 250 178 C262 178 266 {base} {W} {base}"
    )
    body = (
        line(signal, A, ".34", "2.6", signal=True, index=0)
        + hollow([(28, base, 4), (96, base, 4), (128, base, 4), (190, base, 4)], T, ".16")
        + dots([(171, 110, 3.6)], A, ".48", signal=True)
    )
    H, body = fit(body, 110 - 4, 240 + 2)      # the T wave peak and the S trough
    return motif("trace", W, H, body, anchor="experience", side=side)


# -------------------------------------------------------------- hero wash


def network(side="right"):
    """A small network in the margin: inputs to output, one crimson path lit."""
    W = MARGIN_W
    layers = [
        [(24, 46), (24, 128), (24, 210), (24, 292)],
        [(112, 87), (112, 169), (112, 251)],
        [(200, 87), (200, 169), (200, 251)],
        [(276, 169)],
    ]
    path = [layers[0][2], layers[1][1], layers[2][1], layers[3][0]]
    body = ""
    for a, b in zip(layers, layers[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                body += line(f"M{x1} {y1} L{x2} {y2}", T, ".07", "1.2", index=0)
    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        body += line(f"M{x1} {y1} L{x2} {y2}", A, ".32", "2.3", signal=True, index=1)
    others = [n for layer in layers for n in layer if n not in path]
    body += hollow([(x, y, 6) for x, y in others], T, ".2")
    body += dots([(x, y, 5) for x, y in path], A, ".46", signal=True)
    H, body = fit(body, 46 - 7, 292 + 7)
    return motif("network", W, H, body, anchor="community", side=side)


def hero():
    """Two soft crimson washes behind the top of the page."""
    W, H = 1440, 660
    defs = (
        f'<radialGradient id="hero-wash-left" cx="0" cy=".2" r=".9">'
        f'<stop offset="0" stop-color="{A}" stop-opacity=".050"/>'
        f'<stop offset="1" stop-color="{A}" stop-opacity="0"/>'
        f'</radialGradient>'
        f'<radialGradient id="hero-wash-right" cx="1" cy=".35" r=".8">'
        f'<stop offset="0" stop-color="{A}" stop-opacity=".035"/>'
        f'<stop offset="1" stop-color="{A}" stop-opacity="0"/>'
        f'</radialGradient>'
        f'<linearGradient id="hero-wash-fade" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="var(--bg)" stop-opacity="0"/>'
        f'<stop offset=".64" stop-color="var(--bg)" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="var(--bg)" stop-opacity="1"/>'
        f'</linearGradient>'
    )
    body = (
        f'<rect width="{W}" height="{H}" fill="url(#hero-wash-left)"/>'
        f'<rect width="{W}" height="{H}" fill="url(#hero-wash-right)"/>'
        f'<rect width="{W}" height="{H}" fill="url(#hero-wash-fade)"/>'
    )
    wash = (
        f'<svg class="bg-wash" viewBox="0 0 {W} {H}" preserveAspectRatio="none" '
        f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">'
        f'<defs>{defs}</defs>{body}</svg>'
    )
    return f'<div class="bg-stage" aria-hidden="true">{wash}</div>'


def field():
    """The motifs, in page order. Positioning happens in the browser."""
    motifs = [
        posterior(anchor=None, side="right"),   # the About background
        trajectories(side="left"),
        clusters(side="right"),
        interval(side="left"),
        trace(side="right"),
        network(side="left"),
    ]
    return '<div class="bg-field" aria-hidden="true">' + "".join(motifs) + "</div>"


BLOCKS = {
    "hero": hero,
    "field": field,
}

site = pathlib.Path(__file__).resolve().parent.parent / "index.html"
html = site.read_text()
for name, build in BLOCKS.items():
    pattern = re.compile(rf"([ \t]*)<!-- bg:{name} -->.*?<!-- /bg:{name} -->", re.S)
    if not pattern.search(html):
        raise SystemExit(f"index.html has no <!-- bg:{name} --> markers")
    html = pattern.sub(
        lambda match: (
            f"{match.group(1)}<!-- bg:{name} -->\n"
            f"{match.group(1)}{build()}\n"
            f"{match.group(1)}<!-- /bg:{name} -->"
        ),
        html,
        count=1,
    )

site.write_text(html)
print("wrote", ", ".join(BLOCKS), "into index.html")
