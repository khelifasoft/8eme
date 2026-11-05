"""Construit index.html (page d'accueil de l'élève) à partir de manifest.json."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
man = json.load(open(os.path.join(HERE, "manifest.json"), encoding="utf-8"))
import sys; sys.path.insert(0, HERE)
import i18n_fr
games = json.load(open(os.path.join(HERE, "jeux2_manifest.json"), encoding="utf-8"))
games += json.load(open(os.path.join(HERE, "jeux3_manifest.json"), encoding="utf-8"))
for g in json.load(open(os.path.join(HERE, "jeux_manifest.json"), encoding="utf-8")):
    games.append(dict(g, cat="catch", cat_ar="التقاط الأشياء (لكل قصة لعبة)", cat_fr="Attrape-objets (un jeu par conte)"))
man["games"] = games
FR = i18n_fr.build(man, games)
TPL = r'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>قصص سكراتش</title>
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
.hero{border-bottom:3px solid var(--orange);padding:24px 0 18px}
.hero h1{margin:0;font-size:clamp(28px,5vw,44px);color:var(--blue);line-height:1.2}
.hero p{margin:6px 0 0;color:var(--muted);font-size:17px}
html{scroll-padding-top:68px}
body{padding-top:56px}
.topbar{position:fixed;top:0;inset-inline:0;height:56px;background:var(--blue);color:#fff;z-index:50;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:0 max(16px,env(safe-area-inset-left)) 0 max(16px,env(safe-area-inset-right));box-shadow:0 2px 8px rgba(20,40,100,.25)}
.brand{color:#fff;text-decoration:none;font-weight:800;font-size:21px;white-space:nowrap}
.tabsnav{display:flex;gap:6px;height:100%;align-items:stretch}
.tabsnav a{color:rgba(255,255,255,.88);text-decoration:none;font-weight:700;font-size:17px;padding:0 20px;display:flex;align-items:center;border-bottom:4px solid transparent;border-top:4px solid transparent}
.tabsnav a:hover,.tabsnav a:focus-visible{color:#fff;background:rgba(255,255,255,.14)}
.tabsnav a[aria-current=page]{color:#fff;border-bottom-color:#fff;background:rgba(255,255,255,.12)}
.barbtns{display:flex;align-items:center;gap:6px}
.langbtn{font:inherit;font-size:13px;font-weight:700;color:#fff;background:transparent;border:1px solid rgba(255,255,255,.65);border-radius:6px;padding:3px 10px;cursor:pointer}
.langbtn[aria-pressed=true]{background:#fff;color:var(--blue);border-color:#fff}
.back{display:inline-block;margin:16px 0 4px;color:var(--blue);font-weight:700;text-decoration:none}
.back:hover{text-decoration:underline}
.storyhead{border:1px solid var(--line);border-radius:14px;overflow:hidden;margin:8px 0 8px}
.storyhead .sbar{height:10px}
.storyhead .sbody{padding:16px 20px;display:flex;flex-direction:column;gap:8px}
.storyhead h2{margin:0;font-size:30px}
.storyhead p{margin:0;color:var(--muted)}
.helpbox{margin:30px 0 0;border:1px solid var(--line);border-radius:12px;padding:10px 16px}
.helpbox summary{cursor:pointer;font-size:20px;font-weight:700;color:var(--blue)}
.helpbox .help{margin-top:12px}
@media (max-width:560px){.brand{font-size:16px}.tabsnav a{padding:0 11px;font-size:15px}.langbtn{padding:2px 7px}}
.hbtns{display:flex;gap:8px;flex-wrap:wrap}
#getscratch{font-size:16px;padding:8px 18px;white-space:nowrap}
.head{display:flex;justify-content:space-between;gap:16px;align-items:flex-start;flex-wrap:wrap}
#install{display:inline-flex;align-items:center;gap:8px;font-size:16px;padding:8px 18px;white-space:nowrap}
#install[hidden]{display:none}
dialog{border:1px solid var(--line);border-radius:14px;max-width:min(520px,92vw);padding:20px 22px;font-family:var(--font);color:var(--ink)}
dialog::backdrop{background:rgba(20,30,50,.45)}
dialog h3{margin:0 0 8px;font-size:20px;color:var(--blue)}
dialog ul{margin:8px 0 14px;padding-inline-start:20px}
dialog li{margin:4px 0}
dialog .small{font-size:14px;color:var(--muted)}
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
.tools{position:sticky;top:56px;background:#fff;z-index:5;border-bottom:1px solid var(--line);padding:10px 0;display:flex;flex-direction:column;gap:10px}
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
[hidden]{display:none!important}
.vtools{margin:8px 0}
.vhint{margin:0;font-size:13px;color:var(--muted)}
.vgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;padding:10px 0 6px}
.vcard{border:1px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;background:#fff}
.vopen{display:block;position:relative;border:0;padding:0;margin:0;cursor:pointer;background:#1d2433;width:100%;aspect-ratio:16/9;text-decoration:none;overflow:hidden}
.vthumb{position:absolute;inset:0;display:grid;place-items:center;background:linear-gradient(135deg,#27324a,#1d2433)}
.vthumb img,.vthumb video{width:100%;height:100%;object-fit:cover;display:block}
.vthumb .vname{position:absolute;bottom:8px;inset-inline-start:10px;color:#e8edf8;font-size:13px;direction:ltr;opacity:.9}
.vplay{position:absolute;inset:0;margin:auto;width:54px;height:54px;border-radius:50%;background:rgba(232,134,28,.95);color:#fff;font-size:22px;display:grid;place-items:center;box-shadow:0 2px 10px rgba(0,0,0,.35);transition:transform .15s}
.vopen:hover .vplay,.vopen:focus-visible .vplay{transform:scale(1.12)}
.vplay.link{background:rgba(31,74,168,.95)}
.vinfo{padding:8px 12px 10px;display:flex;flex-direction:column;gap:3px;flex:1}
.vinfo h3{margin:0;font-size:16px;line-height:1.4}
.vinfo p{margin:0;font-size:13px;color:var(--muted)}
.vbadge{display:inline-block;font-size:12px;background:var(--soft);border:1px solid var(--line);border-radius:999px;padding:0 10px;align-self:flex-start}
.vdel{align-self:flex-start;font:inherit;font-size:13px;color:#a33;background:none;border:0;padding:0;cursor:pointer;text-decoration:underline}
.vdlg{width:min(960px,96vw);max-width:96vw;padding:12px 14px;border-radius:14px}
.vphead{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:8px}
.vphead h3{margin:0;font-size:19px;color:var(--ink)}
.vpbody{aspect-ratio:16/9;background:#000;border-radius:8px;overflow:hidden}
.vpbody iframe,.vpbody video{width:100%;height:100%;border:0;display:block}
.vpfoot{margin:8px 0 0;font-size:14px}
.srcsites{max-width:520px;grid-template-columns:repeat(3,1fr);margin:6px 0 12px}
.srctools{margin:6px 0}
.tgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;padding:10px 0}
.tcard{border:1px solid var(--line);border-radius:12px;padding:10px 12px;display:flex;flex-direction:column;gap:8px;background:#fff}
.tcard h3{margin:0;font-size:17px;display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.tcard h3 small{font-size:12px;color:var(--muted);direction:ltr;font-weight:400}
.tlinks{display:grid;grid-template-columns:1fr 1fr;gap:5px}
.tlinks .btn{font-size:13px;padding:4px 6px}
.tlinks .btn.vid{border-color:var(--orange);color:#a85a08}
.tlinks .btn.vid:hover{background:var(--orange);color:#fff}
.tnote{margin:6px 0 0;font-size:13px;color:var(--muted)}
.gamegrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px;padding:10px 0}
.gcat{margin:26px 0 4px;font-size:22px;color:var(--blue);border-bottom:2px solid var(--orange);padding-bottom:2px;display:inline-block}
.gcard{border:1px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;background:#fff}
.gcover{aspect-ratio:16/9;background:var(--soft);display:block;width:100%;object-fit:cover}
.gbody{padding:10px 14px 12px;display:flex;flex-direction:column;gap:6px;flex:1}
.gbody h3{margin:0;font-size:18px}
.gbody p{margin:0;font-size:14px;color:var(--muted)}
.gbody .btns{margin-top:auto}
.sr{position:absolute;left:-9999px}
:focus-visible{outline:3px solid var(--orange);outline-offset:2px}
@media (max-width:560px){.btns{grid-template-columns:1fr}}
</style>
</head>
<body>
<header class="topbar" id="top">
  <a class="brand" href="#stories">قصص سكراتش</a>
  <nav class="tabsnav" id="tabsnav" aria-label="القائمة الرئيسية">
    <a href="#stories" data-view="stories">القصص</a>
    <a href="#games" data-view="games">الألعاب</a>
  </nav>
  <div class="barbtns">
    <button type="button" class="langbtn" data-lang="ar" aria-label="العربية">AR</button>
    <button type="button" class="langbtn" data-lang="fr" aria-label="Français">FR</button>
  </div>
</header>
<section class="hero" id="hero"><div class="wrap">
  <div class="head"><h1>قصص سكراتش</h1>
  <div class="hbtns"><a class="btn alt" id="getscratch" href="https://scratch.mit.edu/download" target="_blank" rel="noopener">⬇ تحميل برنامج سكراتش</a>
  <a class="btn" href="https://scratch.mit.edu/projects/editor/" target="_blank" rel="noopener">فتح سكراتش على الإنترنت</a>
  <button type="button" class="btn main" id="install" hidden>⬇ اختصار على سطح المكتب</button></div></div>
  <p>كل ما تحتاجه لإنشاء مشروعك في صفحة واحدة: أوراق المشاريع، مشاريع جاهزة، أصوات، صور، أماكن وديكورات. لا حاجة إلى الإنترنت.</p>
</div></section>

<main class="wrap">
<div id="viewStories">
<section id="start">
  <h2>كيف أبدأ؟</h2>
  <p class="lead">أربع خطوات بسيطة.</p>
  <ol class="steps">
    <li>اختر قصة من القائمة أدناه.</li>
    <li>حمّل <b>ورقة المشروع</b> واقرأها: فيها الملخص والسيناريو وخطوات العمل.</li>
    <li>افتح <b>سكراتش</b> (<a href="https://scratch.mit.edu/download" target="_blank" rel="noopener">حمّله من هنا</a>) ثم «ملف ← تحميل من حاسوبك» واختر ملف المشروع (.sb3).</li>
    <li>غيّر الصور والأصوات والحوارات من <b>المكتبة</b> لتصنع مشروعك الخاص.</li>
  </ol>
</section>
<section id="stories">
  <h2>اختر قصتك</h2>
  <p class="lead">لكل قصة ورقة مشروع، ومشروع سكراتش جاهز، وحزمة واحدة تجمع كل ما تحتاجه.</p>
  <div class="stories" id="storyGrid"></div>
</section>
<details class="helpbox" id="help"><summary>مساعدة</summary>
  <div class="help">
    <div><h3>أضيف صورة جديدة</h3><ol><li>في سكراتش، اضغط على «اختيار لاعب» ثم «رفع لاعب».</li><li>اختر ملف الصورة (.svg) من المجلد.</li></ol></div>
    <div><h3>أضيف مكانًا (خلفية)</h3><ol><li>اضغط على «اختيار خلفية» ثم «رفع خلفية».</li><li>اختر ملفًا من «الأماكن».</li></ol></div>
    <div><h3>أضيف صوتًا</h3><ol><li>افتح لسان «الأصوات» في اللاعب.</li><li>اضغط «رفع صوت» واختر ملف (.wav).</li><li>استعمل الكتلة «ابدأ الصوت».</li></ol></div>
    <div><h3>أصنع حركة</h3><ol><li>حمّل «إطارات» الحركة من تبويب الصور المتحركة.</li><li>فك الضغط، ثم ارفع الصور كأزياء متتالية للاعب.</li><li>استعمل «التالي الزي» داخل حلقة مع «انتظر».</li></ol></div>
    <div><h3>أسجّل صوتي</h3><p>الأصوات الجاهزة المسمّاة «أصوات جاهزة» مولَّدة آليًا. لتسجيل صوتك، افتح لسان «الأصوات» في سكراتش واضغط على الميكروفون.</p></div>
  </div>

</details>
</div>
<div id="viewStory" hidden>
  <a class="back" href="#stories">← كل القصص</a>
  <section id="storyHead"></section>
<section id="library">
  <h2>الصور والأصوات والحركات</h2>
  <p class="lead">كل ما يخص هذه القصة. اضغط «تحميل» ثم أضف الملف في سكراتش.</p>
  <div class="tools">
    <div class="tabs" role="tablist" id="tabs"></div>
    <div class="row">
      <input type="search" id="q" placeholder="ابحث بالعربية أو بالفرنسية…" aria-label="بحث">
      <select id="story" hidden aria-label="تصفية حسب القصة"></select>
      <div class="subs" id="subs"></div>
    </div>
  </div>
  <div class="zipbar"><span id="count"></span><span id="zipwrap"></span></div>
  <div id="out"></div>
</section>
<section id="videos">
  <h2>فيديوهات</h2>
  <p class="lead">اضغط على لقطة الفيديو لمشاهدته هنا دون مغادرة الصفحة.</p>
  <div class="row vtools" id="vtools">
    <input type="search" id="vq" placeholder="ابحث في الفيديوهات…" aria-label="بحث في الفيديوهات">
    <select id="vstory" hidden aria-label="تصفية الفيديوهات حسب القصة"></select>
    <span id="vcount" class="small"></span>
  </div>
  <div class="vgrid" id="vgrid"></div>
</section>
<section id="sources">
  <h2>صور متحركة وفيديوهات جاهزة</h2>
  <p class="lead">مواقع مجانية فيها آلاف الصور والفيديوهات. اختر موضوعًا ليفتح لك البحث الجاهز في الموقع الذي تريده.</p>
  <div class="btns srcsites">
    <a class="btn main" href="https://www.pexels.com/fr-fr/" target="_blank" rel="noopener noreferrer">Pexels</a>
    <a class="btn main" href="https://mixkit.co/" target="_blank" rel="noopener noreferrer">Mixkit</a>
    <a class="btn main" href="https://pixabay.com/photos/" target="_blank" rel="noopener noreferrer">Pixabay</a>
  </div>
  <div class="row srctools">
    <input type="search" id="tq" placeholder="ابحث عن موضوع (غابة، بحر، قصر…)" aria-label="بحث عن موضوع">
    <select id="tstory" hidden aria-label="مواضيع حسب القصة"></select>
    <span id="tcount" class="small"></span>
  </div>
  <div class="tgrid" id="tgrid"></div>
  <p class="small tnote">الصور والفيديوهات تبقى في مواقعها الأصلية ولا تُنسخ في هذا المشروع. لكل موقع رخصته الخاصة، فاقرأ شروطه قبل التحميل، ولا تعد نشر الملفات كمكتبة مستقلة. نتائج البحث قد تتغير مع الوقت.</p>
</section>
</div>
<div id="viewGames" hidden>
<section id="games">
  <h2>ألعاب سكراتش</h2>
  <p class="lead">ألعاب بسيطة وتعليمية: أسئلة وأجوبة، حساب، ذاكرة، وسرعة. حمّل اللعبة وافتحها في سكراتش، ثم عدّلها كما تشاء.</p>
  <div id="gameGrid"></div>
  <div class="gamegrid" id="extGames"></div>
</section>
</div>
</main>
<dialog id="vplayer" aria-labelledby="vpTitle" class="vdlg">
  <div class="vphead"><h3 id="vpTitle"></h3><button type="button" class="btn" id="vpClose" aria-label="إغلاق">✕ إغلاق</button></div>
  <div class="vpbody" id="vpBody"></div>
  <p class="vpfoot"><a id="vpOpen" href="#" target="_blank" rel="noopener"></a></p>
</dialog>
<dialog id="installHelp" aria-labelledby="ihTitle">
  <h3 id="ihTitle">اختصار على سطح المكتب</h3>
  <div id="ihBody"></div>
  <form method="dialog"><button class="btn main" style="margin-top:10px">حسنًا</button></form>
</dialog>
<footer><div class="wrap"><span dir="ltr" style="display:block">__BUILD__</span>الصور مرسومة خصيصًا لهذه الورشة، والأصوات والموسيقى مولَّدة بالحاسوب، ويمكنك استعمالها وتعديلها بحرّية في مشاريعك.</div></footer>

<script src="videos.js"></script>
<script src="jeux.js"></script>
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

// ---- histoires : une carte par conte ; un clic ouvre le conte et tout ce qui le concerne
const GENERAL = {key:"__general", title:"موارد عامة", summary:"صور وأصوات وحركات تصلح لأي قصة.", morale:"", main:"#44506a", accent:"#8a94aa"};
const grid = $("#storyGrid");
DATA.stories.concat([GENERAL]).forEach(s => {
  const link = "#story-" + (s.key === "__general" ? "general" : s.key);
  grid.append(el("article",{class:"card"},
    el("div",{class:"bar",style:`background:${s.accent}`}),
    el("div",{class:"body"},
      el("h3",{text:s.title,style:`color:${s.main}`}),
      el("p",{text:s.summary}),
      s.morale && el("div",{class:"morale",text:s.morale}),
      el("div",{class:"btns"}, el("a",{class:"btn main wide",href:link,text:"فتح القصة وكل ما يخصها"})))));
});

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
  let items = DATA.assets.filter(a => a.cat===state.cat && (!state.sub || a.sub===state.sub) && (!state.story || (state.story === "__general" ? !a.tags.length : a.tags.includes(state.story))) && (!state.q || (a.label+" "+(a.fr||"")+" "+a.id).toLowerCase().includes(state.q)));
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

// ---- فيديوهات : مكتبة لقطات الشاشة، والمشاهدة داخل الصفحة (la vidéo reste chez son hébergeur)
const VOPT = Object.assign({autoThumbnails:true}, window.VIDEOS_OPTIONS||{});
function embedInfo(raw){
  raw = (raw||"").trim();
  const m = raw.match(/<iframe[^>]*\s+src=["']([^"']+)["']/i); if (m) raw = m[1];
  if (raw.startsWith("//")) raw = "https:" + raw;
  let u; try { u = new URL(raw); } catch(e){ return null; }
  if (!/^https?:$/.test(u.protocol)) return null;
  const h = u.hostname.replace(/^(www|m|music)\./,""), p = u.pathname, q = u.searchParams;
  const t = parseInt(q.get("t")||q.get("start")||"0",10) || 0;
  const yt = id => ({kind:"iframe", host:"YouTube", id, thumb:`https://i.ytimg.com/vi/${id}/hqdefault.jpg`, src:`https://www.youtube-nocookie.com/embed/${id}?rel=0${t?`&start=${t}`:""}`});
  if (h === "youtu.be") { const id = p.slice(1).split("/")[0]; return id ? yt(id) : null; }
  if (h === "youtube.com" || h === "youtube-nocookie.com") {
    if (p === "/watch" && q.get("v")) return yt(q.get("v"));
    const mm = p.match(/^\/(embed|shorts|live|v)\/([\w-]{6,})/); if (mm && mm[2] !== "videoseries") return yt(mm[2]);
    if ((p === "/playlist" || mm) && q.get("list")) return {kind:"iframe", host:"YouTube", src:`https://www.youtube-nocookie.com/embed/videoseries?list=${encodeURIComponent(q.get("list"))}`};
    return null;
  }
  if (h === "vimeo.com" || h === "player.vimeo.com") { const id = (p.match(/(\d{5,})/)||[])[1]; return id ? {kind:"iframe", host:"Vimeo", id, oembed:`https://vimeo.com/api/oembed.json?url=${encodeURIComponent("https://vimeo.com/"+id)}`, src:`https://player.vimeo.com/video/${id}`} : null; }
  if (h === "dailymotion.com" || h === "dai.ly") { const id = h === "dai.ly" ? p.slice(1) : (p.match(/\/video\/([a-z0-9]+)/i)||[])[1]; return id ? {kind:"iframe", host:"Dailymotion", id, api:`https://api.dailymotion.com/video/${id}?fields=thumbnail_480_url`, src:`https://www.dailymotion.com/embed/video/${id}`} : null; }
  if (h === "archive.org") { const id = (p.match(/^\/(?:details|embed)\/([^/]+)/)||[])[1]; return id ? {kind:"iframe", host:"Internet Archive", thumb:`https://archive.org/services/img/${id}`, src:`https://archive.org/embed/${id}`} : null; }
  if (h === "drive.google.com") { const id = (p.match(/\/file\/d\/([\w-]+)/)||[])[1] || q.get("id"); return id ? {kind:"iframe", host:"Google Drive", thumb:`https://drive.google.com/thumbnail?id=${id}&sz=w480`, src:`https://drive.google.com/file/d/${id}/preview`} : null; }
  if (h === "ted.com" || h === "embed.ted.com") { const mm = p.match(/\/talks\/([^/?]+)/); return mm ? {kind:"iframe", host:"TED", src:`https://embed.ted.com/talks/${mm[1]}`} : null; }
  if (h === "facebook.com" || h === "fb.watch") return {kind:"iframe", host:"Facebook", src:`https://www.facebook.com/plugins/video.php?href=${encodeURIComponent(u.href)}&show_text=false`};
  if (/\.(mp4|webm|ogv|ogg)$/i.test(p)) return {kind:"video", host:h, src:u.href};
  if (/\/embed\//i.test(p) || /^player\./.test(h)) return {kind:"iframe", host:h, src:u.href};
  return {kind:"link", host:h, src:u.href};
}
const TKEY = "ateliers-contes-thumbs";
const thumbCache = () => { try { return JSON.parse(localStorage.getItem(TKEY)||"{}"); } catch(e){ return {}; } };
const setThumbCache = (k,v) => { try { const c = thumbCache(); c[k] = v; localStorage.setItem(TKEY, JSON.stringify(c)); } catch(e){} };
const vsel = $("#vstory"), vq = $("#vq");
vsel.append(el("option",{value:"",text:"كل القصص"}));
DATA.stories.forEach(s => vsel.append(el("option",{value:s.key,text:s.title})));

// image de couverture : capture fournie > miniature du site > aperçu local > cadre neutre
async function remoteThumb(info){
  if (info.thumb) return info.thumb;
  const key = info.host + ":" + info.id, c = thumbCache(); if (c[key]) return c[key];
  try {
    let url = "";
    if (info.oembed) url = (await (await fetch(info.oembed)).json()).thumbnail_url;
    else if (info.api) url = (await (await fetch(info.api)).json()).thumbnail_480_url;
    if (url) { setThumbCache(key, url); return url; }
  } catch(e){}
  return "";
}
function coverFor(v, info, title){
  const box = el("div",{class:"vthumb"});
  const fallback = () => { box.classList.add("nocover"); box.querySelector("img,video")?.remove(); box.prepend(el("span",{class:"vname",text:info ? info.host : "فيديو"})); };
  if (v.image) { const i = el("img",{src:v.image,alt:title,loading:"lazy"}); i.addEventListener("error", fallback); box.append(i); }
  else if (info && info.kind === "video") box.append(el("video",{src:info.src+"#t=0.6",preload:"metadata",muted:"",playsinline:"","aria-hidden":"true"}));
  else if (info && VOPT.autoThumbnails) {
    remoteThumb(info).then(url => { if (!url) return fallback(); const i = el("img",{src:url,alt:title,loading:"lazy",referrerpolicy:"no-referrer"}); i.addEventListener("error", fallback); box.prepend(i); });
  } else fallback();
  return box;
}
const dlg2 = $("#vplayer");
function openPlayer(v, info, title){
  const body = $("#vpBody"); body.replaceChildren();
  $("#vpTitle").textContent = title;
  if (info.kind === "video") body.append(el("video",{src:info.src,controls:"",autoplay:"",playsinline:"","aria-label":title}));
  else body.append(el("iframe",{src:info.src,title,allow:"autoplay; fullscreen; picture-in-picture; encrypted-media",allowfullscreen:"",referrerpolicy:"strict-origin-when-cross-origin"}));
  const o = $("#vpOpen"); o.href = v.url; o.textContent = "فتح في الموقع الأصلي (" + info.host + ")";
  dlg2.showModal();
}
function closePlayer(){ if (dlg2.open) dlg2.close(); $("#vpBody").replaceChildren(); }
dlg2.addEventListener("close", () => $("#vpBody").replaceChildren());
dlg2.addEventListener("click", e => { if (e.target === dlg2) closePlayer(); });
$("#vpClose").addEventListener("click", closePlayer);

function renderVideos(){
  const g = $("#vgrid"); g.replaceChildren();
  const q = vq.value.trim().toLowerCase();
  const all = (window.VIDEOS||[]).filter(v => (!vsel.value || (vsel.value === "__general" ? !v.story : v.story === vsel.value)) && (!q || ((v.title||"")+" "+(v.note||"")).toLowerCase().includes(q)));
  $("#vcount").textContent = all.length ? `${all.length} فيديو` : "";
  $("#vtools").hidden = !(window.VIDEOS||[]).length;
  if (!all.length) { g.append(el("div",{class:"empty",text: (window.VIDEOS||[]).length ? "لا توجد فيديوهات مطابقة." : "لا توجد فيديوهات حاليًا."})); return; }
  all.forEach(v => {
    const info = embedInfo(v.url); const st = DATA.stories.find(s=>s.key===v.story);
    const title = v.title || (info ? info.host : "فيديو");
    const thumb = coverFor(v, info, title);
    const canPlay = info && info.kind !== "link";
    const trigger = canPlay ? el("button",{class:"vopen",type:"button","aria-label":"مشاهدة: "+title}, thumb, el("span",{class:"vplay",text:"▶"})) : el("a",{class:"vopen",href:v.url,target:"_blank",rel:"noopener","aria-label":"فتح: "+title}, thumb, el("span",{class:"vplay link",text:"↗"}));
    if (canPlay) trigger.addEventListener("click", () => openPlayer(v, info, title));
    const meta = el("div",{class:"vinfo"}, st && el("span",{class:"vbadge",text:st.title}), el("h3",{text:title}), v.note && el("p",{text:v.note}));
    g.append(el("article",{class:"vcard"}, trigger, meta));
  });
}
vsel.addEventListener("change", renderVideos); vq.addEventListener("input", renderVideos);
renderVideos();

// ---- مواضيع جاهزة : روابط بحث نحو Pexels و Mixkit و Pixabay (rien n'est copié ici)
const THEMES = [
 ["غابة","forest",["layla","crow","lion","hare","shepherd"]],["قصر","castle",["cinderella","frog"]],["بحر","sea waves",["sindbad"]],["سفينة","sailing ship",["sindbad"]],
 ["جزيرة","tropical island",["sindbad"]],["صحراء","desert",["alibaba","sindbad"]],["جبل","mountain",["alibaba"]],["كهف","cave",["alibaba"]],["كنز وذهب","gold coins treasure",["alibaba"]],
 ["ليل ونجوم","night sky stars",["cinderella"]],["ساعة","clock",["cinderella"]],["سحر ولمعان","magic sparkles",["cinderella"]],["حفلة ورقص","ball dance",["cinderella"]],
 ["حديقة","garden flowers",["frog","cinderella"]],["بئر","old well",["frog"]],["مزرعة","farm",["pigs","duckling","shepherd"]],["مرعى وتلال","green hills pasture",["shepherd"]],
 ["قرية","village",["djeha","shepherd"]],["سوق","market",["djeha","alibaba"]],["جسر ونهر","bridge river",["djeha"]],["بيت","house",["pigs","layla"]],
 ["مطر","rain",["duckling"]],["ثلج وشتاء","snow winter",["duckling"]],["ربيع","spring blossom",["duckling","hare"]],["نار","fire flames",["alibaba"]],["ريح","wind",["pigs"]],
 ["ذئب","wolf",["layla","pigs","shepherd"]],["أسد","lion",["lion"]],["فأر","mouse",["lion"]],["أرنب","rabbit hare",["hare"]],["سلحفاة","tortoise",["hare"]],
 ["ثعلب","fox",["crow"]],["غراب","crow bird",["crow"]],["ضفدع","frog",["frog"]],["بطة","duck",["duckling"]],["بجعة","swan",["duckling"]],["خروف وغنم","sheep",["shepherd"]],
 ["خنزير","pig",["pigs"]],["حمار","donkey",["djeha"]],["جمل","camel",["alibaba","sindbad"]],["حصان","horse",["cinderella"]],["فراشة","butterfly",[]],["عصفور","bird flying",[]],
 ["سباق","running race",["hare"]],["شجرة","tree",[]],["شمس وغيوم","sun clouds",[]],["أطفال يقرؤون","children reading",[]],["كتاب وقصص","storybook",[]]
];
const tsel = $("#tstory"), tq = $("#tq");
tsel.append(el("option",{value:"",text:"كل المواضيع"})); DATA.stories.forEach(s => tsel.append(el("option",{value:s.key,text:s.title})));
function themeLinks(q){
  const e = encodeURIComponent(q), d = e.replace(/%20/g,"-");
  return [
    ["Pexels صور", `https://www.pexels.com/search/${e}/`, ""], ["Pexels فيديو", `https://www.pexels.com/search/videos/${e}/`, "vid"],
    ["Pixabay صور", `https://pixabay.com/images/search/${e}/`, ""], ["Pixabay فيديو", `https://pixabay.com/videos/search/${e}/`, "vid"],
    ["Mixkit فيديو", `https://mixkit.co/free-stock-video/discover/${d}/`, "vid"]
  ];
}
function renderThemes(){
  const g = $("#tgrid"); g.replaceChildren();
  const q = tq.value.trim().toLowerCase();
  const items = THEMES.filter(t => (!tsel.value || tsel.value === "__general" || t[2].includes(tsel.value)) && (!q || (t[0]+" "+t[1]).toLowerCase().includes(q)));
  $("#tcount").textContent = items.length ? `${items.length} موضوع` : "";
  if (!items.length) { g.append(el("div",{class:"empty",text:"لا توجد مواضيع مطابقة."})); return; }
  items.forEach(t => g.append(el("article",{class:"tcard"}, el("h3",{}, el("span",{text:t[0]}), el("small",{text:t[1]})),
    el("div",{class:"tlinks"}, themeLinks(t[1]).map(([n,u,c]) => el("a",{class:"btn "+c,href:u,target:"_blank",rel:"noopener noreferrer",text:n}))))));
}
tsel.addEventListener("change", renderThemes); tq.addEventListener("input", renderThemes);
renderThemes();

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
if ("serviceWorker" in navigator && secure) {
  const had = !!navigator.serviceWorker.controller;
  navigator.serviceWorker.register("sw.js").catch(() => {});
  navigator.serviceWorker.addEventListener("controllerchange", () => { if (had && !sessionStorage.getItem("sw-reloaded")) { try { sessionStorage.setItem("sw-reloaded","1"); } catch(e){} location.reload(); } });
}
// ---- jeux
const GAME_CATS = ["quiz", "math", "memory", "order", "reflex", "catch"];
function renderGames(){
  const g = $("#gameGrid"); g.replaceChildren();
  GAME_CATS.forEach(cat => {
    const list = (DATA.games||[]).filter(x => x.cat === cat); if (!list.length) return;
    g.append(el("h3",{class:"gcat",text:list[0].cat_ar}));
    const row = el("div",{class:"gamegrid"});
    list.forEach(x => row.append(el("article",{class:"gcard"},
      el("img",{class:"gcover",src:x.cover,alt:x.title_ar,loading:"lazy"}),
      el("div",{class:"gbody"}, el("h3",{text:x.title_ar}), el("p",{text:x.how_ar}),
        el("div",{class:"btns"}, el("a",{class:"btn main",href:x.file,download:x.key+".sb3",text:"تحميل اللعبة (.sb3)"}))))));
    g.append(row);
  });
  // jeux Scratch publiés sur scratch.mit.edu (liste dans jeux.js) : joués ici, sans quitter la page
  const ext = $("#extGames"); ext.replaceChildren();
  (window.JEUX||[]).forEach(j => {
    const id = ((j.url||"").match(/projects\/(\d+)/)||[])[1]; if (!id) return;
    if (j.fr) FRMAP[j.title] = j.fr;
    const info = {kind:"iframe", host:"Scratch", src:`https://scratch.mit.edu/projects/${id}/embed`};
    const b = el("button",{class:"btn main",type:"button",text:"العب هنا"});
    b.addEventListener("click", () => openPlayer({url:`https://scratch.mit.edu/projects/${id}/`}, info, j.title));
    ext.append(el("article",{class:"gcard"}, el("div",{class:"gbody"}, el("h3",{text:j.title}), j.note && el("p",{text:j.note}),
      el("div",{class:"btns"}, b, el("a",{class:"btn",href:`https://scratch.mit.edu/projects/${id}/`,target:"_blank",rel:"noopener",text:"فتح في سكراتش"})))));
  });
}
renderGames();

// ---- vues : #stories (tous les contes), #story-<clé> (un conte et ses ressources), #games (jeux)
function renderStoryHead(key){
  const h = $("#storyHead"); h.replaceChildren();
  const s = key === "__general" ? GENERAL : DATA.stories.find(x => x.key === key); if (!s) return;
  const kids = [el("h2",{text:s.title,style:`color:${s.main}`}), el("p",{text:s.summary}), s.morale && el("div",{class:"morale",text:s.morale})];
  if (key !== "__general") kids.push(el("div",{class:"btns",style:"grid-template-columns:repeat(auto-fit,minmax(160px,1fr))"},
    el("a",{class:"btn main",href:s.docx,download:`ورقة ${s.title}.docx`,text:"ورقة المشروع (Word)"}),
    el("a",{class:"btn",href:s.doc,download:`ورقة ${s.title}.doc`,title:"للإصدارات القديمة من Word (2003 و2007)",text:"Word قديم (.doc)"}),
    el("a",{class:"btn",href:s.html,target:"_blank",rel:"noopener",text:"قراءة الورقة"}),
    el("a",{class:"btn",href:s.sb3,download:`${s.title}.sb3`,text:"مشروع سكراتش"}),
    el("a",{class:"btn",href:s.pack,download:`حزمة ${s.title}.zip`,text:"كل شيء (.zip)"})));
  h.append(el("div",{class:"storyhead"}, el("div",{class:"sbar",style:`background:${s.accent}`}), el("div",{class:"sbody"}, kids)));
}
function showStory(key){
  state.story = key; state.sub = ""; state.q = ""; $("#q").value = ""; vq.value = ""; tq.value = "";
  sel.value = vsel.value = tsel.value = key;
  const has = c => DATA.assets.some(a => a.cat === c && (key === "__general" ? !a.tags.length : a.tags.includes(key)));
  state.cat = (CATS.find(c => has(c.id)) || CATS[0]).id;
  renderStoryHead(key); render(); renderVideos(); renderThemes();
}
function route(){
  const h = decodeURIComponent(location.hash.replace(/^#/, ""));
  let view = "stories", key = null;
  if (h === "games") view = "games";
  else if (h.startsWith("story-")) { key = h.slice(6) === "general" ? "__general" : h.slice(6); if (key === "__general" || DATA.stories.some(s => s.key === key)) view = "story"; }
  $("#viewStories").hidden = view !== "stories"; $("#hero").hidden = view !== "stories";
  $("#viewStory").hidden = view !== "story"; $("#viewGames").hidden = view !== "games";
  if (view === "story") showStory(key);
  document.querySelectorAll("#tabsnav a").forEach(a => { if ((a.dataset.view === "games" && view === "games") || (a.dataset.view === "stories" && view !== "games")) a.setAttribute("aria-current","page"); else a.removeAttribute("aria-current"); });
  window.scrollTo(0, 0);
}
window.addEventListener("hashchange", route);
route();

// ---- اللغة : العربية / Français (traduction de tout le texte de la page)
const FRMAP = __FRMAP__, FRRULES = __FRRULES__.map(([a,b]) => [new RegExp(a), b]);
let LANG = "ar";
const origText = new WeakMap(), origAttr = new WeakMap(), origHTML = new WeakMap(), ATTRS = ["placeholder","aria-label","title","alt"];
function trStr(t){
  const k = t.trim(); if (!k) return null;
  if (FRMAP[k] !== undefined) return t.replace(k, FRMAP[k]);
  for (const [re, rep] of FRRULES) if (re.test(k)) return t.replace(k, k.replace(re, (...m) => rep.replace(/\$(\d)/g, (_, i) => FRMAP[m[+i]] !== undefined ? FRMAP[m[+i]] : m[+i])));
  return null;
}
function trElement(n){
  if (n.hasAttribute("data-fr")) { if (!origHTML.has(n)) origHTML.set(n, n.innerHTML); n.innerHTML = n.getAttribute("data-fr"); return false; }
  for (const a of ATTRS) { const v = n.getAttribute(a); if (v) { const r = trStr(v); if (r !== null && r !== v) { const o = origAttr.get(n) || {}; if (!(a in o)) o[a] = v; origAttr.set(n, o); n.setAttribute(a, r); } } }
  return true;
}
function walk(root, fn){
  const w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, { acceptNode(n){ if (n.nodeType === 1) { if (/^(SCRIPT|STYLE)$/.test(n.tagName) || n.hasAttribute("data-nofr")) return NodeFilter.FILTER_REJECT; return fn(n) === false ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT; } return NodeFilter.FILTER_ACCEPT; } });
  if (root.nodeType === 3) { fn(root); return; }
  if (root.nodeType === 1) { if (fn(root) === false) return; }
  let n; while ((n = w.nextNode())) if (n.nodeType === 3) fn(n);
}
function toFr(n){ if (n.nodeType === 3) { const r = trStr(n.nodeValue); if (r !== null && r !== n.nodeValue) { if (!origText.has(n)) origText.set(n, n.nodeValue); n.nodeValue = r; } return true; } return trElement(n); }
function toAr(n){
  if (n.nodeType === 3) { if (origText.has(n)) n.nodeValue = origText.get(n); return true; }
  if (origHTML.has(n)) { n.innerHTML = origHTML.get(n); origHTML.delete(n); return false; }
  const o = origAttr.get(n); if (o) { for (const a in o) n.setAttribute(a, o[a]); origAttr.delete(n); }
  return true;
}
const obs = new MutationObserver(ms => {
  obs.disconnect();
  for (const m of ms) { if (m.type === "childList") m.addedNodes.forEach(x => walk(x, toFr)); else if (m.type === "characterData") toFr(m.target); else if (m.type === "attributes") trElement(m.target); }
  startObs();
});
function startObs(){ obs.observe(document.body, {childList:true, subtree:true, characterData:true, attributes:true, attributeFilter:ATTRS}); }
function setLang(l){
  if (l === LANG && document.documentElement.lang === l) return;
  obs.disconnect(); LANG = l;
  document.documentElement.lang = l; document.documentElement.dir = l === "fr" ? "ltr" : "rtl";
  if (!document.documentElement.hasAttribute("data-ar-title")) document.documentElement.setAttribute("data-ar-title", document.title);
  if (l === "fr") { walk(document.body, toFr); document.title = FRMAP[document.documentElement.getAttribute("data-ar-title")] || document.title; startObs(); }
  else { walk(document.body, toAr); document.title = document.documentElement.getAttribute("data-ar-title"); }
  document.querySelectorAll(".langbtn").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.lang === l)));
  try { localStorage.setItem("ateliers-contes-lang", l); } catch(e){}
}
document.querySelectorAll(".langbtn").forEach(b => b.addEventListener("click", () => setLang(b.dataset.lang)));
let want = "ar";
try { want = new URLSearchParams(location.search).get("lang") || localStorage.getItem("ateliers-contes-lang") || "ar"; } catch(e){}
document.querySelectorAll(".langbtn").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.lang === "ar")));
if (want === "fr") setLang("fr");

</script>
</body>
</html>
'''
import datetime
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(TPL.replace("__DATA__", json.dumps(man, ensure_ascii=False)).replace("__FRMAP__", json.dumps(FR["map"], ensure_ascii=False)).replace("__FRRULES__", json.dumps(FR["rules"], ensure_ascii=False)).replace("__BUILD__", "نسخة " + datetime.date.today().isoformat()))
print("index.html", os.path.getsize(os.path.join(ROOT, "index.html")) // 1024, "Ko")
