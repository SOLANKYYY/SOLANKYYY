"""Draw the responsive cassette cover and the six linked tape sleeves."""
import base64
from html import escape
from pathlib import Path

ART = Path(__file__).resolve().parents[1] / "assets" / "mixtape"
INK, PAPER, MINT, RED, GOLD = "#20212b", "#fff1d6", "#78ddc6", "#e95034", "#ffc54b"
SANS = "Arial Black,Arial,Helvetica,sans-serif"
MONO = "Courier New,Courier,monospace"

TRACKS = [
    ("Computer vision", "#ffbb91"), ("Language models", "#dfc3ff"),
    ("Full-stack apps", "#9ee8d2"), ("Data experiments", "#b1dcff"),
    ("Arcade games", "#ffdd85"),
]
PROJECTS = [
    ("signal", "A1", "Signal Desk", "Trace a chat answer back", "to the report it cites.", "#ff997d"),
    ("retina", "A2", "RetinaBridge", "See a retinal image beside", "the model’s heatmap.", "#8adecb"),
    ("agrilens", "A3", "AgriLens LLM Benchmark", "Compare two local LLMs", "on 2,200 crop records.", "#ffda78"),
    ("gamearena", "B1", "GameArena", "Play seven arcade games", "in a team tournament.", "#c8b1ef"),
    ("flat-fork", "B2", "Flat & Fork", "Vote on dinner. Trade", "tomorrow’s laundry turn.", "#ffc0cf"),
    ("frameflow", "B3", "FrameFlow", "Skip frames. Add delays.", "Watch the pipeline respond.", "#a7d2f6"),
]


def text(x, y, value, size, *, fill=INK, family=SANS, weight=400, style="", extra=""):
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" style="{style}" {extra}>{escape(value)}</text>')


def reel(x):
    teeth = "".join(f'<rect x="-3" y="-18" width="6" height="9" rx="1.5" fill="{INK}" transform="rotate({a})"/>' for a in range(0,360,60))
    return f'''<g transform="translate({x} 111)">
      <circle r="33" fill="#433e47" stroke="{INK}" stroke-width="3"/>
      <circle r="28" fill="none" stroke="#ac8776" stroke-width="1.4" stroke-dasharray="2 3"/>
      <circle r="21" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>
      <g class="wheel">{teeth}<path d="M-9 0 -4 -7 4 -7 9 0 4 7 -4 7Z" fill="{INK}"/></g>
    </g>'''


def cassette():
    bolts = "".join(f'<g transform="translate({x} {y})"><circle r="4" fill="#f9c39d" stroke="{INK}" stroke-width="1.8"/><path d="m-2 1 4-2" stroke="{INK}" stroke-width="1.3"/></g>' for x,y in ((12,13),(310,13),(12,194),(310,194)))
    marks = "".join(f'<path d="M{x} 137v{6 if x%12 == 0 else 3}" stroke="#dbad79" stroke-width="1.2"/>' for x in range(132,191,6))
    return f'''<rect x="6" y="9" width="324" height="207" rx="16" fill="{INK}"/>
    <rect width="324" height="207" rx="16" fill="{RED}" stroke="{INK}" stroke-width="4"/>
    <rect x="7" y="6" width="310" height="194" rx="12" fill="none" stroke="#ffaf82" stroke-width="2"/>
    <rect x="23" y="15" width="278" height="146" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>
    <rect x="24" y="59" width="276" height="14" fill="{GOLD}"/><rect x="24" y="73" width="276" height="7" fill="{INK}"/>
    {text(37,49,"SIDE A",24,weight=900,style="letter-spacing:-1px")}
    {text(129,48,"THE OM MIX",19,family=MONO,weight=700)}
    <path d="M260 27h23v19h-23z" fill="{INK}"/>{text(265,41,"▶",11,fill=PAPER)}
    <rect x="45" y="84" width="234" height="57" rx="29" fill="#d3aea0" stroke="{INK}" stroke-width="3"/>
    <rect x="111" y="93" width="101" height="33" rx="6" fill="#573f36" stroke="{INK}" stroke-width="3"/>
    <path d="M116 117q27 8 46-1t45-4" fill="none" stroke="#c89e71" stroke-width="2"/>
    <path d="M122 98h69" stroke="#f4ddbd" stroke-width="2"/>{marks}
    {reel(87)}{reel(237)}
    <path d="M67 200l10-27h171l10 27z" fill="#d27c64" stroke="{INK}" stroke-width="3"/>
    <path d="M84 178h155" stroke="#fcb394" stroke-width="2"/>
    <g fill="{INK}"><circle cx="94" cy="193" r="4"/><circle cx="231" cy="193" r="4"/>
    <rect x="121" y="190" width="10" height="8" rx="2"/><rect x="192" y="190" width="10" height="8" rx="2"/></g>
    {bolts}'''


def dial(x, y, scale=1):
    channels = []
    for i, (title, color) in enumerate(TRACKS):
        lag = -((len(TRACKS) - i) % len(TRACKS)) * 3
        channels.append(f'<g class="channel c{i}" opacity="{int(i == 0)}" style="animation-delay:{lag}s">'
                        + text(16,51,title,26,fill=color,weight=700) + '</g>')
    bars = []
    for i,h in enumerate((12,20,29,17,25,11)):
        bars.append(f'<rect class="meter" x="{271+i*8}" y="{52-h}" width="5" height="{h}" rx="1.5" fill="{MINT}" style="animation-delay:{-i*.19:.2f}s"/>')
    return (f'<g transform="translate({x} {y}) scale({scale})"><rect width="336" height="65" rx="7" fill="{INK}"/>'
            + text(17,21,"NOW PLAYING",12,fill=PAPER,family=MONO,weight=700,style="letter-spacing:1.6px")
            + "".join(channels+bars) + '</g>')


