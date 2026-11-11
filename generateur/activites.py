"""Rubrique « Activités Scratch » (placée sous « Jeux Scratch ») : collection d'astuces et d'activités Scratch
(50 astuces en 4 niveaux, 4 projets créatifs + le drapeau de la Tunisie, et un niveau 6 « méthode du programme » : lire, tester, modules, capteurs),
chacune avec une page détaillée (script, scène avant/après, rôle des blocs) et une case « Fait » (progression enregistrée dans le navigateur).
Données : activites_data1.py (niveaux 1-2, blocs), activites_data2.py (niveaux 3-5), activites_data3.py (drapeau et niveau 6) ; activites_help.py (rôle des blocs) ;
activites_specs.py + activites_img.py (images des scripts et des scènes, générées dans fiches-activite/activites/).
Chaque texte est un couple (français, arabe).
export() -> (données JSON pour la page en arabe, dictionnaire arabe -> français)"""
import activites_light as _lt
import activites_data1 as d1, activites_data2 as d2, activites_data3 as d3, activites_help as hp
ACTS = sorted(d1.ACTS1 + d1.ACTS2 + d2.ACTS3 + d2.ACTS4 + d2.ACTS5 + d3.ACTS55 + d3.ACTS6, key=lambda a: a["n"])
IMG = "fiches-activite/activites/a{n}-{k}{s}.svg"
def count_pair(c): return (f"{c} activités", f"{c} أنشطة" if c <= 10 else f"{c} نشاطا")
def export():
    fr = {}
    def P(pair): fr[pair[1]] = pair[0]; return pair[1]
    total = len(ACTS)
    levels = []
    for l in d1.LEVELS:
        n_acts = sum(1 for a in ACTS if a["lvl"] == l["n"])
        levels.append(dict(n=l["n"], t=l["ar"], diff=P(l["diff"]), obj=P(l["obj"]), count=n_acts, count_t=P(count_pair(n_acts)))); fr[l["ar"]] = l["fr"]
    blocks = {}
    for k, v in d1.BLOCKS.items():
        blocks[k] = [v[0], v[2], hp.HELP[k][1]]; fr[v[2]] = v[1]; fr[hp.HELP[k][1]] = hp.HELP[k][0]
    acts = [dict(n=a["n"], lvl=a["lvl"], t=P(a["title"]), obj=P(a["obj"]), blocks=a["blocks"], steps=[P(s) for s in a["steps"]], res=P(a["result"]), defi=P(a["defi"]), light=P(_lt.LIGHT[a["n"]]),
                 img={k: [IMG.format(n=a["n"], k=k, s=""), IMG.format(n=a["n"], k=k, s="-ar")] for k in ("script", "avant", "apres")}) for a in ACTS]
    title = P((f"Collection : {total} astuces et activités Scratch", f"مجموعة: {total} فكرة ونشاطا في سكراتش"))
    intro = P((f"{total} idées et activités classées en six niveaux, avec des projets créatifs et des activités liées au programme. Chaque activité a sa page détaillée : image du script, scène avant et après, rôle de chaque bloc.",
               f"{total} فكرة ونشاطا مصنّفة في ستة مستويات، مع مشاريع إبداعية وأنشطة مرتبطة بالمنهاج. لكل نشاط صفحة مفصلة: صورة السكربت والمشهد قبل التنفيذ وبعده ودور كل كتلة."))
    for ui in [
        ("Activités Scratch", "أنشطة سكراتش"), ("Objectif", "الهدف"), ("Blocs nécessaires", "الكتل اللازمة"), ("Réalisation", "الإنجاز"), ("Résultat attendu", "النتيجة المنتظرة"), ("Défi supplémentaire", "تحدٍّ إضافي"),
        ("Ouvrir le niveau", "فتح المستوى"), ("Ouvrir toute la collection", "فتح المجموعة كاملة"), ("Ouvrir la page détaillée", "فتح الصفحة المفصلة"),
        ("Collection d'activités", "مجموعة الأنشطة"), ("Activité précédente", "النشاط السابق"), ("Activité suivante", "النشاط التالي"), ("Toutes les activités", "كل الأنشطة"),
        ("Les blocs utilisés et leur rôle", "الكتل المستعملة ودورها"), ("Le script complet", "السكربت الكامل"), ("Réalisation pas à pas", "الإنجاز خطوة بخطوة"),
        ("Avant et après", "قبل وبعد"), ("Avant l'exécution", "قبل التنفيذ"), ("Après l'exécution", "بعد التنفيذ"),
        ("Astuce : teste ton projet après chaque étape en cliquant sur le drapeau vert.", "نصيحة: اختبر مشروعك بعد كل خطوة بالنقر على العلم الأخضر."),
        ("Les images sont des illustrations réalisées pour ce site (blocs Scratch et scène du projet).", "الصور رسوم توضيحية أُنجزت لهذا الموقع (كتل سكراتش ومشهد المشروع)."),
        *[(f"Niveau {i}", f"المستوى {i}") for i in range(1, 7)],
        ("Ces activités permettent aux élèves de combiner plusieurs astuces.", "تتيح هذه الأنشطة للتلاميذ الجمع بين عدة أفكار."),
        # case « Fait » et progression
        ("Version allégée", "نسخة مخففة"), ("Pour les élèves qui ont besoin d'une aide : une tâche réduite, à faire avant ou à la place de l'activité complète.", "للتلاميذ المحتاجين إلى مساعدة: مهمة مخففة تُنجز قبل النشاط الكامل أو بدلا منه."), ("Fait", "تم"), ("Fait ✓", "تم ✓"), ("Marquer comme fait", "علّم النشاط كمنجز"), ("Ta progression :", "تقدّمك:"), ("Effacer ma progression", "مسح تقدّمي"),
        ("Ta progression est enregistrée dans ce navigateur seulement.", "يُحفظ تقدّمك في هذا المتصفح فقط.")]:
        P(ui)
    return dict(levels=levels, blocks=blocks, acts=acts, total=total, title=title, intro=intro), fr
if __name__ == "__main__":
    d, f = export(); print(len(d["acts"]), "activités,", len(f), "traductions", [l["count"] for l in d["levels"]])
