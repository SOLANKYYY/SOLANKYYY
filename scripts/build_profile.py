"""Build the profile's theme-aware SVG assets from PROFILE.md.

Requires Pillow, fontTools, and the Windows Georgia Italic and Arial fonts.
The supplied portrait is embedded unchanged; motion is limited to status dots.
"""
from pathlib import Path
from html import escape
import base64
import re
from PIL import ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'studio'
OUT.mkdir(parents=True, exist_ok=True)
SOURCE = (ROOT / 'PROFILE.md').read_text(encoding='utf-8-sig')
FONT = TTFont(r'C:\Windows\Fonts\georgiai.ttf')
GLYPHS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
UPM = FONT['head'].unitsPerEm
PHOTO = base64.b64encode((ROOT / 'assets/profile-photo.jpg').read_bytes()).decode()
PALETTES = [('var(--surface)','var(--accent)','var(--line)')]*4
INK = 'var(--ink)'
CSS = '''
  :root{--ink:#233d45;--accent:#356b77;--secondary:#8a6c47;--line:#d7e2e4;--surface:#fbfcfc;--tint:#eef4f4;--header-start:#fbf9f5;--header-end:#eaf1ef;--status:#25834c}
  @media(prefers-color-scheme:dark){:root{--ink:#dce8ec;--accent:#91cbd2;--secondary:#cdb184;--line:#354a54;--surface:#142129;--tint:#20343d;--header-start:#19232b;--header-end:#193334;--status:#7bdc9c}}
  .pulse{transform-box:fill-box;transform-origin:center;animation:pulse 3s ease-out infinite}
  @keyframes pulse{0%{transform:scale(1);opacity:.45}80%,100%{transform:scale(2.1);opacity:0}}
  @media(prefers-reduced-motion:reduce){.pulse{animation:none;opacity:.15}}
'''

def clean(s):
    s = re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',s)
    return s.replace('**','').replace('`','').replace('🟢 ','').strip()

def script(s,x,y,size,color,max_width=None,center=False):
    advance = sum(FONT['hmtx'].metrics[CMAP.get(ord(c),'.notdef')][0] for c in s)
    scale = size / UPM
    if max_width and advance*scale > max_width:
        scale = max_width/advance
    if center:
        x -= advance*scale/2
    parts=[]
    for c in s:
        glyph = CMAP.get(ord(c),'.notdef')
        pen = SVGPathPen(GLYPHS)
        GLYPHS[glyph].draw(pen)
        path=pen.getCommands()
        if path:
            parts.append(f'<path d="{path}" transform="translate({x:.2f} {y:.2f}) scale({scale:.6f} {-scale:.6f})"/>')
        x += FONT['hmtx'].metrics[glyph][0]*scale
    return f'<g fill="{color}" aria-label="{escape(s,quote=True)}">'+''.join(parts)+'</g>'

def text(s,x,y,size=20,color=INK,weight=400,anchor='start'):
    return f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color}">{escape(s)}</text>'

def wrap(s,width,size):
    font=ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf',size)
    lines=[]
    line=''
    for word in s.split():
        trial=(line+' '+word).strip()
        if line and font.getlength(trial)>width:
            lines.append(line)
            line=word
        else:
            line=trial
    if line:lines.append(line)
    return lines

def base(w,h,palette,title,body,frame=False):
    bg,accent,border=palette
    surface=f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="{bg}" stroke="{border}"/>' if frame else ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(title)}. Full text is available in PROFILE.md.</desc>
