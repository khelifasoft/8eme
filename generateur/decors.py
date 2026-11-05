from svgkit import *
import math

# chaque objet : (largeur, hauteur, corps SVG)
def arbre(): return 120, 160, R(52, 90, 18, 66, "#8a5a2a", 3) + C(60, 62, 40, "#4caf50") + C(34, 82, 28, "#5cc060") + C(88, 80, 28, "#43a047")
def sapin(): return 110, 160, R(48, 120, 14, 36, "#8a5a2a", 3) + T([(55, 10), (15, 70), (95, 70)], "#2e7d32") + T([(55, 40), (8, 104), (102, 104)], "#388e3c") + T([(55, 70), (2, 130), (108, 130)], "#43a047")
def palmier(): return 140, 170, P("M70 160 Q60 100 76 52", "none", 12) + P("M70 160 Q60 100 76 52", "none", 7).replace(OUT, "#a8743a") + "".join(P(f"M76 52 Q{76+dx} {20+dy} {76+2*dx} {46+dy*2}Q{76+dx} {40} 76 52Z", "#3fa34d", 2.5) for dx, dy in [(-50, 4), (-30, -10), (0, -18), (30, -10), (50, 4)]) + C(70, 56, 6, "#8a5a2a", 2) + C(82, 58, 6, "#8a5a2a", 2)
def buisson(): return 120, 70, C(34, 44, 26, "#3f9a46") + C(62, 36, 30, "#4caf50") + C(90, 46, 24, "#43a047")
def fleurs(): return 110, 80, "".join(L(x, 40, x, 76, "#3a8a3a", 4) + C(x, 32, 11, c) + C(x, 32, 4, "#f1c40f", 1.5) for x, c in [(22, "#e74c3c"), (48, "#f39c12"), (74, "#9b59b6"), (96, "#e84393")])
def rocher(): return 120, 80, P("M8 76 L26 34 L56 14 L92 30 L112 76Z", "#9a9aa4") + P("M26 34 L56 50 L92 30", "none", 2) + P("M56 50 L60 76", "none", 2)
def maison(): return 150, 140, R(20, 62, 110, 72, "#f0d9a8", 3) + T([(8, 66), (75, 12), (142, 66)], "#c0563a") + R(62, 90, 28, 44, "#8a5a2a", 3) + C(84, 114, 2.5, "#f1c40f", 0) + R(28, 80, 24, 22, "#bfe0f0", 3) + R(102, 80, 22, 22, "#bfe0f0", 3) + R(104, 14, 14, 30, "#a85a3a", 2)
def chateau(): return 200, 170, R(30, 70, 140, 92, "#d8d2e0", 3) + R(10, 40, 42, 122, "#c4bcd2", 3) + R(148, 40, 42, 122, "#c4bcd2", 3) + T([(4, 44), (31, 4), (58, 44)], "#7a3a8a") + T([(142, 44), (169, 4), (196, 44)], "#7a3a8a") + P("M80 162 L80 114 A20 20 0 0 1 120 114 L120 162Z", "#5a3a2a") + L(31, 4, 31, -10, OUT, 3) + T([(31, -10), (48, -4), (31, 2)], "#e74c3c", 2) + "".join(R(x, 90, 12, 18, "#9ecbe8", 2) for x in (22, 160)) + "".join(R(x, 76, 10, 12, "#bbb", 2) for x in (50, 70, 90, 110, 130))
def tour(): return 80, 180, R(18, 40, 44, 136, "#c8c0b0", 3) + T([(10, 44), (40, 2), (70, 44)], "#b0453a") + R(34, 70, 12, 22, "#444", 2) + R(34, 110, 12, 22, "#444", 2)
def puits(): return 110, 130, R(20, 66, 70, 52, "#b8b0a4", 4) + E(55, 66, 35, 10, "#334", 3) + L(24, 66, 24, 20, "#8a5a2a", 6) + L(86, 66, 86, 20, "#8a5a2a", 6) + T([(14, 24), (55, 0), (96, 24)], "#a8503a") + L(55, 14, 55, 44, OUT, 2) + R(48, 44, 14, 12, "#a07040", 2)
def porte_fermee(): return 100, 150, R(8, 8, 84, 138, "#6a4a2a", 3) + P("M14 144 L14 50 A36 40 0 0 1 86 50 L86 144Z", "#8a5a2a") + L(50, 14, 50, 144, OUT, 2) + C(40, 90, 4, "#f1c40f", 1.5) + C(60, 90, 4, "#f1c40f", 1.5)
def porte_ouverte(): return 120, 150, R(8, 8, 84, 138, "#6a4a2a", 3) + P("M14 144 L14 50 A36 40 0 0 1 86 50 L86 144Z", "#1a1410") + P("M14 144 L14 50 L-4 60 L-4 134Z", "#8a5a2a") + C(2, 94, 3, "#f1c40f", 1.5)
def fenetre(): return 80, 90, R(8, 8, 64, 74, "#bfe0f0", 3) + L(40, 8, 40, 82, OUT, 3) + L(8, 45, 72, 45, OUT, 3) + R(2, 80, 76, 8, "#8a5a2a", 2)
def pont(): return 240, 100, P("M0 50 Q120 -10 240 50 L240 70 Q120 10 0 70Z", "#a07040") + "".join(L(x, 24 + abs(120 - x) / 6, x, 56 + abs(120 - x) / 6 * .3, OUT, 3) for x in range(20, 230, 30)) + P("M0 34 Q120 -26 240 34", "none", 4)
def bateau(): return 200, 170, P("M10 110 L190 110 L160 150 L40 150Z", "#8a5a2a") + L(100, 110, 100, 10, "#5a3a1a", 6) + T([(104, 14), (104, 100), (170, 100)], "#f5f0e0") + T([(96, 30), (96, 100), (40, 100)], "#e8e0c8") + T([(100, 10), (126, 18), (100, 26)], "#e74c3c", 2)
def barque(): return 160, 70, P("M6 24 L154 24 L124 62 L36 62Z", "#a8743a") + L(30, 36, 130, 36, OUT, 2)
def planche(): return 160, 40, R(6, 10, 148, 22, "#b88850", 4) + L(30, 10, 30, 32, OUT, 1.5) + L(90, 10, 90, 32, OUT, 1.5) + L(130, 10, 130, 32, OUT, 1.5)
def ile(): return 220, 150, P("M6 130 Q40 80 110 78 Q180 80 214 130Z", "#e8d28a") + R(104, 40, 10, 40, "#8a5a2a", 2) + "".join(P(f"M109 42 Q{109+dx} {14+dy} {109+2*dx} {36+dy}Q{109+dx} 32 109 42Z", "#3fa34d", 2) for dx, dy in [(-34, 4), (-14, -8), (18, -8), (38, 4)])
def grotte_ouverte(): return 200, 150, P("M6 146 Q10 20 100 12 Q190 20 194 146Z", "#7a7468") + P("M44 146 Q44 52 100 46 Q156 52 156 146Z", "#14100c") + P("M30 60 L50 40 M150 44 L172 64", "none", 2)
def grotte_fermee(): return 200, 150, P("M6 146 Q10 20 100 12 Q190 20 194 146Z", "#7a7468") + P("M44 146 Q44 52 100 46 Q156 52 156 146Z", "#a0988a") + P("M60 146 Q60 66 100 60 Q140 66 140 146Z", "#8a8478", 2)
def coffre(ouvert=False):
    b = R(14, 62, 112, 62, "#8a5a2a", 6) + R(14, 78, 112, 8, "#f1c40f", 2) + R(60, 74, 20, 22, "#f1c40f", 3)
    if ouvert:
        b = R(14, 62, 112, 62, "#8a5a2a", 6) + P("M14 62 L20 22 L120 22 L126 62Z", "#6a4a1a") + E(70, 62, 50, 10, "#f1c40f") + "".join(C(x, 56, 7, "#ffd700", 2) for x in (36, 54, 72, 90, 104)) + R(60, 78, 20, 22, "#f1c40f", 3)
    else:
        b = P("M14 62 Q70 14 126 62Z", "#8a5a2a", 4) + b
    return 140, 130, b
