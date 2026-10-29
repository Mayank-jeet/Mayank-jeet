"""Shared 'dark + light metal' design system for the profile README assets.

Role in the architecture: every generated SVG (hero, section banners, bullet icons
and the live contribution graph) imports this one module, so gradients, bevels and
glyphs are defined once and the whole profile looks like one material.
Standard library only.
"""

FONT = "'Segoe UI Black', 'Arial Black', 'Segoe UI', Helvetica, Arial, sans-serif"
PINK = "#FF69B4"  # accent colour shared with the README badges

# 24x24 line glyphs, drawn later with a chrome gradient stroke.
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
    """Reusable gradients and filters (ids are prefixed m- to avoid clashes)."""
    return f"""<defs>
    <linearGradient id="m-chrome" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff"/><stop offset="0.38" stop-color="#cdd4de"/>
      <stop offset="0.52" stop-color="#7b8490"/><stop offset="0.72" stop-color="#c3cad5"/>
      <stop offset="1" stop-color="#f4f7fa"/>
    </linearGradient>
    <linearGradient id="m-chrome-u" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="24">
      <stop offset="0" stop-color="#ffffff"/><stop offset="0.4" stop-color="#cdd4de"/>
      <stop offset="0.55" stop-color="#8a93a0"/><stop offset="0.75" stop-color="#c9d0da"/>
      <stop offset="1" stop-color="#f4f7fa"/>
    </linearGradient>
    <linearGradient id="m-plate" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2b313b"/><stop offset="0.5" stop-color="#171b22"/><stop offset="1" stop-color="#0c0e13"/>
    </linearGradient>
    <linearGradient id="m-rim" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#f5f7fa"/><stop offset="0.3" stop-color="#5a616c"/>
      <stop offset="0.55" stop-color="#cfd5de"/><stop offset="0.8" stop-color="#2f343d"/><stop offset="1" stop-color="#e9edf2"/>
    </linearGradient>
    <linearGradient id="m-gloss" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.28"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="m-wall" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#8d96a3"/><stop offset="1" stop-color="#1b1f26"/>
    </linearGradient>
    <linearGradient id="m-area" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#d7dde6" stop-opacity="0.30"/><stop offset="1" stop-color="#d7dde6" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="m-orb" cx="0.35" cy="0.3" r="0.8">
      <stop offset="0" stop-color="#ffffff"/><stop offset="0.25" stop-color="#d5dbe4"/>
      <stop offset="0.6" stop-color="#7a8390"/><stop offset="1" stop-color="#1d2128"/>
    </radialGradient>
    <radialGradient id="m-orb-pink" cx="0.35" cy="0.3" r="0.8">
      <stop offset="0" stop-color="#ffffff"/><stop offset="0.25" stop-color="#ffc2e2"/>
      <stop offset="0.6" stop-color="{PINK}"/><stop offset="1" stop-color="#4d1736"/>
    </radialGradient>
    <radialGradient id="m-well" cx="0.5" cy="0.35" r="0.75">
      <stop offset="0" stop-color="#3a414d"/><stop offset="1" stop-color="#0d0f14"/>
    </radialGradient>
    <filter id="m-brush" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.004 0.9" numOctaves="2" seed="7" result="n"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.9 -0.35"/>
    </filter>
    <filter id="m-shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feDropShadow dx="0" dy="3" stdDeviation="2.5" flood-color="#000" flood-opacity="0.65"/>
    </filter>
    <filter id="m-blur"><feGaussianBlur stdDeviation="3"/></filter>
  </defs>"""


def plate(w, h, rx=12):
    """Beveled dark metal panel: rim, gunmetal face, brushed grain, top gloss."""
    return f"""<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{rx}" fill="url(#m-rim)"/>
  <rect x="2.5" y="2.5" width="{w-5}" height="{h-5}" rx="{rx-2}" fill="url(#m-plate)"/>
  <rect x="2.5" y="2.5" width="{w-5}" height="{h-5}" rx="{rx-2}" filter="url(#m-brush)" opacity="0.10"/>
  <rect x="3.5" y="3.5" width="{w-7}" height="{(h-7)*0.45:.1f}" rx="{rx-3}" fill="url(#m-gloss)"/>"""


def embossed_text(x, y, text, size, anchor="start", spacing=0):
    """Chrome text with a dark drop shadow below and a thin light edge above."""
    common = f'text-anchor="{anchor}" font-family="{FONT}" font-size="{size}" font-weight="800" letter-spacing="{spacing}"'
    return (f'<text x="{x}" y="{y - 1}" {common} fill="#ffffff" opacity="0.35">{text}</text>'
            f'<text x="{x}" y="{y}" {common} fill="url(#m-chrome)" filter="url(#m-shadow)">{text}</text>')


def badge(cx, cy, r, glyph):
    """Round 3D medallion: chrome ring, dark well, glossy cap, chrome glyph."""
    s = (r * 0.95) / 12  # glyph scale: 24-unit grid fits inside the well
    return f"""<g filter="url(#m-shadow)">
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#m-rim)"/>
    <circle cx="{cx}" cy="{cy}" r="{r-3}" fill="url(#m-well)"/>
    <ellipse cx="{cx}" cy="{cy - r*0.38:.1f}" rx="{r*0.62:.1f}" ry="{r*0.36:.1f}" fill="url(#m-gloss)"/>
  </g>
  <g transform="translate({cx - 12*s:.2f} {cy - 12*s:.2f}) scale({s:.3f})" fill="none" stroke="url(#m-chrome-u)" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
    {GLYPHS[glyph]}
  </g>"""


def svg(w, h, body, title=""):
    t = f"<title>{title}</title>" if title else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f"{t}\n  {defs()}\n  {body}\n</svg>\n")
