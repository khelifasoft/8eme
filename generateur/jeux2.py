"""Jeux éducatifs variés (pas liés aux contes) : questions à choix, mémoire, calcul, rapidité.
Usage : python3 generateur/jeux2.py jeux"""
import sys, os, json, zipfile, random, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scratch as sc, scratch_art as art
from svgkit import *
from xml.sax.saxutils import escape
OUT = sys.argv[1] if len(sys.argv) > 1 else "jeux"
RND = random.Random(11)

# ------------------------------------------------------------------ blocs
class B(sc.Blocks):
    def add(self, opcode, inputs=None, fields=None, shadow=False):
        if inputs:
            inputs = {k: ([3, v, [10, ""]] if isinstance(v, str) else v) for k, v in inputs.items()}
        i = super().add(opcode, inputs, fields, shadow)
        for v in (inputs or {}).values():
            if isinstance(v, list) and len(v) >= 2 and isinstance(v[1], str) and v[1] in self.b and v[1] != i: self.b[v[1]]["parent"] = i
        return i
    # entrées
    def N(self, x): return [1, [4, str(x)]]
    def S(self, x): return [1, [10, str(x)]]
    def R(self, i): return [3, i, [4, "0"]]          # reporter dans un champ numérique
    def RS(self, i): return [3, i, [10, ""]]         # reporter dans un champ texte
    def C(self, i): return [2, i]                    # condition / pile
    # pile
    def stack(self, *ids):
        ids = [i for i in ids if i]
        for a, c in zip(ids, ids[1:]): self.b[a]["next"] = c; self.b[c]["parent"] = a
        return ids[0]
    def script(self, hat, *blocks, y=0):
        ids = [hat] + [i for i in blocks if i]
        for a, c in zip(ids, ids[1:]): self.b[a]["next"] = c; self.b[c]["parent"] = a
        self.b[hat]["topLevel"] = True; self.b[hat]["x"] = 0; self.b[hat]["y"] = y
        return hat
    # variables / listes
    def var(self, name, vid): return self.add("data_variable", fields={"VARIABLE": [name, vid]})
    def setv(self, name, vid, v): return self.add("data_setvariableto", fields={"VARIABLE": [name, vid]}, inputs={"VALUE": v if isinstance(v, list) else self.S(v)})
    def chg(self, name, vid, v): return self.add("data_changevariableby", fields={"VARIABLE": [name, vid]}, inputs={"VALUE": v if isinstance(v, list) else self.N(v)})
    def item(self, lname, lid, idx): return self.add("data_itemoflist", fields={"LIST": [lname, lid]}, inputs={"INDEX": idx})
    # opérateurs
    def op(self, opc, a, b, k1="NUM1", k2="NUM2"): return self.add(opc, inputs={k1: a, k2: b})
    def add_(self, a, b): return self.op("operator_add", a, b)
    def sub_(self, a, b): return self.op("operator_subtract", a, b)
    def mul_(self, a, b): return self.op("operator_multiply", a, b)
    def join(self, a, b): return self.op("operator_join", a, b, "STRING1", "STRING2")
    def eq(self, a, b): return self.op("operator_equals", a, b, "OPERAND1", "OPERAND2")
    def lt(self, a, b): return self.op("operator_lt", a, b, "OPERAND1", "OPERAND2")
    def gt(self, a, b): return self.op("operator_gt", a, b, "OPERAND1", "OPERAND2")
    def and_(self, a, b): return self.op("operator_and", self.C(a), self.C(b), "OPERAND1", "OPERAND2")
    def or_(self, a, b): return self.op("operator_or", self.C(a), self.C(b), "OPERAND1", "OPERAND2")
    def rand(self, a, b): return self.add("operator_random", inputs={"FROM": a, "TO": b})
    def mod(self, a, b): return self.op("operator_mod", a, b)
    def absv(self, a): return self.add("operator_mathop", fields={"OPERATOR": ["abs", None]}, inputs={"NUM": a})
    # contrôle
    def if_(self, cond, *body): return self.add("control_if", inputs={"CONDITION": self.C(cond), "SUBSTACK": self.C(self.stack(*body))} if body else {"CONDITION": self.C(cond)})
    def ifelse(self, cond, a, b): return self.add("control_if_else", inputs={"CONDITION": self.C(cond), "SUBSTACK": self.C(self.stack(*a)), "SUBSTACK2": self.C(self.stack(*b))})
    def repeat(self, n, *body): return self.add("control_repeat", inputs={"TIMES": [1, [6, str(n)]], "SUBSTACK": self.C(self.stack(*body))})
    def until(self, cond, *body): return self.add("control_repeat_until", inputs={"CONDITION": self.C(cond), "SUBSTACK": self.C(self.stack(*body))})
    def forever_(self, *body): return self.add("control_forever", inputs={"SUBSTACK": self.C(self.stack(*body))})
    def stop_other(self):
        i = self.add("control_stop", fields={"STOP_OPTION": ["other scripts in sprite", None]}); self.b[i]["mutation"] = {"tagName": "mutation", "children": [], "hasnext": "true"}; return i
    def stop_all(self):
        i = self.add("control_stop", fields={"STOP_OPTION": ["all", None]}); self.b[i]["mutation"] = {"tagName": "mutation", "children": [], "hasnext": "false"}; return i
    def when_clicked(self): return self.add("event_whenthisspriteclicked")
    def key(self, name):
        m = self.add("sensing_keyoptions", fields={"KEY_OPTION": [name, None]}, shadow=True)
        return self.add("sensing_keypressed", inputs={"KEY_OPTION": [1, m]})
    def ask(self, q): return self.add("sensing_askandwait", inputs={"QUESTION": q})
    def answer(self): return self.add("sensing_answer")
    def say_(self, m): return self.add("looks_say", inputs={"MESSAGE": m})
    def sayfor(self, m, s): return self.add("looks_sayforsecs", inputs={"MESSAGE": m, "SECS": self.N(s)})
    def costume_n(self, idxrep):
        rid = idxrep[1] if isinstance(idxrep, list) else idxrep
        m = self.add("looks_costume", fields={"COSTUME": ["1", None]}, shadow=True)
        return self.add("looks_switchcostumeto", inputs={"COSTUME": [3, rid, m]})
    def setx(self, v): return self.add("motion_setx", inputs={"X": v})
    def chx(self, v): return self.add("motion_changexby", inputs={"DX": v})
    def xpos(self): return self.add("motion_xposition")
    def ypos(self): return self.add("motion_yposition")
    def gotoxy_(self, x, y): return self.add("motion_gotoxy", inputs={"X": x, "Y": y})
    def chy(self, v): return self.add("motion_changeyby", inputs={"DY": v})
    def recv(self, name, bid): return self.hat_recv(name, bid)