def sac_or(): return 100, 110, P("M20 100 Q8 56 34 34 L66 34 Q92 56 80 100Z", "#d6b878") + L(34, 34, 66, 34, OUT, 5) + TXT(50, 78, "$", 30, "#8a6a1a") + P("M36 30 Q50 14 64 30", "none", 3)
def pieces(): return 110, 70, "".join(E(x, y, 20, 8, "#ffd700", 2.5) for x, y in [(30, 58), (60, 58), (84, 56), (44, 44), (72, 42), (58, 30)])
def fromage(): return 100, 80, P("M6 64 L8 34 L94 20 L94 64Z", "#f6d44c") + P("M6 34 L94 20", "none", 2) + C(30, 52, 7, "#e0b020", 2) + C(62, 46, 9, "#e0b020", 2) + C(80, 32, 5, "#e0b020", 2)
def balle_or(): return 70, 70, C(35, 35, 28, "#f1c40f") + P("M18 26 Q26 16 38 14", "none", 3) 
def panier(): return 100, 100, P("M10 46 L90 46 L80 92 L20 92Z", "#c9a063") + P("M18 46 Q50 -8 82 46", "none", 5) + R(14, 42, 72, 10, "#f2f2f2", 3) + L(30, 50, 34, 90, OUT, 1.5) + L(50, 50, 50, 90, OUT, 1.5) + L(70, 50, 66, 90, OUT, 1.5)
def pain(): return 110, 70, E(55, 38, 46, 26, "#d8a050") + "".join(P(f"M{x} 22 L{x+8} 52", "none", 3) for x in (30, 48, 66))
def gateau(): return 100, 100, R(14, 50, 72, 40, "#e8a0b8", 6) + R(14, 38, 72, 16, "#fff0d8", 6) + L(50, 38, 50, 20, "#e74c3c", 4) + P("M50 10 Q56 18 50 22 Q44 18 50 10Z", "#f39c12", 1.5)
def soulier_verre(): return 140, 90, P("M12 72 Q22 40 30 14 L58 14 Q60 46 96 58 Q128 62 128 76 Q128 84 118 84 L18 84 Q10 82 12 72Z", "#cfeaf8", 3, 'fill-opacity="0.8"') + P("M34 24 Q38 44 56 54", "none", 2, 'stroke-opacity="0.6"') + C(40, 22, 3, "#fff", 1)
def couronne(): return 100, 70, T([(10, 60), (10, 14), (30, 36), (50, 6), (70, 36), (90, 14), (90, 60)], "#f1c40f") + C(50, 14, 5, "#e74c3c", 2) + C(14, 18, 4, "#3498db", 1.5) + C(86, 18, 4, "#3498db", 1.5)
def horloge(h=12, m=0):
    a = math.radians(h % 12 * 30 + m / 2 - 90); b = math.radians(m * 6 - 90)
    body = C(60, 60, 54, "#fffbe8", 4) + "".join(L(60 + 46 * math.cos(math.radians(i * 30)), 60 + 46 * math.sin(math.radians(i * 30)), 60 + 52 * math.cos(math.radians(i * 30)), 60 + 52 * math.sin(math.radians(i * 30)), OUT, 3) for i in range(12))
    body += L(60, 60, 60 + 28 * math.cos(a), 60 + 28 * math.sin(a), OUT, 6) + L(60, 60, 60 + 42 * math.cos(b), 60 + 42 * math.sin(b), OUT, 4) + C(60, 60, 4, OUT, 0)
    return 120, 120, body
