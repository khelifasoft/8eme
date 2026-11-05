from svgkit import *
from decors import frag
import math

W, H = 480, 360
def ciel(c1, c2, h=360):
    return (f'<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
            f'<rect width="{W}" height="{h}" fill="url(#sk)"/>')
def sol(y, col, col2=None):
    s = f'<rect y="{y}" width="{W}" height="{H-y}" fill="{col}"/>'
    if col2: s += f'<rect y="{y}" width="{W}" height="8" fill="{col2}"/>'
    return s
def colline(y, col, amp=30, ph=0):
    pts = " ".join(f"{x},{y - amp*math.sin((x+ph)/70)}" for x in range(0, W + 20, 20))
    return f'<polygon points="0,{H} {pts} {W},{H}" fill="{col}"/>'
def montagnes(col, y=200):
    return f'<polygon points="0,{y} 70,{y-100} 130,{y-30} 200,{y-120} 280,{y-20} 360,{y-90} 420,{y-30} 480,{y-70} 480,{y} " fill="{col}"/>'
def sun(x=400, y=60, s=0.7): return frag("soleil", x, y, s)
def cloud(x, y, s=0.6): return frag("nuage", x, y, s)
def stars(n=40):
    import random
    r = random.Random(5)
    return "".join(f'<circle cx="{r.randint(5,475)}" cy="{r.randint(5,200)}" r="{r.choice([1,1.5,2,2.5])}" fill="#fff8c8"/>' for _ in range(n))
def eau(y, c1="#4a90c8", c2="#2f6fa8"):
    s = f'<rect y="{y}" width="{W}" height="{H-y}" fill="{c1}"/>'
    for yy in range(y + 14, H, 26):
        s += f'<path d="' + "".join(f"M{x} {yy} q10 -8 20 0 " for x in range(-10, W, 40)) + f'" fill="none" stroke="{c2}" stroke-width="3" stroke-linecap="round" opacity="0.7"/>'
    return s
def interieur_mur(col, plinthe, sol_c):
    return f'<rect width="{W}" height="{H}" fill="{col}"/><rect y="250" width="{W}" height="110" fill="{sol_c}"/><rect y="244" width="{W}" height="10" fill="{plinthe}"/>' + "".join(f'<line x1="{x}" y1="254" x2="{x-30}" y2="{H}" stroke="#00000022" stroke-width="2"/>' for x in range(0, 540, 60))

def foret():
    return (ciel("#bfe4f2", "#e6f4d8", 250) + colline(210, "#5aa05a", 20) + sol(240, "#6fba5e", "#4a9a4a") + frag("arbre", 20, 120, 1.1) + frag("arbre", 360, 100, 1.2) + frag("sapin", 150, 120, 1.0) + frag("sapin", 290, 130, 0.9) + frag("buisson", 220, 250, 0.9) + frag("fleurs", 60, 290, 0.9) + frag("champignon", 400, 290, 0.7) + sun(400, 12, .6) + cloud(60, 20, .6))
def foret_nuit():
    return (ciel("#0f1a3a", "#2a3a6a", 260) + stars(50) + frag("lune", 380, 20, 0.9) + colline(230, "#1a3a2a", 18) + sol(250, "#24492f", "#1a3a24") + frag("sapin", 30, 120, 1.1) + frag("sapin", 330, 110, 1.2) + frag("arbre", 170, 100, 1.1) + frag("sapin", 410, 150, 0.9))
def foret_dense():
    s = ciel("#7aa87a", "#4a7a52", 260) + sol(250, "#3d6a3f", "#2f5a36")
    for x in range(-10, 480, 70): s += frag("sapin", x, 70 + (x % 3) * 18, 1.3)
    for x in range(10, 480, 90): s += frag("arbre", x, 110 + (x % 4) * 10, 1.0)
    return s + frag("buisson", 180, 280, 1.0)
def jardin_puits():
    return (ciel("#bfe4f2", "#e8f6e0", 240) + colline(220, "#7acb6a", 12) + sol(240, "#8ad672", "#62b552") + frag("puits", 180, 130, 1.4) + frag("fleurs", 30, 290, 1.0) + frag("fleurs", 360, 290, 1.0) + frag("buisson", 20, 200, 1.0) + frag("buisson", 360, 200, 1.1) + frag("barriere", 280, 250, 1.0) + sun(400, 10, .6) + cloud(60, 20, .6))
