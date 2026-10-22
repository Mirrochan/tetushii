"""Батчі use_figma для сайту v3 з дедуплікацією svg і однакових піддерев."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out2"); sys.path.insert(0, HERE)
from fig4 import builder

comp = json.load(open(os.path.join(OUT, "comp7.json")))
names = {int(k): v for k, v in json.load(open(os.path.join(OUT, "wnames4.json"))).items()}
QRS = {}


def shrink(n, ctx):
    if isinstance(n, list):
        if n[0] == "s" and len(n[5]) > 2000:
            s = n[5]
            if "0 0 160 160" in s or "0 0 170 170" in s: n[5] = "#QR" + ctx
            else: n[5] = "#BC" + ",".join("%s:%s" % b for b in re.findall(r"<rect x='(\d+)' y='0' width='(\d+)'", s))
        elif n[0] == "s" and n[5].startswith("<svg viewBox='0 0 282 54'>"):
            n[5] = "#BC" + ",".join("%s:%s" % b for b in re.findall(r"<rect x='(\d+)' y='0' width='(\d+)'", n[5]))
        return
    for k in n.get("k", []): shrink(k, ctx)


for k, v in comp.items(): shrink(v, QRS.get(k, ""))

def pos(n):
    return (n % 20) * 1560, 30000
def _old(n):
    if n < 140: j = n - 101; return (j % 7) * 1560, (j // 7) * 3200
    if n < 150: return (n - 140) * 1560, 16400
    return (n - 150) * 470, 17700

J = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))


def dedupe(D):
    SV = []
    def ded(n):
        if isinstance(n, list):
            if n[0] == "s" and not n[5].startswith("#"):
                if n[5] not in SV: SV.append(n[5])
                n[5] = "#S%d" % SV.index(n[5])
            return
        for k in n.get("k", []): ded(k)
    for v in D.values(): ded(v)
    TP = []
    while True:
        cnt = {}
        def walk(n, top=False):
            if isinstance(n, list) or "R" in n: return
            if not top:
                key = J({k: v for k, v in n.items() if k != "b"})
                if len(key) > 250: cnt.setdefault(key, []).append(n)
            for k in n.get("k", []): walk(k)
        for v in D.values(): walk(v, True)
        for t in TP: walk(t, True)
        best = None
        for key, lst in cnt.items():
            if len(lst) >= 2:
                gain = len(key) * (len(lst) - 1)
                if not best or gain > best[0]: best = (gain, key, lst)
        if not best or best[0] < 300: break
        _, key, lst = best
        idx = len(TP); TP.append(json.loads(key) | {"b": [0, 0] + lst[0]["b"][2:]})
        for n in lst:
            b = n["b"]; n.clear(); n["R"] = idx; n["b"] = b
    return SV, TP


B = builder().replace("Палітра 1 · зелена","Палітра · Тутешні")
B = B.replace("function B(o,par){const f=figma.createFrame();",
              "const CACHE={};function B(o,par){if(o.R!=null){let c;if(CACHE[o.R]){c=CACHE[o.R].clone();par.appendChild(c);}else{c=B(TP[o.R],par);CACHE[o.R]=c;}c.x=o.b[0];c.y=o.b[1];return c;}const f=figma.createFrame();")
B = B.replace("function I(a,par){const [_,x,y,w,h,key,fit,rad,ex]=a;const e=ex||{};",
              "function I(a,par){const [_,x,y,w,h,key,fit,rad,ex]=a;const e=ex||{};if(key==='s_hero'){const fr=figma.createFrame();par.appendChild(fr);fr.name=\"фото: інтер'єр\";fr.x=x;fr.y=y;fr.resize(w,h);fr.cornerRadius=rad;fr.clipsContent=true;fr.fills=[P('@photo')];const tw=w/3;for(let i=0;i<3;i++){const t=figma.createRectangle();fr.appendChild(t);const k='s_hero_'+(i+1);t.name='фото: '+k;t.x=Math.round(i*tw);t.y=0;t.resize(Math.round((i+1)*tw)-Math.round(i*tw)+(i<2?1:0),h);t.fills=IMGS[k]?[{type:'IMAGE',imageHash:IMGS[k],scaleMode:'FILL'}]:[P('@photo')];}return;}")

def gen(g, gi):
    D = {n: json.loads(J(comp["web%d" % n])) for n in g}
    SV, TP = dedupe(D)
    P = {n: pos(n) for n in g}
    tail = ("\nconst page=figma.root.children.find(p=>p.name==='Сайт');await figma.setCurrentPageAsync(page);%s\n"
            "for(const i in D){const nm=N[i];for(const old of page.findAll(c=>c.type==='FRAME'&&c.name===nm&&(c.parent.type==='SECTION'||c.parent.type==='PAGE')))old.remove();const f=B(D[i],page);f.name=nm;f.x=XY[i][0];f.y=XY[i][1];f.cornerRadius=0;}\n"
            "return {made:Object.keys(D).length,err:err.slice(0,6),nerr:err.length};") % ("" if gi == 0 else "")
    code = ("const SV=" + J(SV) + ";\nconst TP=" + J(TP) + ";\nconst D=" + J(D) + ";\nconst N=" + J({n: names[n] for n in g}) + ";\nconst XY=" + J(P) + ";\n" + B + tail)
    return code.replace(',"<svg', '\n,"<svg').replace('},"', '}\n,"').replace('}},{"', '}}\n,{"')


if __name__ == "__main__":
    order = sorted(names); groups = []; cur = []
    for n in order:
        if cur and len(gen(cur + [n], len(groups))) > 48500: groups.append(cur); cur = []
        cur.append(n)
    groups.append(cur)
    for gi, g in enumerate(groups):
        code = gen(g, gi); open(os.path.join(OUT, "ft%d.js" % gi), "w").write(code); print(gi, g, len(code))
