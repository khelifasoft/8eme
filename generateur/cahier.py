"""« Cahier de l'élève » : fiches à imprimer et à coller dans le cahier, une par séance de programmation (6 en 7e, 10 en 8e, 14 en 9e).
Produit cahier/cahier-7.html, cahier-8.html, cahier-9.html (bilingues arabe / français, avec bouton « Imprimer », affichage du corrigé et choix de la séance)
et, avec --pdf, les PDF correspondants (cahier-N-ar.pdf, cahier-N-fr.pdf, cahier-N-ar-corrige.pdf, cahier-N-fr-corrige.pdf).
Contenu : cahier_cards.py (notions : phrases à trous) et cahier_data.py (trace écrite, script à finir de chaque séance) ; images : cahier_img.py.
Usage : python3 generateur/cahier.py [--pdf]"""
import os, sys, re, json, random, subprocess, shutil
from xml.sax.saxutils import escape
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
import planning as PL, seances as S, cahier_cards as CC, cahier_data as CD, cahier_img as CI
import theorie as TH
OUT = os.path.join(ROOT, "cahier"); os.makedirs(OUT, exist_ok=True)
NID = PL.NID
YEAR = {"7": ("7e année", "السنة السابعة"), "8": ("8e année", "السنة الثامنة"), "9": ("9e année", "السنة التاسعة")}
MAXFILL = 5
BLANK = re.compile(r"\{\{(.+?)\}\}")


# ----------------------------------------------------------------------------- textes bilingues
def bl(s):
    """échappe le texte et transforme {{mot}} en trou (le mot est visible dans le corrigé)"""
    return BLANK.sub(lambda m: f'<span class="bl"><span class="ans">{m.group(1)}</span></span>', escape(s))
def t(pair, cls=""):
    fr, ar = pair
    return f'<span class="ar{(" " + cls) if cls else ""}" lang="ar">{bl(ar)}</span><span class="fr{(" " + cls) if cls else ""}" lang="fr">{bl(fr)}</span>'
def tp(fr, ar): return t((fr, ar))
def words(pair): return BLANK.findall(pair[0]), BLANK.findall(pair[1])
def both(f): return f'<span class="ar">{f("ar")}</span><span class="fr">{f("fr")}</span>'


# ----------------------------------------------------------------------------- blocs de la trace écrite
def chip(cat, fr, ar): return f'<span class="blk {cat}"><span class="ar" lang="ar">{escape(ar)}</span><span class="fr" lang="fr">{escape(fr)}</span></span>'
def cell(c):
    if c is None: return '<span class="wr"></span>'
    if isinstance(c, dict):
        if "blk" in c: return chip(*c["blk"])
        if "blks" in c: return " ".join(chip(*x) for x in c["blks"])
    return t(c)
def lines(n): return "".join('<span class="wl"></span>' for _ in range(n))


def render_table(b):
    cols, rows, w, first, rh = b["cols"], b["rows"], b.get("w"), b.get("first"), b.get("rh")
    tot = sum(w) if w else 0
    cg = "<colgroup>" + "".join(f'<col style="width:{100 * x / tot:.1f}%">' for x in w) + "</colgroup>" if w else ""
    head = "".join(f"<th>{t(c) if c and (c[0] or c[1]) else ''}</th>" for c in cols)
    body = ""
    for i, row in enumerate(rows):
        extra = (rh[i] if rh and i < len(rh) else 0)
        tds = ""
        for j, c in enumerate(row):
            tag = "th" if first and j == 0 else "td"
            content = cell(c)
            if c is None and extra: content = lines(extra)
            tds += f"<{tag}>{content}</{tag}>"
        body += f'<tr class="{"tall" if (extra or any(c is None for c in row)) else ""}">{tds}</tr>'
    return f'<table class="ft">{cg}<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def render_card(b):
    w = b["w"]; tot = sum(w)
    rows = ""
    for label, val, n in b["fields"]:
        v = lines(max(n, 1)) if val is None else cell(val)
        rows += f"<tr><th>{t(label)}</th><td>{v}</td></tr>"
    return f'<table class="fc"><colgroup><col style="width:{100 * w[0] / tot:.1f}%"><col style="width:{100 * w[1] / tot:.1f}%"></colgroup>{rows}</table>'


