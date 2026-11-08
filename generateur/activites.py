"""Rubrique « Activités Scratch » (placée sous « Jeux Scratch ») : collection de 54 astuces et activités Scratch
(50 astuces en 4 niveaux + 4 projets créatifs), chacune avec une page détaillée (script, scène avant/après, rôle des blocs).
Données : activites_data1.py (niveaux 1-2, blocs) et activites_data2.py (niveaux 3-5) ; activites_help.py (rôle des blocs) ;
activites_specs.py + activites_img.py (images des scripts et des scènes, générées dans fiches-activite/activites/).
Chaque texte est un couple (français, arabe).
export() -> (données JSON pour la page en arabe, dictionnaire arabe -> français)"""
import activites_data1 as d1, activites_data2 as d2, activites_help as hp
ACTS = d1.ACTS1 + d1.ACTS2 + d2.ACTS3 + d2.ACTS4 + d2.ACTS5
IMG = "fiches-activite/activites/a{n}-{k}{s}.svg"
def export():
    fr = {}
    def P(pair): fr[pair[1]] = pair[0]; return pair[1]
    levels = []
    for l in d1.LEVELS:
        n_acts = sum(1 for a in ACTS if a["lvl"] == l["n"])
        levels.append(dict(n=l["n"], t=l["ar"], diff=P(l["diff"]), obj=P(l["obj"]), count=n_acts)); fr[l["ar"]] = l["fr"]
    blocks = {}
    for k, v in d1.BLOCKS.items():
        blocks[k] = [v[0], v[2], hp.HELP[k][1]]; fr[v[2]] = v[1]; fr[hp.HELP[k][1]] = hp.HELP[k][0]
    acts = [dict(n=a["n"], lvl=a["lvl"], t=P(a["title"]), obj=P(a["obj"]), blocks=a["blocks"], steps=[P(s) for s in a["steps"]], res=P(a["result"]), defi=P(a["defi"]),
                 img={k: [IMG.format(n=a["n"], k=k, s=""), IMG.format(n=a["n"], k=k, s="-ar")] for k in ("script", "avant", "apres")}) for a in ACTS]
    for ui in [
        ("Collection : 50 astuces et activités Scratch", "مجموعة: 50 فكرة ونشاطا في سكراتش"), ("Activités Scratch", "أنشطة سكراتش"),
        ("50 astuces classées en quatre niveaux, puis des projets créatifs. Chaque activité suit la même fiche : objectif, blocs nécessaires, réalisation, résultat attendu et défi.", "50 فكرة مصنّفة في أربعة مستويات، ثم مشاريع إبداعية. لكل نشاط البطاقة نفسها: الهدف والكتل اللازمة والإنجاز والنتيجة المنتظرة وتحدٍّ إضافي."),
        ("Objectif", "الهدف"), ("Blocs nécessaires", "الكتل اللازمة"), ("Réalisation", "الإنجاز"), ("Résultat attendu", "النتيجة المنتظرة"), ("Défi supplémentaire", "تحدٍّ إضافي"),
        ("50 idées et activités classées en quatre niveaux, avec des projets créatifs. Chaque activité a sa page détaillée : image du script, scène avant et après, rôle de chaque bloc.", "50 فكرة ونشاطا مصنّفة في أربعة مستويات، مع مشاريع إبداعية. لكل نشاط صفحة مفصلة: صورة السكربت والمشهد قبل التنفيذ وبعده ودور كل كتلة."),
        ("Ouvrir le niveau", "فتح المستوى"), ("Ouvrir toute la collection", "فتح المجموعة كاملة"), ("Ouvrir la page détaillée", "فتح الصفحة المفصلة"),
        ("Collection d'activités", "مجموعة الأنشطة"), ("Activité précédente", "النشاط السابق"), ("Activité suivante", "النشاط التالي"), ("Toutes les activités", "كل الأنشطة"),
        ("Les blocs utilisés et leur rôle", "الكتل المستعملة ودورها"), ("Le script complet", "السكربت الكامل"), ("Réalisation pas à pas", "الإنجاز خطوة بخطوة"),
        ("Avant et après", "قبل وبعد"), ("Avant l'exécution", "قبل التنفيذ"), ("Après l'exécution", "بعد التنفيذ"),
        ("Astuce : teste ton projet après chaque étape en cliquant sur le drapeau vert.", "نصيحة: اختبر مشروعك بعد كل خطوة بالنقر على العلم الأخضر."),
        ("Les images sont des illustrations réalisées pour ce site (blocs Scratch et scène du projet).", "الصور رسوم توضيحية أُنجزت لهذا الموقع (كتل سكراتش ومشهد المشروع)."),
        *[(f"Niveau {i}", f"المستوى {i}") for i in range(1, 6)], ("4 activités", "4 أنشطة"), ("10 activités", "10 أنشطة"), ("15 activités", "15 نشاطا"), ("Niveau", "المستوى"),
        ("Ces activités permettent aux élèves de combiner plusieurs astuces.", "تتيح هذه الأنشطة للتلاميذ الجمع بين عدة أفكار.")]:
        P(ui)
    for l in levels: l["count_t"] = {4: "4 أنشطة", 10: "10 أنشطة", 15: "15 نشاطا"}[l["count"]]
    return dict(levels=levels, blocks=blocks, acts=acts), fr
if __name__ == "__main__":
    d, f = export(); print(len(d["acts"]), "activités,", len(f), "traductions", [l["count"] for l in d["levels"]])
