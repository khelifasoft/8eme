"""Images de « Théorie Scratch » : couvertures des sept leçons (4:3), figure des formes de blocs et schéma de l'écran de Scratch
(le schéma est inséré dans la page ; ses zones sont cliquables : voir theorie_js.py).
Usage : python3 generateur/theorie_img.py  ->  theorie/c<n>[-ar].svg et theorie/formes[-ar].svg"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from xml.sax.saxutils import escape
import scratch_art as art
from jeux2 import nest
from activites_img import Canvas, b, R, F, IF, IFE, COL, FONT
from theorie_core import P

OUT = os.path.join(ROOT, "theorie"); os.makedirs(OUT, exist_ok=True)
INK, SOFT, LINE = "#1e3a6e", "#eef3fb", "#c4d3f0"


def T(x, y, s, size=16, fill=INK, weight="700", anchor="start", extra=""):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" unicode-bidi="plaintext" {extra}>{escape(s)}</text>'
def rr(x, y, w, h, r=8, fill="#fff", stroke=None, sw=1.5, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}"{st} {extra}/>'
def circ(x, y, r, fill, stroke=None, sw=1.5):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}"{st}/>'
def line(x1, y1, x2, y2, stroke="#999", sw=2, dash=None, marker=False):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#{MARKS.get(stroke, "ah")})"' if marker else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{d}{m}/>'
MARKS = {"#e8861c": "ah", "#2e9e5b": "ahg", "#c0392b": "ahr"}
DEFS = "<defs>" + "".join(f'<marker id="{i}" markerUnits="userSpaceOnUse" markerWidth="16" markerHeight="16" refX="12" refY="8" orient="auto"><path d="M0,1 L16,8 L0,15 z" fill="{c}"/></marker>' for c, i in MARKS.items()) + "</defs>"
def sprite(kind, key, x, y, w, rot=0, flip=False):
    svg = art.art_svg(kind, key); sw, sh = art.svg_size(svg); h = w * sh / sw
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({-1 if flip else 1},1)">' + nest(svg, -w / 2, -h / 2, w, h) + "</g>"
def canvas_g(c, x, y, s=1.0): return f'<g transform="translate({x},{y}) scale({s})">' + "".join(c.s) + "</g>"
def tag(cx, cy, s, fill, size=17):
    w = len(s) * size * 0.58 + 30
    return rr(cx - w / 2, cy - 15, w, 30, 15, fill) + T(cx, cy + 6, s, size, "#fff", "700", "middle")
def page(body, bg="#fff", w=480, h=360):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}<rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>'
def L(lang, fr, ar): return ar if lang == "ar" else fr


# ----------------------------------------------------------------------------- couvertures
def c1(lang):
    s = rr(26, 40, 188, 250, 14, "#fff", "#b9d8c3", 2) + rr(26, 40, 188, 34, 14, "#2e9e5b") + rr(26, 60, 188, 14, 0, "#2e9e5b")
    for k, wd in enumerate((120, 96, 112, 84)):
        y = 92 + k * 48
        s += circ(56, y + 15, 14, "#2e9e5b") + T(56, y + 21, str(k + 1), 16, "#fff", "700", "middle") + rr(80, y + 6, wd, 18, 9, "#d6ebdc")
    s += T(120, 62, L(lang, "Étapes", "المراحل"), 17, "#fff", "700", "middle")
    s += line(222, 165, 250, 165, "#e8861c", 5, marker=True)
    ox, oy, n, cs = 262, 52, 4, 48
    s += rr(ox - 6, oy - 6, n * cs + 12, n * cs + 12, 10, "#fff", "#b9d8c3", 2)
    for i in range(n + 1): s += line(ox, oy + i * cs, ox + n * cs, oy + i * cs, "#cfe5d6", 1.5) + line(ox + i * cs, oy, ox + i * cs, oy + n * cs, "#cfe5d6", 1.5)
    pts = [(0, 3), (0, 1), (2, 1), (2, 0)]                     # colonne, ligne depuis le haut
    path = " ".join(f"{ox + c * cs + cs / 2:.0f},{oy + r * cs + cs / 2:.0f}" for c, r in pts)
    s += f'<polyline points="{path}" fill="none" stroke="#e8861c" stroke-width="6" stroke-dasharray="10 7" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#ah)"/>'
    c0, r0 = pts[0]; x0, y0 = ox + c0 * cs + cs / 2, oy + r0 * cs + cs / 2
    s += rr(x0 - 16, y0 - 15, 32, 30, 8, "#4C97FF", "#3373CC") + circ(x0 - 6, y0 - 3, 4, "#fff") + circ(x0 + 6, y0 - 3, 4, "#fff") + rr(x0 - 8, y0 + 6, 16, 4, 2, "#fff")
    s += T(ox + 2 * cs + cs / 2, oy + cs / 2 + 9, "★", 26, "#f2b705", "700", "middle")
    s += tag(240, 326, L(lang, "Algorithme → programme", "خوارزمية ← برنامج"), "#2e9e5b")
    return page(s, "#eaf7ee")


def iface_inner(lang, numbers=True, inline=False):
    """schéma de l'écran de Scratch (960 x 600) ; chaque zone est un groupe .zone (cliquable dans la page)"""
    def X(fr, ar): return P(fr, ar) if inline else L(lang, fr, ar)      # inline : texte arabe de la page (retraduit par le dictionnaire de la page) ; sinon image dans la langue demandée
    zones = {}
    def z(i, x, y, w, h, inner): zones[i] = (x, y, w, h, inner)
    # 1 barre de menus
    inner = rr(0, 0, 960, 44, 0, "#855CD6")
    inner += circ(34, 22, 13, "none", "#fff", 2.2) + f'<ellipse cx="34" cy="22" rx="5.5" ry="13" fill="none" stroke="#fff" stroke-width="2"/>' + line(21, 22, 47, 22, "#fff", 2)
    for k, (fr, ar) in enumerate((("Fichier", "ملف"), ("Édition", "تعديل"), ("Tutoriels", "دروس"))): inner += T(78 + k * 96, 28, X(fr, ar), 16, "#fff", "700")
    inner += rr(700, 9, 250, 26, 6, "#6f45c4") + T(825, 28, X("Mon projet Scratch", "مشروعي في سكراتش"), 14, "#fff", "700", "middle")
    z(1, 0, 0, 960, 44, inner)
    # 2 onglets
    inner = rr(0, 48, 620, 36, 0, "#e6efff")
    for k, (fr, ar, on) in enumerate((("Code", "الأكواد", True), ("Costumes", "الأزياء", False), ("Sons", "الأصوات", False))):
        x = 6 + k * 150
        inner += rr(x, 50, 144, 34, 8, "#fff" if on else "#cfe0ff", "#4C97FF" if on else None, 2) + T(x + 72, 73, X(fr, ar), 16, "#4C97FF" if on else "#5a6a85", "700", "middle")
    z(2, 0, 48, 620, 36, inner)
    # 3 palette de blocs (colonne des familles + blocs)
    inner = rr(0, 88, 290, 512, 0, "#f6f8fc", "#d6e0f0", 1.5)
    for k, col in enumerate(("#4C97FF", "#9966FF", "#CF63CF", "#FFBF00", "#FFAB19", "#5CB1D6", "#59C059", "#FF8C1A", "#FF6680")):
        inner += circ(32, 116 + k * 52, 15, col)
    for k, (cat, fr, ar) in enumerate((("mv", "avancer de 10 pas", "تحرك 10 خطوات"), ("mv", "tourner ↻ de 15 degrés", "استدر يمينا 15 درجة"), ("mv", "aller à x : 0 y : 0", "اذهب إلى س: 0 ص: 0"), ("mv", "ajouter 10 à x", "غيّر س بمقدار 10"), ("mv", "mettre x à 0", "اجعل س = 0"))):
        fill, stroke = COL[cat]; t = X(fr, ar); y = 112 + k * 58
        inner += rr(70, y, 208, 38, 6, fill, stroke, 1.5) + T(82, y + 25, t, 14, "#fff", "700")
    z(3, 0, 88, 290, 512, inner)
    # 4 zone des scripts
    inner = rr(294, 88, 326, 512, 0, "#fff", "#d6e0f0", 1.5)
    for gx in range(310, 620, 28):
        for gy in range(104, 600, 28): inner += circ(gx, gy, 1.2, "#e1e8f3")
    fill, stroke = COL["ev"]; t = X("quand le drapeau vert est cliqué", "عند النقر على العلم الأخضر")
    inner += f'<path d="M320,168 Q352,142 392,164 Q456,184 530,164 L530,204 L320,204 Z" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>' + T(334, 196, t, 14, "#fff", "700")
    fill, stroke = COL["mv"]; t = X("avancer de 10 pas", "تحرك 10 خطوات")
    inner += rr(320, 204, 210, 38, 6, fill, stroke, 1.5) + T(334, 229, t, 14, "#fff", "700")
    fill, stroke = COL["lk"]; t = X("dire Bonjour ! pendant 2 secondes", "قل مرحبا! لمدة 2 ثانية")
    inner += rr(320, 242, 270, 38, 6, fill, stroke, 1.5) + T(334, 267, t, 14, "#fff", "700")
    z(4, 294, 88, 326, 512, inner)
    # 5 scène
    inner = rr(632, 88, 328, 246, 0, "#fff", "#4C97FF", 3) + rr(634, 90, 324, 160, 0, "#cfeaff") + rr(634, 250, 324, 82, 0, "#bfe3a6")
    inner += sprite("a", "chat", 790, 226, 96) + sprite("d", "pomme", 888, 270, 34)
    z(5, 632, 88, 328, 246, inner)
    # 6 drapeau vert et stop
    inner = rr(632, 48, 328, 36, 0, "#fff", "#d6e0f0", 1.5)
    inner += '<path d="M862,56 L862,78" stroke="#6a8b3a" stroke-width="3"/><path d="M864,57 Q876,52 888,58 Q900,64 912,58 L912,72 Q900,78 888,72 Q876,66 864,71 Z" fill="#4CBF56" stroke="#2f8f3a" stroke-width="2"/>'
    inner += '<path d="M928,56 L942,56 L950,64 L950,76 L942,84 L928,84 L920,76 L920,64 Z" transform="translate(0,-6)" fill="#EC5959" stroke="#b83a3a" stroke-width="2"/>'
    z(6, 632, 48, 328, 36, inner)
    # 7 liste des lutins
    inner = rr(632, 340, 248, 260, 0, "#f6f8fc", "#d6e0f0", 1.5) + T(646, 364, X("Lutin", "اللاعب"), 15, INK, "700")
    for k, (kind, key) in enumerate((("a", "chat"), ("d", "pomme"))):
        x = 646 + k * 108
        inner += rr(x, 376, 96, 96, 8, "#fff", "#4C97FF" if k == 0 else "#c4d3f0", 3 if k == 0 else 1.5) + sprite(kind, key, x + 48, 424, 64 if k == 0 else 46)
    z(7, 632, 340, 248, 260, inner)
    # 8 arrière-plan
    inner = rr(886, 340, 74, 260, 0, "#f6f8fc", "#d6e0f0", 1.5) + T(923, 364, X("Scène", "المنصة"), 14, INK, "700", "middle")
    inner += rr(896, 376, 54, 42, 6, "#cfeaff", "#4C97FF", 2) + rr(896, 400, 54, 18, 0, "#bfe3a6") + T(923, 444, X("Arrière-plans", "الخلفيات"), 11, "#5a6a85", "700", "middle")
    z(8, 886, 340, 74, 260, inner)
    out = ""
    for i in range(1, 9):
        x, y, w, h, inner = zones[i]
        bx, by = {1: (x + w - 18, y + h / 2), 2: (x + w - 18, y + h / 2), 3: (x + 16, y + h - 18), 6: (x + 18, y + h / 2), 7: (x + w - 18, y + h - 18), 8: (x + w / 2, y + h - 18)}.get(i, (x + 16, y + 16))
        badge = (circ(bx, by, 14, "#e23b3b", "#fff", 2) + T(bx, by + 6, str(i), 16, "#fff", "800", "middle")) if numbers else ""
        out += f'<g class="zone" data-z="{i}">{inner}<rect class="hl" opacity="0" x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#e8861c" stroke-width="5" rx="4"/><rect class="hit" x="{x}" y="{y}" width="{w}" height="{h}" fill="transparent"/>{badge}</g>'
    return out


