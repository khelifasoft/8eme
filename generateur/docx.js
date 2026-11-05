const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,WidthType,ShadingType,BorderStyle,AlignmentType,LevelFormat,HeadingLevel,VerticalAlign}=require('docx');
const outDir=process.argv[2];
const stories=JSON.parse(fs.readFileSync(__dirname+'/stories.json','utf8'));
const FONT='Arial';
const W=10466;
const strip=t=>t.replace(/<[^>]+>/g,'');
const run=(text,o={})=>new TextRun({text,font:FONT,rightToLeft:true,...o});
const para=(children,o={})=>new Paragraph({bidirectional:true,alignment:AlignmentType.START,children:Array.isArray(children)?children:[run(children)],...o});
const hex=c=>c.replace('#','').toUpperCase();
const KIND={ev:'C78A00',lk:'8A55D7',mv:'3F7EE0',ct:'C97F00'};
const thin={style:BorderStyle.SINGLE,size:4,color:'D9D9D9'};
const borders={top:thin,bottom:thin,left:thin,right:thin};

function h2(text,main,accent){
  return para([run(text,{bold:true,size:28,color:hex(main)})],{heading:HeadingLevel.HEADING_2,spacing:{before:160,after:80},keepNext:true,border:{bottom:{style:BorderStyle.SINGLE,size:12,color:hex(accent),space:2}}});
}
function cell(text,w,o={}){
  return new TableCell({width:{size:w,type:WidthType.DXA},borders,verticalAlign:VerticalAlign.TOP,margins:{top:60,bottom:60,left:90,right:90},
    shading:o.fill?{type:ShadingType.CLEAR,fill:o.fill,color:'auto'}:undefined,
    children:[para([run(text,{size:o.size||22,bold:o.bold,color:o.color})])]});
}
function build(s){
  const main=hex(s.main), accent=hex(s.accent), chip=hex(s.chip);
  const children=[];
  children.push(new Paragraph({bidirectional:true,alignment:AlignmentType.START,heading:HeadingLevel.TITLE,spacing:{after:40},children:[run(s.title,{bold:true,size:64,color:main})]}));
  children.push(para([run('ورقة التلميذ · مشروع سكراتش: قصة وسيناريو وتمثيل المشاهد',{size:22,color:'555555'})],{spacing:{after:60}}));
  children.push(para([run('الاسم: ............................        القسم: ........        التاريخ: ........',{size:22})],{spacing:{after:120},border:{bottom:{style:BorderStyle.SINGLE,size:18,color:accent,space:6}}}));

  children.push(h2('١. ملخص القصة',s.main,s.accent));
  children.push(para([run(s.summary,{size:24})],{spacing:{after:100,line:320}}));
  children.push(new Paragraph({bidirectional:true,alignment:AlignmentType.START,spacing:{before:40,after:80},shading:{type:ShadingType.CLEAR,fill:chip,color:'auto'},children:[run(s.morale,{bold:true,size:26,color:main})]}));

  children.push(h2('٢. الشخصيات والديكورات',s.main,s.accent));
  const cast=s.cast.map(([n,x])=>x?`${n} (${x})`:n).join('  ·  ');
  children.push(para([run('الشخصيات: ',{bold:true,size:24}),run(cast,{size:24})],{spacing:{after:60}}));
  const parts=s.decors.split(/(<span class="fig">.*?<\/span>)/);
  const dr=[run('الديكورات: ',{bold:true,size:24})];
  parts.forEach(p=>{ if(!p)return; if(p.startsWith('<span')) dr.push(run(strip(p),{bold:true,size:24})); else dr.push(run(strip(p).replace(/^الديكورات: /,''),{size:24}));});
  children.push(para(dr,{spacing:{after:60}}));

  children.push(h2('٣. السيناريو',s.main,s.accent));
  const cols=[1500,1250,1500,3416,2800];
  const head=['المشهد','الديكور','من يتكلم','النص','ما يحدث في سكراتش'];
  const rows=[new TableRow({tableHeader:true,children:head.map((t,i)=>cell(t,cols[i],{bold:true,fill:chip,color:main,size:22}))})];
  s.rows.forEach(r=>rows.push(new TableRow({cantSplit:true,children:r.map((t,i)=>cell(t,cols[i],{bold:i===0,color:i===0?main:undefined,size:21}))})));
  children.push(new Table({width:{size:W,type:WidthType.DXA},columnWidths:cols,visuallyRightToLeft:true,rows}));

  children.push(h2('٤. تمثيل المشاهد في سكراتش',s.main,s.accent));
  const steps=[`أضف الديكورات واللاعبين: ${s.sprites}.`,'في لاعب الديكور: ابدأ بـ «عند النقر على العلم الأخضر» ثم «أرسل مشهد 1»، وبين كل مشهدين «انتظر 3 ثوان».','في كل لاعب: «عند استلام مشهد N» ثم «بدّل الزي» و«انزلق» و«قل ... لمدة 2 ثانية».','سجّل صوتك في مشهد واحد على الأقل.'];
  steps.forEach(t=>children.push(para([run(t,{size:23})],{numbering:{reference:'steps',level:0},spacing:{after:50}})));
  const br=[run('الكتل المستعملة: ',{bold:true,size:22})];
  s.blocks.forEach(([k,t])=>{br.push(run(' '+t+' ',{size:20,bold:true,color:'FFFFFF',shading:{type:ShadingType.CLEAR,fill:KIND[k],color:'auto'}}));br.push(run('  ',{size:20}));});
  children.push(para(br,{spacing:{before:80,after:60,line:360}}));

  children.push(h2('٥. قائمة التحقق',s.main,s.accent));
  s.checks.forEach(t=>children.push(para([run(t,{size:23})],{numbering:{reference:'checks',level:0},spacing:{after:30}})));

  children.push(h2('٦. رأيي في القصة',s.main,s.accent));
  children.push(para([run('اكتب جملة أو جملتين: ماذا تعلمت من هذه القصة؟',{size:21,color:'666666'})],{spacing:{after:60}}));
  children.push(new Table({width:{size:W,type:WidthType.DXA},columnWidths:[W],rows:[new TableRow({height:{value:700,rule:'atLeast'},children:[new TableCell({width:{size:W,type:WidthType.DXA},borders:{top:{style:BorderStyle.DASHED,size:4,color:'999999'},bottom:{style:BorderStyle.DASHED,size:4,color:'999999'},left:{style:BorderStyle.DASHED,size:4,color:'999999'},right:{style:BorderStyle.DASHED,size:4,color:'999999'}},children:[para([run('')])]})]})]}));

  return new Document({
    creator:'khelifasoft',title:s.title,
    styles:{default:{document:{run:{font:FONT,size:22}}},
      paragraphStyles:[
        {id:'Title',name:'Title',basedOn:'Normal',run:{font:FONT,size:64,bold:true,color:main},paragraph:{spacing:{before:0,after:40},keepNext:true}},
        {id:'Heading2',name:'Heading 2',basedOn:'Normal',next:'Normal',quickFormat:true,run:{font:FONT,size:28,bold:true,color:main},paragraph:{spacing:{before:160,after:80},keepNext:true,outlineLevel:1}}]},
    numbering:{config:[
      {reference:'steps',levels:[{level:0,format:LevelFormat.DECIMAL,text:'%1.',alignment:AlignmentType.START,style:{paragraph:{indent:{left:540,hanging:360}}}}]},
      {reference:'checks',levels:[{level:0,format:LevelFormat.BULLET,text:'☐',alignment:AlignmentType.START,style:{paragraph:{indent:{left:540,hanging:360}}}}]}]},
    sections:[{properties:{page:{size:{width:11906,height:16838},margin:{top:480,bottom:420,left:720,right:720}}},children}]
  });
}
(async()=>{for(const [k,s] of Object.entries(stories)){const b=await Packer.toBuffer(build(s));fs.writeFileSync(`${outDir}/${k}.docx`,b);}console.log('done');})();
