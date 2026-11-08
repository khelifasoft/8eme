"""Ressources du jeu « Attrape les poissons » (images et sons du projet), prêtes à importer dans Scratch :
jeux/ressources/attrape-poissons/ + ressources-attrape-poissons.zip + generateur/ressources.json
Usage : python3 generateur/fiches_ressources.py"""
import os, json, zipfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "jeux", "ressources", "attrape-poissons"); os.makedirs(OUT, exist_ok=True)
NAMES = {  # nom du costume/son dans le projet -> (fichier, titre fr, titre ar, type)
 "fond": ("decor-mer.svg", "Décor : la mer", "الخلفية: البحر", "image"),
 "اللاعب": ("joueur-sindbad.svg", "Joueur : Sindbad", "اللاعب: السندباد", "image"),
 "الشيء": ("objet-poisson.svg", "Objet qui tombe : le poisson", "الشيء الساقط: السمكة", "image"),
 "موسيقى البحر": ("musique-mer.wav", "Musique de fond : la mer", "موسيقى الخلفية: البحر", "son"),
 "قفزة في الماء": ("son-plouf.wav", "Son quand on attrape un poisson : plouf", "صوت التقاط السمكة: قفزة في الماء", "son")}
z = zipfile.ZipFile(os.path.join(ROOT, "jeux", "jeu_sindbad.sb3")); p = json.loads(z.read("project.json")); items = []
for t in p["targets"]:
    for c in t["costumes"] + t["sounds"]:
        f, fr, ar, ty = NAMES[c["name"]]; open(os.path.join(OUT, f), "wb").write(z.read(c["md5ext"]))
        items.append(dict(file=f"jeux/ressources/attrape-poissons/{f}", fr=fr, ar=ar, type=ty))
order = {"image": 0, "son": 1}; items.sort(key=lambda i: (order[i["type"]], i["file"]))
with zipfile.ZipFile(os.path.join(ROOT, "jeux", "ressources", "ressources-attrape-poissons.zip"), "w", zipfile.ZIP_DEFLATED) as zz:
    for i in items: zz.write(os.path.join(ROOT, i["file"]), os.path.basename(i["file"]))
json.dump(items, open(os.path.join(HERE, "ressources.json"), "w", encoding="utf-8"), ensure_ascii=False)
print(len(items), "ressources")
