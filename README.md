# Fiches élèves : contes en arabe à recréer avec Scratch

## Page de l'élève

Adresse publique (après activation de GitHub Pages) : **https://khelifasoft.github.io/8eme/**

Ouvrir **`index.html`** dans un navigateur (aucune connexion nécessaire). L'élève y trouve :
- les douze contes : fiche Word, fiche à lire, projet Scratch et un paquet `.zip` avec tout ce qui concerne le conte ;
- une bibliothèque : lieux (34), décors (74), personnages (37), animaux (29), costumes et accessoires (79), images animées (54, en images successives) et sons (214 : effets, musiques, voix de synthèse).

**Vidéos** : la section « فيديوهات » affiche des vidéos hébergées ailleurs (YouTube, Vimeo, Dailymotion, Internet Archive, Google Drive, TED, Facebook, fichiers `.mp4`, ou un code `<iframe>`), sans quitter la page et sans télécharger la vidéo. Pour qu'une vidéo apparaisse chez tous les élèves, ajouter une ligne dans `videos.js` (explications dans le fichier). Le bouton « + إضافة رابط فيديو » ajoute un lien seulement dans le navigateur de la personne qui l'utilise. YouTube refuse souvent l'affichage quand la page est ouverte comme simple fichier (`file://`) : utiliser GitHub Pages ou `lancer.bat` / `lancer.sh`. Certains propriétaires interdisent l'intégration de leurs vidéos ; la page propose alors le lien vers le site d'origine.

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
- les décors (fonds de couleur avec le nom du lieu) et les lutins (pastilles colorées avec leur nom, parfois deux costumes) ;
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
