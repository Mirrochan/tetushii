const page=figma.root.children.find(p=>p.name==='Сайт');await figma.setCurrentPageAsync(page);
for(const s of ['Regular','Medium','SemiBold','Bold','ExtraBold'])await figma.loadFontAsync({family:'Onest',style:s});
const rep={};
const all=()=>{const a=[];for(const s of page.children){if(s.type==='SECTION'){for(const f of s.children)if(f.type==='FRAME')a.push(f);}else if(s.type==='FRAME'&&s.name!=='Компоненти')a.push(s);}return a;};
const byPre=p=>all().find(f=>f.name.startsWith(p+' '));
// 1. mobile footers
const mg=byPre('МГ1');const mfSrc=mg.children.find(n=>n.name==='mf');
for(const f of all().filter(f=>/^М\d+ /.test(f.name))){const om=f.children.find(n=>n.name==='mf');if(om&&om.findOne(t=>t.type==='TEXT'&&t.characters.startsWith('Retail Hub'))){const nf=mfSrc.clone();f.appendChild(nf);nf.x=om.x;nf.y=om.y;om.remove();}}
// 2. M2 nav row -> gift
const m2=byPre('М2');const row=m2&&m2.children.find(r=>r.name.startsWith('row')&&r.findOne(t=>t.type==='TEXT'&&t.characters==='Продукти'));
if(row){const t=row.findOne(t=>t.type==='TEXT'&&t.characters==='Продукти');await figma.loadFontAsync(t.fontName);t.characters='Подарунок з дому';row.name='row → 170';rep.m2='ok';}
// 3. scenario chips
const SC=['Сніданок із собою','Вечеря за 20 хв','Гості за годину'];
for(const p of ['С2','М3']){const f=byPre(p);if(!f)continue;const ch=f.children.filter(n=>n.type==='INSTANCE'&&/Чип/.test(n.name)).sort((a,b)=>a.y-b.y||a.x-b.x);
 const y0=ch.length?ch[0].y:0;const r1=ch.filter(c=>Math.abs(c.y-y0)<4);rep[p+'before']=r1.map(c=>c.findAll(t=>t.type==='TEXT').map(t=>t.characters).join(''));
 if(r1.length>=4){for(let i=0;i<3;i++){const t=r1[i+1].findOne(n=>n.type==='TEXT');await figma.loadFontAsync(t.fontName);t.characters=SC[i];}
  let x=r1[0].x;const gap=r1[1].x-(r1[0].x+r1[0].width);for(const c of r1){c.x=x;x+=c.width+gap;}
  rep[p+'over']=x>f.width-16;}
}
const s2=byPre('С2');const sub=s2&&s2.children.find(t=>t.type==='TEXT'&&t.characters.startsWith('Одне меню на день'));
if(sub){await figma.loadFontAsync(sub.fontName);sub.characters="Сьогодні готує Солом'янка: одне меню на день з кухні магазину, частина страв за рецептами мешканців району. Склад і алергени є на сторінці страви.";rep.sub=sub.width;}
// 4. sections
const sec=n=>page.children.find(s=>s.type==='SECTION'&&s.name===n);
function mkSec(n){let s=sec(n);if(!s){s=figma.createSection();s.name=n;page.appendChild(s);}return s;}
function lay(s,fr,per){const pad=120,gap=120;let x=pad,y=pad+40,rowH=0,maxW=0,i=0;for(const f of fr){if(f.parent!==s)s.appendChild(f);if(i>0&&i%per===0){x=pad;y+=rowH+gap;rowH=0;}f.x=x;f.y=y;x+=f.width+gap;maxW=Math.max(maxW,x);rowH=Math.max(rowH,f.height);i++;}s.resizeWithoutConstraints(maxW-gap+pad,y+rowH+pad);}
const main=sec('Основний сценарій');lay(main,[byPre('С1'),...main.children.filter(f=>f.type==='FRAME'&&!f.name.startsWith('С1 '))],8);
const gs=mkSec('Основний сценарій · Подарунок з дому');lay(gs,['Г1','Г2','Г3','Г4'].map(byPre),4);
const gm=mkSec('Основний сценарій · Подарунок з дому, мобільна');lay(gm,['МГ1','МГ2','МГ3','МГ4'].map(byPre),4);
const er=sec('Додатково · помилки й порожні стани');lay(er,[...er.children.filter(f=>f.type==='FRAME'),byPre('Г5')],4);
const mb=sec('Додатково · мобільна версія сайту');lay(mb,[byPre('М1'),...mb.children.filter(f=>f.type==='FRAME'&&!f.name.startsWith('М1 '))],8);
const order=['Основний сценарій','Основний сценарій · Подарунок з дому','Основний сценарій · Подарунок з дому, мобільна','Додатково · інші картки й родина',"Додатково · комірка, кур'єр, кава, оплата при отриманні",'Додатково · кабінет і документи','Додатково · помилки й порожні стани','Додатково · мобільна версія сайту','Додатково · панель магазину (для персоналу)'];
let Y=0;for(const n of order){const s=sec(n);if(!s)continue;s.x=0;s.y=Y;Y+=s.height+240;}
rep.loose=page.children.filter(c=>c.type!=='SECTION').map(c=>c.name);
// 5. wiring
const P=c=>c<140?'С'+(c-100):c<150?'П'+(c-139):c<160?'М'+(c-149):c<170?'Г'+(c-159):'МГ'+(c-169);
const top={};const tops=all();for(const f of tops){top[f.id]=f;}
const cache={};const tgt=c=>{if(!(c in cache))cache[c]=byPre(P(c));return cache[c];};
let links=0,self=0,miss=[];
for(const k of tops){for(const nd of k.findAll(x=>/ → \d+$/.test(x.name))){const c=+nd.name.match(/ → (\d+)$/)[1];const t=tgt(c);
 if(!t){miss.push(k.name+':'+c);continue;}
 try{if(t.id===k.id){await nd.setReactionsAsync([]);nd.name=nd.name.replace(/ → \d+$/,'');self++;}
 else{await nd.setReactionsAsync([{trigger:{type:'ON_CLICK'},actions:[{type:'NODE',destinationId:t.id,navigation:'NAVIGATE',transition:{type:'DISSOLVE',duration:0.2,easing:{type:'EASE_OUT'}},preserveScrollPosition:false,resetVideoPosition:false}]}]);links++;}}catch(e){miss.push('err '+k.name+' '+String(e).slice(0,60));}}}
rep.links=links;rep.self=self;rep.miss=miss.slice(0,10);rep.nmiss=miss.length;
// 6. flows
const old=page.flowStartingPoints.filter(f=>!/Сайт|Подарунок|Мобільна/.test(f.name)).map(f=>({nodeId:f.nodeId,name:f.name.replace(/^\d+ · /,'')}));
const fl=[{nodeId:byPre('С1').id,name:'Сайт: головна й замовлення'},{nodeId:byPre('Г1').id,name:'Подарунок з дому'},{nodeId:byPre('МГ1').id,name:'Подарунок з дому · мобільна'},{nodeId:byPre('М1').id,name:'Мобільна версія сайту'},...old];
const seen=new Set();page.flowStartingPoints=fl.filter(f=>!seen.has(f.nodeId)&&seen.add(f.nodeId)).map((f,i)=>({nodeId:f.nodeId,name:(i+1)+' · '+f.name}));
rep.flows=page.flowStartingPoints.map(f=>f.name);
return rep;
