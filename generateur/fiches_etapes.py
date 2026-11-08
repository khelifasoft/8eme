"""Images des étapes pour les pages de fiche d'activité : fiches-activite/etapes/
 - catch-1..6.svg : étapes du jeu « Attrape les poissons » (composées à partir des images du projet .sb3)
 - <conte>-1..n.svg : scènes de chaque conte
Usage : python3 generateur/fiches_etapes.py"""
import os, sys, json, zipfile, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
sys.argv = [sys.argv[0], os.path.join(ROOT, "jeux")]
import jeux3 as J3, scratch as sc
from jeux2 import nest
from xml.sax.saxutils import escape
OUT = os.path.join(ROOT, "fiches-activite", "etapes"); os.makedirs(OUT, exist_ok=True)

def sb3_art(path):
    z = zipfile.ZipFile(path); p = json.loads(z.read("project.json")); res = {}
    for t in p["targets"]:
        c = t["costumes"][0]; svg = z.read(c["md5ext"]).decode("utf-8")
        m = re.match(r'<svg[^>]*', svg); W = float(re.search(r'width="([\d.]+)', m.group(0)).group(1)); H = float(re.search(r'height="([\d.]+)', m.group(0)).group(1))
        res[t["name"]] = dict(svg=svg, w=W, h=H, rcx=c.get("rotationCenterX", W / 2), rcy=c.get("rotationCenterY", H / 2), size=t.get("size") or 100)
    return res
def place(a, x, y, size=None):
    s = (size or a["size"]) / 100; tx, ty = 240 + x - a["rcx"] * s, 180 - y - a["rcy"] * s
    inner = re.sub(r'^<\?xml[^>]*>\s*', '', a["svg"].strip()).replace("<svg", '<svg x="0" y="0"', 1)
    return f'<g transform="translate({tx:.1f},{ty:.1f}) scale({s})">{inner}</g>'
def hud(score, lives):
    return (f'<rect x="8" y="8" width="118" height="26" rx="8" fill="#fff" fill-opacity=".92" stroke="#1f4aa8" stroke-width="2"/><text x="18" y="26" font-family="Arial" font-size="14" font-weight="bold" fill="#1f4aa8">Points : {score}</text>'
            f'<rect x="354" y="8" width="118" height="26" rx="8" fill="#fff" fill-opacity=".92" stroke="#c0392b" stroke-width="2"/><text x="364" y="26" font-family="Arial" font-size="14" font-weight="bold" fill="#c0392b">Vies : {lives}</text>')
def tag(txt, x, y, color="#e8861c"):
    w = 9 * len(txt) + 18
    return f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="14" fill="{color}"/><text x="{x + w/2}" y="{y + 19}" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#fff">{escape(txt)}</text>'
def arrow(x1, y1, x2, y2, color="#e8861c"):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="5" stroke-dasharray="9 6" marker-end="url(#ah)"/>'
CATCH = [  # (caption, titre court, scène)
 ("Je clique sur le drapeau vert : le score est mis à 0, les vies à 3 et la vitesse à 3.", "Début de partie"),
 ("Un poisson apparaît en haut de la scène, à une position choisie au hasard, et il tombe.", "Un poisson tombe"),
 ("Je déplace la souris : le joueur suit la souris et se place sous le poisson.", "Je déplace la souris"),
 ("Si le joueur touche le poisson : le score augmente de 1 et un nouveau poisson apparaît.", "Poisson attrapé"),
 ("Si le poisson touche le bas de la scène : les vies diminuent de 1.", "Poisson manqué"),
 ("Quand les vies arrivent à 0, le jeu s'arrête : c'est la fin de la partie.", "Fin de partie")]
def catch():
    A = sb3_art(os.path.join(ROOT, "jeux", "jeu_sindbad.sb3")); back, pl, it = A["Stage"], A["اللاعب"], A["الشيء"]
    defs = '<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#e8861c"/></marker></defs>'
    S = [  # (joueur x, objet (x,y) ou None, score, vies, décor supplémentaire)
     (0, None, 0, 3, tag("1  Drapeau vert", 160, 150)),
     (0, (-90, 150), 0, 3, arrow(150, 70, 150, 150) + tag("2  Chute", 215, 120)),
     (60, (-90, 10), 0, 3, arrow(300, 275, 150, 275) + tag("3  Souris", 300, 215)),
     (-90, (-90, -95), 1, 3, tag("+1 point", 150, 135, "#2e9e5b")),
     (-90, (120, -150), 1, 2, tag("−1 vie", 300, 240, "#c0392b")),
     (-90, None, 7, 0, f'<rect x="0" y="0" width="480" height="360" fill="#000" fill-opacity=".45"/><text x="240" y="195" text-anchor="middle" font-family="Arial" font-size="58" font-weight="bold" fill="#fff">FIN</text>')]
    for n, (px, itx, sc_, lv, extra) in enumerate(S, 1):
        body = defs + place(back, 0, 0, 100) + place(pl, px, -125) + (place(it, *itx) if itx else "") + hud(sc_, lv) + extra
        open(os.path.join(OUT, f"catch-{n}.svg"), "w", encoding="utf-8").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">{body}</svg>')
    return [dict(img=f"fiches-activite/etapes/catch-{n}.svg", t=CATCH[n - 1][1], c=CATCH[n - 1][0]) for n in range(1, 7)]
def contes():
    out = {}
    for key in sc.D:
        n = len(sc.D[key]["scenes"]); out[key] = []
        for i in range(n):
            open(os.path.join(OUT, f"{key}-{i+1}.svg"), "w", encoding="utf-8").write(J3.scene_svg(key, i))
            out[key].append(dict(img=f"fiches-activite/etapes/{key}-{i+1}.svg", t=f"Scène {i+1}", c=J3.caption(key, i)))
    return out
def export():
    return dict(catch=catch(), contes=contes())
if __name__ == "__main__":
    e = export(); json.dump(e, open(os.path.join(HERE, "etapes.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("étapes :", len(e["catch"]), {k: len(v) for k, v in e["contes"].items()})