def iface_svg(lang="ar"):
    """schéma intégré à la page (viewBox 960 x 600)"""
    return f'<svg class="ifsvg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 600" role="img">{DEFS}<rect width="960" height="600" fill="#e9eef5"/>{iface_inner("ar", inline=True)}</svg>'


def c2(lang):
    return page(f'<g transform="translate(14,22) scale(.4625)">{iface_inner(lang)}</g>' + tag(240, 340, L(lang, "L'écran de Scratch", "شاشة سكراتش"), "#6a4fc7"), "#efeaff")


def c3(lang):
    s = ""
    cv = Canvas(lang); cv.stack(0, [b("flag"), b("move"), b("say"), R(10, [b("costume")])])
    s += canvas_g(cv, 14, 40, 0.93)
    cols = ["#4C97FF", "#9966FF", "#CF63CF", "#FFBF00", "#FFAB19", "#5CB1D6", "#59C059", "#FF8C1A", "#FF6680"]
    names = (("Mouvement", "الحركة"), ("Apparence", "المظهر"), ("Son", "الصوت"), ("Événements", "الأحداث"), ("Contrôle", "التحكم"), ("Capteurs", "الاستشعار"), ("Opérateurs", "العمليات"), ("Variables", "المتغيرات"), ("Mes blocs", "كتلي"))
    for k, col in enumerate(cols):
        y = 34 + k * 31
        s += rr(338, y, 128, 25, 12, col) + T(402, y + 18, L(lang, *names[k]), 13, "#fff", "700", "middle")
    s += tag(150, 326, L(lang, "9 familles de blocs", "9 فئات من الكتل"), "#9966FF")
    return page(s, "#f3edff")


