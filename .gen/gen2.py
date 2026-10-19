import random, html
import gen  # regenerates base assets
from gen import *

random.seed(7)


def stars(w, h, n, ymax=None):
    ymax = ymax or h
    out = []
    for _ in range(n):
        x, y = random.uniform(5, w - 5), random.uniform(5, ymax)
        r = random.choice([0.8, 1, 1.4, 1.8])
        d = random.uniform(1.5, 4)
        b = random.uniform(0, 3)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff"><animate attributeName="opacity" values="0.1;1;0.1" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></circle>')
    return "\n".join(out)


SHIMMER = """<linearGradient id="shim" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="300" y2="0">
<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-400 0;1300 0" dur="4s" repeatCount="indefinite"/></linearGradient>"""


def header2():
    w, h = 1200, 400
    cubes = (cube(130, 150, 46, "#7df3ff", "#00a6c7", "#0077a3", 0)
             + cube(1070, 120, 38, "#d7c4ff", "#8b5cf6", "#5b34c9", .8)
             + cube(230, 290, 26, "#ffe08a", "#f59e0b", "#b45309", 1.4)
             + cube(980, 285, 30, "#ffb3c1", "#ef4444", "#991b1b", .4)
             + cube(60, 310, 18, "#9affc2", "#10b981", "#047857", 2)
             + cube(1150, 260, 20, "#7df3ff", "#00a6c7", "#0077a3", 1.1)
             + cube(330, 70, 16, "#d7c4ff", "#8b5cf6", "#5b34c9", 1.7)
             + cube(880, 60, 16, "#9affc2", "#10b981", "#047857", 2.3))
    title = extruded("REDUAN AHMAD", 600, 200, 100, 15, "url(#face)", "#07324a", "#0b6e94")
    shine = f'<text x="600" y="200" font-size="100" {FONT} text-anchor="middle" fill="url(#shim)">REDUAN AHMAD</text>'
    orbit = """<g fill="none" stroke="#00d9ff" stroke-opacity=".25"><ellipse cx="600" cy="170" rx="520" ry="110"><animateTransform attributeName="transform" type="rotate" from="0 600 170" to="360 600 170" dur="40s" repeatCount="indefinite"/></ellipse>
<ellipse cx="600" cy="170" rx="470" ry="80" stroke="#a78bfa"><animateTransform attributeName="transform" type="rotate" from="360 600 170" to="0 600 170" dur="55s" repeatCount="indefinite"/></ellipse></g>"""
    chips = ""
    for i, t in enumerate(["REACT", "NEXT.JS", "NODE.JS", "TYPESCRIPT", "MONGODB"]):
        cx = 330 + i * 135
        chips += (f'<g class="float" style="animation-delay:{i*.3}s"><rect x="{cx-52}" y="318" width="104" height="30" rx="15" fill="#00d9ff" fill-opacity=".12" stroke="#00d9ff" stroke-opacity=".6"/>'
                  f'<text x="{cx}" y="338" font-size="13" font-weight="800" text-anchor="middle" fill="#8fe9ff" font-family="{SANS}" letter-spacing="1">{t}</text></g>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
{STYLE}{DEFS}<defs>{SHIMMER}</defs>
<rect width="{w}" height="{h}" rx="24" fill="url(#bg)"/>
{stars(w, h, 70, 260)}
<circle cx="600" cy="170" r="340" fill="url(#orb)" class="glow"/>
{orbit}
{floor(w, h, 285)}
{cubes}
<g class="tilt" filter="url(#sh)">{title}{shine}</g>
<text x="600" y="258" font-size="26" {FONT} text-anchor="middle" fill="url(#face2)" letter-spacing="5">FULL-STACK DEVELOPER  •  SOFTWARE ENGINEER</text>
<text x="600" y="296" font-size="16" text-anchor="middle" fill="#9fb3c8" font-family="{SANS}" letter-spacing="3">DHAKA, BANGLADESH</text>
{chips}
</svg>"""


def stats():
    w, h = 1200, 200
    items = [("2+", "YEARS EXPERIENCE", "c"), ("15+", "PROJECTS BUILT", "v"), ("10+", "CERTIFICATIONS", "o"), ("15+", "TECHNOLOGIES", "g")]
    out = ""
    for i, (n, lab, c) in enumerate(items):
        p = PAL[c]
        x = 20 + i * 292
        out += f"""<g class="float" style="animation-delay:{i*.4}s;animation-duration:5s">
<rect x="{x+9}" y="{29}" width="264" height="140" rx="20" fill="{p[2]}" opacity=".7"/>
<rect x="{x+4}" y="{24}" width="264" height="140" rx="20" fill="{p[1]}" opacity=".8"/>
<rect x="{x}" y="20" width="264" height="140" rx="20" fill="url(#bg)" stroke="{p[0]}" stroke-opacity=".7" stroke-width="1.5"/>
{extruded(n, x+132, 100, 58, 7, "url(#face)", p[2], p[1])}
<text x="{x+132}" y="138" font-size="13" font-weight="800" text-anchor="middle" fill="{p[0]}" font-family="{SANS}" letter-spacing="2">{lab}</text></g>"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
{STYLE}{DEFS}{out}</svg>"""


SKILLS = [
    ("JS", "JavaScript", "#f7df1e", "#000"), ("TS", "TypeScript", "#3178c6", "#fff"), ("C++", "C++", "#00599c", "#fff"), ("Jv", "Java", "#ed8b00", "#fff"),
    ("Py", "Python", "#3776ab", "#fff"), ("Re", "React", "#20232a", "#61dafb"), ("Nx", "Next.js", "#111", "#fff"), ("No", "Node.js", "#339933", "#fff"),
    ("Ex", "Express", "#222", "#fff"), ("Tw", "Tailwind", "#06b6d4", "#fff"), ("Mo", "MongoDB", "#47a248", "#fff"), ("Pg", "PostgreSQL", "#4169e1", "#fff"),
    ("My", "MySQL", "#4479a1", "#fff"), ("Fb", "Firebase", "#ffca28", "#000"), ("Gt", "Git & GitHub", "#f05032", "#fff"), ("Vc", "Vercel", "#000", "#fff"),
]


def skills():
    w, h = 1200, 400
    out = ""
    for i, (mono, name, bg, fg) in enumerate(SKILLS):
        r, c = divmod(i, 8)
        x, y = 22 + c * 145, 40 + r * 180
        dly = (i % 8) * .25
        out += f"""<g class="float" style="animation-delay:{dly}s;animation-duration:{4+(i%3)*.5}s">
<rect x="{x+10}" y="{y+12}" width="120" height="120" rx="22" fill="#000" opacity=".45"/>
<rect x="{x+6}" y="{y+8}" width="120" height="120" rx="22" fill="{bg}" opacity=".55"/>
<rect x="{x+3}" y="{y+4}" width="120" height="120" rx="22" fill="{bg}" opacity=".8"/>
<rect x="{x}" y="{y}" width="120" height="120" rx="22" fill="{bg}"/>
<rect x="{x}" y="{y}" width="120" height="60" rx="22" fill="#fff" opacity=".12"/>
<text x="{x+60}" y="{y+68}" font-size="40" font-weight="900" text-anchor="middle" fill="{fg}" font-family="{SANS}">{mono}</text>
<text x="{x+60}" y="{y+100}" font-size="13" font-weight="700" text-anchor="middle" fill="{fg}" font-family="{SANS}">{html.escape(name)}</text></g>"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
{STYLE}{DEFS}<rect width="{w}" height="{h}" rx="24" fill="url(#bg)"/>
{stars(w, h, 40)}
{out}</svg>"""


def divider():
    w, h = 1200, 40
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><linearGradient id="d" x1="0" x2="1"><stop offset="0" stop-color="#00d9ff" stop-opacity="0"/><stop offset=".5" stop-color="#a78bfa"/><stop offset="1" stop-color="#00d9ff" stop-opacity="0"/></linearGradient></defs>
<rect x="100" y="19" width="1000" height="2" fill="url(#d)"/>
<g transform="translate(600 20)"><polygon points="0,-11 10,-5.5 0,0 -10,-5.5" fill="#7df3ff"/><polygon points="-10,-5.5 0,0 0,11 -10,5.5" fill="#00a6c7"/><polygon points="10,-5.5 0,0 0,11 10,5.5" fill="#0077a3"/>
<animateTransform attributeName="transform" type="translate" values="600 20;600 15;600 20" dur="3s" repeatCount="indefinite"/></g>
</svg>"""


wr("header.svg", header2())
wr("stats.svg", stats())
wr("skills.svg", skills())
wr("divider.svg", divider())
print("ok")
