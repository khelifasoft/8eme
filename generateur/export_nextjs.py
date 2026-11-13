"""Exporte le contenu de la 8e année vers le dépôt de la nouvelle application (khelifasoft/8eme-nextjs-postgres).
Lit DATA et FRMAP dans index.html (généré par page.py) ; écrit :
  content/public/*.json     contenu visible par tous (arabe + français)
  content/private/*.json    solutions : lues uniquement côté serveur, jamais servies telles quelles
  public/img, public/jeux   images et fichiers utilisés
Usage : python3 generateur/export_nextjs.py [../8eme-nextjs-postgres]"""
import json, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
DEST = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "..", "8eme-nextjs-postgres"))
h = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
dec = json.JSONDecoder()
DATA, _ = dec.raw_decode(h[h.index("const DATA = ") + 13:])
FR, _ = dec.raw_decode(h[h.index("const FRMAP = ") + 14:])
miss = set()
def eme(t): return re.sub(r"\b8(?:e|ème)\b", "8eme", t)
def bi(s):
    if s is None or s == "": return dict(ar="", fr="")
    f = FR.get(s) or FR.get(s.strip())
    if not f: miss.add(s)
    return dict(ar=s, fr=eme(f or s))
def lst(a): return [bi(x) for x in a]
def put(path, obj):
    p = os.path.join(DEST, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(obj, open(p, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":")); return p
copied = set()
def cp(rel, to=None):
    src = os.path.join(ROOT, rel); dst = os.path.join(DEST, "public", to or rel.replace("fiches-activite/", "img/"))
    if (src, dst) in copied: return
    os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy(src, dst); copied.add((src, dst))
def img(pair):   # [fr, ar] -> chemins publics
    for r in pair: cp(r)
    return dict(fr="/" + pair[0].replace("fiches-activite/", "img/"), ar="/" + pair[1].replace("fiches-activite/", "img/"))
def tok(t):
    o = dict(c=t["c"], k=t["k"], d=t["d"], t=bi(t["t"]))
    if "cond" in t: o.update(pre=bi(t["pre"]), cond=bi(t["cond"]), post=bi(t["post"]) if t["post"] else None)
    return o

A = DATA["activites"]
levels = [dict(n=l["n"], t=bi(l["t"]), diff=bi(l["diff"]), obj=bi(l["obj"]), count=l["count"]) for l in A["levels"]]
blocks = {k: dict(c=v[0], t=bi(v[1]), help=bi(v[2])) for k, v in A["blocks"].items()}
acts, sol = [], {}
for a in A["acts"]:
    n = int(a["n"])
    acts.append(dict(n=n, lvl=int(a["lvl"]), t=bi(a["t"]), obj=bi(a["obj"]), blocks=a["blocks"], steps=lst(a["steps"]), res=bi(a["res"]), defi=bi(a["defi"]), light=bi(a["light"]),
                     img=dict(avant=img(a["img"]["avant"]), apres=img(a["img"]["apres"]))))
    sol[str(n)] = dict(tok=[tok(t) for t in a["tok"]])   # PAS d'image « script » : elle serait un fichier public à l'adresse devinable
put("content/public/activites.json", dict(title=bi(A["title"]), intro=bi(A["intro"]), levels=levels, blocks=blocks, acts=acts))
put("content/private/activites-solutions.json", sol)

# bibliothèque de jeux de la 8eme (31) ; les 4 jeux guidés ont en plus une fiche, des étapes en images et des solutions
CATS = {}
games = []
for g in DATA["games"]:
    fid = g.get("fiche")
    for rel in (g["cover"],) + (() if fid else (g["file"],)) + ((g["video"],) if g.get("video") else ()): cp(rel, rel)
    if fid:   # projet complet = code final du jeu : privé (content/private/jeux), jamais dans public/
        os.makedirs(os.path.join(DEST, "content", "private", "jeux"), exist_ok=True); shutil.copy(os.path.join(ROOT, g["file"]), os.path.join(DEST, "content", "private", "jeux", os.path.basename(g["file"])))
    CATS.setdefault(g["cat"], dict(key=g["cat"], t=dict(ar=g["cat_ar"], fr=eme(g["cat_fr"]))))
    o = dict(key=g["key"], cat=g["cat"], title=dict(ar=g["title_ar"], fr=eme(g["title_fr"])), how=dict(ar=g["how_ar"], fr=eme(g["how_fr"])), cover="/" + g["cover"], sb3=(f"/api/jeu/{g['key']}" if fid else "/" + g["file"]), video="/" + g["video"] if g.get("video") else None, fiche=fid)
    rs = (DATA.get("ressources") or {}).get(g.get("res") or "")
    if rs:   # images et sons du jeu à télécharger (page « Ressources »)
        cp(rs["zip"], rs["zip"])
        for it in rs["items"]: cp(it["file"], it["file"])
        o["ressources"] = dict(zip="/" + rs["zip"], items=[dict(file="/" + it["file"], type=it["type"], t=dict(ar=it["ar"], fr=eme(it["fr"]))) for it in rs["items"]])
    if fid:
        F = DATA["fiches"][fid]
        o["fi"] = dict(title=bi(F["title"]), meta=bi(F["meta"]), situation=bi(F["situation"]), steps=lst(F["steps"]), eleve=lst(F["eleve"]), criteres=lst(F["criteres"]), allegee=bi(F["allegee"]), prolongement=bi(F["prolongement"]))
        o["etapes"] = [dict(img=img([e["img"], e["img_ar"]]), t=bi(e["t"]), c=bi(e["c"])) for e in DATA["etapes"][fid]]
    games.append(o)
put("content/public/jeux.json", dict(cats=list(CATS.values()), games=games))
gs = {}
for fid, lst_ in DATA["solutions"]["steps"].items():
    gs[fid] = [dict(sprite=bi(s["sprite"]), tok=[tok(t) for t in s["tok"]]) for s in lst_]
put("content/private/jeux-solutions.json", gs)

# « Pensée logique et programmation » (8eme) : compétences, détails de l'Aide pédagogique 2026, parcours, projets, exercices
C = DATA["curriculum"]; P8 = C["pages"]["8-prog"]; AI = P8["aide"]; PA = DATA["parcours"]["8"]
def two(ar, fr): return [dict(ar=a, fr=eme(f)) for a, f in zip(ar, fr)]
models = lambda ms: [m.split("/")[1] for m in ms if m.startswith("game:")]
pensee = dict(
    title=dict(ar=P8["title_ar"], fr=eme(P8["title_fr"])), year=dict(ar=C["years"]["8"]["ar"], fr="8eme année"),
    comps=two(P8["comps_ar"], P8["comps_fr"]), life=dict(ar=P8["life_ar"], fr=eme(P8["life_fr"])),
    aide=dict(comp=dict(ar=AI["comp_ar"], fr=eme(AI["comp_fr"])), parts=[dict(t=dict(ar=x["t_ar"], fr=eme(x["t_fr"])), items=two(x["i_ar"], x["i_fr"])) for x in AI["parts"]],
              know=two(AI["know_ar"], AI["know_fr"]), cad=two(AI["cad_ar"], AI["cad_fr"]), note=dict(ar=C["aide_ar"], fr=eme(C["aide_fr"]))),
    src=dict(ar=C["src_ar"], fr=eme(C["src_fr"])),
    steps=[dict(t=bi(s["t"]), comp=bi(s["comp"]), acts=lst(s["acts"]), sais=lst(s["sais"]), models=models(s["models"])) for s in PA["steps"]],
    projets=[dict(t=bi(p["t"]), lvl=p["lvl"], brief=bi(p["brief"]), req=lst(p["req"]), models=models(p["models"])) for p in PA["projets"]],
    livrables=bi(DATA["parcours"]["livrables"]),
    quiz=[dict(q=dict(ar=x["q"], fr=eme(x["q_fr"])), o=two(x["o"], x["o_fr"]), a=x["a"]) for x in DATA["exo"]["8-prog"]],
    todo=[dict(t=dict(ar=a["t"], fr=eme(a["t_fr"])), d=dict(ar=a["d"], fr=eme(a["d_fr"])), ex=dict(ar=a.get("ex", ""), fr=eme(a.get("ex_fr", "")))) for a in DATA["act"]["8-prog"]])
put("content/public/pensee.json", pensee)
# chapitres de la 8eme (menu) : un par domaine du programme, dans l'ordre officiel ; « prog » garde sa page riche (pensee.json)
chapters = []
for k in C["by_year"]["8"]:
    pg = C["pages"]["8-" + k]; ai = pg.get("aide")
    chapters.append(dict(key=k, title=dict(ar=pg["title_ar"], fr=eme(pg["title_fr"])), comps=two(pg["comps_ar"], pg["comps_fr"]), life=dict(ar=pg["life_ar"], fr=eme(pg["life_fr"])),
        aide=dict(comp=dict(ar=ai["comp_ar"], fr=eme(ai["comp_fr"])), parts=[dict(t=dict(ar=x["t_ar"], fr=eme(x["t_fr"])), items=two(x["i_ar"], x["i_fr"])) for x in ai["parts"]], know=two(ai["know_ar"], ai["know_fr"]), cad=two(ai["cad_ar"], ai["cad_fr"])) if ai else None))
put("content/public/chapitres.json", dict(year=dict(ar=C["years"]["8"]["ar"], fr="8eme année"), src=pensee["src"], note=pensee["aide"]["note"], chapters=chapters))
# ---- Sécurité informatique (chapitre « Environnement informatique de travail ») : 4 séances. Le public ne reçoit que les énoncés (blancs vides) ; les corrigés vont dans content/private.
_argv = sys.argv; sys.argv = [_argv[0], ROOT]
import securite as SECMOD
sys.argv = _argv
BL = re.compile(r"\{\{(.*?)\}\}")
def pr(p): return dict(ar="", fr="") if p is None else dict(ar=p[1], fr=eme(p[0]))                       # [fr, ar] -> {ar, fr}
def blank(p): return dict(ar="", fr="") if p is None else dict(ar=BL.sub("{{}}", p[1]), fr=eme(BL.sub("{{}}", p[0])))   # blancs sans réponse
SU = DATA["securite"]; sdat = {x["k"]: x for x in SU["seances"]}
seances, ssol = [], {}
for k, x in SECMOD.SEC.items():
    d = sdat[k]
    for lang in ("ar", "fr"): cp(d["video"][lang], d["video"][lang]); 
    shots = {lang: d["img"][0 if lang == "ar" else 1] for lang in ("ar", "fr")}
    for lang in ("ar", "fr"): cp(shots[lang], "img/securite/" + os.path.basename(shots[lang]))
    forms, solforms = [], []
    for f in x["form"]:
        if f["k"] == "table":
            forms.append(dict(kind="table", cols=[pr(c) for c in f["cols"]], rows=[[blank(c) for c in r] for r in f["rows"]]))
            solforms.append(dict(cols=[pr(c) for c in f["cols"]], rows=[[pr(c) for c in r] for r in f["rows"]]))
        else:   # carte à remplir librement (réflexes personnels) : pas de corrigé
            forms.append(dict(kind="card", fields=[dict(label=pr(fl[0]), lines=fl[2]) for fl in f["fields"]])); solforms.append(None)
    seances.append(dict(k=k, n=d["n"], title=pr(x["title"]), obj=pr(x["obj"]), cas=pr(x["cas"]), act=pr(x["act"]), trace=pr(x["trace"]),
        phases=[dict(t=pr(p[0]), min=p[1], d=pr(p[2])) for p in x["phases"]], video=dict(ar="/" + d["video"]["ar"], fr="/" + d["video"]["fr"]),
        shot=dict(ar="/img/securite/" + os.path.basename(shots["ar"]), fr="/img/securite/" + os.path.basename(shots["fr"])),
        fill=[blank(p) for p in x["fill"]], forms=forms, retain=[pr(p) for p in x["retain"]], acq=[pr(p) for p in x["acq"]]))
    ssol[k] = dict(fill=[pr(p) for p in x["fill"]], forms=solforms)
put("content/public/securite.json", dict(title=bi(SU["ui"]["title"]), intro=bi(SU["ui"]["intro"]), note=bi(SU["ui"]["note"]),
    map=[dict(r=bi(m["r"]), w=bi(m["w"]), p=bi(m["p"])) for m in SU["map"]], seances=seances))
put("content/private/securite-solutions.json", ssol)

# ---- cahier de l'élève (8eme) : la version publique ne contient AUCUNE réponse ; corrigés (HTML complet, PDF) réservés aux enseignants validés
from bs4 import BeautifulSoup
src_html = open(os.path.join(ROOT, "cahier", "cahier-8.html"), encoding="utf-8").read()
soup = BeautifulSoup(src_html, "html.parser")
for a in soup.select("span.ans"): a.string = " " * max(8, int(len(a.get_text()) * 1.3))        # la largeur du blanc est conservée, la réponse disparaît
for c in soup.select(".cor"): c.decompose()                                                              # blocs de corrigé
for lab in soup.find_all("label"):
    if lab.find(id="corr"): lab.decompose()                                                              # case « corrigé »
pub = str(soup).replace('var c = document.getElementById("corr");', 'var c = { checked: false, addEventListener: function(){} };').replace('if (q.get("corrige") === "1") { c.checked = true; }', "").replace("../index.html#planning-8", "/")
assert 'id="corr"' not in pub and 'class="cor"' not in pub
os.makedirs(os.path.join(DEST, "public", "cahier"), exist_ok=True); open(os.path.join(DEST, "public", "cahier", "cahier-8.html"), "w", encoding="utf-8").write(pub)
os.makedirs(os.path.join(DEST, "content", "private", "cahier"), exist_ok=True); open(os.path.join(DEST, "content", "private", "cahier", "cahier-8-corrige.html"), "w", encoding="utf-8").write(src_html.replace("../index.html#planning-8", "/"))
for f in [f"cahier-8-{l}.pdf" for l in ("ar", "fr")]: shutil.copy(os.path.join(ROOT, "cahier", f), os.path.join(DEST, "public", "cahier", f))
for f in [f"cahier-8-{l}-corrige.pdf" for l in ("ar", "fr")]: shutil.copy(os.path.join(ROOT, "cahier", f), os.path.join(DEST, "content", "private", "cahier", f))
for f in [f"cahier-8-{l}-corrige.pdf" for l in ("ar", "fr")]:   # ne laisser aucun corrigé dans public/ (ancien export)
    p = os.path.join(DEST, "public", "cahier", f)
    if os.path.exists(p): os.remove(p)

import glob
for p in glob.glob(os.path.join(DEST, "public", "img", "activites", "*-script*.svg")) + [os.path.join(DEST, "public", g["file"]) for g in DATA["games"] if g.get("fiche")]:
    if os.path.exists(p): os.remove(p)
print("activités", len(acts), "jeux", len(games), "étapes pensée", len(pensee["steps"]), "fichiers copiés", len(copied), "| sans traduction FR :", len(miss))
for m in sorted(miss)[:10]: print("   ", m[:80])
