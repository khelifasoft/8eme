"""Fiches d'activité (enseignant + élève), en français, alignées sur « Pensée logique et programmation ».
Usage : python3 generateur/fiches_programme.py   (depuis la racine du dépôt ; lit generateur/programme.json)"""
import os, json
from html import escape as E
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
PRG = json.load(open(os.path.join(HERE, "programme.json"), encoding="utf-8"))
OUT = os.path.join(ROOT, "fiches-activite"); os.makedirs(OUT, exist_ok=True)

def projects_of(prefix_list):
    return {k: v for k, v in PRG["projects"].items() if any(k.startswith(p) for p in prefix_list)}

FAMILIES = {
 "contes": dict(level=7, title="Raconter un conte avec Scratch", prefix=["conte_"], dir="scratch", pattern="{k}.sb3",
  situation="Comment faire jouer un conte par des personnages qui parlent chacun leur tour, dans le bon ordre, quand on clique sur le drapeau vert ?",
  parts=[0, 1, 2, 3], duree="2 séances de 45 minutes",
  demarche=[("Situation-problème sans ordinateur (15 min)", "Les élèves jouent le conte à six, scène par scène, avec des cartes « scène » numérotées. Le professeur demande : comment dire à l'ordinateur qui parle, quand, et dans quel ordre ? Chaque groupe écrit sur une affiche ce qu'il doit faire, les étapes et la façon de vérifier."),
            ("Découverte du projet (10 min)", "Ouvrir le projet du conte (drapeau vert). Observer et verbaliser ce qui se passe avant de regarder les blocs."),
            ("Lecture de scripts (15 min)", "Repérer le bloc « quand je reçois… » : c'est l'événement déclencheur d'une scène. Suivre un script pas à pas et prévoir le résultat de chaque bloc avant de l'exécuter."),
            ("Modification guidée (20 min)", "Les élèves réalisent les consignes de la fiche élève (changer une réplique, ajouter un costume)."),
            ("Test et correction (10 min)", "Chaque binôme teste le projet d'un autre binôme et note une erreur ou une amélioration, puis corrige."),
            ("Partage (5 min)", "Présenter une scène modifiée à la classe : valoriser l'erreur comme étape d'apprentissage.")],
  eleve=["Ouvre Scratch, puis « Fichier → Charger depuis votre ordinateur » et choisis le projet d'un conte.",
         "Clique sur le drapeau vert. Écris, dans l'ordre, ce que font les personnages.",
         "Trouve le script qui démarre la scène 2. Quel bloc le déclenche ?",
         "Change une réplique (bloc « dire … pendant 2 secondes »), puis teste.",
         "Ajoute un costume à un personnage et utilise « basculer sur le costume… » au bon moment.",
         "Défi : ajoute une scène 7 (un arrière-plan, un message « scène 7 » et le script d'un personnage)."],
  questions=["Quel bloc fait démarrer le projet ?", "Pourquoi les scènes ne se jouent-elles pas toutes en même temps ?", "Que se passe-t-il si tu supprimes le bloc qui envoie le message de la scène suivante ?"],
  allegee="Ne modifier qu'une seule réplique, puis tester et enregistrer.",
  prolongement="Niveau 8e : ajouter une variable numérique « scènes jouées » qui augmente de 1 à chaque scène ; décomposer le conte en sous-problèmes (une scène = un sous-problème) et le représenter par un diagramme.",
  criteres=["Le projet démarre avec le drapeau vert.", "Les scènes s'enchaînent dans le bon ordre.", "Au moins une modification est testée et justifiée.", "L'élève explique le rôle du bloc « quand je reçois… »."]),
 "quiz": dict(level=8, title="Questions à choix multiples (lettres, français, couleurs, comptage, contes)", prefix=["jeu_lettres", "jeu_francais", "jeu_couleurs", "jeu_comptage", "jeu_contes"], dir="jeux", pattern="jeu_{k}.sb3",
  situation="Comment l'ordinateur peut-il vérifier une réponse, compter les points et passer à la question suivante ?",
  parts=[0, 1, 2], duree="2 séances de 45 minutes",
  demarche=[("Besoin à faire émerger sans ordinateur (10 min)", "Le professeur pose des questions ; les élèves lèvent la carte A, B ou C ; un élève tient le tableau des points. Question : que doit mémoriser l'ordinateur ? On fait apparaître le besoin d'une variable (le score, le numéro de la question)."),
            ("Jouer au jeu (5 min)", "Les élèves jouent puis décrivent ce que le jeu fait à chaque réponse."),
            ("Décomposer le problème (15 min)", "En groupe : dessiner un diagramme des sous-problèmes (afficher la question, vérifier la réponse, mettre à jour le score, passer à la suivante, afficher le résultat), puis retrouver chaque sous-problème dans les scripts."),
            ("Lire les scripts (10 min)", "Repérer les variables (numéro de la question, points, bonne réponse), la condition « si… sinon… » (forme complète) et les messages « afficher » et « fin »."),
            ("Modifier le jeu (20 min)", "Changer une question en suivant la fiche élève."),
            ("Tester, corriger, optimiser (15 min)", "Tester avec toutes les bonnes réponses, puis avec toutes les mauvaises ; corriger les erreurs ; proposer une amélioration justifiée (un son, un message d'encouragement).")],
  eleve=["Ouvre un jeu de questions dans Scratch et joue jusqu'à la fin.",
         "Écris le nom des trois variables visibles ou utilisées. À quoi sert chacune ?",
         "Dans le sprite « السؤال », trouve où l'on indique la bonne réponse de la question 1.",
         "Change la question 1 : modifie le costume de la question, celui des trois options et la valeur donnée à « الصحيح ».",
         "Teste : réponds juste, puis faux. Le score et le passage à la question suivante sont-ils corrects ?",
         "Défi : ajoute un son différent quand la réponse est fausse."],
  questions=["Que se passe-t-il si la variable « النقاط » n'est pas remise à 0 au début ?", "Pourquoi utilise-t-on la forme « si… sinon… » ici ?", "Comment le programme sait-il que c'était la dernière question ?"],
  allegee="Ne modifier qu'une seule question (texte du costume) sans toucher à la bonne réponse.",
  prolongement="Créer un module (« Mon bloc ») « bonne réponse » qui ajoute les points et joue le son ; tester que le jeu fonctionne toujours (3 modules au maximum).",
  criteres=["Le score est correct après un test complet.", "La question modifiée s'affiche avec la bonne réponse.", "L'élève explique le rôle de chaque variable.", "Une amélioration est proposée et testée."]),
 "math": dict(level=8, title="Calcul et nombres (addition, soustraction, table de multiplication, devine le nombre)", prefix=["jeu_addition", "jeu_soustraction", "jeu_multiplication", "jeu_devine"], dir="jeux", pattern="jeu_{k}.sb3",
  situation="Comment faire poser dix questions différentes, au hasard, et corriger les réponses tapées ?",
  parts=[0, 1, 2], duree="2 séances de 45 minutes",
  demarche=[("Besoin à faire émerger sans ordinateur (10 min)", "Deux élèves tirent chacun une carte-nombre ; un troisième calcule. Comment un ordinateur choisirait-il les nombres ? Comment retiendrait-il ces nombres pour corriger ? → besoin de variables et d'un nombre au hasard."),
            ("Jouer au jeu (5 min)", "Jouer une partie, puis décrire les étapes d'une question."),
            ("Décomposer le problème (15 min)", "Diagramme : choisir deux nombres, poser la question, lire la réponse, comparer avec le résultat, compter le point, répéter dix fois."),
            ("Lire les scripts (10 min)", "Variables « أ » et « ب », bloc « répéter 10 fois », bloc « demander… et attendre », condition « si réponse = résultat… sinon… »."),
            ("Modifier (20 min)", "Changer l'intervalle des nombres au hasard ; changer le nombre de questions."),
            ("Tester, corriger, optimiser (15 min)", "Vérifier avec des cas limites (plus petit nombre, plus grand) ; corriger ; proposer un réglage de difficulté justifié.")],
  eleve=["Ouvre un jeu de calcul et joue une partie complète.",
         "Dans le script du sprite, repère le bloc qui choisit un nombre au hasard. Entre quelles valeurs ?",
         "Change l'intervalle des nombres pour rendre le jeu plus facile, puis plus difficile.",
         "Change le nombre de questions (10 → 5), puis vérifie que le message final est cohérent.",
         "Teste : réponds juste, puis faux. Que dit le personnage ?",
         "Pour « Devine le nombre » : explique comment trouver le nombre en 7 essais au maximum."],
  questions=["Que faut-il changer pour que la soustraction ne donne jamais un résultat négatif ?", "Pourquoi la variable du score est-elle remise à 0 au début ?", "À quoi sert « répéter jusqu'à » dans « Devine le nombre » ?"],
  allegee="Ne changer que l'intervalle des nombres et rejouer.",
  prolongement="Créer un module « poser la question » (« Mon bloc ») et l'appeler dans la boucle ; ajouter un message d'encouragement quand le score dépasse 8.",
  criteres=["Le jeu pose bien le nombre de questions demandé.", "Les résultats sont corrigés correctement.", "L'élève explique le rôle des variables et du hasard.", "Un test avec cas limites est décrit."]),
 "memory": dict(level=8, title="Jeux de mémoire (paires d'animaux ou de personnages)", prefix=["jeu_memoire"], dir="jeux", pattern="jeu_{k}.sb3",
  situation="Comment retourner deux cartes, retenir la première, vérifier si elles sont identiques puis les garder ou les cacher ?",
  parts=[0, 1, 2], duree="2 séances de 45 minutes",
  demarche=[("Besoin à faire émerger sans ordinateur (10 min)", "Jeu de memory avec douze cartes en papier. Un élève « mémoire de l'ordinateur » note la première carte retournée. Que faut-il retenir ? Qui décide de garder ou de cacher les cartes ?"),
            ("Décomposer le problème (15 min)", "Sous-problèmes : retourner une carte ; mémoriser la première ; comparer avec la deuxième ; garder la paire ou cacher les deux ; détecter la victoire. Représenter par un diagramme."),
            ("Lire les scripts (15 min)", "Variables globales (première carte, verrou, paires trouvées), variable propre au lutin (numéro de paire), conditions imbriquées, messages « نجاح » et « رجوع »."),
            ("Modifier (20 min)", "Remplacer les images de deux cartes pour créer une nouvelle paire."),
            ("Tester, corriger, optimiser (15 min)", "Tester deux cartes différentes puis deux cartes identiques ; corriger ; proposer une amélioration justifiée (durée d'affichage, son).")],
  eleve=["Joue jusqu'à trouver toutes les paires. Combien de tentatives as-tu faites ?",
         "Trouve les variables qui retiennent la première carte et empêchent de retourner une troisième carte.",
         "Dans deux cartes, remplace le costume « وجه » par la même nouvelle image et donne la même valeur à leur variable de paire.",
         "Teste ton changement : les deux cartes forment-elles une paire ?",
         "Modifie la durée d'attente avant de cacher deux cartes différentes ; explique ton choix.",
         "Défi : ajoute un son quand une paire est trouvée."],
  questions=["Pourquoi faut-il une variable « verrou » ?", "Que se passe-t-il si on clique deux fois sur la même carte ?", "Comment le jeu sait-il que toutes les paires sont trouvées ?"],
  allegee="Changer seulement l'image d'une carte et de sa jumelle, puis tester.",
  prolongement="Regrouper « retourner la carte et jouer le son » dans un module ; tester que le jeu fonctionne toujours.",
  criteres=["Les deux cartes modifiées forment une paire.", "Les cartes différentes se cachent de nouveau.", "L'élève explique le rôle du verrou et de la première carte.", "Un test et une correction sont décrits."]),
 "order": dict(level=8, title="Remettre les scènes d'un conte dans l'ordre", prefix=["jeu_ordre_"], dir="jeux", pattern="jeu_{k}.sb3",
  situation="Comment vérifier que l'élève clique sur les scènes dans l'ordre exact du conte ?",
  parts=[0, 1, 2], duree="1 séance de 45 minutes",
  demarche=[("Situation-problème sans ordinateur (10 min)", "Remettre six images du conte dans l'ordre et justifier. Écrire une règle : « la scène suivante est celle qui porte le numéro… » → besoin de mémoriser le prochain numéro attendu."),
            ("Jouer et décrire (10 min)", "Jouer, faire une erreur volontaire, décrire la réaction du jeu."),
            ("Lire les scripts (10 min)", "Variable « التالي » (prochain numéro), variable propre au lutin (numéro de la scène), condition « si… sinon… », costumes numérotés."),
            ("Modifier (10 min)", "Changer la légende d'une scène ; échanger deux scènes en modifiant leurs numéros."),
            ("Tester et corriger (5 min)", "Vérifier le jeu avec le bon ordre puis avec un ordre faux.")],
  eleve=["Joue en cliquant d'abord sur une scène qui n'est pas la première. Que se passe-t-il ?",
         "Remets les six scènes dans l'ordre et compte tes erreurs.",
         "Trouve la variable qui indique la prochaine scène attendue.",
         "Dans une scène, change le numéro de sa variable « ترتيب » et teste : le jeu accepte-t-il le nouvel ordre ?",
         "Défi : fais afficher « Bravo ! » dès que cinq scènes sont bien placées."],
  questions=["Pourquoi la scène placée ne réagit-elle plus quand on clique dessus ?", "Que contient la variable « التالي » à la fin du jeu ?"],
  allegee="Rejouer en notant le numéro de chaque scène avant de cliquer.",
  prolongement="Créer un module « placer la scène » qui met à jour le costume et le compteur ; tester le jeu.",
  criteres=["Le jeu réagit correctement au bon ordre et à un ordre faux.", "L'élève explique le rôle de « التالي ».", "Une modification est testée."]),
 "reflex": dict(level=8, title="Rapidité et précision (attrape le loup ou le renard, évite les rochers ou la neige)", prefix=["jeu_taupe", "jeu_rochers", "jeu_pierres"], dir="jeux", pattern="jeu_{k}.sb3",
  situation="Comment faire apparaître un personnage au hasard, compter les points et arrêter le jeu au bout d'un temps ou quand il n'y a plus de vies ?",
  parts=[0, 1, 2], duree="2 séances de 45 minutes",
  demarche=[("Besoin à faire émerger sans ordinateur (10 min)", "Jeu en classe : un élève lève une carte-animal au hasard, les autres tapent sur la table seulement pour le loup. Comment compter les points et les erreurs ? Comment arrêter ?"),
            ("Jouer et observer (10 min)", "Jouer, relever le score ; noter ce qui change quand le jeu avance (vitesse, temps restant)."),
            ("Lire les scripts (15 min)", "Boucle « répéter indéfiniment », nombre au hasard, événement « quand ce sprite est cliqué » ou touches fléchées, variables (points, temps, vies, vitesse), conditions imbriquées."),
            ("Modifier et optimiser (20 min)", "Régler la durée d'affichage de la cible ou la vitesse de chute ; mesurer l'effet sur le score."),
            ("Tester et corriger (10 min)", "Faire jouer un camarade, noter si le jeu est trop facile ou trop difficile, corriger.")],
  eleve=["Joue deux parties et note ton score.",
         "Trouve dans le script la valeur qui règle la vitesse (ou la durée d'affichage).",
         "Change cette valeur pour rendre le jeu plus facile, teste, puis explique l'effet sur le score.",
         "Que se passe-t-il quand les vies tombent à zéro ou que le temps est écoulé ? Montre le bloc.",
         "Défi : fais gagner 2 points au lieu de 1 pour chaque cible touchée."],
  questions=["Pourquoi utilise-t-on « répéter indéfiniment » ?", "Quelle condition vérifie que le joueur a touché la cible ?", "Quelle valeur choisirais-tu pour un jeu équilibré ? Justifie."],
  allegee="Changer seulement la vitesse ou la durée d'affichage puis rejouer.",
  prolongement="Créer un module « perdre une vie » qui diminue les vies et joue un son ; tester le jeu avec ce module.",
  criteres=["Le réglage modifié change bien la difficulté.", "L'élève explique la boucle et la condition principale.", "Un test avec un camarade est rapporté.", "La modification est justifiée."]),
 "catch": dict(level=8, title="Attrape-objets", prefix=["jeu_sindbad"], dir="jeux", pattern="jeu_{k}.sb3",
  situation="Comment faire tomber des objets de plus en plus vite, les attraper avec la souris et compter les points et les vies ?",
  parts=[0, 1, 2], duree="2 séances de 45 minutes",
  demarche=[("Besoin à faire émerger sans ordinateur (10 min)", "Lancer des balles de papier dans une corbeille tenue par un élève : comment compter les points et les ratés ? → besoin de variables."),
            ("Jouer et décrire (10 min)", "Jouer au jeu d'un conte, décrire les règles."),
            ("Lire les scripts (15 min)", "Le joueur suit la souris ; l'objet tombe (changer y de -vitesse) ; deux conditions imbriquées : « si l'objet est près de la souris, alors si il est assez bas, alors points + 1 »."),
            ("Modifier et optimiser (20 min)", "Changer l'objet qui tombe ou la vitesse initiale ; ajuster l'accélération."),
            ("Tester et corriger (10 min)", "Tester ; corriger ; proposer une amélioration justifiée.")],
  eleve=["Joue jusqu'à la fin et note ton score.",
         "Trouve la variable qui règle la vitesse de chute. Où est-elle initialisée ?",
         "Change la vitesse de départ, teste et explique l'effet.",
         "Repère les deux conditions imbriquées qui détectent un objet attrapé. Explique chacune.",
         "Défi : ajoute un son différent quand tu rates un objet."],
  questions=["Pourquoi les deux conditions sont-elles imbriquées au lieu d'être reliées par ET ?", "Que se passe-t-il quand le nombre de vies atteint 0 ?"],
  allegee="Changer uniquement la vitesse de départ.",
  prolongement="Regrouper « objet attrapé » (points, vitesse, son, retour en haut) dans un module et l'appeler à la place des blocs.",
  criteres=["La vitesse modifiée est constatée au test.", "L'élève explique les conditions imbriquées.", "Une amélioration est testée."]),
 "course": dict(level=8, title="Course : évite les voitures", prefix=["jeu_course"], dir="jeux", pattern="jeu_{k}.sb3",
  situation="Comment déplacer une voiture avec les flèches du clavier, faire arriver des voitures de plus en plus vite et compter les points et les vies ?",
  parts=[0, 1, 2], duree="2 séances de 45 minutes",
  demarche=[("Besoin à faire émerger sans ordinateur (10 min)", "Sur un quadrillage au sol, un élève « voiture » évite les élèves « obstacles » : comment compter les points et les collisions ? → besoin de variables."),
            ("Jouer et décrire (10 min)", "Jouer au jeu, puis décrire les règles : déplacement, voitures adverses, points, vies, vitesse."),
            ("Lire les scripts (15 min)", "Les flèches changent x de la voiture (limites ±85) ; la voiture adverse descend de « vitesse » ; deux conditions imbriquées détectent la collision ; les lignes de la route défilent à la même vitesse ; le nombre de cœurs affichés suit la variable « vies »."),
            ("Modifier et optimiser (20 min)", "Changer la vitesse de départ, l'augmentation de vitesse ou la largeur de collision, puis rejouer et comparer."),
            ("Tester et corriger (10 min)", "Tester : éviter 3 voitures, se faire toucher 3 fois ; vérifier le score, les cœurs et le message de fin ; corriger les erreurs.")],
  eleve=["Joue jusqu'à la fin et note ton score.",
         "Repère les blocs qui déplacent la voiture quand on appuie sur une flèche.",
         "Trouve la variable qui règle la vitesse. Qu'est-ce qui la fait augmenter ?",
         "Change la vitesse de départ ou l'augmentation de la vitesse, teste et explique l'effet.",
         "Défi : ajoute un son quand tu évites une voiture."],
  questions=["Pourquoi les deux conditions de la collision sont-elles imbriquées au lieu d'être reliées par ET ?", "Que se passe-t-il quand le nombre de vies atteint 0 ?"],
  allegee="Changer uniquement la vitesse de départ.",
  prolongement="Créer un module « voiture touchée » (−1 vie, son, retour en haut) et l'appeler à la place des blocs.",
  criteres=["Le changement de vitesse est constaté au test.", "L'élève explique les conditions imbriquées de la collision.", "Une amélioration est testée."]),
}

