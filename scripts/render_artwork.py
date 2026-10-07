#!/usr/bin/env python3
"""Draw the original profile artwork. Python standard library; no network."""
from html import escape
from pathlib import Path

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
@keyframes travel {{ to {{ stroke-dashoffset: -800; }} }}
.signal {{ stroke-dasharray: 20 780; animation: travel 18s linear infinite; }}
@media (prefers-reduced-motion: reduce) {{ .signal {{ animation: none; stroke-dasharray: none; opacity: .35; }} }}
</style>
<rect width="{w}" height="{h}" rx="18" fill="{p['bg']}"/>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="none" stroke="{p['line']}"/>
{''.join(contents)}
</svg>\n'''


def hero(p, mobile=False):
    w, h = (640, 540) if mobile else (1200, 440)
    x = 38 if mobile else 52
    c = [text(x, 48, "TK / SOFTWARE ENGINEER", 19 if mobile else 17, p['muted'], mono=True)]
    # A nautical chart motif ties the profile to Open Water without external assets.
    cx, cy = (526, 325) if mobile else (949, 207)
    c.append(f'<g opacity="{.32 if mobile else 1}">')
    for radius in (52, 79, 107, 135):
        c.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{p["line"]}"/>')
    for offset in (-112, -56, 0, 56, 112):
        c.append(f'<path d="M{cx-164} {cy+offset}H{min(w-20,cx+164)}" stroke="{p["line"]}" stroke-dasharray="2 8"/>')
    route = f'M{cx-190} {cy+74}C{cx-92} {cy+74} {cx-98} {cy-100} {cx-8} {cy-87}S{cx+113} {cy-27} {cx+145} {cy-90}'
    c += [f'<path d="{route}" fill="none" stroke="{p["blue"]}" stroke-width="2"/>',
          f'<path class="signal" d="{route}" fill="none" stroke="{p["ice"]}" stroke-width="4"/>']
    for dx, dy in ((-129, 40), (-8, -87), (123, -59)):
        c.append(f'<circle cx="{cx+dx}" cy="{cy+dy}" r="5" fill="{p["accent"]}"/>')
    c.append('</g>')
    if not mobile:
        c += [text(803, 67, "A LITTLE CURIOSITY.", 15, p['muted'], mono=True),
              text(803, 359, "A LOT TO BUILD.", 15, p['muted'], mono=True),
              text(cx, cy+10, "TK", 50, p['accent'], 600, extra='text-anchor="middle" letter-spacing="-3"')]
    # Text gets its own quiet surface on the narrow layout.
    if mobile:
        c.append(f'<rect x="20" y="77" width="490" height="301" rx="12" fill="{p["bg"]}"/>')
    c += [text(x-4, 155, "Tejass", 100, p['fg'], 650, extra='letter-spacing="-5"'),
          text(x-4, 253, "Kaushik.", 100, p['fg'], 650, extra='letter-spacing="-5"'),
          text(x, 308, "I build AI products", 28, p['accent'], 500),
          text(x, 344, "across apps and devices.", 28, p['muted'])]
    baseline = h-64
    c += [f'<path d="M{x} {baseline}H{w-x}" stroke="{p["line"]}"/>',
          text(x,baseline+37,"WEB / MOBILE / AI",18 if mobile else 16,p['accent'],mono=True),
          text(w-x,baseline+37,"@tejask-dev",18 if mobile else 16,p['muted'],mono=True,extra='text-anchor="end"')]
    return document(w,h,p,"Tejass Kaushik — software engineer", "I build AI products across apps and devices. An original blue nautical chart connects curiosity with engineering, inspired by Open Water.",c)


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
            for name,render in (("hero",hero),("project-atlas",atlas)):
                (OUT/f'{name}-{suffix}').write_text(render(palette,mobile),encoding='utf-8')
    print('Generated 8 original, responsive profile illustrations.')


if __name__ == '__main__':
    main()
