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
LBL = {"fr": dict(points="Points : ", vies="Vies : ", flag="1  Drapeau vert", fall="2  Chute", mouse="3  Souris", plus="+1 point", minus="−1 vie", fin="FIN"),
       "ar": dict(points="النقاط: ", vies="الأرواح: ", flag="1  العلم الأخضر", fall="2  السقوط", mouse="3  الفأرة", plus="+1 نقطة", minus="−1 روح", fin="النهاية")}
def hud(score, lives, L=LBL["fr"]):
    return (f'<rect x="8" y="8" width="118" height="26" rx="8" fill="#fff" fill-opacity=".92" stroke="#1f4aa8" stroke-width="2"/><text x="18" y="26" font-family="Arial" font-size="14" font-weight="bold" fill="#1f4aa8">{L["points"]}{score}</text>'
            f'<rect x="354" y="8" width="118" height="26" rx="8" fill="#fff" fill-opacity=".92" stroke="#c0392b" stroke-width="2"/><text x="364" y="26" font-family="Arial" font-size="14" font-weight="bold" fill="#c0392b">{L["vies"]}{lives}</text>')
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
    for lang in ("fr", "ar"):
        L = LBL[lang]; suffix = "" if lang == "fr" else "-ar"
        S = [  # (joueur x, objet (x,y) ou None, score, vies, décor supplémentaire)
         (0, None, 0, 3, tag(L["flag"], 160, 150)),
         (0, (-90, 150), 0, 3, arrow(150, 70, 150, 150) + tag(L["fall"], 215, 120)),
         (60, (-90, 10), 0, 3, arrow(300, 275, 150, 275) + tag(L["mouse"], 300, 215)),
         (-90, (-90, -95), 1, 3, tag(L["plus"], 150, 135, "#2e9e5b")),
         (-90, (120, -150), 1, 2, tag(L["minus"], 300, 240, "#c0392b")),
         (-90, None, 7, 0, f'<rect x="0" y="0" width="480" height="360" fill="#000" fill-opacity=".45"/><text x="240" y="195" text-anchor="middle" font-family="Tajawal,Arial,sans-serif" font-size="58" font-weight="bold" fill="#fff">{L["fin"]}</text>')]
        for n, (px, itx, sc_, lv, extra) in enumerate(S, 1):
            body = defs + place(back, 0, 0, 100) + place(pl, px, -125) + (place(it, *itx) if itx else "") + hud(sc_, lv, L) + extra
            open(os.path.join(OUT, f"catch{suffix}-{n}.svg"), "w", encoding="utf-8").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">{body}</svg>')
    return [dict(img=f"fiches-activite/etapes/catch-{n}.svg", img_ar=f"fiches-activite/etapes/catch-ar-{n}.svg", t=CATCH[n - 1][1], c=CATCH[n - 1][0]) for n in range(1, 7)]
COURSE = [("Début de partie", "Je clique sur le drapeau vert : le score est mis à 0, les vies à 3 et la vitesse à 3."),
 ("Je déplace la voiture", "J'appuie sur la flèche gauche ou droite : la voiture se déplace, sans sortir de la route."),
 ("Une voiture arrive", "Une voiture adverse apparaît en haut, à une position choisie au hasard, et descend à la vitesse du jeu."),
 ("Voiture évitée", "Si la voiture passe en bas sans me toucher : le score augmente de 1 et la vitesse de 0,15."),
 ("Voiture touchée", "Si la voiture adverse me touche : je perds une vie (un cœur disparaît) et le son de choc retentit."),
 ("Fin de partie", "Quand les vies arrivent à 0, le jeu affiche « Fin de partie » et s'arrête.")]
CL = {"fr": dict(flag="1  Drapeau vert", keys="2  Flèches ← →", come="3  Voiture adverse", up="+1 point", hit="−1 vie", fin="FIN", sc="النقاط", lv="الأرواح"),
      "ar": dict(flag="1  العلم الأخضر", keys="2  الأسهم ← →", come="3  سيارة معاكسة", up="+1 نقطة", hit="−1 روح", fin="النهاية", sc="النقاط", lv="الأرواح")}
