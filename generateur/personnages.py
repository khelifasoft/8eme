from svgkit import *

SKIN = ["#f4c7a1", "#e8b48a", "#c68a5e", "#9a6a43"]

def _hat(name, col, hair):
    """retourne (derrière, devant) pour un couvre-chef"""
    if name == "turban":
        return "", E(100, 40, 42, 24, col) + P("M62 40 Q100 20 138 40", "none", 3) + P("M70 52 Q100 36 130 52", "none", 3) + C(100, 24, 6, "#e8b923", 2)
    if name == "crown":
        return "", T([(66, 38), (66, 8), (84, 24), (100, 2), (116, 24), (134, 8), (134, 38)], "#f1c40f") + C(100, 10, 4, "#e74c3c", 2)
    if name == "tiara":
        return "", T([(78, 34), (82, 18), (91, 28), (100, 12), (109, 28), (118, 18), (122, 34)], "#f1c40f", 2) + C(100, 20, 3, "#3498db", 1.5)
    if name == "hood":
        back = C(100, 66, 44, col) + P("M62 100 Q100 125 138 100 L158 205 Q100 225 42 205Z", col)
        front = P("M60 66 A40 40 0 0 1 140 66 Q100 36 60 66Z", col)
        return back, front
    if name == "cap":
        return "", P("M64 44 A36 34 0 0 1 136 44Z", col) + P("M120 44 L152 50 L122 52Z", col, 3)
    if name == "fez":
        return "", T([(76, 40), (82, 8), (118, 8), (124, 40)], col) + L(100, 8, 112, 24, "#f1c40f", 3)
    if name == "sailor":
        return "", P("M64 40 A36 30 0 0 1 136 40Z", "#fff") + R(62, 36, 76, 10, col, 4)
    if name == "mask":
        return "", P("M68 66 Q100 60 132 66 L128 96 Q100 108 72 96Z", "#222", 3) + P("M66 56 A36 32 0 0 1 134 56Z", "#222", 3)
    if name == "bonnet":
        return "", E(100, 40, 38, 18, "#fff") + P("M64 48 Q60 90 72 96", "none", 3) + P("M136 48 Q140 90 128 96", "none", 3)
    if name == "scarf":
        back = P("M58 64 A42 42 0 0 1 142 64 Q146 118 124 126 L76 126 Q54 118 58 64Z", col)
        front = P("M62 62 A38 38 0 0 1 138 62 Q118 44 100 46 Q82 44 62 62Z", col)
        return back, front
    if name == "helmet":
        return "", P("M62 52 A38 36 0 0 1 138 52Z", "#95a5a6")
    return "", ""

def _extra(name, hx=150, hy=172):
    if name == "wand":
        return L(hx, hy, hx + 28, hy - 56, "#8e5a2b", 5) + T([(hx + 28, hy - 74), (hx + 33, hy - 62), (hx + 46, hy - 62), (hx + 36, hy - 54), (hx + 40, hy - 40), (hx + 28, hy - 48), (hx + 16, hy - 40), (hx + 20, hy - 54), (hx + 10, hy - 62), (hx + 23, hy - 62)], "#f1c40f", 2)
    if name == "basket":
        return P(f"M{hx-26} {hy-8} L{hx+26} {hy-8} L{hx+20} {hy+28} L{hx-20} {hy+28}Z", "#c9a063") + P(f"M{hx-22} {hy-8} Q{hx} {hy-46} {hx+22} {hy-8}", "none", 4) + R(hx - 22, hy - 12, 44, 8, "#fff", 2)
    if name == "axe":
        return L(hx, hy + 20, hx + 6, hy - 60, "#8e5a2b", 6) + P(f"M{hx+4} {hy-60} Q{hx+40} {hy-70} {hx+34} {hy-30} Q{hx+10} {hy-34} {hx+4} {hy-60}Z", "#bdc3c7")
    if name == "sack":
        return P(f"M{hx-24} {hy+30} Q{hx-34} {hy-10} {hx-10} {hy-24} L{hx+10} {hy-24} Q{hx+34} {hy-10} {hx+24} {hy+30}Z", "#d6b878") + L(hx - 10, hy - 24, hx + 10, hy - 24, OUT, 5)
    if name == "whistle":
        return E(hx, hy, 12, 7, "#bdc3c7", 2) + L(hx - 12, hy - 4, hx - 30, hy - 14, "#bdc3c7", 3)
    if name == "sword":
        return L(hx, hy + 10, hx + 6, hy - 70, "#bdc3c7", 7) + L(hx - 14, hy + 8, hx + 14, hy + 4, "#8e5a2b", 6)
    if name == "ball":
        return C(hx, hy - 12, 18, "#f1c40f") + P(f"M{hx-10} {hy-22} Q{hx-4} {hy-18} {hx-8} {hy-10}", "none", 2)
    if name == "cane":
        return L(hx, hy + 24, hx + 4, hy - 56, "#8e5a2b", 5) + P(f"M{hx+4} {hy-56} Q{hx+22} {hy-70} {hx+26} {hy-50}", "none", 5)
    if name == "bag":
        return R(hx - 18, hy - 6, 36, 30, "#a0522d", 6) + P(f"M{hx-10} {hy-6} Q{hx} {hy-22} {hx+10} {hy-6}", "none", 3)
    return ""

