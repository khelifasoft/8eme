"""Jeu « Remets les scènes dans l'ordre » : un jeu par conte (jeux/jeu_ordre_<conte>.sb3).
Usage : python3 generateur/jeux3.py jeux"""
import sys, os, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import jeux2 as J, scratch as sc, scratch_art as art, i18n_fr
from jeux2 import B, Proj, card, nest, bg_svg, wrap
from xml.sax.saxutils import escape
OUT = sys.argv[1] if len(sys.argv) > 1 else "jeux"
J.OUT = OUT
RND = random.Random(23)

def scene_state(key, upto):
    d = sc.D[key]; vis = set(); pos = {}; cos = {}
    for si in range(upto + 1):
        for st in d["scenes"][si][1]:
            op, spr = st[0], st[1]
            if op == "show": vis.add(spr); pos[spr] = (st[2], st[3])
            elif op == "hide": vis.discard(spr)
            elif op in ("goto", "glide"): pos[spr] = (st[2], st[3])
            elif op == "costume": cos[spr] = st[2]
    return vis, pos, cos

def scene_svg(key, i):
    """image 480x360 de la scène i : fond + personnages visibles à la fin de la scène"""
    d = sc.D[key]; bd = d["scenes"][i][0]
    back = art.art_svg("l", art.BACK[key][d["backdrops"][bd][0]])
    inner = nest(back, 0, 0, 480, 360)
    vis, pos, cos = scene_state(key, i)
    for spr in [s[0] for s in d["sprites"]]:
        if spr not in vis or spr not in art.ART[key]: continue
        kind, ak, size, flip, alts = art.ART[key][spr]
        c = cos.get(spr)
        if c and c in alts: kind, ak = alts[c]
        svg = art.art_svg(kind, ak, art.TINT.get((key, spr))); w, h = art.svg_size(svg)
        W, H = w * size / 100, h * size / 100; x, y = pos[spr]
        inner += nest(svg, 240 + x - W / 2, 180 - y - H / 2, W, H)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">{inner}</svg>'

def caption(key, i):
    for st in sc.D[key]["scenes"][i][1]:
        if st[0] == "say": return st[2]
    return ""

def scene_card(key, i, badge=None):
    W, H = 156, 148
    body = f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="12" fill="#ffffff" stroke="#1f4aa8" stroke-width="4"/>'
    body += f'<clipPath id="c"><rect x="6" y="6" width="{W-12}" height="106" rx="8"/></clipPath><g clip-path="url(#c)">' + nest(scene_svg(key, i), 6, 6, W - 12, 106) + '</g>'
    lines = wrap(caption(key, i), 24)[:2]
    for k, l in enumerate(lines):
        body += f'<text x="{W/2}" y="{124 + k*13}" text-anchor="middle" font-family="Sans Serif" font-size="11.5" font-weight="bold" fill="#1d2433">{escape(l)}</text>'
    if badge:
        body = body.replace('stroke="#1f4aa8"', 'stroke="#2e9e5b"', 1)
        body += f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="12" fill="#ffffff" fill-opacity="0.45"/>'
        body += f'<circle cx="26" cy="28" r="20" fill="#2e9e5b" stroke="#fff" stroke-width="4"/><text x="26" y="37" text-anchor="middle" font-family="Sans Serif" font-size="26" font-weight="bold" fill="#fff">{badge}</text>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg>'

