"""Build the profile's light SVG panels from PROFILE.md.

Requires Pillow, fontTools, and the Windows Gabriola and Arial fonts.
The supplied portrait is embedded unchanged; only its SVG frame is animated.
"""
from pathlib import Path
from html import escape
import base64
import re
from PIL import ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'pastel'
OUT.mkdir(parents=True, exist_ok=True)
SOURCE = (ROOT / 'PROFILE.md').read_text(encoding='utf-8-sig')
FONT = TTFont(r'C:\Windows\Fonts\Gabriola.ttf')
GLYPHS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
UPM = FONT['head'].unitsPerEm
PHOTO = base64.b64encode((ROOT / 'assets/profile-photo.jpg').read_bytes()).decode()
PALETTES = [('#fff5ee','#9b5a45','#efd8ca'),('#f4effb','#70548b','#dfd2ee'),('#edf8f4','#346e5b','#c9e4d8'),('#eef5ff','#496a99','#cdddf0')]
INK = '#443e50'
CSS = '''
  .orbit{transform-box:fill-box;transform-origin:center;animation:spin 32s linear infinite}
  .pulse{transform-box:fill-box;transform-origin:center;animation:pulse 3s ease-out infinite}
  .ribbon{stroke-dasharray:8 14;animation:flow 12s linear infinite}
  .float{animation:float 12s ease-in-out infinite alternate}
  @keyframes spin{to{transform:rotate(360deg)}}
  @keyframes pulse{0%{transform:scale(1);opacity:.45}80%,100%{transform:scale(2.1);opacity:0}}
  @keyframes flow{to{stroke-dashoffset:-220}}
  @keyframes float{to{transform:translateX(28px)}}
  @media(prefers-reduced-motion:reduce){.orbit,.pulse,.ribbon,.float{animation:none}.pulse{opacity:.15}}
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

def base(w,h,palette,title,body):
    bg,accent,border=palette
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(title)}. Full text is available in PROFILE.md.</desc>
<style>{CSS}</style><defs><clipPath id="frame"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24"/></clipPath></defs>
<g clip-path="url(#frame)"><rect width="{w}" height="{h}" fill="{bg}"/>
<circle class="float" cx="{w-20}" cy="0" r="150" fill="{border}" opacity=".28"/>
{body}</g><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="none" stroke="{border}"/></svg>\n'''

def panel(name,title,blocks,index=0,kicker=None,cta=None):
    palette=PALETTES[index%4]
    bg,accent,border=palette
    for mobile in (False,True):
        w=440 if mobile else 960
        pad=28 if mobile else 44
        size=18 if mobile else 21
        line_height=29 if mobile else 34
        parts=[]
        if kicker:
            parts.append(text(kicker.upper(),pad,38,11 if mobile else 12,accent))
        parts.append(script(title,pad,91,60 if mobile else 70,accent,w-pad*2))
        parts.append(f'<path class="ribbon" d="M{pad} 112Q{w/2} 102 {w-pad} 112" fill="none" stroke="{border}" stroke-width="2"/>')
        y=151
        for label,paragraph in blocks:
            if label:
                for line in wrap(label,w-pad*2,size):
                    parts.append(text(line,pad,y,size,accent,700));y+=line_height
                y+=3
            for line in wrap(clean(paragraph),w-pad*2,size):
                parts.append(text(line,pad,y,size));y+=line_height
            y+=21
        if cta:
            parts.append(text(cta,pad,y,16,accent,700));y+=28
        h=int(y+16)
        suffix='-mobile' if mobile else ''
        (OUT/(name+suffix+'.svg')).write_text(base(w,h,palette,title,''.join(parts)),encoding='utf-8')

