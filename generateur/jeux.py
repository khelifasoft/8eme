"""Génère un petit jeu Scratch « attrape les objets » pour chaque conte (jeux/*.sb3).
Usage : python3 generateur/jeux.py jeux"""
import sys, os, json, zipfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scratch as sc, scratch_art as art
OUT = sys.argv[1] if len(sys.argv) > 1 else "jeux"
P_, A_, D_ = "p", "a", "d"
# conte -> (joueur, objet qui tombe, effet sonore, fond, titre arabe, titre français, consigne arabe, consigne française)
GAMES = {
 "cinderella": ((P_, "cendrillon_bal", 42), (D_, "etoile", 45), "magie", "salle_bal", "التقطي النجوم السحرية", "Attrape les étoiles magiques", "حرّك الفأرة لتلتقط النجوم قبل منتصف الليل!", "Déplace la souris pour attraper les étoiles avant minuit !"),
 "layla": ((P_, "laila", 42), (D_, "pomme", 45), "pop", "foret", "اجمعي التفاح لجدتك", "Ramasse les pommes pour grand-mère", "حرّك الفأرة لتجمع التفاح في السلة.", "Déplace la souris pour ramasser les pommes."),
 "djeha": ((P_, "djeha", 42), (D_, "pieces", 40), "piece", "marche", "اجمع القطع الذهبية", "Ramasse les pièces d'or", "حرّك الفأرة لتلتقط القطع قبل أن تسقط.", "Déplace la souris pour attraper les pièces."),
 "alibaba": ((P_, "ali_baba", 42), (D_, "sac_or", 40), "piece", "grotte_interieur", "كنز المغارة", "Le trésor de la grotte", "التقط أكياس الذهب قبل أن تصل إلى الأرض.", "Attrape les sacs d'or avant qu'ils touchent le sol."),
 "sindbad": ((P_, "sindbad", 38), (A_, "poisson", 45), "plouf", "mer", "اصطد الأسماك", "Attrape les poissons", "حرّك الفأرة لتلتقط الأسماك.", "Déplace la souris pour attraper les poissons."),
 "crow": ((A_, "corbeau", 50), (D_, "fromage", 35), "ding", "foret", "التقط الجبن", "Attrape le fromage", "ساعد الغراب على التقاط قطع الجبن.", "Aide le corbeau à attraper les morceaux de fromage."),
 "hare": ((A_, "lievre", 55), (D_, "pomme", 40), "pop", "piste_course", "الأرنب الجائع", "Le lièvre gourmand", "حرّك الفأرة ليلتقط الأرنب الفواكه.", "Déplace la souris pour que le lièvre attrape les fruits."),
 "lion": ((A_, "lion", 60), (D_, "pain", 40), "ding", "foret", "غذاء الأسد", "Le repas du lion", "ساعد الأسد على التقاط الطعام.", "Aide le lion à attraper la nourriture."),
 "frog": ((A_, "grenouille", 45), (D_, "etoile", 40), "boing", "jardin_puits", "الضفدع والنجوم", "La grenouille et les étoiles", "قفز الضفدع ليلتقط النجوم.", "Fais sauter la grenouille pour attraper les étoiles."),
 "shepherd": ((P_, "berger", 42), (D_, "foin", 40), "pop", "colline_pature", "علف الأغنام", "Le foin des moutons", "اجمع القش لإطعام الأغنام.", "Ramasse le foin pour nourrir les moutons."),
 "pigs": ((A_, "cochon", 45), (D_, "pomme", 40), "cochon", "colline_pature", "الخنزير يلتقط التفاح", "Le cochon attrape les pommes", "حرّك الفأرة ليلتقط الخنزير التفاح.", "Déplace la souris pour que le cochon attrape les pommes."),
 "duckling": ((A_, "canard", 50), (D_, "pain", 40), "canard", "etang_ferme", "خبز للبطة", "Du pain pour le canard", "التقط قطع الخبز قبل أن تسقط في الماء.", "Attrape les morceaux de pain avant qu'ils tombent à l'eau."),
}