def person(skin=SKIN[0], hair="#3b2a1a", hs="short", top="#c0392b", bottom="#34495e", dress=None,
           hat=None, hatcol="#e8e8e8", beard=None, extra=None, mouth="smile", ph=0, eyes="open",
           cape=None, glasses=False, shoes="#4a3426", sleeve=None, kid=False, apron=None, vest=None):
    body = []
    hb, hf = _hat(hat, hatcol, hair) if hat else ("", "")
    # cape / derrière
    if cape and hat != "hood":
        body.append(P("M70 100 L130 100 L158 232 L42 232Z", cape))
    body.append(hb)
    if hs == "long":
        body.append(P("M62 50 Q56 150 74 160 L126 160 Q144 150 138 50Z", hair))
    if hs == "braids":
        for d in ("M64 66 Q52 110 66 152", "M136 66 Q148 110 134 152"):
            body.append(f'<path d="{d}" fill="none" stroke="{OUT}" stroke-width="15" stroke-linecap="round"/><path d="{d}" fill="none" stroke="{hair}" stroke-width="9" stroke-linecap="round"/>')
    # jambes
    if dress:
        for sg in (-1, 1):
            hx = 100 + sg * 14
            fx = hx + (16 * ph if sg < 0 else -16 * ph)
            body.append(LIMB(hx, 215, fx, 248, skin, 10))
            body.append(E(fx + 4, 252, 13, 6, shoes, 2))
    else:
        for sg in (-1, 1):
            hx = 100 + sg * 16
            fx = hx + sg * 5 + (24 * ph if sg < 0 else -24 * ph)
            body.append(LIMB(hx, 184, fx, 246, bottom, 18))
            body.append(E(fx + 4, 252, 15, 7, shoes, 2))
    # corps
    if dress:
        body.append(P("M72 100 Q100 94 128 100 L156 222 Q100 236 44 222Z", dress))
        if apron:
            body.append(P("M84 116 L116 116 L128 220 Q100 228 72 220Z", apron))
    else:
        body.append(R(68, 98, 64, 92, top, 18))
        if vest:
            body.append(P("M76 98 L100 140 L124 98 L124 190 L76 190Z", vest, 3))
        if apron:
            body.append(P("M80 120 L120 120 L124 190 L76 190Z", apron))
    # bras
    sl = sleeve or (dress or top)
    for sg in (-1, 1):
        sx = 100 + sg * 31
        hx = 100 + sg * 48 + (14 * ph if sg < 0 else -14 * ph) * 0.6
        hy = 172 + (8 * ph if sg < 0 else -8 * ph)
        body.append(LIMB(sx, 112, hx, hy, sl, 16))
        body.append(C(hx, hy + 4, 9, skin, 2.5))
    # accessoire (main droite)
    if extra:
        body.append(_extra(extra))
    # tête
    body.append(C(100, 62, 34, skin))
    if hs == "short":
        body.append(P("M66 58 A34 34 0 0 1 134 58 Q118 42 100 46 Q82 42 66 58Z", hair))
    elif hs == "long":
        body.append(P("M66 62 A34 34 0 0 1 134 62 Q116 40 100 44 Q82 40 66 62Z", hair))
    elif hs == "braids":
        body.append(P("M66 62 A34 34 0 0 1 134 62 Q116 40 100 44 Q82 40 66 62Z", hair))
    elif hs == "bun":
        body.append(C(100, 22, 14, hair)); body.append(P("M66 62 A34 34 0 0 1 134 62 Q116 40 100 44 Q82 40 66 62Z", hair))
    elif hs == "curly":
        for cx in (74, 88, 100, 112, 126):
            body.append(C(cx, 38 if cx in (88, 100, 112) else 46, 12, hair, 2))
    elif hs == "gray":
        body.append(P("M66 58 A34 34 0 0 1 134 58 Q118 42 100 46 Q82 42 66 58Z", "#d0d0d0"))
    # visage
    if eyes == "open":
        body.append(C(88, 62, 4.5, "#222", 0)); body.append(C(112, 62, 4.5, "#222", 0))
    else:
        body.append(L(83, 62, 93, 62, "#222", 3)); body.append(L(107, 62, 117, 62, "#222", 3))
    body.append(E(80, 74, 6, 4, "#f2a0a0", 0)); body.append(E(120, 74, 6, 4, "#f2a0a0", 0))
    if mouth == "smile":
        body.append(P("M88 76 Q100 88 112 76", "none", 3))
    elif mouth == "open":
        body.append(E(100, 81, 8, 7, "#7a1f1f", 2.5))
    elif mouth == "sad":
        body.append(P("M90 84 Q100 74 110 84", "none", 3))
    elif mouth == "flat":
        body.append(L(91, 80, 109, 80, OUT, 3))
    if glasses:
        body.append(C(88, 62, 10, "none", 2.5)); body.append(C(112, 62, 10, "none", 2.5)); body.append(L(98, 62, 102, 62, OUT, 2.5))
    if beard == "full":
        body.append(P("M68 70 Q72 118 100 120 Q128 118 132 70 Q118 90 100 88 Q82 90 68 70Z", hair))
        body.append(P("M90 80 Q100 76 110 80", "none", 3))
    elif beard == "goatee":
        body.append(P("M88 92 Q100 118 112 92 Q100 98 88 92Z", hair))
    elif beard == "mustache":
        body.append(P("M84 74 Q100 66 116 74 Q100 82 84 74Z", hair))
    body.append(hf)
    return SVG(200, 270, "".join(body))

