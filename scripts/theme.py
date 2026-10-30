"""Shared 'terminal green' design system for every generated SVG in this profile.

Role in the architecture: build_assets.py (static cards) and activity_graph.py
(live dashboard + heatmap) both import this module, so colours, the window frame,
chips and icons are defined once and every card looks like part of the same UI.
Standard library only.
"""
import textwrap
from xml.sax.saxutils import escape

MONO = "'JetBrains Mono','SF Mono','Cascadia Code','Fira Code',Consolas,'DejaVu Sans Mono',monospace"
CW = 0.6  # width of one monospace character, in em (used to size chips and place cursors)

BG = "#0b130f"      # card face: near-black with a green tint, close to GitHub dark (#0d1117)
BAR = "#101c15"     # window title bar
LINE = "#1f3b2b"    # 1px borders
CARD = "#0f1a14"    # inner stat cards
TXT = "#e6fff0"     # primary text
BODY = "#c3dccb"    # body text
DIM = "#7fa08d"     # labels
GREEN = "#39d353"   # accent
BTN = "#238636"     # button green (GitHub's own)
LEVELS = ["#14231b", "#0e4429", "#006d32", "#26a641", "#39d353"]  # heatmap, empty -> max

# 24x24 line glyphs (stroke only) used as bullet icons
GLYPHS = {
    "cap": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-4.5"/><path d="M22 9v6"/>',
    "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    "nodes": '<circle cx="12" cy="5" r="2.2"/><circle cx="6" cy="18" r="2.2"/><circle cx="18" cy="18" r="2.2"/><path d="M11 7l-4 9M13 7l4 9"/>',
    "trophy": '<path d="M8 4h8v6a4 4 0 0 1-8 0z"/><path d="M8 6H4v2a3 3 0 0 0 4 3M16 6h4v2a3 3 0 0 1-4 3"/><path d="M12 14v4M8 21h8M9 18h6"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2M3 13h18"/>',
}


def esc(s):
    return escape(str(s))


def svg(w, h, body, title="", css=""):
    t = f"<title>{esc(title)}</title>" if title else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">{t}\n<style>text{{font-family:{MONO}}}{css}</style>\n{body}\n</svg>\n')


def window(w, h, title, body="", right=""):
    """Flat terminal window: 1px green-tinted border, small square-ish corners, dots title bar."""
    r = (f'<text x="{w-16}" y="19.5" font-size="12" fill="{DIM}" text-anchor="end">{esc(right)}</text>') if right else ""
    return (f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="6" fill="{BG}" stroke="{LINE}"/>'
            f'<path d="M0.5 30.5V6.5A6 6 0 0 1 6.5 0.5H{w-6.5}A6 6 0 0 1 {w-0.5} 6.5V30.5Z" fill="{BAR}"/>'
            f'<line x1="0.5" y1="30.5" x2="{w-0.5}" y2="30.5" stroke="{LINE}"/>'
            f'<circle cx="16" cy="15.5" r="4.5" fill="#1b5e32"/><circle cx="32" cy="15.5" r="4.5" fill="#2ea043"/><circle cx="48" cy="15.5" r="4.5" fill="{GREEN}"/>'
            f'<text x="66" y="19.5" font-size="12" fill="{DIM}">{esc(title)}</text>{r}{body}')


def stat_card(x, y, w, h, label, value, unit="", sub=""):
    u = f'<tspan font-size="12" fill="{DIM}" font-weight="400"> {esc(unit)}</tspan>' if unit else ""
    s = f'<text x="{x+14}" y="{y+h-12}" font-size="10.5" fill="{DIM}">{esc(sub)}</text>' if sub else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{CARD}" stroke="{LINE}"/>'
            f'<rect x="{x}" y="{y+10}" width="2.5" height="{h-20}" fill="{GREEN}"/>'
            f'<text x="{x+14}" y="{y+22}" font-size="11" fill="{GREEN}">$ {esc(label)}</text>'
            f'<text x="{x+14}" y="{y+h-32}" font-size="26" font-weight="700" fill="{TXT}">{esc(value)}{u}</text>{s}')


def chips(items, x, y, maxx, size=11, h=22, gap=8):
    """Flow a list of text chips; returns (svg, y_after). Wraps to a new row at maxx."""
    out, cx, cy = [], x, y
    for it in items:
        w = len(it) * size * CW + 18
        if cx + w > maxx:
            cx, cy = x, cy + h + 6
        out.append(f'<rect x="{cx:.1f}" y="{cy}" width="{w:.1f}" height="{h}" rx="3" fill="#10281a" stroke="{LINE}"/>'
                   f'<text x="{cx + w/2:.1f}" y="{cy + h/2 + size*0.35:.1f}" font-size="{size}" fill="{GREEN}" text-anchor="middle">{esc(it)}</text>')
        cx += w + gap
    return "".join(out), cy + h


def wrap(text, width):
    return textwrap.wrap(text, width=width, break_long_words=False)
