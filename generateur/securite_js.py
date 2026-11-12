"""JavaScript de la page « Sécurité informatique » (8e) : #securite. Données : DATA.securite (securite.py)."""
JS = r'''
// ---- cours « Sécurité informatique » (8e) : #securite
const SEC = DATA.securite, SU = SEC.ui;
function secBox(){
  return el("section",{class:"cahierbox tmp"}, el("h3",{text:SU.box}), el("p",{class:"pnote",text:SU.boxn}), el("div",{class:"btns cahierbtns"}, el("a",{class:"btn main",href:"#securite",text:SU.open})));
}
function secCards(){
  return el("div",{class:"gamegrid"}, SEC.seances.map(s => el("article",{class:"gcard"}, el("img",{class:"gcover",src:s.img[0],"data-fr-src":s.img[1],alt:s.t,loading:"lazy"}),
    el("div",{class:"gbody"}, el("h3",{text:s.t}), el("p",{text:s.obj}), el("div",{class:"btns"}, videoBtn(s.video, s.t), el("a",{class:"btn",href:"#securite-" + s.k,text:"بطاقة النشاط"}), el("a",{class:"btn",href:s.fiche,target:"_blank",rel:"noopener",text:"الموارد"}))))));
}
function renderSecurite(){
  $("#axisBack").href = "#y8-env"; $("#axisBack").textContent = "← " + SU.back; park(); $("#resArea").replaceChildren();
  const mapT = el("div",{class:"mxwrap"}, el("table",{class:"thvocab"}, el("thead",{}, el("tr",{}, [SU.risk, SU.what, SU.protect].map(t => el("th",{text:t})))), el("tbody",{}, SEC.map.map(r => el("tr",{}, el("th",{text:r.r}), el("td",{text:r.w}), el("td",{text:r.p}))))));
  const sean = s => el("section",{class:"secseance",id:"sec-" + s.k}, el("div",{class:"acthead"}, el("span",{class:"badge pj",text:s.n}), el("h3",{text:s.t})),
    el("p",{class:"pnote"}, el("b",{text:SU.obj}), " : ", s.obj),
    el("div",{class:"thcall thhook"}, el("b",{text:SU.cas}), " ", el("span",{text:s.cas})),
    el("h4",{text:SU.video}), el("div",{class:"secvid"}, el("video",{class:"v-ar",controls:"",preload:"none",src:s.video.ar}), el("video",{class:"v-fr",controls:"",preload:"none",src:s.video.fr})),
    el("h4",{text:SU.act}), el("p",{text:s.act}),
    el("p",{}, el("b",{text:SU.trace}), " : ", s.trace),
    el("details",{class:"step seanc"}, el("summary",{text:SU.plan}), el("table",{class:"sctable phases"}, el("thead",{}, el("tr",{}, el("th",{text:"المرحلة"}), el("th",{text:"المدة"}), el("th",{text:"الوصف"}))),
      el("tbody",{}, s.phases.map(p => el("tr",{}, el("td",{text:p.t}), el("td",{class:"n"}, p.min + " ", el("span",{text:"د"})), el("td",{text:p.d})))))),
    el("p",{class:"btns"}, el("a",{class:"btn main",href:s.fiche,target:"_blank",rel:"noopener",text:SU.fiche}), el("a",{class:"btn",href:"#planning-8",text:"تخطيط حصص سكراتش"})));
  $("#axisHead").replaceChildren(el("div",{class:"axhead secpage"}, el("span",{class:"lvl",text:CUR.years["8"].ar}), el("h2",{text:SU.title}), el("p",{class:"pnote",text:SU.intro}),
    secCards(), el("h3",{text:SU.map}), mapT, SEC.seances.map(sean), el("p",{class:"pnote",text:SU.note})));
  syncImgs();
}
'''
JS += r'''
// ---- page « Programmation » de la 9e : objet programmable (micro:bit) et application mobile (App Inventor), à la place de Scratch
function objBlock(k){
  const O = DATA.objets, u = O.ui, a = O.items[k]; if (!a) return null;
  const playBtn = el("button",{type:"button",class:"btn main",text:u.play});
  playBtn.addEventListener("click", () => { const v = document.documentElement.lang === "fr" ? a.video.fr : a.video.ar; openPlayer({url:v}, {kind:"video", host:"", src:v}, a.t); $("#vpOpen").href = v; $("#vpOpen").textContent = "فتح الفيديو في نافذة جديدة"; });
  return el("div",{class:"objblock"}, el("h4",{text:u.act}), el("p",{}, el("b",{text:a.t})), el("ol",{class:"bigsteps"}, a.steps.map(t => el("li",{text:t}))), el("p",{class:"tip"}, el("b",{text:u.res}), " : ", a.res),
    el("h4",{text:u.shot}), el("figure",{class:"objshot"}, el("img",{src:a.img[0],"data-fr-src":a.img[1],alt:a.t,loading:"lazy"})),
    el("p",{}, playBtn),
    el("h4",{text:u.files}), el("p",{class:"pnote",text:k[0] === "M" ? u.inzip_m : u.inzip_a}), el("p",{}, el("a",{class:"btn main",href:a.zip,download:k + ".zip",text:u.zip})));
}
function videoBtn(src, title){
  const b = el("button",{type:"button",class:"btn main",text:"شاهد الفيديو"});
  b.addEventListener("click", () => { const v = document.documentElement.lang === "fr" ? src.fr : src.ar; openPlayer({url:v}, {kind:"video", host:"", src:v}, title); $("#vpOpen").href = v; $("#vpOpen").textContent = "فتح الفيديو في نافذة جديدة"; });
  return b;
}
function objCard(k){
  const a = DATA.objets.items[k], x = DATA.planning.years["9"].extra.find(q => q.s === k);
  return el("article",{class:"gcard"}, el("img",{class:"gcover",src:a.img[0],"data-fr-src":a.img[1],alt:a.t,loading:"lazy"}),
    el("div",{class:"gbody"}, el("h3",{text:x.t}), el("p",{text:x.obj}), el("div",{class:"btns"}, videoBtn(a.video, x.t), el("a",{class:"btn",href:"#objet-" + k,text:"بطاقة النشاط"}), el("a",{class:"btn",href:a.zip,download:k + ".zip",text:"الموارد"}))));
}
function renderNeuf(){
  const s = $("#neuf"), ex = DATA.planning.years["9"].extra || [];
  const group = (title, items) => [el("h2",{text:title}), el("div",{class:"gamegrid"}, items.map(x => objCard(x.s)))];
  s.replaceChildren(...[el("p",{class:"lead",text:"في السنة التاسعة تُبرمج أشياء حقيقية أو محاكاة وتُطوَّر تطبيقات هاتف بسيطة (المساعدة البيداغوجية 2026). لكل موضوع أربع حصص: من الاكتشاف إلى المشروع الصغير."}),
    group("الشيء القابل للبرمجة (micro:bit)", ex.filter(x => x.s[0] === "M")), group("تطبيقة الهاتف (App Inventor)", ex.filter(x => x.s[0] === "A")), el("p",{class:"pnote",text:DATA.objets.ui.note})].flat(Infinity));
  syncImgs();
}
// fiche d'activité détaillée d'une séance micro:bit / App Inventor : #objet-M1 ... #objet-A4
function renderObjet(k){
  const a = DATA.objets.items[k], x = DATA.planning.years["9"].extra.find(q => q.s === k), u = DATA.objets.ui; if (!a || !x) return;
  $("#axisBack").href = "#y9-prog"; $("#axisBack").textContent = "← " + CUR.years["9"].ar; park(); $("#resArea").replaceChildren();
  $("#axisHead").replaceChildren(el("div",{class:"axhead secpage"}, el("span",{class:"lvl",text:CUR.years["9"].ar}), el("h2",{text:x.t}), el("p",{class:"pnote"}, el("b",{text:"الهدف"}), " : ", x.obj),
    el("figure",{class:"objshot"}, el("img",{src:a.img[0],"data-fr-src":a.img[1],alt:a.t})),
    el("h3",{text:a.t}), el("ol",{class:"bigsteps"}, a.steps.map(t => el("li",{text:t}))), el("p",{class:"tip"}, el("b",{text:u.res}), " : ", a.res),
    el("p",{class:"btns"}, videoBtn(a.video, x.t), el("a",{class:"btn",href:a.zip,download:k + ".zip",text:u.zip}), el("a",{class:"btn",href:`cahier/cahier-9.html#s${k}`,target:"_blank",rel:"noopener",text:"مذكرة الدفتر لهذه الحصة"})),
    el("p",{class:"pnote",text:k[0] === "M" ? u.inzip_m : u.inzip_a}),
    el("h3",{text:"سير الحصة (تخطيط السنة التاسعة)"}), el("table",{class:"sctable phases"}, el("thead",{}, el("tr",{}, el("th",{text:"المرحلة"}), el("th",{text:"المدة"}), el("th",{text:"الوصف"}))),
      el("tbody",{}, x.phases.map(p => el("tr",{}, el("td",{text:p.t}), el("td",{class:"n"}, p.min + " ", el("span",{text:"د"})), el("td",{text:p.d}))))),
    el("p",{}, el("b",{text:"الأثر المكتوب"}), " : ", x.trace), el("p",{class:"pnote",text:u.note})));
  syncImgs();
}
'''
JS += r'''
// ---- activités Scratch (8e) : « Construis le script » façon code.org — on place les blocs dans l'ordre, puis « Démarrer »
const PZ = {};
function actPuzzle(a){
  const toks = a.tok, n = toks.length, T = a.tok.map((t, i) => Object.assign({id:i}, t));
  const box = el("section",{class:"pz"}, el("h3",{text:"جرّب: ركّب السكربت"}), el("p",{class:"pnote",text:"اضغط على الكتل لوضعها في مساحة العمل بالترتيب الصحيح ثم على «ابدأ»."}));
  const pal = el("div",{class:"pzpal"}), ws = el("div",{class:"pzws"}), msg = el("p",{class:"thfb"}), out = el("div",{class:"pzout"});
  let mine = [], order = []; const reset = () => { mine = []; order = thShuffle(T.map(t => t.id)); out.replaceChildren(); msg.replaceChildren(); msg.className = "thfb"; draw(); };
  const chip = (t, extra) => el("button",{type:"button",class:"blk " + t.c + " pzb" + (extra || ""),text:t.t});
  function draw(hint){
    pal.replaceChildren(...order.filter(i => !mine.includes(i)).map(i => { const b = chip(T[i]); if (hint === i) b.classList.add("hint"); b.addEventListener("click", () => { mine.push(i); msg.replaceChildren(); draw(); }); return b; }));
    ws.replaceChildren(...mine.map((i, k) => { const b = chip(T[i]); b.addEventListener("click", () => { mine.splice(k, 1); msg.replaceChildren(); draw(); }); return b; }));
    if (!mine.length) ws.append(el("span",{class:"pnote",text:"مساحة العمل"}));
  }
  const go = el("button",{type:"button",class:"btn main",text:"ابدأ"}), again = el("button",{type:"button",class:"btn",text:"أعد البداية"}), tip = el("button",{type:"button",class:"btn",text:"تلميح"});
  tip.addEventListener("click", () => { let k = 0; while (k < mine.length && T[mine[k]].t === T[k].t) k++; draw(k < n ? order.find(i => !mine.includes(i) && T[i].t === T[k].t) : undefined); });
  again.addEventListener("click", reset);
  go.addEventListener("click", () => {
    let ok = 0; while (ok < mine.length && T[mine[ok]].t === T[ok].t) ok++;
    if (mine.length === n && ok === n) {
      msg.className = "thfb ok"; msg.replaceChildren(el("b",{text:"أحسنت! السكربت يعمل: شاهد النتيجة."}));
      const sc = el("div",{class:"pznest"}, T.map(t => el("div",{class:"pznb",style:"margin-inline-start:" + (t.d * 22) + "px"}, chip(t))));
      out.replaceChildren(sc, el("div",{class:"pzanim"}, thImg(a.img.avant, a.t), thImg(a.img.apres, a.t)));
      syncImgs(); if (!Done.has(a.n)) Done.toggle(a.n); updateProgress();
    } else {
      msg.className = "thfb ko"; out.replaceChildren();
      const why = mine.length === 0 ? "" : mine.length < n && ok === mine.length ? "تنقصك كتل." : mine.length > n ? "توجد كتلة زائدة." : "";
      msg.replaceChildren(el("b",{text:"ليس بعد: "}), ok + " ", el("span",{text:"كتل في مكانها الصحيح في البداية"}), why ? [" · ", el("span",{text:why})] : null, mine.length === 0 || T[mine[0]].t !== T[0].t ? [" · ", el("span",{text:"ضع أولا كتلة الحدث (القبعة)."})] : null);
    }
  });
  box.append(el("div",{class:"pzcols"}, el("div",{}, el("h5",{text:"الكتل"}), pal), el("div",{}, el("h5",{text:"مساحة العمل"}), ws)), el("div",{class:"btns pzbtns"}, go, tip, again), msg, out);
  reset(); return box;
}
'''
CSS = r'''
.pz{border:2px solid #1e4fa8;border-radius:14px;padding:6px 16px 12px;margin:14px 0;background:#f7faff}.pzcols{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media(max-width:640px){.pzcols{grid-template-columns:1fr}}.pzpal,.pzws{min-height:120px;border:1.5px dashed #9aa5b8;border-radius:10px;padding:8px;display:flex;flex-direction:column;align-items:flex-start;gap:4px;background:#fff}.pzws{border-style:solid;border-color:#3f7ee0}.pzb{border:0;cursor:pointer;font:inherit;font-size:14px;text-align:start}.pzb.hint{outline:3px solid #ffd43b}.pznb{display:block}.pzout{margin-top:8px}.pzanim{position:relative;max-width:420px;margin-top:8px}.pzanim img{width:100%;display:block;border:1px solid var(--line);border-radius:8px}.pzanim img:last-child{position:absolute;inset:0;animation:pzfade 3s ease-in-out infinite alternate}@keyframes pzfade{0%,30%{opacity:0}70%,100%{opacity:1}}
.objshot{margin:6px 0;max-width:720px}.objshot img{width:100%;height:auto;display:block;border:1px solid var(--line);border-radius:10px}
.secseance{border:1px solid var(--line);border-radius:14px;padding:6px 16px 12px;margin:16px 0;background:#fbfcff}.secseance h3{margin:4px 0}.secseance h4{margin:12px 0 4px;color:#1e3a6e}
.secvid video{width:100%;max-width:720px;border-radius:10px;background:#000;display:block}html[lang=fr] .v-ar,html:not([lang=fr]) .v-fr{display:none}
'''
