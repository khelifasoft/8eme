"""Jeu « Le chameau saute-buissons » (jeux/jeu_saut.sb3) : on appuie sur la barre d'espace pour faire sauter le chameau par-dessus les buissons qui arrivent.
Règles (numériques uniquement, sans ET/OU, sans liste) : saut = vitesse verticale +19 puis −1 à chaque image ; vitesse de départ 3 ; +0,15 à chaque buisson évité ; buisson touché = −1 vie ; 3 vies.
Usage : python3 generateur/jeux5.py jeux   (écrit jeux/jeu_saut.sb3, jeux/couvertures/saut.svg, generateur/jeux5_manifest.json)"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import jeux2 as J, scratch_art as art
from jeux2 import B, Proj, nest
from jeux4 import hearts_svg
OUT = sys.argv[1] if len(sys.argv) > 1 else "jeux"
J.OUT = OUT
GROUND = -95; CAMEL_X = -120

def build():
    P = Proj("saut"); P.stage_costumes.append(P.costume("fond", art.art_svg("l", "desert"), 240, 180))
    sco, si = P.V("النقاط"); lv, lvi = P.V("الأرواح"); sp, spi = P.V("السرعة"); vy, vyi = P.V("السرعة العمودية"); ouch = P.sfx("boing")
    # chameau : espace = saut (gravité simple avec une variable numérique)
    cb = B(); space = cb.key("space")
    jump = cb.if_(space, cb.if_(cb.lt(cb.R(cb.ypos()), cb.N(GROUND + 5)), cb.setv(vy, vyi, cb.N(19))))
    move = cb.chy(cb.R(cb.var(vy, vyi))); grav = cb.chg(vy, vyi, -1)
    floor = cb.if_(cb.lt(cb.R(cb.ypos()), cb.N(GROUND)), cb.add("motion_sety", inputs={"Y": cb.N(GROUND)}), cb.setv(vy, vyi, cb.N(0)))
    cb.script(cb.hat_flag(), cb.setv(vy, vyi, cb.N(0)), cb.size(50), cb.gotoxy_(cb.N(CAMEL_X), cb.N(GROUND)), cb.show(), cb.forever_(jump, move, grav, floor), y=0)
    cb.script(cb.hat_flag(), cb.sayfor(cb.S("اضغط على المسافة لتقفز فوق الشجيرات"), 4), y=300)
    P.sprite("الجمل", cb, [P.costume("جمل", art.art_svg("a", "chameau"))], x=CAMEL_X, y=GROUND, size=50, visible=True)
    # buisson qui arrive de la droite
    ob = B()
    def go_start(): return ob.gotoxy_(ob.R(ob.rand(ob.N(270), ob.N(370))), ob.N(-120))
    fall = ob.chx(ob.R(ob.sub_(ob.N(0), ob.R(ob.var(sp, spi)))))
    menu = ob.add("sensing_of_object_menu", fields={"OBJECT": ["الجمل", None]}, shadow=True)
    cy = ob.add("sensing_of", fields={"PROPERTY": ["y position", None]}, inputs={"OBJECT": [1, menu]})
    near = ob.lt(ob.R(ob.absv(ob.R(ob.add_(ob.R(ob.xpos()), ob.N(-CAMEL_X))))), ob.N(45))
    c_hit = ob.if_(near, ob.if_(ob.lt(ob.R(cy), ob.N(GROUND + 50)), ob.chg(lv, lvi, -1), ob.play(ouch["name"]), go_start()))
    c_pass = ob.if_(ob.lt(ob.R(ob.xpos()), ob.N(-270)), ob.chg(sco, si, 1), ob.chg(sp, spi, 0.15), go_start())
    c_end = ob.if_(ob.lt(ob.R(ob.var(lv, lvi)), ob.N(1)), ob.sayfor(ob.join(ob.S("انتهت اللعبة! نقاطك: "), ob.RS(ob.var(sco, si))), 3), ob.stop_all())
    ob.script(ob.hat_flag(), ob.setv(sco, si, 0), ob.setv(lv, lvi, 3), ob.setv(sp, spi, 3), ob.size(40), go_start(), ob.show(), ob.forever_(fall, c_hit, c_pass, c_end), y=0)
    P.sprite("الشجيرة", ob, [P.costume("شجيرة", art.art_svg("d", "buisson"))], [ouch], x=300, y=-120, size=40)
    # cœurs = nombre de vies
    hb = B(); hb.script(hb.hat_flag(), hb.show(), hb.forever_(hb.costume_n(hb.R(hb.var(lv, lvi))), hb.if_(hb.lt(hb.R(hb.var(lv, lvi)), hb.N(1)), hb.hide())), y=0)
    P.sprite("القلوب", hb, [P.costume(f"{n}", hearts_svg(n), 54, 17) for n in (1, 2, 3)], x=-40, y=158, size=100, visible=True)
    P.monitor("النقاط", 5); P.monitor("الأرواح", 32); P.monitor("السرعة", 59, False); P.monitor("السرعة العمودية", 86, False)
    P.finish("aventure")
    cover = ('<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">' + nest(art.art_svg("l", "desert"), 0, 0, 480, 360) +
             nest(art.art_svg("a", "chameau"), 60, 100, 210, 162) + nest(art.art_svg("d", "buisson"), 310, 180, 100, 71) + '</svg>')
    os.makedirs(os.path.join(OUT, "couvertures"), exist_ok=True); open(os.path.join(OUT, "couvertures", "saut.svg"), "w", encoding="utf-8").write(cover)
    meta = [dict(key="saut", file="jeux/jeu_saut.sb3", title_ar="الجمل يقفز: تفادَ الشجيرات", title_fr="Le chameau saute-buissons",
                 how_ar="اضغط على المسافة لتجعل الجمل يقفز فوق الشجيرات القادمة. لديك ثلاثة قلوب.", how_fr="Appuie sur la barre d'espace pour faire sauter le chameau par-dessus les buissons qui arrivent. Tu as trois cœurs.",
                 cover="jeux/couvertures/saut.svg")]
    json.dump(meta, open(os.path.join(HERE, "jeux5_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("jeu saut :", os.path.getsize(os.path.join(OUT, "jeu_saut.sb3")) // 1024, "Ko")
if __name__ == "__main__": build()
