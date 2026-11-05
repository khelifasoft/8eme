# Fiches élèves : contes en arabe à recréer avec Scratch

Neuf fiches A4 (fond blanc, en arabe) pour les élèves de niveau moyen ou faible.
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

## Régénérer les fiches

Le contenu de chaque conte est défini dans `generateur/make.py`.

```bash
python3 generateur/make.py fiches
```

## Versions Word

Les mêmes fiches existent au format Word dans `word/` (une page A4 chacune, texte de droite à gauche).

```bash
npm install docx
node generateur/docx.js word
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