def course():
    import video_jeu as V
    z, T = V.load(os.path.join(ROOT, "jeux", "jeu_course.sb3")); by = {t["name"]: t for t in T}
    def scene(carx, enemy, score, lives, extra, dark=False):
        s = V.place(T[0]["costumes"][0], 0, 0, 100) + V.place(by["الخطوط"]["costumes"][0], 0, 0, 100) + V.place(by["السيارة"]["costumes"][0], carx, -125, 70)
        if enemy: s += V.place(by["سيارة معاكسة"]["costumes"][0], enemy[0], enemy[1], 70)
        if lives: s += V.place(by["القلوب"]["costumes"][lives - 1], 185, 158, 100)
        s += V.monitor("النقاط", score, 4, 4) + V.monitor("الأرواح", lives, 4, 30)
        return s + extra
    for lang in ("fr", "ar"):
        L = CL[lang]; suffix = "" if lang == "fr" else "-ar"
        S = [scene(0, None, 0, 3, tag(L["flag"], 150, 150)),
             scene(-60, None, 0, 3, arrow(250, 235, 190, 235) + tag(L["keys"], 255, 200)),
             scene(-60, (35, 105), 0, 3, arrow(275, 105, 275, 170) + tag(L["come"], 295, 95)),
             scene(55, (-30, -150), 1, 3, tag(L["up"], 140, 150, "#2e9e5b")),
             scene(5, (10, -95), 1, 2, tag(L["hit"], 280, 150, "#c0392b")),
             scene(5, (10, -95), 4, 0, f'<rect x="0" y="0" width="480" height="360" fill="#000" fill-opacity=".5"/><text x="240" y="195" text-anchor="middle" font-family="Tajawal,Arial,sans-serif" font-size="58" font-weight="bold" fill="#fff">{L["fin"]}</text>')]
        defs = '<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#e8861c"/></marker></defs>'
        for n, body in enumerate(S, 1):
            open(os.path.join(OUT, f"course{suffix}-{n}.svg"), "w", encoding="utf-8").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">{defs}{body}</svg>')
    return [dict(img=f"fiches-activite/etapes/course-{n}.svg", img_ar=f"fiches-activite/etapes/course-ar-{n}.svg", t=COURSE[n - 1][0], c=COURSE[n - 1][1]) for n in range(1, 7)]
SAUT = [("Début de partie", "Je clique sur le drapeau vert : le score est mis à 0, les vies à 3 et la vitesse à 3."),
 ("Un buisson arrive", "Un buisson apparaît à droite et avance vers la gauche à la vitesse du jeu."),
 ("Je saute", "J'appuie sur la barre d'espace : le chameau monte, puis retombe (la gravité diminue sa vitesse de 1 à chaque image)."),
 ("Buisson évité", "Si le buisson sort de la scène sans me toucher : le score augmente de 1 et la vitesse de 0,15."),
 ("Buisson touché", "Si le chameau est au sol quand le buisson arrive : je perds une vie (un cœur disparaît) et le son de choc retentit."),
 ("Fin de partie", "Quand les vies arrivent à 0, le jeu affiche « Fin de partie » et s'arrête.")]
SL = {"fr": dict(flag="1  Drapeau vert", come="2  Buisson", jump="3  Barre d'espace", up="+1 point", hit="−1 vie", fin="FIN"),
      "ar": dict(flag="1  العلم الأخضر", come="2  الشجيرة", jump="3  المسافة", up="+1 نقطة", hit="−1 روح", fin="النهاية")}
def saut():
    import video_jeu as V
    z, T = V.load(os.path.join(ROOT, "jeux", "jeu_saut.sb3")); by = {t["name"]: t for t in T}
    def scene(cy, bush, score, lives, extra):
        s = V.place(T[0]["costumes"][0], 0, 0, 100) + V.place(by["الجمل"]["costumes"][0], -120, cy, 50)
        if bush is not None: s += V.place(by["الشجيرة"]["costumes"][0], bush, -120, 40)
        if lives: s += V.place(by["القلوب"]["costumes"][lives - 1], -40, 158, 100)
        return s + V.monitor("النقاط", score, 4, 4) + V.monitor("الأرواح", lives, 4, 30) + extra
    defs = '<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#e8861c"/></marker></defs>'
    for lang in ("fr", "ar"):
        L = SL[lang]; suffix = "" if lang == "fr" else "-ar"
        S = [scene(-95, None, 0, 3, tag(L["flag"], 170, 120)),
             scene(-95, 150, 0, 3, arrow(375, 275, 305, 275) + tag(L["come"], 335, 235)),
             scene(10, 40, 0, 3, arrow(215, 210, 215, 130) + tag(L["jump"], 235, 190)),
             scene(-95, -230, 1, 3, tag(L["up"], 40, 120, "#2e9e5b")),
             scene(-95, -115, 1, 2, tag(L["hit"], 70, 110, "#c0392b")),
             scene(-95, -115, 3, 0, f'<rect x="0" y="0" width="480" height="360" fill="#000" fill-opacity=".5"/><text x="240" y="195" text-anchor="middle" font-family="Tajawal,Arial,sans-serif" font-size="58" font-weight="bold" fill="#fff">{L["fin"]}</text>')]
        for n, body in enumerate(S, 1):
            open(os.path.join(OUT, f"saut{suffix}-{n}.svg"), "w", encoding="utf-8").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">{defs}{body}</svg>')
    return [dict(img=f"fiches-activite/etapes/saut-{n}.svg", img_ar=f"fiches-activite/etapes/saut-ar-{n}.svg", t=SAUT[n - 1][0], c=SAUT[n - 1][1]) for n in range(1, 7)]