def render_flow(b):
    out = ""
    items = b["items"]
    for i, (kind, pair) in enumerate(items):
        out += f'<div class="fb {kind}">{t(pair)}</div>'
        if i < len(items) - 1: out += '<div class="fa">↓</div>'
    return f'<div class="flow">{out}</div>'


def render_svg(b):
    k = b["kind"]
    if k == "iface": return f'<div class="fig">{both(lambda l: CI.iface_static(l))}</div>'
    if k == "robot": return f'<div class="fig small">{both(lambda l: CI.robot_grid(l, marks=b.get("marks", ())))}</div>'
    if k == "plane": return f'<div class="fig plane">{both(lambda l: CI.plane(l, b["pts"]))}</div>'
    raise KeyError(k)


def render_cards(b):
    out = ""
    for sym, shown in b["items"]:
        out += f'<span class="crd shown">{sym}</span>' if shown else f'<span class="crd blank"><span class="ans">{sym}</span></span>'
    return f'<div class="cards">{out}</div>'


def render(b):
    k = b["k"]
    if k == "table": return render_table(b)
    if k == "card": return render_card(b)
    if k == "flow": return render_flow(b)
    if k == "svg": return render_svg(b)
    if k == "cards": return render_cards(b)
    if k == "text": return f'<p class="ftxt">{t(b["t"])}</p>'
    if k == "stack": return "".join(render(x) for x in b["items"])
    if k == "cols":
        w = b["w"]
        return f'<div class="cols" style="grid-template-columns:{w[0]}fr {w[1]}fr">' + "".join(f'<div>{render(x)}</div>' for x in b["items"]) + "</div>"
    raise KeyError(k)


# ----------------------------------------------------------------------------- script à moitié terminé
def scaled(svg, k):
    m = re.match(r'<svg([^>]*?) width="(\d+)" height="(\d+)"', svg)
    if not m or k == 1: return svg
    return svg.replace(m.group(0), f'<svg{m.group(1)} width="{int(int(m.group(2)) * k)}" height="{int(int(m.group(3)) * k)}"', 1)
def svg_height(svg):
    m = re.search(r'height="(\d+)"', svg); return int(m.group(1)) if m else 80
def render_script(sc, act):
    A = PL.ACT[sc["act"]]; out = ""
    for p in sc["parts"]:
        k = 0.78 if svg_height(CI.script_svg(p["full"], "fr")) > 300 else 0.92
        full = both(lambda l: scaled(CI.script_svg(p["full"], l), k))
        if p["masked"] is None:
            h = max(int(svg_height(CI.script_svg(p["full"], "fr")) * k), 90)
            mask_html = f'<div class="frame" style="min-height:{h}px"><span class="hintx">{tp("Écris ici le script corrigé", "اكتب هنا السكربت المصحَّح")}</span></div>'
        else:
            mask_html = both(lambda l: scaled(CI.script_svg(p["masked"], l), k))
        same = p["masked"] is p["full"]
        out += f'<div class="sv"><div class="stu">{mask_html}</div><div class="cor">{full}</div></div>' if not same else f'<div class="sv">{full}</div>'
    q = ""
    if sc.get("q"):
        q = '<ol class="sq">' + "".join(f"<li>{t(x[0] if len(x) == 1 else x)}</li>" for x in sc["q"]) + "</ol>"
    note = f'<p class="ftxt">{t(sc["note"])}</p>' if sc.get("note") else ""
    title = f'<p class="actl"><b>{tp("Activité n°", "النشاط رقم")} {sc["act"]}</b> — {t(A["title"])}</p>'
    return title + note + f'<div class="svs">{out}</div>' + q


