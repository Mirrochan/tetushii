"""Генерує JS для use_figma: батчі екранів і сайту."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out2")
sys.path.insert(0, HERE)
from p2 import THEMES, TOKENS, SCREENS

comp = json.load(open(os.path.join(OUT, "comp.json")))

# replace QR and barcode svgs with generators
def shrink(n, ctx):
    if isinstance(n, list):
        if n[0] == "s" and len(n[5]) > 2500:
            s = n[5]
            if "0 0 170 170" in s:
                n[5] = "#QR" + ctx
            else:
                bars = re.findall(r"<rect x='(\d+)' y='0' width='(\d+)'", s)
                n[5] = "#BC" + ",".join("%s:%s" % b for b in bars)
        return
    for k in n.get("k", []):
        shrink(k, ctx)

shrink(comp["app10"], "274"); shrink(comp["app11"], "1414"); shrink(comp["app13"], "")

PULSE = {THEMES["pulse"][k].lower().lstrip("#"): k for k in TOKENS}

BUILDER = r"""
const W={400:'Regular',500:'Medium',600:'SemiBold',700:'Bold',800:'ExtraBold'};
for(const s of Object.values(W))await figma.loadFontAsync({family:'Onest',style:s});
const coll=(await figma.variables.getLocalVariableCollectionsAsync()).find(c=>c.name==='Бренд · Пульс');
const VARS={};for(const v of await figma.variables.getLocalVariablesAsync()){if(v.variableCollectionId===coll.id)VARS[v.name]=v;}
const TOK=__TOK__;
const RES=figma.root.children.find(p=>p.name==='Фото та джерела');await RES.loadAsync();const IMGS={};for(const n of RES.children){if(n.name.startsWith('img:')&&Array.isArray(n.fills)&&n.fills.length&&n.fills[n.fills.length-1].imageHash)IMGS[n.name.slice(4)]=n.fills[n.fills.length-1].imageHash;}
const hex2=h=>({r:parseInt(h.slice(0,2),16)/255,g:parseInt(h.slice(2,4),16)/255,b:parseInt(h.slice(4,6),16)/255});
function P(c){if(c[0]==='@'){const v=VARS['color/'+c.slice(1)];const p={type:'SOLID',color:{r:0,g:0,b:0}};return figma.variables.setBoundVariableForPaint(p,'color',v);}
 return {type:'SOLID',color:hex2(c),opacity:c.length>6?parseInt(c.slice(6,8),16)/255:1};}
function bindTree(n){const fx=(arr)=>arr.map(p=>{if(p.type!=='SOLID')return p;const h=[p.color.r,p.color.g,p.color.b].map(x=>Math.round(x*255).toString(16).padStart(2,'0')).join('');
 const t=TOK[h];return t?figma.variables.setBoundVariableForPaint(p,'color',VARS['color/'+t]):p;});
 if('fills' in n&&Array.isArray(n.fills)&&n.fills.length)n.fills=fx(n.fills);if('strokes' in n&&n.strokes.length)n.strokes=fx(n.strokes);if('children' in n)for(const c of n.children)bindTree(c);}
function QR(seed){let s=seed;const rnd=()=>{s=(s*16807)%2147483647;return s/2147483647};const n=21,c=170/n;let o="<svg viewBox='0 0 170 170'><rect width='170' height='170' fill='#fff'/>";for(let y=0;y<n;y++)for(let x=0;x<n;x++){if((x<8&&y<8)||(x>12&&y<8)||(x<8&&y>12))continue;if(rnd()<0.48)o+="<rect x='"+(x*c).toFixed(1)+"' y='"+(y*c).toFixed(1)+"' width='"+(c+.3).toFixed(2)+"' height='"+(c+.3).toFixed(2)+"' fill='#111'/>";}
 const fd=(x,y)=>"<rect x='"+x*c+"' y='"+y*c+"' width='"+7*c+"' height='"+7*c+"' fill='#111'/><rect x='"+(x+1)*c+"' y='"+(y+1)*c+"' width='"+5*c+"' height='"+5*c+"' fill='#fff'/><rect x='"+(x+2)*c+"' y='"+(y+2)*c+"' width='"+3*c+"' height='"+3*c+"' fill='#111'/>";return o+fd(0,0)+fd(14,0)+fd(0,14)+"</svg>";}
function BC(spec){return "<svg viewBox='0 0 282 54'>"+spec.split(',').map(p=>{const [x,w]=p.split(':');return "<rect x='"+x+"' y='0' width='"+w+"' height='54' fill='#111'/>"}).join('')+"</svg>";}
const err=[];
function T(a,par){const [_,x,y,w,h,s,wt,fs,lh,col,lines,ex]=a;const e=ex||{};const t=figma.createText();par.appendChild(t);t.fontName={family:'Onest',style:W[wt]||'Regular'};t.characters=s;t.fontSize=fs;t.lineHeight={value:lh,unit:'PIXELS'};t.fills=[P(col)];if(e.ls)t.letterSpacing={value:e.ls,unit:'PIXELS'};
 if(lines>1){t.resize(w+3,lh*lines);t.textAutoResize='HEIGHT';if(e.ta)t.textAlignHorizontal=e.ta==='c'?'CENTER':'RIGHT';t.x=x;}else{t.textAutoResize='WIDTH_AND_HEIGHT';t.x=Math.round(e.ta==='r'?x+w-t.width:e.ta==='c'?x+(w-t.width)/2:x);}
 t.y=Math.round(y+h/2-t.height/2);t.name=s.slice(0,40);
 if(e.v&&VARS[e.v]){t.setBoundVariable('characters',VARS[e.v]);t.name=e.v;}}
