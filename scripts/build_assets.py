"""Generate the static terminal-style cards: hero, about, stack, problem-solving,
section title bars, footer and the three project cards (with screenshots embedded).

Run:  python scripts/build_assets.py      (re-run after adding/changing a screenshot)
Role in the architecture: README.md only references the SVGs written here; the
live ones (dashboard + heatmap) come from activity_graph.py via GitHub Actions.
"""
import base64
import os
import re

from theme import (BG, BODY, BTN, CW, DIM, GLYPHS, GREEN, LINE, TXT, chips, esc, stat_card, svg, window, wrap)

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
SHOTS = os.path.join(ASSETS, "projects")

# slug (= screenshot file name), title, short description, stack
PROJECTS = [
    ("opspilot", "OpsPilot", "AI task worker that drives an accounting app in a real browser. High-value invoices wait for human approval.",
     ["LangGraph", "FastAPI", "Playwright", "React"]),
    ("bloggen", "BlogGEN", "RAG blog generator: splits a topic into tasks, researches each one, writes the post and illustrates it.",
     ["LangGraph", "FastAPI", "React", "Tavily", "Gemini"]),
    ("anomaly-inspect", "Anomaly-Inspect", "Unsupervised defect detection on MVTec AD. PatchCore reaches 0.977 AUROC at ~97 ms on CPU.",
     ["PyTorch", "FAISS", "ONNX Runtime", "FastAPI", "React"]),
]


