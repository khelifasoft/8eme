"""Jeu « Le labyrinthe de la souris » (jeux/jeu_labyrinthe.sb3) : la souris (flèches) traverse un labyrinthe à trois murs pour atteindre le fromage avant la fin du temps ; 3 étoiles à ramasser.
Aucun capteur de couleur ni de contact : les murs sont gérés par les coordonnées (conditions imbriquées, sans ET/OU) ; variables numériques seulement (points, temps, position précédente).
Usage : python3 generateur/jeux6.py jeux   (écrit jeux/jeu_labyrinthe.sb3, jeux/couvertures/labyrinthe.svg, generateur/jeux6_manifest.json)"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import jeux2 as J, scratch_art as art
from jeux2 import B, Proj, nest
OUT = sys.argv[1] if len(sys.argv) > 1 else "jeux"
J.OUT = OUT
STEP = 4
WALLS = [(-60, "right"), (30, "left"), (120, "right")]   # (y du mur, côté de l'ouverture)
GAP = 156            # |x| au-delà duquel la souris passe par l'ouverture
BAND = 30            # demi-hauteur de la zone de contact (mur 8 + souris 22)

def maze_svg():
    s = '<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360"><rect width="480" height="360" fill="#e9f3d0"/>'
    for y, side in WALLS:
        py = 180 - y - 8
        x0, x1 = (0, 370) if side == "right" else (110, 480)
        s += f'<rect x="{x0}" y="{py}" width="{x1 - x0}" height="16" rx="8" fill="#2f6b2f" stroke="#1b441b" stroke-width="3"/>'
    s += '<rect x="2" y="2" width="476" height="356" fill="none" stroke="#1b441b" stroke-width="4"/></svg>'
    return s

def build():
    P = Proj("labyrinthe"); P.stage_costumes.append(P.costume("fond", maze_svg(), 240, 180))
    sco, si = P.V("النقاط"); tm, tmi = P.V("الوقت"); fr, fri = P.V("الإطارات"); px, pxi = P.V("س السابق"); py, pyi = P.V("ص السابق"); ding = P.sfx("ding")
    # souris
    hb = B(); left, right, up, down = hb.key("left arrow"), hb.key("right arrow"), hb.key("up arrow"), hb.key("down arrow")
    face = lambda d: hb.add("motion_pointindirection", inputs={"DIRECTION": [1, [8, str(d)]]})
    save = [hb.setv(px, pxi, hb.R(hb.xpos())), hb.setv(py, pyi, hb.R(hb.ypos()))]
    moves = [hb.if_(left, hb.chx(hb.N(-STEP)), face(-90)), hb.if_(right, hb.chx(hb.N(STEP)), face(90)), hb.if_(up, hb.add("motion_changeyby", inputs={"DY": hb.N(STEP)})), hb.if_(down, hb.add("motion_changeyby", inputs={"DY": hb.N(-STEP)}))]
    back = lambda: hb.gotoxy_(hb.R(hb.var(px, pxi)), hb.R(hb.var(py, pyi)))
    walls = []
    for wy, side in WALLS:   # trois conditions imbriquées : dans la zone du mur, hors de l'ouverture -> retour à la position précédente
        inner = hb.if_(hb.lt(hb.R(hb.xpos()), hb.N(GAP)), back()) if side == "right" else hb.if_(hb.gt(hb.R(hb.xpos()), hb.N(-GAP)), back())
        walls.append(hb.if_(hb.gt(hb.R(hb.ypos()), hb.N(wy - BAND)), hb.if_(hb.lt(hb.R(hb.ypos()), hb.N(wy + BAND)), inner)))
    edges = [hb.if_(hb.gt(hb.R(hb.xpos()), hb.N(214)), hb.setx(hb.N(214))), hb.if_(hb.lt(hb.R(hb.xpos()), hb.N(-214)), hb.setx(hb.N(-214))), hb.if_(hb.lt(hb.R(hb.ypos()), hb.N(-156)), hb.add("motion_sety", inputs={"Y": hb.N(-156)}))]
    secs = hb.sub_(hb.N(60), hb.R(hb.add("operator_round", inputs={"NUM": hb.R(hb.add("operator_divide", inputs={"NUM1": hb.R(hb.var(fr, fri)), "NUM2": hb.N(30)}))})))
    clock = [hb.chg(fr, fri, 1), hb.setv(tm, tmi, hb.R(secs))]
    win = hb.if_(hb.gt(hb.R(hb.ypos()), hb.N(140)), hb.sayfor(hb.join(hb.S("فزت! نقاطك: "), hb.RS(hb.var(sco, si))), 3), hb.stop_all())
    lose = hb.if_(hb.lt(hb.R(hb.var(tm, tmi)), hb.N(1)), hb.sayfor(hb.S("انتهى الوقت!"), 3), hb.stop_all())
    hb.script(hb.hat_flag(), hb.setv(sco, si, 0), hb.setv(fr, fri, 0), hb.setv(tm, tmi, 60), hb.size(22), hb.gotoxy_(hb.N(-200), hb.N(-130)), hb.show(),
              hb.forever_(*save, *moves, *walls, *edges, *clock, win, lose), y=0)
    hb.script(hb.hat_flag(), hb.sayfor(hb.S("استعمل الأسهم للوصول إلى الجبن"), 4), y=500)
    P.sprite("الفأرة", hb, [P.costume("فأرة", art.art_svg("a", "souris"))], x=-200, y=-130, size=22, visible=True, flip=True)
    # fromage (but)
    gb = B(); P.sprite("الجبن", gb, [P.costume("جبن", art.art_svg("d", "fromage"))], x=195, y=150, size=30, visible=True)
    # trois étoiles : ramassées par la distance (conditions imbriquées), pas de capteur de contact
    for k, (sx, sy) in enumerate([(0, -130), (0, -15), (0, 75)], 1):
        sb = B(); menu = sb.add("sensing_of_object_menu", fields={"OBJECT": ["الفأرة", None]}, shadow=True)
        mx = sb.add("sensing_of", fields={"PROPERTY": ["x position", None]}, inputs={"OBJECT": [1, menu]})
        menu2 = sb.add("sensing_of_object_menu", fields={"OBJECT": ["الفأرة", None]}, shadow=True)
        my = sb.add("sensing_of", fields={"PROPERTY": ["y position", None]}, inputs={"OBJECT": [1, menu2]})
        stop = sb.add("control_stop", fields={"STOP_OPTION": ["this script", None]}); sb.b[stop]["mutation"] = {"tagName": "mutation", "children": [], "hasnext": "false"}
        near_y = sb.if_(sb.lt(sb.R(sb.absv(sb.R(sb.sub_(sb.R(sb.ypos()), sb.R(my))))), sb.N(30)), sb.chg(sco, si, 1), sb.play(ding["name"]), sb.add("looks_hide"), stop)
        near_x = sb.if_(sb.lt(sb.R(sb.absv(sb.R(sb.sub_(sb.R(sb.xpos()), sb.R(mx))))), sb.N(30)), near_y)
        sb.script(sb.hat_flag(), sb.gotoxy_(sb.N(sx), sb.N(sy)), sb.size(25), sb.show(), sb.forever_(near_x), y=0)
        P.sprite(f"نجمة {k}", sb, [P.costume("نجمة", art.art_svg("d", "etoile"))], [ding], x=sx, y=sy, size=25, visible=True)
    P.monitor("النقاط", 5); P.monitor("الوقت", 32); P.monitor("الإطارات", 59, False); P.monitor("س السابق", 86, False); P.monitor("ص السابق", 113, False)
    P.finish("mystere")
    cover = ('<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">' + nest(maze_svg(), 0, 0, 480, 360) +
             nest(art.art_svg("a", "souris"), 20, 240, 90, 75) + nest(art.art_svg("d", "fromage"), 350, 20, 80, 69) + nest(art.art_svg("d", "etoile"), 200, 150, 40, 40) + '</svg>')
    os.makedirs(os.path.join(OUT, "couvertures"), exist_ok=True); open(os.path.join(OUT, "couvertures", "labyrinthe.svg"), "w", encoding="utf-8").write(cover)
    meta = [dict(key="labyrinthe", file="jeux/jeu_labyrinthe.sb3", title_ar="متاهة الفأرة", title_fr="Le labyrinthe de la souris",
                 how_ar="حرّك الفأرة بالأسهم عبر المتاهة للوصول إلى الجبن قبل انتهاء الوقت، والتقط النجوم الثلاث.", how_fr="Déplace la souris avec les flèches dans le labyrinthe pour atteindre le fromage avant la fin du temps, et ramasse les trois étoiles.",
                 cover="jeux/couvertures/labyrinthe.svg")]
    json.dump(meta, open(os.path.join(HERE, "jeux6_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("jeu labyrinthe :", os.path.getsize(os.path.join(OUT, "jeu_labyrinthe.sb3")) // 1024, "Ko")
if __name__ == "__main__": build()