CSS = """body{font-family:'Segoe UI',Tahoma,Arial,sans-serif;max-width:820px;margin:0 auto;padding:18px 22px 50px;color:#1d2433;line-height:1.55;background:#fff}
h1{font-size:26px;color:#1f4aa8;margin:6px 0 2px}h2{font-size:20px;color:#1f4aa8;border-bottom:2px solid #e8861c;padding-bottom:3px;margin:26px 0 8px}h3{font-size:16px;margin:14px 0 4px}
.badge{display:inline-block;background:#1f4aa8;color:#fff;border-radius:999px;padding:1px 12px;font-size:13px;margin-right:6px}
.meta{color:#5d6678;font-size:14px}table{border-collapse:collapse;width:100%;font-size:14px;margin:6px 0}th,td{border:1px solid #cfd5e3;padding:6px 8px;vertical-align:top;text-align:left}th{background:#eef2fb}
.box{border:1px solid #cfd5e3;border-radius:8px;padding:8px 14px;background:#f8faff;margin:8px 0}ul,ol{margin:4px 0 4px 20px;padding:0}li{margin:3px 0}
.ok{color:#1b7a43;font-weight:700}.pb{page-break-before:always}.lines p{border-bottom:1px dotted #999;height:26px;margin:0}
a{color:#1f4aa8}.small{font-size:12.5px;color:#5d6678}.nav{font-size:14px;margin-bottom:6px}
@media print{body{padding:0}.nav{display:none}h2{break-after:avoid}}"""

