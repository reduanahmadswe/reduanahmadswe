import os, html
OUT = r"E:\reduanahmadswe\assets"
os.makedirs(OUT, exist_ok=True)
SANS = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
FONT = f'font-family="{SANS}" font-weight="900"'


def cube(x, y, s, c1, c2, c3, delay, dur=4):
    h = s * 0.5
    top = f"{x},{y-s} {x+s*0.87},{y-s+h} {x},{y-s+2*h} {x-s*0.87},{y-s+h}"
    left = f"{x-s*0.87},{y-s+h} {x},{y-s+2*h} {x},{y+s} {x-s*0.87},{y+h}"
    right = f"{x+s*0.87},{y-s+h} {x},{y-s+2*h} {x},{y+s} {x+s*0.87},{y+h}"
    return (f'<g class="float" style="animation-delay:{delay}s;animation-duration:{dur}s">'
            f'<polygon points="{top}" fill="{c1}"/><polygon points="{left}" fill="{c2}"/>'
            f'<polygon points="{right}" fill="{c3}"/></g>')


def extruded(text, x, y, size, depth, top_fill, side_dark, side_light):
    layers = []
    for i in range(depth, 0, -1):
        col = side_dark if i > depth * 0.5 else side_light
        layers.append(f'<text x="{x+i*0.9:.1f}" y="{y+i*0.9:.1f}" font-size="{size}" {FONT} text-anchor="middle" fill="{col}">{text}</text>')
    layers.append(f'<text x="{x}" y="{y}" font-size="{size}" {FONT} text-anchor="middle" fill="{top_fill}">{text}</text>')
    return "\n".join(layers)


STYLE = """<style>
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-14px)}}
@keyframes tilt{0%,100%{transform:rotate(-1deg)}50%{transform:rotate(1deg)}}
@keyframes glow{0%,100%{opacity:.5}50%{opacity:1}}
@keyframes grid{from{stroke-dashoffset:0}to{stroke-dashoffset:-28}}
.float{animation:fl 4s ease-in-out infinite}
.tilt{animation:tilt 6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
.glow{animation:glow 3s ease-in-out infinite}
.gl{animation:grid 1.5s linear infinite}
</style>"""

DEFS = """<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b0f1a"/><stop offset=".5" stop-color="#101a33"/><stop offset="1" stop-color="#0a1626"/></linearGradient>
<linearGradient id="face" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#8fe9ff"/></linearGradient>
<linearGradient id="face2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#00d9ff"/><stop offset="1" stop-color="#a78bfa"/></linearGradient>
<radialGradient id="orb" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#00d9ff" stop-opacity=".35"/><stop offset="1" stop-color="#00d9ff" stop-opacity="0"/></radialGradient>
<filter id="sh" x="-20%" y="-20%" width="140%" height="170%"><feDropShadow dx="0" dy="14" stdDeviation="10" flood-color="#000" flood-opacity=".6"/></filter>
</defs>"""


def floor(w, h, y0):
    g = ['<g opacity=".5" stroke="#00d9ff" stroke-width="1" fill="none">']
    cx = w / 2
    for i in range(-14, 15):
        g.append(f'<line x1="{cx+i*28}" y1="{y0}" x2="{cx+i*140}" y2="{h}"/>')
    for k in range(1, 9):
        yy = y0 + (h - y0) * (k / 8) ** 2
        g.append(f'<line x1="0" y1="{yy:.1f}" x2="{w}" y2="{yy:.1f}"/>')
    g.append("</g>")
    return "\n".join(g)


def header():
    w, h = 1200, 380
    cubes = (cube(130, 150, 46, "#7df3ff", "#00a6c7", "#0077a3", 0)
             + cube(1070, 120, 38, "#d7c4ff", "#8b5cf6", "#5b34c9", .8)
             + cube(230, 280, 26, "#ffe08a", "#f59e0b", "#b45309", 1.4)
             + cube(980, 270, 30, "#ffb3c1", "#ef4444", "#991b1b", .4)
             + cube(60, 300, 18, "#9affc2", "#10b981", "#047857", 2)
             + cube(1150, 250, 20, "#7df3ff", "#00a6c7", "#0077a3", 1.1))
    title = extruded("REDUAN AHMAD", 600, 190, 96, 14, "url(#face)", "#07324a", "#0b6e94")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
{STYLE}{DEFS}
<rect width="{w}" height="{h}" rx="24" fill="url(#bg)"/>
<circle cx="600" cy="170" r="330" fill="url(#orb)" class="glow"/>
{floor(w, h, 270)}
{cubes}
<g class="tilt" filter="url(#sh)">{title}</g>
<text x="600" y="248" font-size="26" {FONT} text-anchor="middle" fill="url(#face2)" letter-spacing="4">FULL-STACK DEVELOPER  •  SOFTWARE ENGINEER</text>
<text x="600" y="296" font-size="17" text-anchor="middle" fill="#9fb3c8" font-family="{SANS}" letter-spacing="2">MERN  ·  NEXT.JS  ·  TYPESCRIPT  ·  DHAKA, BANGLADESH</text>
</svg>"""


def banner(label):
    w, h = 1200, 120
    t = html.escape(label.upper())
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
{STYLE}{DEFS}
<rect width="{w}" height="{h}" rx="18" fill="url(#bg)"/>
<line x1="40" y1="106" x2="1160" y2="106" stroke="#00d9ff" stroke-opacity=".4" stroke-dasharray="6 8" class="gl"/>
{cube(90, 58, 24, "#7df3ff", "#00a6c7", "#0077a3", 0, 3)}
{cube(1110, 58, 24, "#d7c4ff", "#8b5cf6", "#5b34c9", .6, 3)}
<g class="tilt" filter="url(#sh)">{extruded(t, 600, 74, 46, 9, "url(#face)", "#07324a", "#0b6e94")}</g>
</svg>"""