def c4(lang):
    cv = Canvas(lang); cv.stack(0, [b("flag"), b("move", "avancer de 100 pas", "تحرك 100 خطوة"), b("turnr", "tourner ↻ de 90 degrés", "استدر يمينا 90 درجة"), b("say", "dire Arrivé ! pendant 2 secondes", "قل وصلت! لمدة 2 ثانية")])
    s = canvas_g(cv, 12, 34, 0.8)
    s += rr(262, 32, 206, 250, 12, "#fff", "#e6d9a8", 2)
    s += rr(264, 34, 202, 150, 10, "#cfeaff") + rr(264, 184, 202, 96, 0, "#bfe3a6")
    s += line(306, 120, 410, 120, "#e8861c", 4, "9 7", True) + line(410, 120, 410, 206, "#e8861c", 4, "9 7", True)
    s += sprite("a", "chat", 296, 118, 54)
    for k, (x, y) in enumerate(((310, 146), (410, 150), (430, 214))):
        s += circ(x, y, 13, "#e8a21c", "#fff", 2) + T(x, y + 6, str(k + 1), 16, "#fff", "800", "middle")
    s += tag(240, 326, L(lang, "Un événement, puis des blocs dans l'ordre", "حدث ثم كتل بالترتيب"), "#e8a21c", 15)
    return page(s, "#fff7e0")


