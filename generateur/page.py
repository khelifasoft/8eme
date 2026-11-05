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
.sr{position:absolute;left:-9999px}
:focus-visible{outline:3px solid var(--orange);outline-offset:2px}
@media (max-width:560px){.btns{grid-template-columns:1fr}}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <h1>ورشة القصص مع سكراتش</h1>
  <p>كل ما تحتاجه لإنشاء مشروعك في صفحة واحدة: أوراق المشاريع، مشاريع جاهزة، أصوات، صور، أماكن وديكورات. لا حاجة إلى الإنترنت.</p>
  <nav class="jump" aria-label="التنقّل"><a href="#start">كيف أبدأ؟</a><a href="#stories">اختر قصتك</a><a href="#library">المكتبة</a><a href="#help">مساعدة</a></nav>
</div></header>

<main class="wrap">
<section id="start">
  <h2>كيف أبدأ؟</h2>
  <p class="lead">أربع خطوات بسيطة.</p>
  <ol class="steps">
    <li>اختر قصة من القائمة أدناه.</li>
    <li>حمّل <b>ورقة المشروع</b> واقرأها: فيها الملخص والسيناريو وخطوات العمل.</li>
    <li>افتح <b>سكراتش</b> ثم «ملف ← تحميل من حاسوبك» واختر ملف المشروع (.sb3).</li>
    <li>غيّر الصور والأصوات والحوارات من <b>المكتبة</b> لتصنع مشروعك الخاص.</li>
  </ol>
</section>

<section id="stories">
  <h2>اختر قصتك</h2>
  <p class="lead">لكل قصة ورقة مشروع، ومشروع سكراتش جاهز، وحزمة واحدة تجمع كل ما تحتاجه.</p>
  <div class="stories" id="storyGrid"></div>
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
<footer><div class="wrap">الصور مرسومة خصيصًا لهذه الورشة، والأصوات والموسيقى مولَّدة بالحاسوب، ويمكنك استعمالها وتعديلها بحرّية في مشاريعك.</div></footer>

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
        el("a",{class:"btn",href:s.html,target:"_blank",rel:"noopener",text:"قراءة الورقة"}),
        el("a",{class:"btn",href:s.sb3,download:`${s.title}.sb3`,text:"مشروع سكراتش"}),
        el("button",{class:"btn alt",type:"button","data-story":s.key,text:`موارد القصة (${s.n})`}),
        el("a",{class:"btn wide",href:s.pack,download:`حزمة ${s.title}.zip`,text:"تحميل كل شيء لهذه القصة (.zip)"}))));
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
</script>
</body>
</html>
'''
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(TPL.replace("__DATA__", json.dumps(man, ensure_ascii=False)))
print("index.html", os.path.getsize(os.path.join(ROOT, "index.html")) // 1024, "Ko")
