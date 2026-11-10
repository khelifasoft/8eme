"""Accès enseignant : répartition annuelle (PROPOSITION À ADAPTER) + fiches de séance imprimables (60 min).
Usage : python3 generateur/enseignant.py   -> enseignant/niveau-{7,8,9}.html et generateur/seances.json
Modifier le contenu : generateur/seances.py"""
import os, json, sys
from html import escape as E
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from seances import SEANCES
from curriculum import AX, YEARS
import planning as PL
OUT = os.path.join(ROOT, "enseignant"); os.makedirs(OUT, exist_ok=True)
TYPES = {"decouverte": "Découverte", "manip": "Manipulation", "projet": "Projet", "eval": "Évaluation"}
# phases d'une séance de 60 min : (phase, minutes, professeur, élève)
PHASES = {
 "decouverte": [("Accueil et rappel", 5, "Rappelle la séance précédente par 2 questions orales.", "Répondent, rappellent les acquis."),
  ("Situation déclenchante", 10, "Présente une situation ou un problème lié à « {t} » ; recueille les idées.", "Observent, formulent des hypothèses."),
  ("Recherche / exploration", 20, "Distribue l'activité, circule, aide sans donner la réponse. Activité : {a}", "Réalisent l'activité en binômes ou en groupes."),
  ("Mise en commun", 10, "Fait confronter les résultats, corrige les erreurs, institutionnalise.", "Présentent, comparent, corrigent."),
  ("Trace écrite", 10, "Guide la rédaction de la trace : {r}", "Copient ou complètent la trace dans le cahier."),
  ("Clôture", 5, "Pose une question de contrôle et annonce la suite.", "Répondent individuellement.")],
 "manip": [("Accueil et rappel", 5, "Vérifie les postes et rappelle la séance précédente.", "Ouvrent leur session, rappellent les acquis."),
  ("Démonstration", 10, "Montre pas à pas la manipulation de « {t} » en verbalisant chaque geste.", "Observent et posent des questions."),
  ("Manipulation guidée puis autonome", 25, "Circule, aide les élèves en difficulté. Activité : {a}", "Manipulent, d'abord en suivant le modèle, ensuite seuls."),
  ("Mise en commun et correction", 10, "Fait présenter 2 ou 3 productions, relève les erreurs fréquentes.", "Comparent leur production, corrigent."),
  ("Trace écrite", 5, "Fait compléter : {r}", "Complètent la fiche-mémo."),
  ("Clôture", 5, "Fait ranger, enregistrer et fermer correctement.", "Enregistrent leur travail.")],
 "projet": [("Accueil et rappel", 5, "Rappelle l'objectif et le cahier des charges du projet.", "Rappellent où ils en sont."),
  ("Consignes et planification", 10, "Présente la tâche « {t} » et les critères de réussite ; fait répartir les rôles.", "Planifient les étapes et se répartissent les rôles."),
  ("Réalisation", 30, "Accompagne chaque équipe, pose des questions plutôt que de donner des solutions. Activité : {a}", "Réalisent le projet, testent, corrigent."),
  ("Tests croisés et partage", 10, "Organise l'échange entre équipes autour d'une grille.", "Testent la production d'un autre groupe, donnent un avis."),
  ("Bilan", 5, "Fait noter : {r}", "Notent ce qui a été réussi et ce qui reste à faire.")],
 "eval": [("Installation et consignes", 5, "Distribue l'épreuve et lit les consignes.", "Prennent connaissance de l'épreuve."),
  ("Épreuve individuelle", 40, "Surveille, relève les difficultés dans une grille d'observation. Épreuve : {a}", "Réalisent l'épreuve seuls."),
  ("Correction collective", 10, "Corrige avec la classe et fait repérer les erreurs.", "Corrigent leur travail."),
  ("Remédiation", 5, "Identifie les élèves à accompagner et prévoit une activité de remédiation.", "Notent les points à retravailler.")],
}
MAT = {"env": "Poste de travail par élève ; cartes-images ; vidéoprojecteur.", "net": "Poste connecté à Internet ; vidéoprojecteur ; fiche de comparaison.",
       "create": "Poste avec logiciel de traitement de texte ou de présentation ; banque d'images libres (voir bibliothèque du site).",
       "prog": "Poste avec Scratch 3 ; projets du site (contes, jeux) ; cartes-instructions pour l'activité débranchée.", "prod": "Poste avec tableur ; fichiers de données fournis."}