def c5(lang):
    ox, oy = 240, 170
    s = rr(40, 20, 400, 300, 0, "#fff", "#4C97FF", 3)
    for k in range(-3, 4):
        s += line(ox + k * 60 + 0, 20, ox + k * 60 + 0, 320, "#dbe7fb", 1.5) if abs(k * 60) < 200 else ""
    for k in range(-2, 3): s += line(40, oy + k * 60, 440, oy + k * 60, "#dbe7fb", 1.5)
    s += line(40, oy, 440, oy, "#4C97FF", 3) + line(ox, 20, ox, 320, "#4C97FF", 3)
    s += T(432, oy - 8, "x", 18, "#4C97FF", "800", "end") + T(ox + 10, 40, "y", 18, "#4C97FF", "800")
    cx, cy = ox - 100, oy - 60
    s += line(cx, cy, cx, oy, "#e8861c", 3, "7 6") + line(cx, cy, ox, cy, "#e8861c", 3, "7 6")
    s += sprite("a", "chat", cx, cy - 6, 84)
    s += circ(cx, cy, 6, "#e23b3b", "#fff", 2) + rr(cx - 62, cy + 24, 124, 30, 15, "#e8861c") + T(cx, cy + 45, "(-100, 60)", 17, "#fff", "800", "middle", 'direction="ltr"')
    s += circ(ox, oy, 6, "#1e3a6e") + T(ox + 10, oy + 22, "(0, 0)", 15, INK, "800", "start", 'direction="ltr"')
    s += tag(240, 342, L(lang, "x et y : la position du lutin", "س وص: مكان اللاعب"), "#4C97FF", 15)
    return page(s, "#eaf2ff", h=360)


