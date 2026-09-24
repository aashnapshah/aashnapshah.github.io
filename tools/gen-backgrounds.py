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

Six themes, each drawn as a pair: one half in the left margin, one in the
right, so the pair reads as one picture continuing behind the text.
  posterior      Bayesian updating on one baseline: a wide prior at the left
                 narrowing to a tight posterior at the right, three bells
                 visible in each margin (About)
  trajectories   the reference interval climbing left to right (into Research)
  clusters       three patient clusters, right, left, right (down Featured Publications)
  trace          one ECG strip: P wave at the left, QRS and T wave at the right (into Experience)
  interval       the same interval, falling left to right (into Community)

Each block replaces the content between matching bg markers in index.html,
so rerunning this script is safe.
"""

import math
import pathlib
import re


# Global multiplier on every stroke and fill opacity. The authored values were
# tuned for a page that read as too white; this lifts the whole system in
# proportion so the hierarchy between lines is unchanged.
PRESENCE = 1.35


def lift(opacity):
    return f"{min(1.0, float(opacity) * PRESENCE):.3f}".rstrip("0").rstrip(".")


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


def line(d, color=T, opacity=".10", width="1.3", signal=False, index=0, still=False):
    """One line in the shared system.

    pathLength normalises every path to 1 so the draw-in animation takes the
    same time whatever the length; index staggers the start (see the CSS).
    """
    modifier = (" art-line--signal" if signal else "") + (" art-line--still" if still else "")
    return (
        f'<path class="art-line{modifier}" style="--i:{index}" pathLength="1" '
        f'd="{d}" {NS} stroke="{color}" stroke-opacity="{lift(opacity)}" '
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
    return f'<g class="art-nodes{modifier}" fill="{fill}" fill-opacity="{lift(opacity)}">{body}</g>'


def hollow(circles, stroke=T, opacity=".18"):
    """Open nodes: page-coloured discs with a thin outline."""
    body = "".join(
        f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{r}"/>' for x, y, r in circles
    )
    return (
        f'<g class="art-nodes" fill="var(--bg)" stroke="{stroke}" '
        f'stroke-opacity="{lift(opacity)}" stroke-width="1.5">{body}</g>'
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


def motif(name, width, height, body, anchor=None, baseline=None, scale=None):
    """One SVG in the background field, spanning the main area.

    anchor is a section id, and the page script centres the motif on the
    divider line above that section, where the margins are quiet. Pass
    (section id, "middle") to centre it inside the section, or
    (section id, "start") to begin it at the section's top edge. Without an
    anchor the script centres it in the About section.

    Each motif carries a whisper of crimson wash in its two margins, behind
    the line work, so the art sits on warm paper rather than flat white.
    Keep it very low: it stacks with the hero wash at the top of the page.
    """
    if not anchor:
        data = ' data-hero=""'
    elif isinstance(anchor, tuple):
        data = f' data-section="{anchor[0]}" data-align="{anchor[1]}"'
    else:
        data = f' data-section="{anchor}"'
    # A figure with a baseline is sat on its divider by that baseline (rather
    # than centred on it by its box), masked to meet the rule end to end, and
    # held still. scale stretches it taller. Both live here, not in the
    # markup, so a regeneration cannot lose them.
    if baseline is not None:
        data += f' data-baseline="{fmt(baseline)}"'
    if scale is not None:
        data += f' data-scale="{scale}"'

    defs = "".join(
        f'<radialGradient id="wash-{name}-{side}" cx="{cx}" cy=".5" r=".55">'
        f'<stop offset="0" stop-color="{A}" stop-opacity=".026"/>'
        f'<stop offset="1" stop-color="{A}" stop-opacity="0"/>'
        f'</radialGradient>'
        for side, cx in (("left", "0"), ("right", "1"))
    )
    wash = "".join(
        f'<rect width="{width}" height="{height}" fill="url(#wash-{name}-{side})"/>'
        for side in ("left", "right")
    )

    out = svg(f"motif motif--{name}", width, height, wash + body, defs)
    return out.replace("<svg ", f'<svg preserveAspectRatio="none"{data} ', 1)


def posterior(peak=85, anchor="research"):
    """Bayesian updating along one baseline: a wide prior narrowing to a posterior.

    Six distributions, three in each margin. The wide, low prior is at the
    far left and each one after it is narrower and taller, ending in the
    crimson posterior at the right. The means and spreads are set so all
    three bells sit whole inside their margin at any viewport width.
    """
    W = 1240
    # (mean, spread, colour, opacity, stroke width), prior first
    curves = [
        (35, 68, T, ".095", "1.5"),      # prior
        (100, 50, T, ".125", "1.55"),    # update 1
        (165, 38, T, ".155", "1.6"),     # update 2
        (1070, 24, T, ".155", "1.6"),    # update 3
        (1135, 18, T, ".21", "1.7"),   # update 4
        (1195, 13, A, ".40", "2.6"),    # posterior
    ]
    heights = [peak * (68 / s) ** 0.5 for _, s, _, _, _ in curves]

    pad = 24
    H = max(heights) + 2 * pad
    base = H - pad

    # still: the baseline meets the page's own divider and must not bob
    body = line(f"M0 {fmt(base)} H{W}", T, ".075", "1.2", index=0, still=True)
    for i, ((mu, s, colour, opacity, width), h) in enumerate(zip(curves, heights)):
        x0, x1 = max(0, mu - 4 * s), min(W, mu + 4 * s)
        body += line(
            gaussian(x0, x1, mu, s, base, h), colour, opacity, width,
            signal=colour == A, index=i + 1,
        )
    return motif("posterior", W, fmt(H), body, anchor=anchor,
                 baseline=base, scale=1.3 if anchor is None else None)


def clusters():
    """Three patient clusters: right, left, then right again, faintly linked."""
    W = 1240
    scale = 1.4
    first, second, third = (1120, 185), (118, 600), (1122, 1015)
    body = cluster(*first, scale=scale, index=0)
    body += cluster(*second, scale=scale, index=2)
    body += cluster(*third, scale=scale, index=4)
    body += line(
        smooth([(940, 330), (760, 405), (560, 450), (360, 490), (230, 515)]),
        T, ".065", "1.3", index=6,
    )
    body += line(
        smooth([(280, 740), (470, 810), (660, 855), (850, 900), (950, 930)]),
        T, ".065", "1.3", index=7,
    )
    ry = 112 * scale
    H, body = fit(body, first[1] - ry - 18, third[1] + ry + 18)
    return motif("clusters", W, H, body, anchor=("publications", "start"))


def envelope(rising):
    """A personal reference interval inside the population one.

    A wandering centre line, a wide grey envelope, a narrow crimson envelope,
    and a few measurements in each margin. One point sits outside the
    personal band but inside the population one: normal for the population,
    abnormal for the person.

    Both longitudinal motifs come from this one shape so they stay
    consistent: rising=True mirrors it vertically so it climbs instead of
    falling.
    """
    W = 1240

    def centre(x):
        y = 150 + 240 * x / W + 16 * math.sin(x / 92) + 7 * math.sin(x / 41 + 1.3)
        return 540 - y if rising else y

    xs = list(range(0, W + 1, 20))

    def band(offset):
        return smooth([(x, centre(x) + offset) for x in xs])

    body = (
        line(band(-70), T, ".075", "1.5", index=0)
        + line(band(70), T, ".075", "1.5", index=1)
        + line(band(-22), A, ".26", "2.2", signal=True, index=2)
        + line(band(22), A, ".26", "2.2", signal=True, index=3)
    )
    samples = [(50, -8), (108, 6), (168, -12), (226, 4), (1030, 10), (1090, -6), (1150, 8), (1206, -4)]
    body += hollow([(x, centre(x) + dy, 3) for x, dy in samples], T, ".2")
    outlier = centre(1120) - 50
    body += dots([(1120, outlier, 3.4)], A, ".48", signal=True)

    top = min(min(centre(x) for x in xs) - 74, outlier - 4)
    return fit(body, top, max(centre(x) for x in xs) + 74)


def trajectories():
    """The reference interval climbing from left to right."""
    H, body = envelope(rising=True)
    # Centred inside Research rather than on the divider above it: Education is
    # short, and centred on that divider the figure climbs into the hero bells.
    return motif("trajectories", 1240, H, body, anchor=("research", "middle"))


def interval():
    """The same interval, falling from left to right."""
    H, body = envelope(rising=False)
    return motif("interval", 1240, H, body, anchor="community")


def trace():
    """One ECG strip across the page: a P wave in the left margin, the same
    flat baseline behind the text, the QRS spike and T wave in the right."""
    W = 1240
    base = 200
    signal = (
        f"M0 {base} H70 C90 {base} 96 182 116 182 C136 182 142 {base} 162 {base} "
        f"H1040 C1056 {base} 1060 196 1066 188 L1074 176 L1088 240 L1106 110 L1122 226 L1134 {base} "
        f"H1170 C1184 {base} 1188 178 1204 178 C1220 178 1224 {base} {W} {base}"
    )
    body = (
        # still: the flat segments run into the page's divider and must not bob
        line(signal, A, ".34", "2.6", signal=True, index=0, still=True)
        + hollow([(40, base, 4), (162, base, 4), (1040, base, 4), (1134, base, 4)], T, ".16")
        + dots([(1106, 110, 3.6)], A, ".48", signal=True)
    )
    top_extent, pad = 110 - 4, 24               # the T wave peak; fit() pads by 24
    H, body = fit(body, top_extent, 240 + 2, pad)   # ... down to the S trough
    return motif("trace", W, H, body, anchor="experience",
                 baseline=base + pad - top_extent)


# -------------------------------------------------------------- hero wash


def network():
    """A small network across the page: inputs at the left, output at the
    right, one crimson path lit through it."""
    W = 1240
    layers = [
        [(22, 55), (22, 165), (22, 275), (22, 385)],
        [(200, 110), (200, 220), (200, 330)],
        [(1040, 110), (1040, 220), (1040, 330)],
        [(1218, 220)],
    ]
    path = [layers[0][2], layers[1][1], layers[2][1], layers[3][0]]
    body = ""
    for a, b in zip(layers, layers[1:]):
        # Connections between the margins run behind the text.
        opacity = ".05" if a[0][0] < W / 2 < b[0][0] else ".08"
        for (x1, y1) in a:
            for (x2, y2) in b:
                body += line(f"M{x1} {y1} L{x2} {y2}", T, opacity, "1.2", index=0)
    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        body += line(f"M{x1} {y1} L{x2} {y2}", A, ".32", "2.3", signal=True, index=1)
    others = [n for layer in layers for n in layer if n not in path]
    body += hollow([(x, y, 6) for x, y in others], T, ".2")
    body += dots([(x, y, 5) for x, y in path], A, ".46", signal=True)
    H, body = fit(body, 55 - 7, 385 + 7)
    return motif("network", W, H, body, anchor="community")


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
        posterior(anchor=None),   # the About background
        trajectories(),
        clusters(),
        trace(),
        interval(),               # network() is kept above but no longer placed
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
