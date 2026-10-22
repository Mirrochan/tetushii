import json, os, re, sys
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"out2"); sys.path.insert(0,HERE)
def shrink(n,ctx):
    if isinstance(n,list):
        if n[0]=="s" and len(n[5])>2500:
            s=n[5]
            if "0 0 170 170" in s: n[5]="#QR"+ctx
            else: n[5]="#BC"+",".join("%s:%s"%b for b in re.findall(r"<rect x='(\d+)' y='0' width='(\d+)'",s))
        return
    for k in n.get("k",[]): shrink(k,ctx)
def builder():
    f2=open(os.path.join(HERE,"fig2.py")).read()
    B=f2[f2.index('BUILDER = r"""')+len('BUILDER = r"""'):]; B=B[:B.index('"""')]
    TOK=json.dumps({"f7eee2":"bg","fffaf3":"surface","142a1f":"ink","5d6b60":"soft","e8dccb":"line","23402c":"brand","0e2319":"deep","ffffff":"onbrand","f3dcc6":"tint","dfe4d2":"tint2","fa7f52":"accent","eec39e":"photo"})
    B=B.replace("__TOK__",TOK).replace("'Бренд · Пульс'","'Палітра 1 · зелена'")
    B=B.replace("fill='#fff'/>\";for","fill='#fefefe'/>\";for").replace("fill='#fff'/>\";return o+fd","fill='#fefefe'/>\";return o+fd")
    B=B.replace("n.name=src.length>3000?'code':'icon';bindTree(n);","if(src.length>3000){const g=figma.flatten([n]);g.name='код';}else{n.name='icon';bindTree(n);}")
    B=B.replace("(o.cl?'вставка екрана '+o.cl:o.n)","o.n")
    B=B.replace("let src=a[5];if(","let src=a[5];if(src.startsWith('#S'))src=SV[+src.slice(2)];if(")
    return B
if __name__=="__main__":
    comp=json.load(open(os.path.join(OUT,"comp5.json"))); names=json.load(open(os.path.join(OUT,"names3.json")))
    ctx={"app10":"274","app11":"1414","app20":"12"}
    for k,v in comp.items(): shrink(v,ctx.get(k,""))
    B=builder()
    tail=("\nconst page=figma.root.children.find(p=>p.name==='Застосунок');await figma.setCurrentPageAsync(page);const made={};\n"
          "for(const i in D){const nm=N[i];for(const old of page.children.filter(c=>c.name===nm))old.remove();const f=B(D[i],page);f.name=nm;const j=+i-1;f.x=(j%7)*470;f.y=Math.floor(j/7)*1000;f.cornerRadius=0;made[nm]=f.id;}\n"
          "return {made:Object.keys(made).length,err:err.slice(0,6),nerr:err.length};")
    LIM=int(os.environ.get("LIM","60000"));groups=[];cur=[];sz=0
    for n in range(1,42):
        d=len(json.dumps(comp["app%02d"%n],ensure_ascii=False,separators=(",",":")))
        if sz+d>LIM and cur: groups.append(cur);cur=[];sz=0
        cur.append(n);sz+=d
    groups.append(cur)
    for gi,g in enumerate(groups):
        D={n:comp["app%02d"%n] for n in g}
        SV=[];
        def ded(n):
            if isinstance(n,list):
                if n[0]=="s" and not n[5].startswith("#"):
                    if n[5] not in SV: SV.append(n[5])
                    n[5]="#S%d"%SV.index(n[5])
                return
            for k in n.get("k",[]): ded(k)
        for v in D.values(): ded(v)
        SV=[("#BC"+",".join("%s:%s"%b for b in re.findall(r"<rect x='(\d+)' y='0' width='(\d+)'",x))) if x.startswith("<svg viewBox='0 0 282 54'>") else x for x in SV]
        code="const SV="+json.dumps(SV,ensure_ascii=False,separators=(",",":"))+";\nconst D="+json.dumps(D,ensure_ascii=False,separators=(",",":"))+";\nconst N="+json.dumps({n:names[str(n)] for n in g},ensure_ascii=False)+";\n"+B+tail
        code=code.replace(',"<svg','\n,"<svg').replace('},"','}\n,"').replace('const D={"','const D={\n"')
        open(os.path.join(OUT,"fa%d.js"%gi),"w").write(code);print(gi,g,len(code))
