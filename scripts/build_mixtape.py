"""Build the GitHub-safe album cover and six linked project sleeves."""
import base64
from html import escape
from pathlib import Path

ART = Path(__file__).resolve().parents[1] / "assets" / "mixtape"
SANS = "Inter,Arial,Helvetica,sans-serif"
MONO = "IBM Plex Mono,Consolas,Liberation Mono,monospace"
INK = "#151630"
WHITE = "#f7f5ff"
MUTED = "#d7d9f1"
TRACK_SECONDS = 6

# The A and B sides follow the six featured repositories in their pinned order.
TRACKS = (
    ("A1", "Source-backed search", "Follow a chat answer back to its report.", "#9fc0ff"),
    ("A2", "Computer vision", "Look at the pixels behind a prediction.", "#d2aaff"),
    ("A3", "Language models", "Give two models the same seven numbers.", "#d8ee8e"),
    ("B1", "Arcade games", "Keep score while fifty teams play.", "#ff91c2"),
    ("B2", "Full-stack apps", "Give tonight’s kitchen shift to a flatmate.", "#87dfff"),
    ("B3", "Data experiments", "Turn up the delay and watch frames drop.", "#aeb0ff"),
)

# Each mark represents the thing visitors can actually explore in the repo.
PROJECTS = (
    ("signal", "Signal Desk", "Trace a chat answer back", "to the report it cites.",
     "#bacbff", "#83a6ff", '<path d="M4 9h9l5 5h10M4 23h9l5-5h10"/><circle cx="3" cy="9" r="2"/><circle cx="3" cy="23" r="2"/><circle cx="29" cy="16" r="3"/>'),
    ("retina", "RetinaBridge", "See a retinal image beside", "the model’s heatmap.",
     "#e2c6ff", "#c58cf9", '<path d="M1 16q15-19 30 0-15 19-30 0Z"/><circle cx="16" cy="16" r="6"/><circle cx="17" cy="15" r="1.5"/>'),
    ("agrilens", "AgriLens LLM Benchmark", "Compare two local models", "on 2,200 crop records.",
     "#e7f8a4", "#c2e574", '<path d="M6 27c2-8 9-13 18-20M9 23C4 12 12 3 28 3c0 14-6 23-19 20Z"/><path d="m15 17-1-6m5 2 5-1"/>'),
    ("gamearena", "GameArena", "Play seven arcade games", "in a team tournament.",
     "#ffbdde", "#ff87b9", '<path d="M9 10h14q4 0 6 8l2 7q-2 4-5 1l-5-5H11l-5 5q-4 3-5-1l2-9q2-6 6-6Z"/><path d="M8 13v6m-3-3h6"/><circle cx="23" cy="15" r="1"/><circle cx="26" cy="18" r="1"/>'),
    ("flat-fork", "Flat & Fork", "Vote on dinner. Hand over", "today’s laundry turn.",
     "#b5edff", "#78d6f2", '<circle cx="18" cy="16" r="8"/><circle cx="18" cy="16" r="5"/><path d="M3 4v9q1 4 3 0V4M4.5 16v12M29 4v24"/>'),
    ("frameflow", "FrameFlow", "Skip frames. Add delays.", "Watch the pipeline respond.",
     "#c5bdff", "#a9a0fa", '<rect x="11" y="6" width="19" height="15" rx="2"/><path d="M7 10H5v15h20v-2M2 15v13h18"/><path d="m16 10 7 4-7 4z"/>'),
)


def label(x, y, value, size, *, fill=WHITE, weight=400, family=SANS, attrs=""):
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" {attrs}>{escape(value)}</text>')