# ----------------------------------------------------------------------------- une fiche
def fill_from(notions):
    out = []
    for rnd in range(3):
        for n in notions:
            c = CC.CARDS[n]["fill"]
            if len(c) > rnd and len(out) < MAXFILL: out.append(c[rnd])
    return out
def retain_from(notions):
    out = []
    for n in notions:
        for r in CC.CARDS[n]["retain"][:1]:
            if len(out) < 3: out.append(r)
    return out


def fiche(y, s):
    if isinstance(s, str):      # séance complémentaire proposée (cahier_extra.py)
        import cahier_extra as CE; e = CE.EXTRA[s]
        title, obj, trace = e["title"], e["obj"], e["trace"]; spec = dict(form=e["form"], script=None, fill=e["fill"], retain=e["retain"])
        p = dict(new=[], deep=[], core=[], support=[], challenge=[], acq=e["acq"]); seed = int(y) * 100 + ord(s[0]) * 7 + int(s[1:])
    else:
        base = S.SEANCES[y][s - 1]; p = PL.PLAN[y][s]; ar = PL.AR_TXT[(y, s)]
        title = (base["title"], ar[0]); obj = (base["obj"][0].upper() + base["obj"][1:], ar[1]); trace = (base["trace"], ar[2])
        spec = CD.SPEC[(y, s)]; seed = int(y) * 100 + s
    notions = [i for i in NID if i in p["new"] + p["deep"]]
    fill = spec.get("fill") or fill_from(notions)
    retain = spec.get("retain") or retain_from(notions) or [("Je relis ma fiche et je termine les parties à compléter.", "أعيد قراءة مذكرتي وأكمل الأجزاء الناقصة.")]
    # boîte à mots : tous les mots à écrire dans les phrases à trous
    wf, wa = [], []
    for pair in fill:
        a, b = words(pair); wf += a; wa += b
    rnd = random.Random(seed); rnd.shuffle(wf); rnd.shuffle(wa)
    bank = '<div class="bank"><b>' + tp("Mots à placer :", "كلمات للاستعمال:") + "</b> " + both(lambda l: " ".join(f'<span class="wd">{escape(w)}</span>' for w in (wa if l == "ar" else wf))) + "</div>" if wf else ""
    fills = '<ol class="fills">' + "".join(f"<li>{t(x)}</li>" for x in fill) + "</ol>" + bank
    form = "".join(render(x) for x in spec["form"])
    scr = render_script(spec["script"], None) if spec.get("script") else ""
    nums = lambda lst: " · ".join(str(n) for n in lst)
    acts = ""
    if p["core"] or p["support"] or p["challenge"]:
        parts = []
        if p["core"]: parts.append(f'<b>{nums(p["core"])}</b>')
        if p["support"]: parts.append(nums(p["support"]))
        if p["challenge"]: parts.append(f'({nums(p["challenge"])})')
        acts = f'<p class="acts">{tp("Activités du site pour s’entraîner :", "أنشطة الموقع للتدرّب:")} <span dir="ltr">{" · ".join(parts)}</span></p>'
    acq = ""
    if p["acq"]:
        acq = '<ul class="acq">' + "".join(f'<li><span class="cb">☐</span> {t(a)}</li>' for a in p["acq"]) + "</ul>"
    n_sec = 1
    def sec(label, inner, cls=""):
        nonlocal n_sec
        h = f'<h2><span class="no">{n_sec}</span> {label}</h2>'; n_sec += 1
        return f'<section class="sec {cls}">{h}{inner}</section>'
    secs = sec(tp("Je complète", "أكمل"), fills)
    secs += sec(f'{tp("Trace écrite", "الأثر المكتوب")} : <span class="tr">{t(trace)}</span>', form)
    if scr: secs += sec(tp("Je termine le script en classe", "أنهي السكربت في القسم"), scr)
    secs += sec(tp("Ce que je retiens", "ما أحتفظ به"), '<ul class="ret">' + "".join(f"<li>{t(r)}</li>" for r in retain) + "</ul>", "retain")
    lv = YEAR[y]
    head = (f'<header class="fh"><div class="top"><span class="lv">{t(lv)}</span><span class="ft">{tp("Cahier de l’élève · Séance", "دفتر التلميذ · الحصة")} {s}</span>'
            f'<span class="who">{tp("Nom et prénom", "الاسم واللقب")} : <i></i> {tp("Classe", "القسم")} : <i class="s"></i> {tp("Date", "التاريخ")} : <i class="s"></i></span></div>'
            f'<h1>{t(title)}</h1><p class="obj"><b>{tp("Objectif", "الهدف")} :</b> {t(obj)}</p></header>')
    return f'<section class="fiche" id="s{s}" data-s="{s}">{head}{secs}<footer>{acq}{acts}</footer></section>'


