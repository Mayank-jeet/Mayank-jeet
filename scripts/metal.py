"""Shared 'clean dark' design system for the profile README assets.

Role in the architecture: every generated SVG (hero, section banners, bullet icons
and the live contribution graph) imports this one module, so the card style, the
icons and the text are defined once and the whole profile looks consistent.
(The module is still called metal.py so existing imports keep working.)
Standard library only.

Look: pure black cards with a thin white border, flat white text, flat white icons.
"""

FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
PINK = "#FF69B4"  # accent colour shared with the README badges

# 24x24 line glyphs, drawn later as flat white strokes.
GLYPHS = {
    "rocket": '<path d="M12 2c3 2 5 5 5 9l-2 4H9l-2-4c0-4 2-7 5-9z"/><circle cx="12" cy="9" r="1.6"/><path d="M9 15l-3 3v3l3-2M15 15l3 3v3l-3-2"/>',
    "cap": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-4.5"/><path d="M22 9v6"/>',
    "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    "nodes": '<circle cx="12" cy="5" r="2.2"/><circle cx="6" cy="18" r="2.2"/><circle cx="18" cy="18" r="2.2"/><path d="M11 7l-4 9M13 7l4 9"/>',
    "trophy": '<path d="M8 4h8v6a4 4 0 0 1-8 0z"/><path d="M8 6H4v2a3 3 0 0 0 4 3M16 6h4v2a3 3 0 0 1-4 3"/><path d="M12 14v4M8 21h8M9 18h6"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2M3 13h18"/>',
    "layers": '<path d="M12 2l10 5-10 5L2 7z"/><path d="M2 12l10 5 10-5"/><path d="M2 17l10 5 10-5"/>',
    "bars": '<path d="M5 20V11M11 20V4M17 20v-6"/><path d="M3 21h18"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "pulse": '<path d="M3 12h4l3-8 4 16 3-8h4"/>',
    "code": '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>',
    "commit": '<circle cx="12" cy="12" r="3.5"/><path d="M2 12h6.5M15.5 12H22"/>',
    "wrench": '<path d="M14.5 6.5a4 4 0 0 0 5 5L11 20a2.1 2.1 0 0 1-3-3z"/><path d="M14.5 6.5l3-3 3 3-3 3"/>',
}


def defs():
    """Only what the clean style needs: a soft white fade for the graph area."""
    return """<defs>
    <linearGradient id="m-area" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.16"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
  </defs>"""


def plate(w, h, rx=12):
    """Clean card: pure black fill with a thin white border."""
    return (f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="{rx}" '
            f'fill="#000000" stroke="#ffffff" stroke-width="1.25" stroke-opacity="0.9"/>')


def embossed_text(x, y, text, size, anchor="start", spacing=0):
    """Flat white text (name kept so existing callers keep working)."""
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="700" letter-spacing="{spacing}" fill="#ffffff">{text}</text>')


def badge(cx, cy, r, glyph):
    """Flat round icon: thin white ring, black inside, white line glyph."""
    s = r * 0.05  # glyph scale: the 24-unit grid ends up about 1.2 x radius wide
    return f"""<circle cx="{cx}" cy="{cy}" r="{r - 0.75}" fill="#000000" stroke="#ffffff" stroke-width="1.25"/>
  <g transform="translate({cx - 12 * s:.2f} {cy - 12 * s:.2f}) scale({s:.3f})" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    {GLYPHS[glyph]}
  </g>"""


def svg(w, h, body, title=""):
    t = f"<title>{title}</title>" if title else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f"{t}\n  {defs()}\n  {body}\n</svg>\n")
