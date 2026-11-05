"""Construit la bibliothèque (images, sons, animations) et les paquets de téléchargement.
Usage : python3 generateur/bibliotheque.py   (depuis la racine du dépôt)"""
import os, sys, json, shutil, zipfile, subprocess, wave, tempfile, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import personnages as pe, animaux as an, decors as de, lieux as li, animations as anim, sons
from svgkit import *

B = os.path.join(ROOT, "bibliotheque"); DL = os.path.join(ROOT, "telechargements")
for d in (B, DL): shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
M = []   # manifest des ressources
def out(rel, data, mode="w"):
    p = os.path.join(B, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, mode + ("b" if isinstance(data, bytes) else ""), **({} if isinstance(data, bytes) else {"encoding": "utf-8"})).write(data)
def add(cat, sub, key, label, ext, data, tags=(), fr=""):
    rel = f"{cat}/{sub + '/' if sub else ''}{key}.{ext}"
    out(rel, data); M.append(dict(cat=cat, sub=sub, id=key, label=label, fr=fr, file="bibliotheque/" + rel, ext=ext, tags=list(tags)))

# --- personnages
CAT = pe.catalogue()
for k, (n, kw, tg) in CAT.items(): add("personnages", "", k, n, "svg", pe.render_person(kw), tg)
for k, (n, fn, tg) in an.ANIMAUX.items(): add("animaux", "", k, n, "svg", fn(), tg)
# --- décors (objets) et lieux
for k, (n, fn, tg) in de.OBJETS.items(): add("decors", "", k, n, "svg", de.objet_svg(k), tg)
for k, (n, fn, tg) in li.LIEUX.items(): add("lieux", "", k, n, "svg", li.lieu_svg(k), tg)
# --- costumes : accessoires, tenues, variantes d'histoire
def item_svg(inner): return SVG(200, 170, G(inner, 0, 30))
HATS = [("turban", "عمامة", "#f2f2f2"), ("crown", "تاج", None), ("tiara", "تاج صغير", None), ("hood", "قبّعة ليلى الحمراء", "#c4302b"), ("cap", "قبعة", "#d08a1e"),
        ("fez", "طربوش", "#b32a3a"), ("sailor", "قبعة بحّار", "#1f3a6a"), ("mask", "قناع لص", None), ("bonnet", "قبعة الجدة", None), ("scarf", "حجاب / وشاح", "#e8c15a"), ("helmet", "خوذة", None)]
for k, n, col in HATS:
    back, front = pe._hat(k, col or "#c0392b", "#222")
    add("costumes", "accessoires", "chapeau_" + k, n, "svg", item_svg(back + front), ["cinderella"] if k in ("tiara", "crown") else [])
EXTRAS = [("wand", "عصا سحرية"), ("basket", "سلّة"), ("axe", "فأس"), ("sack", "كيس"), ("whistle", "صفّارة"), ("sword", "سيف"), ("ball", "كرة ذهبية"), ("cane", "عكّاز"), ("bag", "حقيبة")]
for k, n in EXTRAS:
    add("costumes", "accessoires", "objet_" + k, n, "svg", SVG(200, 200, G(pe._extra(k, 0, 0), 60, 110)), [])
add("costumes", "accessoires", "ailes_fee", "أجنحة الجنية", "svg", SVG(200, 140, E(60, 60, 44, 24, "#dff0ff", 3, -30) + E(140, 60, 44, 24, "#dff0ff", 3, 30) + E(66, 96, 32, 16, "#cfe6fa", 3, 24) + E(134, 96, 32, 16, "#cfe6fa", 3, -24) + C(100, 80, 8, "#c9a7f2", 3)), ["cinderella"])
add("costumes", "accessoires", "lunettes", "نظّارات", "svg", SVG(200, 100, C(60, 50, 28, "#dff4ff", 4) + C(140, 50, 28, "#dff4ff", 4) + L(88, 50, 112, 50, OUT, 4) + L(32, 50, 8, 42, OUT, 4) + L(168, 50, 192, 42, OUT, 4)), ["layla"])
add("costumes", "accessoires", "cape_rouge", "عباءة حمراء", "svg", SVG(200, 200, P("M60 30 L140 30 L190 190 L10 190Z", "#c4302b") + L(100, 30, 100, 190, "#8a1a1a", 2) + C(100, 34, 8, "#f1c40f", 2)), [])
add("costumes", "accessoires", "robe_bal", "فستان الحفلة", "svg", SVG(200, 230, P("M70 20 Q100 12 130 20 L190 210 Q100 232 10 210Z", "#8ecbf0") + P("M70 20 Q100 40 130 20", "none", 3) + "".join(C(x, y, 4, "#fff", 1.5) for x, y in [(70, 140), (110, 120), (140, 160), (90, 180), (40, 190)])), ["cinderella"])
add("costumes", "accessoires", "robe_servante", "ثوب الخادمة", "svg", SVG(200, 230, P("M70 20 Q100 12 130 20 L180 210 Q100 226 20 210Z", "#9a8f80") + P("M84 40 L116 40 L124 200 Q100 208 76 200Z", "#e8e2d0")), ["cinderella"])
COL = [("أحمر", "#c0392b"), ("أزرق", "#2980b9"), ("أخضر", "#27ae60"), ("أصفر", "#f1c40f"), ("بنفسجي", "#8e44ad"), ("برتقالي", "#e67e22"), ("وردي", "#e84393"), ("أسود", "#2c2c2c")]
for i, (cn, c) in enumerate(COL):
    add("costumes", "tenues", f"garcon_{i+1}", f"ولد بلباس {cn}", "svg", pe.person(top=c, bottom="#34495e", hair="#4a2a1a"))
    add("costumes", "tenues", f"fille_{i+1}", f"بنت بفستان {cn}", "svg", pe.person(hs="braids", hair="#4a2a1a", dress=c))
    add("costumes", "tenues", f"djellaba_{i+1}", f"رجل بجلباب {cn}", "svg", pe.person(top=c, bottom=c, sleeve=c, hat="turban", hatcol="#f2f2f2", beard="mustache", hair="#222", skin=pe.SKIN[2]))
    add("costumes", "tenues", f"femme_{i+1}", f"امرأة بثوب {cn}", "svg", pe.person(hs="long", hair="#2a2a2a", dress=c, hat="scarf", hatcol="#f2f2f2", skin=pe.SKIN[1]))
