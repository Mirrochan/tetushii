const fs=require('fs');
function node(type){const n={type,children:[],fills:[],strokes:[],name:'',x:0,y:0,width:100,height:100,
 appendChild(c){c.parent=n;n.children.push(c)},resize(w,h){if(!(w>0&&h>0))throw new Error('bad resize '+w+','+h);n.width=w;n.height=h},
 clone(){const c=node(type);Object.assign(c,{name:n.name,width:n.width,height:n.height});c.children=n.children.map(k=>{const kk=k.clone();kk.parent=c;return kk});return c},
 remove(){},findAll(f){let r=[];for(const c of n.children){if(f(c))r.push(c);r=r.concat(c.findAll(f))}return r},findOne(f){return n.findAll(f)[0]},
 setBoundVariable(){},async setReactionsAsync(){},set characters(v){if(typeof v!=='string')throw new Error('chars');n._c=v},get characters(){return n._c}};return n}
const pages=['Застосунок','Сайт','Фото та джерела'].map(nm=>{const p=node('PAGE');p.name=nm;p.loadAsync=async()=>{};return p});
const res=pages[2];for(const k of ['d_bowl','d_borsch','d_soup','d_holubtsi','d_syrnyky','d_deruny','g_gala','g_potato','g_tomato','g_carrots','z_coffee','z_fresh','z_kitchen','z_locker','z_space']){const r=node('RECTANGLE');r.name='img:'+k;r.fills=[{type:'IMAGE',imageHash:'h'+k}];res.children.push(r)}
const vars=['bg','surface','ink','soft','line','brand','deep','onbrand','tint','tint2','accent','photo'].map(t=>({id:'v'+t,name:'color/'+t,variableCollectionId:'c1'}));
global.figma={root:{children:pages},loadFontAsync:async()=>{},setCurrentPageAsync:async()=>{},
 variables:{getLocalVariableCollectionsAsync:async()=>[{id:'c1',name:'Палітра · Тутешні'}],getLocalVariablesAsync:async()=>vars,setBoundVariableForPaint:(p,f,v)=>{if(!v)throw new Error('no var');return p}},
 createFrame:()=>node('FRAME'),createText:()=>node('TEXT'),createRectangle:()=>node('RECTANGLE'),
 createNodeFromSvg:(s)=>{if(!s.startsWith('<svg'))throw new Error('svg '+s.slice(0,30));return node('FRAME')},flatten:(a)=>node('VECTOR')};
(async()=>{for(const f of process.argv.slice(2)){const AF=Object.getPrototypeOf(async function(){}).constructor;try{const r=await new AF(fs.readFileSync(f,'utf8'))();console.log(f,JSON.stringify(r))}catch(e){console.log(f,'ERR',e.message)}}})();
