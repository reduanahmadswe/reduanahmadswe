"""Builds self-hosted stat cards (no third-party image services needed):

  assets/gh-stats.svg, assets/top-langs.svg, assets/streak.svg, assets/leetcode.svg

Data: GitHub REST API + public contributions calendar + LeetCode GraphQL.
Usage: python scripts/cards.py [github_user] [leetcode_user]
Optional env: GITHUB_TOKEN (higher API rate limit).
"""
import datetime, json, os, re, sys, urllib.request

USER = sys.argv[1] if len(sys.argv) > 1 else "reduanahmadswe"
LC_USER = sys.argv[2] if len(sys.argv) > 2 else USER
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
SANS = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "'Fira Code','Consolas',monospace"
W, H = 590, 240


def get(url, data=None, headers=None):
    h = {"User-Agent": "Mozilla/5.0", **(headers or {})}
    tok = os.environ.get("GITHUB_TOKEN")
    if tok and "api.github.com" in url:
        h["Authorization"] = f"Bearer {tok}"
    req = urllib.request.Request(url, data=data, headers=h)
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8")


def card(inner, h=H, title="", sub=""):
    head = ""
    if title:
        head = (f'<text x="32" y="46" font-size="19" font-weight="800" fill="#fff" font-family="{SANS}">{title}</text>'
                f'<text x="32" y="68" font-size="12" fill="#8fa3b8" font-family="{SANS}">{sub}</text>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
<style>@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
@keyframes glow{{0%,100%{{opacity:.45}}50%{{opacity:.9}}}}@keyframes pop{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
.bar{{transform-box:fill-box;transform-origin:left;animation:grow 1s ease-out both}}.gl{{animation:glow 4s ease-in-out infinite}}
</style>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b0f1a"/><stop offset=".55" stop-color="#101a33"/><stop offset="1" stop-color="#0a1626"/></linearGradient>
<linearGradient id="ac" x1="0" x2="1"><stop offset="0" stop-color="#00d9ff"/><stop offset="1" stop-color="#a78bfa"/></linearGradient>
<radialGradient id="o" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#00d9ff" stop-opacity=".22"/><stop offset="1" stop-color="#00d9ff" stop-opacity="0"/></radialGradient></defs>
<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="22" fill="url(#bg)" stroke="#1e2a44" stroke-width="2"/>
<circle cx="{W-60}" cy="30" r="150" fill="url(#o)" class="gl"/>
{head}{inner}</svg>"""


def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", name)


# ---------------- GitHub data ----------------
user = json.loads(get(f"https://api.github.com/users/{USER}"))
repos = [r for r in json.loads(get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")) if not r["fork"]]
stars = sum(r["stargazers_count"] for r in repos)
forks = sum(r["forks_count"] for r in repos)

page = get(f"https://github.com/users/{USER}/contributions")
days = {}
for m in re.finditer(r'data-date="([^"]+)"[^>]*id="(contribution-day-component-\d+-\d+)"', page):
    days[m.group(2)] = [m.group(1), 0]
for m in re.finditer(r'for="(contribution-day-component-\d+-\d+)"[^>]*>\s*(No|\d+) contributions?', page):
    if m.group(1) in days:
        days[m.group(1)][1] = 0 if m.group(2) == "No" else int(m.group(2))
series = sorted((datetime.date.fromisoformat(d), n) for d, n in days.values())
total = sum(n for _, n in series)
longest = cur = 0
for _, n in series:
    cur = cur + 1 if n else 0
    longest = max(longest, cur)
today = datetime.date.today()
cur = 0
for d, n in reversed(series):
    if d > today:
        continue
    if n:
        cur += 1
    elif d == today:  # today may still be empty
        continue
    else:
        break
print("total", total, "streak", cur, "longest", longest)

# ---------------- Stats card ----------------
items = [("Repositories", user["public_repos"], "#00d9ff"), ("Followers", user["followers"], "#a78bfa"),
         ("Stars earned", stars, "#00d9ff"), ("Contributions (1y)", total, "#a78bfa")]
inner = ""
for i, (label, val, col) in enumerate(items):
    x = 32 + (i % 2) * 270
    y = 110 + (i // 2) * 62
    inner += (f'<g><rect x="{x}" y="{y-28}" width="250" height="52" rx="14" fill="#ffffff" fill-opacity=".04" stroke="#1e2a44"/>'
              f'<rect x="{x}" y="{y-28}" width="5" height="52" rx="2.5" fill="{col}"/>'
              f'<text x="{x+22}" y="{y+8}" font-size="26" font-weight="800" fill="#fff" font-family="{SANS}">{val:,}</text>'
              f'<text x="{x+240}" y="{y+6}" text-anchor="end" font-size="12.5" fill="#8fa3b8" font-family="{SANS}">{label}</text></g>')
write("gh-stats.svg", card(inner, title="GitHub Stats", sub=f"@{USER}  ·  public activity"))

# ---------------- Top languages ----------------
langs = {}
for r in repos:
    try:
        for k, v in json.loads(get(r["languages_url"])).items():
            langs[k] = langs.get(k, 0) + v
    except Exception as e:
        print("lang fail", r["name"], e)
COL = {"JavaScript": "#f7df1e", "TypeScript": "#3178c6", "Python": "#4b8bbe", "C++": "#f34b7d", "Java": "#ed8b00", "HTML": "#e34c26",
       "CSS": "#8b5cf6", "C": "#9aa4b2", "SCSS": "#c6538c", "Shell": "#89e051", "PHP": "#8892bf"}
top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]
tot = sum(v for _, v in top) or 1
inner = ""
x = 32.0
for k, v in top:  # stacked ratio bar
    w = (W - 64) * v / tot
    inner += f'<rect x="{x:.1f}" y="92" width="{max(w-2,2):.1f}" height="12" rx="6" fill="{COL.get(k, "#00d9ff")}"/>'
    x += w
for i, (k, v) in enumerate(top):
    cx = 32 + (i % 2) * 270
    cy = 142 + (i // 2) * 30
    inner += (f'<g><circle cx="{cx+6}" cy="{cy-4}" r="6" fill="{COL.get(k, "#00d9ff")}"/>'
              f'<text x="{cx+20}" y="{cy}" font-size="14" fill="#e6edf3" font-family="{SANS}" font-weight="600">{k}</text>'
              f'<text x="{cx+240}" y="{cy}" text-anchor="end" font-size="13" fill="#8fa3b8" font-family="{MONO}">{v/tot*100:.1f}%</text></g>')
write("top-langs.svg", card(inner, title="Top Languages", sub="by code size across public repos"))

# ---------------- Streak ----------------
h2 = 190
cols = [("Total", total, "#a78bfa"), ("Current streak", cur, "#00d9ff"), ("Longest streak", longest, "#a78bfa")]
inner = ""
for i, (label, val, col) in enumerate(cols):
    cx = 32 + 175 * i + 80
    inner += (f'<g>'
              f'<text x="{cx}" y="115" text-anchor="middle" font-size="40" font-weight="800" fill="{"#fff"}" font-family="{SANS}">{val}</text>'
              f'<text x="{cx}" y="142" text-anchor="middle" font-size="12.5" fill="{col}" font-family="{SANS}" font-weight="600">{label}</text></g>')
    if i:
        inner += f'<rect x="{cx-87}" y="82" width="1.5" height="70" fill="#1e2a44"/>'
inner += f'<circle cx="{32+175+80}" cy="115" r="62" fill="none" stroke="url(#ac)" stroke-width="3" stroke-dasharray="6 8" opacity=".5"/>'
write("streak.svg", card(inner, h=h2, title="Contribution Streak", sub="days with at least one contribution"))

# ---------------- LeetCode ----------------
try:
    q = {"query": "query($u:String!){matchedUser(username:$u){profile{ranking} submitStats{acSubmissionNum{difficulty count}}} userContestRanking(username:$u){rating attendedContestsCount}}",
         "variables": {"u": LC_USER}}
    d = json.loads(get("https://leetcode.com/graphql", json.dumps(q).encode(), {"Content-Type": "application/json", "Referer": "https://leetcode.com"}))["data"]
    ac = {x["difficulty"]: x["count"] for x in d["matchedUser"]["submitStats"]["acSubmissionNum"]}
    rank = d["matchedUser"]["profile"]["ranking"]
    rating = d["userContestRanking"] or {}
    inner = (f'<text x="32" y="118" font-size="40" font-weight="800" fill="#fff" font-family="{SANS}">{ac["All"]}</text>'
             f'<text x="32" y="140" font-size="12.5" fill="#FFA116" font-weight="600" font-family="{SANS}">problems solved</text>')
    tot_ = max(ac["All"], 1)
    for i, (k, col) in enumerate([("Easy", "#00b8a3"), ("Medium", "#ffc01e"), ("Hard", "#ff375f")]):
        y = 96 + i * 26
        w = 230 * ac[k] / max(ac["Easy"], ac["Medium"], ac["Hard"], 1)
        inner += (f'<text x="190" y="{y+4}" font-size="12.5" fill="#e6edf3" font-family="{SANS}" font-weight="600">{k}</text>'
                  f'<rect x="250" y="{y-6}" width="230" height="10" rx="5" fill="#ffffff" fill-opacity=".07"/>'
                  f'<rect x="250" y="{y-6}" width="{max(w,6):.1f}" height="10" rx="5" fill="{col}"/>'
                  f'<text x="{W-32}" y="{y+4}" text-anchor="end" font-size="12.5" fill="#8fa3b8" font-family="{MONO}">{ac[k]}</text>')
    foot = f"Global rank #{rank:,}"
    if rating:
        foot += f"  ·  contest rating {rating['rating']:.0f}  ·  {rating['attendedContestsCount']} contests"
    write("leetcode.svg", card(inner, h=h2, title="LeetCode", sub=foot))
except Exception as e:
    print("leetcode skipped:", e)