def hero():
    for mobile in (False,True):
        w,h=(440,690) if mobile else (960,500)
        cx,cy,r=(220,163,106) if mobile else (755,238,132)
        scale=r/140*.625
        imgx,imgy=cx-464*scale,cy-585.6*scale
        parts=[f'''<defs><linearGradient id="wash" x2="1" y2="1"><stop stop-color="#fff7ee"/><stop offset=".42" stop-color="#f4edfc"/><stop offset="1" stop-color="#e7f7f1"/></linearGradient><clipPath id="portrait"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath></defs>
<rect width="{w}" height="{h}" fill="url(#wash)"/>
<path class="ribbon" d="M-80 {h-75}Q{w*.3} {h-150} {w*.6} {h-75}T{w+100} {h-75}" fill="none" stroke="#dec4e3" stroke-width="2"/>
<g class="orbit"><circle cx="{cx}" cy="{cy}" r="{r+22}" fill="none" stroke="#c9dacc"/><circle cx="{cx}" cy="{cy-r-22}" r="6" fill="#9b80b4"/><circle cx="{cx}" cy="{cy+r+22}" r="4" fill="#66b595"/></g>
<circle cx="{cx}" cy="{cy}" r="{r+7}" fill="#fffdfa"/>
<g clip-path="url(#portrait)"><image x="{imgx}" y="{imgy}" width="{720*scale}" height="{1280*scale}" href="data:image/jpeg;base64,{PHOTO}"/></g>
<circle cx="{cx+r*.73}" cy="{cy+r*.73}" r="16" fill="#fffdfa"/>
<circle class="pulse" cx="{cx+r*.73}" cy="{cy+r*.73}" r="9" fill="#16a34a"/>
<circle cx="{cx+r*.73}" cy="{cy+r*.73}" r="9" fill="#16a34a"/>''']
        if mobile:
            parts.append(text('THE NOTEBOOK OF / SOLANKYYY',220,29,11,'#78617d',anchor='middle'))
            parts.append(script('Om Solanki',220,391,106,'#684b7b',390,True))
            parts.append(script('Curiosity, turned into',220,443,45,'#986552',370,True))
            parts.append(script('something useful.',220,489,45,'#986552',370,True))
            parts.append(text('AI/ML student · Bengaluru, India',220,534,17,anchor='middle'))
            parts.append(text('Applied AI · Computer vision · Web',220,565,16,anchor='middle'))
            parts.append('<rect x="104" y="599" width="232" height="37" rx="18" fill="#edf8ef" stroke="#c7e4d0"/><circle class="pulse" cx="124" cy="617" r="5" fill="#16a34a"/><circle cx="124" cy="617" r="5" fill="#16a34a"/>')
            parts.append(text('Open to collaboration',140,623,15,'#32684a'))
        else:
            parts.append(text('THE NOTEBOOK OF / SOLANKYYY',44,46,12,'#78617d'))
            parts.append(script('Om Solanki',40,200,126,'#684b7b',530))
            parts.append(script('Curiosity, turned into',44,270,57,'#986552',520))
            parts.append(script('something useful.',44,322,57,'#986552',520))
            parts.append(text('Applied AI · Computer vision · Web',44,375,19))
            parts.append(text('AI/ML student · Bengaluru, India',44,450,16))
            parts.append('<rect x="630" y="412" width="246" height="37" rx="18" fill="#edf8ef" stroke="#c7e4d0"/><circle class="pulse" cx="651" cy="430" r="5" fill="#16a34a"/><circle cx="651" cy="430" r="5" fill="#16a34a"/>')
            parts.append(text('Open to collaboration',667,436,16,'#32684a'))
        (OUT/('hero-mobile.svg' if mobile else 'hero.svg')).write_text(base(w,h,PALETTES[1],'Om Solanki — curiosity, turned into something useful',''.join(parts)),encoding='utf-8')

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
for i,raw in enumerate(raw_projects):
    raw=raw.split('<details>')[0].strip()
    lines=raw.split('\n',1)
    title=lines[0].split(' / ',1)[1]
    ps=paragraphs(lines[1])
    subtitle=ps.pop(0)
    blocks=[]
    links=re.findall(r'\]\((https://github.com/[^)]+)\)',raw)
    for p in ps:
        if p.startswith(('Source &','Explore the demo')):continue
        if p.startswith('Built with:'):
            blocks.append(('Tools & technologies',p[len('Built with:'):].strip()))
        else:blocks.append((None,p))
    panel(f'project-{i+1}',title,[(subtitle,'')]+blocks,i,'Selected work / '+f'{i+1:02}', 'Explore the project →')
    projects.append((title,links[0]))

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
panel('contributions','Little steps, lasting progress',[(None,'Small iterations add up. The moving contribution trail below follows my public work on GitHub.')],3,'07 / The contribution trail')
panel('connect','Good ideas begin with hello',[(None,p) for p in paragraphs(section("Let's connect")) if not p.startswith(('Email me','Open to collaboration'))],0,'08 / Let’s connect','Open to collaboration · Bengaluru, India')