def order_game(key):
    n = len(sc.D[key]["scenes"]); title = sc.STORIES[key]["title"]
    P = Proj("ordre_" + key); sb = P.stage
    P.stage_costumes.append(P.costume("fond", bg_svg("#fff7e6", "#ffe6b8"), 240, 180))
    nxt, ni = P.V("التالي"); mis, mi = P.V("الأخطاء")
    ding, bad = P.sfx("ding"), P.sfx("echec")
    order = list(range(n))
    while order == sorted(order): RND.shuffle(order)
    for hatname in ("flag", "إعادة"):
        hat = sb.hat_flag() if hatname == "flag" else P.hat(sb, "إعادة")
        sb.script(hat, sb.setv(nxt, ni, 1), sb.setv(mis, mi, 0), P.bc(sb, "عرض"), y=0 if hatname == "flag" else 200)
    pos = [(-160, 70), (0, 70), (160, 70), (-160, -80), (0, -80), (160, -80)]
    for slot in range(n):
        i = order[slot]; ci = i + 1; b = B(); lc, lci = "ترتيب", f"lv_o{slot}"; lp, lpi = "وُضعت", f"lv_p{slot}"
        cos = [P.costume("عادية", scene_card(key, i))] + [P.costume(f"رقم {k}", scene_card(key, i, k)) for k in range(1, n + 1)]
        def first_costume(): return b.add("looks_switchcostumeto", inputs={"COSTUME": [1, b.add("looks_costume", fields={"COSTUME": ["عادية", None]}, shadow=True)]})
        b.script(P.hat(b, "عرض"), b.setv(lp, lpi, 0), first_costume(), b.show(), y=0)
        right = [b.setv(lp, lpi, 1), b.play(ding["name"]), b.costume_n(b.add_(b.R(b.var(nxt, ni)), b.N(1))), b.chg(nxt, ni, 1),
                 b.if_(b.gt(b.R(b.var(nxt, ni)), b.N(n)), P.bc(b, "فوز"))]
        wrong = [b.play(bad["name"]), b.chg(mis, mi, 1), b.sayfor(b.S("ليس بعد!"), 0.9)]
        b.script(b.when_clicked(), b.if_(b.eq(b.R(b.var(lp, lpi)), b.N(0)), b.ifelse(b.eq(b.R(b.var(nxt, ni)), b.N(ci)), right, wrong)), y=200)
        P.sprite(f"مشهد {slot+1}", b, cos, [ding, bad], x=pos[slot][0], y=pos[slot][1], visible=True, local_vars=[(lc, lci, ci), (lp, lpi, 0)])
    ib = B()
    P.sprite("التعليمات", ib, [P.costume("تعليمات", card(450, 34, wrap(f"رتّب مشاهد قصة «{title}» بالضغط عليها بالترتيب الصحيح", 60)[:1], "#e8f0ff", size=15, stroke="#1f4aa8"))], x=0, y=160, visible=True)
    eb = B()
    eb.script(P.hat(eb, "فوز"), eb.wait(0.5), eb.show(), eb.say_(eb.join(eb.S("أحسنت! رتّبت القصة. عدد الأخطاء: "), eb.join(eb.RS(eb.var(mis, mi)), eb.S("  (اضغط للإعادة)")))), y=0)
    eb.script(P.hat(eb, "عرض"), eb.hide(), eb.say_(eb.S("")), y=160)
    eb.script(eb.when_clicked(), P.bc(eb, "إعادة"), y=320)
    P.sprite("الفوز", eb, [P.costume("فوز", card(300, 70, ["أحسنت! القصة مرتبة"], "#fff3c4", size=24, stroke="#e8861c"))], x=0, y=0)
    P.monitor("الأخطاء", 5); P.monitor("التالي", 32, False)
    P.finish(art.MUSIC.get(key, "joyeuse"))
    return order

def cover(key, order, path):
    body = '<rect width="480" height="270" fill="#fff1d6"/>'
    for slot, i in enumerate(order):
        body += nest(scene_card(key, i), 8 + (slot % 3) * 158, 6 + (slot // 3) * 128, 152, 124)
    open(path, "w", encoding="utf-8").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="270" viewBox="0 0 480 270">{body}</svg>')

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); cov = os.path.join(OUT, "couvertures"); os.makedirs(cov, exist_ok=True)
    meta = []
    for key in sc.D:
        order = order_game(key); cover(key, order, os.path.join(cov, f"ordre_{key}.svg"))
        tfr = i18n_fr.STORIES_FR[key][0]
        meta.append(dict(key="ordre_" + key, file=f"jeux/jeu_ordre_{key}.sb3", title_ar=f"رتّب مشاهد: {sc.STORIES[key]['title']}", title_fr=f"Remets les scènes dans l'ordre : {tfr}",
                         how_ar="اضغط على المشاهد بالترتيب الذي حدثت به الأحداث، من البداية إلى النهاية.", how_fr="Clique sur les scènes dans l'ordre où les événements se sont passés, du début à la fin.",
                         cover=f"jeux/couvertures/ordre_{key}.svg", cat="order", cat_ar="ترتيب مشاهد القصص", cat_fr="Remettre les scènes dans l'ordre"))
    json.dump(meta, open(os.path.join(HERE, "jeux3_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("jeux d'ordre :", len(meta))