def li(items): return "<ul>" + "".join(f"<li>{E(x)}</li>" for x in items) + "</ul>"
def make(fid, F):
    lvl = PRG["levels"][str(F["level"])]; ps = projects_of(F["prefix"])
    concepts = []
    for p in ps.values():
        for c in p["concepts"]:
            if c not in concepts: concepts.append(c)
    n = len(ps); nolog = all(not p["logic"] for p in ps.values()); nolist = all(not p["lists"] for p in ps.values()); nomod = all(p["modules"] == 0 for p in ps.values())
    files = "".join(f'<li><a href="../{F["dir"]}/{os.path.basename(k.replace("conte_","").replace("jeu_","jeu_")) if False else (k.replace("conte_","") + ".sb3" if k.startswith("conte_") else k + ".sb3")}">{E(k)}.sb3</a></li>' for k in ps)
    parts = "".join(f"<h3>{E(lvl['parts'][i]['t_fr'])}</h3>{li(lvl['parts'][i]['i_fr'])}" for i in F["parts"])
    cc = "".join(f"<li>{E(PRG['concepts'][c]['fr'])}</li>" for c in concepts)
    cad = "<ul>" + "".join(f"<li>{E(x)}</li>" for x in lvl["cad_fr"]) + "</ul>"
    check = (f"<table><tr><th>Directive de cadrage ({E(lvl['year_fr'])})</th><th>Constat sur les {n} projets</th></tr>"
             f"<tr><td>Environnement de programmation visuelle par blocs (Scratch)</td><td class='ok'>Oui</td></tr>"
             f"<tr><td>Conditions simples, sans opérateur logique (ET, OU)</td><td class='ok'>{'Oui : aucun opérateur ET/OU' if nolog else 'À vérifier'}</td></tr>"
             f"<tr><td>Variables numériques uniquement ; aucune liste</td><td class='ok'>{'Oui' if nolist else 'À vérifier'}</td></tr>"
             f"<tr><td>Trois modules au maximum</td><td class='ok'>{'Oui : aucun bloc personnalisé' if nomod else 'À vérifier'}</td></tr>"
             f"<tr><td>Variables introduites en réponse à un besoin ; phases de test, correction et optimisation explicites</td><td class='ok'>Prévu dans la démarche ci-dessous</td></tr></table>")
    demarche = "<table><tr><th>Phase</th><th>Déroulement</th></tr>" + "".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td></tr>" for a, b in F["demarche"]) + "</table>"
    html = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(F['title'])} – fiche d'activité</title><style>{CSS}</style></head><body>
