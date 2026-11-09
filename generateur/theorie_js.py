"""JavaScript et CSS de la rubrique « Théorie Scratch », insérés dans index.html par page.py (repères __THEORIE_JS__ et __THEORIE_CSS__).
Les textes viennent tous de DATA.theorie (theorie.py) : U.xxx = textes de l'interface, en arabe (la page les retraduit en français avec son dictionnaire).
Les éléments sont toujours recréés (jamais modifiés sur place) pour que la traduction automatique suive : voir trStr / MutationObserver dans page.py."""

JS = r'''
// ---- Théorie Scratch (7e) : leçons, activités interactives, progression « Fait »
const TH = DATA.theorie, U = TH.ui;
const TH_KEY = "scratch-theorie-faites", TH_SCORE = "scratch-theorie-scores";
const ThDone = (() => {
  let mem = [], sc = {};
  try { const v = JSON.parse(localStorage.getItem(TH_KEY) || "[]"); if (Array.isArray(v)) mem = v; } catch (e) {}
  try { const v = JSON.parse(localStorage.getItem(TH_SCORE) || "{}"); if (v && typeof v === "object") sc = v; } catch (e) {}
  const save = () => { try { localStorage.setItem(TH_KEY, JSON.stringify(mem)); localStorage.setItem(TH_SCORE, JSON.stringify(sc)); } catch (e) {} };
  return { has: n => mem.includes(n), count: () => mem.length, score: n => sc[n],
           toggle(n){ const i = mem.indexOf(n); if (i >= 0) mem.splice(i, 1); else mem.push(n); save(); return i < 0; },
           setScore(n, v){ if (!(sc[n] >= v)) { sc[n] = v; save(); } }, reset(){ mem = []; sc = {}; save(); } };
})();
function updateTheoryProgress(){
  const total = TH.total, n = ThDone.count();
  document.querySelectorAll("[data-th-prog]").forEach(e => { const t = n + " / " + total; if (e.textContent !== t) e.textContent = t; });
  document.querySelectorAll(".thbar > i").forEach(e => { e.style.width = (100 * n / total) + "%"; });
  document.querySelectorAll("[data-th]").forEach(e => { const d = ThDone.has(+e.dataset.th); e.classList.toggle("is-done", d); const cb = e.querySelector("input.actcb"); if (cb) cb.checked = d; });
  document.querySelectorAll("button.thdone").forEach(b => { const d = ThDone.has(+b.dataset.n); b.setAttribute("aria-pressed", String(d)); const t = d ? U.done : U.markDone; if (b.dataset.t !== t) { b.textContent = t; b.dataset.t = t; } });
  document.querySelectorAll("[data-th-score]").forEach(e => { const s = ThDone.score(+e.dataset.thScore); e.hidden = s === undefined; if (s !== undefined) { const t = s + " / 5"; if (e.querySelector(".num") && e.querySelector(".num").textContent !== t) e.querySelector(".num").textContent = t; } });
}
const THFAM = {ev:"#c78a00", mv:"#3f7ee0", lk:"#8a55d7", sn:"#b448b0", ct:"#d68a00", se:"#2a9fc9", op:"#3fa854", va:"#e0592a", pen:"#0f9e7a", my:"#e0506b"};
const thShuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const thURI = s => "data:image/svg+xml;charset=utf-8," + encodeURIComponent(s);
const thArt = {cat: thURI(TH.sprites.cat), apple: thURI(TH.sprites.apple)};
const thNum = v => { v = Math.round(v); return String(v === 0 ? 0 : v).replace("-", "−"); };
function thImg(pair, alt){ return el("img",{src:pair[1],"data-fr-src":pair[0],alt,loading:"lazy"}); }
// pastille d'un bloc : couleur = famille ; « chapeau » arrondi en haut ; condition = hexagone
function blkChip(n, extra){
  const kids = [];
  if (n.cond) { kids.push(el("span",{text:n.pre}), " ", el("span",{class:"hex",text:n.cond.t}), " ", el("span",{text:n.post})); if (n.els) kids.push(" … ", el("span",{text:n.else_t})); }
  else kids.push(n.t);
  return el("span",{class:"blk " + n.c + (n.hat ? " hat" : "") + (extra ? " " + extra : "")}, kids);
}
function thMark(n){
  const cb = el("input",{type:"checkbox",class:"actcb","aria-label":U.doneShort}); cb.checked = ThDone.has(n); cb.addEventListener("change", () => { ThDone.toggle(n); updateTheoryProgress(); });
  return el("label",{class:"actdone"}, cb, el("span",{text:U.doneShort}));
}
function thCard(L){
  return el("div",{class:"actcard thcard","data-th":L.n,style:"border-top-color:" + L.color},
    el("a",{class:"actlink",href:"#cours-" + L.n,title:L.t}, el("div",{class:"actthumb"}, thImg(L.img, L.t), el("span",{class:"badge pj",text:L.n})), el("h4",{text:L.t}),
      el("p",{class:"thmeta"}, el("span",{class:"chip",text:"ح" + L.seance}), " ", el("span",{class:"pnote"}, "≈ " + L.min + " ", el("span",{text:U.min})))),
    thMark(L.n));
}
function thProgress(){ return el("div",{class:"actprog"}, el("b",{text:U.progress}), el("span",{class:"allprog","data-th-prog":""}), el("div",{class:"actbar thbar"}, el("i",{}))); }
// rubrique affichée sur la page 7e (avant les contes)
function renderTheorySection(){
  const s = $("#theory");
  s.replaceChildren(el("h2",{text:U.hubTitle}), el("p",{class:"lead",text:U.hubIntro}), thProgress(), el("div",{class:"actgrid thgrid"}, TH.lessons.map(thCard)),
    el("p",{}, el("a",{class:"btn main",href:"#theorie",text:U.openAll}), " ", el("a",{class:"btn",href:"#planning-7",text:U.seePlanning})));
  syncImgs(); updateTheoryProgress();
}
function glossTable(){
  const th = (t, nofr) => el("th",nofr ? {"data-nofr":""} : {}, t);
  return el("div",{class:"mxwrap"}, el("table",{class:"thvocab"}, el("thead",{}, el("tr",{}, th("العربية", 1), th("Français", 1), th("English", 1), th(U.meaning))),
    el("tbody",{}, TH.glossary.map(g => el("tr",{}, el("td",{"data-nofr":"",dir:"rtl",lang:"ar",text:g.ar}), el("td",{"data-nofr":"",dir:"ltr",text:g.fr}), el("td",{"data-nofr":"",dir:"ltr",text:g.en}), el("td",{text:g.d}))))));
}
function renderTheoryHub(){
  $("#axisBack").href = "#y7-prog"; $("#axisBack").textContent = "← " + CUR.years["7"].ar; park(); $("#resArea").replaceChildren();
  const prn = el("button",{type:"button",class:"btn main",text:U.printMemo});
  prn.addEventListener("click", () => { document.body.classList.add("print-memo"); const off = () => { document.body.classList.remove("print-memo"); window.removeEventListener("afterprint", off); }; window.addEventListener("afterprint", off); window.print(); });
  const reset = el("button",{type:"button",class:"btn",text:U.reset});
  reset.addEventListener("click", () => { if (confirm(document.documentElement.lang === "fr" ? "Effacer toute ta progression ?" : "هل تريد مسح كل تقدّمك؟")) { ThDone.reset(); updateTheoryProgress(); } });
  const memo = el("div",{class:"memo"}, el("h3",{text:U.memoTitle}),
    el("div",{class:"memotop"}, el("div",{class:"memofig"}, thImg(TH.memoImg, U.memoTitle)), el("div",{}, el("h4",{text:U.rulesTitle}), el("ol",{class:"thrules"}, TH.rules.map(r => el("li",{text:r}))))),
    el("h4",{text:U.words}), glossTable());
  $("#axisHead").replaceChildren(el("div",{class:"axhead thpage"}, el("span",{class:"lvl",text:CUR.years["7"].ar}), el("h2",{text:U.hubTitle}), el("p",{class:"pnote",text:U.hubIntro}),
    thProgress(), el("p",{class:"pnote",text:U.saved}), el("div",{class:"thgrid actgrid"}, TH.lessons.map(thCard)),
    el("p",{class:"btns thtools"}, prn, el("a",{class:"btn",href:"#planning-7",text:U.seePlanning}), el("a",{class:"btn",href:"#activites",text:U.moreActs}), reset), memo));
  syncImgs(); updateTheoryProgress();
}

// ---- une leçon
function renderLesson(n){
  const L = TH.lessons.find(x => x.n === n); if (!L) return;
  const prev = TH.lessons.find(x => x.n === n - 1), next = TH.lessons.find(x => x.n === n + 1);
  $("#axisBack").href = "#theorie"; $("#axisBack").textContent = "← " + U.hubTitle; park(); $("#resArea").replaceChildren();
  const mkDone = () => { const x = el("button",{type:"button",class:"btn donebtn thdone","data-n":L.n,"aria-pressed":"false"}); x.addEventListener("click", () => { ThDone.toggle(L.n); updateTheoryProgress(); }); return x; };
  const callout = (cls, title, text) => el("div",{class:"thcall " + cls}, el("b",{text:title}), " ", el("span",{text}));
  const list = (items, cls) => el("ul",{class:cls || ""}, items.map(t => el("li",{text:t})));
  const bestScore = el("span",{class:"thscore pnote","data-th-score":L.n,hidden:""}, el("b",{text:U.bestScore}), " ", el("span",{class:"num"}));
  const quizBox = el("section",{class:"thw thw-quiz final"});
  wQuiz({qs:L.quiz}, quizBox, s => { ThDone.setScore(L.n, s); updateTheoryProgress(); });
  const actCards = L.acts.map(k => DATA.activites.acts.find(a => a.n === k)).filter(Boolean);
  $("#axisHead").replaceChildren(el("div",{class:"axhead thpage thlesson"},
    el("div",{class:"acthead"}, el("span",{class:"badge pj",text:L.n}), el("span",{class:"lvlf"}, el("span",{text:U.lesson}), " " + L.n + " / " + TH.total), mkDone()),
    el("h2",{text:L.t}),
    el("p",{class:"thmeta2 pnote"}, el("b",{text:U.seanceLinked}), " : ", el("a",{class:"chip",href:"#planning-7",text:"ح" + L.seance}), "  ≈ " + L.min + " ", el("span",{text:U.min}), "  ", bestScore),
    el("p",{class:"pnote"}, el("b",{text:U.objective}), " : ", L.obj),
    callout("thhook", U.hook, L.hook), callout("thlife", U.life, L.life), L.recall ? el("p",{class:"threcall"}, L.recall) : null,
    el("h3",{text:U.essential}), el("div",{class:"thidea"}, L.idea.map(t => el("p",{text:t}))),
    L.fig.length ? [el("h3",{text:U.figures}), el("div",{class:"thfigs"}, L.fig.map(f => el("figure",{}, thImg(f.img, f.cap), el("figcaption",{text:f.cap}))))] : null,
    L.widgets.length ? [el("h3",{text:U.activities}), L.widgets.map(buildWidget)] : null,
    el("h3",{text:U.vocab}), el("div",{class:"mxwrap"}, el("table",{class:"thvocab"}, el("thead",{}, el("tr",{}, ["العربية", "Français", "English"].map(t => el("th",{"data-nofr":"",text:t})))),
      el("tbody",{}, L.vocab.map(v => el("tr",{}, el("td",{"data-nofr":"",dir:"rtl",lang:"ar",text:v[0]}), el("td",{"data-nofr":"",dir:"ltr",text:v[1]}), el("td",{"data-nofr":"",dir:"ltr",text:v[2]})))))),
    el("h3",{text:U.mistakes}), list(L.mistakes, "thmist"), el("h3",{text:U.retain}), list(L.retain, "check"),
    el("h3",{text:U.testYou}), quizBox,
    el("h3",{text:U.practice}), el("p",{class:"defi"}, el("b",{text:U.challenge}), " : ", L.defi),
    actCards.length ? el("div",{class:"actgrid mini"}, actCards.map(actCard)) : null,
    el("div",{class:"btns actnav"}, mkDone(), prev ? el("a",{class:"btn",href:"#cours-" + prev.n,text:U.prevLesson}) : null, el("a",{class:"btn main",href:"#theorie",text:U.allLessons}), next ? el("a",{class:"btn",href:"#cours-" + next.n,text:U.nextLesson}) : null)));
  syncImgs(); updateProgress();
}
function buildWidget(w){
  const box = el("section",{class:"thw thw-" + w.k}, el("h4",{text:w.t}), el("p",{class:"pnote",text:w.p}));
  ({order: wOrder, trace: wTrace, iface: wIface, coord: wCoord, quiz: wQuiz})[w.k](w, box);
  return box;
}

// ---- QCM corrigé automatiquement (les réponses sont mélangées à chaque essai)
function wQuiz(w, box, onScore){
  const qs = w.qs, list = el("div",{class:"thq"}), res = el("div",{class:"thres"});
  let score = 0, answered = 0;
  function build(){
    score = 0; answered = 0; res.replaceChildren(); res.hidden = true;
    list.replaceChildren(...qs.map((q, qi) => {
      const opts = el("div",{class:"thopts"}), fb = el("p",{class:"thfb"}), card = el("div",{class:"thqq"});
      card.append(...[el("p",{class:"thqt"}, el("b",{class:"num",text:(qi + 1) + "."}), " ", q.q), q.blk ? el("div",{class:"thstem scr"}, (Array.isArray(q.blk) ? q.blk : [q.blk]).map(x => blkChip(x))) : null, opts, fb].filter(Boolean));
      const byIdx = {};
      thShuffle(q.o.map((_, i) => i)).forEach(i => {
        const o = q.o[i], b = el("button",{type:"button",class:"thopt"}, typeof o === "string" ? o : blkChip(o)); byIdx[i] = b;
        b.addEventListener("click", () => {
          if (card.dataset.done) return; card.dataset.done = "1"; answered++;
          const ok = i === q.a; if (ok) score++;
          [...opts.children].forEach(x => x.disabled = true);
          b.classList.add(ok ? "ok" : "ko"); if (!ok) byIdx[q.a].classList.add("ok");
          fb.replaceChildren(...[el("b",{text:ok ? U.bravo : U.notYet}), q.why ? " " : null, q.why || null].filter(Boolean)); fb.className = "thfb " + (ok ? "ok" : "ko");
          if (answered === qs.length) finish();
        });
        opts.append(b);
      });
      return card;
    }));
  }
  function finish(){
    const k = qs.length, msg = score === k ? U.perfect : score >= k - 1 ? U.good : U.again, again = el("button",{type:"button",class:"btn",text:U.retry});
    again.addEventListener("click", build);
    res.replaceChildren(el("b",{text:U.score}), " ", el("span",{class:"num big",text:score + " / " + k}), el("p",{text:msg}), again); res.hidden = false;
    if (onScore) onScore(score);
  }
  build(); box.append(list, res);
}

// ---- remettre dans l'ordre (flèches haut / bas)
function wOrder(w, box){
  const n = w.items.length; let cur = [];
  const list = el("ol",{class:"thord"}), msg = el("p",{class:"thfb"});
  const mix = () => { do { cur = thShuffle([...Array(n).keys()]); } while (cur.every((v, i) => v === i)); };
  function draw(marks){
    list.replaceChildren(...cur.map((idx, pos) => {
      const it = w.items[idx], up = el("button",{type:"button",class:"thmv","aria-label":U.up,text:"▲"}), dn = el("button",{type:"button",class:"thmv","aria-label":U.down,text:"▼"});
      up.disabled = pos === 0; dn.disabled = pos === n - 1;
      up.addEventListener("click", () => { [cur[pos - 1], cur[pos]] = [cur[pos], cur[pos - 1]]; msg.replaceChildren(); draw(); });
      dn.addEventListener("click", () => { [cur[pos + 1], cur[pos]] = [cur[pos], cur[pos + 1]]; msg.replaceChildren(); draw(); });
      return el("li",{class:"thit" + (marks ? (marks[pos] ? " ok" : " ko") : "")}, el("span",{class:"thctrl"}, up, dn), it.c ? blkChip(it) : el("span",{class:"thtxt",text:it.t}));
    }));
  }
  const chk = el("button",{type:"button",class:"btn main",text:U.check}), shf = el("button",{type:"button",class:"btn",text:U.shuffle});
  chk.addEventListener("click", () => {
    const marks = cur.map((idx, pos) => idx === pos), good = marks.filter(Boolean).length; draw(marks);
    msg.className = "thfb " + (good === n ? "ok" : "ko");
    msg.replaceChildren(...(good === n ? [el("b",{text:U.bravo})] : [el("b",{text:U.notYet}), " ", el("span",{class:"num",text:good + " / " + n}), " ", el("span",{text:U.wellPlaced})]));
  });
  shf.addEventListener("click", () => { mix(); msg.replaceChildren(); draw(); });
  mix(); draw();
  box.append(el("p",{class:"thgoal"}, el("b",{text:U.goal}), " : ", w.goal), list, el("div",{class:"btns thbtns"}, chk, shf), msg);
}

// ---- exécution pas à pas : petit interprète de blocs Scratch (déplacements, rotations, parole, stylo, boucle « répéter », condition)
function wTrace(w, box){
  const grid = w.world === "grid";
  let sc = 0, snaps = [], pos = -1, guess = null, ang = 0, initSt = null;
  const scriptHost = el("div",{class:"thscript"}), stageHost = el("div",{class:"thstage"}), info = el("div",{class:"thinfo"}), msg = el("p",{class:"thfb"});
  let ids = [], byId = [];
  function nodeEl(n){
    const id = ids.length; n._id = id; ids.push(null); byId[id] = n;
    if (n.body) {
      const head = el("div",{class:"blk " + n.c + " chead"}, n.cond ? [el("span",{text:n.pre}), " ", el("span",{class:"hex",text:n.cond.t}), " ", el("span",{text:n.post})] : n.t);
      ids[id] = head;
      const kids = [head], body = el("div",{class:"cbody"}, n.body.map(nodeEl)); n._thenEl = body; kids.push(body);
      if (n.els) { const eb = el("div",{class:"cbody"}, n.els.map(nodeEl)); n._elseEl = eb; kids.push(el("div",{class:"blk " + n.c + " csep",text:n.else_t}), eb); }
      kids.push(el("div",{class:"cend"}));
      return el("div",{class:"cwrap",style:"--cb:" + THFAM[n.c]}, kids);
    }
    const e = blkChip(n); ids[id] = e; return e;
  }
  const norm = d => { d = ((d % 360) + 360) % 360; return d > 180 ? d - 360 : d; };
  function simulate(init){
    const st = Object.assign({x:0, y:0, dir:90, pen:false, say:"", lines:[], costume:1, c:0, r:0}, init), out = [];
    const touching = obj => { const o = (w.objects || []).find(q => q.art === obj); return !!o && Math.abs(st.x - o.x) < 62 && Math.abs(st.y - o.y) < 54; };
    const snap = (n, extra) => out.push(Object.assign({id:n._id, x:st.x, y:st.y, c:st.c, r:st.r, dir:st.dir, say:st.say, pen:st.pen, costume:st.costume, lines:st.lines.map(l => l.slice())}, extra || {}));
    const run = list => list.forEach(exec);
    function exec(n){
      switch (n.op) {
        case "hat": snap(n); break;
        case "move": { const x0 = st.x, y0 = st.y; st.x += n.n * Math.sin(st.dir * Math.PI / 180); st.y += n.n * Math.cos(st.dir * Math.PI / 180); if (st.pen) st.lines.push([x0, y0, st.x, st.y]); snap(n); break; }
        case "turn": st.dir = norm(st.dir + n.d); snap(n); break;
        case "goto": { const x0 = st.x, y0 = st.y; st.x = n.x; st.y = n.y; if (st.pen) st.lines.push([x0, y0, st.x, st.y]); snap(n); break; }
        case "say": st.say = n.text; snap(n); if (n.s) st.say = ""; break;
        case "costume": st.costume = st.costume % 2 + 1; snap(n); break;
        case "pendown": st.pen = true; snap(n); break;
        case "penup": st.pen = false; snap(n); break;
        case "fwd": st.c += Math.round(Math.sin(st.dir * Math.PI / 180)); st.r += Math.round(Math.cos(st.dir * Math.PI / 180)); snap(n); break;
        case "right": st.dir = (st.dir + 90) % 360; snap(n); break;
        case "left": st.dir = (st.dir + 270) % 360; snap(n); break;
        case "repeat": for (let k = 1; k <= n.n; k++) { snap(n, {iter:k, total:n.n}); run(n.body); } break;
        case "forever": for (let k = 1; k <= 3; k++) { snap(n, {iter:k, total:0}); run(n.body); } break;
        case "if": case "ifelse": { const v = n.cond.op === "touch" ? touching(n.cond.obj) : false; snap(n, {cond:v, branch:v ? "then" : "else"}); if (v) run(n.body); else if (n.els) run(n.els); break; }
      }
    }
    run(w.script); return out;
  }
  // décor de la scène : quadrillage, objets fixes, trace du stylo, lutin, bulle
  function baseSvg(){
    if (grid) {
      const N = w.grid.n, cs = 60, S = N * cs; let s = `<svg class="thsvg" viewBox="0 0 ${S} ${S}" role="img"><rect width="${S}" height="${S}" fill="#fff"/>`;
      for (let i = 0; i <= N; i++) s += `<line x1="${i * cs}" y1="0" x2="${i * cs}" y2="${S}" stroke="#cfe5d6" stroke-width="2"/><line x1="0" y1="${i * cs}" x2="${S}" y2="${i * cs}" stroke="#cfe5d6" stroke-width="2"/>`;
      w.grid.marks.forEach(m => { const cx = m.c * cs + cs / 2, cy = S - (m.r * cs + cs / 2); s += `<circle cx="${cx}" cy="${cy}" r="19" fill="#fff6e0" stroke="#e8a21c" stroke-width="3"/><text x="${cx}" y="${cy + 7}" text-anchor="middle" font-size="21" font-weight="800" fill="#8a5a00" font-family="Arial">${m.l}</text>`; });
      return s + `<g class="gsp"><rect x="-19" y="-19" width="38" height="38" rx="9" fill="#4C97FF" stroke="#3373CC" stroke-width="3"/><circle cx="-7" cy="-3" r="4.5" fill="#fff"/><circle cx="7" cy="-3" r="4.5" fill="#fff"/><path d="M-9,-22 L0,-34 L9,-22 Z" fill="#e8861c"/></g></svg>`;
    }
    let s = `<svg class="thsvg" viewBox="0 0 480 360" role="img"><rect width="480" height="360" fill="#fff"/>`;
    for (let x = 0; x <= 480; x += 60) s += `<line x1="${x}" y1="0" x2="${x}" y2="360" stroke="#e6edf8"/>`;
    for (let y = 0; y <= 360; y += 60) s += `<line x1="0" y1="${y}" x2="480" y2="${y}" stroke="#e6edf8"/>`;
    if (w.coords) s += `<line x1="0" y1="180" x2="480" y2="180" stroke="#9db8e8" stroke-width="2"/><line x1="240" y1="0" x2="240" y2="360" stroke="#9db8e8" stroke-width="2"/>`;
    (w.objects || []).forEach(o => { s += `<image href="${thArt[o.art]}" x="${240 + o.x - 22}" y="${180 - o.y - 22}" width="44" height="44"/>`; });
    return s + `<g class="glines"></g><g class="gsp"><image href="${thArt.cat}" x="-40" y="-32" width="80" height="64"/></g><g class="gbub"></g></svg>`;
  }
  function paint(s){
    const svg = stageHost.querySelector("svg"), sp = svg.querySelector(".gsp");
    if (grid) {
      const cs = 60, S = w.grid.n * cs, tx = s.c * cs + cs / 2, ty = S - (s.r * cs + cs / 2), target = s.dir; let d = ((target - ang) % 360 + 540) % 360 - 180; ang += d;
      sp.style.transform = `translate(${tx}px,${ty}px) rotate(${ang}deg)`; return;
    }
    const target = s.dir - 90; let d = ((target - ang) % 360 + 540) % 360 - 180; ang += d;
    sp.style.transform = `translate(${240 + s.x}px,${180 - s.y}px) rotate(${ang}deg)`;
    svg.querySelector(".glines").innerHTML = s.lines.map(l => `<line x1="${240 + l[0]}" y1="${180 - l[1]}" x2="${240 + l[2]}" y2="${180 - l[3]}" stroke="#c0392b" stroke-width="4" stroke-linecap="round"/>`).join("");
    const bub = svg.querySelector(".gbub");
    if (s.say) { const t = s.say, bw = Math.max(80, t.length * 9 + 28), bx = Math.min(Math.max(240 + s.x + 24, bw / 2 + 6), 474 - bw / 2), by = Math.max(180 - s.y - 58, 22);
      bub.innerHTML = `<rect x="${bx - bw / 2}" y="${by - 18}" width="${bw}" height="34" rx="15" fill="#fff" stroke="#9aa3b2" stroke-width="2"/><text x="${bx}" y="${by + 5}" text-anchor="middle" font-size="16" font-weight="700" fill="#333" font-family="Tajawal,Arial,sans-serif">${t.replace(/&/g, "&amp;").replace(/</g, "&lt;")}</text>`; }
    else bub.innerHTML = "";
  }
  const bPrev = el("button",{type:"button",class:"btn",text:U.prev}), bNext = el("button",{type:"button",class:"btn main",text:U.next}), bAll = el("button",{type:"button",class:"btn",text:U.runAll}), bReset = el("button",{type:"button",class:"btn",text:U.retry});
  function show(k){
    pos = k; const s = k < 0 ? initSt : snaps[k];
    ids.forEach(e => e && e.classList.remove("run")); scriptHost.querySelectorAll(".skip").forEach(e => e.classList.remove("skip"));
    for (let i = 0; i <= k; i++) { const q = snaps[i]; if (q.branch) { const n = byId[q.id], other = q.branch === "then" ? n._elseEl : n._thenEl; if (other) other.classList.add("skip"); } }
    if (k >= 0 && ids[snaps[k].id]) ids[snaps[k].id].classList.add("run");
    paint(s);
    const row = [el("span",{class:"thi"}, el("b",{text:U.step}), " ", el("span",{class:"num",text:(k + 1) + " / " + snaps.length}))];
    if (!grid) { if (w.coords) row.push(el("span",{class:"thi"}, el("b",{text:U.xName}), " ", el("span",{class:"num",text:thNum(s.x)}), "  ", el("b",{text:U.yName}), " ", el("span",{class:"num",text:thNum(s.y)}))); row.push(el("span",{class:"thi"}, el("b",{text:U.direction}), " ", el("span",{class:"num",text:Math.round(s.dir) + "°"}))); }
    if (k >= 0 && s.iter) row.push(el("span",{class:"thi"}, el("b",{text:U.turnN}), " ", el("span",{class:"num",text:s.iter + " / " + s.total})));
    if (k >= 0 && s.cond !== undefined) row.push(el("span",{class:"thi"}, el("b",{text:U.condLbl}), " : ", el("span",{text:s.cond ? U.isTrue : U.isFalse})));
    info.replaceChildren(...row);
    bPrev.disabled = k < 0; bNext.disabled = k >= snaps.length - 1; bAll.disabled = k >= snaps.length - 1;
    msg.className = "thfb"; msg.replaceChildren();
    if (k === snaps.length - 1) {
      msg.className = "thfb ok";
      msg.append(el("b",{text:U.endScript}), " ", w.end || "");
      if (w.predict && guess !== null) { const okp = guess === w.predict.a; msg.append(el("br"), el("b",{text:okp ? U.guessOk : U.guessKo}), " ", okp ? w.predict.ok : w.predict.ko); }
      if (w.predict) box.querySelectorAll(".thpred .thopt").forEach((b, i) => { b.classList.toggle("ok", i === w.predict.a); b.classList.toggle("ko", guess === i && i !== w.predict.a); });
    } else if (w.predict) box.querySelectorAll(".thpred .thopt").forEach(b => b.classList.remove("ok", "ko"));
  }
  function rebuild(){
    ids = []; byId = []; guess = null; ang = 0;
    scriptHost.replaceChildren(el("div",{class:"thlbl",text:U.script}), el("div",{class:"scr"}, w.script.map(nodeEl)));
    initSt = Object.assign({x:0, y:0, dir:90, c:0, r:0, say:"", lines:[]}, w.scenarios ? w.scenarios[sc].init : w.init);
    snaps = simulate(w.scenarios ? w.scenarios[sc].init : w.init);
    stageHost.innerHTML = baseSvg(); ang = grid ? initSt.dir : initSt.dir - 90;
    box.querySelectorAll(".thpred .thopt").forEach(b => b.classList.remove("sel", "ok", "ko"));
    show(-1);
  }
  bNext.addEventListener("click", () => { if (pos < snaps.length - 1) show(pos + 1); });
  bPrev.addEventListener("click", () => { if (pos >= 0) show(pos - 1); });
  bAll.addEventListener("click", () => show(snaps.length - 1));
  bReset.addEventListener("click", () => { guess = null; box.querySelectorAll(".thpred .thopt").forEach(b => b.classList.remove("sel")); ang = grid ? initSt.dir : initSt.dir - 90; show(-1); });
  if (w.scenarios) {
    const chips = el("div",{class:"dlchips"}, el("b",{text:U.chooseCase}), " ", w.scenarios.map((s, i) => { const c = el("button",{type:"button",class:"chip","aria-pressed":String(i === sc),text:s.t}); c.addEventListener("click", () => { sc = i; chips.querySelectorAll(".chip").forEach((x, j) => x.setAttribute("aria-pressed", String(j === i))); rebuild(); }); return c; }));
    box.append(chips);
  }
  if (w.predict) {
    const pr = el("div",{class:"thpred"}, el("b",{text:w.predict.q}), " ", w.predict.o.map((t, i) => { const b = el("button",{type:"button",class:"thopt",text:t}); b.addEventListener("click", () => { guess = i; box.querySelectorAll(".thpred .thopt").forEach((x, j) => x.classList.toggle("sel", j === i)); }); return b; }));
    box.append(pr);
  }
  box.append(el("div",{class:"thtrace"}, scriptHost, el("div",{class:"thside"}, el("div",{class:"thlbl",text:U.stage}), stageHost, info)), el("div",{class:"btns thbtns"}, bPrev, bNext, bAll, bReset), msg);
  rebuild();
}

// ---- schéma cliquable de l'écran de Scratch : explorer, puis jouer à « Où est… ? »
function wIface(w, box){
  const host = el("div",{class:"ifhost"}); host.innerHTML = TH.iface.svg;
  const svg = host.querySelector("svg"), zones = {}; TH.iface.zones.forEach(z => zones[z.id] = z);
  const info = el("div",{class:"ifinfo"}), chips = el("div",{class:"dlchips ifchips"}), bar = el("div",{class:"dlchips"}), score = el("p",{class:"thfb"});
  let mode = "explore", queue = [], qi = 0, good = 0, locked = false, run = 0;
  const mark = (id, cls) => { const g = svg.querySelector(`.zone[data-z="${id}"]`); if (g) { g.classList.remove("sel", "ok", "ko"); if (cls) g.classList.add(cls); } };
  const clear = () => svg.querySelectorAll(".zone").forEach(g => g.classList.remove("sel", "ok", "ko"));
  function explore(id){ clear(); mark(id, "sel"); const z = zones[id]; info.className = "ifinfo"; info.replaceChildren(el("b",{class:"ifnum",text:id}), " ", el("b",{text:z.name}), el("p",{text:z.desc})); }
  function ask(){
    clear(); locked = false; const id = queue[qi], z = zones[id]; info.className = "ifinfo ask";
    info.replaceChildren(el("span",{class:"num",text:(qi + 1) + " / " + queue.length}), " ", el("b",{text:U.clickOn}), " ", el("b",{class:"ifq",text:z.name}));
  }
  function pick(id){
    if (mode === "explore") { explore(id); return; }
    if (locked || qi >= queue.length) return;
    const tok = run;
    if (id === queue[qi]) { good++; mark(id, "ok"); locked = true; info.className = "ifinfo ok"; info.replaceChildren(el("b",{text:U.good1}), el("p",{text:zones[id].desc})); qi++;
      setTimeout(() => { if (mode !== "game" || tok !== run) return; if (qi < queue.length) ask(); else { clear(); info.className = "ifinfo ok"; info.replaceChildren(el("b",{text:U.score}), " ", el("span",{class:"num big",text:good + " / " + queue.length}), el("p",{text: good === queue.length ? U.perfect : U.good})); } }, 1500); }
    else { mark(id, "ko"); info.className = "ifinfo ko"; info.replaceChildren(el("b",{text:U.wrongZone}), " ", el("b",{class:"ifq",text:zones[queue[qi]].name})); setTimeout(() => { if (mode === "game" && tok === run && !locked) { mark(id, null); info.className = "ifinfo ask"; ask(); } }, 1100); }
  }
  svg.querySelectorAll(".zone").forEach(g => g.addEventListener("click", () => pick(+g.dataset.z)));
  TH.iface.zones.forEach(z => { const c = el("button",{type:"button",class:"chip"}, el("b",{class:"ifnum",text:z.id}), " ", z.name); c.addEventListener("click", () => pick(z.id)); chips.append(c); });
  const bE = el("button",{type:"button",class:"chip","aria-pressed":"true",text:U.explore}), bG = el("button",{type:"button",class:"chip","aria-pressed":"false",text:U.game});
  const setMode = m => { mode = m; run++; bE.setAttribute("aria-pressed", String(m === "explore")); bG.setAttribute("aria-pressed", String(m === "game")); clear();
    if (m === "game") { queue = thShuffle(TH.iface.zones.map(z => z.id)); qi = 0; good = 0; ask(); } else { info.className = "ifinfo"; info.replaceChildren(el("p",{class:"pnote",text:U.pickZone})); } };
  bE.addEventListener("click", () => setMode("explore")); bG.addEventListener("click", () => setMode("game")); bar.append(bE, bG);
  box.append(bar, el("div",{class:"ifwrap"}, host, info), el("h5",{text:U.zonesList}), chips);
  setMode("explore");
}

// ---- coordonnées : lire x et y en cliquant sur la scène, puis placer le lutin
function wCoord(w, box){
  const host = el("div",{class:"thstage coordhost"}), info = el("div",{class:"thinfo"}), task = el("p",{class:"thgoal"}), msg = el("p",{class:"thfb"});
  let ti = 0, px = 0, py = 0, solved = [];
  function svgHtml(){
    let s = `<svg class="thsvg" viewBox="0 0 480 360" role="img"><rect width="480" height="360" fill="#fff"/>`;
    for (let x = 0; x <= 480; x += 60) s += `<line x1="${x}" y1="0" x2="${x}" y2="360" stroke="#e6edf8"/>`;
    for (let y = 0; y <= 360; y += 60) s += `<line x1="0" y1="${y}" x2="480" y2="${y}" stroke="#e6edf8"/>`;
    s += `<line x1="0" y1="180" x2="480" y2="180" stroke="#4C97FF" stroke-width="2.5"/><line x1="240" y1="0" x2="240" y2="360" stroke="#4C97FF" stroke-width="2.5"/>`;
    for (let v = -180; v <= 180; v += 60) if (v) s += `<text x="${240 + v}" y="196" text-anchor="middle" font-size="11" fill="#4C6FB5" font-family="Arial">${thNum(v)}</text>`;
    for (let v = -120; v <= 120; v += 60) if (v) s += `<text x="248" y="${184 - v}" font-size="11" fill="#4C6FB5" font-family="Arial">${thNum(v)}</text>`;
    solved.forEach(i => { const t = w.targets[i]; s += `<circle cx="${240 + t.x}" cy="${180 - t.y}" r="9" fill="#2e9e5b" opacity=".55"/>`; });
    s += `<line x1="${240 + px}" y1="${180 - py}" x2="${240 + px}" y2="180" stroke="#e8861c" stroke-width="2.5" stroke-dasharray="6 5"/><line x1="${240 + px}" y1="${180 - py}" x2="240" y2="${180 - py}" stroke="#e8861c" stroke-width="2.5" stroke-dasharray="6 5"/>`;
    s += `<image href="${thArt.cat}" x="${240 + px - 40}" y="${180 - py - 32}" width="80" height="64"/><circle cx="${240 + px}" cy="${180 - py}" r="4.5" fill="#e23b3b"/></svg>`;
    return s;
  }
  function draw(){
    host.innerHTML = svgHtml();
    info.replaceChildren(el("span",{class:"thi"}, el("b",{text:U.xName}), " ", el("span",{class:"num",text:thNum(px)}), "  ", el("b",{text:U.yName}), " ", el("span",{class:"num",text:thNum(py)})));
    const t = w.targets[ti];
    if (ti >= w.targets.length) { task.replaceChildren(el("b",{text:U.challengesDone})); return; }
    task.replaceChildren(el("b",{text:U.challengeN}), " ", el("span",{class:"num",text:(ti + 1) + " / " + w.targets.length}), " : ", el("span",{text:U.placeAt}), " ", el("b",{text:U.xName}), " = ", el("span",{class:"num",text:thNum(t.x)}), "  ", el("b",{text:U.yName}), " = ", el("span",{class:"num",text:thNum(t.y)}));
  }
  host.addEventListener("click", e => {
    const svg = host.querySelector("svg"), r = svg.getBoundingClientRect();
    px = Math.max(-240, Math.min(240, Math.round((e.clientX - r.left) / r.width * 480 - 240))); py = Math.max(-180, Math.min(180, Math.round(180 - (e.clientY - r.top) / r.height * 360)));
    msg.className = "thfb"; msg.replaceChildren();
    if (ti < w.targets.length) {
      const t = w.targets[ti], dist = Math.hypot(px - t.x, py - t.y);
      if (dist <= 20) { solved.push(ti); ti++; msg.className = "thfb ok"; msg.append(el("b",{text:ti >= w.targets.length ? U.challengesDone : U.wellPlacedOne})); }
      else { msg.className = "thfb ko"; msg.append(el("b",{text:U.tooFar}), " ", el("span",{text:U.youClicked}), " ", el("b",{text:U.xName}), " = ", el("span",{class:"num",text:thNum(px)}), "  ", el("b",{text:U.yName}), " = ", el("span",{class:"num",text:thNum(py)})); }
    }
    draw();
  });
  const again = el("button",{type:"button",class:"btn",text:U.retry}); again.addEventListener("click", () => { ti = 0; solved = []; px = 0; py = 0; msg.replaceChildren(); msg.className = "thfb"; draw(); });
  box.append(task, host, info, msg, el("div",{class:"btns thbtns"}, again)); draw();
}
'''

