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
    sol[str(n)] = dict(script=img(a["img"]["script"]), tok=[tok(t) for t in a["tok"]])
put("content/public/activites.json", dict(title=bi(A["title"]), intro=bi(A["intro"]), levels=levels, blocks=blocks, acts=acts))
put("content/private/activites-solutions.json", sol)

# bibliothèque de jeux de la 8eme (31) ; les 4 jeux guidés ont en plus une fiche, des étapes en images et des solutions
CATS = {}
games = []
for g in DATA["games"]:
    fid = g.get("fiche")
    for rel in (g["cover"], g["file"]) + ((g["video"],) if g.get("video") else ()): cp(rel, rel)
    CATS.setdefault(g["cat"], dict(key=g["cat"], t=dict(ar=g["cat_ar"], fr=eme(g["cat_fr"]))))
    o = dict(key=g["key"], cat=g["cat"], title=dict(ar=g["title_ar"], fr=eme(g["title_fr"])), how=dict(ar=g["how_ar"], fr=eme(g["how_fr"])), cover="/" + g["cover"], sb3="/" + g["file"], video="/" + g["video"] if g.get("video") else None, fiche=fid)
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
# cahier de l'élève (fiches à imprimer et à coller) : fichiers autonomes
for f in ["cahier-8.html"] + [f"cahier-8-{l}{c}.pdf" for l in ("ar", "fr") for c in ("", "-corrige")]:
    src = os.path.join(ROOT, "cahier", f); dst = os.path.join(DEST, "public", "cahier", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
    if f.endswith(".html"): open(dst, "w", encoding="utf-8").write(open(src, encoding="utf-8").read().replace("../index.html#planning-8", "/"))
    else: shutil.copy(src, dst)
print("activités", len(acts), "jeux", len(games), "étapes pensée", len(pensee["steps"]), "fichiers copiés", len(copied), "| sans traduction FR :", len(miss))
for m in sorted(miss)[:10]: print("   ", m[:80])
