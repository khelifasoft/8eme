"""Images du « cahier de l'élève » (fiches à coller dans le cahier) :
scripts Scratch à moitié terminés (blocs manquants, nombres et conditions à écrire), schéma de l'écran de Scratch à légender,
grille du robot et plan à coordonnées. Tout est dessiné en SVG ; les fonctions renvoient des chaînes SVG prêtes à être insérées dans la page.
mask(items, g=, over=, cnt=, cond=) : copie d'un script (même description que activites_specs.py) où l'on masque
  g    = numéros de blocs (dans l'ordre de lecture) remplacés par un bloc vide en pointillés,
  over = {numéro de bloc : (français, arabe)} nouveau texte du bloc (par exemple « avancer de ……… pas »),
  cnt  = {numéro de boucle « répéter » : texte du nombre de tours},
  cond = {numéro de condition : (français, arabe)} nouvelle condition."""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from xml.sax.saxutils import escape
from activites_img import Canvas, b, R, F, IF, IFE, UNTIL, WU, LBL, COL, FONT, LANGIDX
from activites_data1 import BLOCKS
import theorie_img as TI
import scratch_art as art
from jeux2 import nest

DOTS = "………"


class GapCanvas(Canvas):
    """comme Canvas, avec un bloc « vide » (clé « gap ») dessiné en pointillés"""
    def block(self, x, key, fr, ar, width=None):
        if key == "gap":
            w, h = 176, 30
            self.s.append(f'<rect x="{x}" y="{self.y}" width="{w}" height="{h}" rx="4" fill="#fff" stroke="#7b8598" stroke-width="2" stroke-dasharray="7 5"/>')
            self.txt(x + 14, self.y + 21, DOTS * 2, fill="#7b8598", size=15)
            self.y += h; self.maxw = max(self.maxw, x + w); return
        super().block(x, key, fr, ar, width)


def script_svg(scripts, lang):
    """équivalent de activites_img.script_svg, avec les blocs vides"""
    c = GapCanvas(lang)
    flat, cur = [], []
    for it in scripts:
        if isinstance(it, list):
            if cur: flat.append(cur); cur = []
            flat.append(it)
        else: cur.append(it)
    if cur: flat.append(cur)
    for sc in flat:
        c.stack(0, sc); c.y += 22
    c.y -= 22
    return c.svg()


def mask(items, g=(), over=None, cnt=None, cond=None):
    over, cnt, cond = over or {}, cnt or {}, cond or {}
    ctr = dict(b=0, r=0, c=0)
    def nxt(k): i = ctr[k]; ctr[k] += 1; return i
    def walk(lst):
        out = []
        for it in lst:
            if isinstance(it, list): out.append(walk(it)); continue
            k = it[0]
            if k == "B":
                i = nxt("b")
                if i in g: out.append(("B", "gap", None, None))
                elif i in over: out.append(("B", it[1], over[i][0], over[i][1]))
                else: out.append(it)
            elif k == "F": out.append(("F", walk(it[1])))
            elif k == "R": i = nxt("r"); out.append(("R", cnt.get(i, it[1]), walk(it[2])))
            elif k in ("IF", "U"): i = nxt("c"); out.append((k, cond.get(i, it[1]), walk(it[2])))
            elif k == "IFE": i = nxt("c"); out.append(("IFE", cond.get(i, it[1]), walk(it[2]), walk(it[3])))
            elif k == "WU": i = nxt("c"); out.append(("WU", cond.get(i, it[1])))
            else: out.append(it)
        return out
    return walk(items)


def block_text(key, lang):
    """texte par défaut d'un bloc (pour écrire un texte modifié avec over=)"""
    return BLOCKS[key][1 if lang == "fr" else 2]


# ----------------------------------------------------------------------------- schéma de l'écran de Scratch (à légender)
def iface_static(lang):
    return f'<svg class="figsvg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 600" role="img">{TI.DEFS}<rect width="960" height="600" fill="#e9eef5"/>{TI.iface_inner(lang)}</svg>'