CSS = r'''
/* ---- Théorie Scratch */
.thgrid{grid-template-columns:repeat(auto-fill,minmax(225px,1fr))}.thmeta{margin:0;padding:0 12px 10px;display:flex;gap:6px;align-items:center;flex-wrap:wrap}.thmeta .chip{font-size:12px;padding:0 10px;cursor:default}
.thcard .actthumb{aspect-ratio:4/3}.thcard .actthumb img{object-fit:contain;background:#fff}
.thpage h3{margin:20px 0 6px;color:#1e3a6e}.thmeta2{display:flex;flex-wrap:wrap;align-items:center;gap:6px}.thscore{margin-inline-start:6px}
.thcall{border-radius:12px;padding:10px 14px;margin:8px 0;font-size:16px;line-height:1.7}.thhook{background:#fff6e0;border:1px solid #f0dca0}.thlife{background:#eaf6ff;border:1px solid #bcdcf5}
.threcall{background:#f3f0ff;border:1px dashed #c8bdf0;border-radius:10px;padding:6px 12px;font-size:14px;color:#4a3d8a;margin:8px 0}
.thidea p{font-size:17px;line-height:1.8;margin:6px 0}.thfigs{display:flex;flex-wrap:wrap;gap:12px}.thfigs figure{margin:0;flex:1 1 280px;max-width:480px;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:#fff}.thfigs img{width:100%;height:auto;display:block}.thfigs figcaption{padding:6px 10px;font-weight:700;color:#1e3a6e;font-size:14px}
.thw{border:1px solid var(--line);border-radius:14px;padding:12px 14px;margin:14px 0;background:#fbfcff}.thw h4{margin:0 0 2px;color:#1e3a6e;font-size:17px}.thw h5{margin:12px 0 4px}.thw .pnote{margin:2px 0 8px}
.thvocab{width:100%;border-collapse:collapse;font-size:15px}.thvocab th,.thvocab td{border:1px solid var(--line);padding:5px 10px;text-align:start;vertical-align:top}.thvocab th{background:#eaf1fb;color:#1e3a6e}
.thmist li{margin:3px 0}.thrules{padding-inline-start:26px;display:flex;flex-direction:column;gap:4px}
/* QCM */
.thq{display:flex;flex-direction:column;gap:10px}.thqq{border:1px solid var(--line);border-radius:10px;padding:8px 12px;background:#fff}.thqt{margin:0 0 6px;font-weight:700}.thstem{margin:4px 0 8px}
.thopts{display:flex;flex-direction:column;gap:6px;align-items:stretch}.thopt{font:inherit;font-size:15px;text-align:start;border:1.5px solid var(--line);background:#fff;border-radius:8px;padding:6px 12px;cursor:pointer;line-height:1.5;color:var(--ink)}
.thopt:hover:not(:disabled){border-color:#1e4fa8;background:#f1f6ff}.thopt.sel{border-color:#1e4fa8;background:#e6efff}.thopt.ok{border-color:#2e9e5b;background:#e4f6e8;font-weight:700}.thopt.ko{border-color:#c0392b;background:#fde8e5}.thopt:disabled{cursor:default;color:var(--ink)}
.thfb{margin:6px 0 0;min-height:1.2em;font-size:15px}.thfb.ok{color:#1d6b3b}.thfb.ko{color:#a02f23}.thres{margin-top:10px;border:2px solid #1e4fa8;border-radius:12px;padding:8px 14px;background:#f1f6ff}.thres p{margin:4px 0}.num{direction:ltr;unicode-bidi:isolate;display:inline-block}.num.big{font-size:22px;font-weight:800;color:#1e4fa8}
.thopt .blk,.thstem .blk,.thit .blk{display:inline-block}.thopt .blk{font-size:14px}.ifsvg,.thsvg{direction:ltr}
/* blocs Scratch (pastilles et scripts) */
.blk.hat{border-radius:16px 16px 5px 5px;padding-top:7px}.blk .hex{display:inline-block;background:#2a9fc9;border:1.5px solid #fff;border-radius:12px;padding:0 10px;margin:0 2px}
.scr{display:flex;flex-direction:column;align-items:flex-start;gap:2px}.scr .blk{display:inline-block;font-size:14px;padding:6px 12px;border-radius:6px;transition:outline-color .2s,box-shadow .2s}.scr .blk.hat{border-radius:16px 16px 6px 6px}
.scr .blk.run{outline:3px solid #ffd43b;box-shadow:0 0 0 6px rgba(255,212,59,.4)}
.cwrap{display:flex;flex-direction:column;align-items:flex-start}.cwrap>.cbody{padding-block:2px;padding-inline:12px 0;border-inline-start:16px solid var(--cb);display:flex;flex-direction:column;align-items:flex-start;gap:2px;min-height:14px;transition:opacity .25s}
.cwrap>.cend{height:14px;width:96px;background:var(--cb);border-radius:0 0 6px 6px}.cwrap>.cbody.skip{opacity:.28}.csep{border-radius:0!important}
/* remettre dans l'ordre */
.thgoal{margin:4px 0 8px;background:#fff;border:1px solid var(--line);border-radius:8px;padding:6px 12px}.thord{list-style:none;margin:8px 0;padding:0;display:flex;flex-direction:column;gap:6px}
.thit{display:flex;align-items:center;gap:10px;border:1.5px solid var(--line);background:#fff;border-radius:10px;padding:5px 8px}.thit.ok{border-color:#2e9e5b;background:#e4f6e8}.thit.ko{border-color:#c0392b;background:#fde8e5}
.thctrl{display:inline-flex;flex-direction:column;gap:2px}.thmv{font:inherit;font-size:11px;line-height:1;border:1px solid var(--line);background:#f6f8fc;border-radius:5px;width:26px;height:20px;cursor:pointer;padding:0}.thmv:disabled{opacity:.3;cursor:default}.thtxt{font-size:16px}
.thbtns{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}.thbtns .btn{min-width:110px}
/* exécution pas à pas */
.thpred{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:6px 0}.thtrace{display:grid;grid-template-columns:minmax(220px,1fr) minmax(240px,1.2fr);gap:14px;align-items:start;margin-top:8px}
.thscript{border:1px solid var(--line);border-radius:10px;padding:10px;background:#fff;overflow-x:auto}.thlbl{font-size:12px;font-weight:700;color:#5d6678;margin-bottom:4px}
.thside{min-width:0}.thstage{border:2px solid #4C97FF;border-radius:6px;overflow:hidden;background:#fff;line-height:0}.thsvg{width:100%;height:auto;display:block}.thstage .gsp{transition:transform .5s ease}
.thinfo{display:flex;flex-wrap:wrap;gap:6px 16px;margin-top:6px;font-size:14px;line-height:1.5}.thi{white-space:nowrap}.coordhost{max-width:560px;cursor:crosshair}
@media (max-width:640px){.thtrace{grid-template-columns:1fr}}
/* schéma de l'écran de Scratch */
.ifwrap{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(200px,1fr);gap:14px;align-items:start}.ifhost{border:2px solid #6a4fc7;border-radius:8px;overflow:hidden;line-height:0}.ifsvg{width:100%;height:auto;display:block}
.ifsvg .zone{cursor:pointer}.ifsvg .zone .hl{opacity:0;transition:opacity .15s}.ifsvg .zone:hover .hl{opacity:.55}.ifsvg .zone.sel .hl{opacity:1}.ifsvg .zone.ok .hl{opacity:1;stroke:#2e9e5b}.ifsvg .zone.ko .hl{opacity:1;stroke:#c0392b}
.ifinfo{border:1.5px solid var(--line);border-radius:10px;padding:8px 12px;background:#fff;min-height:96px;font-size:15px}.ifinfo p{margin:4px 0 0}.ifinfo.ok{border-color:#2e9e5b;background:#e4f6e8}.ifinfo.ko{border-color:#c0392b;background:#fde8e5}.ifinfo.ask{border-color:#6a4fc7;background:#f3f0ff}.ifq{color:#6a4fc7}
.ifnum{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:#e23b3b;color:#fff;font-size:13px}.ifchips .chip{display:inline-flex;gap:6px;align-items:center}
@media (max-width:760px){.ifwrap{grid-template-columns:1fr}}
/* aide-mémoire imprimable */
.memo{margin-top:24px;border:2px solid #1e4fa8;border-radius:14px;padding:6px 16px 14px;background:#fff}.memo h4{margin:14px 0 6px;color:#1e4fa8}.memotop{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:16px;align-items:start}.memotop h4{margin-top:4px}.memofig img{width:100%;height:auto;display:block;border-radius:8px}@media (max-width:760px){.memotop{grid-template-columns:1fr}}.thtools{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}
@media print{body.print-memo #axisHead .axhead>*:not(.memo){display:none!important}body.print-memo #axisHead .axhead,body.print-memo .memo{border:0;padding:0;margin:0}body.print-memo main.wrap{padding-top:0;margin-top:0}body.print-memo .memotop{grid-template-columns:1.2fr 1fr}body.print-memo .thvocab{font-size:11.5px}body.print-memo .thvocab td,body.print-memo .thvocab th{padding:2px 6px}body.print-memo .thrules{font-size:13px;gap:2px}body.print-memo .memo h3{margin:0 0 6px}body.print-memo .memo h4{margin:8px 0 4px}.thw .btns,.thbtns,.thpred,.dlchips{display:none!important}.thw{break-inside:avoid}}
'''
