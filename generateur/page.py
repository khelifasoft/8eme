"""Construit index.html (page d'accueil de l'élève) à partir de manifest.json."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
man = json.load(open(os.path.join(HERE, "manifest.json"), encoding="utf-8"))
TPL = r'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ورشة القصص مع سكراتش</title>
<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#1f4aa8">
<link rel="icon" href="icones/icone.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icones/icone-192.png">
<style>
:root{--ink:#1d2433;--muted:#5d6678;--line:#dfe3ec;--soft:#f4f6fb;--blue:#1f4aa8;--orange:#e8861c;--green:#1e8a5a;
 --font:'Segoe UI','Tahoma','Arial','Noto Sans Arabic',sans-serif}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:#fff;color:var(--ink);font-family:var(--font);line-height:1.7;font-size:16px}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left)) 0 max(16px,env(safe-area-inset-right))}
header.top{border-bottom:3px solid var(--orange);padding:28px 0 20px}
header.top h1{margin:0;font-size:clamp(28px,5vw,44px);color:var(--blue);line-height:1.2}
header.top p{margin:6px 0 0;color:var(--muted);font-size:17px}
.head{display:flex;justify-content:space-between;gap:16px;align-items:flex-start;flex-wrap:wrap}
#install{display:inline-flex;align-items:center;gap:8px;font-size:16px;padding:8px 18px;white-space:nowrap}
#install[hidden]{display:none}
dialog{border:1px solid var(--line);border-radius:14px;max-width:min(520px,92vw);padding:20px 22px;font-family:var(--font);direction:rtl;color:var(--ink)}
dialog::backdrop{background:rgba(20,30,50,.45)}
dialog h3{margin:0 0 8px;font-size:20px;color:var(--blue)}
dialog ul{margin:8px 0 14px;padding-inline-start:20px}
dialog li{margin:4px 0}
dialog .small{font-size:14px;color:var(--muted)}
nav.jump{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}
nav.jump a{border:1px solid var(--line);border-radius:999px;padding:4px 16px;text-decoration:none;font-size:15px;background:#fff}
nav.jump a:hover,nav.jump a:focus-visible{border-color:var(--blue);color:var(--blue)}
section{padding:30px 0 6px}
h2{font-size:26px;margin:0 0 6px;color:var(--blue)}
h2+.lead{margin:0 0 18px;color:var(--muted)}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;counter-reset:s;padding:0;list-style:none;margin:0}
.steps li{border:1px solid var(--line);border-radius:10px;padding:14px 16px 14px 14px;counter-increment:s;background:var(--soft)}
.steps li::before{content:counter(s);display:inline-grid;place-items:center;width:30px;height:30px;border-radius:50%;background:var(--blue);color:#fff;font-weight:700;margin-inline-end:10px}
.stories{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:16px}
.card{border:1px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;background:#fff}
.card .bar{height:8px}
.card .body{padding:14px 16px;display:flex;flex-direction:column;gap:8px;flex:1}
.card h3{margin:0;font-size:21px}
.card p{margin:0;font-size:15px;color:var(--muted)}
.card .morale{font-size:14px;color:var(--ink);background:var(--soft);padding:4px 10px;border-radius:6px}
.btns{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:auto}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;border:1px solid var(--blue);color:var(--blue);background:#fff;border-radius:8px;padding:6px 8px;font:inherit;font-size:14px;text-decoration:none;cursor:pointer;text-align:center;line-height:1.35}
.btn:hover,.btn:focus-visible{background:var(--blue);color:#fff}
.btn.main{background:var(--blue);color:#fff}
.btn.main:hover{background:#163a86}
.btn.wide{grid-column:1/-1}
.btn.alt{border-color:var(--orange);color:#a85a08}.btn.alt:hover{background:var(--orange);color:#fff}
.tools{position:sticky;top:0;background:#fff;z-index:5;border-bottom:1px solid var(--line);padding:10px 0;display:flex;flex-direction:column;gap:10px}
.tabs{display:flex;gap:6px;flex-wrap:wrap}
.tab{border:1px solid var(--line);background:#fff;border-radius:999px;padding:5px 16px;font:inherit;font-size:15px;cursor:pointer}
.tab[aria-selected=true]{background:var(--blue);border-color:var(--blue);color:#fff}
.tab small{opacity:.75;margin-inline-start:4px}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.row input[type=search],.row select{font:inherit;font-size:15px;padding:6px 12px;border:1px solid var(--line);border-radius:8px;background:#fff;min-width:0}
.row input[type=search]{flex:1 1 220px}
.subs{display:flex;gap:6px;flex-wrap:wrap}
.chip{border:1px solid var(--line);background:#fff;border-radius:8px;padding:2px 12px;font:inherit;font-size:14px;cursor:pointer}
.chip[aria-pressed=true]{background:var(--soft);border-color:var(--ink);font-weight:700}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;padding:16px 0}
.grid.wideg{grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}
.tile{border:1px solid var(--line);border-radius:10px;padding:8px;display:flex;flex-direction:column;gap:6px;align-items:stretch;background:#fff;min-width:0}
.tile .pv{height:120px;display:grid;place-items:center;background:repeating-conic-gradient(#f4f6fb 0 25%,#fff 0 50%) 0 0/16px 16px;border-radius:6px;overflow:hidden}
.wideg .tile .pv{height:150px}
.tile .pv img{max-width:100%;max-height:100%;object-fit:contain}
.tile .nm{font-size:14px;text-align:center;line-height:1.35;min-height:2.7em;display:grid;place-items:center;overflow-wrap:anywhere}
.tile .fr{font-size:12px;color:var(--muted);text-align:center;margin-top:-4px;direction:ltr}
.tile .dl{font-size:13px;padding:3px 6px}
.sound{flex-direction:row;align-items:center;gap:10px;padding:8px 10px}
.sounds{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px;padding:16px 0}
.play{flex:none;width:42px;height:42px;border-radius:50%;border:0;background:var(--green);color:#fff;font-size:18px;cursor:pointer}
.play[aria-pressed=true]{background:#c0392b}
.sound .nm{flex:1;min-height:0;text-align:right;place-items:start}
.sound .meta{font-size:12px;color:var(--muted)}
.empty{padding:40px 0;color:var(--muted);text-align:center}
.zipbar{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;color:var(--muted);font-size:14px;padding-top:10px}
.help{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.help div{border:1px solid var(--line);border-radius:10px;padding:12px 16px}
.help h3{margin:0 0 4px;font-size:18px}
.help p,.help ol{margin:0;font-size:15px;padding-inline-start:20px}
.help p{padding:0}
footer{margin-top:40px;border-top:1px solid var(--line);padding:18px 0 40px;color:var(--muted);font-size:14px}
.vtools{margin:8px 0}
.vform{border:1px solid var(--line);border-radius:12px;padding:14px 16px;display:grid;gap:10px;background:var(--soft);margin-bottom:14px}
.vform label{display:grid;gap:4px;font-size:15px}
.vform input,.vform select{font:inherit;padding:6px 10px;border:1px solid var(--line);border-radius:8px;background:#fff;min-width:0}
.vhint{margin:0;font-size:13px;color:var(--muted)}
.vgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;padding:10px 0 6px}
.vcard{border:1px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;background:#fff}
.vmedia{aspect-ratio:16/9;background:#1d2433;position:relative;display:grid;place-items:center}
.vmedia iframe,.vmedia video{position:absolute;inset:0;width:100%;height:100%;border:0}
.vplay{width:68px;height:68px;border-radius:50%;border:0;background:var(--orange);color:#fff;font-size:28px;cursor:pointer}
.vmedia .host{position:absolute;bottom:8px;inset-inline-start:10px;color:#fff;font-size:13px;opacity:.85;direction:ltr}
.vinfo{padding:10px 14px;display:flex;flex-direction:column;gap:4px}
.vinfo h3{margin:0;font-size:17px}
.vinfo p{margin:0;font-size:14px;color:var(--muted)}
.vinfo .vlinks{display:flex;gap:8px;flex-wrap:wrap;align-items:center;font-size:13px}
.vinfo .vlinks a,.vinfo .vlinks button{font:inherit;color:var(--blue);background:none;border:0;padding:0;cursor:pointer;text-decoration:underline}
.vbadge{display:inline-block;font-size:12px;background:var(--soft);border:1px solid var(--line);border-radius:999px;padding:0 10px;align-self:flex-start}
.sr{position:absolute;left:-9999px}
:focus-visible{outline:3px solid var(--orange);outline-offset:2px}
@media (max-width:560px){.btns{grid-template-columns:1fr}}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <div class="head"><h1>ورشة القصص مع سكراتش</h1>
  <button type="button" class="btn main" id="install" hidden>⬇ اختصار على سطح المكتب</button></div>
  <p>كل ما تحتاجه لإنشاء مشروعك في صفحة واحدة: أوراق المشاريع، مشاريع جاهزة، أصوات، صور، أماكن وديكورات. لا حاجة إلى الإنترنت.</p>
  <nav class="jump" aria-label="التنقّل"><a href="#start">كيف أبدأ؟</a><a href="#scratch">تحميل سكراتش</a><a href="#stories">اختر قصتك</a><a href="#videos">فيديوهات</a><a href="#library">المكتبة</a><a href="#help">مساعدة</a></nav>
</div></header>

<main class="wrap">
<section id="start">
  <h2>كيف أبدأ؟</h2>
  <p class="lead">أربع خطوات بسيطة.</p>
  <ol class="steps">
    <li>اختر قصة من القائمة أدناه.</li>
    <li>حمّل <b>ورقة المشروع</b> واقرأها: فيها الملخص والسيناريو وخطوات العمل.</li>
    <li>افتح <b>سكراتش</b> (<a href="#scratch">حمّله من هنا</a>) ثم «ملف ← تحميل من حاسوبك» واختر ملف المشروع (.sb3).</li>
    <li>غيّر الصور والأصوات والحوارات من <b>المكتبة</b> لتصنع مشروعك الخاص.</li>
  </ol>
</section>

<section id="scratch">
  <h2>سكراتش 3</h2>
  <p class="lead">لتشغيل المشاريع تحتاج إلى برنامج سكراتش. يمكنك استعماله على الإنترنت أو تثبيته على الحاسوب.</p>
  <div class="btns" style="max-width:640px">
    <a class="btn main" href="https://scratch.mit.edu/download" target="_blank" rel="noopener">⬇ تحميل سكراتش 3 للحاسوب (من الموقع الرسمي)</a>
    <a class="btn" href="https://scratch.mit.edu/projects/editor/" target="_blank" rel="noopener">فتح سكراتش على الإنترنت</a>
  </div>
  <p class="small" style="margin:8px 0 0;font-size:14px;color:var(--muted)">النسخة المثبّتة تعمل دون إنترنت وتفتح ملفات المشاريع (.sb3) مباشرة. الروابط تفتح الموقع الرسمي لسكراتش في نافذة جديدة.</p>
</section>

<section id="stories">
  <h2>اختر قصتك</h2>
  <p class="lead">لكل قصة ورقة مشروع، ومشروع سكراتش جاهز، وحزمة واحدة تجمع كل ما تحتاجه.</p>
  <div class="stories" id="storyGrid"></div>
</section>

<section id="videos">
  <h2>فيديوهات</h2>
  <p class="lead">شاهد الفيديو هنا دون مغادرة الصفحة. الفيديوهات تبقى في موقعها الأصلي (يوتيوب وغيره) ولا تُحمَّل في المشروع.</p>
  <div class="row vtools">
    <select id="vstory" aria-label="تصفية الفيديوهات حسب القصة"></select>
    <button type="button" class="btn" id="vadd">+ إضافة رابط فيديو</button>
  </div>
  <form id="vform" class="vform" hidden>
    <label>رابط الفيديو أو كود التضمين
      <input type="text" id="vurl" placeholder="https://www.youtube.com/watch?v=… أو https://vimeo.com/…" dir="ltr" required></label>
    <label>العنوان (اختياري)<input type="text" id="vtitle"></label>
    <label>القصة<select id="vst"></select></label>
    <div class="row"><button class="btn main" type="submit">إضافة</button><button class="btn" type="button" id="vcancel">إلغاء</button></div>
    <p class="vhint">الرابط يُحفَظ في هذا المتصفح فقط. لإظهاره للجميع، أضِفه في الملف <b dir="ltr">videos.js</b>.</p>
  </form>
  <div class="vgrid" id="vgrid"></div>
</section>

<section id="library">
  <h2>المكتبة</h2>
  <p class="lead">صور وأصوات ورسوم متحركة يمكنك استعمالها في أي قصة. اضغط «تحميل» ثم أضف الملف في سكراتش.</p>
  <div class="tools">
    <div class="tabs" role="tablist" id="tabs"></div>
    <div class="row">
      <input type="search" id="q" placeholder="ابحث بالعربية أو بالفرنسية…" aria-label="بحث">
      <select id="story" aria-label="تصفية حسب القصة"></select>
      <div class="subs" id="subs"></div>
    </div>
  </div>
  <div class="zipbar"><span id="count"></span><span id="zipwrap"></span></div>
  <div id="out"></div>
</section>

<section id="help">
  <h2>مساعدة</h2>
  <div class="help">
    <div><h3>أضيف صورة جديدة</h3><ol><li>في سكراتش، اضغط على «اختيار لاعب» ثم «رفع لاعب».</li><li>اختر ملف الصورة (.svg) من المجلد.</li></ol></div>
    <div><h3>أضيف مكانًا (خلفية)</h3><ol><li>اضغط على «اختيار خلفية» ثم «رفع خلفية».</li><li>اختر ملفًا من «الأماكن».</li></ol></div>
    <div><h3>أضيف صوتًا</h3><ol><li>افتح لسان «الأصوات» في اللاعب.</li><li>اضغط «رفع صوت» واختر ملف (.wav).</li><li>استعمل الكتلة «ابدأ الصوت».</li></ol></div>
    <div><h3>أصنع حركة</h3><ol><li>حمّل «إطارات» الحركة من تبويب الصور المتحركة.</li><li>فك الضغط، ثم ارفع الصور كأزياء متتالية للاعب.</li><li>استعمل «التالي الزي» داخل حلقة مع «انتظر».</li></ol></div>
    <div><h3>أسجّل صوتي</h3><p>الأصوات الجاهزة المسمّاة «أصوات جاهزة» مولَّدة آليًا. لتسجيل صوتك، افتح لسان «الأصوات» في سكراتش واضغط على الميكروفون.</p></div>
  </div>
</section>
</main>
<dialog id="installHelp" aria-labelledby="ihTitle">
  <h3 id="ihTitle">اختصار على سطح المكتب</h3>
  <div id="ihBody"></div>
  <form method="dialog"><button class="btn main" style="margin-top:10px">حسنًا</button></form>
</dialog>
<footer><div class="wrap">الصور مرسومة خصيصًا لهذه الورشة، والأصوات والموسيقى مولَّدة بالحاسوب، ويمكنك استعمالها وتعديلها بحرّية في مشاريعك.</div></footer>

<script src="videos.js"></script>
<script>
const DATA = __DATA__;
const CATS = [
  {id:"lieux", name:"الأماكن", wide:true, hint:"خلفيات كاملة للمشاهد"},
  {id:"decors", name:"الديكور", hint:"أشياء تضعها في المشهد"},
  {id:"personnages", name:"الشخصيات"},
  {id:"animaux", name:"الحيوانات"},
  {id:"costumes", name:"الأزياء", subs:{accessoires:"إكسسوارات", tenues:"ملابس", variantes:"نسخ القصص"}},
  {id:"animations", name:"الصور المتحركة"},
  {id:"sons", name:"الأصوات", subs:{effets:"مؤثرات صوتية", musique:"موسيقى", voix:"أصوات جاهزة"}},
];
const $ = s => document.querySelector(s);
const el = (t, a={}, ...kids) => { const e = document.createElement(t); for (const k in a){ if(k==="class") e.className=a[k]; else if(k==="text") e.textContent=a[k]; else e.setAttribute(k,a[k]); } kids.flat().forEach(c=>c&&e.append(c)); return e; };
const state = {cat:"lieux", sub:"", q:"", story:""};
try { const h = location.hash.replace("#",""); if (CATS.some(c=>c.id===h)) state.cat = h; } catch(e){}

// ---- histoires
const grid = $("#storyGrid");
DATA.stories.forEach(s => {
  const card = el("article",{class:"card"},
    el("div",{class:"bar",style:`background:${s.accent}`}),
    el("div",{class:"body"},
      el("h3",{text:s.title,style:`color:${s.main}`}),
      el("p",{text:s.summary}),
      el("div",{class:"morale",text:s.morale}),
      el("div",{class:"btns"},
        el("a",{class:"btn main",href:s.docx,download:`ورقة ${s.title}.docx`,text:"ورقة المشروع (Word)"}),
        el("a",{class:"btn",href:s.doc,download:`ورقة ${s.title}.doc`,title:"للإصدارات القديمة من Word (2003 و2007)",text:"Word قديم (.doc)"}),
        el("a",{class:"btn",href:s.html,target:"_blank",rel:"noopener",text:"قراءة الورقة"}),
        el("a",{class:"btn",href:s.sb3,download:`${s.title}.sb3`,text:"مشروع سكراتش"}),
        el("button",{class:"btn alt",type:"button","data-story":s.key,text:`موارد القصة (${s.n})`}),
        el("a",{class:"btn",href:s.pack,download:`حزمة ${s.title}.zip`,text:"كل شيء (.zip)"}))));
  grid.append(card);
});
grid.addEventListener("click", e => { const b = e.target.closest("[data-story]"); if(!b) return; state.story = b.dataset.story; $("#story").value = state.story; render(); document.getElementById("library").scrollIntoView(); });

// ---- bibliothèque
const counts = {}; DATA.assets.forEach(a => counts[a.cat] = (counts[a.cat]||0)+1);
const tabs = $("#tabs");
CATS.forEach(c => tabs.append(el("button",{class:"tab",role:"tab",type:"button","data-cat":c.id},c.name,el("small",{text:counts[c.id]||0}))));
tabs.addEventListener("click", e => { const b=e.target.closest("[data-cat]"); if(!b) return; state.cat=b.dataset.cat; state.sub=""; render(); });
const sel = $("#story"); sel.append(el("option",{value:"",text:"كل القصص"})); DATA.stories.forEach(s => sel.append(el("option",{value:s.key,text:s.title})));
sel.addEventListener("change", () => { state.story = sel.value; render(); });
$("#q").addEventListener("input", e => { state.q = e.target.value.trim().toLowerCase(); render(); });

let audio = null, playBtn = null;
function stop(){ if(audio){ audio.pause(); audio=null;} if(playBtn){ playBtn.setAttribute("aria-pressed","false"); playBtn.textContent="▶"; playBtn=null; } }
function play(btn, file){
  if(playBtn===btn){ stop(); return; }
  stop(); audio = new Audio(file); playBtn = btn; btn.setAttribute("aria-pressed","true"); btn.textContent="■";
  audio.addEventListener("ended", stop); audio.play().catch(()=>stop());
}
function fname(a){ return (a.label||a.id).replace(/[\\/:*?"<>|«»؟!]/g,"").slice(0,60) + "." + a.ext; }
let timers = [];
function render(){
  stop(); timers.forEach(clearInterval); timers = [];
  const cat = CATS.find(c=>c.id===state.cat);
  tabs.querySelectorAll(".tab").forEach(b => b.setAttribute("aria-selected", b.dataset.cat===state.cat));
  const subs = $("#subs"); subs.replaceChildren();
  if(cat.subs){ subs.append(el("button",{class:"chip",type:"button","aria-pressed":String(!state.sub),"data-sub":"",text:"الكل"})); for(const k in cat.subs) subs.append(el("button",{class:"chip",type:"button","aria-pressed":String(state.sub===k),"data-sub":k,text:cat.subs[k]})); }
  let items = DATA.assets.filter(a => a.cat===state.cat && (!state.sub || a.sub===state.sub) && (!state.story || a.tags.includes(state.story)) && (!state.q || (a.label+" "+(a.fr||"")+" "+a.id).toLowerCase().includes(state.q)));
  $("#count").textContent = items.length ? `${items.length} عنصر` : "";
  const zw = $("#zipwrap"); zw.replaceChildren();
  if(DATA.zips[state.cat]) zw.append(el("a",{class:"btn",href:DATA.zips[state.cat],download:`${cat.name}.zip`,text:`تحميل كل «${cat.name}» (.zip)`}));
  const out = $("#out"); out.replaceChildren();
  if(!items.length){ out.append(el("div",{class:"empty",text:"لا توجد نتائج. جرّب كلمة أخرى أو اختر «كل القصص»."})); return; }
  if(state.cat==="sons"){
    const g = el("div",{class:"sounds"});
    items.forEach(a => {
      const b = el("button",{class:"play",type:"button","aria-pressed":"false","aria-label":"استمع: "+a.label,text:"▶"});
      b.addEventListener("click", () => play(b, a.file));
      g.append(el("div",{class:"tile sound"}, b, el("div",{class:"nm"}, el("span",{text:a.label}), el("span",{class:"meta",text:(a.fr?a.fr+" · ":"")+a.dur+" ث"})),
        el("a",{class:"btn dl",href:a.file,download:fname(a),text:"تحميل"})));
    });
    out.append(g); return;
  }
  const g = el("div",{class:"grid"+(cat.wide?" wideg":"")});
  items.forEach(a => {
    const img = el("img",{src:a.file,alt:a.label,loading:"lazy"});
    if(a.frames){ let i=0; timers.push(setInterval(()=>{ i=(i+1)%a.frames.length; img.src=a.frames[i]; }, 1000/a.fps/1.0*1.2)); }
    const t = el("div",{class:"tile"}, el("div",{class:"pv"}, img), el("div",{class:"nm",text:a.label}),
      a.frames ? el("a",{class:"btn dl",href:a.zip,download:`${a.label}.zip`,text:`تحميل الإطارات (${a.frames.length})`}) : el("a",{class:"btn dl",href:a.file,download:fname(a),text:"تحميل"}));
    g.append(t);
  });
  out.append(g);
}
$("#subs").addEventListener("click", e => { const b=e.target.closest("[data-sub]"); if(!b) return; state.sub=b.dataset.sub; render(); });
render();

// ---- فيديوهات : affichage dans la page, sans télécharger la vidéo
function embedInfo(raw){
  raw = (raw||"").trim();
  const m = raw.match(/<iframe[^>]*\ssrc=["']([^"']+)["']/i); if (m) raw = m[1];
  if (raw.startsWith("//")) raw = "https:" + raw;
  let u; try { u = new URL(raw); } catch(e){ return null; }
  if (!/^https?:$/.test(u.protocol)) return null;
  const h = u.hostname.replace(/^(www|m|music)\./,""), p = u.pathname, q = u.searchParams;
  const t = parseInt(q.get("t")||q.get("start")||"0",10) || 0;
  const yt = id => ({kind:"iframe", host:"YouTube", src:`https://www.youtube-nocookie.com/embed/${id}?rel=0${t?`&start=${t}`:""}`});
  if (h === "youtu.be") { const id = p.slice(1).split("/")[0]; return id ? yt(id) : null; }
  if (h === "youtube.com" || h === "youtube-nocookie.com") {
    if (p === "/watch" && q.get("v")) return yt(q.get("v"));
    const mm = p.match(/^\/(embed|shorts|live|v)\/([\w-]{6,})/); if (mm && mm[2] !== "videoseries") return yt(mm[2]);
    if ((p === "/playlist" || mm) && q.get("list")) return {kind:"iframe", host:"YouTube", src:`https://www.youtube-nocookie.com/embed/videoseries?list=${encodeURIComponent(q.get("list"))}`};
    return null;
  }
  if (h === "vimeo.com" || h === "player.vimeo.com") { const id = (p.match(/(\d{5,})/)||[])[1]; return id ? {kind:"iframe", host:"Vimeo", src:`https://player.vimeo.com/video/${id}`} : null; }
  if (h === "dailymotion.com" || h === "dai.ly") { const id = h === "dai.ly" ? p.slice(1) : (p.match(/\/video\/([a-z0-9]+)/i)||[])[1]; return id ? {kind:"iframe", host:"Dailymotion", src:`https://www.dailymotion.com/embed/video/${id}`} : null; }
  if (h === "archive.org") { const id = (p.match(/^\/(?:details|embed)\/([^/]+)/)||[])[1]; return id ? {kind:"iframe", host:"Internet Archive", src:`https://archive.org/embed/${id}`} : null; }
  if (h === "drive.google.com") { const id = (p.match(/\/file\/d\/([\w-]+)/)||[])[1] || q.get("id"); return id ? {kind:"iframe", host:"Google Drive", src:`https://drive.google.com/file/d/${id}/preview`} : null; }
  if (h === "ted.com" || h === "embed.ted.com") { const mm = p.match(/\/talks\/([^/?]+)/); return mm ? {kind:"iframe", host:"TED", src:`https://embed.ted.com/talks/${mm[1]}`} : null; }
  if (h === "facebook.com" || h === "fb.watch") return {kind:"iframe", host:"Facebook", src:`https://www.facebook.com/plugins/video.php?href=${encodeURIComponent(u.href)}&show_text=false`};
  if (/\.(mp4|webm|ogv|ogg)$/i.test(p)) return {kind:"video", host:h, src:u.href};
  if (/\/embed\//i.test(p) || /^player\./.test(h)) return {kind:"iframe", host:h, src:u.href};
  return {kind:"link", host:h, src:u.href};
}
const VKEY = "ateliers-contes-videos";
const userVideos = () => { try { return JSON.parse(localStorage.getItem(VKEY)||"[]"); } catch(e){ return []; } };
const saveUserVideos = a => { try { localStorage.setItem(VKEY, JSON.stringify(a)); return true; } catch(e){ return false; } };
const vsel = $("#vstory"), vst = $("#vst");
vsel.append(el("option",{value:"",text:"كل القصص"})); vst.append(el("option",{value:"",text:"بدون قصة"}));
DATA.stories.forEach(s => { vsel.append(el("option",{value:s.key,text:s.title})); vst.append(el("option",{value:s.key,text:s.title})); });
function playVideo(box, info, title){
  const old = box.querySelector(".vplay"); if (old) old.remove();
  if (info.kind === "video") box.append(el("video",{src:info.src,controls:"",autoplay:"",playsinline:"","aria-label":title}));
  else box.append(el("iframe",{src:info.src,title,allow:"autoplay; fullscreen; picture-in-picture; encrypted-media",allowfullscreen:"",referrerpolicy:"strict-origin-when-cross-origin",loading:"lazy"}));
}
function renderVideos(){
  const g = $("#vgrid"); g.replaceChildren();
  const mine = userVideos().map((v,i)=>({...v,mine:i}));
  const all = (window.VIDEOS||[]).concat(mine).filter(v => !vsel.value || v.story === vsel.value);
  if (!all.length) { g.append(el("div",{class:"empty",text: (window.VIDEOS||[]).length+mine.length ? "لا توجد فيديوهات لهذه القصة." : "لا توجد فيديوهات بعد. اضغط «إضافة رابط فيديو» والصق رابطًا من يوتيوب أو غيره."})); return; }
  all.forEach(v => {
    const info = embedInfo(v.url); const st = DATA.stories.find(s=>s.key===v.story);
    const title = v.title || (info ? info.host : "فيديو");
    const media = el("div",{class:"vmedia"});
    if (info && info.kind !== "link") { const b = el("button",{class:"vplay",type:"button","aria-label":"تشغيل: "+title,text:"▶"}); b.addEventListener("click", () => playVideo(media, info, title)); media.append(b); }
    else media.append(el("a",{class:"btn",href:v.url,target:"_blank",rel:"noopener",text:"هذا الموقع لا يسمح بالعرض هنا. افتحه في موقعه"}));
    if (info) media.append(el("span",{class:"host",text:info.host}));
    const links = el("div",{class:"vlinks"}, el("a",{href:v.url,target:"_blank",rel:"noopener",text:"فتح في الموقع الأصلي"}));
    if (v.mine !== undefined) { const r = el("button",{type:"button",text:"حذف"}); r.addEventListener("click", () => { const a = userVideos(); a.splice(v.mine,1); saveUserVideos(a); renderVideos(); }); links.append(r); }
    g.append(el("article",{class:"vcard"}, media, el("div",{class:"vinfo"}, st && el("span",{class:"vbadge",text:st.title}), el("h3",{text:title}), v.note && el("p",{text:v.note}), links)));
  });
}
vsel.addEventListener("change", renderVideos);
$("#vadd").addEventListener("click", () => { const f = $("#vform"); f.hidden = !f.hidden; if (!f.hidden) $("#vurl").focus(); });
$("#vcancel").addEventListener("click", () => { $("#vform").hidden = true; });
$("#vform").addEventListener("submit", e => {
  e.preventDefault(); const url = $("#vurl").value.trim(); const info = embedInfo(url);
  if (!info) { $("#vurl").setCustomValidity("الرابط غير صحيح"); $("#vurl").reportValidity(); setTimeout(()=>$("#vurl").setCustomValidity(""),2500); return; }
  const a = userVideos(); a.push({title:$("#vtitle").value.trim(), url: (info.kind==="iframe" && /<iframe/i.test(url)) ? info.src : url, story:$("#vst").value}); saveUserVideos(a);
  $("#vform").reset(); $("#vform").hidden = true; renderVideos();
});
renderVideos();

// ---- installation / raccourci sur le bureau
const instBtn = $("#install"), dlg = $("#installHelp");
let deferred = null;
const standalone = () => matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;
const secure = location.protocol === "https:" || location.hostname === "localhost" || location.hostname === "127.0.0.1";
const ua = navigator.userAgent;
const OS = /android/i.test(ua) ? "android" : /iphone|ipad|ipod/i.test(ua) ? "ios" : /windows/i.test(ua) ? "windows" : /mac/i.test(ua) ? "mac" : "linux";
const TITLE = "ورشة القصص", FILE = "Atelier-contes";
if (!standalone()) instBtn.hidden = false;
window.addEventListener("beforeinstallprompt", e => { e.preventDefault(); deferred = e; instBtn.hidden = false; });
window.addEventListener("appinstalled", () => { deferred = null; instBtn.hidden = true; });

// Fichier raccourci : fonctionne aussi en HTTP sur un réseau local (pas besoin de HTTPS).
function shortcut(){
  const url = location.href.split("#")[0];
  const esc = x => x.replace(/&/g,"&amp;").replace(/</g,"&lt;");
  if (OS === "windows") return {name: FILE + ".url", type: "application/octet-stream", text: "[InternetShortcut]\r\nURL=" + url + "\r\n"};
  if (OS === "mac") return {name: FILE + ".webloc", type: "application/xml", text: '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0"><dict><key>URL</key><string>' + esc(url) + '</string></dict></plist>\n'};
  return {name: FILE + ".desktop", type: "application/x-desktop", text: "[Desktop Entry]\nVersion=1.0\nType=Application\nName=" + TITLE + "\nExec=xdg-open " + url + "\nTerminal=false\nIcon=applications-education\nCategories=Education;\n"};
}
function download(f){
  const a = el("a",{href:URL.createObjectURL(new Blob([f.text],{type:f.type})),download:f.name}); document.body.append(a); a.click(); a.remove();
}
function showHelp(kids){ const body = $("#ihBody"); body.replaceChildren(...kids); dlg.showModal(); }
instBtn.addEventListener("click", async () => {
  if (deferred) { deferred.prompt(); try { await deferred.userChoice; } catch(e){} deferred = null; return; }
  if (OS === "ios") return showHelp([el("p",{text:"في آيفون وآيباد:"}), el("ul",{}, el("li",{text:"اضغط على زر المشاركة في Safari."}), el("li",{text:"اختر «إضافة إلى الشاشة الرئيسية»."}))]);
  if (OS === "android") return showHelp([el("p",{text:"في هاتف أندرويد:"}), el("ul",{}, el("li",{text:"اضغط على قائمة المتصفح (⋮)."}), el("li",{text:"اختر «إضافة إلى الشاشة الرئيسية»."}))]);
  const f = shortcut(); download(f);
  const where = OS === "windows" ? "اسحب الملف إلى سطح المكتب." : OS === "mac" ? "اسحب الملف إلى سطح المكتب أو إلى الـ Dock." : "انقله إلى سطح المكتب، ثم انقر عليه بالزر الأيمن واختر «السماح بالتشغيل».";
  const kids = [el("p",{text:"تم تنزيل ملف الاختصار «" + f.name + "». " + where}),
    el("p",{text:"عند النقر عليه يفتح الموقع في المتصفح مباشرة. إن ظهر تحذير أثناء التنزيل فاختر «الاحتفاظ بالملف»."})];
  if (!secure) kids.push(el("p",{class:"small",text:"ملاحظة: التثبيت كتطبيق مستقل يتطلب HTTPS. على شبكة محلية بدون HTTPS يعمل الاختصار بالشكل الموضّح أعلاه."}));
  showHelp(kids);
});
if ("serviceWorker" in navigator && secure) navigator.serviceWorker.register("sw.js").catch(() => {});
</script>
</body>
</html>
'''
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(TPL.replace("__DATA__", json.dumps(man, ensure_ascii=False)))
print("index.html", os.path.getsize(os.path.join(ROOT, "index.html")) // 1024, "Ko")