RES = {("7", "prog"): "Contes Scratch du site (page « Pensée logique et programmation »).", ("8", "prog"): "Jeux Scratch du site (quiz, mémoire, attrape-objets…).",
       ("9", "prog"): "Jeux Scratch du site et références du niveau.", ("7", "create"): "Bibliothèque d'images, de sons et de lieux du site.", ("8", "create"): "Bibliothèque de sons du site et vidéos."}
CSS = """*{box-sizing:border-box}body{font:14px/1.5 'Segoe UI',Tahoma,Arial,sans-serif;color:#222;background:#fff;margin:0;padding:16px}
.wrap{max-width:820px;margin:0 auto}h1{font-size:22px;color:#1e3a6e;margin:0 0 4px}h2{font-size:17px;color:#1e3a6e;margin:18px 0 6px;border-bottom:2px solid #1e6fd6;padding-bottom:2px}
table{width:100%;border-collapse:collapse;margin:8px 0}th,td{border:1px solid #bbb;padding:4px 7px;vertical-align:top;text-align:left}th{background:#eaf1fb}
.warn{background:#fff6e0;border:1px solid #e3b44b;border-radius:6px;padding:8px 12px;margin:10px 0}.fiche{break-before:page;padding-top:6px}.fiche:first-of-type{break-before:auto}
.meta{display:grid;grid-template-columns:repeat(4,1fr);gap:4px 10px;font-size:13px;margin:6px 0}.meta span{border-bottom:1px dotted #999;padding:1px 0}
.tag{display:inline-block;border-radius:999px;background:#eaf1fb;color:#1e3a6e;font-size:12px;padding:0 9px}.toolbar{margin-bottom:10px}.toolbar a,.toolbar button{font:inherit;margin-inline-end:8px}
.t-eval{background:#fde8e8!important}.t-projet{background:#e8f5e9!important}td.n{white-space:nowrap}
@media print{.toolbar,.noprint{display:none}body{padding:0}.wrap{max-width:none}a{color:inherit;text-decoration:none}@page{size:A4;margin:14mm}}"""
def fmt(s, s_): return s.format(t=s_["title"].lower().rstrip("."), a=s_["act"].rstrip("."), r=s_["trace"].rstrip("."))
def acts_cell(pl):
    if not pl: return ""
    a = ", ".join(f"{n}" for r, n, t in pl["acts"]); g = " ; ".join(("jeu : " if k == "game" else "conte : ") + t for k, t, m in pl["games"])
    return " · ".join(x for x in (a, g) if x)
def matrix_html(y):
    """progression des notions du module « programmation » : ● nouvelle, ◆ approfondie, ○ réinvestie (voir le planning des séances Scratch du site)"""
    if y not in PL.PLAN: return ""
    cols, lines = PL.matrix(y); sym = {"N": "●", "A": "◆", "R": "○", "": ""}
    head = "".join(f"<th>S{c}</th>" for c in cols)
    body = "".join(f'<tr><td>{E(n)}</td><td class="n">{"✓" if known else ""}</td>' + "".join(f'<td class="n">{sym[c]}</td>' for c in cells) + "</tr>" for n, known, cells in lines)
    return (f'<h2>Progression cumulative des notions Scratch (module « programmation »)</h2><p>● notion nouvelle · ◆ notion approfondie · ○ notion réinvestie · ✓ acquise les années précédentes. '
            f'Chaque séance s\'appuie sur les précédentes ; l\'autonomie des élèves augmente peu à peu (guidé, semi-guidé, autonome).</p><table><tr><th>Notion</th><th>Acquis antérieurs</th>{head}</tr>{body}</table>')