def jardin():
    return (ciel("#bfe4f2", "#e8f6e0", 240) + colline(215, "#7acb6a", 14) + sol(240, "#8ad672", "#62b552") + frag("arbre", 20, 110, 1.2) + frag("fleurs", 160, 270, 1.2) + frag("fleurs", 330, 280, 1.0) + frag("barriere", 230, 240, 1.0) + frag("maison", 300, 100, 1.0) + sun(400, 10, .6))
def maison_int():
    return (interieur_mur("#f0dcb0", "#a8743a", "#c9a066") + frag("fenetre", 60, 70, 1.2) + frag("fenetre", 340, 70, 1.2) + frag("table", 150, 210, 1.2) + frag("chaise", 110, 190, 1.0) + frag("chaise", 310, 190, 1.0) + frag("panier", 200, 190, 0.7) + frag("lanterne", 230, 40, 0.7))
def chambre():
    return (interieur_mur("#dbe4f6", "#8a6a4a", "#b8946a") + frag("lit", 40, 200, 1.6) + frag("fenetre", 330, 60, 1.3) + frag("tapis", 200, 290, 1.2) + frag("lanterne", 280, 150, 0.7))
def cuisine():
    return (interieur_mur("#f6e8c8", "#8a5a2a", "#c9a066") + frag("table", 150, 200, 1.4) + frag("pain", 200, 190, 0.7) + frag("gateau", 250, 175, 0.8) + frag("fenetre", 40, 60, 1.2) + frag("feu_camp", 360, 180, 1.2) + frag("tonneau", 400, 240, 0.8))
def salle_bal():
    s = interieur_mur("#f8e8c0", "#c9a032", "#e8d098") + frag("trone", 190, 100, 1.5)
    for x in (40, 130, 330, 420): s += f'<rect x="{x}" y="40" width="22" height="210" fill="#e8d098" stroke="#333" stroke-width="3"/>' + frag("lanterne", x - 12, 60, 0.7)
    for x in range(30, 450, 60): s += f'<polygon points="{x},0 {x+20},50 {x+40},0" fill="#c0392b" stroke="#333" stroke-width="2"/>'
    return s + frag("tapis", 150, 300, 1.5)
def palais_ext():
    return (ciel("#9ad0f2", "#e8f0f8", 250) + colline(230, "#8ad672", 10) + sol(250, "#9ae082", "#6ab852") + frag("chateau", 110, 60, 1.9) + frag("arbre", 10, 140, 1.0) + frag("arbre", 400, 150, 1.0) + frag("fleurs", 110, 300, 1.1) + frag("fleurs", 300, 300, 1.1) + cloud(30, 20, .7) + cloud(340, 36, .6))
def village_route():
    return (ciel("#bfe4f2", "#f6f0d8", 230) + colline(215, "#9ad06a", 12) + sol(220, "#a0d878", "#7ab852") + f'<polygon points="0,300 480,250 480,290 0,350" fill="#d8b878" stroke="#b89858" stroke-width="3"/>' + frag("maison", 20, 80, 0.9) + frag("maison", 300, 90, 0.9) + frag("arbre", 200, 90, 0.9) + frag("panneau", 410, 110, 0.7) + sun(380, 8, .6) + cloud(150, 20, .6))
def marche():
    s = ciel("#ffe0a8", "#fff0d0", 250) + sol(250, "#d8b878", "#c09858")
    for i, (x, c) in enumerate([(20, "#d93a3a"), (170, "#3a8ad6"), (320, "#4caf50")]):
        s += f'<polygon points="{x},110 {x+70},60 {x+140},110" fill="{c}" stroke="#333" stroke-width="3"/><rect x="{x+10}" y="110" width="120" height="8" fill="#fff" stroke="#333" stroke-width="2"/>' + frag("table", x + 6, 150, 0.8) + frag("panier", x + 20, 128, 0.6) + frag("pain", x + 70, 150, 0.45) + frag("pomme", x + 90, 125, 0.45)
    return s + frag("tapis", 150, 290, 1.4)