def c6(lang):
    cv = Canvas(lang); cv.stack(0, [b("flag"), b("pendown"), R(4, [b("move", "avancer de 100 pas", "تحرك 100 خطوة"), b("turnr", "tourner ↻ de 90 degrés", "استدر يمينا 90 درجة")])])
    s = canvas_g(cv, 14, 34, 0.95)
    x0, y0, sd = 290, 100, 110
    s += f'<polygon points="{x0},{y0} {x0 + sd},{y0} {x0 + sd},{y0 + sd} {x0},{y0 + sd}" fill="#fff4e3" stroke="#e8861c" stroke-width="6" stroke-linejoin="round"/>'
    s += line(x0 + 6, y0 - 14, x0 + 90, y0 - 14, "#c0392b", 3, None, True) + line(x0 + sd + 14, y0 + 6, x0 + sd + 14, y0 + 90, "#c0392b", 3, None, True) + line(x0 + sd - 6, y0 + sd + 14, x0 + 16, y0 + sd + 14, "#c0392b", 3, None, True) + line(x0 - 14, y0 + sd - 6, x0 - 14, y0 + 16, "#c0392b", 3, None, True)
    s += sprite("a", "chat", x0 + 20, y0 - 8, 46)
    s += T(x0 + sd / 2, y0 + sd / 2 + 12, "4×", 38, "#e8861c", "800", "middle")
    s += tag(240, 326, L(lang, "Répéter 4 fois : un carré", "كرّر 4 مرات: مربع"), "#e8861c")
    return page(s, "#fff1e0")