def cle(): return 100, 60, C(22, 30, 16, "#f1c40f") + C(22, 30, 6, "#fff", 2) + R(36, 26, 56, 8, "#f1c40f", 3) + R(76, 34, 8, 14, "#f1c40f", 2) + R(62, 34, 8, 10, "#f1c40f", 2)
def lampe(): return 130, 80, P("M16 52 Q40 70 80 66 Q110 62 118 44 L100 48 Q80 30 50 40 Q30 40 16 52Z", "#e8b030") + P("M16 52 L2 40 L10 36 L24 46", "#e8b030", 3) + P("M52 40 Q56 28 64 30 Q70 36 60 40", "#e8b030", 3) + P("M100 48 Q124 36 120 28", "none", 4)
def trone(): return 110, 150, R(20, 14, 70, 90, "#a03030", 8) + R(10, 90, 90, 40, "#c04040", 6) + R(14, 126, 12, 20, "#8a5a2a", 2) + R(84, 126, 12, 20, "#8a5a2a", 2) + C(55, 22, 8, "#f1c40f", 2)
def table(): return 150, 90, R(6, 10, 138, 14, "#a8743a", 4) + R(18, 24, 12, 58, "#8a5a2a", 2) + R(120, 24, 12, 58, "#8a5a2a", 2)
def lit(): return 160, 100, R(8, 54, 144, 30, "#8a5a2a", 4) + R(14, 38, 132, 22, "#f2f2f2", 6) + R(14, 38, 40, 22, "#c9a7f2", 6) + R(6, 20, 10, 66, "#6a4a1a", 3)
def chaise(): return 80, 110, R(14, 6, 52, 50, "#a8743a", 6) + R(10, 50, 60, 12, "#8a5a2a", 3) + R(14, 60, 10, 44, "#8a5a2a", 2) + R(56, 60, 10, 44, "#8a5a2a", 2)
def torche(): return 60, 130, R(24, 50, 12, 70, "#8a5a2a", 3) + P("M30 6 Q50 28 42 50 L18 50 Q10 28 30 6Z", "#f39c12") + P("M30 22 Q40 34 36 48 L24 48 Q20 34 30 22Z", "#f1c40f", 2)
def feu_camp(): return 120, 100, R(14, 76, 92, 12, "#6a4a2a", 4) + L(20, 90, 100, 70, "#8a5a2a", 8) + L(100, 90, 20, 70, "#7a4a2a", 8) + P("M60 10 Q92 44 76 72 L44 72 Q28 44 60 10Z", "#e74c3c") + P("M60 30 Q78 52 68 70 L52 70 Q42 52 60 30Z", "#f39c12", 2)
def barriere(): return 180, 70, "".join(R(x, 8, 14, 58, "#c9a063", 3) for x in range(8, 170, 36)) + R(2, 20, 176, 10, "#b88850", 3) + R(2, 42, 176, 10, "#b88850", 3)
def lune(): return 90, 90, P("M56 8 A38 38 0 1 0 82 62 A30 30 0 1 1 56 8Z", "#f6e8a0")
def soleil():
    r = "".join(L(60 + 40 * math.cos(math.radians(a)), 60 + 40 * math.sin(math.radians(a)), 60 + 54 * math.cos(math.radians(a)), 60 + 54 * math.sin(math.radians(a)), "#f39c12", 6) for a in range(0, 360, 30))
    return 120, 120, r + C(60, 60, 32, "#ffd23c", 3)
