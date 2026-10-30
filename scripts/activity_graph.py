"""Generate assets/activity-graph.svg: a clean black-card chart of the last 31 days
of GitHub contributions (soft white bars, white trend line, pink data dots).

Role in the architecture: run by the Actions workflow every 6 hours; it imports the
shared look from metal.py so the graph matches the hero, banners and icons.
Standard library only.

Env vars:
  GH_TOKEN  token for the GitHub GraphQL API (Actions provides GITHUB_TOKEN)
  GH_USER   GitHub username (defaults to Mayank-jeet)
Run with --demo to render fake data without calling the API.
"""
import json
import os
import random
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

import metal

USER = os.environ.get("GH_USER", "Mayank-jeet")
DAYS = 31
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "activity-graph.svg")

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch_days():
    token = os.environ["GH_TOKEN"]
    to = datetime.now(timezone.utc)
    frm = to - timedelta(days=DAYS + 2)
    payload = json.dumps({
        "query": QUERY,
        "variables": {
            "login": USER,
            "from": frm.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "to": to.strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
    }).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "activity-graph-script"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:  # surface the API's own message in the Actions log
        raise SystemExit(f"GitHub API HTTP {e.code}: {e.read().decode(errors='replace')}")
    if "errors" in data or not data.get("data", {}).get("user"):
        raise SystemExit(f"GraphQL error: {data}")
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    days.sort(key=lambda d: d["date"])
    return days[-DAYS:]


def demo_days():
    base = datetime.now(timezone.utc).date()
    return [
        {"date": (base - timedelta(days=DAYS - 1 - i)).isoformat(), "contributionCount": random.choice([0, 0, 1, 2, 3, 5, 8])}
        for i in range(DAYS)
    ]


def render(days):
    W, H = 900, 360
    L, R, T, B = 64, 34, 86, 58
    pw, ph = W - L - R, H - T - B
    counts = [d["contributionCount"] for d in days]
    ymax = max(4, max(counts))
    if ymax % 4:
        ymax += 4 - ymax % 4
    n = len(days)
    step = pw / (n - 1)
    total = sum(counts)

    def x(i):
        return L + step * i

    def y(v):
        return T + ph - ph * v / ymax

    pts = [(x(i), y(c)) for i, c in enumerate(counts)]
    line = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    area = f"{L},{T + ph} " + line + f" {x(n - 1):.1f},{T + ph}"

    grid = []
    for k in range(5):
        v = ymax * k / 4
        gy = y(v)
        grid.append(f'<line x1="{L}" y1="{gy:.1f}" x2="{W - R}" y2="{gy:.1f}" stroke="#8d96a3" stroke-opacity="0.22" stroke-dasharray="4 5"/>')
        grid.append(f'<text x="{L - 12}" y="{gy + 4:.1f}" text-anchor="end" fill="#aab2be" font-size="11">{int(v)}</text>')

    # metal bars: one per day with activity (skipped for zero so nothing renders at height 0)
    bw = step * 0.5
    bars = "".join(
        f'<rect x="{px - bw / 2:.1f}" y="{py:.1f}" width="{bw:.1f}" height="{T + ph - py:.1f}" rx="2" fill="#ffffff" opacity="0.14"/>'
        for (px, py), c in zip(pts, counts) if c > 0
    )
    xlabels = "".join(
        f'<text x="{x(i):.1f}" y="{T + ph + 20}" text-anchor="middle" fill="#aab2be" font-size="10">{d["date"][8:10].lstrip("0") or "0"}</text>'
        for i, d in enumerate(days)
    )
    # solid-colour line (a gradient on a flat line has a zero-height box and would vanish)
    trend = f'<polyline points="{line}" fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>'
    orbs = "".join(
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{metal.PINK}" stroke="#000000" stroke-width="1.5"/>'
        for px, py in pts
    )
    first = datetime.fromisoformat(days[0]["date"]).strftime("%b %d")
    last = datetime.fromisoformat(days[-1]["date"]).strftime("%b %d")

    body = (
        metal.plate(W, H, 16)
        + metal.badge(44, 40, 20, "commit")
        + metal.embossed_text(78, 48, "Contribution Graph", 26, spacing=1)
        + f'<text x="78" y="68" fill="#aab2be" font-size="12" font-family="Segoe UI, Helvetica, Arial, sans-serif">{first} - {last} · {total} contributions in the last {n} days</text>'
        + "".join(grid)
        + bars
        + f'<polygon points="{area}" fill="url(#m-area)"/>'
        + trend
        + orbs
        + f'<g font-family="Segoe UI, Helvetica, Arial, sans-serif">{xlabels}</g>'
        + f'<text x="{W / 2}" y="{H - 14}" text-anchor="middle" fill="#8d96a3" font-size="11" font-family="Segoe UI, Helvetica, Arial, sans-serif">Day of month</text>'
    )
    return metal.svg(W, H, body, "Contribution graph")


def main():
    days = demo_days() if "--demo" in sys.argv else fetch_days()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(render(days))
    print(f"Wrote {os.path.normpath(OUT)} ({len(days)} days)")


if __name__ == "__main__":
    main()
