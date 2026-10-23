# Genera un sito "salone" (barbiere / parrucchiere / estetica) per ogni dati/*.json:  python3 genera.py [slug]
import json,os,glob,html,sys
B=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(os.path.dirname(B))
T=open(os.path.join(B,'template.html')).read()
BASE='https://jdozio.github.io/dozioswebsites-anteprime/'
FONTS={
 'classico':("https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Manrope:wght@400;500;600;700;800&display=swap","'DM Serif Display',serif","'Manrope',system-ui,sans-serif"),
 'morbido':("https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500&family=Jost:wght@400;500;600;700&display=swap","'Fraunces',serif","'Jost',system-ui,sans-serif"),
 'elegante':("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Nunito+Sans:opsz,wght@6..12,400;6..12,600;6..12,700;6..12,800&display=swap","'Cormorant Garamond',serif","'Nunito Sans',system-ui,sans-serif"),
}

# --- segnaposto foto (23.10): ogni img "foto/<nome>.svg" con nota "foto" viene generata qui, finché Jacopo non mette la foto vera
import textwrap
def segnaposto(path,nota,w,h,t):
    k=2.0 if h/w>1.6 else 1.6
    fl,fn=round(15*k),round(17*k)
    lines=textwrap.wrap(nota.split(': ',1)[-1],max(10,int(w/(fn*0.55))))[:4]
    cy=h/2-(len(lines)*fn*1.3)/2; ty=cy+30*k
    txt=''.join(f'<text x="{w/2}" y="{ty+fn*1.45+i*fn*1.3:.0f}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="{fn}" fill="{t["ink2"]}">{html.escape(l)}</text>' for i,l in enumerate(lines))
    svg=f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg3']}"/><stop offset="1" stop-color="{t['acc2']}"/></linearGradient>
<pattern id="p" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="14" stroke="{t['ink']}" stroke-opacity=".05" stroke-width="2"/></pattern></defs>
<rect width="{w}" height="{h}" fill="url(#g)"/><rect width="{w}" height="{h}" fill="url(#p)"/>
<rect x="14" y="14" width="{w-28}" height="{h-28}" fill="none" stroke="{t['acc']}" stroke-opacity=".35" stroke-dasharray="6 6" rx="10"/>
<g transform="translate({w/2-26*k:.0f} {cy-40*k:.0f}) scale({k})" fill="none" stroke="{t['acc']}" stroke-width="2.2" stroke-linejoin="round"><rect x="0" y="10" width="52" height="38" rx="7"/><path d="M16 10 l5 -8 h10 l5 8"/><circle cx="26" cy="29" r="10"/></g>
<text x="{w/2}" y="{ty:.0f}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="{fl}" font-weight="700" letter-spacing="{2*k:.0f}" fill="{t['acc']}">FOTO DA INSERIRE</text>{txt}
</svg>"""
    os.makedirs(os.path.dirname(path),exist_ok=True); open(path,'w').write(svg)
def ratio(hs,base=400):
    a,b=[float(x) for x in hs.split('/')]; return base,int(base*b/a)
def segnaposti(D,slug):
    t=D['theme']; d=os.path.join(ROOT,slug)
    def go(x,w,h):
        if x.get('img','').startswith('foto/') and x['img'].endswith('.svg'): segnaposto(os.path.join(d,x['img']),x.get('foto',''),w,h,t)
    for x in D['hero']['imgs']: go(x,*( (400,840) if D['hero'].get('trio') else (400,500)))
    for g in D['gallery']: go(g,*ratio(g.get('h','4/5')))
    go(D['why'],400,470)
only=sys.argv[1] if len(sys.argv)>1 else None
for f in sorted(glob.glob(os.path.join(B,'dati','*.json'))):
    slug=os.path.basename(f)[:-5]
    if only and slug!=only: continue
    D=json.load(open(f)); e=lambda s: html.escape(s,quote=True)
    t=D['theme']; fu,fd,fb=FONTS[D.get('fonts','classico')]
    og=f'''
<!-- anteprima link (WhatsApp) -->
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="Jacopo Dozio · siti web">
<meta property="og:title" content="{e(D['name'])} · anteprima del nuovo sito">
<meta property="og:description" content="{e(D['desc'])}">
<meta property="og:url" content="{BASE}{slug}/">
<meta property="og:image" content="{e(D['ogImage'])}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(D['name'])}">
<meta name="twitter:card" content="summary_large_image">
<!-- /anteprima link -->'''
    s=T.replace('{{TITLE}}',e(D['name']+' · '+D['city'])).replace('{{DESC}}',e(D['desc']))
    md='<meta name="description" content="'+e(D['desc'])+'">'
    s=s.replace(md,md+og,1).replace('{{FONTS}}',fu).replace('{{FD}}',fd).replace('{{FB}}',fb)
    for k in ['BG','BG2','BG3','INK','INK2','ACC','ACC2','ON','LINE']: s=s.replace('{{'+k+'}}',t[k.lower()])
    s=s.replace('{{BODY}}',D['kind']+(' dark' if t.get('dark') else ''))
    s=s.replace('{{DATA}}',json.dumps(D,ensure_ascii=False).replace('</','<\\/'))
    os.makedirs(os.path.join(ROOT,slug),exist_ok=True)
    open(os.path.join(ROOT,slug,'index.html'),'w').write(s); segnaposti(D,slug); print('OK',slug)