def nuage(): return 160, 80, C(44, 48, 24, "#fff", 3) + C(74, 36, 30, "#fff", 3) + C(106, 46, 26, "#fff", 3) + R(30, 48, 90, 24, "#fff", 12, 0)
def etoile(): return 70, 70, T([(35, 4), (43, 26), (66, 26), (48, 40), (55, 64), (35, 50), (15, 64), (22, 40), (4, 26), (27, 26)], "#ffd23c", 2.5)
def filet(): return 150, 110, "".join(L(8, 10 + y, 142, 10 + y, "#7a7a50", 2.5) for y in range(0, 100, 16)) + "".join(L(8 + x, 6, 8 + x, 104, "#7a7a50", 2.5) for x in range(0, 140, 16)) + P("M6 8 L144 8", "none", 4)
def hache(): return 90, 110, L(40, 100, 44, 12, "#8a5a2a", 8) + P("M42 12 Q86 2 80 50 Q52 48 42 12Z", "#bdc3c7")
def citrouille(): return 110, 100, E(34, 60, 26, 32, "#f39c12") + E(76, 60, 26, 32, "#f39c12") + E(55, 60, 28, 34, "#f7a52c") + R(51, 14, 8, 16, "#3a7a2a", 2)
def carrosse(): return 200, 130, E(100, 66, 64, 38, "#f7a52c") + R(60, 50, 80, 36, "#bfe0f0", 6) + C(50, 108, 22, "#c0392b") + C(50, 108, 8, "#f1c40f", 2) + C(150, 108, 22, "#c0392b") + C(150, 108, 8, "#f1c40f", 2) + R(94, 18, 12, 14, "#3a7a2a", 2)
def navet(): return 110, 140, P("M55 130 Q4 110 14 66 Q30 40 55 44 Q80 40 96 66 Q106 110 55 130Z", "#f4f0e8") + P("M14 70 Q30 52 55 56 Q80 52 96 70 Q70 60 55 64 Q40 60 14 70Z", "#b57edc", 2) + P("M44 44 Q30 8 18 2 M55 44 Q55 6 55 -2 M66 44 Q80 8 92 2", "none", 5)
def champignon(): return 80, 80, R(30, 40, 20, 36, "#f5ede0", 6) + P("M6 44 Q40 -16 74 44Z", "#d93a3a") + C(26, 30, 5, "#fff", 0) + C(46, 20, 5, "#fff", 0) + C(58, 34, 4, "#fff", 0)
def panneau(): return 90, 130, R(40, 40, 10, 86, "#8a5a2a", 3) + P("M6 48 L68 48 L80 34 L68 20 L6 20Z", "#c9a063") + P("M84 84 L22 84 L10 70 L22 56 L84 56Z", "#b88850")
def tente(): return 160, 110, T([(80, 6), (8, 102), (152, 102)], "#e8a23a") + P("M80 6 L62 102 L98 102Z", "#7a3a1a") 
def tonneau(): return 90, 100, E(45, 50, 34, 44, "#a8743a") + L(12, 28, 78, 28, OUT, 3) + L(12, 72, 78, 72, OUT, 3)
def drapeau(): return 80, 140, L(20, 8, 20, 134, "#6a4a1a", 5) + T([(22, 12), (72, 28), (22, 48)], "#d93a3a", 2.5)
def epee(): return 60, 130, L(30, 10, 30, 100, "#bdc3c7", 8) + L(12, 96, 48, 96, "#8a5a2a", 7) + L(30, 96, 30, 122, "#6a3a1a", 7)
def bouclier(): return 90, 110, P("M45 6 L84 20 Q84 70 45 104 Q6 70 6 20Z", "#3a5a9c", 4) + T([(45, 28), (52, 46), (70, 46), (56, 56), (62, 74), (45, 64), (28, 74), (34, 56), (20, 46), (38, 46)], "#f1c40f", 1.5)
def echelle(): return 70, 150, L(16, 6, 16, 144, "#8a5a2a", 6) + L(54, 6, 54, 144, "#8a5a2a", 6) + "".join(L(16, y, 54, y, "#8a5a2a", 5) for y in range(24, 140, 22))
def lanterne(): return 60, 100, R(16, 26, 28, 50, "#f6e8a0", 5) + R(12, 20, 36, 8, "#444", 2) + R(12, 74, 36, 8, "#444", 2) + P("M20 20 Q30 0 40 20", "none", 3)
def pomme(): return 70, 70, C(35, 40, 24, "#d93a3a") + L(35, 18, 38, 6, "#6a3a1a", 4) + P("M38 10 Q52 2 54 14 Q44 16 38 10Z", "#4caf50", 2)
def souche(): return 100, 70, E(50, 54, 38, 12, "#8a5a2a", 3) + R(14, 24, 72, 30, "#a8743a", 3) + E(50, 24, 36, 11, "#d8b070", 3)
def tapis(): return 160, 70, P("M10 20 L150 20 L136 56 L24 56Z", "#b32a3a") + P("M22 26 L138 26 L128 50 L32 50Z", "none", 2.5) + "".join(L(10 + i * 14, 20, 6 + i * 14, 12, "#f1c40f", 2) for i in range(11))

