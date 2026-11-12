# Curriculum Informatique en Tunisie

Site bilingue (arabe / français) sur l'enseignement de l'informatique en Tunisie : programme, références et ressources pédagogiques de la 7e à la 9e année de base (les pages des niveaux secondaires existent toujours dans le dépôt mais ne sont plus proposées dans les menus : voir ci-dessous).

## Page de l'élève

Titre : **Curriculum Informatique en Tunisie**. La page est en arabe et en français : les boutons AR / FR (en haut et dans le menu) changent la langue et le sens de lecture, et le choix est mémorisé ; `index.html?lang=fr` ouvre directement la version française. La barre bleue du haut est un **menu à trois entrées : 7e, 8e et 9e année** ; chaque entrée déroule les **quatre domaines d'apprentissage** du programme (Environnement informatique de travail, Technologies : Internet, Création de contenus numériques, Pensée logique et programmation). Chaque domaine ouvre une page avec sa compétence, ses composantes et capacités, ses savoirs associés et les directives de cadrage (`generateur/curriculum.py`, transcrit des photographies de l'*Aide pédagogique – Informatique* ; la page de « Création de contenus » de 9e n'était pas dans les photos). Les ressources sont rattachées aux domaines concernés : **7e Programmation** = les 12 contes (chaque conte ouvre sa page avec fiches, projet Scratch, images, sons, animations, vidéos) ; **8e Programmation** = les 39 jeux ; **7e et 8e Création** = bibliothèque d'images, de sons et d'animations, vidéos et liens vers des ressources libres ; **7e Internet** = recherche de ressources libres. Les adresses sont `#home`, `#y7`, `#y7-prog`…, `#story-<clé>`. Les traductions sont dans `generateur/i18n_fr.py` ; les noms d'éléments de la bibliothèque sont déduits de leurs identifiants français et les voix prêtes restent en arabe. Les fiches (HTML, Word) et les dialogues des projets sont en arabe.

Adresse publique (après activation de GitHub Pages) : **https://khelifasoft.github.io/8eme/**

Ouvrir **`index.html`** dans un navigateur (aucune connexion nécessaire). L'élève y trouve :
- les douze contes : fiche Word, fiche à lire, projet Scratch et un paquet `.zip` avec tout ce qui concerne le conte ;
- une bibliothèque : lieux (34), décors (74), personnages (37), animaux (29), costumes et accessoires (79), images animées (54, en images successives) et sons (214 : effets, musiques, voix de synthèse).

**Références** : chaque niveau (7e, 8e, 9e, puis 1ère, 2e, 3e et 4e année secondaire) a une page « المراجع / Références » avec deux colonnes : pour l'élève et pour l'enseignant. La liste est dans `references.js` (une ligne par référence : niveau, public, titre, adresse ou fichier) et les fichiers sont à déposer dans `references/`. Elle contient pour l'instant le curriculum officiel 7e–8e–9e (`references/curriculum-informatique-7-8-9.pdf`), Scratch, App Inventor et les ressources de ce site. **Les pages des niveaux secondaires et les manuels scolaires restent à compléter** : aucun document n'a encore été fourni pour eux.

**Lien avec le programme** : le domaine « Pensée logique et programmation » de l'*Aide pédagogique – Informatique* (Ministère de l'Éducation, septembre 2025) est transcrit dans `generateur/programme.py` (7e et 8e année) à partir des pages photographiées : à relire avec le document officiel. Le script lit les blocs de chaque projet `.sb3` (40 projets) pour relever les savoirs mobilisés (séquence, événement, boucles, conditions, variables…) et vérifier les directives de cadrage : **aucun opérateur ET/OU, aucune liste, aucun bloc personnalisé** (voir `generateur/programme.json`). Résultat : les 12 contes sont au niveau 7e (séquence, événement) et les 28 jeux au niveau 8e (variables numériques). Sur la page, chaque conte et chaque jeu porte son niveau et ses savoirs, et l'onglet « Jeux » contient le panneau « Lien avec le programme ». Sept fiches d'activité en français (enseignant + élève) sont dans `fiches-activite/` : contes, questions à choix, calcul, mémoire, remise en ordre, rapidité, attrape-objets.

```bash
python3 generateur/programme.py && python3 generateur/curriculum.py && python3 generateur/fiches_programme.py && python3 generateur/page.py
```

