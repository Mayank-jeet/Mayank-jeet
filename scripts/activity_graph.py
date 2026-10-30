"""Generate the two live SVGs for the profile README:
  assets/dashboard.svg  stats tiles (streaks, totals) + contributions-per-month bars
  assets/heatmap.svg    contribution heatmap whose columns sweep in from the left

Role in the architecture: a GitHub Actions workflow runs this every 6 hours, commits
the SVGs, and README.md embeds them as images. Standard library only.

Data sources, in order:
  1. GitHub GraphQL API (GH_TOKEN; Actions provides GITHUB_TOKEN) - last 12 months
  2. Public page https://github.com/users/<user>/contributions (no token needed)
If both fail the script exits non-zero, so the workflow run goes red instead of
silently leaving stale or placeholder images.

Env: GH_TOKEN, GH_USER (default Mayank-jeet).   Flag: --demo renders fake data.
"""
import html
import json
import os
import random
import re
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone

from theme import BAR, BAR_HOT, BG, DIM, LABEL, LEVELS, LINE, TXT, panel, stat_card, svg

USER = os.environ.get("GH_USER", "Mayank-jeet")
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

QUERY = """query($login: String!) { user(login: $login) { contributionsCollection {
  contributionCalendar { weeks { contributionDays { date contributionCount } } } } } }"""


# ---------------------------------------------------------------- data
def fetch_graphql():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GH_TOKEN']}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data or not data.get("data", {}).get("user"):
        raise RuntimeError(f"GraphQL error: {data}")
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return [d for w in weeks for d in w["contributionDays"]]


def fetch_public_page():
    req = urllib.request.Request(f"https://github.com/users/{USER}/contributions", headers={"User-Agent": "Mozilla/5.0 profile-graph"})
    with urllib.request.urlopen(req, timeout=30) as r:
        page = r.read().decode("utf-8", "replace")
    tips = {}
    for m in re.finditer(r'<tool-tip[^>]*\bfor="([^"]+)"[^>]*>([^<]*)</tool-tip>', page):
        n = re.match(r"\s*(\d+)\s+contribution", html.unescape(m.group(2)))
        tips[m.group(1)] = int(n.group(1)) if n else 0
    days = []
    for tag in re.findall(r"<td[^>]*data-date=[^>]*>", page):
        d = re.search(r'data-date="([\d-]+)"', tag)
        i = re.search(r'\bid="([^"]+)"', tag)
        if d:
            days.append({"date": d.group(1), "contributionCount": tips.get(i.group(1), 0) if i else 0})
    if not days:
        raise RuntimeError("could not parse public contributions page")
    return days


def fetch_days():
    errs = []
    for fn in (fetch_graphql, fetch_public_page):
        try:
            days = sorted(fn(), key=lambda d: d["date"])
            today = datetime.now(timezone.utc).date().isoformat()
            return [{"date": date.fromisoformat(d["date"]), "n": d["contributionCount"]} for d in days if d["date"] <= today]
        except Exception as e:
            errs.append(f"{fn.__name__}: {e}")
            print("WARN", errs[-1], file=sys.stderr)
    raise SystemExit("All data sources failed: " + " | ".join(errs))


def demo_days():
    end = datetime.now(timezone.utc).date()
    return [{"date": end - timedelta(days=370 - i), "n": random.choice([0, 0, 1, 2, 3, 5, 8, 14, 30])} for i in range(371)]


# ---------------------------------------------------------------- stats
def fmt(d):
    return f"{d:%b} {d.day}"


def compute(days):
    last = days[-371:]                       # what the heatmap draws (<= 53 weeks)
    year = days[-365:]                       # what the numbers describe
    total = sum(d["n"] for d in year)
    active = [d for d in year if d["n"] > 0]
    best = max(year, key=lambda d: d["n"])
    # current streak: walk back from today; an empty *today* does not break it yet
    i = len(year) - 1
    if year[i]["n"] == 0:
        i -= 1
    cur_end = i
    while i >= 0 and year[i]["n"] > 0:
        i -= 1
    cur = (cur_end - i, year[i + 1]["date"] if cur_end - i else None, year[cur_end]["date"] if cur_end - i else None)
    # longest streak
    lg, run, start = (0, None, None), 0, 0
    for k, d in enumerate(year):
        if d["n"] > 0:
            if run == 0:
                start = k
            run += 1
            if run > lg[0]:
                lg = (run, year[start]["date"], d["date"])
        else:
            run = 0
    # contributions per calendar month, last 12 months
    today = year[-1]["date"]
    months = []
    y, m = today.year, today.month
    for _ in range(12):
        months.append((y, m))
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    months.reverse()
    per = {k: 0 for k in months}
    for d in year:
        k = (d["date"].year, d["date"].month)
        if k in per:
            per[k] += d["n"]
    return dict(last=last, total=total, active=len(active), best=best, cur=cur, longest=lg,
                avg=(total / len(active) if active else 0), months=[(datetime(y, m, 1).strftime("%b"), per[(y, m)]) for y, m in months],
                span=len(year))