# ----------------------------------------------------------------------------- page d'un niveau
CSS = r'''
:root{--ink:#1d2433;--line:#9aa5b8;--blue:#1e4fa8;--soft:#eef3fb}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:#e9edf4;color:var(--ink);font-family:"Segoe UI","Tahoma","Arial","Noto Sans Arabic",sans-serif;font-size:11.5pt;line-height:1.5}
body.lang-ar .fr,body.lang-fr .ar{display:none!important}
.bar{position:sticky;top:0;z-index:5;background:#1e4fa8;color:#fff;padding:8px 14px;display:flex;flex-wrap:wrap;gap:10px;align-items:center;font-size:14px}
.bar a{color:#fff}.bar button,.bar select{font:inherit;font-size:14px;border-radius:7px;border:1px solid #fff;background:#fff;color:#1e4fa8;padding:3px 12px;cursor:pointer}
.bar button[aria-pressed=true]{background:#ffd24d;border-color:#ffd24d;color:#222;font-weight:700}.bar label{display:inline-flex;gap:5px;align-items:center;cursor:pointer}.bar .hint{font-size:12.5px;opacity:.9;flex-basis:100%}
.pages{display:flex;flex-direction:column;align-items:center;gap:16px;padding:16px 8px 40px}
.fiche{background:#fff;width:210mm;min-height:297mm;padding:8mm 10mm;box-shadow:0 2px 10px rgba(0,0,0,.18);position:relative}
.fh .top{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;font-size:10pt;border-bottom:2px solid var(--blue);padding-bottom:3px}
.lv{background:var(--blue);color:#fff;border-radius:999px;padding:0 10px;font-weight:700}.ft{font-weight:700;color:var(--blue)}.who{margin-inline-start:auto;display:inline-flex;gap:6px;align-items:baseline}
.who i{display:inline-block;width:46mm;border-bottom:1.2px dotted #444;height:1em}.who i.s{width:20mm}
.fh h1{font-size:15.5pt;margin:5px 0 1px;line-height:1.3;color:#122a5c}.obj{margin:0 0 4px;font-size:10.5pt;color:#333}
.sec{margin:5px 0 0}.sec h2{font-size:11.5pt;margin:0 0 3px;color:var(--blue);display:flex;align-items:center;gap:7px;line-height:1.3}.sec h2 .no{display:inline-flex;align-items:center;justify-content:center;width:19px;height:19px;border-radius:50%;background:var(--blue);color:#fff;font-size:10pt;flex:none}.tr{color:#333;font-weight:600}
.fills{margin:0;padding-inline-start:22px;display:flex;flex-direction:column;gap:3px}.fills li{line-height:1.6}
.bl{border-bottom:1.5px dotted #333;padding:0 3px}.ans{visibility:hidden}body.corrige .ans{visibility:visible;color:#b3261e;font-weight:600}
.bank{margin-top:4px;border:1px dashed #8a94a6;border-radius:8px;padding:2px 8px;font-size:10pt;background:#fafbfd}.wd{display:inline-block;border:1px solid #c4cbd8;border-radius:5px;padding:0 6px;margin:1px 2px;background:#fff}
table.ft,table.fc{width:100%;border-collapse:collapse;table-layout:fixed;margin:4px 0;font-size:10.5pt}.ft th,.ft td,.fc th,.fc td{border:1.2px solid var(--line);padding:3px 7px;vertical-align:top;text-align:start;word-wrap:break-word}
.ft thead th{background:var(--soft);color:#1e3a6e}.ft tbody th,.fc th{background:var(--soft);color:#1e3a6e;font-weight:700}.ft tr.tall td{height:8.4mm}
.wl{display:block;border-bottom:1.2px dotted #666;height:6.6mm}.wr{display:block;min-height:6mm}
.blk{display:inline-block;color:#fff;font-weight:600;font-size:9.5pt;line-height:1.35;padding:2px 9px;border-radius:5px;margin:1px 0}
.blk.ev{background:#c78a00}.blk.mv{background:#3f7ee0}.blk.lk{background:#8a55d7}.blk.sn{background:#b448b0}.blk.ct{background:#d68a00}.blk.se{background:#2a9fc9}.blk.op{background:#3fa854}.blk.va{background:#e0592a}.blk.pen{background:#0f9e7a}.blk.my{background:#e0506b}
.cols{display:grid;gap:10px;align-items:start}svg{direction:ltr}.fig svg{width:100%;height:auto;display:block;border:1px solid #c4cbd8;border-radius:6px}.fig.small{max-width:62mm}.fig.plane{max-width:78mm}
.cards{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}.crd{display:inline-flex;width:12mm;height:12mm;align-items:center;justify-content:center;border:1.5px solid #333;border-radius:7px;font-size:15pt}.crd.blank{border-style:dashed;background:#fafbfd}.crd.shown{background:#e7f0ff}
.ftxt{margin:3px 0;font-size:10.5pt}.flow{display:flex;flex-direction:column;align-items:center;gap:0;margin:3px 0 5px}.fb{border:1.5px solid #1e4fa8;border-radius:8px;padding:2px 14px;background:#fff;min-width:60mm;text-align:center;font-size:10.5pt}.fb.start,.fb.end{border-radius:999px;background:var(--soft)}.fa{line-height:1;font-size:12pt;color:#e8861c;font-weight:700}
.actl{margin:2px 0;font-size:10.5pt}.svs{display:flex;flex-wrap:wrap;gap:12px;align-items:flex-start;margin:3px 0}.sv svg{max-width:100%;height:auto;display:block}.sv{border:1px solid #d3d9e6;border-radius:8px;padding:5px;background:#fff}
.frame{border:2px dashed #7b8598;border-radius:8px;min-width:70mm;display:flex;align-items:flex-start;padding:4px 8px}.hintx{font-size:9.5pt;color:#7b8598}
.stu{display:block}.cor{display:none}body.corrige .stu{display:none}body.corrige .cor{display:block}
.sq{margin:2px 0;padding-inline-start:22px;font-size:10.5pt}.sq li{line-height:1.6}
.retain{border:1.5px solid #2e9e5b;border-radius:8px;padding:3px 10px 4px;background:#f3fbf5}.retain h2{color:#1d6b3b}.retain h2 .no{background:#2e9e5b}.ret{margin:0;padding-inline-start:20px}
footer{margin-top:6px;font-size:10pt}.acq{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:1px}.cb{font-size:12pt}.acts{margin:3px 0 0;color:#444}
.fiche.hide{display:none}
@page{size:A4;margin:0}
@media print{body{background:#fff}.bar{display:none}.pages{padding:0;gap:0;display:block}.fiche{box-shadow:none;margin:0;width:210mm;height:297mm;min-height:0;overflow:hidden;break-after:page;page-break-after:always}.fiche:last-child{break-after:auto;page-break-after:auto}.fiche.hide{display:none}}
'''

