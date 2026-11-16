# Jeux guidés « Le singe et les bananes » et « Le jeu du requin »

Outils qui ont servi à créer les deux jeux (projets Scratch 3, ressources, étapes en images, solutions, vidéos de démonstration). Le résultat est conservé dans ce dépôt :
`jeux/jeu_singe.sb3`, `jeux/jeu_requin.sb3`, `jeux/couvertures/`, `jeux/videos/`, `jeux/ressources/`, `fiches-activite/etapes/` et `generateur/jeux7_content.json` (fiches, étapes, solutions).
`python3 generateur/export_nextjs.py` les ajoute à l'application Next.js (jeux, solutions par étape, ressources, projets privés).

Régénérer (depuis ce dossier) : `python3 assets.py && python3 build_sb3.py` (singe) ; `python3 assets_requin.py && python3 build_requin.py` (requin) ;
vidéos : `node rec.cjs singe 25` puis `python3 mux.py` (Playwright, ffmpeg) ; `content_*.py` écrivent fiches et solutions dans l'application Next.js (variable `NEXTJS_REPO`).
Dépendances : Python 3, Playwright, ffmpeg ; validation optionnelle des `.sb3` avec `scratch-parser`.

Ils apparaissent aussi dans la page statique (`index.html#games`, fiche `#fiche-singe` / `#fiche-requin`, ressources, vidéo, solutions avec le code habituel) grâce à `generateur/jeux7_data.py` (relié à `page.py`, `fiches_ar.py`, `fiches_programme.py` et `solutions.py`) ; fiches imprimables : `fiches-activite/singe.html` et `requin.html`. Reconstruire : `python3 generateur/page.py && python3 generateur/fiches_programme.py`.
