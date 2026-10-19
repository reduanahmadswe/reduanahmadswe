import html
from gen import *


def chip(x, y, t, pal):
    tw = 22 + len(t) * 8.2
    return (f'<rect x="{x}" y="{y}" width="{tw}" height="30" rx="15" fill="{pal[1]}" fill-opacity=".25" stroke="{pal[0]}" stroke-opacity=".6"/>'
            f'<text x="{x+tw/2}" y="{y+20}" font-size="13" font-weight="700" text-anchor="middle" fill="{pal[0]}" font-family="{SANS}">{html.escape(t)}</text>'), tw + 10


def chips(x, y, items, pal):
    out, cx = "", x
    for t in items:
        s, adv = chip(cx, y, t, pal)
        out += s
        cx += adv
    return out


def row(y, label, body, ic):
    return (f'<text x="60" y="{y}" font-size="12" font-weight="800" fill="#6f86a0" font-family="{SANS}" letter-spacing="2">{ic}  {label}</text>{body}')


def about():
    w, h = 1200, 470
    c, v, o, g = PAL["c"], PAL["v"], PAL["o"], PAL["g"]
    body = ""
    body += row(150, "ROLE", f'<text x="60" y="180" font-size="24" font-weight="800" fill="#fff" font-family="{SANS}">Full-Stack Developer</text>', "◆")
    body += row(222, "EDUCATION", f'<text x="60" y="252" font-size="20" font-weight="700" fill="#e6f1ff" font-family="{SANS}">B.Sc. in Software Engineering</text><text x="60" y="276" font-size="15" fill="#8fa3b8" font-family="{SANS}">Daffodil International University</text>', "◆")
    body += row(318, "LOCATION", f'<text x="60" y="348" font-size="20" font-weight="700" fill="#e6f1ff" font-family="{SANS}">Dhaka, Bangladesh</text>', "◆")
    body += row(390, "FUN FACT", f'<text x="60" y="420" font-size="18" fill="#cfe3f7" font-family="{SANS}">I solve problems on LeetCode for fun</text>', "◆")
    right = ""
    right += f'<text x="640" y="150" font-size="12" font-weight="800" fill="#6f86a0" font-family="{SANS}" letter-spacing="2">◆  CORE STACK</text>'
    right += chips(640, 166, ["React", "Next.js", "TypeScript"], c)
    right += chips(640, 206, ["Node.js", "Express", "MongoDB"], g)
    right += chips(640, 246, ["PostgreSQL", "Tailwind CSS"], v)
    right += f'<text x="640" y="318" font-size="12" font-weight="800" fill="#6f86a0" font-family="{SANS}" letter-spacing="2">◆  CURRENTLY LEARNING</text>'
    right += chips(640, 334, ["System Design", "Cloud & DevOps"], o)
    right += chips(640, 374, ["AI Integrations"], o)
    # progress bars
    bars = ""
    for i, (n, p, pal) in enumerate([("Frontend", 90, c), ("Backend", 85, g), ("Problem Solving", 80, v)]):
        yy = 410 + i * 0
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
{STYLE}{DEFS}
<rect x="22" y="22" width="1156" height="426" rx="26" fill="#0077a3" opacity=".6"/>
<rect x="16" y="16" width="1156" height="426" rx="26" fill="#00a6c7" opacity=".7"/>
<rect x="10" y="10" width="1156" height="426" rx="26" fill="url(#bg)" stroke="#7df3ff" stroke-opacity=".5" stroke-width="1.5"/>
<circle cx="1000" cy="120" r="200" fill="url(#orb)" class="glow"/>
<circle cx="40" cy="44" r="6" fill="#ff5f56"/><circle cx="62" cy="44" r="6" fill="#ffbd2e"/><circle cx="84" cy="44" r="6" fill="#27c93f"/>
<text x="600" y="49" font-size="13" text-anchor="middle" fill="#6f86a0" font-family="'Fira Code',Consolas,monospace">reduan@portfolio: ~/about</text>
<text x="60" y="104" font-size="30" font-weight="900" fill="url(#face2)" font-family="{SANS}">Hi, I'm Reduan 👋</text>
<line x1="60" y1="118" x2="1116" y2="118" stroke="#7df3ff" stroke-opacity=".2"/>
<line x1="600" y1="140" x2="600" y2="420" stroke="#7df3ff" stroke-opacity=".15"/>
{body}
{right}
<g class="float" style="animation-duration:5s">{cube(1060, 330, 44, "#7df3ff", "#00a6c7", "#0077a3", 0)}</g>
<g class="float" style="animation-delay:1s">{cube(1000, 395, 22, "#d7c4ff", "#8b5cf6", "#5b34c9", 1)}</g>
</svg>"""


wr("about.svg", about())
print("about ok")