def extra_fiches(y):
    """9e : fiches des séances complémentaires proposées (objet programmable micro:bit, application mobile App Inventor), cahier_extra.py"""
    import cahier_extra as CE
    if y not in CE.YEAR_EXTRA: return ""
    out = f'<section class="fiche" id="complement"><h1>{"Cours « Sécurité informatique » en 4 séances" if y == "8" else "Séances complémentaires proposées (aide pédagogique 2026)"}</h1><p>{"Menaces et protection (carte mentale du cours résumée). Proposition non officielle, hors répartition annuelle." if y == "8" else "Objet programmable (micro:bit) et application mobile (App Inventor). Proposition non officielle, hors répartition annuelle : à insérer à la place de séances de révision ou en projet."}</p></section>'
    for key in CE.YEAR_EXTRA[y]:
        e = CE.EXTRA[key]; kind = {"M": "Objet programmable (micro:bit)", "A": "Application mobile (App Inventor)", "S": "Sécurité informatique"}[key[0]]
        ph = "".join(f'<tr><td>{E(t[0])}</td><td class="n">{m} min</td><td>{E(d[0])}</td></tr>' for t, m, d in CE.PHASES[key])
        acq = "".join(f"<li>{E(a[0])}</li>" for a in e["acq"])
        out += f'''<section class="fiche" id="s{key}"><h1>Fiche pédagogique — séance complémentaire {key}</h1>
<p><span class="tag">{E(YEARS[9][0])}</span> <span class="tag">{kind}</span> <span class="tag">60 min</span> <span class="tag">Proposition</span></p>
<h2>Titre de la séance</h2><p><b>{E(e["title"][0])}</b></p><h2>Objectif (l'élève sera capable de…)</h2><p>{E(e["obj"][0])}</p>
<h2>Matériel et ressources</h2><p>Ordinateurs avec accès à { {"M": "l'éditeur MakeCode micro:bit (simulateur, sans carte)", "A": "App Inventor (émulateur ou application compagnon)", "S": "un ordinateur, la vidéo de la séance (page « Sécurité informatique » du site) et des fichiers de test"}[key[0]] } ; fiche du cahier de l'élève : <b>cahier/cahier-{y}.html#s{key}</b>.</p>
<h2>Démarche (60 minutes)</h2><table><tr><th>Phase</th><th>Durée</th><th>Déroulement</th></tr>{ph}</table>
<h2>Trace écrite</h2><p>{E(e["trace"][0])}</p><h2>Je sais…</h2><ul>{acq}</ul>
<h2>Évaluation et différenciation</h2><ul><li>Observer : l'élève atteint-il l'objectif sans aide ? (✓ / ~ / ✗)</li><li>Soutien : version allégée de la fiche (un seul événement ou composant).</li><li>Approfondissement : le défi proposé dans la démarche.</li></ul>
<h2>Remarques du professeur après la séance</h2><p style="min-height:50px;border:1px dashed #aaa"></p></section>'''
    return out
def extra_table(y):
    """tableau de répartition des séances complémentaires proposées (8e : sécurité informatique ; 9e : micro:bit et App Inventor)"""
    import cahier_extra as CE
    if y not in CE.YEAR_EXTRA: return ""
    t = {"8": "Séances complémentaires : cours « Sécurité informatique » (domaine Environnement informatique)", "9": "Séances complémentaires : objet programmable et application mobile"}[y]
    rows = "".join(f'<tr><td class="n">{k}</td><td>…… / ……</td><td><a href="#s{k}">{E(CE.EXTRA[k]["title"][0])}</a></td><td>{E(CE.EXTRA[k]["trace"][0])}</td></tr>' for k in CE.YEAR_EXTRA[y])
    return f'<h2>{t}</h2><p>Proposition non officielle, hors des 27 séances : à insérer à la place de séances de révision ou de projet. Chaque séance dure 60 minutes ; la fiche détaillée suit les 27 fiches.</p><table><tr><th>Séance</th><th>Date</th><th>Titre</th><th>Trace écrite</th></tr>{rows}</table>'