JS = r'''
(function(){
  var q = new URLSearchParams(location.search), lang = q.get("lang"), b = document.body;
  try { if (!lang) lang = localStorage.getItem("ateliers-contes-lang"); } catch (e) {}
  if (lang !== "fr") lang = "ar";
  function setLang(l){ b.classList.toggle("lang-ar", l === "ar"); b.classList.toggle("lang-fr", l === "fr"); document.documentElement.lang = l; document.documentElement.dir = l === "ar" ? "rtl" : "ltr";
    document.querySelectorAll("[data-lang]").forEach(function(x){ x.setAttribute("aria-pressed", String(x.dataset.lang === l)); }); try { localStorage.setItem("ateliers-contes-lang", l); } catch (e) {} }
  document.querySelectorAll("[data-lang]").forEach(function(x){ x.addEventListener("click", function(){ setLang(x.dataset.lang); }); });
  var c = document.getElementById("corr"); function setCorr(){ b.classList.toggle("corrige", c.checked); } c.addEventListener("change", setCorr);
  if (q.get("corrige") === "1") { c.checked = true; } setCorr(); setLang(lang);
  var sel = document.getElementById("sel");
  function filter(){ var v = sel.value; document.querySelectorAll(".fiche").forEach(function(f){ f.classList.toggle("hide", !!v && f.dataset.s !== v); }); }
  sel.addEventListener("change", filter);
  document.getElementById("prt").addEventListener("click", function(){ window.print(); });
})();
'''