# ---------- catalogue des personnages ----------
def catalogue():
    k = {}
    k["cendrillon_servante"] = ("سندريلا خادمة", dict(hs="long", hair="#e8c15a", dress="#9a8f80", apron="#e8e2d0", hat="scarf", hatcol="#c9b99a", mouth="sad"), ["cinderella"])
    k["cendrillon_bal"] = ("سندريلا في الحفلة", dict(hs="long", hair="#e8c15a", dress="#8ecbf0", hat="tiara", sleeve="#8ecbf0"), ["cinderella"])
    k["belle_mere"] = ("زوجة الأب", dict(hs="bun", hair="#2a2a2a", dress="#7a3a8a", mouth="flat"), ["cinderella"])
    k["soeur_1"] = ("الأخت الأولى", dict(hs="curly", hair="#c0392b", dress="#e87aa8"), ["cinderella"])
    k["soeur_2"] = ("الأخت الثانية", dict(hs="braids", hair="#6b3a1a", dress="#f2a23a"), ["cinderella"])
    k["fee"] = ("الجنية", dict(hs="long", hair="#f3e8b0", dress="#c9a7f2", extra="wand", hat="tiara", cape="#e8d9ff"), ["cinderella"])
    k["prince"] = ("الأمير", dict(top="#b32a3a", bottom="#2a3f7a", hat="crown", cape="#8a1a2a", sleeve="#b32a3a", hair="#5a3a1a"), ["cinderella", "frog"])
    k["laila"] = ("ليلى ذات القبعة الحمراء", dict(hs="braids", hair="#5a3a1a", dress="#f2f2f2", hat="hood", hatcol="#c4302b", extra="basket", sleeve="#f2f2f2"), ["layla"])
    k["mere"] = ("الأم", dict(hs="bun", hair="#5a3a1a", dress="#4a8a6a", apron="#f2f2f2"), ["layla"])
    k["grand_mere"] = ("الجدة", dict(hs="gray", dress="#b79ad0", glasses=True, hat="bonnet", extra="cane", skin=SKIN[1]), ["layla"])
    k["bucheron"] = ("الحطاب", dict(top="#2f7d4a", bottom="#5a4a3a", beard="full", hair="#8a3a1a", extra="axe", hat="cap", hatcol="#a0522d"), ["layla"])
    k["djeha"] = ("جحا", dict(top="#3a5a9c", bottom="#3a5a9c", hat="turban", hatcol="#f2f2f2", beard="full", hair="#6a6a6a", skin=SKIN[2], extra="cane", sleeve="#3a5a9c"), ["djeha"])
    k["fils_djeha"] = ("ابن جحا", dict(top="#6c8fd6", bottom="#3a5a9c", hat="cap", hatcol="#d08a1e", hair="#2a2a2a", skin=SKIN[2]), ["djeha"])
    k["passant_1"] = ("المارّ الأول", dict(top="#c07a3a", bottom="#5a4a3a", hat="fez", hatcol="#b32a3a", beard="mustache", hair="#222", skin=SKIN[1]), ["djeha"])
    k["passant_2"] = ("المارّة", dict(hs="long", hair="#2a2a2a", dress="#8a4a7a", hat="scarf", hatcol="#e8c15a", skin=SKIN[1]), ["djeha"])
    k["ali_baba"] = ("علي بابا", dict(top="#8a5a2a", bottom="#5a3a1a", hat="turban", hatcol="#c9a063", beard="full", hair="#3a2a1a", skin=SKIN[2], sleeve="#8a5a2a", extra="axe"), ["alibaba"])
    k["qasim"] = ("قاسم", dict(top="#4a6fa5", bottom="#2a3f6a", hat="turban", hatcol="#4a6fa5", beard="goatee", hair="#222", skin=SKIN[2], extra="bag"), ["alibaba"])
    k["morgiane"] = ("مرجانة", dict(hs="long", hair="#222", dress="#d46a9e", hat="scarf", hatcol="#f2c230", skin=SKIN[1], mouth="smile"), ["alibaba"])
    k["chef_voleurs"] = ("رئيس اللصوص", dict(top="#222", bottom="#333", hat="turban", hatcol="#222", beard="full", hair="#111", skin=SKIN[3], sleeve="#222", extra="sword"), ["alibaba"])
    k["voleur"] = ("لص", dict(top="#444", bottom="#2a2a2a", hat="mask", hair="#111", skin=SKIN[2], extra="sack"), ["alibaba"])
    k["sindbad"] = ("السندباد", dict(top="#e8e2d0", vest="#c0392b", bottom="#1f5a8a", hat="turban", hatcol="#c0392b", hair="#222", beard="mustache", skin=SKIN[2]), ["sindbad"])
    k["marin"] = ("بحّار", dict(top="#fff", bottom="#1f3a6a", hat="sailor", hatcol="#1f3a6a", hair="#6a3a1a", beard="goatee", sleeve="#fff"), ["sindbad"])
    k["capitaine"] = ("قبطان", dict(top="#1f3a6a", bottom="#1f3a6a", hat="helmet", beard="full", hair="#aaa", skin=SKIN[1], cape="#1f3a6a"), ["sindbad"])
    k["princesse"] = ("الأميرة", dict(hs="long", hair="#6a3a1a", dress="#f2a0c8", hat="tiara"), ["frog", "cinderella"])
    k["roi"] = ("الملك", dict(top="#8a1a2a", bottom="#5a1a1a", hat="crown", beard="full", hair="#ddd", cape="#c0392b", skin=SKIN[1], sleeve="#8a1a2a"), ["frog"])
    k["reine"] = ("الملكة", dict(hs="bun", hair="#aaa", dress="#6a3a8a", hat="tiara", skin=SKIN[1]), ["frog"])
    k["chasseur"] = ("الصياد", dict(top="#6a4a2a", bottom="#3a4a2a", hat="cap", hatcol="#3a4a2a", beard="mustache", hair="#3a2a1a"), ["lion"])
    k["arbitre"] = ("الحكم", dict(top="#222", bottom="#222", hat="cap", hatcol="#222", extra="whistle", hair="#2a2a2a", vest="#fff"), ["hare"])
    k["garcon"] = ("ولد", dict(top="#3a8ad6", bottom="#3a3a5a", hair="#4a2a1a", kid=True), [])
    k["fille"] = ("بنت", dict(hs="braids", hair="#4a2a1a", dress="#e8683a"), [])
    k["marchand"] = ("تاجر", dict(top="#8a6a1a", bottom="#6a4a1a", hat="turban", hatcol="#e8c15a", beard="full", hair="#444", skin=SKIN[2], extra="sack"), [])
    k["maitre"] = ("المعلّم", dict(top="#556", bottom="#334", glasses=True, hair="#555", beard="goatee"), [])
    k["maitresse"] = ("المعلّمة", dict(hs="bun", hair="#4a2a1a", dress="#3a8a8a", glasses=True), [])
    k["vieux"] = ("رجل عجوز", dict(top="#8a8a6a", bottom="#5a5a4a", hs="gray", beard="full", hair="#ddd", extra="cane", skin=SKIN[1]), [])
    k["pecheur"] = ("صيّاد سمك", dict(top="#3a6a8a", bottom="#2a3a4a", hat="cap", hatcol="#e8c15a", hair="#3a2a1a", skin=SKIN[2]), ["sindbad"])
    k["berger"] = ("الراعي", dict(top="#c9a063", vest="#6a4a2a", bottom="#5a4a3a", hat="cap", hatcol="#8a5a2a", extra="cane", hair="#3a2a1a", skin=SKIN[2]), ["shepherd"])
    k["villageois"] = ("قروي", dict(top="#6a8a4a", bottom="#4a4a3a", hat="turban", hatcol="#e8e8d8", beard="mustache", hair="#333", skin=SKIN[1]), ["shepherd", "djeha"])
    return k

def render_person(spec, **over):
    kw = dict(spec); kw.update(over)
    return person(**kw)