def build_year(y):
    L = SEANCES[y]; Y = YEARS[int(y)]; rows = []; fiches = []
    plan = PL.french_year(y) if y in PL.PLAN else {}
    for i, s in enumerate(L, 1):
        tri = (i - 1) // 9 + 1; mod = AX[s["module"]][0] if s["module"] in AX else ("Production numérique" if s["module"] == "prod" else s["module"])
        if y == "9" and s["module"] == "prog": mod = "Initiation à la logique et à la programmation"
        if y == "9" and s["module"] == "prod": mod = "Production numérique (tableur)"
        s["mod_fr"] = mod; s["n"] = i; s["tri"] = tri
        rows.append(f'<tr class="t-{s["type"] if s["type"] in ("eval","projet") else ""}"><td class="n">S{i}</td><td>T{tri}</td><td>…… / ……</td><td>{E(mod)}</td><td><a href="#s{i}">{E(s["title"])}</a></td><td>{TYPES[s["type"]]}</td><td>{E(acts_cell(plan.get(i)))}</td></tr>')
        ph = "".join(f'<tr><td>{E(p)}</td><td class="n">{m} min</td><td>{E(fmt(t, s))}</td><td>{E(e)}</td></tr>' for p, m, t, e in PHASES[s["type"]])
        assert sum(m for _, m, _, _ in PHASES[s["type"]]) == 60
        demarche = f'<table><tr><th>Phase</th><th>Durée</th><th>Activité du professeur</th><th>Activité de l\'élève</th></tr>{ph}</table>'
        extra = ""
        if i in plan:   # séance du module « programmation » : démarche et progression du planning Scratch
            pl = plan[i]
            demarche = "<table><tr><th>Phase</th><th>Durée</th><th>Déroulement</th></tr>" + "".join(f'<tr><td>{E(a)}</td><td class="n">{m} min</td><td>{E(c)}</td></tr>' for a, m, c in pl["phases"]) + "</table>"
            lst = lambda t, l: f'<p><b>{t} :</b> {E(", ".join(l))}</p>' if l else ""
            roles = {"core": "Activité principale", "support": "Pour s'entraîner", "challenge": "Défi"}
            acts = "".join(f'<li>{roles[r]} : n° {n} — {E(t)}</li>' for r, n, t in pl["acts"])
            gms = "".join(f'<li>{"Jeu" if k == "game" else "Conte"} : {E(t)} ({"vidéo à regarder" if m == "watch" else "à jouer / à modifier"})</li>' for k, t, m in pl["games"])
            extra = (f'<h2>Progression : notions et autonomie</h2><p><b>Niveau d\'autonomie :</b> {E(pl["auto"])} — séance {pl["k"]} du planning Scratch de l\'année ; notions acquises à la fin de la séance : {pl["cum"]} / {len(PL.NOTIONS)}</p>'
                     + lst("Notions nouvelles", pl["new"]) + lst("Notions approfondies", pl["deep"]) + lst("Notions réinvesties", pl["re"])
                     + (f'<h2>Activités et jeux (collection « Activités Scratch » du site)</h2><ul>{acts}{gms}</ul>' if acts or gms else "")
                     + (f'<h2>Théorie Scratch à lire (rubrique « Théorie Scratch » du site)</h2><ul>{"".join("<li>Leçon " + str(n) + " — " + E(t) + "</li>" for n, t in pl["theory"])}</ul>' if pl["theory"] else "")
                     + f'<h2>Fiche du cahier de l\'élève</h2><p>À imprimer et à coller dans le cahier (phrases à trous, trace écrite à compléter, script à moitié terminé à finir en classe) : <b>cahier/cahier-{y}.html#s{i}</b> ou page {pl["k"]} du PDF <b>cahier/cahier-{y}-fr.pdf</b> (version arabe : <b>cahier-{y}-ar.pdf</b>). Le corrigé s\'affiche avec la case « Afficher le corrigé » ou dans les PDF « corrigé ».</p>'
                     + (f'<p><b>Complément :</b> {E(pl["extra"])}</p>' if pl["extra"] else "")
                     + (f'<h2>Je sais…</h2><ul>{"".join("<li>" + E(a) + "</li>" for a in pl["acq"])}</ul>' if pl["acq"] else ""))
        res = RES.get((y, s["module"]))
        fiches.append(f'''<section class="fiche" id="s{i}"><h1>Fiche pédagogique — séance {i} / 27</h1>
<p><span class="tag">{E(Y[0])}</span> <span class="tag">{E(mod)}</span> <span class="tag">{TYPES[s["type"]]}</span> <span class="tag">60 min</span></p>
<div class="meta"><span>Classe : ………</span><span>Date : …… / …… / ……</span><span>Jour : ……………</span><span>Trimestre : T{tri}</span></div>
<h2>Titre de la séance</h2><p><b>{E(s["title"])}</b></p>
<h2>Objectif (l'élève sera capable de…)</h2><p>{E(s["obj"][0].upper() + s["obj"][1:])}.</p>
<h2>Matériel et ressources</h2><p>{E(MAT.get(s["module"], ""))}{(" " + E(res)) if res else ""}</p>
<h2>Démarche (60 minutes)</h2>{demarche}
{extra}<h2>Trace écrite</h2><p>{E(s["trace"])}</p>
<h2>Évaluation et différenciation</h2><ul><li>Observer : l'élève atteint-il l'objectif sans aide ? (✓ / ~ / ✗)</li><li>Soutien : donner un modèle et réduire la tâche à une seule étape.</li><li>Approfondissement : demander de justifier ou de proposer une amélioration.</li></ul>
<h2>Remarques du professeur après la séance</h2><p style="min-height:50px;border:1px dashed #aaa"></p></section>''')
    html = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Accès enseignant — {E(Y[0])}</title><style>{CSS}</style></head><body><div class="wrap">
