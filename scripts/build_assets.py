"""Generate the static metal-style README assets: hero, section banners, bullet icons.

Role: run by the Actions workflow (or locally with python scripts/build_assets.py);
output goes to assets/. The live contribution graph is produced separately by
activity_graph.py. Both import the shared look from metal.py.
"""
import os
from html import escape

import metal

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

# (file name, glyph, title) for the section banners shown above each README section.
BANNERS = [
    ("contribution", "commit", "Contribution Graph"),
    ("analytics", "pulse", "GitHub Analytics"),
    ("stack", "chip", "Tech Stack"),
    ("about", "rocket", "About Me"),
    ("projects", "wrench", "Featured Projects"),
    ("problem-solving", "nodes", "Problem Solving"),
    ("connect", "mail", "Let's Connect"),
]

# Bullet icons for the About me list.
ICONS = ["cap", "layers", "code", "trophy", "briefcase"]


def write(rel, content):
    path = os.path.normpath(os.path.join(ROOT, rel))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)


def banner(glyph, title):
    w, h = 900, 64
    body = (
        metal.plate(w, h, 14)
        + metal.badge(40, 32, 22, glyph)
        + metal.embossed_text(78, 42, escape(title), 28, spacing=1)
        + f'<rect x="78" y="50" width="{min(80 + len(title) * 14, 520)}" height="2" rx="1" fill="{metal.PINK}" opacity="0.85"/>'
    )
    return metal.svg(w, h, body, title)


def icon(glyph):
    size = 28
    return metal.svg(size, size, metal.badge(14, 14, 12, glyph), glyph)


def hero():
    w, h = 900, 190
    body = (
        metal.plate(w, h, 18)
        + metal.embossed_text(48, 86, "Mayank Jeet", 56, spacing=1)
        + metal.embossed_text(50, 124, "AI / ML ENGINEER  ·  DATA SCIENTIST", 20, spacing=3)
        + '<text x="50" y="154" font-family="\'Segoe UI\', Helvetica, Arial, sans-serif" font-size="15" fill="#aab2be">'
        + "B.Tech Civil Engineering @ IIT Bhubaneswar (2028)  ·  applied ML and agentic AI, end to end</text>"
    )
    return metal.svg(w, h, body, "Mayank Jeet")


def main():
    write("hero.svg", hero())
    for name, glyph, title in BANNERS:
        write(f"banners/{name}.svg", banner(glyph, title))
    for g in ICONS:
        write(f"icons/{g}.svg", icon(g))


if __name__ == "__main__":
    main()