<div class="nav"><a href="../index.html#games">← Retour aux jeux</a></div>
<p class="meta">République tunisienne · Aide pédagogique – Informatique · Domaine « Pensée logique et programmation »</p>
<h1>{E(F['title'])}</h1><p><span class="badge">{E(lvl['year_fr'])}</span><span class="meta">Durée indicative : {E(F['duree'])}</span></p>
<h2>Fiche enseignant</h2>
<div class="box"><b>Situation-problème :</b> {E(F['situation'])}</div>
<h3>Compétence visée</h3><p>{E(lvl['comp_fr'])}</p>
<h3>Composantes et capacités visées</h3>{parts}
<h3>Savoirs associés mobilisés par les projets (relevés automatiquement dans les blocs)</h3><ul>{cc}</ul>
<h3>Projets Scratch de cette fiche</h3><ul>{files}</ul>
<h2>Démarche pédagogique</h2>{demarche}
<h2>Directives de cadrage</h2>{cad}{check}
<h2>Différenciation</h2><ul><li><b>Version allégée :</b> {E(F['allegee'])}</li><li><b>Prolongement :</b> {E(F['prolongement'])}</li></ul>
<p class="small">{E(PRG['general_fr'])}</p>
<h2>Critères de réussite</h2>{li(F['criteres'])}
<p class="small">Sources : Aide pédagogique – Informatique, Ministère de l'Éducation (septembre 2025). Le texte du programme a été transcrit à partir de photographies : à relire avec le document officiel.</p>
<div class="pb"></div>
<h2>Fiche élève</h2><p>Nom : ........................................ Classe : ........ Date : ........</p>
<div class="box"><b>Situation-problème :</b> {E(F['situation'])}</div>
<h3>Consignes</h3><ol>{"".join(f"<li>{E(x)}</li>" for x in F['eleve'])}</ol>
<h3>Questions</h3><ol>{"".join(f"<li>{E(x)}</li>" for x in F['questions'])}</ol>
<div class="lines"><p></p><p></p><p></p><p></p></div>
<h3>Mon bilan</h3><table><tr><th>J'ai testé</th><th>J'ai corrigé</th><th>J'ai amélioré</th></tr><tr><td style="height:70px"></td><td></td><td></td></tr></table>
</body></html>"""
    open(os.path.join(OUT, fid + ".html"), "w", encoding="utf-8").write(html)

if __name__ == "__main__":
    for fid, F in FAMILIES.items(): make(fid, F)
    print("fiches :", len(FAMILIES), os.listdir(OUT))
