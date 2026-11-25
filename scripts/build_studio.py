"""Build the GitHub profile illustrations. Run with Python 3 and Pillow."""
import base64
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "studio"
ART_SPACE = "0 0 2172 724"
ROLES = ("Computer vision", "Language models", "Full-stack apps")
ROLE_COLORS = ("#9ff4d9", "#e5b9ff", "#ffc18e")


def jpeg_uri(content):
    return "data:image/jpeg;base64," + base64.b64encode(content).decode("ascii")


def portrait_uri():
    with Image.open(ROOT / "assets" / "profile-photo.jpg") as original:
        # Frame the same public portrait used in the original profile design.
        portrait = original.crop((319, 366, 667, 714)).convert("RGB")
        portrait.thumbnail((160, 160), Image.Resampling.LANCZOS)
        output = BytesIO()
        portrait.save(output, format="JPEG", quality=88, optimize=True)
    return jpeg_uri(output.getvalue())


def banner(mobile, art, portrait):
    if mobile:
        width, height = 480, 392
        view, frame = "730 0 1442 724", 'width="480" height="196"'
        shade = '<rect y="196" width="480" height="196" fill="#211c39"/><rect y="188" width="480" height="9" fill="url(#edge)"/>'
        photo_x, photo_y, diameter, identity_x, handle_y = 24, 171, 54, 91, 209
        name_x, name_y, name_size = 22, 287, 70
        line_x, line_y, line_size = 27, 323, 20
        role_y, role_size, role_length = 361, 21, 190
        handle_size = 15
        location = ""
    else:
        width, height = 1200, 416
        view, frame = ART_SPACE, 'width="1200" height="416"'
        shade = '<rect width="805" height="416" fill="url(#wall)"/>'
        photo_x, photo_y, diameter, identity_x, handle_y = 48, 47, 64, 129, 73
        name_x, name_y, name_size = 45, 233, 100
        line_x, line_y, line_size = 52, 283, 25
        role_y, role_size, role_length = 341, 24, 219
        handle_size = 17
        location = f'<text class="body" x="{identity_x}" y="100" font-size="18" fill="#f1dff3">Bengaluru, India</text>'

    clips, roles = [], []
    for i, (word, color) in enumerate(zip(ROLES, ROLE_COLORS)):
        initial_width = role_length if i == 0 else 0
        delay = (-1.8, 3.2, 8.2)[i]
        clips.append(f'<clipPath id="word{i}"><rect class="type" x="0" y="-31" width="{initial_width}" height="43" style="animation-delay:{delay}s"/></clipPath>')
        roles.append(f'<text class="mono" clip-path="url(#word{i})" textLength="{role_length}" lengthAdjust="spacingAndGlyphs" font-size="{role_size}" fill="{color}">{word}</text>')

    portrait_cx, portrait_cy = photo_x + diameter / 2, photo_y + diameter / 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="title desc">
  <title id="title">Om Solanki · Computer science and AI/ML</title>
  <desc id="desc">Om’s portrait beside an illustrated Bengaluru studio at dusk. A scan line crosses a retinal image and the lettering cycles through computer vision, language models and full-stack apps.</desc>
  <defs>
    <clipPath id="frame"><rect width="{width}" height="{height}" rx="20"/></clipPath>
    <clipPath id="portrait"><circle cx="{portrait_cx:g}" cy="{portrait_cy:g}" r="{diameter/2:g}"/></clipPath>
    <clipPath id="screen"><path d="M1358 316L1807 316L1807 519L1358 516Z"/></clipPath>
    <linearGradient id="name" x1="0" y1="0" x2="1" y2=".1" gradientUnits="objectBoundingBox"><stop stop-color="#fff0ba"/><stop offset=".42" stop-color="#ffb9a0"/><stop offset="1" stop-color="#f6b7ff"/></linearGradient>
    <linearGradient id="wall"><stop stop-color="#18132d" stop-opacity=".66"/><stop offset=".47" stop-color="#211b39" stop-opacity=".67"/><stop offset="1" stop-color="#241b33" stop-opacity="0"/></linearGradient>
    <linearGradient id="edge" x2="0" y2="1"><stop stop-color="#211c39" stop-opacity="0"/><stop offset="1" stop-color="#211c39"/></linearGradient>
    <linearGradient id="light" x2="0" y2="1"><stop stop-color="#ffe0a4" stop-opacity="0"/><stop offset="1" stop-color="#ffcda2" stop-opacity=".44"/></linearGradient>
    {''.join(clips)}
  </defs>
  <style>
    .serif {{font-family:Georgia,'Liberation Serif','Times New Roman',serif;font-weight:700;font-style:italic}}
    .body {{font-family:'Segoe UI',Arial,sans-serif}}
    .mono {{font-family:'DejaVu Sans Mono','Courier New',monospace}}
    @media (prefers-reduced-motion:no-preference) {{
      .type {{animation:typeword 15s steps(15,end) infinite both}}
      .sweep {{animation:monitor 7.8s ease-in-out infinite}}
    }}
    @keyframes typeword {{0%{{width:0}} 10%,27%{{width:{role_length}px}} 32%,100%{{width:0}}}}
    @keyframes monitor {{0%,32%{{opacity:0;transform:translateY(-55px)}} 40%{{opacity:.66}} 71%{{opacity:.5}} 77%,100%{{opacity:0;transform:translateY(215px)}}}}
  </style>
  <g clip-path="url(#frame)">
    <rect width="{width}" height="{height}" fill="#211c39"/>
    <svg {frame} viewBox="{view}" preserveAspectRatio="xMidYMid slice">
      <image width="2172" height="724" xlink:href="{art}"/>
      <g clip-path="url(#screen)"><g class="sweep" opacity="0"><rect x="1356" y="301" width="456" height="42" fill="url(#light)"/><path d="M1356 343h456" stroke="#ffe3bc" stroke-width="3"/></g></g>
    </svg>
    {shade}
    <circle cx="{portrait_cx:g}" cy="{portrait_cy:g}" r="{diameter/2+3:g}" fill="#ffe3ba"/>
    <image x="{photo_x}" y="{photo_y}" width="{diameter}" height="{diameter}" clip-path="url(#portrait)" xlink:href="{portrait}"/>
    <text class="mono" x="{identity_x}" y="{handle_y}" font-size="{handle_size}" font-weight="bold" letter-spacing="1.7" fill="#ffdfb7">@SOLANKYYY</text>
    {location}
    <text class="serif" x="{name_x}" y="{name_y}" font-size="{name_size}" letter-spacing="-2" fill="url(#name)">Om Solanki</text>
    <text class="body" x="{line_x}" y="{line_y}" font-size="{line_size}" font-weight="550" fill="#fff4ee">Computer Science · AI &amp; ML</text>
    <text class="mono" x="{line_x}" y="{role_y}" font-size="{role_size+4}" fill="#ffbd95">›</text>
    <g transform="translate({line_x+25} {role_y})">{''.join(roles)}</g>
  </g>