# ----------------------------------------------------------------------------- jeu du robot : grille 5 x 5, départ en bas à gauche, arrivée marquée d'une étoile
def robot_grid(lang, n=5, goal=(2, 3), marks=()):
    cs = 52; S = n * cs
    s = f'<svg class="figsvg" xmlns="http://www.w3.org/2000/svg" viewBox="-6 -6 {S + 12} {S + 30}" role="img"><rect x="-6" y="-6" width="{S + 12}" height="{S + 30}" fill="#fff"/>'
    for i in range(n + 1):
        s += f'<line x1="{i * cs}" y1="0" x2="{i * cs}" y2="{S}" stroke="#9fb5a8" stroke-width="2"/><line x1="0" y1="{i * cs}" x2="{S}" y2="{i * cs}" stroke="#9fb5a8" stroke-width="2"/>'
    def cell(c, r): return c * cs + cs / 2, S - (r * cs + cs / 2)
    gx, gy = cell(*goal)
    s += f'<text x="{gx}" y="{gy + 12}" text-anchor="middle" font-size="34" fill="#e8a21c" stroke="#b07a00" stroke-width="1" font-family="Arial">★</text>'
    for (c, r, lab) in marks:
        x, y = cell(c, r); s += f'<circle cx="{x}" cy="{y}" r="15" fill="#fff6e0" stroke="#e8a21c" stroke-width="2.5"/><text x="{x}" y="{y + 6}" text-anchor="middle" font-size="17" font-weight="800" fill="#8a5a00" font-family="Arial">{lab}</text>'
    x, y = cell(0, 0)
    s += f'<g transform="translate({x},{y})"><rect x="-17" y="-17" width="34" height="34" rx="8" fill="#4C97FF" stroke="#3373CC" stroke-width="2.5"/><circle cx="-6" cy="-3" r="4" fill="#fff"/><circle cx="6" cy="-3" r="4" fill="#fff"/><path d="M-8,-20 L0,-32 L8,-20 Z" fill="#e8861c"/></g>'
    s += f'<text x="{x}" y="{y + 36}" text-anchor="middle" font-size="12" font-weight="700" fill="#1e3a6e" font-family="{FONT}">{escape(TI.L(lang, "départ", "الانطلاق"))}</text>'
    return s + "</svg>"


# ----------------------------------------------------------------------------- plan à coordonnées : points à lire (A, B, C…)
def plane(lang, pts):
    """scène 480 x 360 avec quadrillage de 60 en 60 ; pts = [(lettre, x, y)]"""
    s = '<svg class="figsvg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" role="img"><rect width="480" height="360" fill="#fff" stroke="#4C97FF" stroke-width="3"/>'
    for x in range(0, 481, 60): s += f'<line x1="{x}" y1="0" x2="{x}" y2="360" stroke="#dbe7fb" stroke-width="1.5"/>'
    for y in range(0, 361, 60): s += f'<line x1="0" y1="{y}" x2="480" y2="{y}" stroke="#dbe7fb" stroke-width="1.5"/>'
    s += '<line x1="0" y1="180" x2="480" y2="180" stroke="#4C97FF" stroke-width="3"/><line x1="240" y1="0" x2="240" y2="360" stroke="#4C97FF" stroke-width="3"/>'
    for v in range(-180, 181, 60):
        if v: s += f'<text x="{240 + v}" y="196" text-anchor="middle" font-size="12" fill="#4C6FB5" font-family="Arial">{str(v).replace("-", chr(0x2212))}</text>'
    for v in range(-120, 121, 60):
        if v: s += f'<text x="246" y="{184 - v}" font-size="12" fill="#4C6FB5" font-family="Arial">{str(v).replace("-", chr(0x2212))}</text>'
    s += '<text x="470" y="170" text-anchor="end" font-size="15" font-weight="800" fill="#4C97FF" font-family="Arial">x</text><text x="250" y="16" font-size="15" font-weight="800" fill="#4C97FF" font-family="Arial">y</text>'
    for (lab, x, y) in pts:
        s += f'<circle cx="{240 + x}" cy="{180 - y}" r="7" fill="#e23b3b" stroke="#fff" stroke-width="2"/><text x="{240 + x + 11}" y="{180 - y - 8}" font-size="19" font-weight="800" fill="#c0392b" font-family="Arial">{lab}</text>'
    return s + "</svg>"