# variantes d'histoire (même fichiers que les autres dossiers, référencés)
VARIANTES = [("personnages/cendrillon_servante", "سندريلا خادمة", ["cinderella"]), ("personnages/cendrillon_bal", "سندريلا في الحفلة", ["cinderella"]),
 ("animaux/loup", "الذئب", ["layla"]), ("animaux/loup_grand_mere", "الذئب في ثوب الجدة", ["layla"]), ("animaux/loup_gueule", "الذئب فاتح فمه", ["layla"]),
 ("animaux/grenouille", "الضفدع", ["frog"]), ("animaux/grenouille_saut", "الضفدع يقفز", ["frog"]), ("personnages/prince", "الأمير (بعد التحوّل)", ["frog"]),
 ("animaux/lion", "الأسد", ["lion"]), ("animaux/lion_piege", "الأسد في الشبكة", ["lion"]), ("animaux/lievre", "الأرنب مستيقظ", ["hare"]), ("animaux/lievre_endormi", "الأرنب نائم", ["hare"]),
 ("animaux/corbeau", "الغراب", ["crow"]), ("animaux/corbeau_bec_ouvert", "الغراب فاتح منقاره", ["crow"]), ("decors/porte_fermee", "الباب مغلق", ["alibaba"]), ("decors/porte_ouverte", "الباب مفتوح", ["alibaba"]),
 ("decors/grotte_fermee", "المغارة مغلقة", ["alibaba"]), ("decors/grotte_ouverte", "المغارة مفتوحة", ["alibaba"]), ("decors/ile", "الجزيرة", ["sindbad"]), ("animaux/baleine", "الحوت", ["sindbad"]),
 ("decors/coffre_ferme", "الصندوق مغلق", ["alibaba"]), ("decors/coffre_ouvert", "الصندوق مفتوح", ["alibaba"])]
for rel, n, tg in VARIANTES:
    cat, k = rel.split("/"); src = os.path.join(B, rel + ".svg")
    M.append(dict(cat="costumes", sub="variantes", id="var_" + k, label=n, fr="", file=f"bibliotheque/{rel}.svg", ext="svg", tags=tg))