def build(key):
    (pk, pkey, psize), (ik, ikey, isize), fx, back, tar, tfr, har, hfr = GAMES[key]
    zf = zipfile.ZipFile(os.path.join(OUT, f"jeu_{key}.sb3"), "w", zipfile.ZIP_DEFLATED); store = set()
    VARS = {"score": "النقاط", "lives": "الأرواح", "speed": "السرعة"}
    vid = {k: f"var_{k}" for k in VARS}
    def var_block(b, k): return b.add("data_variable", fields={"VARIABLE": [VARS[k], vid[k]]})
    def setv(b, k, v): return b.add("data_setvariableto", fields={"VARIABLE": [VARS[k], vid[k]]}, inputs={"VALUE": [1, [10, str(v)]]})
    def chgv(b, k, v): return b.add("data_changevariableby", fields={"VARIABLE": [VARS[k], vid[k]]}, inputs={"VALUE": [1, [4, str(v)]]})
    def asset_of(svg): return sc.asset(zf, svg, store)
    # fond
    bg = art.art_svg("l", back); md = asset_of(bg)
    stage_b = sc.Blocks()
    stage = {"isStage": True, "name": "Stage", "variables": {vid[k]: [VARS[k], 0] for k in VARS}, "lists": {}, "broadcasts": {}, "blocks": stage_b.b, "comments": {},
             "currentCostume": 0, "costumes": [{"assetId": md, "name": "fond", "md5ext": md + ".svg", "dataFormat": "svg", "rotationCenterX": 240, "rotationCenterY": 180}],
             "sounds": [], "volume": 100, "layerOrder": 0, "tempo": 60, "videoTransparency": 50, "videoState": "on", "textToSpeechLanguage": None}
    # musique douce
    music = art.MUSIC.get(key, "joyeuse"); ms = sc.sfx(zf, store, music); stage["sounds"].append(ms)
    mids = [stage_b.hat_flag(), stage_b.volume(15)]; mids.append(stage_b.forever(stage_b.play_wait(ms["name"]))); stage_b.chain(mids, 0, 0)
    # joueur
    pb = sc.Blocks(); psvg = art.art_svg(pk, pkey); pw, ph = art.svg_size(psvg); pmd = asset_of(psvg)
    mx = pb.add("sensing_mousex")
    goto = pb.add("motion_gotoxy", inputs={"X": [3, mx, [4, "0"]], "Y": pb.num(-125)})
    fe = pb.forever(goto)
    ids = [pb.hat_flag(), pb.size(psize), pb.goto(0, -125), pb.show(), fe]
    pb.chain(ids, 0, 0)
    pb.chain([pb.hat_flag(), pb.say(har, 4)], 300, 0)
    for i in ids: 
        for v in pb.b[i]["inputs"].values():
            pass
    pb.b[goto]["parent"] = fe; pb.b[mx]["parent"] = goto
    player = {"isStage": False, "name": "اللاعب", "variables": {}, "lists": {}, "broadcasts": {}, "blocks": pb.b, "comments": {}, "currentCostume": 0,
              "costumes": [{"assetId": pmd, "name": "اللاعب", "md5ext": pmd + ".svg", "dataFormat": "svg", "rotationCenterX": pw // 2, "rotationCenterY": ph // 2}],
              "sounds": [], "volume": 100, "layerOrder": 1, "visible": True, "x": 0, "y": -125, "size": psize, "direction": 90, "draggable": False, "rotationStyle": "left-right"}
    # objet qui tombe
    b = sc.Blocks(); isvg = art.art_svg(ik, ikey); iw, ih = art.svg_size(isvg); imd = asset_of(isvg)
    snd = sc.sfx(zf, store, fx)
    def num_in(x): return [1, [4, str(x)]]
    def rnd_x():  # position x aléatoire
        return b.add("operator_random", inputs={"FROM": num_in(-200), "TO": num_in(200)})
    def go_top():
        r = rnd_x(); g = b.add("motion_gotoxy", inputs={"X": [3, r, [4, "0"]], "Y": num_in(180)}); b.b[r]["parent"] = g; return g
    # 1) chute : y diminue de « vitesse »
    spd = var_block(b, "speed"); sub = b.add("operator_subtract", inputs={"NUM1": num_in(0), "NUM2": [3, spd, [4, "0"]]}); b.b[spd]["parent"] = sub
    fall = b.add("motion_changeyby", inputs={"DY": [3, sub, [4, "0"]]}); b.b[sub]["parent"] = fall
    # 2) attrapé : |x - souris| < 50 et y < -90
    ix = b.add("motion_xposition"); mx2 = b.add("sensing_mousex")
    diff = b.add("operator_subtract", inputs={"NUM1": [3, ix, [4, "0"]], "NUM2": [3, mx2, [4, "0"]]}); b.b[ix]["parent"] = diff; b.b[mx2]["parent"] = diff
    ab = b.add("operator_mathop", fields={"OPERATOR": ["abs", None]}, inputs={"NUM": [3, diff, [4, "0"]]}); b.b[diff]["parent"] = ab
    c1 = b.add("operator_lt", inputs={"OPERAND1": [3, ab, [10, ""]], "OPERAND2": [1, [10, "55"]]}); b.b[ab]["parent"] = c1
    iy = b.add("motion_yposition")
    c2 = b.add("operator_lt", inputs={"OPERAND1": [3, iy, [10, ""]], "OPERAND2": [1, [10, "-90"]]}); b.b[iy]["parent"] = c2
    pl = b.play(snd["name"]); sc1 = chgv(b, "score", 1); sp1 = chgv(b, "speed", 0.25); top1 = go_top()
    for a, c in zip([pl, sc1, sp1, top1], [sc1, sp1, top1, None]):
        if c: b.b[a]["next"] = c; b.b[c]["parent"] = a
    if_low = b.add("control_if", inputs={"CONDITION": [2, c2], "SUBSTACK": [2, pl]}); b.b[c2]["parent"] = if_low; b.b[pl]["parent"] = if_low
    if_catch = b.add("control_if", inputs={"CONDITION": [2, c1], "SUBSTACK": [2, if_low]}); b.b[c1]["parent"] = if_catch; b.b[if_low]["parent"] = if_catch
    # 3) manqué : y < -165
    iy2 = b.add("motion_yposition")
    c3 = b.add("operator_lt", inputs={"OPERAND1": [3, iy2, [10, ""]], "OPERAND2": [1, [10, "-165"]]}); b.b[iy2]["parent"] = c3
    lose = chgv(b, "lives", -1); top2 = go_top(); b.b[lose]["next"] = top2; b.b[top2]["parent"] = lose
    if_miss = b.add("control_if", inputs={"CONDITION": [2, c3], "SUBSTACK": [2, lose]}); b.b[c3]["parent"] = if_miss; b.b[lose]["parent"] = if_miss
    # 4) fin : vies < 1
    lv = var_block(b, "lives")
    c4 = b.add("operator_lt", inputs={"OPERAND1": [3, lv, [10, ""]], "OPERAND2": [1, [10, "1"]]}); b.b[lv]["parent"] = c4
    say_end = b.say("انتهت اللعبة!", 3)
    stop = b.add("control_stop", fields={"STOP_OPTION": ["all", None]}); b.b[stop]["mutation"] = {"tagName": "mutation", "children": [], "hasnext": "false"}
    b.b[say_end]["next"] = stop; b.b[stop]["parent"] = say_end
    if_end = b.add("control_if", inputs={"CONDITION": [2, c4], "SUBSTACK": [2, say_end]}); b.b[c4]["parent"] = if_end; b.b[say_end]["parent"] = if_end
    # enchaînement dans forever
    inner = [fall, if_catch, if_miss, if_end]
    for a, c in zip(inner, inner[1:]): b.b[a]["next"] = c; b.b[c]["parent"] = a
    fv = b.forever(fall)
    start = [b.hat_flag(), setv(b, "score", 0), setv(b, "lives", 3), setv(b, "speed", 3), b.size(isize), go_top(), b.show(), fv]
    b.chain(start, 0, 0)
    item = {"isStage": False, "name": "الشيء", "variables": {}, "lists": {}, "broadcasts": {}, "blocks": b.b, "comments": {}, "currentCostume": 0,
            "costumes": [{"assetId": imd, "name": "الشيء", "md5ext": imd + ".svg", "dataFormat": "svg", "rotationCenterX": iw // 2, "rotationCenterY": ih // 2}],
            "sounds": [snd], "volume": 100, "layerOrder": 2, "visible": False, "x": 0, "y": 180, "size": isize, "direction": 90, "draggable": False, "rotationStyle": "don't rotate"}
    mon = lambda k, y: {"id": vid[k], "mode": "default", "opcode": "data_variable", "params": {"VARIABLE": VARS[k]}, "spriteName": None, "value": 0, "width": 0, "height": 0, "x": 5, "y": y, "visible": k != "speed", "sliderMin": 0, "sliderMax": 100, "isDiscrete": True}
    proj = {"targets": [stage, player, item], "monitors": [mon("score", 5), mon("lives", 32), mon("speed", 59)], "extensions": [],
            "meta": {"semver": "3.0.0", "vm": "0.2.0", "agent": "Mozilla/5.0"}}
    zf.writestr("project.json", json.dumps(proj, ensure_ascii=False)); zf.close()

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    meta = []
    for k, g in GAMES.items():
        build(k)
        meta.append(dict(key=k, file=f"jeux/jeu_{k}.sb3", title_ar=g[4], title_fr=g[5], how_ar=g[6], how_fr=g[7], cover=f"bibliotheque/lieux/{g[3]}.svg"))
    json.dump(meta, open(os.path.join(HERE, "jeux_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("jeux :", len(meta))
