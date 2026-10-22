import re,json,sys
def parse(fn):
    L=open(fn).read().split('\n')
    sv_txt=''; i=0
    while not L[i].startswith('const TP='): sv_txt+=L[i]+'\n'; i+=1
    sv=json.loads(sv_txt.strip()[len('const SV='):].rstrip(';'))
    d_txt=''
    j=[k for k,l in enumerate(L) if l.startswith('const D=')][0]
    while not L[j].startswith('const N='): d_txt+=L[j]+'\n'; j+=1
    D=json.loads(d_txt.strip()[len('const D='):].rstrip(';'))
    return sv,D
sv0,D0=parse('ft0.js'); sv1,D1=parse('ft1.js')
SV=[];D={}
def remap(o,sv):
    if isinstance(o,list):
        if o and o[0]=='s' and isinstance(o[5],str) and o[5].startswith('#S'):
            s=sv[int(o[5][2:])]
            if s not in SV: SV.append(s)
            o[5]='#S%d'%SV.index(s)
        for x in o: remap(x,sv)
    elif isinstance(o,dict):
        for x in o.values(): remap(x,sv)
for k in ['162','170','171']: remap(D0[k],sv0); D[k]=D0[k]
for k in ['172','173']: remap(D1[k],sv1); D[k]=D1[k]
out='const SV='+json.dumps(SV,ensure_ascii=False)+';\nconst TP='
# TP from ft0 (footer) needed for 162
tp=[l for l in open('ft0.js').read().split('\n') if l.startswith('const TP=')][0]
out='const SV='+json.dumps(SV,ensure_ascii=False)+';\n'+tp+'\nconst D='+json.dumps(D,ensure_ascii=False,separators=(',',':'))+';\n'
N={"162":"Г3 Оформлення подарунка","170":"МГ1 Подарунок з дому","171":"МГ2 Набір","172":"МГ3 Оформлення подарунка","173":"МГ4 Подарунок прийнято"}
XY={k:[9360+i*1560,30000] for i,k in enumerate(N)}
out+='const N='+json.dumps(N,ensure_ascii=False)+';\nconst XY='+json.dumps(XY)+';\n'
open('fb2data.js','w').write(out); print(len(out), len(SV))
