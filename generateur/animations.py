from svgkit import *
import math, re
import personnages as pe, animaux as an, decors as de

def inner(svg):
    return re.sub(r"^<svg[^>]*>|</svg>$", "", svg)
def size(svg):
    m = re.search(r'width="(\d+)" height="(\d+)"', svg); return int(m.group(1)), int(m.group(2))

PH = [1, 0, -1, 0]
CAT = pe.catalogue()

def walk_person(key):
    return lambda i, n: pe.person(**{**CAT[key][1], "ph": PH[i]})
def talk_person(key):
    return lambda i, n: pe.person(**{**CAT[key][1], "mouth": ["smile", "open"][i]})
def walk_animal(fn):
    return lambda i, n: fn(ph=PH[i])

def oiseau_vol(i, n): return an.oiseau([-8, 0, 8, 0][i])
def poisson_nage(i, n): return an.poisson([-1, 0, 1, 0][i])
def grenouille_saut(i, n):
    s = an.grenouille(i in (1, 2, 3))
    dy = [0, -30, -52, -26, 0][i]
    return SVG(240, 260, f'<g transform="translate(0 {60+dy})">{inner(s)}</g>')
def baleine_plonge(i, n):
    s = an.baleine(i < 2); dy = [0, 20, 50, 90, 130, 170][i]
    return SVG(300, 260, f'<g transform="translate(0 {dy})">{inner(s)}</g><rect y="150" width="300" height="110" fill="#4a90c8" opacity="0.75"/>' if i < 5 else f'<rect y="150" width="300" height="110" fill="#4a90c8" opacity="0.75"/>')
def papillon(i, n):
    s = [1, .6, .2, .6][i]
    b = ""
    for sg in (-1, 1):
        b += E(100 + sg * 34 * s, 70, 34 * s, 44, "#e87ac0", 3, sg * 20) + E(100 + sg * 28 * s, 118, 24 * s, 28, "#f2a0d8", 3, -sg * 20)
    b += E(100, 94, 7, 38, "#3a2a2a") + L(96, 58, 84, 38, OUT, 2.5) + L(104, 58, 116, 38, OUT, 2.5)
    return SVG(200, 170, b)
def porte(i, n):
    ang = [0, 25, 50, 70, 80][i]; dx = 84 * math.cos(math.radians(ang)); skew = 84 * math.sin(math.radians(ang)) * 0.25
    b = R(8, 8, 84, 138, "#6a4a2a", 3) + P("M14 144 L14 50 A36 40 0 0 1 86 50 L86 144Z", "#14100c")
    b += P(f"M14 144 L{14+dx*0.84} {144+skew} L{14+dx*0.84} {50-skew} L14 50Z", "#8a5a2a") + C(14 + dx * 0.7, 98, 3, "#f1c40f", 1.5)
    return SVG(110, 154, b)
def feu(i, n):
    h = [1, .9, 1.1, .95][i]; w = [1, 1.1, .9, 1.05][i]
    b = R(14, 118, 92, 12, "#6a4a2a", 4) + L(20, 132, 100, 112, "#8a5a2a", 8) + L(100, 132, 20, 112, "#7a4a2a", 8)
    b += P(f"M60 {112-96*h} Q{60+36*w} {112-60*h} {76} 112 L44 112 Q{60-36*w} {112-60*h} 60 {112-96*h}Z", "#e74c3c") + P(f"M60 {112-62*h} Q{60+20*w} {112-40*h} 68 112 L52 112 Q{60-20*w} {112-40*h} 60 {112-62*h}Z", "#f39c12", 2)
    return SVG(120, 140, b)
def vagues(i, n):
    b = '<rect width="240" height="140" fill="#cfe8f6"/><rect y="40" width="240" height="100" fill="#4a90c8"/>'
    for k, yy in enumerate((60, 86, 112)):
        off = (i * 20 + k * 10) % 40
        b += f'<path d="' + "".join(f"M{x-off} {yy} q10 -10 20 0 " for x in range(0, 280, 40)) + '" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity="0.8"/>'
    return SVG(240, 140, b)
