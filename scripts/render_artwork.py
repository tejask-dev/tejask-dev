#!/usr/bin/env python3
"""Draw the original profile artwork. Python standard library; no network."""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets" / "profile"
PALETTES = {
    "dark": dict(bg="#101719", fg="#f5f2eb", muted="#a7b6b0", line="#30423f", mint="#a8e5cd", orange="#f6b08a", blue="#a5bff5", panel="#182426"),
    "light": dict(bg="#f5f2eb", fg="#172827", muted="#526660", line="#cad5cc", mint="#146953", orange="#a14c24", blue="#355da8", panel="#e9eee7"),
}


def text(x, y, value, size, color, weight=400, mono=False, extra=""):
    font = "'SFMono-Regular',Consolas,monospace" if mono else "-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif"
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{font}" font-size="{size}" font-weight="{weight}" {extra}>{escape(value)}</text>'


def document(w, h, p, title, desc, contents):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<style>
@keyframes travel {{ to {{ stroke-dashoffset: -800; }} }}
.signal {{ stroke-dasharray: 14 786; animation: travel 12s linear infinite; }}
@media (prefers-reduced-motion: reduce) {{ .signal {{ animation: none; stroke-dasharray: none; opacity: .35; }} }}
</style>
<rect width="{w}" height="{h}" rx="18" fill="{p['bg']}"/>
{''.join(contents)}
</svg>\n'''


def hero(p, mobile=False):
    w, h = (640, 610) if mobile else (1200, 430)
    c = [text(40 if mobile else 52, 48, "TK / ENGINEERING FIELDNOTES", 17, p['muted'], mono=True)]
    if not mobile:
        c.append(text(1148, 48, "IDEAS → WORKING SOFTWARE", 16, p['muted'], mono=True, extra='text-anchor="end"'))
    x = 38 if mobile else 48
    c += [text(x, 154, "Tejas", 100, p['fg'], 650, extra='letter-spacing="-5"'),
          text(x, 252, "Kaushik.", 100, p['fg'], 650, extra='letter-spacing="-5"'),
          text(x+4, 302, "From an idea to something you can use.", 23 if mobile else 25, p['muted'])]
    ox, oy, scale = (100, 338, .78) if mobile else (725, 89, 1)
    c.append(f'<g transform="translate({ox} {oy}) scale({scale})">')
    # An original routed-system illustration: one input, three product surfaces.
    paths = ["M20 100H80Q100 100 100 80V25Q100 10 120 10H190", "M20 100H190", "M20 100H80Q100 100 100 120V175Q100 190 120 190H190"]
    for path in paths:
        c += [f'<path d="{path}" fill="none" stroke="{p["line"]}" stroke-width="2"/>',
              f'<path class="signal" d="{path}" fill="none" stroke="{p["mint"]}" stroke-width="3"/>']
    c += [f'<circle cx="20" cy="100" r="10" fill="{p["mint"]}"/>',
          f'<circle cx="20" cy="100" r="22" fill="none" stroke="{p["line"]}"/>']
    for y, title, label, color in [(10,"01", "INTERFACES", p['mint']), (100,"02", "INTELLIGENCE", p['blue']), (190,"03", "SYSTEMS", p['orange'])]:
        c += [f'<rect x="190" y="{y-31}" width="220" height="62" rx="9" fill="{p["panel"]}" stroke="{p["line"]}"/>',
              text(207,y+6,title,17,color,mono=True),text(248,y+6,label,17,p['fg'],mono=True)]
    c.append('</g>')
    baseline = h-58
    c += [f'<path d="M40 {baseline-20}H{w-40}" stroke="{p["line"]}"/>',
          text(42,baseline+18,"WEB / MOBILE / AI",17,p['mint'],mono=True),
          text(w-42,baseline+18,"@tejask-dev",17,p['muted'],mono=True,extra='text-anchor="end"')]
    return document(w,h,p,"Tejas Kaushik — engineering fieldnotes", "From an idea to something you can use. Web, mobile, and AI engineering. A moving signal connects interfaces, intelligence, and systems.",c)


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
        c.append(f'<path d="M13 92L40 68L68 80L99 43" fill="none" stroke="{accent}" stroke-width="4"/>')
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
    c=[text(32,40,"SELECTED BUILDS / OPEN THE FIELDNOTES BELOW",16 if mobile else 18,p['muted'],mono=True)]
    entries=[("acs","01","ACS Can Drive","Community logistics",p['mint']), ("molecule","02","MoleculeAI","Chemistry, made visual",p['blue']), ("modelmind","03","ModelMind","Questions → analysis",p['orange']), ("prommatch","04","PromMatch","Preferences → matches",p['mint'])]
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
            for name,render in (("hero",hero),("project-atlas",atlas)):
                (OUT/f'{name}-{suffix}').write_text(render(palette,mobile),encoding='utf-8')
    print('Generated 8 original, responsive profile illustrations.')


if __name__ == '__main__':
    main()