# ---------------------------------------------------------------- stats image
def dashboard(s, W=900, H=360):
    """Six neutral stat tiles + a card with the green monthly histogram. No outer box."""
    g = 12
    cw, ch = (W - 1 - 2 * g) / 3, 80
    rng = lambda a, b: f"{fmt(a)} - {fmt(b)}" if a else "no active streak"
    cards = [
        ("current streak", str(s["cur"][0]), "days", rng(s["cur"][1], s["cur"][2])),
        ("longest streak", str(s["longest"][0]), "days", rng(s["longest"][1], s["longest"][2])),
        ("contributions", f"{s['total']:,}", "", "in the last year"),
        ("active days", str(s["active"]), f"/ {s['span']}", f"{100 * s['active'] / s['span']:.0f}% of the year"),
        ("best day", str(s["best"]["n"]), "", fmt(s["best"]["date"])),
        ("avg / active day", f"{s['avg']:.1f}", "", "contributions"),
    ]
    body = ""
    for i, c in enumerate(cards):
        body += stat_card((i % 3) * (cw + g), (i // 3) * (ch + g), cw, ch, *c)
    # monthly histogram card
    cy = 2 * (ch + g)
    chh = H - cy - 1
    body += panel(0, cy, W, chh, 4)
    body += f'<text x="16" y="{cy+24}" font-size="11" fill="{LABEL}">$ contributions / month</text>'
    base, top = cy + chh - 30, cy + 56
    mx = max(v for _, v in s["months"]) or 1
    slot = (W - 40) / 12
    for i, (lab, v) in enumerate(s["months"]):
        bh = max(3, (base - top) * v / mx)
        bx = 20 + i * slot + slot * 0.2
        hot = v == mx and v > 0
        body += (f'<rect class="b" style="animation-delay:{i*0.07:.2f}s" x="{bx:.1f}" y="{base-bh:.1f}" width="{slot*0.6:.1f}" height="{bh:.1f}" rx="2" fill="{BAR_HOT if hot else BAR}"/>'
                 f'<text x="{bx+slot*0.3:.1f}" y="{base-bh-6:.1f}" text-anchor="middle" font-size="10.5" font-weight="{700 if hot else 400}" fill="{TXT if hot else DIM}">{v}</text>'
                 f'<text x="{bx+slot*0.3:.1f}" y="{base+16}" text-anchor="middle" font-size="10.5" fill="{DIM}">{lab}</text>')
    css = ".b{transform-box:fill-box;transform-origin:50% 100%;animation:grow .9s cubic-bezier(.2,.8,.2,1) both}@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}"
    return svg(W, H, body, "GitHub stats", css)


# ---------------------------------------------------------------- heatmap
def heatmap(s, W=900):
    days = s["last"]
    first = days[0]["date"]
    start = first - timedelta(days=(first.weekday() + 1) % 7)       # Sunday-first columns like GitHub
    ncols = (days[-1]["date"] - start).days // 7 + 1
    padx, lab = 24, 30
    pitch = (W - 2 * padx - lab) / ncols
    cell = pitch - 3
    gy = 112
    nz = sorted(d["n"] for d in days if d["n"] > 0)
    q = [nz[int(len(nz) * f)] for f in (0.25, 0.5, 0.75)] if nz else [1, 2, 3]
    level = lambda c: 0 if c == 0 else 1 if c <= q[0] else 2 if c <= q[1] else 3 if c <= q[2] else 4
    cols = {}
    for d in days:
        idx = (d["date"] - start).days
        cols.setdefault(idx // 7, []).append((idx % 7, d))
    ly = gy + 7 * pitch + 22
    H = int(ly + 28)
    body = panel(0, 0, W, H)
    body += (f'<text x="{padx}" y="56" font-size="34" font-weight="700" fill="{TXT}">{s["total"]:,}</text>'
             f'<text x="{padx}" y="76" font-size="10" fill="{DIM}" letter-spacing="1.6">CONTRIBUTIONS IN THE LAST YEAR</text>')
    lastx, prev = -99, None                                         # month labels
    for c in range(ncols):
        d0 = start + timedelta(days=7 * c)
        if d0.month != prev and c - lastx >= 3 and (d0 + timedelta(days=6)) >= days[0]["date"]:
            body += f'<text x="{padx+lab+c*pitch:.1f}" y="{gy-8}" font-size="10" fill="{DIM}">{d0:%b}</text>'
            lastx = c
        prev = d0.month
    for r, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        body += f'<text x="{padx}" y="{gy + r*pitch + cell*0.8:.1f}" font-size="10" fill="{DIM}">{name}</text>'
    for c in sorted(cols):
        rects = "".join(f'<rect x="{padx+lab+c*pitch:.1f}" y="{gy+r*pitch:.1f}" width="{cell:.1f}" height="{cell:.1f}" rx="2.5" fill="{LEVELS[level(d["n"])]}"/>'
                        for r, d in cols[c])
        body += f'<g class="c" style="animation-delay:{c*0.045:.3f}s">{rects}</g>'
    lx = W - padx - 5 * 16 - 70
    body += f'<text x="{lx}" y="{ly+9}" font-size="10" fill="{DIM}" text-anchor="end">Less</text>'
    body += "".join(f'<rect x="{lx+8+i*16}" y="{ly}" width="12" height="12" rx="2.5" fill="{LEVELS[i]}"/>' for i in range(5))
    body += f'<text x="{lx+8+5*16+4}" y="{ly+9}" font-size="10" fill="{DIM}">More</text>'
    css = (".c{opacity:0;animation:sweep 10s ease-out infinite both}"
           "@keyframes sweep{0%{opacity:0;transform:translateX(-14px)}6%{opacity:1;transform:translateX(0)}88%{opacity:1}96%{opacity:0}100%{opacity:0}}"
           "@media (prefers-reduced-motion:reduce){.c{animation:none;opacity:1}}")
    return svg(W, H, body, "Contribution heatmap", css)


def main():
    days = demo_days() if "--demo" in sys.argv else fetch_days()
    s = compute(days)
    os.makedirs(ASSETS, exist_ok=True)
    for name, content in (("dashboard.svg", dashboard(s)), ("heatmap.svg", heatmap(s))):
        with open(os.path.join(ASSETS, name), "w", encoding="utf-8") as f:
            f.write(content)
    print(f"Wrote dashboard.svg + heatmap.svg ({len(days)} days, {s['total']} contributions, streak {s['cur'][0]})")


if __name__ == "__main__":
    main()