def page(y):
    seances = sorted(PL.PLAN[y])
    extra = ["M1", "M2", "M3", "A1", "A2", "A3"] if y == "9" else []
    fiches = "".join(fiche(y, s) for s in seances + extra)
    lv = YEAR[y]
    sel = "".join(f'<option value="{s}">{s} · {escape(S.SEANCES[y][s - 1]["title"])}</option>' for s in seances) + "".join(f'<option value="{k}">{k} · {escape(__import__("cahier_extra").EXTRA[k]["title"][0])}</option>' for k in extra)
    html = f'''<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(lv[1])} — دفتر التلميذ · {escape(lv[0])} — Cahier de l’élève</title><style>{CSS}</style></head>
<body class="lang-ar">
<div class="bar"><a href="../index.html#planning-{y}">← <span class="ar">الموقع</span><span class="fr">Retour au site</span></a>
<button type="button" data-lang="ar" aria-pressed="true">العربية</button><button type="button" data-lang="fr" aria-pressed="false">Français</button>
<label><input type="checkbox" id="corr"> <span class="ar">عرض الإجابات (للأستاذ)</span><span class="fr">Afficher le corrigé (enseignant)</span></label>
<select id="sel" aria-label="séance"><option value="">— {escape("كل الحصص / Toutes les séances")} —</option>{sel}</select>
<button type="button" id="prt"><span class="ar">طباعة</span><span class="fr">Imprimer</span></button>
<span class="hint"><span class="ar">كل حصة في ورقة A4 واحدة، للطباعة واللصق في الدفتر. تُطبع الأجزاء الفارغة ليكملها التلاميذ؛ وتظهر الإجابات بالأحمر عند تفعيل «عرض الإجابات». اقتراح غير رسمي قابل للتعديل.</span><span class="fr">Une fiche A4 par séance, à imprimer et à coller dans le cahier. Les parties vides sont à compléter par les élèves ; le corrigé apparaît en rouge si l’on coche « Afficher le corrigé ». Proposition non officielle, à adapter.</span></span></div>
<main class="pages">{fiches}</main>
<script>{JS}</script></body></html>'''
    return html


def build():
    n = 0
    for y in PL.YEAR_ORDER:
        open(os.path.join(OUT, f"cahier-{y}.html"), "w", encoding="utf-8").write(page(y)); n += len(PL.PLAN[y])
    return n


def pdfs():
    """imprime les pages en PDF avec Chromium (Playwright) : cahier-N-{ar,fr}[-corrige].pdf"""
    js = os.path.join(HERE, "cahier_pdf.js")
    subprocess.run(["node", js, OUT], check=True)


if __name__ == "__main__":
    n = build(); print(n, "fiches écrites dans", OUT)
    if "--pdf" in sys.argv: pdfs()
