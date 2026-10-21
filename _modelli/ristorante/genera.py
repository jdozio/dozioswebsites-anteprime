# Genera un sito "ristorante / locanda" per ogni dati/*.json:  python3 genera.py [slug]
import json,os,glob,html,sys
B=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(os.path.dirname(B))
T=open(os.path.join(B,'template.html')).read()
BASE='https://jdozio.github.io/dozioswebsites-anteprime/'
only=sys.argv[1] if len(sys.argv)>1 else None
for f in sorted(glob.glob(os.path.join(B,'dati','*.json'))):
    slug=os.path.basename(f)[:-5]
    if only and slug!=only: continue
    D=json.load(open(f)); e=lambda s: html.escape(s,quote=True)
    og=f'''
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="Jacopo Dozio · siti web">
<meta property="og:title" content="{e(D['name'])} · anteprima del nuovo sito">
<meta property="og:description" content="{e(D['desc'])}">
<meta property="og:url" content="{BASE}{slug}/">
<meta property="og:image" content="{e(D['ogImage'])}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">'''
    s=T.replace('{{TITLE}}',e(D['name']+' · '+D['city'])).replace('{{DESC}}',e(D['desc']))
    md='<meta name="description" content="'+e(D['desc'])+'">'
    s=s.replace(md,md+og,1)
    for k,v in D['theme'].items(): s=s.replace('{{'+k.upper()+'}}',v)
    s=s.replace('{{DATA}}',json.dumps(D,ensure_ascii=False).replace('</','<\\/'))
    os.makedirs(os.path.join(ROOT,slug),exist_ok=True)
    open(os.path.join(ROOT,slug,'index.html'),'w').write(s); print('OK',slug)
