"""Builds assets/contrib-3d.svg and assets/activity.svg from the public GitHub contributions calendar.

No token needed. Usage: python scripts/contrib3d.py [username]
"""
import os, re, sys, urllib.request

USER = sys.argv[1] if len(sys.argv) > 1 else "reduanahmadswe"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
SANS = "'Segoe UI','Helvetica Neue',Arial,sans-serif"

req = urllib.request.Request(f"https://github.com/users/{USER}/contributions", headers={"User-Agent": "Mozilla/5.0"})
page = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")

cells = {}
for m in re.finditer(r'<td[^>]*data-date="([^"]+)"[^>]*id="contribution-day-component-(\d+)-(\d+)"[^>]*data-level="(\d)"', page):
    cells[(int(m.group(3)), int(m.group(2)))] = [m.group(1), int(m.group(4)), 0]
counts = {}
for m in re.finditer(r'for="(contribution-day-component-\d+-\d+)"[^>]*>\s*(No|\d+) contributions?', page):
    counts[m.group(1)] = 0 if m.group(2) == "No" else int(m.group(2))
for (c, r), v in cells.items():
    v[2] = counts.get(f"contribution-day-component-{r}-{c}", 0)

weeks = max(c for c, _ in cells) + 1
total = sum(v[2] for v in cells.values())
best = max(v[2] for v in cells.values()) or 1
print("weeks", weeks, "total", total, "max", best)

LEVEL = {0: ("#1b2433", "#141b27", "#0f1520"), 1: ("#4fe3ff", "#1ba6c4", "#0f7a96"), 2: ("#38c7f5", "#1587b8", "#0c5f8c"),
         3: ("#8b7bff", "#5b4bd1", "#3b2fa0"), 4: ("#d4a3ff", "#9b5de5", "#6a35b0")}

# ---------- 3D bars (oblique projection) ----------
W, H = 1200, 440
BW, SX, SY = 17.0, 7.0, 6.0
bars = []
for (c, r), (date, lvl, n) in sorted(cells.items(), key=lambda kv: (kv[0][1], kv[0][0])):
    bx = 28 + c * 19.5 + (6 - r) * 8.5
    by = 400 - (6 - r) * 13
    h = 3 if n == 0 else 6 + 82 * (n / best) ** 0.5
    top, left, right = LEVEL[lvl]
    front = f"{bx},{by-h} {bx+BW},{by-h} {bx+BW},{by} {bx},{by}"
    topf = f"{bx},{by-h} {bx+BW},{by-h} {bx+BW+SX},{by-h-SY} {bx+SX},{by-h-SY}"
    side = f"{bx+BW},{by-h} {bx+BW+SX},{by-h-SY} {bx+BW+SX},{by-SY} {bx+BW},{by}"
    delay = (c * 0.05) % 5
    bars.append(
        f'<g class="b" style="animation-delay:{delay:.2f}s"><polygon points="{front}" fill="{left}"/><polygon points="{side}" fill="{right}"/>'
        f'<polygon points="{topf}" fill="{top}"/><title>{date}: {n}</title></g>')

svg3d = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>@keyframes rise{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes glow{{0%,100%{{opacity:.5}}50%{{opacity:1}}}}
.b{{animation:rise .8s ease-out both}}.gl{{animation:glow 4s ease-in-out infinite}}</style>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b0f1a"/><stop offset=".5" stop-color="#101a33"/><stop offset="1" stop-color="#0a1626"/></linearGradient>
<radialGradient id="o" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#00d9ff" stop-opacity=".25"/><stop offset="1" stop-color="#00d9ff" stop-opacity="0"/></radialGradient></defs>
<rect width="{W}" height="{H}" rx="24" fill="url(#bg)"/>
<ellipse cx="600" cy="260" rx="520" ry="170" fill="url(#o)" class="gl"/>
<g>{''.join(bars)}</g>
<text x="40" y="60" font-size="22" font-weight="800" fill="#fff" font-family="{SANS}">{total:,} contributions</text>
<text x="40" y="86" font-size="14" fill="#8fa3b8" font-family="{SANS}">in the last year  ·  best day: {best}</text>
<g font-family="{SANS}" font-size="12" fill="#8fa3b8"><text x="40" y="{H-26}">Less</text>
{''.join(f'<rect x="{80+i*20}" y="{H-37}" width="14" height="14" rx="3" fill="{LEVEL[i][0]}"/>' for i in range(5))}
<text x="190" y="{H-26}">More</text></g>
</svg>"""

# ---------- weekly activity area chart ----------
weekly = [sum(cells[(c, r)][2] for r in range(7) if (c, r) in cells) for c in range(weeks)]
CW, CH, pad = 1200, 300, 50
mx = max(weekly) or 1
pts = [(pad + i * (CW - 2 * pad) / (weeks - 1), CH - 50 - (v / mx) * (CH - 110)) for i, v in enumerate(weekly)]


def smooth(p):
    d = f"M{p[0][0]:.1f},{p[0][1]:.1f}"
    for i in range(1, len(p)):
        cx = (p[i - 1][0] + p[i][0]) / 2
        d += f" C{cx:.1f},{p[i-1][1]:.1f} {cx:.1f},{p[i][1]:.1f} {p[i][0]:.1f},{p[i][1]:.1f}"
    return d


line = smooth(pts)
area = line + f" L{pts[-1][0]:.1f},{CH-50} L{pts[0][0]:.1f},{CH-50} Z"
dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#fff"><title>{v}</title></circle>' for (x, y), v in zip(pts, weekly) if v == mx)
grid = "".join(f'<line x1="{pad}" x2="{CW-pad}" y1="{CH-50-i*(CH-110)/4:.0f}" y2="{CH-50-i*(CH-110)/4:.0f}" stroke="#fff" stroke-opacity=".06"/>' for i in range(5))
svgact = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}">
<style>@keyframes dash{{from{{stroke-dashoffset:3000}}to{{stroke-dashoffset:0}}}}.ln{{stroke-dasharray:3000;animation:dash 4s ease-out forwards}}</style>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b0f1a"/><stop offset="1" stop-color="#0a1626"/></linearGradient>
<linearGradient id="a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#00d9ff" stop-opacity=".55"/><stop offset="1" stop-color="#a78bfa" stop-opacity="0"/></linearGradient>
<linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="#00d9ff"/><stop offset="1" stop-color="#a78bfa"/></linearGradient></defs>
<rect width="{CW}" height="{CH}" rx="24" fill="url(#bg)"/>{grid}
<path d="{area}" fill="url(#a)"/><path class="ln" d="{line}" fill="none" stroke="url(#l)" stroke-width="3.5" stroke-linecap="round"/>{dots}
<text x="40" y="44" font-size="20" font-weight="800" fill="#fff" font-family="{SANS}">Weekly Activity</text>
<text x="{CW-40}" y="44" text-anchor="end" font-size="13" fill="#8fa3b8" font-family="{SANS}">peak week: {mx} contributions</text>
</svg>"""

for name, s in (("contrib-3d.svg", svg3d), ("activity.svg", svgact)):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(s)
print("written")