def pont_riviere():
    return (ciel("#bfe4f2", "#e8f4f8", 200) + colline(190, "#7acb6a", 12) + sol(200, "#8ad672") + eau(250) + frag("pont", 120, 190, 1.5) + frag("arbre", 20, 80, 1.0) + frag("arbre", 410, 90, 1.0) + frag("rocher", 20, 290, 0.8) + sun(380, 10, .6))
def riviere():
    return (ciel("#bfe4f2", "#e8f4f8", 190) + colline(185, "#7acb6a", 12) + sol(190, "#8ad672") + eau(230) + frag("arbre", 30, 70, 1.1) + frag("buisson", 380, 160, 1.0) + frag("rocher", 300, 290, 1.0))
def mer():
    return ciel("#9ad4f2", "#e0f2fa", 170) + sun(380, 20, .7) + cloud(50, 30, .7) + cloud(220, 50, .5) + eau(160)
def ile_():
    return ciel("#9ad4f2", "#e0f2fa", 170) + sun(40, 14, .6) + eau(170, "#3a86c0", "#2a6aa0") + frag("ile", 130, 100, 1.5) + frag("nuage", 330, 30, .6)
def port():
    return (ciel("#bfe4f2", "#fff0d8", 200) + eau(200) + f'<rect y="260" width="480" height="100" fill="#b88850" stroke="#333" stroke-width="3"/>' + "".join(f'<line x1="{x}" y1="260" x2="{x}" y2="360" stroke="#333" stroke-width="2"/>' for x in range(0, 480, 48)) + frag("bateau", 20, 70, 1.3) + frag("tonneau", 330, 190, 0.9) + frag("tonneau", 400, 195, 0.9) + frag("maison", 300, 40, 0.7) + sun(400, 10, .5))
def plage():
    return ciel("#9ad4f2", "#e0f2fa", 170) + eau(150) + f'<polygon points="0,230 480,200 480,360 0,360" fill="#f2e3b0"/><polygon points="0,230 480,200 480,214 0,244" fill="#fff" opacity="0.6"/>' + frag("palmier", 20, 90, 1.5) + frag("rocher", 380, 270, 1.0) + sun(380, 10, .7)
def montagne():
    return ciel("#9ad0f2", "#e8f0f8", 220) + montagnes("#8a8aa0", 220) + montagnes("#b0b0c8", 250).replace("<polygon", '<polygon transform="translate(40 0)"', 1) + sol(250, "#8ab86a", "#6a9a4a") + frag("sapin", 30, 150, 1.1) + frag("sapin", 400, 140, 1.2) + frag("rocher", 200, 280, 1.2) + cloud(60, 20, .6)
def grotte_exterieur():
    return ciel("#d8e4c8", "#f2f0d8", 200) + montagnes("#9a947a", 240) + sol(250, "#b8a878", "#a09060") + frag("grotte_fermee", 140, 100, 1.4) + frag("rocher", 20, 270, 1.0) + frag("rocher", 380, 280, 0.9)
def grotte_interieur():
    s = f'<rect width="{W}" height="{H}" fill="#2a2420"/><polygon points="0,0 480,0 480,60 400,40 320,70 240,40 160,70 80,40 0,60" fill="#1a1612"/><rect y="260" width="{W}" height="100" fill="#4a3f36"/>'
    return s + frag("torche", 40, 90, 1.2) + frag("torche", 400, 90, 1.2) + frag("coffre_ouvert", 150, 190, 1.2) + frag("sac_or", 20, 250, 0.9) + frag("pieces", 330, 290, 1.0) + frag("sac_or", 400, 260, 0.9)
def desert():
    return ciel("#ffd89a", "#fff0d0", 220) + f'<polygon points="0,260 120,200 240,250 360,190 480,240 480,360 0,360" fill="#f0c878"/><polygon points="0,300 160,250 300,290 480,250 480,360 0,360" fill="#e8b860"/>' + frag("soleil", 360, 14, 0.9) + frag("palmier", 40, 120, 1.2) + frag("rocher", 380, 290, 0.8)