# --- animations (images successives, importables dans Scratch comme costumes)
ANIM_META = []
for k, (lab, n, fn, tg) in anim.ANIMS.items():
    files = []
    for i in range(n):
        rel = f"animations/{k}/{k}_{i+1}.svg"; out(rel, fn(i, n)); files.append("bibliotheque/" + rel)
    zp = os.path.join(DL, f"anim_{k}.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files: z.write(os.path.join(ROOT, f), os.path.basename(f))
    ANIM_META.append(dict(cat="animations", sub="", id=k, label=lab, fr="", file=files[0], frames=files, fps=(6 if n > 2 else 4), zip=f"telechargements/anim_{k}.zip", ext="svg", tags=tg))
M += ANIM_META

# --- sons
def wavinfo(p):
    w = wave.open(p); d = w.getnframes() / w.getframerate(); w.close(); return round(d, 1)
for k, ar, fr, fn, tg in sons.EFFETS:
    p = os.path.join(B, "sons/effets", k + ".wav"); os.makedirs(os.path.dirname(p), exist_ok=True); sons.save(p, fn())
    M.append(dict(cat="sons", sub="effets", id=k, label=ar, fr=fr, file=f"bibliotheque/sons/effets/{k}.wav", ext="wav", dur=wavinfo(p), tags=tg))
for k, ar, fr, fn, tg in sons.MUSIQUES:
    p = os.path.join(B, "sons/musique", k + ".wav"); os.makedirs(os.path.dirname(p), exist_ok=True); sons.save(p, fn())
    M.append(dict(cat="sons", sub="musique", id=k, label=ar, fr=fr, file=f"bibliotheque/sons/musique/{k}.wav", ext="wav", dur=wavinfo(p), tags=tg))

# voix de synthèse (espeak-ng) : répliques des contes, morales et phrases utiles
src = open(os.path.join(HERE, "scratch.py"), encoding="utf-8").read().split("# ---------- fabrication ----------")[0]
src = src.replace("OUT = sys.argv[1]", "OUT = '.'"); ns = {"__file__": os.path.join(HERE, "scratch.py")}; exec(src, ns)
STORIES = ns["STORIES"]; D = ns["D"]
COMMON = ["مرحبا", "صباح الخير", "مساء الخير", "شكرا", "من فضلك", "عفوا", "نعم", "لا", "هيا بنا", "انتظر", "النجدة", "ما أجمل!", "أنا سعيد", "أنا حزين", "أنا خائف",
 "لا تخف", "أحسنت", "تعال", "اذهب", "ماذا تفعل؟", "من أنت؟", "أين أنت؟", "إلى اللقاء", "الحمد لله", "مبروك", "كان يا ما كان", "وعاشوا في سعادة", "انتهت القصة",
 "المشهد الأول", "المشهد الثاني", "المشهد الثالث", "المشهد الرابع", "المشهد الخامس", "المشهد السادس", "واحد", "اثنان", "ثلاثة", "أربعة", "خمسة", "ستة", "سبعة", "ثمانية", "تسعة", "عشرة"]
VOICES = [(t, []) for t in COMMON]
seen = set(COMMON)
for sk, d in D.items():
    for (bd, steps) in d["scenes"]:
        for st in steps:
            if st[0] == "say" and st[2] not in seen: VOICES.append((st[2], [sk])); seen.add(st[2])
    m = STORIES[sk]["morale"]
    if m not in seen: VOICES.append((m, [sk])); seen.add(m)
if shutil.which("espeak-ng"):
    for i, (t, tg) in enumerate(VOICES, 1):
        p = os.path.join(B, "sons/voix", f"voix_{i:03d}.wav"); os.makedirs(os.path.dirname(p), exist_ok=True)
        subprocess.run(["espeak-ng", "-v", "ar", "-s", "125", "-p", "45", "-w", p, t], check=True, stderr=subprocess.DEVNULL)
        M.append(dict(cat="sons", sub="voix", id=f"voix_{i:03d}", label=t, fr="", file=f"bibliotheque/sons/voix/voix_{i:03d}.wav", ext="wav", dur=wavinfo(p), tags=tg))
else:
    print("espeak-ng absent : pas de voix de synthèse")

# --- paquets .zip
def zipcat(name, cats):
    with zipfile.ZipFile(os.path.join(DL, name), "w", zipfile.ZIP_DEFLATED) as z:
        seen = set()
        for a in M:
            if a["cat"] in cats and a["cat"] != "animations" and a["file"] not in seen:
                seen.add(a["file"]); z.write(os.path.join(ROOT, a["file"]), a["file"].replace("bibliotheque/", ""))
        for a in M:
            if a["cat"] == "animations" and "animations" in cats:
                for f in a["frames"]: z.write(os.path.join(ROOT, f), f.replace("bibliotheque/", ""))
ZIPS = {"lieux": ["lieux"], "decors": ["decors"], "personnages": ["personnages"], "animaux": ["animaux"], "costumes": ["costumes"], "animations": ["animations"]}
for k, c in ZIPS.items(): zipcat(f"{k}.zip", c)
STORY_LIST = []
for sk in D:
    s = STORIES[sk]
    with zipfile.ZipFile(os.path.join(DL, f"histoire_{sk}.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for src_, dst in ((f"word/{sk}.docx", f"{sk}/ورقة_المشروع.docx"), (f"fiches/{sk}.html", f"{sk}/ورقة_المشروع.html"), (f"scratch/{sk}.sb3", f"{sk}/مشروع_سكراتش.sb3")):
            z.write(os.path.join(ROOT, src_), dst)
        seen = set()
        for a in M:
            if sk in a["tags"] and a["file"] not in seen and a["cat"] != "animations":
                seen.add(a["file"]); z.write(os.path.join(ROOT, a["file"]), f"{sk}/موارد/{a['cat']}/{os.path.basename(a['file'])}")
            if sk in a["tags"] and a["cat"] == "animations":
                for f in a["frames"]: z.write(os.path.join(ROOT, f), f"{sk}/موارد/animations/{a['id']}/{os.path.basename(f)}")
    summary = s["summary"].split(".")[0] + "."
    STORY_LIST.append(dict(key=sk, title=s["title"], summary=summary, morale=s["morale"], main=s["main"], accent=s["accent"],
        docx=f"word/{sk}.docx", html=f"fiches/{sk}.html", sb3=f"scratch/{sk}.sb3", pack=f"telechargements/histoire_{sk}.zip",
        n=sum(1 for a in M if sk in a["tags"])))
json.dump(dict(stories=STORY_LIST, assets=M, zips={k: f"telechargements/{k}.zip" for k in ZIPS}), open(os.path.join(HERE, "manifest.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("ressources :", len(M), "| zips :", len(os.listdir(DL)))