def c7(lang):
    s = ""
    w = 190
    s += f'<polygon points="{240 - w / 2 + 14},44 {240 + w / 2 - 14},44 {240 + w / 2},70 {240 + w / 2 - 14},96 {240 - w / 2 + 14},96 {240 - w / 2},70" fill="{COL["se"][0]}" stroke="{COL["se"][1]}" stroke-width="2"/>'
    s += T(240, 76, L(lang, "touche la pomme ?", "هل تلمس التفاحة؟"), 16, "#fff", "700", "middle")
    s += line(190, 96, 112, 160, "#2e9e5b", 4, None, True) + line(290, 96, 368, 160, "#c0392b", 4, None, True)
    s += tag(130, 134, L(lang, "vrai", "صحيح"), "#2e9e5b", 15) + tag(350, 134, L(lang, "faux", "خطأ"), "#c0392b", 15)
    for cx, col, txt, bg in ((112, "#2e9e5b", L(lang, "Miam !", "لذيذ!"), "#e4f6e8"), (368, "#c0392b", L(lang, "Je cherche…", "أبحث…"), "#fde8e5")):
        s += rr(cx - 88, 166, 176, 142, 14, bg, col, 2.5)
        s += sprite("a", "chat", cx - 20 if cx < 240 else cx - 28, 252, 74) + sprite("d", "pomme", cx + 54 if cx < 240 else cx + 58, 276 if cx < 240 else 276, 30)
        wb = len(txt) * 9.5 + 26
        s += rr(cx - wb / 2, 176, wb, 30, 13, "#fff", "#9aa3b2", 2) + T(cx, 197, txt, 15, "#333", "700", "middle")
    s += tag(240, 336, L(lang, "Une condition : vrai ou faux", "الشرط: صحيح أو خطأ"), "#2a9fc9")
    return page(s, "#e9f6fb")


def formes(lang):
    A = lang == "ar"
    rows = [("ev", "chapeau", "كتلة البداية", "commence un script", "تبدأ السكربت"), ("mv", "empilable", "كتلة قابلة للتراص", "fait une action", "تنفّذ فعلا"), ("ct", "bloc en C", "كتلة على شكل C", "contient d'autres blocs", "تحتوي كتلا أخرى"),
            ("se", "hexagone", "السداسي", "vrai ou faux", "جوابه صحيح أو خطأ"), ("op", "arrondi", "المستدير", "donne une valeur", "يعطي قيمة")]
    s = ""
    for k, (cat, fr, ar, rfr, rar) in enumerate(rows):
        y = 14 + k * 62; fill, stroke = COL[cat]
        gx = 352 if A else 18                                  # forme : à droite en arabe, à gauche en français
        if cat == "ev": g = f'<path d="M0,12 Q24,-8 54,8 Q84,16 104,6 L104,44 L0,44 Z" transform="translate({gx},{y})" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        elif cat == "mv": g = rr(gx, y + 4, 104, 40, 5, fill, stroke, 2) + rr(gx + 14, y + 44, 26, 6, 2, fill, stroke, 1.5)
        elif cat == "ct": g = rr(gx, y, 104, 18, 4, fill, stroke, 2) + rr(gx, y + 18, 18, 28, 0, fill, stroke, 2) + rr(gx, y + 44, 104, 14, 4, fill, stroke, 2)
        elif cat == "se": g = f'<polygon points="{gx + 14},{y + 6} {gx + 90},{y + 6} {gx + 104},{y + 26} {gx + 90},{y + 46} {gx + 14},{y + 46} {gx},{y + 26}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        else: g = rr(gx, y + 8, 104, 36, 18, fill, stroke, 2)
        tx = 334 if A else 140
        s += g + T(tx, y + 24, ar if A else fr, 18, INK, "800", "end" if A else "start") + T(tx, y + 46, rar if A else rfr, 15, "#51607a", "600", "end" if A else "start")
        if k < 4: s += line(10, y + 60, 470, y + 60, "#e3eaf6", 1.5)
    return page(s, "#fff", h=330)


COVERS = {1: c1, 2: c2, 3: c3, 4: c4, 5: c5, 6: c6, 7: c7}
def render_all():
    n = 0
    for k, fn in COVERS.items():
        for lang in ("fr", "ar"):
            open(os.path.join(OUT, f"c{k}{'' if lang == 'fr' else '-ar'}.svg"), "w", encoding="utf-8").write(fn(lang)); n += 1
    for lang in ("fr", "ar"):
        open(os.path.join(OUT, f"formes{'' if lang == 'fr' else '-ar'}.svg"), "w", encoding="utf-8").write(formes(lang)); n += 1
    return n
if __name__ == "__main__": print(render_all(), "images")