# ------------------------------------------------------------------ images
def nest(svg, x, y, w, h):
    m = re.match(r'<svg[^>]*width="(\d+)" height="(\d+)"[^>]*>', svg)
    W, H = m.group(1), m.group(2)
    return f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet">' + svg[m.end():]
def wrap(text, n):
    lines, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 > n and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    return lines + ([cur] if cur else [])
def card(w, h, lines, fill="#ffffff", ink="#1d2433", size=26, stroke="#1f4aa8", art_svg=None, art_w=0, art_mode="left"):
    body = f'<rect x="2" y="2" width="{w-4}" height="{h-4}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="4"/>'
    tx = w / 2 + (art_w / 2 if art_svg and art_mode == "left" else 0)
    cy = h / 2
    if art_svg and art_mode == "left": body += nest(art_svg, 10, 10, art_w, h - 20)
    elif art_svg: body += nest(art_svg, 10, 8, w - 20, h - 56); cy = h - 26
    n = len(lines); lh = size * 1.25; y0 = cy - (n - 1) * lh / 2 + size * 0.33
    for i, l in enumerate(lines):
        body += f'<text x="{tx}" y="{y0 + i*lh}" text-anchor="middle" font-family="Sans Serif" font-size="{size}" font-weight="bold" fill="{ink}">{escape(l)}</text>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>'
