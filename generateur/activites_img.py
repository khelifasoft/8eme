"""Images des pages détaillées d'activités : scripts Scratch dessinés en SVG (« captures » de blocs) et scènes avant/après.
Usage : python3 generateur/activites_img.py  -> fiches-activite/activites/a<n>-script[-ar].svg, a<n>-avant[-ar].svg, a<n>-apres[-ar].svg"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from xml.sax.saxutils import escape
import scratch_art as art
from activites_data1 import BLOCKS
OUT = os.path.join(ROOT, "fiches-activite", "activites"); os.makedirs(OUT, exist_ok=True)
COL = {"ev": ("#FFBF00", "#CC9900"), "mv": ("#4C97FF", "#3373CC"), "lk": ("#9966FF", "#774DCB"), "sn": ("#CF63CF", "#BD42BD"), "ct": ("#FFAB19", "#CF8B17"),
       "se": ("#5CB1D6", "#2E8EB8"), "op": ("#59C059", "#389438"), "va": ("#FF8C1A", "#DB6E00"), "pen": ("#0FBD8C", "#0B8E69")}
FONT = "Tajawal,Arial,sans-serif"
LANGIDX = {"fr": 0, "ar": 1}
# mots des blocs en C
CWORD = {"if": (("si", "alors"), ("إذا", "فإن")), "until": (("répéter jusqu'à ce que", ""), ("كرّر حتى", "")), "else": ("sinon", "وإلا")}
CTEXT = {"forever": ("répéter indéfiniment", "كرّر باستمرار"), "repeat": ("répéter {n} fois", "كرّر {n} مرات")}

# ---------- spécification d'un script : listes de blocs ; b("clé"), b("clé", fr, ar), F(corps), R(n, corps), IF(cond, corps), IFE(cond, a, b), UNTIL(cond, corps)
def b(key, fr=None, ar=None): return ("B", key, fr, ar)
def F(body): return ("F", body)
def R(n, body): return ("R", n, body)
def IF(cond, body): return ("IF", cond, body)
def IFE(cond, a, c): return ("IFE", cond, a, c)
def UNTIL(cond, body): return ("U", cond, body)
def WU(cond): return ("WU", cond)

def tw(s, size=13): return sum(size * (0.62 if ord(c) < 0x600 else 0.52) for c in s) + 2
class Canvas:
    def __init__(self, lang): self.i = LANGIDX[lang]; self.lang = lang; self.s = []; self.y = 0; self.maxw = 0
    def txt(self, x, y, t, fill="#fff", size=13, weight="700"):
        self.s.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" unicode-bidi="plaintext">{escape(t)}</text>')
    def hexa(self, x, y, text, cat="op"):
        w = tw(text) + 22; fill, stroke = COL[cat]
        self.s.append(f'<polygon points="{x + 9},{y} {x + w - 9},{y} {x + w},{y + 11} {x + w - 9},{y + 22} {x + 9},{y + 22} {x},{y + 11}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        self.txt(x + 11, y + 16, text); return w
    def block(self, x, key, fr, ar, width=None):
        cat = BLOCKS[key][0]; fill, stroke = COL[cat]; text = (fr or BLOCKS[key][1]) if self.i == 0 else (ar or BLOCKS[key][2])
        w = tw(text) + 26; h = 30
        if cat == "ev":   # chapeau
            self.s.append(f'<path d="M{x},{self.y + 8} Q{x + w * .3},{self.y - 8} {x + w * .55},{self.y + 6} Q{x + w * .75},{self.y + 12} {x + w},{self.y + 6} L{x + w},{self.y + 36} L{x},{self.y + 36} Z" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
            self.txt(x + 12, self.y + 28, text); self.y += 36; self.maxw = max(self.maxw, x + w); return
        self.s.append(f'<rect x="{x}" y="{self.y}" width="{w:.1f}" height="{h}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        self.txt(x + 12, self.y + 20, text); self.y += h; self.maxw = max(self.maxw, x + w)
    def cblock(self, x, head_parts, body_fn, else_body=None, cat="ct"):
        """en-tête (liste de ('t', texte) / ('h', texte)) puis corps ; ferme avec un bas de bloc"""
        fill, stroke = COL[cat]; top = self.y; cx = x + 12; w0 = 24
        for kind, t in head_parts:
            if kind == "t": w0 += tw(t) + 8
            else: w0 += tw(t) + 22 + 8
        self.s.append(f'<rect x="{x}" y="{top}" width="{w0:.1f}" height="32" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'); self.maxw = max(self.maxw, x + w0)
        for kind, t in head_parts:
            if kind == "t": self.txt(cx, top + 21, t); cx += tw(t) + 8
            else: wd = self.hexa(cx, top + 5, t, "op"); cx += wd + 8
        self.y += 32; arm0 = self.y
        body_fn(x + 16); arm1 = self.y
        self.s.append(f'<rect x="{x}" y="{arm0}" width="16" height="{max(arm1 - arm0, 14)}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        if arm1 == arm0: self.y += 14
        if else_body:
            self.s.append(f'<rect x="{x}" y="{self.y}" width="60" height="26" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'); self.txt(x + 10, self.y + 18, CWORD["else"][self.i]); self.y += 26
            a0 = self.y; else_body(x + 16); a1 = self.y
            self.s.append(f'<rect x="{x}" y="{a0}" width="16" height="{max(a1 - a0, 14)}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
            if a1 == a0: self.y += 14
        self.s.append(f'<rect x="{x}" y="{self.y}" width="{min(w0, 120):.1f}" height="16" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'); self.y += 16
    def stack(self, x, items):
        for it in items:
            k = it[0]
            if k == "B": self.block(x, it[1], it[2], it[3])
            elif k == "F": self.cblock(x, [("t", CTEXT["forever"][self.i])], lambda xx, it=it: self.stack(xx, it[1]))
            elif k == "R": self.cblock(x, [("t", CTEXT["repeat"][self.i].format(n=it[1]))], lambda xx, it=it: self.stack(xx, it[2]))
            elif k in ("IF", "IFE"):
                w = CWORD["if"][self.i]; cond = it[1][self.i]
                self.cblock(x, [("t", w[0]), ("h", cond), ("t", w[1])], lambda xx, it=it: self.stack(xx, it[2]), (lambda xx, it=it: self.stack(xx, it[3])) if k == "IFE" else None)
            elif k == "U":
                w = CWORD["until"][self.i]; self.cblock(x, [("t", w[0]), ("h", it[1][self.i])], lambda xx, it=it: self.stack(xx, it[2]))
            elif k == "WU":
                text = ("attendre jusqu'à ce que", "انتظر حتى")[self.i]; fill, stroke = COL["ct"]; w = tw(text) + 24 + tw(it[1][self.i]) + 30
                self.s.append(f'<rect x="{x}" y="{self.y}" width="{w:.1f}" height="32" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'); self.txt(x + 12, self.y + 21, text); self.hexa(x + 18 + tw(text), self.y + 5, it[1][self.i]); self.y += 32; self.maxw = max(self.maxw, x + w)
    def svg(self, pad=12):
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.maxw + pad * 2:.0f}" height="{self.y + pad * 2:.0f}" viewBox="{-pad} {-pad} {self.maxw + pad * 2:.0f} {self.y + pad * 2:.0f}">' + "".join(self.s) + "</svg>"

def script_svg(scripts, lang):
    c = Canvas(lang)
    flat, cur = [], []                      # une liste mixte = blocs consécutifs (un script) + listes (scripts supplémentaires)
    for it in scripts:
        if isinstance(it, list):
            if cur: flat.append(cur); cur = []
            flat.append(it)
        else: cur.append(it)
    if cur: flat.append(cur)
    scripts = flat
    for k, sc in enumerate(scripts):
        c.stack(0, sc); c.y += 22
    c.y -= 22
    return c.svg()

# ---------- scènes : back (clé de lieu ou None), items = [(art, x, y, w, rot, opa, flip)], bubble=(fr, ar, x, y), tags=[(fr, ar, x, y, couleur)], lines=[(d)], hud=[(fr, ar, valeur)]
def S(back, items=(), bubble=None, tags=(), lines=(), hud=(), arrows=()): return dict(back=back, items=list(items), bubble=bubble, tags=list(tags), lines=list(lines), hud=list(hud), arrows=list(arrows))
def I(a, x, y, w=90, rot=0, opa=1.0, flip=False): return (a, x, y, w, rot, opa, flip)
def _inner(svg): return svg
def scene_svg(sp, lang):
    i = LANGIDX[lang]; s = ""
    s += (re.sub(r'^<svg[^>]*>|</svg>$', '', art.art_svg("l", sp["back"])) if False else "")
    from jeux2 import nest
    if sp["back"]: s += nest(art.art_svg("l", sp["back"]), 0, 0, 480, 360)
    else: s += '<rect width="480" height="360" fill="#fff"/><rect x="2" y="2" width="476" height="356" fill="none" stroke="#ddd"/>'
    for ln in sp["lines"]: s += f'<path d="{ln}" fill="none" stroke="#c0392b" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
    for (a, x, y, w, rot, opa, flip) in sp["items"]:
        kind, key = a.split(":"); svg = art.art_svg(kind, key); sw, sh = art.svg_size(svg); h = w * sh / sw
        cx, cy = 240 + x, 180 - y
        g = f'<g transform="translate({cx},{cy}) rotate({rot}) scale({-1 if flip else 1},1)" opacity="{opa}">' + nest(svg, -w / 2, -h / 2, w, h) + "</g>"
        s += g
    for (x1, y1, x2, y2) in sp["arrows"]:
        s += f'<line x1="{240 + x1}" y1="{180 - y1}" x2="{240 + x2}" y2="{180 - y2}" stroke="#e8861c" stroke-width="5" stroke-dasharray="9 6" marker-end="url(#ah)"/>'
    for k, (fr, ar, v) in enumerate(sp["hud"]):
        lab = (fr, ar)[i]; s += f'<rect x="6" y="{6 + 28 * k}" width="130" height="24" rx="5" fill="#e6f0ff" stroke="#c4d3f0"/><text x="12" y="{23 + 28 * k}" font-family="{FONT}" font-size="13" font-weight="700" fill="#575e75">{escape(lab)}</text><rect x="92" y="{9 + 28 * k}" width="40" height="18" rx="3" fill="#ff8c1a"/><text x="112" y="{23 + 28 * k}" text-anchor="middle" font-family="Arial" font-size="13" font-weight="700" fill="#fff">{v}</text>'
    if sp["bubble"]:
        fr, ar, x, y = sp["bubble"]; t = (fr, ar)[i]; w = tw(t, 16) + 26
        s += f'<g><rect x="{240 + x - w / 2}" y="{180 - y - 17}" width="{w}" height="34" rx="14" fill="#fff" stroke="#9aa3b2" stroke-width="2"/><text x="{240 + x}" y="{180 - y + 6}" text-anchor="middle" font-family="{FONT}" font-size="16" font-weight="700" fill="#333">{escape(t)}</text></g>'
    for (fr, ar, x, y, color) in sp["tags"]:
        t = (fr, ar)[i]; w = tw(t, 15) + 24
        s += f'<rect x="{240 + x - w / 2}" y="{180 - y - 14}" width="{w}" height="28" rx="14" fill="{color}"/><text x="{240 + x}" y="{180 - y + 6}" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="700" fill="#fff">{escape(t)}</text>'
    defs = '<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#e8861c"/></marker></defs>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">{defs}{s}</svg>'

def render_all():
    from activites_specs import SPECS
    n = 0
    for num, sp in SPECS.items():
        for lang in ("fr", "ar"):
            suf = "" if lang == "fr" else "-ar"
            open(os.path.join(OUT, f"a{num}-script{suf}.svg"), "w", encoding="utf-8").write(script_svg(sp["script"], lang))
            open(os.path.join(OUT, f"a{num}-avant{suf}.svg"), "w", encoding="utf-8").write(scene_svg(sp["before"], lang))
            open(os.path.join(OUT, f"a{num}-apres{suf}.svg"), "w", encoding="utf-8").write(scene_svg(sp["after"], lang)); n += 3
    return n
if __name__ == "__main__": print(render_all(), "images")