function S(a,par){try{let src=a[5];if(src.startsWith('#QR'))src=QR(+src.slice(3));else if(src.startsWith('#BC'))src=BC(src.slice(3));
 const n=figma.createNodeFromSvg(src.replace('<svg','<svg xmlns="http://www.w3.org/2000/svg"'));par.appendChild(n);n.x=a[1];n.y=a[2];if(a[3]>0&&a[4]>0)n.resize(a[3],a[4]);n.name=src.length>3000?'code':'icon';bindTree(n);}catch(e){err.push(String(e).slice(0,80))}}
function I(a,par){const [_,x,y,w,h,key,fit,rad,ex]=a;const e=ex||{};const r=figma.createRectangle();par.appendChild(r);r.x=x;r.y=y;r.resize(Math.max(1,w),Math.max(1,h));r.cornerRadius=rad||0;r.name='фото: '+key;
 const fills=[];if(e.f)fills.push(P(e.f));if(IMGS[key])fills.push({type:'IMAGE',imageHash:IMGS[key],scaleMode:fit==='n'?'FIT':'FILL'});else{fills.push(P('@photo'));err.push('noimg '+key)}r.fills=fills;}
function B(o,par){const f=figma.createFrame();par.appendChild(f);f.name=o.g?o.n+' → '+String(o.g).padStart(2,'0'):(o.cl?'вставка екрана '+o.cl:o.n);f.x=o.b[0];f.y=o.b[1];f.resize(Math.max(1,o.b[2]),Math.max(1,o.b[3]));f.fills=o.f?[P(o.f)]:[];
 if(o.s){f.strokes=[P(o.s[0])];f.strokeWeight=o.s[1];f.strokeAlign='INSIDE';}
 if(o.r!=null){if(Array.isArray(o.r)){f.topLeftRadius=o.r[0];f.topRightRadius=o.r[1];f.bottomRightRadius=o.r[2];f.bottomLeftRadius=o.r[3];}else f.cornerRadius=o.r;}
 f.clipsContent=!!o.c;if(o.o!=null)f.opacity=o.o;
 for(const k of o.k||[]){if(Array.isArray(k)){k[0]==='t'?T(k,f):k[0]==='i'?I(k,f):S(k,f)}else B(k,f)}return f;}
"""


def builder(imgs):
    tok = {h: k for h, k in PULSE.items()}
    return BUILDER.replace("__TOK__", json.dumps(tok))


def screen_batch(nums, imgs, page_name):
    names = {n: "%02d %s" % (n, t) for n, t, _ in SCREENS}
    D = {n: comp["app%02d" % n] for n in nums}
    code = ("const D=" + json.dumps(D, ensure_ascii=False, separators=(",", ":")) + ";\nconst N=" +
            json.dumps({n: names[n] for n in nums}, ensure_ascii=False) + ";\n" + builder(imgs) +
            "\nconst page=figma.root.children.find(p=>p.name===%s);await figma.setCurrentPageAsync(page);const made={};\n"
            "for(const i in D){const nm=N[i];for(const old of page.children.filter(c=>c.name===nm))old.remove();const f=B(D[i],page);f.name=nm;const j=+i-1;f.x=(j%%7)*470;f.y=Math.floor(j/7)*1000;f.cornerRadius=0;made[nm]=f.id;}\n"
            "return {made,err:err.slice(0,6),nerr:err.length};" % json.dumps(page_name, ensure_ascii=False))
    return code


def site_batch(imgs, page_name):
    D = comp["site"]
    code = ("const D=" + json.dumps(D, ensure_ascii=False, separators=(",", ":")) + ";\n" + builder(imgs) +
            "\nconst page=figma.root.children.find(p=>p.name===%s);await figma.setCurrentPageAsync(page);\n"
            "for(const old of page.children.filter(c=>c.name==='Сайт · десктоп'))old.remove();const f=B(D,page);f.name='Сайт · десктоп';f.x=0;f.y=0;f.cornerRadius=0;\n"
            "return {id:f.id,h:f.height,err:err.slice(0,6),nerr:err.length};" % json.dumps(page_name, ensure_ascii=False))
    return code


if __name__ == "__main__":
    imgs = json.load(open(os.path.join(OUT, "hashes.json"))) if os.path.exists(os.path.join(OUT, "hashes.json")) else {}
    pn = "Застосунок"
    groups = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11], [12, 13, 14]]
    for i, g in enumerate(groups):
        c = screen_batch(g, imgs, pn)
        open(os.path.join(OUT, "fb%d.js" % i), "w").write(c); print("fb%d" % i, len(c))
    c = site_batch(imgs, "Сайт")
    open(os.path.join(OUT, "fsite.js"), "w").write(c); print("fsite", len(c))