def bg_svg(color1, color2):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{color1}"/><stop offset="1" stop-color="{color2}"/></linearGradient></defs><rect width="480" height="360" fill="url(#g)"/></svg>')

# ------------------------------------------------------------------ projet
class Proj:
    def __init__(self, gid):
        self.gid = gid; self.zf = zipfile.ZipFile(os.path.join(OUT, f"jeu_{gid}.sb3"), "w", zipfile.ZIP_DEFLATED); self.store = set()
        self.vars = {}; self.lists = {}; self.bcs = {}; self.targets = []; self.layer = 1; self.monitors = []
        self.stage = B(); self.stage_costumes = []; self.stage_sounds = []
    def V(self, name):
        if name not in self.vars: self.vars[name] = "v_" + str(len(self.vars) + 1)
        return name, self.vars[name]
    def L(self, name, items):
        self.lists[name] = ("l_" + str(len(self.lists) + 1), [str(x) for x in items]); return name, self.lists[name][0]
    def mid(self, name):
        if name not in self.bcs: self.bcs[name] = "m_" + str(len(self.bcs) + 1)
        return name, self.bcs[name]
    def bc(self, b, name, wait=False): n, i = self.mid(name); return b.bc(n, i, wait)
    def hat(self, b, name): n, i = self.mid(name); return b.recv(n, i)
    def costume(self, name, svg, cx=None, cy=None):
        md = sc.asset(self.zf, svg, self.store); w, h = art.svg_size(svg)
        return {"assetId": md, "name": name, "md5ext": md + ".svg", "dataFormat": "svg", "rotationCenterX": (cx if cx is not None else w // 2), "rotationCenterY": (cy if cy is not None else h // 2)}
    def sfx(self, key): return sc.sfx(self.zf, self.store, key)
    def sprite(self, name, b, costumes, sounds=(), x=0, y=0, size=100, visible=False, local_vars=None, flip=False):
        t = {"isStage": False, "name": name, "variables": {vid: [n, v] for (n, vid, v) in (local_vars or [])}, "lists": {}, "broadcasts": {}, "blocks": b.b, "comments": {},
             "currentCostume": 0, "costumes": costumes, "sounds": list(sounds), "volume": 100, "layerOrder": self.layer, "visible": visible, "x": x, "y": y,
             "size": size, "direction": 90, "draggable": False, "rotationStyle": "left-right" if flip else "don't rotate"}
        self.layer += 1; self.targets.append(t); return t
    def monitor(self, name, y, visible=True):
        n, vid = self.V(name)
        self.monitors.append({"id": vid, "mode": "default", "opcode": "data_variable", "params": {"VARIABLE": n}, "spriteName": None, "value": 0, "width": 0, "height": 0, "x": 5, "y": y, "visible": visible, "sliderMin": 0, "sliderMax": 100, "isDiscrete": True})
    def finish(self, music=None):
        if music:
            ms = self.sfx(music); self.stage_sounds.append(ms); sb = self.stage
            sb.script(sb.hat_flag(), sb.volume(12), sb.forever(sb.play_wait(ms["name"])), y=900)
        stage = {"isStage": True, "name": "Stage", "variables": {vid: [n, 0] for n, vid in self.vars.items()}, "lists": {lid: [n, items] for n, (lid, items) in self.lists.items()},
                 "broadcasts": {i: n for n, i in self.bcs.items()}, "blocks": self.stage.b, "comments": {}, "currentCostume": 0, "costumes": self.stage_costumes, "sounds": self.stage_sounds,
                 "volume": 100, "layerOrder": 0, "tempo": 60, "videoTransparency": 50, "videoState": "on", "textToSpeechLanguage": None}
        proj = {"targets": [stage] + self.targets, "monitors": self.monitors, "extensions": [], "meta": {"semver": "3.0.0", "vm": "0.2.0", "agent": "Mozilla/5.0"}}
        self.zf.writestr("project.json", json.dumps(proj, ensure_ascii=False)); self.zf.close()

# ------------------------------------------------------------------ 1) QUESTIONS À CHOIX
def mc_game(gid, questions, layout="row", bg=("#e8f0ff", "#c9dcff"), music="joyeuse", intro=None):
    """questions : [{"lines":[...], "art":(kind,key) ou None, "opts":[(lignes...)x3], "ans": 1..3}]"""
    P = Proj(gid); N = len(questions); sb = P.stage
    P.stage_costumes.append(P.costume("fond", bg_svg(*bg), 240, 180))
    q, qi = P.V("السؤال"); sco, si = P.V("النقاط"); lk, li = P.V("قفل")
    okv, oki = P.V("الصحيح")
    ding, bad = P.sfx("ding"), P.sfx("echec")
    # scène : démarrage
    for hatname in ("flag", "إعادة"):
        hat = sb.hat_flag() if hatname == "flag" else P.hat(sb, "إعادة")
        sb.script(hat, sb.setv(q, qi, 1), sb.setv(sco, si, 0), sb.setv(lk, li, 0), P.bc(sb, "عرض"), y=0 if hatname == "flag" else 200)
    # carte de la question
    qb = B(); qc = []
    for qi_, it in enumerate(questions):
        a = it.get("art"); asvg = art.art_svg(*a) if a else it.get("art_svg")
        qc.append(P.costume(f"q{qi_+1}", card(420, it.get("h", 150 if layout == "row" else 120), it["lines"], "#ffffff", size=28 if len(it["lines"]) < 3 else 22, art_svg=asvg, art_w=it.get("art_w", 120) if asvg else 0, art_mode=it.get("art_mode", "left"))))
    chain = [qb.if_(qb.eq(qb.R(qb.var(q, qi)), qb.N(k + 1)), qb.setv(okv, oki, it["ans"])) for k, it in enumerate(questions)]
    qb.script(P.hat(qb, "عرض"), qb.costume_n(qb.R(qb.var(q, qi))), qb.show(), *chain, y=0)
    qb.script(P.hat(qb, "نهاية"), qb.hide(), y=160)
    P.sprite("السؤال", qb, qc, x=0, y=(85 if layout == "row" else 120), size=100)
    # options
    pos = {"row": [(-150, -85), (0, -85), (150, -85)], "col": [(0, 25), (0, -40), (0, -105)]}[layout]
    ow, oh = (140, 70) if layout == "row" else (400, 56)
    for k in range(3):
        ob = B(); oc = []
        for qi_, it in enumerate(questions):
            ln = it["opts"][k]; oc.append(P.costume(f"o{qi_+1}", card(ow, oh, ln if isinstance(ln, list) else [ln], "#fff7e0", stroke="#e8861c", size=(30 if layout == "row" else 22) if sum(len(x) for x in (ln if isinstance(ln, list) else [ln])) < 14 else 20)))
        ob.script(P.hat(ob, "عرض"), ob.costume_n(ob.R(ob.var(q, qi))), ob.show(), y=0)
        ob.script(P.hat(ob, "نهاية"), ob.hide(), y=160)
        good = [P.bc(ob, "صح")]; bad_ = [P.bc(ob, "خطأ")]
        hit = ob.eq(ob.R(ob.var(okv, oki)), ob.N(k + 1))
        body = ob.if_(ob.eq(ob.R(ob.var(lk, li)), ob.N(0)),
            ob.setv(lk, li, 1),
            ob.ifelse(hit, [ob.chg(sco, si, 1), ob.play(ding["name"]), good[0]], [ob.play(bad["name"]), bad_[0]]),
            ob.wait(0.9), ob.chg(q, qi, 1),
            ob.ifelse(ob.gt(ob.R(ob.var(q, qi)), ob.N(N)), [P.bc(ob, "نهاية")], [ob.setv(lk, li, 0), P.bc(ob, "عرض")]))
        ob.script(ob.when_clicked(), body, y=320)
        P.sprite(f"خيار {k+1}", ob, oc, [ding, bad], x=pos[k][0], y=pos[k][1])
    # retour visuel ✔ ✘
    fb = B()
    ok = f'<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 120 120"><circle cx="60" cy="60" r="54" fill="#2e9e5b" stroke="#1d6b3c" stroke-width="5"/><path d="M32 62 L52 82 L90 38" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    no = f'<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 120 120"><circle cx="60" cy="60" r="54" fill="#d6453d" stroke="#8e1f19" stroke-width="5"/><path d="M38 38 L82 82 M82 38 L38 82" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round"/></svg>'
    fb.script(P.hat(fb, "صح"), fb.add("looks_switchcostumeto", inputs={"COSTUME": [1, fb.add("looks_costume", fields={"COSTUME": ["صح", None]}, shadow=True)]}), fb.show(), fb.wait(0.8), fb.hide(), y=0)
    fb.script(P.hat(fb, "خطأ"), fb.add("looks_switchcostumeto", inputs={"COSTUME": [1, fb.add("looks_costume", fields={"COSTUME": ["خطأ", None]}, shadow=True)]}), fb.show(), fb.wait(0.8), fb.hide(), y=160)
    P.sprite("النتيجة الفورية", fb, [P.costume("صح", ok), P.costume("خطأ", no)], x=0, y=-10, size=70)
    # fin
    eb = B()
    eb.script(P.hat(eb, "نهاية"), eb.show(), eb.say_(eb.join(eb.S("انتهت اللعبة! نتيجتك: "), eb.join(eb.RS(eb.var(sco, si)), eb.S(f" من {N}  (اضغط للإعادة)")))), y=0)
    eb.script(P.hat(eb, "عرض"), eb.hide(), eb.say_(eb.S("")), y=160)
    eb.script(eb.when_clicked(), P.bc(eb, "إعادة"), y=320)
    P.sprite("النهاية", eb, [P.costume("نهاية", card(300, 90, ["انتهت اللعبة"], "#fff3c4", size=28, stroke="#e8861c"))], x=0, y=-20)
    P.monitor("النقاط", 5); P.monitor("السؤال", 32); P.monitor("قفل", 59, False)
    P.finish(music)
    return dict(N=N)


# ------------------------------------------------------------------ 2) MÉMOIRE (paires)
def memory_game(gid, pairs, bg=("#e9f7ea", "#cdebd0"), music="joyeuse"):
    """pairs : 6 éléments [(genre, clé)]"""
    P = Proj(gid); sb = P.stage
    P.stage_costumes.append(P.costume("fond", bg_svg(*bg), 240, 180))
    first, fi = P.V("الأولى"); pair1, pi1 = P.V("زوج الأولى"); lock, li = P.V("قفل"); mt, mi = P.V("الأزواج"); mv, mvi = P.V("المحاولات")
    ding, bad = P.sfx("ding"), P.sfx("echec")
    ids = list(range(1, 13)); order = [(k // 2) for k in range(12)]; RND.shuffle(order)   # carte -> numéro de paire
    for hatname in ("flag", "إعادة"):
        hat = sb.hat_flag() if hatname == "flag" else P.hat(sb, "إعادة")
        sb.script(hat, sb.setv(first, fi, 0), sb.setv(pair1, pi1, 0), sb.setv(lock, li, 0), sb.setv(mt, mi, 0), sb.setv(mv, mvi, 0), P.bc(sb, "إخفاء"), y=0 if hatname == "flag" else 240)
    pos = [(-150 + 100 * c, 95 - 95 * r) for r in range(3) for c in range(4)]
    back = card(84, 84, ["؟"], "#2f5fc4", "#ffffff", size=46, stroke="#1a3a85")
    for k in range(12):
        b = B(); pr = order[k]; kind, key = pairs[pr]
        lp, lpi = f"pr_{k}", f"lv_p{k}"; lm, lmi = f"hd_{k}", f"lv_h{k}"
        front = card(84, 84, [], "#ffffff", stroke="#e8861c")
        front = front.replace("</svg>", nest(art.art_svg(kind, key), 8, 8, 68, 68) + "</svg>")
        cos = [P.costume("ظهر", back), P.costume("وجه", front)]
        my = b.N(k + 1)
        def L(name, vid): return b.var(name, vid)
        # reset
        b.script(P.hat(b, "إخفاء"), b.setv(lm, lmi, 0), b.add("looks_switchcostumeto", inputs={"COSTUME": [1, b.add("looks_costume", fields={"COSTUME": ["ظهر", None]}, shadow=True)]}), b.show(), y=0)
        def flip(name): return b.add("looks_switchcostumeto", inputs={"COSTUME": [1, b.add("looks_costume", fields={"COSTUME": [name, None]}, shadow=True)]})
        # clic
        samepair = b.eq(b.R(b.var(pair1, pi1)), b.R(L(lp, lpi)))
        second_branch = [b.setv(lock, li, 1), b.chg(mv, mvi, 1),
            b.ifelse(samepair,
                [b.setv(lm, lmi, 1), b.play(ding["name"]), P.bc(b, "نجاح", True), b.chg(mt, mi, 1), b.setv(first, fi, 0), b.setv(lock, li, 0),
                 b.if_(b.eq(b.R(b.var(mt, mi)), b.N(6)), P.bc(b, "فوز"))],
                [b.play(bad["name"]), b.wait(0.9), flip("ظهر"), P.bc(b, "رجوع", True), b.setv(first, fi, 0), b.setv(lock, li, 0)])]
        first_branch = [b.setv(first, fi, k + 1), b.setv(pair1, pi1, b.RS(L(lp, lpi)))]
        click = b.if_(b.eq(b.R(b.var(lock, li)), b.N(0)),
            b.if_(b.eq(b.R(L(lm, lmi)), b.N(0)),
                b.if_(b.eq(b.R(b.add("looks_costumenumbername", fields={"NUMBER_NAME": ["number", None]})), b.N(1)),
                    flip("وجه"),
                    b.ifelse(b.eq(b.R(b.var(first, fi)), b.N(0)), first_branch, second_branch))))
        b.script(b.when_clicked(), click, y=200)
        b.script(P.hat(b, "نجاح"), b.if_(b.eq(b.R(b.var(first, fi)), b.N(k + 1)), b.setv(lm, lmi, 1)), y=360)
        b.script(P.hat(b, "رجوع"), b.if_(b.eq(b.R(b.var(first, fi)), b.N(k + 1)), b.if_(b.eq(b.R(L(lm, lmi)), b.N(0)), flip("ظهر"))), y=480)
        P.sprite(f"بطاقة {k+1}", b, cos, [ding, bad], x=pos[k][0], y=pos[k][1], visible=True,
                 local_vars=[(lp, lpi, pr + 1), (lm, lmi, 0)])
    eb = B()
    eb.script(P.hat(eb, "فوز"), eb.wait(0.6), eb.show(), eb.say_(eb.join(eb.S("أحسنت! عدد المحاولات: "), eb.join(eb.RS(eb.var(mv, mvi)), eb.S("  (اضغط للإعادة)")))), y=0)
    eb.script(P.hat(eb, "إخفاء"), eb.hide(), eb.say_(eb.S("")), y=160)
    eb.script(eb.when_clicked(), P.bc(eb, "إعادة"), y=320)
    P.sprite("الفوز", eb, [P.costume("فوز", card(300, 80, ["أحسنت، وجدت كل الأزواج"], "#fff3c4", size=22, stroke="#e8861c"))], x=0, y=0)
    P.monitor("الأزواج", 5); P.monitor("المحاولات", 32)
    for n in ("الأولى", "زوج الأولى", "قفل"): P.monitor(n, 60, False)
    P.finish(music)

# ------------------------------------------------------------------ 3) RAPIDITÉ : taupe (cible / leurre)
def whack_game(gid, target, decoy, bg_lieu, music="aventure", secs=30):
    P = Proj(gid); sb = P.stage
    P.stage_costumes.append(P.costume("fond", art.art_svg("l", bg_lieu), 240, 180))
    sco, si = P.V("النقاط"); tm, ti = P.V("الوقت"); on, oi = P.V("جارية")
    pop, bad = P.sfx("pop"), P.sfx("echec")
    for hatname in ("flag", "إعادة"):
        hat = sb.hat_flag() if hatname == "flag" else P.hat(sb, "إعادة")
        sb.script(hat, sb.setv(sco, si, 0), sb.setv(tm, ti, secs), sb.setv(on, oi, 1), P.bc(sb, "ابدأ"),
                  sb.repeat(secs, sb.wait(1), sb.chg(tm, ti, -1)), sb.setv(on, oi, 0), P.bc(sb, "نهاية"), y=0 if hatname == "flag" else 300)
    def critter(name, spec, good, y0):
        b = B(); kind, key, size = spec; svg = art.art_svg(kind, key)
        spawn = b.forever_(b.gotoxy_(b.R(b.rand(b.N(-190), b.N(190))), b.R(b.rand(b.N(-90), b.N(110)))), b.show(), b.wait(0.9 if good else 1.1), b.hide(), b.wait(0.35 if good else 0.8))
        b.script(P.hat(b, "ابدأ"), b.hide(), spawn, y=0)
        b.script(P.hat(b, "نهاية"), b.stop_other(), b.hide(), y=160)
        click = [b.chg(sco, si, 1 if good else -1), b.play(pop["name"] if good else bad["name"]), b.hide()]
        b.script(b.when_clicked(), b.if_(b.eq(b.R(b.var(on, oi)), b.N(1)), *click), y=320)
        P.sprite(name, b, [P.costume(name, svg)], [pop, bad], size=size, flip=True)
    critter("الهدف", target, True, 0); critter("الفخ", decoy, False, 0)
    eb = B()
    eb.script(P.hat(eb, "نهاية"), eb.show(), eb.say_(eb.join(eb.S("انتهى الوقت! نقاطك: "), eb.join(eb.RS(eb.var(sco, si)), eb.S("  (اضغط للإعادة)")))), y=0)
    eb.script(P.hat(eb, "ابدأ"), eb.hide(), eb.say_(eb.S("")), y=160)
    eb.script(eb.when_clicked(), P.bc(eb, "إعادة"), y=320)
    P.sprite("النهاية", eb, [P.costume("نهاية", card(300, 80, ["انتهى الوقت"], "#fff3c4", size=26, stroke="#e8861c"))], x=0, y=0)
    P.monitor("النقاط", 5); P.monitor("الوقت", 32); P.monitor("جارية", 59, False)
    P.finish(music)

# ------------------------------------------------------------------ 4) TOUCHES : éviter les obstacles
def dodge_game(gid, hero, obstacle, bg_lieu, music="aventure"):
    P = Proj(gid); sb = P.stage
    P.stage_costumes.append(P.costume("fond", art.art_svg("l", bg_lieu), 240, 180))
    sco, si = P.V("النقاط"); lv, lvi = P.V("الأرواح"); sp, spi = P.V("السرعة")
    ouch = P.sfx("boing")
    hb = B(); hkind, hkey, hsize = hero; hsvg = art.art_svg(hkind, hkey)
    left, right = hb.key("left arrow"), hb.key("right arrow")
    loop = hb.forever_(hb.if_(left, hb.chx(hb.N(-11)), hb.add("motion_pointindirection", inputs={"DIRECTION": [1, [8, "-90"]]})),
                       hb.if_(right, hb.chx(hb.N(11)), hb.add("motion_pointindirection", inputs={"DIRECTION": [1, [8, "90"]]})))
    clamp = [hb.if_(hb.gt(hb.R(hb.xpos()), hb.N(215)), hb.setx(hb.N(215))), hb.if_(hb.lt(hb.R(hb.xpos()), hb.N(-215)), hb.setx(hb.N(-215)))]
    loop = hb.forever_(hb.if_(left, hb.chx(hb.N(-11)), hb.add("motion_pointindirection", inputs={"DIRECTION": [1, [8, "-90"]]})),
                       hb.if_(right, hb.chx(hb.N(11)), hb.add("motion_pointindirection", inputs={"DIRECTION": [1, [8, "90"]]})), *clamp)
    hb.script(hb.hat_flag(), hb.size(hsize), hb.gotoxy_(hb.N(0), hb.N(-125)), hb.show(), loop, y=0)
    hb.script(hb.hat_flag(), hb.sayfor(hb.S("استعمل السهمين ← → لتتفادى الصخور"), 4), y=300)
    P.sprite("البطل", hb, [P.costume("بطل", hsvg)], x=0, y=-125, size=hsize, visible=True, flip=True)
    ob = B(); okind, okey, osize = obstacle; osvg = art.art_svg(okind, okey)
    def go_top():
        return ob.gotoxy_(ob.R(ob.rand(ob.N(-200), ob.N(200))), ob.N(190))
    fall = ob.chy(ob.R(ob.sub_(ob.N(0), ob.R(ob.var(sp, spi)))))
    menu = ob.add("sensing_of_object_menu", fields={"OBJECT": ["البطل", None]}, shadow=True)
    hero_x = ob.add("sensing_of", fields={"PROPERTY": ["x position", None]}, inputs={"OBJECT": [1, menu]})
    diff = ob.sub_(ob.R(ob.xpos()), ob.R(hero_x)); ab = ob.absv(ob.R(diff))
    near = ob.lt(ob.R(ab), ob.N(48))
    c_hit = ob.if_(near, ob.if_(ob.lt(ob.R(ob.ypos()), ob.N(-95)), ob.chg(lv, lvi, -1), ob.play(ouch["name"]), go_top()))
    c_pass = ob.if_(ob.lt(ob.R(ob.ypos()), ob.N(-170)), ob.chg(sco, si, 1), ob.chg(sp, spi, 0.15), go_top())
    c_end = ob.if_(ob.lt(ob.R(ob.var(lv, lvi)), ob.N(1)), ob.sayfor(ob.join(ob.S("انتهت اللعبة! نقاطك: "), ob.RS(ob.var(sco, si))), 3), ob.stop_all())
    ob.script(ob.hat_flag(), ob.setv(sco, si, 0), ob.setv(lv, lvi, 3), ob.setv(sp, spi, 3), ob.size(osize), go_top(), ob.show(), ob.forever_(fall, c_hit, c_pass, c_end), y=0)
    P.sprite("العقبة", ob, [P.costume("عقبة", osvg)], [ouch], x=0, y=180, size=osize)
    P.monitor("النقاط", 5); P.monitor("الأرواح", 32); P.monitor("السرعة", 59, False)
    P.finish(music)

# ------------------------------------------------------------------ 5) CALCUL : réponses tapées
def math_game(gid, op, bg=("#fff1d6", "#ffe0a8"), music="joyeuse", n=10):
    P = Proj(gid); sb = P.stage
    P.stage_costumes.append(P.costume("fond", bg_svg(*bg), 240, 180))
    a, ai = P.V("أ"); b_, bi = P.V("ب"); sco, si = P.V("النقاط"); k, ki = P.V("السؤال")
    ding, bad = P.sfx("ding"), P.sfx("echec")
    hb = B()
    if op == "+": rule = [hb.setv(a, ai, hb.R(hb.rand(hb.N(1), hb.N(20)))), hb.setv(b_, bi, hb.R(hb.rand(hb.N(1), hb.N(20))))]; res = lambda: hb.add_(hb.R(hb.var(a, ai)), hb.R(hb.var(b_, bi))); sign = " + "
    elif op == "-": rule = [hb.setv(b_, bi, hb.R(hb.rand(hb.N(1), hb.N(15)))), hb.setv(a, ai, hb.R(hb.add_(hb.R(hb.var(b_, bi)), hb.R(hb.rand(hb.N(0), hb.N(15))))))]; res = lambda: hb.sub_(hb.R(hb.var(a, ai)), hb.R(hb.var(b_, bi))); sign = " - "
    else: rule = [hb.setv(a, ai, hb.R(hb.rand(hb.N(2), hb.N(10)))), hb.setv(b_, bi, hb.R(hb.rand(hb.N(2), hb.N(10))))]; res = lambda: hb.mul_(hb.R(hb.var(a, ai)), hb.R(hb.var(b_, bi))); sign = " × "
    question = hb.join(hb.S("كم ناتج "), hb.join(hb.RS(hb.var(a, ai)), hb.join(hb.S(sign), hb.join(hb.RS(hb.var(b_, bi)), hb.S(" ؟")))))
    good = [hb.chg(sco, si, 1), hb.play(ding["name"]), hb.sayfor(hb.S("أحسنت!"), 1)]
    bad_ = [hb.play(bad["name"]), hb.sayfor(hb.join(hb.S("الجواب الصحيح: "), hb.RS(res())), 2)]
    loop = hb.repeat(n, *rule, hb.chg(k, ki, 1), hb.ask(question), hb.ifelse(hb.eq(hb.R(hb.answer()), hb.R(res())), good, bad_))
    hb.script(hb.hat_flag(), hb.setv(sco, si, 0), hb.setv(k, ki, 0), hb.show(), hb.sayfor(hb.S(f"سأطرح عليك {n} أسئلة. اكتب الجواب ثم اضغط Enter"), 3), loop,
              hb.say_(hb.join(hb.S("انتهت اللعبة! نتيجتك: "), hb.join(hb.RS(hb.var(sco, si)), hb.S(f" من {n}")))), y=0)
    svg = art.art_svg("p", "maitresse")
    P.sprite("المعلمة", hb, [P.costume("معلمة", svg)], x=-110, y=-35, size=85, visible=True)
    P.monitor("النقاط", 5); P.monitor("السؤال", 32)
    P.finish(music)

# ------------------------------------------------------------------ 6) Devine le nombre
def guess_game(gid, bg=("#e6f4ff", "#bcdcff"), music="mystere"):
    P = Proj(gid); sb = P.stage
    P.stage_costumes.append(P.costume("fond", bg_svg(*bg), 240, 180))
    sec, sei = P.V("الرقم السري"); tr, tri = P.V("المحاولات")
    ding = P.sfx("ding"); hb = B()
    ans = lambda: hb.R(hb.answer()); secv = lambda: hb.R(hb.var(sec, sei))
    again = [hb.chg(tr, tri, 1),
             hb.ifelse(hb.lt(ans(), secv()), [hb.sayfor(hb.S("أكبر! جرّب رقما أكبر"), 1.2)], [hb.sayfor(hb.S("أصغر! جرّب رقما أصغر"), 1.2)]),
             hb.ask(hb.S("خمّن الرقم (بين 1 و 100)")), ]
    hb.script(hb.hat_flag(), hb.setv(sec, sei, hb.R(hb.rand(hb.N(1), hb.N(100)))), hb.setv(tr, tri, 1), hb.show(),
              hb.sayfor(hb.S("فكّرت في رقم بين 1 و 100. هل تخمّنه؟"), 2.5), hb.ask(hb.S("خمّن الرقم (بين 1 و 100)")),
              hb.until(hb.eq(ans(), secv()), *again),
              hb.play(ding["name"]), hb.say_(hb.join(hb.S("أحسنت! وجدت الرقم "), hb.join(hb.RS(hb.var(sec, sei)), hb.join(hb.S(" بعد "), hb.join(hb.RS(hb.var(tr, tri)), hb.S(" محاولات")))))), y=0)
    P.sprite("المفكّر", hb, [P.costume("مفكر", art.art_svg("p", "maitre"))], [ding], x=-110, y=-35, size=85, visible=True)
    P.monitor("المحاولات", 5); P.monitor("الرقم السري", 32, False)
    P.finish(music)

# ------------------------------------------------------------------ définitions des jeux
LETTERS = list("ابتثجحخدذرزسشصضطظعغفقكلمنهوي")
ANIM_AR = [("loup", "ذئب", "ذ", "loup"), ("lion", "أسد", "أ", "lion"), ("lievre", "أرنب", "أ", "lièvre"), ("grenouille", "ضفدع", "ض", "grenouille"), ("chameau", "جمل", "ج", "chameau"),
           ("cheval", "حصان", "ح", "cheval"), ("mouton", "خروف", "خ", "mouton"), ("cochon", "خنزير", "خ", "cochon"), ("canard", "بطة", "ب", "canard"), ("cygne", "بجعة", "ب", "cygne"),
           ("souris", "فأر", "ف", "souris"), ("renard", "ثعلب", "ث", "renard"), ("corbeau", "غراب", "غ", "corbeau"), ("tortue", "سلحفاة", "س", "tortue"), ("ane", "حمار", "ح", "âne"),
           ("chat", "قطة", "ق", "chat"), ("oiseau", "عصفور", "ع", "oiseau"), ("poule", "دجاجة", "د", "poule"), ("chien", "كلب", "ك", "chien"), ("poisson", "سمكة", "س", "poisson")]
def three(correct, pool):
    d = [x for x in pool if x != correct]; RND.shuffle(d); opts = [correct] + d[:2]; RND.shuffle(opts); return opts, opts.index(correct) + 1

def q_letters():
    qs = []
    for key, ar, first, fr in RND.sample(ANIM_AR, 10):
        opts, ans = three(first, LETTERS)
        qs.append({"lines": [ar, "ما الحرف الأول؟"], "art": ("a", key), "opts": opts, "ans": ans})
    return qs
def q_vocab():
    qs = []; frs = [x[3] for x in ANIM_AR]
    for key, ar, first, fr in RND.sample(ANIM_AR, 10):
        opts, ans = three(fr, frs)
        qs.append({"lines": [ar, "كيف نقولها بالفرنسية؟"], "art": ("a", key), "opts": opts, "ans": ans})
    return qs
COLORS = [("أحمر", "Rouge", "#d93a3a"), ("أزرق", "Bleu", "#2f6fd6"), ("أخضر", "Vert", "#3aa04a"), ("أصفر", "Jaune", "#f2d02e"), ("برتقالي", "Orange", "#f08a1e"),
          ("بنفسجي", "Violet", "#8a4fd0"), ("وردي", "Rose", "#f08ab8"), ("أسود", "Noir", "#222222"), ("بني", "Marron", "#8a5a2a"), ("رمادي", "Gris", "#8a8f99")]
def q_colors():
    qs = []
    for ar, fr, hx in RND.sample(COLORS, 10):
        others = [c for c in COLORS if c[0] != ar]; RND.shuffle(others); opts = [(ar, fr)] + [(c[0], c[1]) for c in others[:2]]; RND.shuffle(opts)
        ans = [o[0] for o in opts].index(ar) + 1
        circ = f'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="{hx}" stroke="#333" stroke-width="4"/></svg>'
        qs.append({"lines": ["ما اسم هذا اللون؟"], "art_svg": circ, "art_w": 110, "opts": [[o[0], o[1]] for o in opts], "ans": ans})
    return qs
def counting_svg(kind, key, n):
    cells = "".join(nest(art.art_svg(kind, key), 8 + (i % 5) * 64, 6 + (i // 5) * 64, 60, 60) for i in range(n))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="330" height="140" viewBox="0 0 330 140">{cells}</svg>'
def q_counting():
    qs = []; objs = [("d", "pomme", "التفاح"), ("d", "etoile", "النجوم"), ("a", "poisson", "الأسماك"), ("d", "oeuf", "البيض"), ("d", "fromage", "قطع الجبن")]
    for i in range(10):
        n = RND.randint(1, 9); kind, key, name = objs[i % len(objs)]; opts, ans = three(n, list(range(1, 10)))
        qs.append({"lines": [f"كم عدد {name}؟"], "art_svg": counting_svg(kind, key, n), "art_mode": "top", "h": 180, "opts": [str(o) for o in opts], "ans": ans})
    return qs
STORY_Q = [("من هي التي فقدت حذاءها في الحفلة؟", ["سندريلا", "الجنية", "زوجة الأب"], 1), ("ماذا قال علي بابا ليفتح باب المغارة؟", ["افتح يا سمسم", "افتح يا شعير", "افتح يا ذهب"], 1),
           ("ماذا حمل جحا وابنه فوق الجسر؟", ["الحمار", "الذهب", "الحطب"], 1), ("من فاز في السباق؟", ["الأرنب", "السلحفاة", "الثعلب"], 2), ("ماذا سقط من فم الغراب؟", ["الخبز", "الجبن", "الفاكهة"], 2),
           ("من أخرج الكرة الذهبية من البئر؟", ["الضفدع", "الأمير", "الملك"], 1), ("من ساعد الأسد وهو في الشبكة؟", ["الفأر", "الذئب", "الصياد"], 1), ("من بنى بيته من الآجر؟", ["الخنزير الأول", "الخنزير الثاني", "الخنزير الثالث"], 3),
           ("ماذا كان الراعي يصرخ كذبا؟", ["الذئب! الذئب!", "النجدة!", "تعالوا إلى الحفلة!"], 1), ("إلى ماذا تحوّلت البطة القبيحة؟", ["دجاجة", "بجعة", "إوزة"], 2)]
def q_stories():
    return [{"lines": wrap(t, 24), "art": None, "opts": o, "ans": a} for t, o, a in STORY_Q]

def mc_build(gid, qs, layout, **kw):
    # prise en charge d'images SVG brutes (couleurs, comptage)
    for it in qs:
        if "art_svg" in it: it["_svg"] = it["art_svg"]
    # patch : mc_game lit it["art"], ici on gère aussi art_svg
    return mc_game(gid, qs, layout, **kw)

GAMES = [
 # (id, catégorie, titre ar, titre fr, consigne ar, consigne fr, couverture(symbole, couleurs, illustrations), fabrication)
 ("lettres", "quiz", "الحرف الأول", "La première lettre", "انظر إلى الصورة واختر الحرف الذي تبدأ به الكلمة.", "Regarde l'image et choisis la lettre par laquelle commence le mot.", ("أ ب ت", "#fff1d6", [("a", "lion"), ("a", "loup")]), lambda g: mc_build(g, q_letters(), "row", bg=("#fff1d6", "#ffe0a8"))),
 ("francais", "quiz", "كيف نقولها بالفرنسية؟", "Comment le dire en français ?", "اختر الكلمة الفرنسية المناسبة لاسم الحيوان.", "Choisis le mot français qui correspond au nom de l'animal.", ("FR", "#e3ecff", [("a", "cochon"), ("a", "canard")]), lambda g: mc_build(g, q_vocab(), "row", bg=("#e3ecff", "#c4d6ff"))),
 ("couleurs", "quiz", "الألوان", "Les couleurs", "ما اسم اللون؟ اختر الإجابة الصحيحة بالعربية والفرنسية.", "Quel est le nom de la couleur ? Choisis la bonne réponse en arabe et en français.", ("ألوان", "#ffe7f0", [("d", "fleurs"), ("d", "papillon" if False else "etoile")]), lambda g: mc_build(g, q_colors(), "row", bg=("#ffe7f0", "#ffcfe3"))),
 ("comptage", "quiz", "كم عددها؟", "Combien y en a-t-il ?", "عُدّ الأشياء في الصورة واختر الرقم الصحيح.", "Compte les objets de l'image et choisis le bon nombre.", ("١ ٢ ٣", "#e6f7ea", [("d", "pomme"), ("d", "oeuf")]), lambda g: mc_build(g, q_counting(), "row", bg=("#e6f7ea", "#c9ecd1"))),
 ("contes", "quiz", "اختبر معلوماتك عن القصص", "Teste tes connaissances sur les contes", "عشرة أسئلة عن القصص التي قرأتها. اختر الجواب الصحيح.", "Dix questions sur les contes que tu as lus. Choisis la bonne réponse.", ("؟", "#efe6ff", [("p", "laila"), ("a", "loup")]), lambda g: mc_build(g, q_stories(), "col", bg=("#efe6ff", "#d8c8ff"))),
 ("addition", "math", "الجمع", "L'addition", "اكتب ناتج الجمع ثم اضغط Enter. عشرة أسئلة.", "Écris le résultat de l'addition puis appuie sur Entrée. Dix questions.", ("٣ + ٤", "#fff1d6", [("p", "maitresse"), ("d", "pomme")]), lambda g: math_game(g, "+")),
 ("soustraction", "math", "الطرح", "La soustraction", "اكتب ناتج الطرح ثم اضغط Enter. عشرة أسئلة.", "Écris le résultat de la soustraction puis appuie sur Entrée. Dix questions.", ("٩ − ٤", "#ffe9d6", [("p", "maitresse"), ("d", "pain")]), lambda g: math_game(g, "-")),
 ("multiplication", "math", "جدول الضرب", "La table de multiplication", "اكتب ناتج الضرب ثم اضغط Enter. عشرة أسئلة.", "Écris le résultat de la multiplication puis appuie sur Entrée. Dix questions.", ("٦ × ٧", "#e9e6ff", [("p", "maitresse"), ("d", "etoile")]), lambda g: math_game(g, "*")),
 ("devine", "math", "خمّن الرقم", "Devine le nombre", "فكّرتُ في رقم بين 1 و100. خمّنه، وسأقول لك أكبر أم أصغر.", "J'ai pensé à un nombre entre 1 et 100. Devine-le : je te dirai plus grand ou plus petit.", ("؟ ١٠٠", "#e6f4ff", [("p", "maitre"), ("d", "etoile")]), lambda g: guess_game(g)),
 ("memoire_animaux", "memory", "ذاكرة الحيوانات", "Mémoire des animaux", "اقلب بطاقتين وابحث عن الأزواج المتشابهة.", "Retourne deux cartes et trouve les paires identiques.", ("؟ ؟", "#e9f7ea", [("a", "lion"), ("a", "tortue")]), lambda g: memory_game(g, [("a", "loup"), ("a", "lion"), ("a", "lievre"), ("a", "grenouille"), ("a", "cygne"), ("a", "cochon")])),
 ("memoire_personnages", "memory", "ذاكرة شخصيات القصص", "Mémoire des personnages", "اقلب بطاقتين وابحث عن أزواج شخصيات القصص.", "Retourne deux cartes et trouve les paires de personnages des contes.", ("؟ ؟", "#fdeaf2", [("p", "princesse"), ("p", "sindbad")]), lambda g: memory_game(g, [("p", "laila"), ("p", "djeha"), ("p", "ali_baba"), ("p", "sindbad"), ("p", "princesse"), ("p", "berger")], bg=("#fdeaf2", "#f9cfe1"))),
 ("taupe_loup", "reflex", "اصطد الذئب", "Attrape le loup", "اضغط على الذئب بسرعة، ولا تضغط على الخروف! لديك 30 ثانية.", "Clique vite sur le loup, mais pas sur le mouton ! Tu as 30 secondes.", ("!", "#e1f3d8", [("a", "loup"), ("a", "mouton")]), lambda g: whack_game(g, ("a", "loup", 50), ("a", "mouton", 50), "colline_pature")),
 ("taupe_renard", "reflex", "اصطد الثعلب", "Attrape le renard", "اضغط على الثعلب بسرعة، ولا تضغط على الدجاجة! لديك 30 ثانية.", "Clique vite sur le renard, mais pas sur la poule ! Tu as 30 secondes.", ("!", "#fbe9d0", [("a", "renard"), ("a", "poule")]), lambda g: whack_game(g, ("a", "renard", 50), ("a", "poule", 50), "foret")),
 ("rochers", "reflex", "تفادى الصخور", "Évite les rochers", "حرّك الأرنب بالسهمين ← → لتتفادى الصخور. لديك ثلاث أرواح.", "Déplace le lièvre avec les flèches ← → pour éviter les rochers. Tu as trois vies.", ("← →", "#e1f3d8", [("a", "lievre"), ("d", "rocher")]), lambda g: dodge_game(g, ("a", "lievre", 50), ("d", "rocher", 50), "piste_course")),
 ("pierres_cygne", "reflex", "الهروب من الثلج", "Fuis la neige", "حرّك البطة بالسهمين ← → لتتفادى كرات الثلج.", "Déplace le canard avec les flèches ← → pour éviter les boules de neige.", ("← →", "#e3eef8", [("a", "canard"), ("d", "bonhomme_neige")]), lambda g: dodge_game(g, ("a", "canard", 50), ("d", "bonhomme_neige", 50), "etang_hiver")),
]
CATS = {"quiz": ("أسئلة وأجوبة", "Questions et réponses"), "math": ("حساب وأرقام", "Calcul et nombres"), "memory": ("ذاكرة", "Mémoire"), "reflex": ("السرعة والدقة", "Rapidité et précision")}

def cover(symbol, color, items, path):
    body = f'<rect width="480" height="270" fill="{color}"/><rect y="190" width="480" height="80" fill="#000" fill-opacity="0.06"/>'
    for i, (k, key) in enumerate(items): body += nest(art.art_svg(k, key), 20 + i * 250, 40, 200, 190)
    body += f'<text x="240" y="70" text-anchor="middle" font-family="Sans Serif" font-size="56" font-weight="bold" fill="#1f4aa8" stroke="#fff" stroke-width="6" paint-order="stroke">{escape(symbol)}</text>'
    open(path, "w", encoding="utf-8").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="270" viewBox="0 0 480 270">{body}</svg>')

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); cov = os.path.join(OUT, "couvertures"); os.makedirs(cov, exist_ok=True)
    meta = []
    for gid, cat, tar, tfr, har, hfr, (sym, col, items), fn in GAMES:
        fn(gid); cover(sym, col, items, os.path.join(cov, gid + ".svg"))
        meta.append(dict(key=gid, file=f"jeux/jeu_{gid}.sb3", title_ar=tar, title_fr=tfr, how_ar=har, how_fr=hfr, cover=f"jeux/couvertures/{gid}.svg", cat=cat, cat_ar=CATS[cat][0], cat_fr=CATS[cat][1]))
    json.dump(meta, open(os.path.join(HERE, "jeux2_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("jeux éducatifs :", len(meta))
