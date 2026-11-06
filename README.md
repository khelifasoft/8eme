# Fiches élèves : contes en arabe à recréer avec Scratch

## Page de l'élève

Titre : **قصص سكراتش / Histoires Scratch**. La page est en arabe et en français : les boutons AR / FR (en haut et dans le menu) changent la langue et le sens de lecture, et le choix est mémorisé ; `index.html?lang=fr` ouvre directement la version française. La barre bleue du haut n'a que deux onglets : **القصص / Contes** et **الألعاب / Jeux**. Dans « Contes », chaque conte a sa carte ; un clic ouvre la page du conte avec tout ce qui le concerne (fiches Word / .doc / à lire, projet Scratch, paquet .zip, images, sons, animations, vidéos et liens de recherche d'images), et une carte « Ressources générales » regroupe ce qui sert à tous les contes. Les adresses sont `#stories`, `#story-<clé>` et `#games`. Les traductions sont dans `generateur/i18n_fr.py` ; les noms d'éléments de la bibliothèque sont déduits de leurs identifiants français et les voix prêtes restent en arabe. Les fiches (HTML, Word) et les dialogues des projets sont en arabe.

Adresse publique (après activation de GitHub Pages) : **https://khelifasoft.github.io/8eme/**

Ouvrir **`index.html`** dans un navigateur (aucune connexion nécessaire). L'élève y trouve :
- les douze contes : fiche Word, fiche à lire, projet Scratch et un paquet `.zip` avec tout ce qui concerne le conte ;
- une bibliothèque : lieux (34), décors (74), personnages (37), animaux (29), costumes et accessoires (79), images animées (54, en images successives) et sons (214 : effets, musiques, voix de synthèse).

**Lien avec le programme** : le domaine « Pensée logique et programmation » de l'*Aide pédagogique – Informatique* (Ministère de l'Éducation, septembre 2025) est transcrit dans `generateur/programme.py` (7e et 8e année) à partir des pages photographiées : à relire avec le document officiel. Le script lit les blocs de chaque projet `.sb3` (51 projets) pour relever les savoirs mobilisés (séquence, événement, boucles, conditions, variables…) et vérifier les directives de cadrage : **aucun opérateur ET/OU, aucune liste, aucun bloc personnalisé** (voir `generateur/programme.json`). Résultat : les 12 contes sont au niveau 7e (séquence, événement) et les 39 jeux au niveau 8e (variables numériques). Sur la page, chaque conte et chaque jeu porte son niveau et ses savoirs, et l'onglet « Jeux » contient le panneau « Lien avec le programme ». Sept fiches d'activité en français (enseignant + élève) sont dans `fiches-activite/` : contes, questions à choix, calcul, mémoire, remise en ordre, rapidité, attrape-objets.

```bash
python3 generateur/programme.py && python3 generateur/fiches_programme.py && python3 generateur/page.py
```

**Jeux Scratch** : l'onglet « الألعاب / Jeux » regroupe 39 jeux à télécharger (`jeux/jeu_*.sb3`), classés en cinq familles : **questions-réponses** (première lettre, vocabulaire français, couleurs, dénombrement, quiz sur les contes), **calcul** (addition, soustraction, table de multiplication, devine le nombre), **mémoire** (paires d'animaux ou de personnages), **remettre les scènes d'un conte dans l'ordre** (un jeu par conte, `python3 generateur/jeux3.py jeux` : on clique sur les six scènes dans l'ordre des événements), **rapidité et précision** (attrape le loup ou le renard, évite les rochers ou la neige au clavier) et **attrape-objets** (un par conte). Les jeux éducatifs sont générés par `python3 generateur/jeux2.py jeux`, les attrape-objets par `python3 generateur/jeux.py jeux` ; les couvertures sont dans `jeux/couvertures/`. Pour afficher aussi des jeux publiés sur scratch.mit.edu, ajouter une ligne dans `jeux.js` : ils se jouent dans la page.

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
