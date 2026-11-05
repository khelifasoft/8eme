"""Petites fonctions pour dessiner des SVG de style dessin animé."""
OUT = "#333333"
def P(d, fill="none", sw=3, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{OUT}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'
def E(cx, cy, rx, ry, fill, sw=3, rot=0):
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ""
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{OUT}" stroke-width="{sw}"{t}/>'
def C(cx, cy, r, fill, sw=3):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{OUT}" stroke-width="{sw}"/>'
def R(x, y, w, h, fill, rx=0, sw=3):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{OUT}" stroke-width="{sw}"/>'
def T(pts, fill, sw=3):
    s = " ".join(f"{x},{y}" for x, y in pts)
    return f'<polygon points="{s}" fill="{fill}" stroke="{OUT}" stroke-width="{sw}" stroke-linejoin="round"/>'
def L(x1, y1, x2, y2, color=OUT, w=3):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
def LIMB(x1, y1, x2, y2, color, w=16):
    """segment épais avec contour"""
    return L(x1, y1, x2, y2, OUT, w + 6) + L(x1, y1, x2, y2, color, w)
def G(body, tx=0, ty=0, sx=1, sy=None, rot=0, cx=0, cy=0):
    sy = sx if sy is None else sy
    return f'<g transform="translate({tx} {ty}) rotate({rot} {cx} {cy}) scale({sx} {sy})">{body}</g>'
def SVG(w, h, body, bg=None, defs=""):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{defs}{b}{body}</svg>'
def TXT(x, y, s, size=20, fill="#222", anchor="middle", bold=True):
    from xml.sax.saxutils import escape
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Sans Serif" font-size="{size}" font-weight="{"bold" if bold else "normal"}" fill="{fill}">{escape(s)}</text>'
