import json, os, re, sys
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"out2"); sys.path.insert(0,HERE)
from site2 import NAMES
comp=json.load(open(os.path.join(OUT,"comp3.json")))
def shrink(n):
    if isinstance(n,list):
        if n[0]=="s" and "0 0 160 160" in n[5] and len(n[5])>2500: n[5]="#QR274"
        return
    for k in n.get("k",[]): shrink(k)
for v in comp.values(): shrink(v)
f2=open(os.path.join(HERE,"fig2.py")).read()
B=f2[f2.index('BUILDER = r"""')+len('BUILDER = r"""'):]
B=B[:B.index('"""')]
TOK=json.dumps({"f7eee2":"bg","fffaf3":"surface","142a1f":"ink","5d6b60":"soft","e8dccb":"line","23402c":"brand","0e2319":"deep","ffffff":"onbrand","f3dcc6":"tint","dfe4d2":"tint2","fa7f52":"accent","eec39e":"photo"})
B=B.replace("__TOK__",TOK).replace("'Бренд · Пульс'","'Палітра 1 · зелена'")
B=B.replace("function QR(seed){let s=seed;const rnd=()=>{s=(s*16807)%2147483647;return s/2147483647};const n=21,c=170/n;let o=\"<svg viewBox='0 0 170 170'><rect width='170' height='170' fill='#fff'/>\"","function QR(seed){let s=seed;const rnd=()=>{s=(s*16807)%2147483647;return s/2147483647};const n=21,c=170/n;let o=\"<svg viewBox='0 0 170 170'><rect width='170' height='170' fill='#fefefe'/>\"")
B=B.replace("fill='#fff'/>\";return o+fd","fill='#fefefe'/>\";return o+fd")
# hero tiles + go names with 3 digits
B=B.replace("function I(a,par){const [_,x,y,w,h,key,fit,rad,ex]=a;const e=ex||{};",
 "function I(a,par){const [_,x,y,w,h,key,fit,rad,ex]=a;const e=ex||{};if(key==='s_hero'){const fr=figma.createFrame();par.appendChild(fr);fr.name=\"фото: інтер'єр\";fr.x=x;fr.y=y;fr.resize(w,h);fr.cornerRadius=rad;fr.clipsContent=true;fr.fills=[P('@photo')];const tw=w/3;for(let i=0;i<3;i++){const t=figma.createRectangle();fr.appendChild(t);const k='s_hero_'+(i+1);t.name='фото: '+k;t.x=Math.round(i*tw);t.y=0;t.resize(Math.round((i+1)*tw)-Math.round(i*tw)+(i<2?1:0),h);t.fills=IMGS[k]?[{type:'IMAGE',imageHash:IMGS[k],scaleMode:'FILL'}]:[P('@photo')];}return;}")
B=B.replace("f.name=o.g?o.n+' → '+String(o.g).padStart(2,'0'):(o.cl?'вставка екрана '+o.cl:o.n);","f.name=o.g?o.n+' → '+o.g:o.n;")
B=B.replace("n.name=src.length>3000?'code':'icon';bindTree(n);","if(src.length>3000){const g=figma.flatten([n]);g.name='код';}else{n.name='icon';bindTree(n);}")
groups=[[101,102,103],[104,105,106,108],[107,109]]
for gi,g in enumerate(groups):
    D={n:comp["web%d"%n] for n in g}
    code=("const D="+json.dumps(D,ensure_ascii=False,separators=(",",":"))+";\nconst N="+json.dumps({n:NAMES[n] for n in g},ensure_ascii=False)+";\n"+B+
      "\nconst page=figma.root.children.find(p=>p.name==='Сайт');await figma.setCurrentPageAsync(page);for(const o of page.children.filter(c=>c.name.startsWith('Сайт ·')))o.remove();const made={};\n"
      "for(const i in D){const nm=N[i];for(const old of page.children.filter(c=>c.name===nm))old.remove();const f=B(D[i],page);f.name=nm;f.x=(+i-101)*1560;f.y=0;made[nm]=f.id;}\n"
      "return {made,err:err.slice(0,6),nerr:err.length};")
    open(os.path.join(OUT,"fw%d.js"%gi),"w").write(code); print(gi,len(code))
