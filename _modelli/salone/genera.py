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
    open(os.path.join(ROOT,slug,'index.html'),'w').write(s); print('OK',slug)