<style>{CSS}</style><defs><clipPath id="frame"><rect width="{w}" height="{h}" rx="14"/></clipPath></defs>
<g clip-path="url(#frame)">{surface}{body}</g></svg>\n'''

def panel(name,title,blocks,index=0,kicker=None,cta=None):
    palette=PALETTES[index%4]
    bg,accent,border=palette
    for mobile in (False,True):
        w=440 if mobile else 960
        pad=12 if mobile else 20
        size=18 if mobile else 21
        line_height=29 if mobile else 34
        parts=[]
        if kicker:
            parts.append(text(kicker.upper(),pad,28,11 if mobile else 12,'var(--secondary)'))
        parts.append(script(title,pad,79,36 if mobile else 43,accent,w-pad*2))
        parts.append(f'<path d="M{pad} 101H{w-pad}" fill="none" stroke="{border}"/>')
        y=136
        for label,paragraph in blocks:
            if label:
                for line in wrap(label,w-pad*2,size):
                    parts.append(text(line,pad,y,size,accent,700));y+=line_height
                y+=3
            for line in wrap(clean(paragraph),w-pad*2,size):
                parts.append(text(line,pad,y,size));y+=line_height
            y+=17
        if cta:
            parts.append(text(cta,pad,y,16,accent,700));y+=28
        h=int(y+16)
        suffix='-mobile' if mobile else ''
        (OUT/(name+suffix+'.svg')).write_text(base(w,h,palette,title,''.join(parts)),encoding='utf-8')

def hero():
    for mobile in (False,True):
        w,h=(440,580) if mobile else (960,410)
        cx,cy,r=(220,144,92) if mobile else (760,186,106)
        scale=r/140*.625
        imgx,imgy=cx-464*scale,cy-585.6*scale
        parts=[f"""<defs>
<linearGradient id="wash" x2="1" y2="1"><stop stop-color="var(--header-start)"/><stop offset="1" stop-color="var(--header-end)"/></linearGradient>
<pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="var(--line)" stroke-width=".5"/></pattern>
<clipPath id="portrait"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath></defs>
<rect width="{w}" height="{h}" fill="url(#wash)"/>
<rect x="{20 if mobile else 600}" y="28" width="{400 if mobile else 330}" height="285" fill="url(#grid)" opacity=".6"/>
<circle cx="{cx}" cy="{cy}" r="{r+9}" fill="none" stroke="var(--line)"/>
<circle cx="{cx}" cy="{cy}" r="{r+3}" fill="var(--surface)"/>
<g clip-path="url(#portrait)"><image x="{imgx}" y="{imgy}" width="{720*scale}" height="{1280*scale}" href="data:image/jpeg;base64,{PHOTO}"/></g>
<circle cx="{cx+r*.73}" cy="{cy+r*.73}" r="15" fill="var(--surface)"/>
<circle class="pulse" cx="{cx+r*.73}" cy="{cy+r*.73}" r="9" fill="#16a34a"/>
<circle cx="{cx+r*.73}" cy="{cy+r*.73}" r="9" fill="#16a34a"/>"""]
        if mobile:
            parts.append(text('SOLANKYYY / SELECTED WORK',220,28,11,'var(--accent)',anchor='middle'))
            parts.append(script('Om Solanki',220,324,61,INK,392,True))
            parts.append(script('Ideas, made useful.',220,375,28,'var(--secondary)',390,True))
            parts.append(text('Applied AI · Computer vision · Web',220,421,17,anchor='middle'))
            parts.append(text('AI/ML student · Bengaluru, India',220,452,16,anchor='middle'))
            parts.append('<path d="M28 480H412" stroke="var(--line)"/><circle class="pulse" cx="122" cy="519" r="5" fill="#16a34a"/><circle cx="122" cy="519" r="5" fill="#16a34a"/>')
            parts.append(text('Open to collaboration',137,525,15,'var(--status)'))
        else:
            parts.append(text('SOLANKYYY / SELECTED WORK',44,48,12,'var(--accent)'))
            parts.append(script('Om Solanki',40,187,84,INK,550))
            parts.append(script('Ideas, made useful.',44,250,36,'var(--secondary)',530))
            parts.append(text('Applied AI · Computer vision · Web',44,299,19))
            parts.append('<path d="M44 341H916" stroke="var(--line)"/>')
            parts.append(text('AI/ML student · Bengaluru, India',44,380,16))
            parts.append('<circle class="pulse" cx="701" cy="375" r="5" fill="#16a34a"/><circle cx="701" cy="375" r="5" fill="#16a34a"/>')
            parts.append(text('Open to collaboration',716,381,16,'var(--status)'))
        parts.append(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="none" stroke="var(--line)"/>')
        (OUT/('hero-mobile.svg' if mobile else 'hero.svg')).write_text(base(w,h,PALETTES[0],'Om Solanki — ideas, made useful',''.join(parts)),encoding='utf-8')

def section(name):
    return SOURCE.split('## '+name+'\n',1)[1].split('\n## ',1)[0]

def paragraphs(raw):
    return [clean(x) for x in raw.split('\n\n') if x.strip() and not x.startswith(('<','---'))]

hero()
about=paragraphs(section('About me'))
panel('about','A little about me',[(None,p) for p in about if not p.startswith('Open to collaboration')],1,'01 / The introduction')
panel('focus','Where curiosity takes me',[
    ('Applied machine learning','I explore how models should be evaluated, what their errors reveal, and how experiments can be made reproducible.'),
    ('Computer vision','I work with image-processing and recognition workflows, with an interest in making model decisions easier to inspect.'),
    ('Software & interfaces','I connect technical experiments with clear APIs, thoughtful controls, and applications people can explore.')],2,'02 / Areas of interest')

projects=[]
raw_projects=section('Selected projects').split('\n### ')[1:]
icons=[
    '<path d="M5 24Q24 3 43 24Q24 45 5 24Z"/><circle cx="24" cy="24" r="7"/>',
    '<path d="M24 5L40 11V24Q38 37 24 44Q10 37 8 24V11Z"/><path d="M17 21H31M17 27H27"/>',
    '<path d="M10 36Q5 10 37 8Q43 34 10 36ZM10 36L31 16"/><path d="M22 26V17M22 26H32"/>',
    '<path d="M11 13L35 12L24 36ZM11 13L24 25L35 12M24 25V36"/><circle cx="11" cy="13" r="5"/><circle cx="35" cy="12" r="5"/><circle cx="24" cy="36" r="5"/>',
    '<path d="M6 17V7H16M32 7H42V17M42 31V41H32M16 41H6V31"/><path d="M16 31Q24 37 32 31"/><circle cx="18" cy="22" r="1"/><circle cx="30" cy="22" r="1"/>',
    '<path d="M22 6V23M26 6V23M22 19Q15 9 11 17Q5 27 7 38Q12 44 21 35V23M26 19Q33 9 37 17Q43 27 41 38Q36 44 27 35V23"/>'
]
for i,raw in enumerate(raw_projects):
    raw=raw.split('<details>')[0].strip()
    lines=raw.split('\n',1)
    title=lines[0].split(' / ',1)[1]
    ps=paragraphs(lines[1])
    subtitle=ps[0]
    links=re.findall(r'\]\((https://github.com/[^)]+)\)',raw)
    tags=next(p.removeprefix('Built with:').strip() for p in ps if p.startswith('Built with:'))
    short_title={'AgriLens LLM Benchmark':'AgriLens','TraceLens Sysmon Lab':'TraceLens','VeraGate Face Lab':'VeraGate'}.get(title,title)
    bg,accent,border=PALETTES[i%4]
    card=f'<rect x="24" y="23" width="60" height="60" rx="16" fill="var(--tint)"/>'
    card+=f'<g transform="translate(30 29)" fill="none" stroke="{accent}" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">{icons[i]}</g>'
    card+=script(short_title,102,66,31,accent,275)
    card+=f'<path d="M397 31H409V43M409 31L396 44" fill="none" stroke="{accent}" stroke-width="2" stroke-linecap="round"/>'
    card+=text(subtitle,24,117,18)
    card+=text(tags,24,151,15,accent)
    (OUT/f'project-card-{i+1}.svg').write_text(base(440,178,PALETTES[i%4],title+' — '+subtitle,card,frame=True),encoding='utf-8')
    projects.append((title,links[0],subtitle))

toolkit=[]
for line in section('Technical toolkit').splitlines():
    if line.startswith('| **'):
        cols=line.strip('|').split('|');toolkit.append((clean(cols[0]),clean(cols[1])))
panel('toolkit','The tools on my desk',toolkit,3,'03 / Technical toolkit')
panel('approach','From a question to a project',[
    ('01 · Understand','Start with the problem, the data, and the constraints before choosing a model or framework.'),
    ('02 · Experiment','Establish a baseline, compare results, and inspect errors as well as headline metrics.'),
    ('03 · Build','Connect processing, inference or application logic, APIs, and an interface people can use.'),
    ('04 · Refine','Document assumptions and limitations, then use what the project reveals to guide the next iteration.')],0,'04 / How I approach the work')
panel('learning','Learning through building',[(None,p) for p in paragraphs(section('Learning through building'))],1,'05 / A few notes from the journey')
panel('exploring','The next things to explore',[
    ('Model evaluation','Better baselines, error analysis, and reproducible comparisons.'),
    ('Computer vision','Inference pipelines, visual explanations, and understandable decision boundaries.'),
    ('Software foundations','Data structures, algorithms, databases, and clear API design.'),
    ('Application development','Turning individual experiments into coherent, documented user workflows.')],2,'06 / Currently exploring')
panel('connect','Good ideas begin with hello',[(None,p) for p in paragraphs(section("Let's connect")) if not p.startswith(('Email me','Open to collaboration'))],0,'07 / Let’s connect','Open to collaboration · Bengaluru, India')

for mobile in (False,True):
    w,h=(440,112) if mobile else (960,112)
    content=script('Keep learning. Keep building.',w/2,67,24 if mobile else 35,'var(--secondary)',w-24,True)
    (OUT/('footer-mobile.svg' if mobile else 'footer.svg')).write_text(base(w,h,PALETTES[1],'Keep learning. Keep building.',content),encoding='utf-8')

contacts=[('portfolio','Portfolio ↗','https://solanki-portfolio-v4.vercel.app/'),('linkedin','LinkedIn','https://www.linkedin.com/in/solanki-om-b89793330/'),('email','Email me','mailto:om.n.solanki49@gmail.com'),('x','Find me on X','https://x.com/Om_solanki49')]
for i,(slug,label,_) in enumerate(contacts):
    (OUT/(slug+'.svg')).write_text(base(180,48,PALETTES[i],label,text(label,90,31,17,PALETTES[i][1],600,'middle'),frame=True),encoding='utf-8')

def picture(name,alt,link=None):
    pic=f'<picture>\n  <source media="(max-width: 600px)" srcset="assets/studio/{name}-mobile.svg">\n  <img src="assets/studio/{name}.svg" width="100%" alt="{escape(alt,quote=True)}">\n</picture>'
    if link:pic=f'<a href="{link}">\n{pic}\n</a>'
    return pic+'\n\n'

def contact_row():
    return '<p align="center">\n'+'\n'.join(f'  <a href="{url}"><img src="assets/studio/{slug}.svg" width="130" alt="{label}"></a>' for slug,label,url in contacts)+'\n</p>\n\n'

md=picture('hero','Om Solanki. AI/ML student in Bengaluru, India. Open to collaboration. Portrait with a green status dot.')
md+=contact_row()
md+='<p align="center"><a href="PROFILE.md">Read the complete profile in text</a></p>\n\n'
md+=picture('about','About Om: AI/ML student at Jain University, working across computer vision, language-model evaluation, security analytics, and web development.')
md+=picture('focus','Focus: applied machine learning, computer vision, and software interfaces.')
md+='<p align="center">\n'
for i,(title,link,subtitle) in enumerate(projects):
    md+=f'  <a href="{link}"><img src="assets/studio/project-card-{i+1}.svg" width="410" alt="{escape(title+": "+subtitle,quote=True)}"></a>\n'
md+='</p>\n\n'
md+='<details>\n<summary><strong>More experiments to explore</strong></summary>\n\n'
md+=section('Selected projects').split('<details>',1)[1].split('<br>',1)[1].split('</details>')[0].strip()+'\n\n</details>\n\n'
for name,alt in [('toolkit','Technical toolkit: languages, machine learning, vision, data, web, UI, databases, and local LLM experiments.'),('approach','Project approach: understand, experiment, build, and refine.'),('learning','Learning through building: notes about connecting experiments, interfaces, and software foundations.'),('exploring','Currently exploring model evaluation, computer vision, software foundations, and application development.')]:
    md+=picture(name,alt)
md+='<p align="center"><a href="https://github.com/SOLANKYYY?tab=repositories">Browse all repositories ↗</a></p>\n\n'
md+=picture('connect','Open to collaboration on applied AI, computer vision, useful web tools, and open-source improvements.')+contact_row()+picture('footer','Keep learning. Keep building.')
(ROOT/'ReadMe.md').write_text(md.rstrip()+'\n',encoding='utf-8')
print(f'Built {len(list(OUT.glob("*.svg")))} theme-aware SVG assets and the visual README.')
