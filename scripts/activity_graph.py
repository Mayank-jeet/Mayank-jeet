"""Generate assets/activity-graph.svg: a pink line chart of the last 31 days of
GitHub contributions. Uses only the standard library.

Env vars:
  GH_TOKEN  token for the GitHub GraphQL API (Actions provides GITHUB_TOKEN)
  GH_USER   GitHub username (defaults to Mayank-jeet)
Run with --demo to render fake data without calling the API.
"""
import json
import os
import random
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

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
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
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
    W, H = 900, 340
    L, R, T, B = 60, 30, 70, 55
    pw, ph = W - L - R, H - T - B
    counts = [d["contributionCount"] for d in days]
    ymax = max(4, max(counts))
    if ymax % 4:
        ymax += 4 - ymax % 4
    n = len(days)

    def x(i):
        return L + pw * i / (n - 1)

    def y(v):
        return T + ph - ph * v / ymax

    pts = [(x(i), y(c)) for i, c in enumerate(counts)]
    line = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    area = f"{L},{T + ph} " + line + f" {x(n - 1):.1f},{T + ph}"
    total = sum(counts)

    grid = []
    for k in range(5):
        v = ymax * k / 4
        gy = y(v)
        grid.append(f'<line x1="{L}" y1="{gy:.1f}" x2="{W - R}" y2="{gy:.1f}" stroke="#FF69B4" stroke-opacity="0.15"/>')
        grid.append(f'<text x="{L - 10}" y="{gy + 4:.1f}" text-anchor="end" fill="#FF69B4" font-size="11">{int(v)}</text>')
    xlabels = []
    for i, d in enumerate(days):
        day = d["date"][8:10].lstrip("0") or "0"
        xlabels.append(f'<text x="{x(i):.1f}" y="{T + ph + 20}" text-anchor="middle" fill="#FF69B4" font-size="11">{day}</text>')
    first = datetime.fromisoformat(days[0]["date"]).strftime("%b %d")
    last = datetime.fromisoformat(days[-1]["date"]).strftime("%b %d")
    dots = "".join(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.5" fill="#FFFFFF" stroke="#FF69B4" stroke-width="2"/>' for px, py in pts)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI, Ubuntu, Helvetica, Arial, sans-serif">
  <defs>
    <linearGradient id="fill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FF69B4" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#FF69B4" stop-opacity="0.02"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" rx="10" fill="#0D1117" stroke="#FF69B4" stroke-opacity="0.25"/>
  <text x="{W / 2}" y="32" text-anchor="middle" fill="#FFFFFF" font-size="20" font-weight="600">Contribution Graph</text>
  <text x="{W / 2}" y="52" text-anchor="middle" fill="#9E9E9E" font-size="12">{first} - {last} · {total} contributions in the last {n} days</text>
  {''.join(grid)}
  <polygon points="{area}" fill="url(#fill)"/>
  <polyline points="{line}" fill="none" stroke="#FF69B4" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>
  {dots}
  {''.join(xlabels)}
  <text x="{W / 2}" y="{H - 8}" text-anchor="middle" fill="#9E9E9E" font-size="11">Days</text>
</svg>
"""


def main():
    days = demo_days() if "--demo" in sys.argv else fetch_days()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(render(days))
    print(f"Wrote {os.path.normpath(OUT)} ({len(days)} days)")


if __name__ == "__main__":
    main()
