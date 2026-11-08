"""Ressources des jeux (images et sons du projet), prêtes à importer dans Scratch :
jeux/ressources/<jeu>/ + jeux/ressources/ressources-<jeu>.zip + generateur/ressources.json  (dictionnaire jeu -> liste)
Usage : python3 generateur/fiches_ressources.py"""
import os, json, zipfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
GAMES = {
 "catch": dict(sb3="jeu_sindbad.sb3", dir="attrape-poissons", names={  # (lutin, nom) -> (fichier, titre fr, titre ar, type)
   ("Stage", "fond"): ("decor-mer.svg", "Décor : la mer", "الخلفية: البحر", "image"),
   ("اللاعب", "اللاعب"): ("joueur-sindbad.svg", "Joueur : Sindbad", "اللاعب: السندباد", "image"),
   ("الشيء", "الشيء"): ("objet-poisson.svg", "Objet qui tombe : le poisson", "الشيء الساقط: السمكة", "image"),
   ("Stage", "موسيقى البحر"): ("musique-mer.wav", "Musique de fond : la mer", "موسيقى الخلفية: البحر", "son"),
   ("الشيء", "قفزة في الماء"): ("son-plouf.wav", "Son quand on attrape un poisson : plouf", "صوت التقاط السمكة: قفزة في الماء", "son")}),
 "course": dict(sb3="jeu_course.sb3", dir="course", names={
   ("Stage", "fond"): ("decor-route.svg", "Décor : la route", "الخلفية: الطريق", "image"),
   ("الخطوط", "خطوط"): ("lignes-route.svg", "Lignes blanches de la route", "خطوط الطريق البيضاء", "image"),
   ("السيارة", "سيارة"): ("voiture-joueur.svg", "Voiture du joueur", "سيارة اللاعب", "image"),
   ("سيارة معاكسة", "معاكسة"): ("voiture-adverse.svg", "Voiture adverse", "السيارة المعاكسة", "image"),
   ("القلوب", "1"): ("coeurs-1.svg", "Cœurs : 1 vie", "القلوب: روح واحدة", "image"),
   ("القلوب", "2"): ("coeurs-2.svg", "Cœurs : 2 vies", "القلوب: روحان", "image"),
   ("القلوب", "3"): ("coeurs-3.svg", "Cœurs : 3 vies", "القلوب: ثلاثة أرواح", "image"),
   ("Stage", "موسيقى مغامرة"): ("musique-aventure.wav", "Musique de fond : aventure", "موسيقى الخلفية: مغامرة", "son"),
   ("سيارة معاكسة", "نطّة"): ("son-choc.wav", "Son quand on est touché", "صوت الاصطدام", "son")}),
 "saut": dict(sb3="jeu_saut.sb3", dir="saut", names={
   ("Stage", "fond"): ("decor-desert.svg", "Décor : le désert", "الخلفية: الصحراء", "image"),
   ("الجمل", "جمل"): ("chameau.svg", "Le chameau", "الجمل", "image"),
   ("الشجيرة", "شجيرة"): ("buisson.svg", "Le buisson (obstacle)", "الشجيرة (العقبة)", "image"),
   ("القلوب", "1"): ("coeurs-1.svg", "Cœurs : 1 vie", "القلوب: روح واحدة", "image"),
   ("القلوب", "2"): ("coeurs-2.svg", "Cœurs : 2 vies", "القلوب: روحان", "image"),
   ("القلوب", "3"): ("coeurs-3.svg", "Cœurs : 3 vies", "القلوب: ثلاثة أرواح", "image"),
   ("Stage", "موسيقى مغامرة"): ("musique-aventure.wav", "Musique de fond : aventure", "موسيقى الخلفية: مغامرة", "son"),
   ("الشجيرة", "نطّة"): ("son-choc.wav", "Son quand on touche un buisson", "صوت لمس الشجيرة", "son")}),
 "labyrinthe": dict(sb3="jeu_labyrinthe.sb3", dir="labyrinthe", names={
   ("Stage", "fond"): ("decor-labyrinthe.svg", "Décor : le labyrinthe", "الخلفية: المتاهة", "image"),
   ("الفأرة", "فأرة"): ("souris.svg", "La souris (joueur)", "الفأرة (اللاعب)", "image"),
   ("الجبن", "جبن"): ("fromage.svg", "Le fromage (but)", "الجبن (الهدف)", "image"),
   ("نجمة 1", "نجمة"): ("etoile.svg", "L'étoile à ramasser", "النجمة المطلوب التقاطها", "image"),
   ("Stage", "موسيقى غامضة"): ("musique-mystere.wav", "Musique de fond : mystère", "موسيقى الخلفية: غموض", "son"),
   ("نجمة 1", "جرس صغير"): ("son-clochette.wav", "Son quand on ramasse une étoile", "صوت التقاط النجمة", "son"),
   ("نجمة 2", "نجمة"): None, ("نجمة 3", "نجمة"): None, ("نجمة 2", "جرس صغير"): None, ("نجمة 3", "جرس صغير"): None})}
allres = {}
for gid, G in GAMES.items():
    OUT = os.path.join(ROOT, "jeux", "ressources", G["dir"]); os.makedirs(OUT, exist_ok=True)
    z = zipfile.ZipFile(os.path.join(ROOT, "jeux", G["sb3"])); p = json.loads(z.read("project.json")); items = []
    for t in p["targets"]:
        for c in t["costumes"] + t["sounds"]:
            nm = G["names"][(t["name"], c["name"])]
            if nm is None: continue
            f, fr, ar, ty = nm; open(os.path.join(OUT, f), "wb").write(z.read(c["md5ext"]))
            items.append(dict(file=f"jeux/ressources/{G['dir']}/{f}", fr=fr, ar=ar, type=ty))
    items.sort(key=lambda i: ({"image": 0, "son": 1}[i["type"]], i["file"]))
    with zipfile.ZipFile(os.path.join(ROOT, "jeux", "ressources", f"ressources-{G['dir']}.zip"), "w", zipfile.ZIP_DEFLATED) as zz:
        for i in items: zz.write(os.path.join(ROOT, i["file"]), os.path.basename(i["file"]))
    allres[gid] = dict(items=items, zip=f"jeux/ressources/ressources-{G['dir']}.zip"); print(gid, len(items), "ressources")
json.dump(allres, open(os.path.join(HERE, "ressources.json"), "w", encoding="utf-8"), ensure_ascii=False)
