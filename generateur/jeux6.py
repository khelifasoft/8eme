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

def ghost_svg(body, edge):
    """Fantôme (70 x 80) : drap ondulé, yeux et joues."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="70" height="80" viewBox="0 0 70 80"><path d="M6 40 Q6 6 35 6 Q64 6 64 40 L64 72 Q57 64 50 72 Q43 80 35 72 Q27 64 20 72 Q13 80 6 72Z" fill="{body}" stroke="{edge}" stroke-width="3" stroke-linejoin="round"/>'
            '<ellipse cx="25" cy="36" rx="6" ry="8" fill="#243044"/><ellipse cx="45" cy="36" rx="6" ry="8" fill="#243044"/><circle cx="27" cy="33" r="2.2" fill="#fff"/><circle cx="47" cy="33" r="2.2" fill="#fff"/>'
            '<ellipse cx="35" cy="54" rx="6" ry="4.5" fill="#243044"/><circle cx="16" cy="48" r="4" fill="#ff9db3" fill-opacity=".7"/><circle cx="54" cy="48" r="4" fill="#ff9db3" fill-opacity=".7"/></svg>')
GX, TOP_END, BOTTOM_END = 185, 105, 140   # fantôme 1 : colonne x = 185 ; demi-tour en y = 105 et y = -140 (conditions sur la position, comme les murs)
GHOST_NEAR = 30      # contact avec un fantôme : différence |x| et |y| inférieures à 28 (comme pour les étoiles : conditions imbriquées, sans capteur) ; 30 couvre toute la largeur de la colonne d'ouverture (x de 156 à 214)

def build():
    P = Proj("labyrinthe"); P.stage_costumes.append(P.costume("fond", maze_svg(), 240, 180))
    sco, si = P.V("النقاط"); tm, tmi = P.V("الوقت"); fr, fri = P.V("الإطارات"); px, pxi = P.V("س السابق"); py, pyi = P.V("ص السابق"); ding = P.sfx("ding")
    lvl, lvli = P.V("المستوى"); gsp, gspi = P.V("سرعة الشبح"); ghd, ghdi = P.V("اختفاء الشبح"); tot, toti = P.V("المدة"); tip, tipi = P.V("النصيحة")
    def wait_level(b): return b.add("control_wait_until", inputs={"CONDITION": b.C(b.gt(b.R(b.var(lvl, lvli)), b.N(0)))})   # tous les lutins attendent le choix du niveau
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
    secs = hb.sub_(hb.R(hb.var(tot, toti)), hb.R(hb.add("operator_round", inputs={"NUM": hb.R(hb.add("operator_divide", inputs={"NUM1": hb.R(hb.var(fr, fri)), "NUM2": hb.N(30)}))})))
    clock = [hb.chg(fr, fri, 1), hb.setv(tm, tmi, hb.R(secs))]
    win = hb.if_(hb.gt(hb.R(hb.ypos()), hb.N(140)), hb.sayfor(hb.join(hb.S("فزت! نقاطك: "), hb.RS(hb.var(sco, si))), 3), hb.sayfor(hb.S("نصيحة: جرّب مستوى أصعب وحاول التقاط النجوم الثلاث!"), 3), hb.stop_all())
    lose = hb.if_(hb.lt(hb.R(hb.var(tm, tmi)), hb.N(1)), hb.sayfor(hb.S("انتهى الوقت!"), 3), hb.sayfor(hb.S("نصيحة: كل نجمة تمنحك 5 ثوان إضافية، التقطها!"), 3), hb.stop_all())
    setlevel = lambda n, v, g, d, t: hb.if_(hb.eq(hb.R(hb.var(lvl, lvli)), hb.N(n)), hb.setv(gsp, gspi, hb.N(g)), hb.setv(ghd, ghdi, hb.N(d)), hb.setv(tot, toti, hb.N(t)))
    choose = hb.until(hb.gt(hb.R(hb.var(lvl, lvli)), hb.N(0)), hb.if_(hb.key("1"), hb.setv(lvl, lvli, hb.N(1))), hb.if_(hb.key("2"), hb.setv(lvl, lvli, hb.N(2))), hb.if_(hb.key("3"), hb.setv(lvl, lvli, hb.N(3))))
    hb.script(hb.hat_flag(), hb.setv(sco, si, 0), hb.setv(fr, fri, 0), hb.setv(lvl, lvli, 0), hb.setv(tip, tipi, 0), hb.size(22), hb.gotoxy_(hb.N(-200), hb.N(-130)), hb.show(),
              hb.say_(hb.S("اختر المستوى: 1 سهل · 2 عادي · 3 صعب")), choose, setlevel(1, 1, 2, 3, 90), setlevel(2, 2, 3, 2, 60), setlevel(3, 3, 4, 1, 45),
              hb.setv(tm, tmi, hb.R(hb.var(tot, toti))), hb.say_(hb.S("")),
              hb.forever_(*save, *moves, *walls, *edges, *clock, win, lose), y=0)
    hb.script(hb.hat_flag(), wait_level(hb), hb.sayfor(hb.S("استعمل الأسهم للوصول إلى الجبن. اضغط H للحصول على نصيحة"), 4), y=500)
    # astuces éducatives : la touche H affiche une astuce différente à chaque appui (variable « النصيحة », conditions simples)
    TIPS = ["نصيحة 1: راقب الشبح 1: يصعد ثم ينزل بإيقاع ثابت. انتظر اللحظة المناسبة قبل أن تمرّ.", "نصيحة 2: الشبح 2 يظهر نصف ثانية دون خطر: ابتعد بسرعة!", "نصيحة 3: كل نجمة تمنحك نقطة و5 ثوان: الوقت متغير يمكن أن يزيد.",
            "نصيحة 4: الجدار يعيدك إلى (س السابق، ص السابق): متغيران يحفظان مكانك قبل كل حركة.", "نصيحة 5: المستوى يغيّر سرعة الشبح ومدة اللعبة: هذه قيم تحفظها متغيرات."]
    hb.script(hb.add("event_whenkeypressed", fields={"KEY_OPTION": ["h", None]}), hb.chg(tip, tipi, 1), hb.if_(hb.gt(hb.R(hb.var(tip, tipi)), hb.N(5)), hb.setv(tip, tipi, 1)),
              *[hb.if_(hb.eq(hb.R(hb.var(tip, tipi)), hb.N(k)), hb.sayfor(hb.S(t), 4)) for k, t in enumerate(TIPS, 1)], y=1500)
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
        near_y = sb.if_(sb.lt(sb.R(sb.absv(sb.R(sb.sub_(sb.R(sb.ypos()), sb.R(my))))), sb.N(30)), sb.chg(sco, si, 1), sb.chg(fr, fri, -150), sb.play(ding["name"]), sb.add("looks_hide"), stop)
        near_x = sb.if_(sb.lt(sb.R(sb.absv(sb.R(sb.sub_(sb.R(sb.xpos()), sb.R(mx))))), sb.N(30)), near_y)
        sb.script(sb.hat_flag(), sb.gotoxy_(sb.N(sx), sb.N(sy)), sb.size(25), sb.show(), wait_level(sb), sb.forever_(near_x), y=0)
        P.sprite(f"نجمة {k}", sb, [P.costume("نجمة", art.art_svg("d", "etoile"))], [ding], x=sx, y=sy, size=25, visible=True)
    # deux fantômes : le premier fait des va-et-vient dans le couloir du milieu, le second se cache puis réapparaît à une position aléatoire ; le toucher = perdu
    def near_mouse(sb, *body):
        m1 = sb.add("sensing_of_object_menu", fields={"OBJECT": ["الفأرة", None]}, shadow=True); mx = sb.add("sensing_of", fields={"PROPERTY": ["x position", None]}, inputs={"OBJECT": [1, m1]})
        m2 = sb.add("sensing_of_object_menu", fields={"OBJECT": ["الفأرة", None]}, shadow=True); my = sb.add("sensing_of", fields={"PROPERTY": ["y position", None]}, inputs={"OBJECT": [1, m2]})
        near_y = sb.if_(sb.lt(sb.R(sb.absv(sb.R(sb.sub_(sb.R(sb.ypos()), sb.R(my))))), sb.N(GHOST_NEAR)), *body)
        return sb.if_(sb.lt(sb.R(sb.absv(sb.R(sb.sub_(sb.R(sb.xpos()), sb.R(mx))))), sb.N(GHOST_NEAR)), near_y)
    g1 = B()   # fantôme 1 : va-et-vient vertical dans la colonne des ouvertures de droite : il faut choisir le bon moment pour passer
    g1.script(g1.hat_flag(), g1.gotoxy_(g1.N(GX), g1.N(-140)), g1.direction(0), g1.size(30), g1.show(), wait_level(g1),
              g1.forever_(g1.add("motion_movesteps", inputs={"STEPS": g1.R(g1.var(gsp, gspi))}), g1.if_(g1.gt(g1.R(g1.ypos()), g1.N(TOP_END)), g1.direction(180)), g1.if_(g1.lt(g1.R(g1.ypos()), g1.N(-BOTTOM_END)), g1.direction(0)),
                          near_mouse(g1, P.bc(g1, "خسرت", True), g1.stop_all())), y=0)
    P.sprite("الشبح 1", g1, [P.costume("شبح", ghost_svg("#ffffff", "#5b6b8c"), 35, 40)], x=GX, y=-140, size=30, visible=True)
    g2 = B()
    g2.script(g2.hat_flag(), g2.hide(), g2.size(30), wait_level(g2), g2.forever_(g2.hide(), g2.add("control_wait", inputs={"DURATION": g2.R(g2.var(ghd, ghdi))}), g2.gotoxy_(g2.R(g2.rand(g2.N(-200), g2.N(200))), g2.R(g2.rand(g2.N(-110), g2.N(120)))), g2.show(), g2.wait(0.5),
              g2.repeat(40, near_mouse(g2, P.bc(g2, "خسرت", True), g2.stop_all()))), y=0)
    P.sprite("الشبح 2", g2, [P.costume("شبح", ghost_svg("#e6dcff", "#6b4fb3"), 35, 40)], x=0, y=0, size=30, visible=False)
    hb.script(P.hat(hb, "خسرت"), hb.stop_other(), hb.sayfor(hb.S("لمسك شبح! خسرت"), 3), hb.sayfor(hb.S("نصيحة: راقب إيقاع الشبح قبل المرور (اضغط H)"), 3), y=1000)
    P.monitor("النقاط", 5); P.monitor("الوقت", 32); P.monitor("المستوى", 59); P.monitor("الإطارات", 86, False); P.monitor("س السابق", 113, False); P.monitor("ص السابق", 140, False)
    P.finish("mystere")
    cover = ('<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">' + nest(maze_svg(), 0, 0, 480, 360) +
             nest(art.art_svg("a", "souris"), 20, 240, 90, 75) + nest(art.art_svg("d", "fromage"), 350, 20, 80, 69) + nest(art.art_svg("d", "etoile"), 200, 150, 40, 40) + nest(ghost_svg("#ffffff", "#5b6b8c"), 250, 190, 60, 69) + nest(ghost_svg("#e6dcff", "#6b4fb3"), 110, 60, 50, 57) + '</svg>')
    os.makedirs(os.path.join(OUT, "couvertures"), exist_ok=True); open(os.path.join(OUT, "couvertures", "labyrinthe.svg"), "w", encoding="utf-8").write(cover)
    meta = [dict(key="labyrinthe", file="jeux/jeu_labyrinthe.sb3", title_ar="متاهة الفأرة", title_fr="Le labyrinthe de la souris",
                 how_ar="حرّك الفأرة بالأسهم عبر المتاهة للوصول إلى الجبن قبل انتهاء الوقت، والتقط النجوم الثلاث وتجنّب الشبحين: إن لمسك أحدهما خسرت.", how_fr="Déplace la souris avec les flèches dans le labyrinthe pour atteindre le fromage avant la fin du temps, ramasse les trois étoiles et évite les deux fantômes : si l'un d'eux te touche, tu perds.",
                 cover="jeux/couvertures/labyrinthe.svg")]
    json.dump(meta, open(os.path.join(HERE, "jeux6_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("jeu labyrinthe :", os.path.getsize(os.path.join(OUT, "jeu_labyrinthe.sb3")) // 1024, "Ko")
if __name__ == "__main__": build()