for mobile in (False,True):
    w,h=(440,220) if mobile else (960,190)
    content=script('Keep learning. Keep building.',w/2,100,60 if mobile else 76,'#70548b',w-48,True)
    content+=f'<path class="ribbon" d="M-50 {h-45}Q{w/4} {h-100} {w/2} {h-45}T{w+50} {h-45}" fill="none" stroke="#b9dacb" stroke-width="3"/>'
    (OUT/('footer-mobile.svg' if mobile else 'footer.svg')).write_text(base(w,h,PALETTES[1],'Keep learning. Keep building.',content),encoding='utf-8')

contacts=[('portfolio','Portfolio ↗','https://solanki-portfolio-v4.vercel.app/'),('linkedin','LinkedIn','https://www.linkedin.com/in/solanki-om-b89793330/'),('email','Email me','mailto:om.n.solanki49@gmail.com'),('x','Find me on X','https://x.com/Om_solanki49')]
for i,(slug,label,_) in enumerate(contacts):
    (OUT/(slug+'.svg')).write_text(base(180,48,PALETTES[i],label,text(label,90,31,17,PALETTES[i][1],600,'middle')),encoding='utf-8')

def picture(name,alt,link=None):
    pic=f'<picture>\n  <source media="(max-width: 600px)" srcset="assets/pastel/{name}-mobile.svg">\n  <img src="assets/pastel/{name}.svg" width="100%" alt="{escape(alt,quote=True)}">\n</picture>'
    if link:pic=f'<a href="{link}">\n{pic}\n</a>'
    return pic+'\n\n'

def contact_row():
    return '<p align="center">\n'+'\n'.join(f'  <a href="{url}"><img src="assets/pastel/{slug}.svg" width="130" alt="{label}"></a>' for slug,label,url in contacts)+'\n</p>\n\n'

md=picture('hero','Om Solanki. AI/ML student in Bengaluru, India. Open to collaboration. Portrait with pastel animation and a green status dot.')
md+=contact_row()
md+='<p align="center"><a href="PROFILE.md">Read the complete profile in text</a></p>\n\n'
md+=picture('about','About Om: AI/ML student at Jain University, working across computer vision, language-model evaluation, security analytics, and web development.')
md+=picture('focus','Focus: applied machine learning, computer vision, and software interfaces.')
for i,(title,link) in enumerate(projects):
    md+=picture(f'project-{i+1}',f'{title} — project overview, approach, scope, and technologies. Open repository.',link)
    if i==0:md+='<p align="center"><a href="https://retina-bridge.vercel.app/">Explore the RetinaBridge demonstration ↗</a></p>\n\n'
md+='<details>\n<summary><strong>More experiments to explore</strong></summary>\n\n'
md+=section('Selected projects').split('<details>',1)[1].split('<br>',1)[1].split('</details>')[0].strip()+'\n\n</details>\n\n'
for name,alt in [('toolkit','Technical toolkit: languages, machine learning, vision, data, web, UI, databases, and local LLM experiments.'),('approach','Project approach: understand, experiment, build, and refine.'),('learning','Learning through building: notes about connecting experiments, interfaces, and software foundations.'),('exploring','Currently exploring model evaluation, computer vision, software foundations, and application development.'),('contributions','Little steps, lasting progress: my GitHub contribution trail.')]:
    md+=picture(name,alt)
md+='<p align="center"><img src="https://raw.githubusercontent.com/SOLANKYYY/SOLANKYYY/output/github-contribution-grid-snake-pastel.svg" width="100%" alt="Animated green GitHub contribution snake on a light pastel background."></p>\n\n'
md+='<p align="center"><a href="https://github.com/SOLANKYYY?tab=repositories">Browse all repositories ↗</a></p>\n\n'
md+=picture('connect','Open to collaboration on applied AI, computer vision, useful web tools, and open-source improvements.')+contact_row()+picture('footer','Keep learning. Keep building.')
(ROOT/'ReadMe.md').write_text(md.rstrip()+'\n',encoding='utf-8')
print(f'Built {len(list(OUT.glob("*.svg")))} pastel SVG assets and the visual README.')