def horloge(i, n):
    w, h, b = de.horloge(12, (i * 60 // n))
    return SVG(w, h, b)
def piece(i, n):
    rx = abs(math.cos(math.pi * i / n)) * 40 + 3
    return SVG(100, 100, E(50, 50, rx, 40, "#ffd700", 3.5) + (E(50, 50, max(rx - 10, 1), 30, "none", 2) if rx > 14 else ""))
def etoile(i, n):
    s = [1, 1.25, 0.9, 1.15][i]
    return SVG(100, 100, G(de.etoile()[2], 50 - 35 * s, 50 - 35 * s, s))
def soleil(i, n):
    r = ""
    for a in range(0, 360, 30):
        aa = a + i * 7.5
        r += L(60 + 40 * math.cos(math.radians(aa)), 60 + 40 * math.sin(math.radians(aa)), 60 + 54 * math.cos(math.radians(aa)), 60 + 54 * math.sin(math.radians(aa)), "#f39c12", 6)
    return SVG(120, 120, r + C(60, 60, 32, "#ffd23c", 3))
def pluie(i, n):
    b = "".join(f'<path d="M{x} {(y + i*20) % 150} l-5 14" stroke="#3a86c0" stroke-width="3" stroke-linecap="round"/>' for x, y in [(20, 10), (50, 70), (80, 30), (110, 100), (140, 50), (170, 120), (190, 20), (35, 120), (95, 140), (155, 5)])
    return SVG(210, 170, de.nuage()[2].join(['<g transform="translate(25 6)">', '</g>']) + b)
def neige(i, n):
    b = "".join(f'<circle cx="{x + (3 if i%2 else -3)}" cy="{(y + i*18) % 150}" r="5" fill="#fff" stroke="#9ac" stroke-width="1.5"/>' for x, y in [(20, 10), (50, 70), (80, 30), (110, 100), (140, 50), (170, 120), (190, 20), (35, 120), (95, 140), (155, 5)])
    return SVG(210, 170, '<g transform="translate(25 6)">' + de.nuage()[2] + '</g>' + b)
def bateau(i, n):
    rot = [-4, 0, 4, 0][i]; dy = [0, 4, 0, -4][i]
    b = f'<g transform="translate(0 {dy}) rotate({rot} 100 130)">' + de.bateau()[2] + '</g>' + f'<rect y="146" width="200" height="40" fill="#4a90c8" opacity="0.85"/>'
    return SVG(200, 190, b)
def baguette(i, n):
    b = de.etoile  # placeholder
    base = L(30, 160, 120, 70, "#8e5a2b", 7)
    pts = [(120, 60, 1.0), (150, 40, .6), (100, 30, .5), (150, 90, .5), (80, 70, .4)]
    s = ""
    for k, (x, y, sc) in enumerate(pts):
        if k <= i: s += G(de.etoile()[2], x - 35 * sc * (0.6 + 0.2 * (i - k)), y - 35 * sc * (0.6 + 0.2 * (i - k)), sc * (0.6 + 0.2 * (i - k)))
    return SVG(200, 180, base + s)
def coeur(i, n):
    s = [1, 1.25, 1, 0.9][i]
    return SVG(120, 110, G(P("M60 96 C10 60 10 20 40 20 C55 20 60 32 60 38 C60 32 65 20 80 20 C110 20 110 60 60 96Z", "#e74c3c"), 60 - 60 * s, 55 - 55 * s, s))
def nuage_vent(i, n):
    return SVG(300, 100, G(de.nuage()[2], 20 + i * 30, 10, 1))
def porte_hache(i, n): return SVG(10, 10, "")

ANIMS = {}
def add(key, label, n, fn, tags=()): ANIMS[key] = (label, n, fn, list(tags))

for k, lab, tg in [("cendrillon_bal", "سندريلا تمشي", ["cinderella"]), ("laila", "ليلى تمشي", ["layla"]), ("djeha", "جحا يمشي", ["djeha"]), ("ali_baba", "علي بابا يمشي", ["alibaba"]),
                   ("sindbad", "السندباد يمشي", ["sindbad"]), ("prince", "الأمير يمشي", ["cinderella"]), ("fee", "الجنية تمشي", ["cinderella"]), ("bucheron", "الحطاب يمشي", ["layla"]),
                   ("morgiane", "مرجانة تمشي", ["alibaba"]), ("berger", "الراعي يمشي", ["shepherd"]), ("princesse", "الأميرة تمشي", ["frog"]), ("garcon", "ولد يمشي", []), ("fille", "بنت تمشي", [])]:
    add("marche_" + k, lab, 4, walk_person(k), tg)
for k, lab, tg in [("cendrillon_bal", "سندريلا تتكلم", ["cinderella"]), ("laila", "ليلى تتكلم", ["layla"]), ("djeha", "جحا يتكلم", ["djeha"]), ("ali_baba", "علي بابا يتكلم", ["alibaba"]),
                   ("grand_mere", "الجدة تتكلم", ["layla"]), ("roi", "الملك يتكلم", ["frog"])]:
    add("parle_" + k, lab, 2, talk_person(k), tg)
for k, lab, fn, tg in [("loup", "الذئب يجري", an.loup, ["layla"]), ("ane", "الحمار يمشي", an.ane, ["djeha"]), ("lion", "الأسد يمشي", an.lion, ["lion"]),
                       ("renard", "الثعلب يجري", an.renard, ["crow"]), ("lievre", "الأرنب يجري", an.lievre, ["hare"]), ("tortue", "السلحفاة تمشي", an.tortue, ["hare"]),
                       ("cheval", "الحصان يجري", an.cheval, []), ("chameau", "الجمل يمشي", an.chameau, ["alibaba"]), ("chien", "الكلب يجري", an.chien, []), ("mouton", "الخروف يمشي", an.mouton, ["shepherd"]), ("cochon", "الخنزير يمشي", an.cochon, ["pigs"]), ("canard", "البطة تمشي", an.canard, ["duckling"]), ("poule", "الدجاجة تمشي", an.poule, []), ("souris", "الفأر يجري", an.souris, ["lion"])]:
    add("marche_" + k, lab, 4, walk_animal(fn), tg)
def maison_effondre(i, n):
    sy = [1, .85, .6, .35, .18][i]; rot = [0, -2, 3, -4, 0][i]
    b = G(de.maison_paille()[2], 0, 130 * (1 - sy), 1, sy, rot, 75, 130)
    if i:
        b += "".join(L(20 + k * 30, 140, 10 + k * 34 + i * 6, 150 + i * 4, "#c9a030", 4) for k in range(5))
        b += "".join(E(30 + k * 38, 150 - i * 3, 4 + i * 2, 3 + i, "#d8d0c0", 0) for k in range(4))
    return SVG(180, 170, b)
add("maison_s_effondre", "بيت يتهدّم", 5, maison_effondre, ["pigs"])
def oeuf_eclot(i, n):
    b = E(100, 130, 40, 50, "#f4ecd8") if i < 2 else P("M60 130 Q60 80 100 78 Q140 80 140 130 L128 118 L116 132 L100 116 L86 132 L72 118Z", "#f4ecd8") if i == 2 else P("M60 134 Q60 120 100 118 Q140 120 140 134 Q130 182 100 182 Q70 182 60 134Z", "#f4ecd8")
    if i == 1: b += P("M80 100 L92 114 L84 126 L98 140", "none", 3)
    if i >= 2: b += C(100, 98 - (i - 2) * 6, 20, "#f2d04a") + C(94, 94 - (i - 2) * 6, 3, "#222", 0) + C(108, 94 - (i - 2) * 6, 3, "#222", 0) + T([(98, 104 - (i - 2) * 6), (108, 106 - (i - 2) * 6), (98, 110 - (i - 2) * 6)], "#e8872a", 2)
    return SVG(200, 200, b)
def cygne_nage(i, n):
    dy = [0, 3, 0, -3][i]
    return SVG(230, 210, f'<g transform="translate({i*3} {dy})">{inner(an.cygne())}</g>')
add("oeuf_eclot", "بيضة تنفقس", 4, oeuf_eclot, ["duckling"]); add("cygne_nage", "بجعة تسبح", 4, cygne_nage, ["duckling"])
add("oiseau_vole", "عصفور يطير", 4, oiseau_vol); add("poisson_nage", "سمكة تسبح", 4, poisson_nage, ["sindbad"])
add("grenouille_saute", "ضفدع يقفز", 5, grenouille_saut, ["frog"]); add("baleine_plonge", "الحوت يغوص", 6, baleine_plonge, ["sindbad"])
add("papillon", "فراشة", 4, papillon); add("porte_s_ouvre", "باب ينفتح", 5, porte, ["alibaba"]); add("feu", "نار تشتعل", 4, feu); add("vagues", "أمواج", 4, vagues, ["sindbad"])
add("horloge_tourne", "ساعة تدور", 8, horloge, ["cinderella"]); add("piece_tourne", "قطعة نقود تدور", 6, piece, ["alibaba"]); add("etoile_scintille", "نجمة تلمع", 4, etoile)
add("soleil_tourne", "شمس مشرقة", 4, soleil); add("pluie", "مطر", 4, pluie); add("neige", "ثلج", 4, neige, ["duckling"]); add("bateau_tangue", "سفينة تتمايل", 4, bateau, ["sindbad"])
add("baguette_magique", "عصا سحرية", 5, baguette, ["cinderella"]); add("coeur_bat", "قلب ينبض", 4, coeur); add("nuage_passe", "سحابة تمرّ", 5, nuage_vent)