**Jeux Scratch** : l'onglet « الألعاب / Jeux » regroupe 28 jeux à télécharger (`jeux/jeu_*.sb3`), classés en cinq familles : **questions-réponses** (première lettre, vocabulaire français, couleurs, dénombrement, quiz sur les contes), **calcul** (addition, soustraction, table de multiplication, devine le nombre), **mémoire** (paires d'animaux ou de personnages), **remettre les scènes d'un conte dans l'ordre** (un jeu par conte, `python3 generateur/jeux3.py jeux` : on clique sur les six scènes dans l'ordre des événements), **rapidité et précision** (attrape le loup ou le renard, évite les rochers ou la neige au clavier) et **attrape-objets** (un seul jeu : « Attrape les poissons »). Les jeux éducatifs sont générés par `python3 generateur/jeux2.py jeux`, les attrape-objets par `python3 generateur/jeux.py jeux` ; les couvertures sont dans `jeux/couvertures/`. Pour afficher aussi des jeux publiés sur scratch.mit.edu, ajouter une ligne dans `jeux.js` : ils se jouent dans la page.

**Images animées et vidéos** : la section « صور متحركة وفيديوهات جاهزة » propose 48 thèmes (forêt, château, mer, loup, tortue…) filtrables par conte. Chaque thème ouvre la recherche correspondante sur Pexels, Pixabay et Mixkit. Rien n'est copié dans le dépôt : les licences de ces sites interdisent de redistribuer leurs fichiers sous forme de bibliothèque. Les adresses de recherche sont construites dans `generateur/page.py` (`THEMES`, `themeLinks`) et peuvent changer si les sites modifient leurs URL.

**Scratch** : la page contient un lien vers le téléchargement officiel de Scratch 3 (`https://scratch.mit.edu/download`) et vers l'éditeur en ligne.

**Vidéos** : la section « فيديوهات » est une bibliothèque de captures d'écran : chaque vidéo apparaît avec une image de couverture (miniature fournie par YouTube, Vimeo, Dailymotion, Internet Archive, Google Drive, ou capture importée / placée dans `videos/`). Un clic ouvre la vidéo dans un lecteur au centre de la page, sans quitter le site. Les vidéos sont hébergées ailleurs (YouTube, Vimeo, Dailymotion, Internet Archive, Google Drive, TED, Facebook, fichiers `.mp4`, ou un code `<iframe>`), sans télécharger la vidéo. Les miniatures contactent l'hébergeur : mettre `autoThumbnails: false` dans `videos.js` pour n'afficher que les captures locales. Pour ajouter une vidéo, ajouter une ligne dans `videos.js` (explications dans le fichier). YouTube refuse souvent l'affichage quand la page est ouverte comme simple fichier (`file://`) : utiliser GitHub Pages ou `lancer.bat` / `lancer.sh`. Certains propriétaires interdisent l'intégration de leurs vidéos ; la page propose alors le lien vers le site d'origine.

**Raccourci sur le bureau** : le bouton « ⬇ اختصار على سطح المكتب » en haut de la page a deux comportements.
- Si la page est servie en HTTPS (GitHub Pages) ou sur `localhost`, et que le navigateur le permet, il installe l'application (Chrome, Edge). Elle fonctionne alors hors connexion pour les pages déjà ouvertes (`manifest.webmanifest`, `sw.js`, `icones/`).
- Sinon, par exemple sur un réseau local en HTTP, il télécharge un petit fichier de raccourci (`.url` sous Windows, `.webloc` sous macOS, `.desktop` sous Linux) que l'élève place sur le bureau. Sur téléphone, il explique « Ajouter à l'écran d'accueil ».

**Réseau local** : lancer `lancer.bat` (Windows) ou `./lancer.sh` (Linux, macOS) sur un poste. Le script affiche l'adresse à donner aux autres postes, par exemple `http://192.168.1.20:8000/`. Il demande Python.

Tout est dessiné ou généré par les scripts de `generateur/` ; les fichiers sont dans `bibliotheque/` et `telechargements/`.

```bash
python3 generateur/bibliotheque.py   # images, sons, animations et .zip
python3 generateur/page.py           # index.html
```

Les sons sont synthétisés (numpy) : ce ne sont pas des enregistrements réels. Les voix viennent d'espeak-ng.

Douze fiches A4 (fond blanc, en arabe) pour les élèves de niveau moyen ou faible.
Chaque fiche contient : résumé du conte, personnages et décors, scénario en six scènes, étapes de réalisation dans Scratch, liste de contrôle et espace d'avis personnel.

| Fichier | Conte |
|---|---|
| `fiches/cinderella.html` | Cendrillon (سندريلا) |
| `fiches/layla.html` | Le Petit Chaperon rouge (ليلى والذئب) |
| `fiches/djeha.html` | Djeha et l'âne (جحا والحمار) |
| `fiches/alibaba.html` | Ali Baba (علي بابا) |
| `fiches/sindbad.html` | Sindbad le marin (السندباد) |
| `fiches/crow.html` | Le corbeau et le renard (الغراب والثعلب) |
| `fiches/hare.html` | Le lièvre et la tortue (الأرنب والسلحفاة) |
| `fiches/lion.html` | Le lion et le rat (الأسد والفأر) |
| `fiches/frog.html` | La princesse et la grenouille (الأميرة والضفدع) |
| `fiches/shepherd.html` | Le berger menteur (الراعي الكذاب) |
| `fiches/pigs.html` | Les trois petits cochons (الخنازير الثلاثة والذئب) |
| `fiches/duckling.html` | Le vilain petit canard (البطة القبيحة) |

## Espace élève et espace enseignant (par niveau)

Chaque niveau (7e, 8e, 9e) a deux accès : **Espace élève** (pages de modules) et **Espace enseignant** (menu du niveau → « فضاء الأستاذ »).

- **Élève** : sous chaque module, des exercices à choix multiples auto-corrigés (options mélangées à chaque essai, bilingues AR/FR) et des activités à réaliser, avec exemples et liens vers les ressources du site. Données : `generateur/exercices.py` (`EXO`, `ACT`).
- **Enseignant** : répartition annuelle **proposée (non officielle, à adapter)**, à raison d'**une séance de 60 min par semaine** (27 séances, 9 par trimestre), et une **fiche pédagogique par séance** (objectif, matériel, démarche minutée sur 60 min, trace écrite, évaluation/différenciation). Pages imprimables : `enseignant/niveau-7.html`, `niveau-8.html`, `niveau-9.html`.
  - Modifier la répartition ou le contenu des séances : `generateur/seances.py`, puis régénérer.
  - Niveaux secondaires (1S à 4S) : 3 domaines généraux par niveau (algorithmique et programmation, information et données, systèmes et réseaux) avec exercices **proposés à titre non officiel** (`generateur/secondaire.py`) ; l'espace enseignant reste vide tant que les programmes ne sont pas fournis.

```bash
python3 generateur/enseignant.py   # fiches enseignant + seances.json
python3 generateur/page.py         # index.html
```

## Parcours de programmation et projets (7e, 8e, 9e)

La page « Pensée logique et programmation » de chaque niveau est organisée en **parcours par compétences** : de petites activités Scratch, de niveau en niveau (par exemple en 8e : décomposer → variables → condition complète → boucles et hasard → modules → tester/corriger/optimiser), chacune avec sa compétence, ses 2-3 petites activités, un jeu ou un conte modèle à télécharger et une liste « Je suis capable de… ». Suivent des **projets de base** à réaliser (exigences et livrables). Les jeux et contes prêts à l'emploi sont rangés dans une bibliothèque repliée en bas de page.

Modifier le parcours : `generateur/parcours.py` (textes arabe/français), puis `python3 generateur/page.py`.

## Fiches d'activité (pages du site)

Le bouton « بطاقة النشاط » / « Fiche d'activité », à côté du téléchargement du jeu ou du conte, ouvre une **page du site** (`#fiche-catch`, `#fiche-contes-<conte>`) : situation-problème, **étapes en images** (6 images du jeu « Attrape les poissons », 6 scènes par conte), déroulement, activités de l'élève, critères de réussite et différenciation. Les images sont générées par `python3 generateur/fiches_etapes.py` (dans `fiches-activite/etapes/`, avec `generateur/etapes.json`) ; le texte vient de `generateur/fiches_programme.py`. Les fiches complètes à imprimer restent dans `fiches-activite/*.html`.

**Deuxième jeu : « Course : évite les voitures »** (`jeux/jeu_course.sb3`, généré par `python3 generateur/jeux4.py jeux`) : on conduit une voiture avec les flèches ← → et on évite les voitures qui arrivent ; variables numériques seulement (points, vies, vitesse), trois cœurs affichés. Il a sa vidéo, sa fiche d'activité (`#fiche-course`, 6 étapes en images, arabe/français) et ses ressources (`#ressources-course`, 9 fichiers : route, voitures, cœurs, sons).

**Troisième jeu : « Le chameau saute-buissons »** (`jeux/jeu_saut.sb3`, `python3 generateur/jeux5.py jeux`) : la barre d'espace fait sauter le chameau (vitesse verticale = variable numérique, gravité −1 par image) par-dessus les buissons qui arrivent ; points, vies, vitesse ; vidéo, fiche d'activité (`#fiche-saut`) et ressources (`#ressources-saut`).

**Quatrième jeu : « Le labyrinthe de la souris »** (`jeux/jeu_labyrinthe.sb3`, `python3 generateur/jeux6.py jeux`) : la souris (flèches) traverse un labyrinthe à trois murs pour atteindre le fromage avant la fin du temps, en ramassant trois étoiles. Les murs sont gérés par les coordonnées (conditions imbriquées, retour à la position précédente mémorisée dans deux variables), sans capteur de couleur ni de contact ; temps = 60 − secondes écoulées. Vidéo, fiche (`#fiche-labyrinthe`) et ressources (`#ressources-labyrinthe`).

**Vidéos des jeux** : le bouton « شاهد فيديو اللعبة » (« Regarder la vidéo du jeu ») remplace le téléchargement du `.sb3` et ouvre `jeux/videos/<jeu>.mp4` dans le lecteur de la page. La partie est **réellement exécutée par scratch-vm** (`generateur/enregistrer_jeu.js`, une passe de boucle par image à 30 images/s), puis dessinée avec les éléments du projet et encodée avec ffmpeg (musique et sons inclus) : `SCRATCH_NODE_MODULES=<node_modules avec scratch-vm et scratch-storage> python3 generateur/video_jeu.py [catch|course|saut|maze]` (Node, Playwright et ffmpeg requis).

**Ressources du jeu « Attrape les poissons »** : le bouton « موارد اللعبة » ouvre `#ressources-catch` avec les 3 images et les 2 sons du projet (à importer dans Scratch) et un zip (`jeux/ressources/`, régénéré par `python3 generateur/fiches_ressources.py`).

## Activités Scratch : collection d'astuces (sous « Jeux Scratch »)

Sous la section **« Jeux Scratch »** des pages 8e et 9e (`#y8-prog`), la rubrique **« أنشطة سكراتش / Activités Scratch »** présente **65 activités Scratch** en six niveaux : 1 Débutant (10), 2 Intermédiaire (10), 3 Avancé (15), 4 Expert (15), 5 Projets créatifs (5, dont **le drapeau de la Tunisie** dessiné au stylo) et 6 **Méthode du programme** (10 : lire et prévoir, chasse aux erreurs, du diagramme au programme, créer un module, module avec paramètre, optimiser un script, capteurs et actionneurs simulés avec une porte automatique, un feu tricolore et un arrosage automatique, remixer et partager).

La collection (`#activites`, `#activites-<n>`) est une **grille d'images par niveau** : chaque activité est une image explicative (la scène après exécution) avec son titre en dessous et une **case « Fait »**. Un clic sur l'image ouvre la **page détaillée** (`#activite-<n>`) : rôle de chaque bloc, **image du script complet** (blocs Scratch dessinés), **scène avant / après**, étapes, résultat attendu, défi, bouton « Fait » et navigation précédente / suivante. Bilingue arabe/français ; les images existent en deux langues.

**Case « Fait » et progression** : les activités cochées sont mémorisées dans le navigateur de l'élève (`localStorage`, clé `scratch-activites-faites`) ; la page affiche la progression globale (barre et « n / 65 »), la progression par niveau (aussi sur les cartes de niveau sous « Jeux Scratch ») et un bouton « Effacer ma progression ». Rien n'est envoyé à un serveur : un autre navigateur ou un autre poste repart de zéro.

- Textes : `generateur/activites_data1.py` (niveaux 1-2, niveaux, dictionnaire des blocs), `activites_data2.py` (niveaux 3-5), `activites_data3.py` (drapeau et niveau 6), `activites_help.py` (rôle des blocs).
- Images (illustrations dessinées pour le site, pas des captures de l'éditeur Scratch) : `generateur/activites_specs.py` décrit le script et les deux scènes de chaque activité ; `python3 generateur/activites_img.py` écrit les 390 SVG dans `fiches-activite/activites/`. Puis `python3 generateur/page.py`.

**Menu principal et accueil** : seuls les niveaux 7e, 8e et 9e y figurent (menu du haut et cartes de la page d'accueil). Les pages des niveaux secondaires (1S à 4S : modules, exercices non officiels, références) sont conservées et restent accessibles par leur adresse (`#ys1`, `#ys2`, `#ys3`, `#ys4`) ; pour les réafficher, remplacer `MENU_YEARS` par `YEARS` dans `generateur/page.py`. La page Téléchargements est accessible depuis le bouton de l'accueil.

## Planning des séances Scratch (progression cumulative, 7e à 9e)

Les activités et les jeux sont organisés en **séances de 60 minutes** (celles du module « programmation » de la répartition annuelle : 6 séances en 7e, 10 en 8e, 14 en 9e). Accès : menu de chaque année → « Planning des séances Scratch » (`#planning-7`, `#planning-8`, `#planning-9`), bouton dans l'espace enseignant, liens depuis la collection d'activités et depuis chaque page d'activité (« Utilisée en séance… »).

- **Progression cumulative** : 28 notions (séquence, événements, déplacements, apparence, coordonnées, messages, sons, boucles, stylo, capteurs, conditions, projet, décomposition, lecture de script, opérateurs, variables, hasard, saisie, modules, paramètres, tests, répéter jusqu'à, optimisation, entrées/traitement/sorties, capteurs et actionneurs, partage). Une **carte des notions** (lignes = notions, colonnes = séances) montre pour chaque séance ● la notion nouvelle, ◆ la notion approfondie, ○ la notion réinvestie, et ✓ les acquis des années précédentes ; chaque séance indique le nombre de notions acquises à sa fin.
- **Gradation de la difficulté et de l'autonomie** : chaque séance est marquée *guidé* (l'enseignant modélise, l'élève suit les étapes), *semi-guidé* (l'élève part de l'objectif et du résultat attendu) ou *autonome* ; l'accompagnement diminue au fil de l'année puis reprend en douceur à chaque nouvelle année.
- **Démarche de 60 minutes** pour chaque séance : rappel (5), situation déclenchante (10), découverte guidée ou réalisation (15), entraînement différencié (20), mise en commun et trace écrite (10) ; séances de projet et d'évaluation : démarches adaptées. Chaque séance propose une activité principale, des activités d'entraînement, un défi, des jeux (vidéo) ou contes, les acquis « Je sais… » et la trace écrite. Les cartes d'activité portent la case « Fait » : la progression de chaque séance s'affiche (par exemple « 2 / 4 »).
- **Contrôle de cohérence** : `python3 generateur/planning.py` vérifie qu'**aucune activité ni aucun jeu proposé à programmer ne demande une notion qui n'a pas encore été introduite** (les notions techniques sont lues dans le script dessiné de chaque activité) et affiche la couverture : 58 activités sur 65 sont placées dans le planning ; les 7 autres (clones, liste, « et », grands projets) sont proposées en **enrichissement** hors planning.
- **Fiches imprimables** (`enseignant/niveau-N.html`, générées par `python3 generateur/enseignant.py`) : le tableau de répartition indique les activités de chaque séance de programmation, la **progression des notions** est imprimable, et la fiche de chaque séance de programmation reprend la démarche, l'autonomie, les notions, les activités et les acquis. Le planning du site s'imprime aussi (bouton « Imprimer le planning »).
- **Modifier le planning** : `generateur/planning.py` (dictionnaire `PLAN` : notions nouvelles, activités, jeux, autonomie, acquis ; textes arabes des séances dans `AR_TXT`), puis `python3 generateur/enseignant.py` et `python3 generateur/page.py`. Proposition non officielle à adapter.

## Théorie Scratch (page 7e, avant les contes)

Sur la page **7e → « Programmation »** (`#y7-prog`), la rubrique **« نظرية سكراتش / Théorie Scratch »** précède les contes. Elle propose **sept mini-leçons** pour comprendre Scratch avant de programmer (la 8e n'a pas de théorie ; la 9e non plus). Accès : cartes de la page 7e, menu de la 7e et carte de la 7e sur l'accueil (« Théorie Scratch »), page `#theorie` (toutes les leçons, **aide-mémoire imprimable** sur une page A4 : schéma de l'écran, 12 mots de Scratch en arabe / français / anglais, six règles d'or), leçons `#cours-1` à `#cours-7`. La page de chaque séance du planning 7e (`#planning-7`) et la fiche imprimable de séance (`enseignant/niveau-7.html`) indiquent les leçons à lire.

| Leçon | Titre | Séance du planning 7e |
|---|---|---|
| 1 | Qu'est-ce qu'un programme ? (algorithme, programme, jeu du robot) | S22 |
| 2 | Scratch en un coup d'œil (les huit zones de l'écran) | S23 |
| 3 | Les blocs de Scratch (9 familles, 5 formes) | S23 |
| 4 | Séquence et événements | S23 |
| 5 | Lutins, costumes, décors et coordonnées (+ messages) | S24 |
| 6 | Répéter : les boucles | S25 |
| 7 | Décider : conditions et capteurs | S26 |

**Gabarit identique pour chaque leçon** : objectif, question d'accroche, comparaison de la vie courante, rappel de la leçon précédente, l'essentiel en deux phrases, images (illustrations dessinées pour le site et images des activités liées), **activités interactives**, vocabulaire arabe / français / anglais, erreurs fréquentes, « À retenir », **« Teste-toi » (5 questions corrigées automatiquement, réponses mélangées à chaque essai)**, activités liées du planning, défi et case « Fait ».

**Activités interactives** (pas de serveur, tout se passe dans le navigateur) : remettre un texte ou un script en ordre (flèches ▲ ▼ puis « Vérifier »), **exécution pas à pas** d'un script (petit interprète de blocs : avancer, tourner, dire, stylo, « répéter n fois », « si… sinon » ; le bloc en cours est surligné, le lutin glisse sur la scène, la branche non exécutée est grisée ; un pronostic « Que va faire ce script ? » est proposé avant l'exécution), **schéma cliquable de l'écran de Scratch** (explorer, puis jeu « Où est… ? »), **lire et placer des coordonnées** en cliquant sur la scène, QCM de familles de blocs et d'événements.

**Progression** : case « Fait » (cartes et pages) et meilleur score du « Teste-toi » mémorisés dans le navigateur de l'élève (`localStorage`, clés `scratch-theorie-faites` et `scratch-theorie-scores`) ; la barre « Ta progression » indique « n / 7 ».

- Contenu : `generateur/theorie_data.py` (les sept leçons ; chaque texte est un couple français / arabe), `theorie_core.py` (blocs, QCM et activités), `theorie.py` (glossaire, règles d'or, zones du schéma, textes de l'interface, export vers la page et contrôles de cohérence : `python3 generateur/theorie.py`), `theorie_img.py` (images dans `theorie/` : couvertures des leçons, figure des formes de blocs, schéma de l'écran), `theorie_js.py` (JavaScript et CSS de la rubrique, insérés dans `index.html` par `page.py`).
- Les images sont des **schémas dessinés** (pas de captures de l'éditeur Scratch). Les textes arabes sont une proposition à relire.
- **Étendre à une autre année** (par exemple la 9e) : ajouter son numéro à `YEARS` dans `generateur/theorie.py` (liens du menu et de l'accueil) et `"theory"` à `RES` dans `generateur/page.py` (`"9-prog": ["theory", "games"]`), puis adapter dans `theorie_js.py` les liens de retour `#y7-prog` et `#planning-7`. Le contenu des leçons est celui de la 7e : à compléter (par exemple variables, modules, tester et corriger pour la 8e et la 9e).
- Régénérer : `python3 generateur/theorie.py` (contrôles + images), `python3 generateur/enseignant.py` (fiches imprimables), `python3 generateur/page.py`.

## Cahier de l'élève : fiches à imprimer et à coller dans le cahier (7e, 8e, 9e)

Pour que les élèves aient une **partie théorique dans leur cahier** en plus de la pratique sur Scratch, chaque **séance de programmation** du planning (6 en 7e, 10 en 8e, 14 en 9e : 30 fiches) a sa **fiche A4** à imprimer et à coller. Accès : cadre « مذكرات الدفتر / Fiches du cahier » en bas de la page « Programmation » de chaque année (`#y7-prog`, `#y8-prog`, `#y9-prog`), en haut de la page du planning (`#planning-N`, avec un bouton par séance), dans l'espace enseignant et dans le menu de chaque année ; dossier `cahier/`.

**Une fiche = une séance** : en-tête (nom, classe, date) · objectif · **phrases à trous** avec une boîte « mots à placer » · **trace écrite de la séance à compléter** (c'est la « trace écrite » prévue par la répartition annuelle : dessin de l'interface de Scratch à légender, tableau événement → effet, structures répétitives, forme réduite et complète de la condition, fiche « variable », fiche « module », tableau de tests et corrections, diagramme, carte de projet, grille d'évaluation…) · **script « à moitié terminé »** (l'activité principale de la séance, avec blocs, nombres ou conditions à écrire) que les élèves **finissent en classe** sur l'ordinateur · ce que je retiens · « Je sais… » et numéros des activités du site pour s'entraîner.

- **Formats** : pages `cahier/cahier-7.html`, `cahier-8.html`, `cahier-9.html` (bilingues arabe / français ; boutons Imprimer, **« Afficher le corrigé »** pour l'enseignant — les réponses apparaissent en rouge sur les pointillés —, choix d'une séance) et **PDF** prêts à imprimer : `cahier-N-ar.pdf`, `cahier-N-fr.pdf`, `cahier-N-ar-corrige.pdf`, `cahier-N-fr-corrige.pdf` (une page par séance). Pour économiser du papier : imprimer deux pages par feuille.
- **Modifier une fiche** : `generateur/cahier_data.py` (trace écrite et script de chaque séance ; `{{mot}}` marque un mot à écrire, visible seulement dans le corrigé), `generateur/cahier_cards.py` (phrases à trous et « à retenir » des 28 notions du planning), `generateur/cahier_img.py` (scripts avec blocs manquants, schéma de l'écran, grille du robot, plan à coordonnées). Le titre, l'objectif, la trace et les « Je sais… » viennent de la répartition annuelle (`seances.py`) et du planning (`planning.py`). Puis `python3 generateur/cahier.py --pdf` (écrit les pages et les PDF ; contrôle qu'aucune fiche ne déborde d'une page A4 ; nécessite Chromium / Playwright pour les PDF) et `python3 generateur/page.py`.
- Les textes arabes sont une proposition à relire ; les fiches suivent le planning (proposition non officielle à adapter). Seules les séances du module « programmation » ont une fiche.

## Téléchargements

Rubrique « Téléchargements » (bouton de la page d'accueil) : logiciels utilisés en 7e, 8e et 9e (Scratch, App Inventor, mBlock, Arduino IDE, LibreOffice, Audacity, Shotcut, GIMP, Inkscape, 7-Zip), filtrables par niveau, avec liens vers les sites officiels. Les logiciels réservés aux niveaux secondaires (Python, Thonny, Visual Studio Code, DB Browser for SQLite, Filius) restent dans `logiciels.js` mais ne sont pas affichés tant que `MENU_YEARS` (dans `generateur/page.py`) ne contient que 7, 8 et 9. Pour ajouter ou modifier un logiciel : éditer `logiciels.js` (aucune régénération nécessaire). **Scratch 3 sur le bureau** : le bouton « Installer Scratch » de l'accueil et la carte « Scratch 3 (version hors ligne) » de la page Téléchargements proposent des **liens directs** vers les installateurs officiels (`https://downloads.scratch.mit.edu/desktop/Scratch%20Setup.exe` pour Windows, `.../Scratch.dmg` pour macOS ; ces adresses redirigent vers la dernière version, 3.32.1 au 09/11/2026) ; le bouton du système détecté passe en premier, et un bouton mène à la page officielle `https://scratch.mit.edu/download` pour les autres systèmes. L'éditeur en ligne a son lien direct : `https://scratch.mit.edu/projects/editor/`. Un bouton « Raccourci de ce site sur le bureau » est aussi disponible sur la page.

## Régénérer les fiches

Le contenu de chaque conte est défini dans `generateur/make.py`.

```bash
python3 generateur/make.py fiches
```

## Versions Word

Les mêmes fiches existent au format Word dans `word/` (une page A4 chacune, texte de droite à gauche) : `.docx` et `.doc`. Le `.doc` (Word 97-2003) s'ouvre dans toutes les versions de Word, y compris Word 2007 ; les `.docx` sont corrigés par `generateur/word_compat.py` pour Word 2007.

```bash
npm install docx
node generateur/docx.js word
python3 generateur/word_compat.py word   # compatibilité Word 2007 + versions .doc
```

Le contenu est lu dans `generateur/stories.json`. Si vous modifiez `make.py`, régénérez ce fichier avant de lancer `docx.js`.

## Projets Scratch

Dans `scratch/`, un projet `.sb3` par conte, déjà préparé pour les élèves :
- les décors et les lutins sont les illustrations de la bibliothèque (lieux, personnages, animaux, objets), avec les costumes de l'histoire (robe de Cendrillon, loup déguisé, porte ouverte, cygne…) ; les animaux se retournent selon leur direction ;
- des effets sonores de la bibliothèque (hurlement du loup, rugissement, magie…) et une musique de fond par histoire ;
- le scénario en six scènes : le décor lance « مشهد 1 », puis chaque réplique et chaque déplacement est un message reçu par le lutin concerné ;
- une voix de synthèse en arabe (espeak-ng) pour chaque réplique et pour la morale : le lutin joue le son puis affiche la bulle, dont la durée s'adapte au son ;
- le bandeau de la morale, affiché à la fin.

Pour les utiliser : Scratch (en ligne ou hors ligne), **Fichier > Charger depuis votre ordinateur**, puis le drapeau vert. Les élèves peuvent ensuite dessiner leurs propres costumes, changer les répliques et enregistrer leur voix.

```bash
python3 generateur/scratch.py scratch
```

La régénération avec les voix demande `espeak-ng` (`apt install espeak-ng`) ; sans lui, les projets sont créés sans son.

La voix de synthèse est robotique. Pour une vraie voix, ouvrir un lutin dans Scratch, onglet **Sons**, enregistrer la réplique avec le micro, puis remplacer le son joué.

## Impression

Ouvrir un fichier dans le navigateur, puis imprimer en A4 portrait.

**Planning 9e : séances complémentaires** — les huit séances micro:bit (4) puis App Inventor (4) (`generateur/cahier_extra.py`) apparaissent à la suite des 14 séances de `#planning-9`, sous « Séances complémentaires proposées », avec démarche de 60 minutes et lien vers leur fiche du cahier. Proposition non officielle, hors carte des notions.

## Cours « Sécurité informatique » (8e année, 4 séances)

Page `#securite` (accessible depuis le menu de la 8e, la carte de la 8e sur l'accueil et le bas de la page « Environnement informatique de travail » `#y8-env`) : cours en **4 séances de 60 minutes** tiré de la carte mentale du cours de Mme Chelly Baccar Souheila (EP Korba), reformulé : (1) reconnaître une menace et protéger sa vie privée, (2) logiciels malveillants et piratage, (3) risques des communautés virtuelles, (4) protéger ses données et bilan. Chaque séance : **cas d'introduction fictif**, **vidéo explicative** silencieuse (arabe et français, 4 à 6 scènes légendées : `videos/securite/securite-N-{ar,fr}.mp4`), activité, trace écrite, démarche de 60 minutes. Elle apparaît aussi dans le planning 8e (`#planning-8`, séances complémentaires), dans le cahier de l'élève (`cahier/cahier-8.html`, fiches S1 à S4) et dans les fiches enseignant (`enseignant/niveau-8.html`). Précautions de l'aide pédagogique 2026 : cas fictifs, aucun logiciel malveillant réel, aucun mot de passe personnel.
- Contenu : `generateur/securite.py` (textes, cas, activités, scènes des vidéos) ; vidéos : `python3 generateur/video_securite.py` (eSpeak NG, ffmpeg, Node et Playwright) ; page : `securite_js.py`. Puis `python3 generateur/cahier.py --pdf`, `enseignant.py`, `page.py`.
- La voix arabe de synthèse est robotique : pour une voix naturelle, enregistrer les commentaires et remplacer les fichiers `.mp4`. Textes arabes à relire.

**Version allégée des activités** : chacune des 65 activités a, sous « Défi supplémentaire », une rubrique **« نسخة مخففة / Version allégée »** (tâche réduite pour les élèves en difficulté : script presque construit, un seul lutin, une seule règle à écrire…). Textes : `generateur/activites_light.py`, puis `python3 generateur/page.py`.

**9e sans Scratch** : conformément à l'aide pédagogique 2026 (objets programmables et applications mobiles), la page « Programmation » de la 9e, son planning, son cahier et ses fiches enseignant ne contiennent plus ni jeux, ni activités, ni scripts Scratch (les séances S1 à S14 de la répartition gardent leurs titres et leurs traces écrites ; les huit séances micro:bit et App Inventor sont la pratique). Scratch reste en 7e et en 8e.

**9e : activité, vidéo et ressources pour chaque séance micro:bit / App Inventor** — la page `#y9-prog` donne pour chacune des 8 séances (M1-M4, A1-A4) une activité ou un mini-projet avec étapes, résultat attendu, une **capture d'écran** de présentation (`objets/captures/`) puis un bouton « Regarder la vidéo explicative » qui ouvre une **animation silencieuse, sans voix** (la carte micro:bit « en marche » ou l'écran de l'application, légendes en arabe ou en français : `videos/objets/`) et un **zip de ressources** (`objets/ressources/<séance>.zip` : programme MakeCode en JavaScript, plan des blocs App Inventor, images PNG de chaque étape, notice). Tout est simulé, rien n'est testé sur une vraie carte ni dans App Inventor. Contenu : `generateur/objets.py` ; fabrication : `python3 generateur/video_objets.py` ; puis `page.py`. Le lien « Planning des séances » a été retiré de cette page.

**Présentation en cartes (comme les jeux Scratch de la 8e)** : sur `#y9-prog` (micro:bit / App Inventor) et en tête de `#securite`, chaque séance est une carte avec capture d'écran, titre, description et trois boutons : « Regarder la vidéo » (animation silencieuse dans le lecteur du site), « Fiche d'activité » (page détaillée `#objet-M1` … `#objet-A4`, ou section de `#securite-S1` … `S4`) et « Ressources » (zip, ou fiche du cahier pour la sécurité).

**Activités Scratch façon code.org (8e)** : (1) sur chaque page d'activité, un puzzle **« Construis le script »** (`securite_js.py`, jetons calculés par `activites.tokens()`) : l'élève clique sur les blocs de la palette pour les placer dans l'espace de travail, puis sur « Démarrer » ; le script correct affiche le script emboîté, l'animation avant → après et coche « Fait » automatiquement ; sinon, un message dit combien de blocs sont bien placés ; boutons « Indice » et « Recommencer » ; le script complet est replié sous « Voir la solution ». (2) La page `#activites` s'affiche par défaut en **vue liste** : un module par niveau (repliable), une ligne par activité avec des pastilles numérotées (◆ objectif, une pastille par étape, ★ résultat) qui deviennent vertes quand l'activité est faite ; un bouton bascule vers la vue grille d'images (choix mémorisé).

- **Puzzle « Construis le script »** : les blocs gardent la forme de Scratch 3 (chapeau arrondi, encoche/ergot, blocs en C emboîtés pour répéter/si/sinon, condition hexagonale, couleurs par catégorie).

- **Solutions des étapes** (fiches des jeux catch/course/saut/labyrinthe) : bouton « Solution » sous chaque étape, modal protégé par un code (`CODE` dans `generateur/solutions.py`, `123` par défaut) puis blocs de l’étape. Le code est vérifié côté navigateur : il écarte les élèves curieux, ce n’est pas une sécurité.

- **Export vers la nouvelle application** (8e année seulement) : `python3 generateur/export_nextjs.py ../8eme-nextjs-postgres` écrit le contenu bilingue (`content/public`), les solutions (`content/private`) et les images dans le dépôt [8eme-nextjs-postgres](https://github.com/khelifasoft/8eme-nextjs-postgres).
