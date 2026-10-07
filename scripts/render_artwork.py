#!/usr/bin/env python3
"""Draw the original profile artwork. Python standard library; no network."""
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parents[1] / "assets" / "profile"
PALETTES = {
    "dark": dict(bg="#08182e", fg="#edf5ff", muted="#a1b9db", line="#24466d", accent="#78b7ff", ice="#acdfff", blue="#6097ff", panel="#102b4d"),
    "light": dict(bg="#eff6ff", fg="#102c52", muted="#48658a", line="#c0d5f0", accent="#235bce", ice="#17679b", blue="#355edb", panel="#e0edff"),
}


def text(x, y, value, size, color, weight=400, mono=False, extra=""):
    font = "'SFMono-Regular',Consolas,monospace" if mono else "-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif"
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{font}" font-size="{size}" font-weight="{weight}" {extra}>{escape(value)}</text>'


def document(w, h, p, title, desc, contents):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<style>
@keyframes travel {{ to {{ stroke-dashoffset: -100; }} }}
@keyframes breathe {{ 0%,100% {{ opacity: .35; }} 50% {{ opacity: .85; }} }}
@keyframes voice {{ 0%,100% {{ transform: scaleY(.45); }} 50% {{ transform: scaleY(1); }} }}
@keyframes drift {{ 0%,100% {{ transform: translateX(0); }} 50% {{ transform: translateX(-24px); }} }}
@keyframes float {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-5px); }} }}
@keyframes draw {{ 0%,15% {{ stroke-dashoffset: 100; }} 65%,100% {{ stroke-dashoffset: 0; }} }}
.signal {{ stroke-dasharray: 13 87; animation: travel 5s linear infinite; }}
.beacon {{ animation: breathe 5s ease-in-out infinite; }}
.wavebar {{ transform-box: fill-box; transform-origin: center; animation: voice 3.2s ease-in-out infinite; }}
.drift {{ animation: drift 12s ease-in-out infinite; }}
.float {{ animation: float 7s ease-in-out infinite; }}
.trace {{ stroke-dasharray: 100; animation: draw 9s ease-in-out infinite; }}
@media (prefers-reduced-motion: reduce) {{
  .signal,.beacon,.wavebar,.drift,.float,.trace {{ animation: none; }}
  .signal {{ stroke-dasharray: none; opacity: .55; }}
  .trace {{ stroke-dasharray: none; }}
}}
</style>
<rect width="{w}" height="{h}" rx="18" fill="{p['bg']}"/>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="none" stroke="{p['line']}"/>
{''.join(contents)}
</svg>\n'''


def hero(p, mobile=False):
    w, h = (640, 700) if mobile else (1200, 430)
    x = 40 if mobile else 52
    c = [text(x, 48, "TK / ENGINEERING FIELDNOTES", 19 if mobile else 17, p['muted'], mono=True)]
    if not mobile:
        c.append(text(1148, 48, "IDEAS → WORKING SOFTWARE", 16, p['muted'], mono=True, extra='text-anchor="end"'))
    c += [text(x-4, 154, "Tejass", 100, p['fg'], 650, extra='letter-spacing="-5"'),
          text(x-4, 252, "Kaushik.", 100, p['fg'], 650, extra='letter-spacing="-5"'),
          text(x, 302, "From an idea to something you can use.", 23 if mobile else 25, p['muted'])]
    # Restore the user's preferred one-input / three-surfaces diagram.
    ox, oy, scale = (65, 350, 1.15) if mobile else (725, 89, 1)
    c.append(f'<g transform="translate({ox} {oy}) scale({scale})">')
    paths = ["M20 100H80Q100 100 100 80V25Q100 10 120 10H190", "M20 100H190", "M20 100H80Q100 100 100 120V175Q100 190 120 190H190"]
    for i, path in enumerate(paths):
        c += [f'<path d="{path}" fill="none" stroke="{p["line"]}" stroke-width="2"/>',
              f'<path class="signal" pathLength="100" d="{path}" fill="none" stroke="{p["accent"]}" stroke-width="3" style="animation-delay:{-i*1.6}s"/>']
    c += [f'<circle class="beacon" cx="20" cy="100" r="24" fill="{p["accent"]}" opacity=".15"/>',
          f'<circle cx="20" cy="100" r="10" fill="{p["ice"]}"/>',
          f'<circle cx="20" cy="100" r="24" fill="none" stroke="{p["line"]}"/>']
    for i, (y, label, color) in enumerate([(10,"INTERFACES",p['accent']), (100,"INTELLIGENCE",p['blue']), (190,"SYSTEMS",p['ice'])]):
        c += [f'<rect x="190" y="{y-31}" width="220" height="62" rx="10" fill="{p["panel"]}" stroke="{p["line"]}"/>',
              f'<rect class="beacon" x="190" y="{y-31}" width="3" height="62" rx="1.5" fill="{color}" style="animation-delay:{-i*1.6}s"/>',
              text(207,y+6,f"0{i+1}",17,color,mono=True), text(248,y+6,label,17,p['fg'],mono=True)]
    c.append('</g>')
    baseline = h-70
    c += [f'<path d="M{x} {baseline}H{w-x}" stroke="{p["line"]}"/>',
          text(x,baseline+37,"WEB / MOBILE / AI",18 if mobile else 16,p['accent'],mono=True),
          text(w-x,baseline+37,"@tejask-dev",18 if mobile else 16,p['muted'],mono=True,extra='text-anchor="end"')]
    return document(w,h,p,"Tejass Kaushik — engineering fieldnotes", "From an idea to something you can use. Animated blue signals connect interfaces, intelligence, and systems. Web, mobile, and AI engineering.",c)


def anticipy(p, mobile=False):
    w,h = (640,540) if mobile else (1200,310)
    x = 36 if mobile else 48
    c = [text(x,44,"BUILDING / ANTICIPATION LABS",18 if mobile else 16,p['muted'],mono=True),
         text(x-3,126,"Anticipy.",76,p['fg'],650,extra='letter-spacing="-3"'),
         text(x,174,"Spoken intentions. Useful actions.",26,p['accent'],500),
         text(x,211,"An AI wearable, with your approval.",23,p['muted'])]
    ox,oy = (118,263) if mobile else (776,42)
    c.append(f'<g transform="translate({ox} {oy})">')
    c.append(f'<circle class="beacon" cx="164" cy="100" r="87" fill="none" stroke="{p["line"]}"/>')
    for i,height in enumerate((22,44,68,40,88,58,30)):
        c.append(f'<rect class="wavebar" x="{i*12}" y="{100-height/2}" width="4" height="{height}" rx="2" fill="{p["accent"]}" style="animation-delay:{-i*.36}s"/>')
    c += [f'<path d="M90 100H117M210 100H267" stroke="{p["line"]}" fill="none"/>',
          f'<path class="signal" pathLength="100" d="M90 100H117M210 100H267" stroke="{p["accent"]}" stroke-width="3" fill="none"/>',
          f'<rect x="118" y="29" width="92" height="142" rx="35" fill="{p["panel"]}" stroke="{p["accent"]}" stroke-width="2"/>',
          f'<circle cx="164" cy="62" r="8" fill="none" stroke="{p["line"]}" stroke-width="2"/>',
          f'<circle class="beacon" cx="164" cy="103" r="15" fill="{p["blue"]}"/>',
          f'<circle cx="164" cy="103" r="5" fill="{p["ice"]}"/>',
          f'<circle cx="291" cy="100" r="24" fill="{p["panel"]}" stroke="{p["line"]}"/>',
          f'<path d="M281 100L288 107L302 91" stroke="{p["ice"]}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
          text(164,216,"VOICE → INTENT → APPROVAL",14,p['muted'],mono=True,extra='text-anchor="middle"'), '</g>',
          text(x,h-30,"EXPLORE ANTICIPY ↗",19 if mobile else 17,p['accent'],600,mono=True)]
    return document(w,h,p,"Anticipy — building at Anticipation Labs", "Spoken intentions, useful actions. An AI wearable being built with the person's approval. Follow this card to explore Anticipy.",c)


def open_water(p, mobile=False):
    w,h = (640,560) if mobile else (1200,310)
    x = 36 if mobile else 48
    c = [text(x,44,"EXPLORE / MY PERSONAL PORTFOLIO",17 if mobile else 16,p['muted'],mono=True),
         text(x-3,125,"Open Water.",70,p['fg'],650,extra='letter-spacing="-3"'),
         text(x,174,"Engineering, research,",25,p['accent'],500),
         text(x,210,"and an ocean to explore.",25,p['muted'])]
    ox,oy = (38,260) if mobile else (690,46)
    c.append(f'<g transform="translate({ox} {oy})">')
    c += [f'<circle cx="382" cy="37" r="25" fill="{p["panel"]}"/>',
          f'<path d="M8 65H480" stroke="{p["line"]}" stroke-dasharray="2 8"/>',
          '<g class="float">',
          f'<path d="M98 131H354L328 160H130Z" fill="{p["accent"]}"/>',
          f'<path d="M154 101H286L313 126H132Z" fill="{p["fg"]}"/>',
          f'<path d="M177 82H248L270 98H164Z" fill="{p["ice"]}"/>',
          f'<path d="M196 80V58H231" fill="none" stroke="{p["ice"]}" stroke-width="3"/>',
          f'<path d="M177 108H207M216 108H245M254 108H278" stroke="{p["bg"]}" stroke-width="6"/>',
          '</g>']
    for i in range(3):
        y = 165+i*24
        c.append(f'<path class="drift" d="M0 {y}Q30 {y-14} 60 {y}T120 {y}T180 {y}T240 {y}T300 {y}T360 {y}T420 {y}T480 {y}T540 {y}" fill="none" stroke="{p["accent"] if i==0 else p["line"]}" stroke-width="{2 if i==0 else 1}" style="animation-duration:{10+i*3}s;animation-delay:{-i*3}s"/>')
    c += ['</g>',text(x,h-30,"STEP INSIDE OPEN WATER ↗",19 if mobile else 17,p['accent'],600,mono=True)]
    return document(w,h,p,"Open Water — Tejass Kaushik's personal portfolio", "Engineering, research, and an ocean to explore. A gently moving yacht and blue waves invite you into the interactive portfolio. Reading pages are also available.",c)


def icon(kind, p, accent):
    c = []
    if kind == "acs":
        for x,h in [(2,35),(28,63),(54,89),(80,110)]:
            c.append(f'<rect x="{x}" y="{115-h}" width="17" height="{h}" rx="3" fill="{accent}" opacity="{.4+x/150}"/>')
        c.append(f'<path d="M0 124H110" stroke="{p["line"]}" stroke-width="2"/>')
    elif kind == "molecule":
        pts=[(52,7),(98,33),(98,85),(52,111),(6,85),(6,33)]
        c.append(f'<polygon points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="none" stroke="{accent}" stroke-width="3"/>')
        c.append(f'<path d="M18 40V77M54 96L85 78M54 21L85 40" fill="none" stroke="{accent}" stroke-width="2"/>')
        for x,y in pts:
            c.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{p["bg"]}" stroke="{accent}" stroke-width="2"/>')
    elif kind == "modelmind":
        c.append(f'<rect x="0" y="15" width="110" height="92" rx="7" fill="none" stroke="{accent}" stroke-width="2"/>')
        for x in [28,56,84]:
            c.append(f'<path d="M{x} 15V107" stroke="{p["line"]}"/>')
        for y in [38,61,84]:
            c.append(f'<path d="M0 {y}H110" stroke="{p["line"]}"/>')
        c.append(f'<path class="trace" pathLength="100" d="M13 92L40 68L68 80L99 43" fill="none" stroke="{accent}" stroke-width="4"/>')
    else:
        for y1,y2 in [(15,15),(15,57),(57,15),(57,100),(100,57),(100,100)]:
            c.append(f'<path d="M13 {y1}C50 {y1} 60 {y2} 98 {y2}" fill="none" stroke="{p["line"]}" stroke-width="2"/>')
        c.append(f'<path d="M13 57C50 57 60 100 98 100" fill="none" stroke="{accent}" stroke-width="3"/>')
        for x in [13,98]:
            for y in [15,57,100]:
                c.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{p["bg"]}" stroke="{accent}" stroke-width="2"/>')
    return ''.join(c)


def atlas(p,mobile=False):
    w,h=(640,670) if mobile else (1200,335)
    c=[text(32,40,"SELECTED BUILDS / EXPLORE THE STORIES BELOW",16 if mobile else 18,p['muted'],mono=True)]
    entries=[("acs","01","ACS Can Drive","Community logistics",p['accent']), ("molecule","02","MoleculeAI","Chemistry, made visual",p['blue']), ("modelmind","03","ModelMind","Questions → analysis",p['ice']), ("prommatch","04","PromMatch","Preferences → matches",p['accent'])]
    for i,(kind,num,name,label,accent) in enumerate(entries):
        x,y=(32+(i%2)*308,90+(i//2)*290) if mobile else (32+i*296,80)
        c += [text(x,y+4,num,17,p['muted'],mono=True),f'<g transform="translate({x+68} {y})">{icon(kind,p,accent)}</g>',
              text(x,y+175,name,30 if mobile else 28,p['fg'],600),text(x,y+207,label,18,p['muted'])]
        if (i%2==0 if mobile else i<3):
            sx=x+280
            c.append(f'<path d="M{sx} {y}V{y+216}" stroke="{p["line"]}"/>')
    return document(w,h,p,"Four selected builds", "ACS Can Drive: community logistics. MoleculeAI: visual chemistry. ModelMind: spreadsheet analysis. PromMatch: compatibility matching.",c)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for theme,palette in PALETTES.items():
        for mobile in (False,True):
            suffix=f'{theme}{"-mobile" if mobile else ""}.svg'
            for name,render in (("hero",hero),("project-atlas",atlas),("anticipy",anticipy),("open-water",open_water)):
                svg = render(palette,mobile)
                (OUT/f'{name}-{suffix}').write_text(svg,encoding='utf-8')
                (OUT/f'{name}-still-{suffix}').write_text(still(svg),encoding='utf-8')
    print('Generated 16 animated illustrations and 16 still alternatives.')


def still(svg):
    """Freeze artwork for host-page picture selection, including SVG image contexts."""
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    root = ET.fromstring(svg)
    root.find('{http://www.w3.org/2000/svg}style').text = '.signal {opacity:.55} .beacon {opacity:.4}'
    for element in root.iter():
        # Animation delays/durations without a name are inert, but omit them entirely.
        if 'animation-' in element.get('style', ''):
            del element.attrib['style']
    return ET.tostring(root,encoding='unicode') + '\n'


if __name__ == '__main__':
    main()
