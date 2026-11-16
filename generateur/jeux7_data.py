"""Jeux guidés « Le singe et les bananes » et « Le jeu du requin » : données pour la page statique (jeux, fiche, étapes, solutions, ressources).
Source : generateur/jeux7_content.json (le même contenu que l'application Next.js). Outils de création : generateur/jeux7/."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE, "jeux7_content.json"), encoding="utf-8"))
KEYS = [g["key"] for g in C["games"]]
G = {g["key"]: g for g in C["games"]}
eme = lambda t: re.sub(r"\b8(?:e|ème)\b", "8eme", t)
cat = dict(cat="catch", cat_ar="ألعاب سكراتش", cat_fr="Jeux Scratch")
GAMES = [dict(key=k, file=f"jeux/jeu_{k}.sb3", title_ar=G[k]["title"]["ar"], title_fr=G[k]["title"]["fr"], how_ar=G[k]["how"]["ar"], how_fr=G[k]["how"]["fr"], cover=G[k]["cover"].lstrip("/")) for k in KEYS]
EXTRA = {k: dict(video=f"jeux/videos/{k}.mp4", fiche=k, res=k) for k in KEYS}
RES7 = {k: dict(zip=G[k]["ressources"]["zip"].lstrip("/"), items=[dict(file=i["file"].lstrip("/"), fr=i["t"]["fr"], ar=i["t"]["ar"], type=i["type"]) for i in G[k]["ressources"]["items"]]) for k in KEYS}
STEPS7 = {k: [(e["t"]["ar"], e["c"]["ar"]) for e in G[k]["etapes"]] for k in KEYS}
ETAPES7 = {k: [dict(img=e["img"]["fr"].replace("/img/etapes/", "fiches-activite/etapes/"), img_ar=e["img"]["ar"].replace("/img/etapes/", "fiches-activite/etapes/"), t=e["t"]["fr"], c=e["c"]["fr"]) for e in G[k]["etapes"]] for k in KEYS}
def _ar(k):
    f = G[k]["fi"]
    fr = dict(title=f["title"]["fr"], duree="2 séances de 45 minutes", year="8e année", situation=f["situation"]["fr"], steps=[x["fr"] for x in f["steps"]], eleve=[x["fr"] for x in f["eleve"]], criteres=[x["fr"] for x in f["criteres"]], allegee=f["allegee"]["fr"], prolongement=f["prolongement"]["fr"])
    return dict(title=f["title"]["ar"], duree="حصتان من 45 دقيقة", year="السنة الثامنة", situation=f["situation"]["ar"], steps=[x["ar"] for x in f["steps"]], eleve=[x["ar"] for x in f["eleve"]], criteres=[x["ar"] for x in f["criteres"]], allegee=f["allegee"]["ar"], prolongement=f["prolongement"]["ar"], fr=fr)
AR7 = {k: _ar(k) for k in KEYS}
# fiche imprimable (fiches-activite/<clé>.html) : français ; `questions` et `demarche` rédigés pour ces deux jeux
_DEM = {
 "singe": [("Besoin à faire émerger sans ordinateur (10 min)", "Un élève « singe » se déplace à droite et à gauche pour attraper des balles de papier lancées du haut, sauf les balles orange. Faire dire ce qu'il faut décrire à l'ordinateur : qui bouge, qui tombe, quand on gagne un point, quand on perd."),
           ("Jouer et décrire (10 min)", "Ouvrir le projet, cliquer sur le drapeau vert et jouer. Décrire les trois lutins (singe, banane, orange), le score et l'arrière-plan « perdu »."),
           ("Lire les scripts (15 min)", "Lire le script de la banane puis celui de l'orange : « répéter jusqu'à ce que touche le sol ou touche le singe ». Repérer où le score est mis à 0 et où il augmente, et le message « perdu » envoyé à tous."),
           ("Modifier et optimiser (20 min)", "Changer le nombre de pas de chute, ajouter un lutin « citron » qui retire un point, tester chaque changement."),
           ("Tester et corriger (10 min)", "Chaque binôme teste le projet d'un autre binôme, note une erreur ou une amélioration, puis corrige.")],
 "requin": [("Besoin à faire émerger sans ordinateur (10 min)", "Compléter au tableau la carte mentale du jeu (décors, personnages, sons, score, but, commandes). Faire dire ce qu'est un menu et comment passer du menu au jeu."),
            ("Jouer et décrire (10 min)", "Ouvrir le projet, cliquer sur le drapeau vert puis sur « Commencer » et manger les dix poissons. Décrire ce qui change quand on clique sur le bouton."),
            ("Lire les scripts (15 min)", "Suivre le message envoyé par le bouton (arrière-plan, requin, poissons) ; lire le script du poisson (dix clones) puis celui d'un clone (il nage, rebondit, se fait manger)."),
            ("Modifier et optimiser (20 min)", "Changer le nombre de clones et le but, ajouter un « poisson-piège » qui retire un point, tester chaque changement."),
            ("Tester et corriger (10 min)", "Chaque binôme teste le projet d'un autre binôme, note une erreur ou une amélioration, puis corrige.")]}
_QUE = {
 "singe": ["Dans quel lutin se trouve le bloc qui met le score à 0 ? Pourquoi à cet endroit ?", "Pourquoi la banane et l'orange utilisent-elles « touche le sol ou touche le singe » ?", "Que se passe-t-il si on supprime le bloc « envoyer à tous perdu » du singe ?"],
 "requin": ["Qu'est-ce qui déclenche le jeu quand on clique sur « Commencer » ?", "Quelle est la différence entre le lutin « poisson » et ses clones ?", "Comment le jeu sait-il que le but est atteint ?"]}
FAM7 = {k: dict(level=8, title=G[k]["fi"]["title"]["fr"], prefix=[f"jeu_{k}"], dir="jeux", pattern="jeu_{k}.sb3", situation=G[k]["fi"]["situation"]["fr"], parts=[0, 1, 2], duree="2 séances de 45 minutes", demarche=_DEM[k],
                eleve=[x["fr"] for x in G[k]["fi"]["eleve"]], questions=_QUE[k], allegee=G[k]["fi"]["allegee"]["fr"], prolongement=G[k]["fi"]["prolongement"]["fr"], criteres=[x["fr"] for x in G[k]["fi"]["criteres"]]) for k in KEYS}
# solutions : jetons au format de la page (texte arabe ; la traduction passe par la table FRMAP)
def solutions():
    steps, fr = {}, {}
    for k in KEYS:
        steps[k] = []
        for s in C["solutions"][k]:
            toks = []
            for t in s["tok"]:
                if t.get("cond"):
                    o = dict(c=t["c"], k=t["k"], t=f'{t["pre"]["ar"]} {t["cond"]["ar"]}' + (f' {t["post"]["ar"]}' if t.get("post") else ""), d=t["d"], pre=t["pre"]["ar"], cond=t["cond"]["ar"], post=t["post"]["ar"] if t.get("post") else None)
                    for p in ("pre", "cond", "post"):
                        if t.get(p): fr[t[p]["ar"]] = t[p]["fr"]
                else:
                    o = dict(c=t["c"], k=t["k"], t=t["t"]["ar"], d=t["d"]); fr[t["t"]["ar"]] = t["t"]["fr"]
                toks.append(o)
            steps[k].append(dict(sprite=s["sprite"]["ar"], tok=toks)); fr[s["sprite"]["ar"]] = s["sprite"]["fr"]
    return steps, fr