<div class="toolbar"><button onclick="print()">Imprimer</button><a href="../index.html#y{y}-ens">← Retour au site</a></div>
<h1>Répartition annuelle — {E(Y[0])}</h1>
<div class="warn"><b>Proposition à adapter — document non officiel.</b> Cette répartition est construite à partir des domaines et des capacités du curriculum, à raison d'<b>une séance de 60 minutes par semaine</b> (27 séances, 9 par trimestre). Elle ne remplace ni le programme officiel ni les instructions de l'inspection : chaque professeur l'ajuste selon son calendrier (compléter la colonne « Date »).</div>
<table><tr><th>Séance</th><th>Trim.</th><th>Date</th><th>Module</th><th>Titre</th><th>Type</th><th>Activités Scratch (n°) et jeux</th></tr>{"".join(rows)}</table>
{extra_table(y)}
{matrix_html(y)}
{"".join(fiches)}{extra_fiches(y)}</div></body></html>'''
    open(os.path.join(OUT, f"niveau-{y}.html"), "w", encoding="utf-8").write(html)
data = {}
for y in SEANCES:
    build_year(y); data[y] = [{k: s[k] for k in ("n", "tri", "module", "mod_fr", "type", "title", "obj")} for s in SEANCES[y]]
json.dump(data, open(os.path.join(HERE, "seances.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("OK", {y: len(v) for y, v in data.items()})