</svg>
'''


# The three covers use the same pixel illustration scale as the studio banner.
PAPERS = '''<g stroke-linejoin="miter" stroke-width="2">
  <path d="M-44 12h48v5h6v45h-54z" fill="#74639f" stroke="#aa99d7"/>
  <path d="M-31 5h48v5h6v47h-54z" fill="#b29adc" stroke="#ceb4ed"/>
  <path d="M-16 0h44v10h10v45h-54z" fill="#ffeac6" stroke="#fff4d9"/>
  <path d="M28 0v10h10" fill="none" stroke="#aa79a1"/>
  <path d="M-7 16h29m-29 8h23m-23 8H9" fill="none" stroke="#a86e8e" stroke-width="3"/>
  <path d="M15 38h6v-4h14v4h6v13h-6v4H21v-4h-6z" fill="#543e77" stroke="#a5ead8"/>
  <path d="m37 52 13 12" stroke="#a5ead8" stroke-width="7"/>
</g>'''
RETINA = '''<g>
  <path d="M-25 2h48v4h9v5h8v7h6v9h3v13h-3v8h-6v7h-8v5h-9v4h-48v-4h-9v-5h-7v-7h-5v-8h-3V27h3v-9h5v-7h7V6h9z" fill="#f88677"/>
  <path d="M-21 7h42v4h9v4h7v5h-6v-4H13v-3H-8v4h-15v8h-11V14h13z" fill="#ffb185"/>
  <path d="M-38 42h10v7h15v5h29v-4h16v-6h9v5h-7v6h-8v5h-9v3h-39v-4h-9v-6h-7z" fill="#d96272"/>
  <g fill="none" stroke="#a34b69" stroke-width="2.5" stroke-linecap="square">
    <path d="m14 31-19-4-15-12-12-1m27 13-9-2-12 6-15 3M14 31 2 42l-14 3-13 9m32-17 1 11-4 7"/>
    <path d="m13 31 3-13 8-8m-9 13-10-8-8-2m17 18 14 7 9 7"/>
  </g><path d="M10 24h9v3h4v8h-4v3h-9v-3H7v-8h3z" fill="#ffe5a4"/>