def nuit_etoiles():
    return ciel("#0b1230", "#2a3a7a", 360) + stars(80) + frag("lune", 360, 24, 1.1) + colline(300, "#14204a", 20) + frag("maison", 60, 190, 0.8)
def ciel_():
    return ciel("#7ac0f0", "#e8f4fc", 360) + cloud(30, 40, 1.0) + cloud(250, 90, .9) + cloud(120, 220, .8) + sun(390, 20, .8)
def piste_course():
    s = ciel("#bfe4f2", "#e8f6e0", 190) + colline(185, "#7acb6a", 12) + sol(190, "#8ad672") + f'<polygon points="0,250 480,230 480,330 0,350" fill="#d8b878" stroke="#b89858" stroke-width="3"/>'
    return s + frag("arbre", 330, 40, 1.2) + frag("buisson", 40, 170, 1.0) + frag("panneau", 410, 110, 0.7)
def ligne_arrivee():
    s = ciel("#bfe4f2", "#e8f6e0", 190) + colline(185, "#7acb6a", 12) + sol(190, "#8ad672") + f'<polygon points="0,250 480,230 480,330 0,350" fill="#d8b878" stroke="#b89858" stroke-width="3"/>'
    for i in range(8):
        for j in range(2):
            s += f'<rect x="{200+j*14}" y="{238+i*14 - j*0 }" width="14" height="14" fill="{"#222" if (i+j)%2 else "#fff"}"/>'
    return s + frag("drapeau", 160, 90, 1.0) + frag("drapeau", 300, 90, 1.0) + frag("arbre", 20, 50, 1.1)
def ville_nuit():
    s = ciel("#14204a", "#3a4a8a", 360) + stars(40) + frag("lune", 380, 20, .8) + sol(280, "#3a3a4a")
    for i, x in enumerate(range(10, 470, 110)): s += frag("maison", x, 150 + (i % 2) * 10, 0.8) + frag("fenetre", x + 28, 190, 0.45)
    return s
def ecole_cour():
    return ciel("#bfe4f2", "#f6f0d8", 220) + sol(220, "#b0b0a8", "#98988e") + frag("maison", 120, 80, 1.8) + frag("arbre", 20, 80, 1.1) + frag("arbre", 410, 90, 1.1) + frag("barriere", 40, 270, 1.0) + frag("drapeau", 400, 120, .7)

def colline_pature():
    return (ciel("#bfe4f2", "#eaf6e0", 230) + colline(190, "#8bc870", 26, 40) + colline(240, "#6fba5e", 22) + sol(280, "#5aa84e", "#4a9040") + frag("arbre", 20, 70, 1.2) + frag("barriere", 300, 230, 1.2) + frag("rocher", 380, 280, 0.8) + frag("fleurs", 60, 300, 1.1) + sun(390, 12, .7) + cloud(150, 24, .7))
def colline_soir():
    return (ciel("#f2894a", "#f9dd9a", 250) + sun(200, 120, 1.1) + colline(230, "#6a8a4a", 20, 10) + colline(280, "#4a6a3a", 20) + frag("arbre", 24, 120, 1.1) + frag("barriere", 300, 250, 1.2) + frag("rocher", 400, 290, 0.8))

def prairie_maisons():
    return (ciel("#bfe4f2", "#eaf6e0", 230) + colline(200, "#8bc870", 20, 20) + sol(240, "#7acb6a", "#62b552") + frag("maison_paille", 10, 130, 0.9) + frag("maison_bois", 170, 130, 0.9) + frag("maison_brique", 330, 125, 0.95) + frag("fleurs", 40, 300, 1.0) + frag("buisson", 380, 280, 0.9) + sun(400, 10, .6) + cloud(180, 20, .7))

def _etang(c1, c2, sol_c, eau_c, deco=""):
    return (ciel(c1, c2, 230) + colline(200, sol_c, 14, 30) + sol(235, sol_c) + f'<ellipse cx="260" cy="290" rx="190" ry="60" fill="{eau_c}" stroke="#333" stroke-width="3"/>' + deco)