def cover(mobile, sticker):
    width, height = (440,470) if mobile else (1100,390)
    panel = "M0 249L440 232V470H0Z" if mobile else "M642 0H1100V390H589Z"
    title_x, title_y, scale = (23,20,.72) if mobile else (40,41,1)
    tape = "translate(35 255) rotate(-8 144 94) scale(.80)" if mobile else "translate(677 76) rotate(-8 162 103) scale(1.08)"
    duck = "translate(297 314) rotate(7 59 59) scale(.79)" if mobile else "translate(939 205) rotate(6 75 75)"
    star = "translate(335 248) scale(.7)" if mobile else "translate(1015 67)"
    playing = dial(22,176,.76) if mobile else dial(44,276,1.02)
    small = text(0,11,"BENGALURU, INDIA",16,weight=700,family=MONO,style="letter-spacing:2px")
    titles = (text(0,109,"Om Solanki",98,weight=900,style="letter-spacing:-6px",extra='textLength="512" lengthAdjust="spacingAndGlyphs"')
              + text(4,193,"on shuffle.",90,fill="#b23929",family="Georgia,Times New Roman,serif",weight=700,style="font-style:italic;letter-spacing:-4px"))
    colophon = (text(18,height-15,"PERSONAL MIXTAPE",11,family=MONO,weight=700,style="letter-spacing:1.1px")
                + text(width-18,height-15,"SIDE A  /  STEREO",11,family=MONO,weight=700,extra='text-anchor="end"',style="letter-spacing:1px"))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">Om Solanki on shuffle</title>
<desc id="desc">A rotating cassette plays computer vision, language models, full-stack apps, data experiments and arcade games. A rubber duck in headphones keeps an eye on the mix.</desc>
<defs>
 <clipPath id="cover"><rect width="{width}" height="{height}" rx="13"/></clipPath>
 <pattern id="speck" width="11" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".65" fill="{INK}" opacity=".16"/><circle cx="7" cy="6" r=".55" fill="{INK}" opacity=".15"/></pattern>
 <pattern id="dots" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.25" fill="#286f66" opacity=".40"/></pattern>
 <style>
 @keyframes spin{{to{{transform:rotate(360deg)}}}}
 @keyframes channel{{0%,18%{{opacity:1}}20%,99.8%{{opacity:0}}100%{{opacity:1}}}}
 @keyframes meter{{0%,100%{{transform:scaleY(.48)}}50%{{transform:scaleY(1)}}}}
 @keyframes nod{{0%,100%{{transform:rotate(-2deg)}}50%{{transform:rotate(2deg)}}}}
 @media (prefers-reduced-motion:no-preference){{
 .wheel{{animation:spin 3.2s linear infinite}} .channel{{animation:channel 15s linear infinite}}
 .meter{{transform-box:fill-box;transform-origin:center bottom;animation:meter 1.05s ease-in-out infinite}}
 .duck{{transform-box:fill-box;transform-origin:center bottom;animation:nod 2.5s ease-in-out infinite}}
 }}
 </style>
</defs>
<g clip-path="url(#cover)">
<rect width="{width}" height="{height}" fill="{PAPER}"/><path d="{panel}" fill="{MINT}"/><path d="{panel}" fill="url(#dots)"/>
<rect width="{width}" height="{height}" fill="url(#speck)"/>
<g transform="{star}" fill="{GOLD}" stroke="{INK}" stroke-width="2.5"><path d="m0-26 6 15 14-8-6 15 17 3-16 6 9 13-16-6-5 17-4-16-15 7 8-14-17-4 17-5-7-15 14 8z"/></g>
<g transform="translate({title_x} {title_y}) scale({scale})">{small}{titles}</g>
{playing}
<g transform="{tape}">{cassette()}</g>
<g transform="{duck}"><g class="duck"><image width="155" height="155" xlink:href="data:image/png;base64,{sticker}"/></g></g>
<rect y="{height-31}" width="{width}" height="31" fill="{PAPER}"/><path d="M0 {height-31}H{width}" stroke="{INK}" stroke-width="2"/>{colophon}
</g></svg>
'''


def sleeve(entry):
    slug, code, title, line1, line2, color = entry
    size = 17 if len(title)>18 else 23
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="270" height="96" viewBox="0 0 270 96" role="img" aria-labelledby="title">
<title id="title">{escape(title)}. {escape(line1)} {escape(line2)}</title>
<rect x="1" y="1" width="268" height="94" rx="7" fill="{color}" stroke="{INK}" stroke-width="2"/>
<path d="M35 2v92m5-92v92" fill="none" stroke="{INK}" stroke-width="1.5"/>
<g fill="none" stroke="{INK}" stroke-width="2"><circle cx="18" cy="18" r="6"/><circle cx="18" cy="18" r="2"/><circle cx="18" cy="78" r="6"/><circle cx="18" cy="78" r="2"/></g>
{text(18,53,code,13,weight=700,family=MONO,extra='text-anchor="middle"')}
{text(50,30,title,size,weight=800,style='letter-spacing:-.7px')}
{text(50,58,line1,15,family='Arial,Helvetica,sans-serif')}
{text(50,78,line2,15,family='Arial,Helvetica,sans-serif')}
</svg>
'''


if __name__ == "__main__":
    sticker = base64.b64encode((ART / "duck.png").read_bytes()).decode()
    for mobile, filename in ((False,"cover.svg"),(True,"cover-mobile.svg")):
        (ART / filename).write_text(cover(mobile,sticker), encoding="utf-8")
    for project in PROJECTS:
        (ART / f"{project[0]}.svg").write_text(sleeve(project), encoding="utf-8")
