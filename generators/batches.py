import json, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
NAMES = {1: "01 Вибір картки", 2: "02 Головна", 3: "03 Меню кухні", 4: "04 Страва", 5: "05 Продукти", 6: "06 Кошик",
         7: "07 Отримання", 8: "08 Оплата", 9: "09 Статус замовлення", 10: "10 Готово у віконці", 11: "11 Комірка-холодильник",
         12: "12 Кур'єр", 13: "13 Картка лояльності", 14: "14 Профіль"}
BUILDER = r"""const F={L400:['Lora','Regular'],L500:['Lora','Medium'],L600:['Lora','SemiBold'],L700:['Lora','Bold'],N400:['Nunito Sans','Regular'],N500:['Nunito Sans','Medium'],N600:['Nunito Sans','SemiBold'],N700:['Nunito Sans','Bold'],N800:['Nunito Sans','ExtraBold'],N900:['Nunito Sans','ExtraBold']};
for(const k in F){try{await figma.loadFontAsync({family:F[k][0],style:F[k][1]})}catch(e){F[k]=['Nunito Sans','Regular']}}
await figma.loadFontAsync({family:'Nunito Sans',style:'Regular'});
const P=h=>{const c={r:parseInt(h.slice(0,2),16)/255,g:parseInt(h.slice(2,4),16)/255,b:parseInt(h.slice(4,6),16)/255};return {type:'SOLID',color:c,opacity:h.length>6?parseInt(h.slice(6,8),16)/255:1}};
const err=[];
function T(a,par){const [_,x,y,w,h,s,fk,fs,lh,col,lines,ex]=a;const e=ex||{};const t=figma.createText();par.appendChild(t);const fn=F[fk]||F.N400;t.fontName={family:fn[0],style:fn[1]};t.characters=s;t.fontSize=fs;t.lineHeight={value:lh,unit:'PIXELS'};t.fills=[P(col)];if(e.ls)t.letterSpacing={value:e.ls,unit:'PIXELS'};if(e.st)t.textDecoration='STRIKETHROUGH';
if(lines>1){t.resize(w+3,lh*lines);t.textAutoResize='HEIGHT';if(e.ta)t.textAlignHorizontal=e.ta==='c'?'CENTER':'RIGHT';t.x=x;}else{t.textAutoResize='WIDTH_AND_HEIGHT';t.x=Math.round(e.ta==='r'?x+w-t.width:e.ta==='c'?x+(w-t.width)/2:x);}
t.y=Math.round(y+h/2-t.height/2);t.name=s.slice(0,40);}
function S(a,par){try{const src=a[5][0]==='#'?V[+a[5].slice(1)]:a[5];const n=figma.createNodeFromSvg(src.replace('<svg','<svg xmlns="http://www.w3.org/2000/svg"'));par.appendChild(n);n.x=a[1];n.y=a[2];if(a[3]>0&&a[4]>0)n.resize(a[3],a[4]);n.name='graphic';}catch(e){err.push(String(e).slice(0,80))}}
function B(o,par){const f=figma.createFrame();par.appendChild(f);f.name=o.g?o.n+' → '+String(o.g).padStart(2,'0'):o.n;f.x=o.b[0];f.y=o.b[1];f.resize(Math.max(1,o.b[2]),Math.max(1,o.b[3]));f.fills=o.f?[P(o.f)]:[];
if(o.s){f.strokes=[P(o.s[0])];f.strokeWeight=o.s[1];f.strokeAlign='INSIDE';if(o.s[2])f.dashPattern=[5,4];}
if(o.r!=null){if(Array.isArray(o.r)){f.topLeftRadius=o.r[0];f.topRightRadius=o.r[1];f.bottomRightRadius=o.r[2];f.bottomLeftRadius=o.r[3];}else f.cornerRadius=o.r;}
f.clipsContent=!!o.c;if(o.o!=null)f.opacity=o.o;for(const k of o.k||[]){if(Array.isArray(k)){k[0]==='t'?T(k,f):S(k,f)}else B(k,f)}return f;}
const page=figma.currentPage;const made={};
for(const i in D){const nm=N[i];for(const old of page.children.filter(c=>c.name===nm))old.remove();const f=B(D[i],page);f.name=nm;const j=+i-1;f.x=(j%7)*470;f.y=Math.floor(j/7)*1000;f.cornerRadius=0;made[nm]=f.id;}
return {made,err:err.slice(0,5),nerr:err.length};"""

GROUPS = [[1, 4, 6, 8, 9, 12], [2, 5], [3, 14], [10, 11], [7, 13], [2, 5, 3, 14]]
for gi, g in enumerate(GROUPS):
    D = {i: json.loads(open(os.path.join(OUT, "c%02d.json" % i)).read()) for i in g}
    from collections import Counter
    cnt = Counter()
    def walk(n, f):
        if isinstance(n, list):
            if n[0] == "s": f(n)
            return
        for k in n.get("k", []): walk(k, f)
    for d in D.values(): walk(d, lambda n: cnt.update([n[5]]))
    lib = [s for s, c in cnt.items() if c > 1 and len(s) > 120]
    idx = {s: i for i, s in enumerate(lib)}
    def rep(n):
        if n[5] in idx: n[5] = "#%d" % idx[n[5]]
    for d in D.values(): walk(d, rep)
    ds = json.dumps(D, ensure_ascii=False, separators=(",", ":"))
    ds += ";\nconst V=" + json.dumps(lib, ensure_ascii=False, separators=(",", ":"))
    ns = json.dumps({i: NAMES[i] for i in g}, ensure_ascii=False, separators=(",", ":"))
    code = "const D=" + ds + ";\nconst N=" + ns + ";\n" + BUILDER
    open(os.path.join(OUT, "batch%d.js" % gi), "w").write(code)
    print(gi, len(code))
