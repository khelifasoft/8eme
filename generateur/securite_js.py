"""JavaScript de la page « Sécurité informatique » (8e) : #securite. Données : DATA.securite (securite.py)."""
JS = r'''
// ---- cours « Sécurité informatique » (8e) : #securite
const SEC = DATA.securite, SU = SEC.ui;
function secBox(){
  return el("section",{class:"cahierbox tmp"}, el("h3",{text:SU.box}), el("p",{class:"pnote",text:SU.boxn}), el("div",{class:"btns cahierbtns"}, el("a",{class:"btn main",href:"#securite",text:SU.open})));
}
function renderSecurite(){
  $("#axisBack").href = "#y8-env"; $("#axisBack").textContent = "← " + SU.back; park(); $("#resArea").replaceChildren();
  const mapT = el("div",{class:"mxwrap"}, el("table",{class:"thvocab"}, el("thead",{}, el("tr",{}, [SU.risk, SU.what, SU.protect].map(t => el("th",{text:t})))), el("tbody",{}, SEC.map.map(r => el("tr",{}, el("th",{text:r.r}), el("td",{text:r.w}), el("td",{text:r.p}))))));
  const sean = s => el("section",{class:"secseance"}, el("div",{class:"acthead"}, el("span",{class:"badge pj",text:s.n}), el("h3",{text:s.t})),
    el("p",{class:"pnote"}, el("b",{text:SU.obj}), " : ", s.obj),
    el("div",{class:"thcall thhook"}, el("b",{text:SU.cas}), " ", el("span",{text:s.cas})),
    el("h4",{text:SU.video}), el("div",{class:"secvid"}, el("video",{class:"v-ar",controls:"",preload:"none",src:s.video.ar}), el("video",{class:"v-fr",controls:"",preload:"none",src:s.video.fr})),
    el("h4",{text:SU.act}), el("p",{text:s.act}),
    el("p",{}, el("b",{text:SU.trace}), " : ", s.trace),
    el("details",{class:"step seanc"}, el("summary",{text:SU.plan}), el("table",{class:"sctable phases"}, el("thead",{}, el("tr",{}, el("th",{text:"المرحلة"}), el("th",{text:"المدة"}), el("th",{text:"الوصف"}))),
      el("tbody",{}, s.phases.map(p => el("tr",{}, el("td",{text:p.t}), el("td",{class:"n"}, p.min + " ", el("span",{text:"د"})), el("td",{text:p.d})))))),
    el("p",{class:"btns"}, el("a",{class:"btn main",href:s.fiche,target:"_blank",rel:"noopener",text:SU.fiche}), el("a",{class:"btn",href:"#planning-8",text:"تخطيط حصص سكراتش"})));
  $("#axisHead").replaceChildren(el("div",{class:"axhead secpage"}, el("span",{class:"lvl",text:CUR.years["8"].ar}), el("h2",{text:SU.title}), el("p",{class:"pnote",text:SU.intro}),
    el("h3",{text:SU.map}), mapT, SEC.seances.map(sean), el("p",{class:"pnote",text:SU.note})));
}
'''
JS += r'''
// ---- page « Programmation » de la 9e : objet programmable (micro:bit) et application mobile (App Inventor), à la place de Scratch
function renderNeuf(){
  const s = $("#neuf"), ex = DATA.planning.years["9"].extra || [];
  const group = (title, items) => [el("h2",{text:title}), items.map(x => el("section",{class:"secseance"}, el("div",{class:"acthead"}, el("span",{class:"badge pj",text:x.s}), el("h3",{text:x.t})),
    el("p",{class:"pnote"}, el("b",{text:"الهدف"}), " : ", x.obj),
    el("details",{class:"step seanc"}, el("summary",{text:"سير الحصة (تخطيط السنة التاسعة)"}), el("table",{class:"sctable phases"}, el("thead",{}, el("tr",{}, el("th",{text:"المرحلة"}), el("th",{text:"المدة"}), el("th",{text:"الوصف"}))),
      el("tbody",{}, x.phases.map(p => el("tr",{}, el("td",{text:p.t}), el("td",{class:"n"}, p.min + " ", el("span",{text:"د"})), el("td",{text:p.d})))))),
    el("p",{}, el("b",{text:"الأثر المكتوب"}), " : ", x.trace),
    el("p",{class:"btns"}, el("a",{class:"btn main",href:`cahier/cahier-9.html#s${x.s}`,target:"_blank",rel:"noopener",text:"مذكرة الدفتر لهذه الحصة"}), el("a",{class:"btn",href:"#planning-9",text:"تخطيط حصص سكراتش"}))))];
  s.replaceChildren(...[el("p",{class:"lead",text:"في السنة التاسعة تُبرمج أشياء حقيقية أو محاكاة وتُطوَّر تطبيقات هاتف بسيطة (المساعدة البيداغوجية 2026). لكل موضوع أربع حصص: من الاكتشاف إلى المشروع الصغير."}),
    group("الشيء القابل للبرمجة (micro:bit)", ex.filter(x => x.s[0] === "M")), group("تطبيقة الهاتف (App Inventor)", ex.filter(x => x.s[0] === "A"))].flat(Infinity));
}
'''
CSS = r'''
.secseance{border:1px solid var(--line);border-radius:14px;padding:6px 16px 12px;margin:16px 0;background:#fbfcff}.secseance h3{margin:4px 0}.secseance h4{margin:12px 0 4px;color:#1e3a6e}
.secvid video{width:100%;max-width:720px;border-radius:10px;background:#000;display:block}html[lang=fr] .v-ar,html:not([lang=fr]) .v-fr{display:none}
'''
