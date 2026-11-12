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
def bi(s):
    if s is None or s == "": return dict(ar="", fr="")
    f = FR.get(s) or FR.get(s.strip())
    if not f: miss.add(s)
    return dict(ar=s, fr=f or s)
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

# jeux guidés de la 8e année : fiche + étapes en images + solutions de chaque étape
games = []
for g in DATA["games"]:
    if g["key"] not in ("sindbad", "course", "saut", "labyrinthe"): continue
    fid = g["fiche"]; F = DATA["fiches"][fid]
    for rel in (g["cover"], g["file"]) + ((g["video"],) if g.get("video") else ()): cp(rel, rel)
    steps = [dict(img=img([e["img"], e["img_ar"]]), t=bi(e["t"]), c=bi(e["c"])) for e in DATA["etapes"][fid]]
    games.append(dict(key=g["key"], fiche=fid, title=dict(ar=g["title_ar"], fr=g["title_fr"]), how=dict(ar=g["how_ar"], fr=g["how_fr"]), cover="/" + g["cover"], sb3="/" + g["file"], video="/" + g["video"] if g.get("video") else None,
        fi=dict(title=bi(F["title"]), meta=bi(F["meta"]), situation=bi(F["situation"]), steps=lst(F["steps"]), eleve=lst(F["eleve"]), criteres=lst(F["criteres"]), allegee=bi(F["allegee"]), prolongement=bi(F["prolongement"])), etapes=steps))
put("content/public/jeux.json", games)
gs = {}
for fid, lst_ in DATA["solutions"]["steps"].items():
    gs[fid] = [dict(sprite=bi(s["sprite"]), tok=[tok(t) for t in s["tok"]]) for s in lst_]
put("content/private/jeux-solutions.json", gs)
print("activités", len(acts), "jeux", len(games), "fichiers copiés", len(copied), "| sans traduction FR :", len(miss))
for m in sorted(miss)[:10]: print("   ", m[:80])
