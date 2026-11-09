// PDF de chaque fiche d'activité : fiches-activite/pdf/fiche-<id>[-<conte>]-{ar,fr}.pdf   Usage : node fichepdf.js
const { chromium } = require('playwright'); const {execSync}=require('child_process'); const path=require('path'), fs=require('fs');
(async()=>{ const root=path.resolve(__dirname,'..'), out=path.join(root,'fiches-activite','pdf'); fs.mkdirSync(out,{recursive:true});
 const b=await chromium.launch(); const p=await (await b.newContext({viewport:{width:900,height:1200}})).newPage();
 await p.goto('file://'+root+'/index.html'); await p.waitForTimeout(500);
 const keys=await p.evaluate(()=>DATA.stories.map(s=>s.key));
 const routes=['catch','course','saut','labyrinthe',...keys.map(k=>'contes-'+k)];
 for(const r of routes) for(const l of ['ar','fr']){
  await p.goto('file://'+root+'/index.html?lang='+l+'#fiche-'+r); await p.waitForTimeout(500);
  await p.evaluate(()=>{document.querySelectorAll('img[loading]').forEach(i=>i.loading='eager')}); await p.waitForTimeout(600);
  await p.addStyleTag({content:'.pdfrow,.btns,#viewHome,.fiche .btn,.fiche p:has(.btn){display:none!important}'});
  const f=path.join(out,'fiche-'+r+'-'+l+'.pdf');
  for(let sc=1; sc>=0.3; sc-=0.05){ await p.pdf({path:f,format:'A4',printBackground:true,scale:sc,margin:{top:'8mm',bottom:'8mm',left:'8mm',right:'8mm'}});
   if(+execSync('pdfinfo '+f).toString().match(/Pages:\s+(\d+)/)[1]===1) break; }
 } await b.close(); console.log(routes.length*2,'PDF'); })();