PAL = {"c": ("#7df3ff", "#00a6c7", "#0077a3"), "v": ("#d7c4ff", "#8b5cf6", "#5b34c9"),
       "o": ("#ffe08a", "#f59e0b", "#b45309"), "r": ("#ffb3c1", "#ef4444", "#991b1b"),
       "g": ("#9affc2", "#10b981", "#047857")}


def card(idx, title, sub, tags, color):
    w, h = 560, 230
    pal = PAL[color]
    tg, x = "", 40
    for t in tags:
        tw = 24 + len(t) * 8
        tg += (f'<rect x="{x}" y="172" width="{tw}" height="28" rx="14" fill="{pal[1]}" opacity=".3"/>'
               f'<text x="{x+tw/2}" y="191" font-size="13" font-weight="700" text-anchor="middle" fill="{pal[0]}" font-family="{SANS}">{html.escape(t)}</text>')
        x += tw + 10
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
{STYLE}{DEFS}
<rect x="14" y="14" width="{w-28}" height="{h-28}" rx="22" fill="{pal[2]}" opacity=".6" transform="translate(10 12)"/>
<rect x="14" y="14" width="{w-28}" height="{h-28}" rx="22" fill="{pal[1]}" opacity=".7" transform="translate(5 6)"/>
<rect x="14" y="14" width="{w-28}" height="{h-28}" rx="22" fill="url(#bg)" stroke="{pal[0]}" stroke-opacity=".6" stroke-width="1.5"/>
<circle cx="{w-100}" cy="90" r="90" fill="{pal[0]}" opacity=".1" class="glow"/>
{cube(w-100, 90, 36, *pal, idx*0.5, 4)}
<text x="40" y="76" font-size="30" font-weight="900" fill="#ffffff" font-family="{SANS}">{html.escape(title)}</text>
<text x="40" y="112" font-size="15" fill="#9fb3c8" font-family="{SANS}">{html.escape(sub[0])}</text>
<text x="40" y="136" font-size="15" fill="#9fb3c8" font-family="{SANS}">{html.escape(sub[1])}</text>
{tg}
</svg>"""


def footer():
    w, h = 1200, 200
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
{STYLE}{DEFS}
<rect width="{w}" height="{h}" rx="24" fill="url(#bg)"/>
{floor(w, h, 112)}
{cube(150, 70, 30, "#7df3ff", "#00a6c7", "#0077a3", 0)}
{cube(1050, 70, 30, "#d7c4ff", "#8b5cf6", "#5b34c9", .7)}
<g class="tilt" filter="url(#sh)">{extruded("LET'S BUILD SOMETHING GREAT", 600, 80, 44, 9, "url(#face)", "#07324a", "#0b6e94")}</g>
<text x="600" y="150" font-size="16" text-anchor="middle" fill="#9fb3c8" font-family="{SANS}" letter-spacing="2">MADE WITH LOVE IN BANGLADESH  ·  © 2025 REDUAN AHMAD</text>
</svg>"""


def wr(name, s):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(s)


wr("header.svg", header())
for k, lab in {"about": "About Me", "projects": "Featured Projects", "stack": "Tech Stack",
               "stats": "GitHub Universe", "cp": "Problem Solving", "contact": "Contact"}.items():
    wr(f"banner-{k}.svg", banner(lab))
wr("card-mama.svg", card(0, "Mama Bazar", ("Online grocery & lifestyle store", "delivering essentials across Bangladesh"), ["E-commerce", "Full-Stack"], "g"))
wr("card-micro.svg", card(1, "MicroLearning", ("AI-powered 1-2 minute micro lessons", "on literally any topic"), ["AI", "EdTech", "Next.js"], "v"))
wr("card-oriyet.svg", card(2, "ORIYET", ("Educational platform: events, certificates", "and expert connections"), ["EdTech", "Events"], "c"))
wr("card-mbl.svg", card(3, "MBL Global Academy", ("Courses, podcasts, testimonials and", "executive leadership development"), ["Education", "Website"], "o"))
wr("card-provet.svg", card(4, "Provet Resources", ("Poultry nutrition & feed solutions", "company website in Bangladesh"), ["Corporate", "AgriTech"], "r"))
wr("card-gc.svg", card(5, "GC ServiceX", ("Business development and", "growth services website"), ["Business", "Corporate"], "v"))
wr("footer.svg", footer())
print(sorted(os.listdir(OUT)))
