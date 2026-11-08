"""Jeu « Course : évite les voitures » (jeux/jeu_course.sb3) : on conduit une voiture avec les flèches ← → et on évite les voitures qui arrivent.
Règles (numériques uniquement, sans ET/OU, sans liste) : vitesse de départ 3 ; vitesse +0,15 à chaque voiture évitée ; voiture touchée = −1 vie ; 3 vies.
Usage : python3 generateur/jeux4.py jeux   (écrit jeux/jeu_course.sb3, jeux/couvertures/course.svg, generateur/jeux4_manifest.json)"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import jeux2 as J
from jeux2 import B, Proj
OUT = sys.argv[1] if len(sys.argv) > 1 else "jeux"
J.OUT = OUT
W, H = 480, 360

def car_svg(body, dark, down=False):
    g = (f'<rect x="3" y="14" width="10" height="24" rx="3" fill="#222"/><rect x="47" y="14" width="10" height="24" rx="3" fill="#222"/>'
         f'<rect x="3" y="72" width="10" height="24" rx="3" fill="#222"/><rect x="47" y="72" width="10" height="24" rx="3" fill="#222"/>'
         f'<rect x="8" y="2" width="44" height="106" rx="18" fill="{body}" stroke="#111" stroke-width="3"/>'
         f'<rect x="14" y="26" width="32" height="20" rx="6" fill="#7fb9e8" stroke="#111" stroke-width="2"/>'
         f'<rect x="16" y="50" width="28" height="30" rx="8" fill="{dark}"/><rect x="14" y="84" width="32" height="12" rx="5" fill="#7fb9e8" stroke="#111" stroke-width="2"/>'
         f'<rect x="12" y="6" width="9" height="6" rx="2" fill="#fff3a0"/><rect x="39" y="6" width="9" height="6" rx="2" fill="#fff3a0"/>')
    if down: g = f'<g transform="rotate(180 30 55)">{g}</g>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="60" height="110" viewBox="0 0 60 110">{g}</svg>'
def road_svg():
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="#3d7a28"/>'
            f'<rect x="130" width="220" height="{H}" fill="#c8c8c8"/><rect x="127" width="4" height="{H}" fill="#eee"/><rect x="349" width="4" height="{H}" fill="#eee"/></svg>')
def lines_svg():  # 4 tirets, période 120 : défilement sans coupure
    d = "".join(f'<rect x="234" y="{k * 120 + 30}" width="12" height="60" fill="#fff"/>' for k in range(4))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="480" viewBox="0 0 480 480">{d}</svg>'
def hearts_svg(n):
    heart = '<path d="M16 28 C2 18 2 6 10 4 C14 3 16 6 16 8 C16 6 18 3 22 4 C30 6 30 18 16 28Z" fill="#d11" stroke="#400" stroke-width="2"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="108" height="34" viewBox="0 0 108 34">' + "".join(f'<g transform="translate({k * 36 + 2},1)">{heart}</g>' for k in range(n)) + '</svg>'

def build():
    P = Proj("course"); P.stage_costumes.append(P.costume("fond", road_svg(), 240, 180))
    sco, si = P.V("النقاط"); lv, lvi = P.V("الأرواح"); sp, spi = P.V("السرعة"); ouch = P.sfx("boing")
    # lignes de la route (défilent à la vitesse du jeu)
    lb = B(); fall_l = lb.chy(lb.R(lb.sub_(lb.N(0), lb.R(lb.var(sp, spi)))))
    wrap = lb.if_(lb.lt(lb.R(lb.ypos()), lb.N(-60)), lb.chy(lb.N(120)))
    lb.script(lb.hat_flag(), lb.gotoxy_(lb.N(0), lb.N(0)), lb.show(), lb.forever_(fall_l, wrap), y=0)
    P.sprite("الخطوط", lb, [P.costume("خطوط", lines_svg(), 240, 240)], x=0, y=0, size=100, visible=True)
    # voiture du joueur : flèches gauche / droite
    hb = B(); left, right = hb.key("left arrow"), hb.key("right arrow")
    clamp = [hb.if_(hb.gt(hb.R(hb.xpos()), hb.N(85)), hb.setx(hb.N(85))), hb.if_(hb.lt(hb.R(hb.xpos()), hb.N(-85)), hb.setx(hb.N(-85)))]
    loop = hb.forever_(hb.if_(left, hb.chx(hb.N(-11))), hb.if_(right, hb.chx(hb.N(11))), *clamp)
    hb.script(hb.hat_flag(), hb.size(70), hb.gotoxy_(hb.N(0), hb.N(-125)), hb.show(), loop, y=0)
    hb.script(hb.hat_flag(), hb.sayfor(hb.S("استعمل السهمين ← → لتتفادى السيارات"), 4), y=300)
    P.sprite("السيارة", hb, [P.costume("سيارة", car_svg("#1b2a9c", "#10186a"))], x=0, y=-125, size=70, visible=True)
    # voiture adverse
    ob = B()
    def go_top(): return ob.gotoxy_(ob.R(ob.rand(ob.N(-85), ob.N(85))), ob.N(210))
    fall = ob.chy(ob.R(ob.sub_(ob.N(0), ob.R(ob.var(sp, spi)))))
    menu = ob.add("sensing_of_object_menu", fields={"OBJECT": ["السيارة", None]}, shadow=True)
    hero_x = ob.add("sensing_of", fields={"PROPERTY": ["x position", None]}, inputs={"OBJECT": [1, menu]})
    ab = ob.absv(ob.R(ob.sub_(ob.R(ob.xpos()), ob.R(hero_x)))); near = ob.lt(ob.R(ab), ob.N(48))
    c_hit = ob.if_(near, ob.if_(ob.lt(ob.R(ob.ypos()), ob.N(-95)), ob.chg(lv, lvi, -1), ob.play(ouch["name"]), go_top()))
    c_pass = ob.if_(ob.lt(ob.R(ob.ypos()), ob.N(-170)), ob.chg(sco, si, 1), ob.chg(sp, spi, 0.15), go_top())
    c_end = ob.if_(ob.lt(ob.R(ob.var(lv, lvi)), ob.N(1)), ob.sayfor(ob.join(ob.S("انتهت اللعبة! نقاطك: "), ob.RS(ob.var(sco, si))), 3), ob.stop_all())
    ob.script(ob.hat_flag(), ob.setv(sco, si, 0), ob.setv(lv, lvi, 3), ob.setv(sp, spi, 3), ob.size(70), go_top(), ob.show(), ob.forever_(fall, c_hit, c_pass, c_end), y=0)
    P.sprite("سيارة معاكسة", ob, [P.costume("معاكسة", car_svg("#d62828", "#8f1414", down=True))], [ouch], x=0, y=210, size=70)
    # cœurs = nombre de vies
    cb = B(); cb.script(cb.hat_flag(), cb.show(), cb.forever_(cb.costume_n(cb.R(cb.var(lv, lvi))), cb.if_(cb.lt(cb.R(cb.var(lv, lvi)), cb.N(1)), cb.hide())), y=0)
    P.sprite("القلوب", cb, [P.costume(f"{n}", hearts_svg(n), 54, 17) for n in (1, 2, 3)], x=185, y=158, size=100, visible=True)
    P.monitor("النقاط", 5); P.monitor("الأرواح", 32); P.monitor("السرعة", 59, False)
    P.finish("aventure")
    cover = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + road_svg().split(">", 1)[1].rsplit("</svg>", 1)[0] + \
            lines_svg().split(">", 1)[1].rsplit("</svg>", 1)[0].replace('y="30"', 'y="-30"') + \
            f'<g transform="translate(213,60)">{car_svg("#d62828", "#8f1414", True).split(">", 1)[1].rsplit("</svg>", 1)[0]}</g><g transform="translate(197,230) scale(1.0)">{car_svg("#1b2a9c", "#10186a").split(">", 1)[1].rsplit("</svg>", 1)[0]}</g></svg>'
    os.makedirs(os.path.join(OUT, "couvertures"), exist_ok=True); open(os.path.join(OUT, "couvertures", "course.svg"), "w", encoding="utf-8").write(cover)
    meta = [dict(key="course", file="jeux/jeu_course.sb3", title_ar="سباق السيارات: تفادَ السيارات", title_fr="Course : évite les voitures",
                 how_ar="حرّك السيارة بالسهمين ← → لتتفادى السيارات القادمة. لديك ثلاثة قلوب.", how_fr="Déplace la voiture avec les flèches ← → pour éviter les voitures qui arrivent. Tu as trois cœurs.",
                 cover="jeux/couvertures/course.svg")]
    json.dump(meta, open(os.path.join(HERE, "jeux4_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("jeu course :", os.path.getsize(os.path.join(OUT, "jeu_course.sb3")) // 1024, "Ko")
if __name__ == "__main__": build()