def write(rel, content):
    path = os.path.join(ASSETS, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def cursor(x, y, h=30, w=14):
    return (f'<rect x="{x:.1f}" y="{y}" width="{w}" height="{h}" fill="{GREEN}">'
            '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect>')


def hero(w=900, h=210):
    name = "Mayank Jeet"
    cx = 32 + len(name) * 46 * CW + 8
    body = (f'<text x="32" y="64" font-size="14" fill="{GREEN}">$ whoami</text>'
            f'<text x="32" y="112" font-size="46" font-weight="700" fill="{TXT}">{name}</text>' + cursor(cx, 80, 38, 16)
            + f'<text x="32" y="146" font-size="19" font-weight="700" fill="{GREEN}">AI / ML Engineer  ·  Data Scientist</text>'
            f'<text x="32" y="172" font-size="13" fill="{BODY}">B.Tech Civil Engineering @ IIT Bhubaneswar (2028). I build applied ML and agentic AI systems, end to end.</text>')
    return svg(w, h, window(w, h, "github ~ $ whoami", body, "Mayank-jeet"), "Mayank Jeet")


def segs(text, x, y, size=13):
    """Tiny markup: **bold** segments become bright tspans."""
    parts = re.split(r"(\*\*.+?\*\*)", text)
    t = "".join(f'<tspan font-weight="700" fill="{TXT}">{esc(p[2:-2])}</tspan>' if p.startswith("**") else esc(p) for p in parts)
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{BODY}" xml:space="preserve">{t}</text>'


def glyph(name, x, y, s=0.85):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{GREEN}" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round">{GLYPHS[name]}</g>')


def about(w=900):
    rows = [
        ("cap", "B.Tech student at **IIT Bhubaneswar**, spending most of my time building software."),
        ("chip", "I take ideas from model to API to UI to live deployment, using LangGraph, FastAPI, React and PyTorch."),
        ("nodes", "**600+ DSA problems** solved in C++ on LeetCode and CodeForces."),
        ("trophy", "Core Head of Sports Fest at IIT Bhubaneswar, leading a team of organizers."),
        ("briefcase", "**Open to** AI Engineer, ML Engineer, Data Scientist and SDE (ML) roles."),
    ]
    h = 78 + len(rows) * 36
    body = f'<text x="24" y="58" font-size="13" fill="{GREEN}">$ cat about.md</text>'
    for i, (g, t) in enumerate(rows):
        y = 94 + i * 36
        body += glyph(g, 24, y - 15) + segs(t, 58, y)
    return svg(w, h, window(w, h, "~/about $ cat about.md", body), "About me")


def stack(w=900):
    groups = [
        ("languages", ["Python", "C++", "C", "JavaScript", "MySQL"]),
        ("ml / data", ["PyTorch", "TensorFlow", "Keras", "ONNX", "FAISS", "Pandas", "NumPy", "Matplotlib", "Seaborn"]),
        ("llm / agents", ["LangChain", "LangGraph", "RAG", "OpenAI", "Anthropic", "Gemini", "Playwright"]),
        ("web / api", ["FastAPI", "React", "Streamlit"]),
        ("tools", ["Docker", "Git", "GitHub", "Vercel", "Render", "VS Code", "Jupyter", "Google Colab"]),
    ]
    body, y = "", 52
    for label, items in groups:
        c, bottom = chips(items, 150, y, w - 24)
        body += f'<text x="24" y="{y + 15}" font-size="12" fill="{DIM}">{label}</text>' + c
        y = bottom + 14
    h = y + 6
    return svg(w, h, window(w, h, "~/stack $ ls", body), "Tech stack")


def problem(w=900):
    h, m, g = 118, 16, 12
    cw = (w - 2 * m - 2 * g) / 3
    cards = [("leetcode", "m_j_bhardwaj"), ("codeforces", "Mayank_Jeet"), ("solved", "600+")]
    body = ""
    for i, (lab, val) in enumerate(cards):
        body += stat_card(m + i * (cw + g), 46, cw, 60, lab, val)
    return svg(w, h, window(w, h, "~/problem-solving $ stats", body), "Problem solving")


def strip(title, name):
    return svg(900, 34, window(900, 34, title), name)


def footer():
    t = '$ git commit -m "see you in the next commit"'
    cx = 8 + len(t) * 14 * CW + 6
    body = f'<text x="8" y="26" font-size="14" fill="{GREEN}">{esc(t)}</text>' + cursor(cx, 12, 18, 9)
    return svg(900, 40, body, "Footer")


def shot_data(slug):
    for ext, mime in (("png", "image/png"), ("jpg", "image/jpeg"), ("jpeg", "image/jpeg"), ("webp", "image/webp")):
        p = os.path.join(SHOTS, f"{slug}.{ext}")
        if os.path.exists(p):
            with open(p, "rb") as f:
                return f"data:{mime};base64," + base64.b64encode(f.read()).decode()
    return None


def card(slug, title, desc, stack_items, w=290, h=352):
    iw, ih = w - 20, 151
    data = shot_data(slug)
    if data:
        img = (f'<image x="10" y="10" width="{iw}" height="{ih}" preserveAspectRatio="xMidYMid slice" '
               f'clip-path="url(#c-{slug})" href="{data}" xlink:href="{data}"/>')
    else:
        img = (f'<rect x="10" y="10" width="{iw}" height="{ih}" rx="4" fill="url(#g-{slug})"/>'
               f'<text x="{w/2}" y="{10 + ih/2 - 4}" text-anchor="middle" font-size="12" fill="{GREEN}">add screenshot:</text>'
               f'<text x="{w/2}" y="{10 + ih/2 + 14}" text-anchor="middle" font-size="11" fill="{DIM}">assets/projects/{slug}.png</text>')
    lines = wrap(desc, 36)[:3]
    d = "".join(f'<text x="14" y="{208 + i*16}" font-size="11.5" fill="{BODY}">{esc(l)}</text>' for i, l in enumerate(lines))
    c, _ = chips(stack_items, 14, 258, w - 10, size=10, h=20, gap=6)
    by = h - 10 - 30
    defs = (f'<defs><clipPath id="c-{slug}"><rect x="10" y="10" width="{iw}" height="{ih}" rx="4"/></clipPath>'
            f'<linearGradient id="g-{slug}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#10281a"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>')
    body = (defs + f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="6" fill="{BG}" stroke="{LINE}"/>' + img
            + f'<rect x="10" y="10" width="{iw}" height="{ih}" rx="4" fill="none" stroke="{LINE}"/>'
            + f'<rect x="14" y="177" width="6" height="6" fill="{GREEN}"/>'
            + f'<text x="26" y="184" font-size="15" font-weight="700" fill="{TXT}">{esc(title)}</text>' + d + c
            + f'<rect x="10" y="{by}" width="{iw}" height="30" rx="4" fill="{BTN}"/>'
            f'<text x="{w/2}" y="{by + 20}" text-anchor="middle" font-size="13" font-weight="700" fill="#ffffff">Live  ↗</text>')
    return svg(w, h, body, title)


def main():
    write("hero.svg", hero())
    write("about.svg", about())
    write("stack.svg", stack())
    write("problem.svg", problem())
    write("headers/projects.svg", strip("~/projects $ ls featured/", "Featured projects"))
    write("headers/connect.svg", strip("~/connect $ ping --me", "Let's connect"))
    write("footer.svg", footer())
    for slug, title, desc, st in PROJECTS:
        write(f"cards/{slug}.svg", card(slug, title, desc, st))
        print(f"card {slug}: screenshot " + ("embedded" if shot_data(slug) else "MISSING (placeholder drawn)"))
    print("assets written to", os.path.normpath(ASSETS))


if __name__ == "__main__":
    main()