def player(x, y, scale):
    """A 36-second playlist with six full-size, individually readable tracks."""
    slots = "".join(f'<rect x="{17+i*66}" y="99" width="59" height="4" rx="2"/>' for i in range(len(TRACKS)))
    out = [f'<g transform="translate({x} {y}) scale({scale})">',
           '<rect x=".75" y=".75" width="424.5" height="117" rx="13" fill="#141932" stroke="#5662a5" stroke-width="1.5"/>',
           label(17,25,"NOW PLAYING",13,family=MONO,weight=700,fill="#c4c9ed",attrs='letter-spacing="1.6"'),
           f'<g fill="#3a416b">{slots}</g>']
    for i, (code, name, line, color) in enumerate(TRACKS):
        # Start each later track in its hidden portion of the cycle.
        delay = -((len(TRACKS)-i) % len(TRACKS)) * TRACK_SECONDS
        out.extend([f'<g class="track" opacity="{int(i==0)}" style="animation-delay:{delay}s">',
                    label(409,25,code,14,family=MONO,fill=color,weight=700,attrs='text-anchor="end"'),
                    label(16,61,name,31,weight=750,fill=color,attrs='letter-spacing="-.6"'),
                    label(17,85,line,16,fill=WHITE),
                    f'<rect x="{17+i*66}" y="99" width="59" height="4" rx="2" fill="{color}"/></g>'])
    for i,h in enumerate((12,19,30,22,13,25)):
        out.append(f'<rect class="meter" x="{353+i*10}" y="{64-h}" width="5" height="{h}" rx="2" fill="#a5b5ff" style="animation-delay:{-.23*i:.2f}s"/>')
    return "".join([*out, "</g>"])


def turn_reel(cx, cy, speed):
    # Clip and rotate only the printed hub. The tape window stays aligned.
    return f'''<g transform="translate({cx} {cy})"><g clip-path="url(#hub)">
    <g class="reel" style="animation-duration:{speed}s"><use xlink:href="#rooftop" x="{-cx}" y="{-cy}"/></g></g></g>'''


def cover(mobile, artwork):
    w,h = (460,571) if mobile else (1120,432)
    margin = 22 if mobile else 40
    location_y = 316 if mobile else 54
    name_y, sub_y = (376,428) if mobile else (153,236)
    name_size, sub_size = (65,59) if mobile else (94,90)
    name_width = 303 if mobile else 452
    placement = 'translate(0 -2) scale(.29948)' if mobile else 'translate(430 -7) scale(.45)'
    player_group = player(margin,446,.975) if mobile else player(margin,275,1)
    direction = 'x1="0" x2="0" y1="0" y2="1"' if mobile else 'x1="0" x2="1" y1="0" y2="0"'
    fade = ('<stop offset="0" stop-color="#10142e" stop-opacity="0"/><stop offset=".78" stop-color="#10142e" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#10142e"/>') if mobile else (
            '<stop offset="0" stop-color="#10142e"/><stop offset=".40" stop-color="#10142e"/>'
            '<stop offset=".53" stop-color="#10142e" stop-opacity=".45"/><stop offset=".61" stop-color="#10142e" stop-opacity="0"/>')
    fade_h = 307 if mobile else h
    # Without CSS animation (including a reduced-motion preference), track A1 is visible.
    static_alt = "Six tracks cover search, computer vision, language models, arcade games, full-stack apps and data experiments."
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="cover-title cover-desc">
<title id="cover-title">Om Solanki on shuffle</title>
<desc id="cover-desc">A headphone-wearing duck sits on a cassette deck above the Bengaluru skyline at night. {static_alt}</desc>
<defs>
 <clipPath id="outer"><rect width="{w}" height="{h}" rx="17"/></clipPath>
 <clipPath id="hub"><circle r="35"/></clipPath>
 <image id="rooftop" width="1536" height="1024" preserveAspectRatio="none" xlink:href="data:image/jpeg;base64,{artwork}"/>
 <linearGradient id="image-fade" {direction} gradientUnits="objectBoundingBox">{fade}</linearGradient>
 <linearGradient id="title-ink"><stop stop-color="#9caeff"/><stop offset=".51" stop-color="#d4a5ff"/><stop offset="1" stop-color="#ff87be"/></linearGradient>
 <style>
 @keyframes play{{0%,15.7%{{opacity:1}}16.6667%,99.8%{{opacity:0}}100%{{opacity:1}}}}
 @keyframes wind{{to{{transform:rotate(360deg)}}}}
 @keyframes levels{{0%,100%{{transform:scaleY(.45)}}50%{{transform:scaleY(1)}}}}
 @media (prefers-reduced-motion:no-preference){{
  .track{{animation:play {len(TRACKS)*TRACK_SECONDS}s linear infinite}}
  .reel{{animation:wind 4s linear infinite;transform-origin:0 0}}
  .meter{{animation:levels 1.25s ease-in-out infinite;transform-box:fill-box;transform-origin:center bottom}}
 }}
 </style>
