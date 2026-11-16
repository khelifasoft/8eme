import re, json, os
ST = '#333333'
def inner(path):
    s = open(path, encoding='utf-8').read()
    return re.sub(r'^<svg[^>]*>|</svg>\s*$', '', s.strip())
def viewbox(path):
    m = re.search(r'viewBox="0 0 (\d+) (\d+)"', open(path, encoding='utf-8').read()); return int(m[1]), int(m[2])
def place(path, cx, cy, scale=1.0):
    """Lutin centré en (cx, cy) de la scène (coordonnées SVG 480x360)."""
    w, h = viewbox(path); W, H = w * scale, h * scale
    return f'<svg x="{cx - W / 2:.1f}" y="{cy - H / 2:.1f}" width="{W:.1f}" height="{H:.1f}" viewBox="0 0 {w} {h}">{inner(path)}</svg>'
def monitor(label, val, x=4, y=4, w=118):
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="22" rx="4" fill="#e6f0ff" stroke="#c4d3f0"/><text x="{x + 6}" y="{y + 16}" font-family="Tajawal,Arial,sans-serif" font-size="13" fill="#575e75" font-weight="bold">{label}</text>'
            f'<rect x="{x + w - 38}" y="{y + 3}" width="34" height="16" rx="3" fill="#ff8c1a"/><text x="{x + w - 21}" y="{y + 16}" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#fff">{val}</text></g>')
def arrow(x1, y1, x2, y2): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#e8861c" stroke-width="5" stroke-dasharray="9 6" marker-end="url(#ah)"/>'
def pill(x, y, text, w=None):
    w = w or max(60, int(len(text) * 8.2 + 26))
    return f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="14" fill="#e8861c"/><text x="{x + w / 2}" y="{y + 19}" text-anchor="middle" font-family="Tajawal,Arial,sans-serif" font-size="15" font-weight="bold" fill="#fff">{text}</text>'
def scene(*layers):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360"><defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#e8861c"/></marker></defs>'
            + ''.join(layers) + '</svg>')
def bg(path): return f'<svg x="0" y="0" width="480" height="360" viewBox="0 0 480 360">{inner(path)}</svg>'
def T(c, k, d, fr, ar, cond=None, pre=None, post=None):
    t = {'c': c, 'k': k, 'd': d, 't': {'ar': ar, 'fr': fr}}
    if cond: t['pre'] = {'ar': pre[0], 'fr': pre[1]}; t['cond'] = {'ar': cond[0], 'fr': cond[1]}; t['post'] = {'ar': post[0], 'fr': post[1]} if post else None
    if not cond: pass
    return t
IF = lambda d, fr, ar: T('ct', 'if', d, '', '', (ar, fr), ('إذا', 'si'), ('فإن', 'alors'))
UNTIL = lambda d, fr, ar: T('ct', 'until', d, '', '', (ar, fr), ('كرّر حتى', "répéter jusqu'à ce que"), None)