</g>'''
SPROUT = '''<g>
  <path d="M-41 9h13v3h12v5h9v9h5v9h-12v-3h-11v-6h-9v-8h-7z" fill="#8ad8a8"/>
  <path d="M1 27h6V16h7V9h10V5h19v10h-5v7h-7v6H19v3H7v16H1z" fill="#d4ee83"/>
  <path d="M-32 17h10v6h11v5h8v6h7v13" fill="none" stroke="#48756f" stroke-width="3"/>
  <path d="m10 26 9-8 13-5" fill="none" stroke="#69996d" stroke-width="3"/>
  <path d="M-24 43h52v8h-5v9h-6v6h-31v-6h-6v-9h-4z" fill="#eb9b79"/>
  <path d="M-24 43h52v6h-52z" fill="#ffca9b"/><path d="M12 51h9v8h-6v5H5v-5h7z" fill="#c87973"/>
</g>'''

PROJECTS = [
    ("signal", "Signal Desk", ("Trace an answer back to", "the threat report it cites."), "#352549", "#eadffb", "#332244", "#a89ac9", PAPERS),
    ("retina", "RetinaBridge", ("Inspect a heatmap beside", "the original retinal image."), "#452b41", "#ffe3db", "#4a2036", "#cb9cac", RETINA),
    ("agri", "AgriLens", ("Compare two local LLMs", "on 2,200 crop records."), "#243e42", "#def2e1", "#173d39", "#99bdac", SPROUT),
]


def project_cover(title, lines, top, paper, ink, grid, illustration):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 226" width="360" height="226" role="img" aria-labelledby="t d">
  <title id="t">{title}</title><desc id="d">{' '.join(lines)}</desc>
  <defs><clipPath id="card"><rect width="360" height="226" rx="16"/></clipPath>
  <pattern id="dots" width="9" height="9" patternUnits="userSpaceOnUse"><rect x="1" y="1" width="1.3" height="1.3" fill="{grid}"/></pattern></defs>
  <g clip-path="url(#card)">
    <rect width="360" height="226" fill="{paper}"/><rect width="360" height="98" fill="{top}"/>
    <rect width="360" height="98" fill="url(#dots)" opacity=".45"/>
    <g transform="translate(180 12) scale(1.1)">{illustration}</g>
    <path d="M326 22h12v12m0-12-13 13" fill="none" stroke="{paper}" stroke-width="2.5"/>
    <text x="20" y="140" font-family="Georgia,'Liberation Serif',serif" font-size="36" font-weight="bold" fill="{ink}">{title}</text>
    <text x="22" y="174" font-family="Arial,sans-serif" font-size="21" fill="{ink}"><tspan x="22">{lines[0]}</tspan><tspan x="22" dy="26">{lines[1]}</tspan></text>
  </g>
</svg>
'''


def main():
    art = jpeg_uri((ASSETS / "bengaluru-dusk.jpg").read_bytes())
    portrait = portrait_uri()
    for name, mobile in (("hero.svg", False), ("hero-mobile.svg", True)):
        (ASSETS / name).write_text(banner(mobile, art, portrait), encoding="utf-8")
    for slug, *settings in PROJECTS:
        (ASSETS / f"featured-{slug}.svg").write_text(project_cover(*settings), encoding="utf-8")


if __name__ == "__main__":
    main()