</defs>
<g clip-path="url(#outer)">
 <rect width="{w}" height="{h}" fill="#10142e"/>
 <g transform="{placement}"><use xlink:href="#rooftop"/>{turn_reel(725,611,4)}{turn_reel(902,611,4.4)}</g>
 <rect width="{w}" height="{fade_h}" fill="url(#image-fade)"/>
 <g transform="translate({margin} {location_y-12})"><circle cx="7" cy="6" r="5" fill="#ff86c2"/><path d="M17 0q6 6 0 12m6-16q10 10 0 20" fill="none" stroke="#889fff" stroke-width="2.2" stroke-linecap="round"/></g>
 {label(margin+41,location_y,"BENGALURU, INDIA",15,fill=MUTED,weight=700,family=MONO,attrs='letter-spacing="1.5"')}
 {label(margin-3,name_y,"Om Solanki",name_size,weight=800,attrs=f'letter-spacing="-4" textLength="{name_width}" lengthAdjust="spacingAndGlyphs"')}
 {label(margin-1,sub_y,"on shuffle.",sub_size,fill='url(#title-ink)',weight=700,family='Georgia,Times New Roman,serif',attrs='font-style="italic" letter-spacing="-3"')}
 {player_group}
</g>
<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="17" fill="none" stroke="#54558b" stroke-width="1.5"/>
</svg>
'''


def sleeve(project, track):
    _, title, first, second, light, bright, mark = project
    code = track[0]
    size = 18 if len(title)>18 else 25
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="110" viewBox="0 0 300 110" role="img" aria-labelledby="title">
<title id="title">{escape(code)} · {escape(title)}. {escape(first)} {escape(second)}</title>
<defs><linearGradient id="wash" x2="1" y2=".8"><stop stop-color="{light}"/><stop offset="1" stop-color="{bright}"/></linearGradient></defs>
<rect x="1" y="1" width="298" height="108" rx="11" fill="url(#wash)" stroke="{INK}" stroke-width="2"/>
<path d="M56 3v104" stroke="{INK}" stroke-opacity=".45" stroke-dasharray="2 3"/>
<g transform="translate(11 21)" stroke="{INK}" fill="none" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">{mark}</g>
{label(27,83,code,15,fill=INK,family=MONO,weight=700,attrs='text-anchor="middle"')}
{label(69,38,title,size,fill=INK,weight=750,attrs='letter-spacing="-.6"')}
{label(69,67,first,16,fill=INK)}
{label(69,88,second,16,fill=INK)}
</svg>
'''


if __name__ == "__main__":
    image = base64.b64encode((ART / "rooftop-radio.jpg").read_bytes()).decode("ascii")
    for mobile, filename in ((False,"cover.svg"),(True,"cover-mobile.svg")):
        (ART / filename).write_text(cover(mobile,image), encoding="utf-8")
    for project, track in zip(PROJECTS, TRACKS, strict=True):
        (ART / (project[0] + ".svg")).write_text(sleeve(project, track), encoding="utf-8")
