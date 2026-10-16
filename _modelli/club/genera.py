# Genera un sito "club" per ogni file dati/*.json:  python3 genera.py
import json,os,glob,html
B=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(os.path.dirname(B))
T=open(os.path.join(B,'template.html')).read()
BASE='https://jdozio.github.io/dozioswebsites-anteprime/'
for f in sorted(glob.glob(os.path.join(B,'dati','*.json'))):
    D=json.load(open(f)); slug=os.path.basename(f)[:-5]
    e=lambda s: html.escape(s,quote=True)
    title=f"{D['name']} · {D['city']}"; desc=D['desc']
    og=f'''
<!-- anteprima link (WhatsApp) -->
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="Jacopo Dozio · siti web">
<meta property="og:title" content="{e(D['name'])} · anteprima del nuovo sito">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{BASE}{slug}/">'''
    if D.get('ogImage'):
        og+=f'''
<meta property="og:image" content="{e(D['ogImage'])}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(D['name'])}">
<meta name="twitter:card" content="summary_large_image">'''
    og+='\n<!-- /anteprima link -->'
    s=T.replace('{{TITLE}}',e(title)).replace('{{DESC}}',e(desc))
    md='<meta name="description" content="'+e(desc)+'">'
    s=s.replace(md,md+og,1)
    s=s.replace('{{C1}}',D['c1']).replace('{{C2}}',D['c2']).replace('{{C3}}',D['c3'])
    s=s.replace('{{DATA}}',json.dumps(D,ensure_ascii=False).replace('</','<\\/'))
    os.makedirs(os.path.join(ROOT,slug),exist_ok=True)
    open(os.path.join(ROOT,slug,'index.html'),'w').write(s); print('OK',slug)