OBJETS = {
 "arbre": ("شجرة", arbre, ["layla", "crow"]), "sapin": ("صنوبر", sapin, ["layla"]), "palmier": ("نخلة", palmier, ["sindbad", "alibaba"]),
 "buisson": ("شجيرة", buisson, []), "fleurs": ("زهور", fleurs, ["cinderella"]), "rocher": ("صخرة", rocher, ["alibaba"]),
 "maison": ("بيت", maison, ["layla", "djeha"]), "chateau": ("قصر", chateau, ["cinderella", "frog"]), "tour": ("برج", tour, []),
 "puits": ("بئر", puits, ["frog"]), "porte_fermee": ("باب مغلق", porte_fermee, ["alibaba"]), "porte_ouverte": ("باب مفتوح", porte_ouverte, ["alibaba"]),
 "fenetre": ("نافذة", fenetre, []), "pont": ("جسر", pont, ["djeha"]), "bateau": ("سفينة", bateau, ["sindbad"]), "barque": ("قارب", barque, ["sindbad"]),
 "planche": ("لوح خشبي", planche, ["sindbad"]), "ile": ("جزيرة", ile, ["sindbad"]), "grotte_ouverte": ("مغارة مفتوحة", grotte_ouverte, ["alibaba"]),
 "grotte_fermee": ("مغارة مغلقة", grotte_fermee, ["alibaba"]), "coffre_ferme": ("صندوق مغلق", lambda: coffre(False), ["alibaba"]),
 "coffre_ouvert": ("صندوق كنز مفتوح", lambda: coffre(True), ["alibaba"]), "sac_or": ("كيس ذهب", sac_or, ["alibaba"]), "pieces": ("قطع ذهبية", pieces, ["alibaba"]),
 "fromage": ("قطعة جبن", fromage, ["crow"]), "balle_or": ("كرة ذهبية", balle_or, ["frog"]), "panier": ("سلّة", panier, ["layla"]),
 "pain": ("خبز", pain, []), "gateau": ("كعكة", gateau, []), "soulier_verre": ("حذاء من زجاج", soulier_verre, ["cinderella"]), "couronne": ("تاج", couronne, ["frog", "cinderella"]),
 "horloge_minuit": ("ساعة منتصف الليل", lambda: horloge(12, 0), ["cinderella"]), "horloge_trois": ("ساعة الثالثة", lambda: horloge(3, 0), []),
 "cle": ("مفتاح", cle, []), "lampe": ("مصباح سحري", lampe, []), "trone": ("عرش", trone, ["frog"]), "table": ("طاولة", table, []), "lit": ("سرير", lit, ["layla"]),
 "chaise": ("كرسي", chaise, []), "torche": ("مشعل", torche, ["alibaba"]), "feu_camp": ("نار", feu_camp, []), "barriere": ("سياج", barriere, []),
 "lune": ("قمر", lune, []), "soleil": ("شمس", soleil, []), "nuage": ("سحابة", nuage, []), "etoile": ("نجمة", etoile, []), "filet": ("شبكة صيد", filet, ["lion"]),
 "hache": ("فأس", hache, ["layla"]), "citrouille": ("يقطينة", citrouille, ["cinderella"]), "carrosse": ("عربة", carrosse, ["cinderella"]),
 "navet": ("لفت كبير", navet, []), "champignon": ("فطر", champignon, ["layla"]), "panneau": ("لافتة طريق", panneau, ["hare"]),
 "tente": ("خيمة", tente, []), "tonneau": ("برميل", tonneau, ["sindbad"]), "drapeau": ("علم", drapeau, ["hare"]), "epee": ("سيف", epee, ["alibaba"]),
 "bouclier": ("درع", bouclier, []), "echelle": ("سلّم", echelle, []), "lanterne": ("فانوس", lanterne, []), "pomme": ("تفاحة", pomme, []),
 "souche": ("جذع شجرة", souche, ["layla"]), "tapis": ("زربية", tapis, []),
}

def objet_svg(key):
    w, h, b = OBJETS[key][1]()
    pad = 26
    return SVG(w + 2 * pad, h + 2 * pad, f'<g transform="translate({pad} {pad})">{b}</g>')

def frag(key, x, y, s=1):
    w, h, b = OBJETS[key][1]()
    return f'<g transform="translate({x} {y}) scale({s})">{b}</g>'