def etang_ferme():
    return _etang("#bfe4f2", "#eaf6e0", "#8ad672", "#4a90c8", frag("maison", 10, 90, 0.9) + frag("roseaux", 390, 190, 0.9) + frag("nenuphar", 200, 280, 0.8) + frag("buisson", 380, 150, 0.8) + sun(400, 10, .6) + cloud(150, 20, .6))
def etang_hiver():
    return _etang("#c8d0dc", "#eef2f6", "#f2f6fa", "#c8e4f2", frag("sapin", 20, 70, 1.1) + frag("sapin", 400, 80, 1.0) + frag("bonhomme_neige", 340, 150, 0.8) + frag("roseaux", 30, 210, 0.8) + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#fff"/>' for x, y in [(40, 30), (120, 60), (200, 20), (290, 50), (360, 20), (440, 70), (80, 100), (250, 90)]))
def etang_printemps():
    return _etang("#9ad4f2", "#f4fbe8", "#9ae082", "#5aa8d8", frag("arbre", 20, 80, 1.1) + frag("fleurs", 380, 220, 1.0) + frag("roseaux", 400, 160, 0.8) + frag("nenuphar", 190, 280, 0.8) + frag("nenuphar", 300, 300, 0.7) + sun(380, 10, .7) + cloud(140, 20, .6))

LIEUX = {
 "etang_ferme": ("المزرعة والبركة", etang_ferme, ["duckling"]), "etang_hiver": ("البركة في الشتاء", etang_hiver, ["duckling"]), "etang_printemps": ("البركة في الربيع", etang_printemps, ["duckling"]),
 "prairie_maisons": ("المرج وثلاثة بيوت", prairie_maisons, ["pigs"]),
 "colline_pature": ("التل والمرعى", colline_pature, ["shepherd"]), "colline_soir": ("التل في المساء", colline_soir, ["shepherd"]),
 "foret": ("غابة", foret, ["layla", "crow", "lion", "hare"]), "foret_nuit": ("غابة في الليل", foret_nuit, ["layla"]), "foret_dense": ("غابة كثيفة", foret_dense, ["layla"]),
 "jardin": ("حديقة", jardin, ["cinderella"]), "jardin_puits": ("حديقة وبئر", jardin_puits, ["frog"]),
 "maison_interieur": ("داخل البيت", maison_int, ["cinderella", "layla"]), "chambre": ("غرفة نوم", chambre, ["layla"]), "cuisine": ("مطبخ", cuisine, ["cinderella"]),
 "salle_bal": ("قاعة الحفلة", salle_bal, ["cinderella"]), "palais_exterieur": ("القصر من الخارج", palais_ext, ["cinderella", "frog"]),
 "village_route": ("طريق القرية", village_route, ["djeha", "cinderella"]), "marche": ("السوق", marche, ["djeha"]),
 "pont_riviere": ("الجسر والنهر", pont_riviere, ["djeha"]), "riviere": ("نهر", riviere, []), "mer": ("البحر", mer, ["sindbad"]), "ile": ("جزيرة في البحر", ile_, ["sindbad"]),
 "port": ("الميناء", port, ["sindbad"]), "plage": ("الشاطئ", plage, ["sindbad"]), "montagne": ("الجبل", montagne, ["alibaba"]),
 "grotte_exterieur": ("المغارة من الخارج", grotte_exterieur, ["alibaba"]), "grotte_interieur": ("داخل المغارة والكنز", grotte_interieur, ["alibaba"]),
 "desert": ("الصحراء", desert, ["alibaba", "sindbad"]), "nuit_etoiles": ("ليل ونجوم", nuit_etoiles, []), "ciel": ("السماء", ciel_, []),
 "piste_course": ("مضمار السباق", piste_course, ["hare"]), "ligne_arrivee": ("خط النهاية", ligne_arrivee, ["hare"]), "ville_nuit": ("المدينة ليلا", ville_nuit, []),
 "cour_ecole": ("ساحة المدرسة", ecole_cour, []),
}
def lieu_svg(key):
    return SVG(W, H, LIEUX[key][1]())