LABY = [("Début de partie", "Je clique sur le drapeau vert : la souris part en bas à gauche, le score est à 0 et le temps à 60."),
 ("Je déplace la souris", "J'utilise les flèches : à chaque image, x ou y change de 4, après avoir mémorisé la position précédente."),
 ("Un mur m'arrête", "Si j'entre dans la zone d'un mur hors de l'ouverture, je reviens à la position précédente : je ne traverse pas."),
 ("Je passe l'ouverture", "À l'ouverture, x est hors de la zone du mur : je continue vers le couloir suivant."),
 ("Étoile ramassée", "Quand la souris est proche d'une étoile (petite différence en x et en y) : le score augmente de 1 et l'étoile disparaît."),
 ("Arrivée au fromage", "Quand y dépasse 140 : le message « Gagné ! » s'affiche et le jeu s'arrête. Si le temps tombe à 0, le jeu s'arrête aussi.")]
LL = {"fr": dict(flag="1  Drapeau vert", keys="2  Flèches", wall="3  Mur : retour", gap="4  Ouverture", star="+1 point", win="GAGNÉ !"),
      "ar": dict(flag="1  العلم الأخضر", keys="2  الأسهم", wall="3  جدار: رجوع", gap="4  الفتحة", star="+1 نقطة", win="فزت!")}
def labyrinthe():
    import video_jeu as V
    z, T = V.load(os.path.join(ROOT, "jeux", "jeu_labyrinthe.sb3")); by = {t["name"]: t for t in T}
    def scene(mx, my, score, t, stars, extra, flip=False):
        s = V.place(T[0]["costumes"][0], 0, 0, 100) + V.place(by["الجبن"]["costumes"][0], 195, 150, 30)
        for k, (sx, sy) in enumerate([(0, -130), (0, -15), (0, 75)], 1):
            if k in stars: s += V.place(by["نجمة 1"]["costumes"][0], sx, sy, 25)
        s += V.place(by["الفأرة"]["costumes"][0], mx, my, 22, flip)
        return s + V.monitor("النقاط", score, 4, 4) + V.monitor("الوقت", t, 4, 30) + extra
    defs = '<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#e8861c"/></marker></defs>'
    for lang in ("fr", "ar"):
        L = LL[lang]; suffix = "" if lang == "fr" else "-ar"
        S = [scene(-200, -130, 0, 60, (1, 2, 3), tag(L["flag"], 140, 250)),
             scene(-90, -130, 0, 57, (1, 2, 3), arrow(250, 310, 330, 310) + tag(L["keys"], 270, 255)),
             scene(-90, -91, 0, 55, (1, 2, 3), tag(L["wall"], 30, 175)),
             scene(195, -60, 1, 52, (2, 3), arrow(330, 300, 330, 220) + tag(L["gap"], 340, 255)),
             scene(0, -15, 1, 51, (2, 3), tag(L["star"], 255, 140, "#2e9e5b")),
             scene(192, 142, 3, 47, (), f'<rect x="0" y="0" width="480" height="360" fill="#000" fill-opacity=".45"/><text x="240" y="195" text-anchor="middle" font-family="Tajawal,Arial,sans-serif" font-size="52" font-weight="bold" fill="#fff">{L["win"]}</text>')]
        for n, body in enumerate(S, 1):
            open(os.path.join(OUT, f"labyrinthe{suffix}-{n}.svg"), "w", encoding="utf-8").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">{defs}{body}</svg>')
    return [dict(img=f"fiches-activite/etapes/labyrinthe-{n}.svg", img_ar=f"fiches-activite/etapes/labyrinthe-ar-{n}.svg", t=LABY[n - 1][0], c=LABY[n - 1][1]) for n in range(1, 7)]
def contes():
    out = {}
    for key in sc.D:
        n = len(sc.D[key]["scenes"]); out[key] = []
        for i in range(n):
            open(os.path.join(OUT, f"{key}-{i+1}.svg"), "w", encoding="utf-8").write(J3.scene_svg(key, i))
            out[key].append(dict(img=f"fiches-activite/etapes/{key}-{i+1}.svg", t=f"Scène {i+1}", c=J3.caption(key, i)))
    return out
def export():
    return dict(catch=catch(), course=course(), saut=saut(), labyrinthe=labyrinthe(), contes=contes())
if __name__ == "__main__":
    e = export(); json.dump(e, open(os.path.join(HERE, "etapes.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("étapes :", len(e["catch"]), {k: len(v) for k, v in e["contes"].items()})
