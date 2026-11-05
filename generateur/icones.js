// Génère les icônes PNG de l'application à partir de icone.svg (Playwright).
const {chromium}=require('playwright'),fs=require('fs'),path=require('path');
(async()=>{const b=await chromium.launch();const svg=fs.readFileSync(path.join(__dirname,'icone.svg'),'utf8');
 for(const s of [192,512]){const p=await b.newPage({viewport:{width:s,height:s}});
  await p.setContent(`<body style="margin:0"><img src="data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}" width="${s}" height="${s}"></body>`);
  await p.screenshot({path:path.join(__dirname,'..','icones',`icone-${s}.png`)});}
 await b.close();})();
