"""Lien avec le programme : « Aide pédagogique – Informatique » (Ministère de l'Éducation, Tunisie, septembre 2025),
domaine « Pensée logique et programmation ».
- données du programme (7e et 8e année), transcrites des pages photographiées : à relire avec le document officiel ;
- analyse automatique des blocs de chaque projet (.sb3) : concepts utilisés et respect des directives de cadrage.
Usage : python3 generateur/programme.py   (depuis la racine du dépôt)"""
import os, json, glob, zipfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)

CONCEPTS = {
 "sequence": ("تسلسل التعليمات", "Séquence d'instructions"),
 "event": ("حدث مُطلِق", "Événement déclencheur"),
 "message": ("بثّ الرسائل", "Diffusion de messages"),
 "loop_n": ("التكرار عددا محددا من المرات", "Répéter un nombre déterminé de fois"),
 "loop_inf": ("التكرار إلى ما لا نهاية", "Répéter indéfiniment"),
 "loop_until": ("التكرار إلى أن يتحقق شرط", "Répéter jusqu'à"),
 "cond_simple": ("شرط (صيغة مختصرة)", "Condition (forme réduite)"),
 "cond_full": ("شرط (صيغة كاملة)", "Condition (forme complète)"),
 "variable": ("متغير عددي", "Variable numérique"),
 "variable_local": ("متغير خاص بالشخصية", "Variable propre au lutin"),
 "input": ("طلب إجابة من المستعمل", "Saisie (demander / réponse)"),
 "mouse_key": ("الفأرة ولوحة المفاتيح", "Souris et clavier"),
 "arith": ("عمليات حسابية ومقارنة", "Opérateurs arithmétiques et comparaison"),
 "random": ("عدد عشوائي", "Nombre aléatoire"),
}
OPS = {
 "event": ["event_whenflagclicked", "event_whenthisspriteclicked", "event_whenkeypressed", "event_whenbroadcastreceived"],
 "message": ["event_broadcast", "event_broadcastandwait", "event_whenbroadcastreceived"],
 "loop_n": ["control_repeat"], "loop_inf": ["control_forever"], "loop_until": ["control_repeat_until"],
 "cond_simple": ["control_if"], "cond_full": ["control_if_else"],
 "variable": ["data_setvariableto", "data_changevariableby", "data_variable"],
 "input": ["sensing_askandwait", "sensing_answer"], "mouse_key": ["sensing_mousex", "sensing_keypressed"],
 "arith": ["operator_add", "operator_subtract", "operator_multiply", "operator_mod", "operator_lt", "operator_gt", "operator_equals", "operator_mathop"],
 "random": ["operator_random"],
}
def analyse(path):
    p = json.loads(zipfile.ZipFile(path).read("project.json"))
    ops = {b["opcode"] for t in p["targets"] for b in t["blocks"].values()}
    found = ["sequence"] + [c for c, lst in OPS.items() if ops & set(lst)]
    if any(t["variables"] for t in p["targets"] if not t["isStage"]): found.append("variable_local")
    # critères de cadrage (programme)
    logic = sorted(ops & {"operator_and", "operator_or", "operator_not"})
    lists = any(t["lists"] for t in p["targets"]) or any(o.startswith("data_") and "list" in o for o in ops)
    modules = sum(1 for o in ops if o == "procedures_definition")
    level = 8 if "variable" in found else 7
    return dict(concepts=found, level=level, logic=logic, lists=bool(lists), modules=modules)

# ---------------- le programme (transcription des pages 7e / 8e « Pensée logique et programmation ») ----------------
LEVELS = {
 7: dict(
  year_ar="السنة السابعة", year_fr="7e année",
  comp_ar="تطوير استراتيجية منطقية لحل المشكلات: حل المشكلات باستعمال لغة برمجة بصرية.",
  comp_fr="Développer une stratégie logique de résolution de problèmes : résoudre des problèmes à l'aide d'un langage de programmation visuelle.",
  parts=[
   ("تحليل مشكلة وتخطيط الحل", "Analyser un problème et planifier une solution", ["تحديد العناصر الأساسية للمشكلة المراد حلها", "استخراج المراحل اللازمة للحل"], ["Identifier les éléments clés du problème à résoudre", "Dégager les étapes nécessaires à la résolution"]),
   ("تنفيذ الحل وتعديله", "Mettre en œuvre et réguler une solution", ["تنفيذ حل باتباع المراحل المحددة", "تقييم نجاعة الحل بمقارنته بالهدف المنشود", "تعديل الحل حسب النتائج المحصل عليها"], ["Mettre en œuvre une solution en suivant les étapes définies", "Évaluer l'efficacité de la solution en la confrontant à l'objectif visé", "Réajuster la solution en fonction des résultats obtenus"]),
   ("بناء برنامج الحل", "Construire un script solution", ["إنشاء برامج وتعديلها باختيار الكتل المناسبة", "استعمال هياكل تكرارية وشرطية بسيطة", "تشغيل برنامج انطلاقا من حدث"], ["Créer et modifier des scripts en sélectionnant les blocs adaptés", "Utiliser des structures itératives et conditionnelles simples", "Déclencher un script à partir d'un événement"]),
   ("اختبار الحل وتحسينه", "Tester et améliorer la solution", ["تنفيذ حل واختباره وتصحيحه وتقييمه"], ["Exécuter, tester, corriger et évaluer une solution"]),
  ],
  know_ar=["مراحل الحل: المشكلة، المعطيات المفيدة، النتيجة المنتظرة، الخوارزمية", "بيئة البرمجة البصرية: برنامج، كتل، شخصية، مسرح، خلفية", "تسلسل التعليمات وحدث مُطلِق", "الهيكل التكراري: التكرار إلى ما لا نهاية أو عددا محددا من المرات", "الهيكل الشرطي: الصيغة المختصرة والصيغة الكاملة"],
  know_fr=["Démarche de résolution : problème, données utiles, résultat attendu, algorithme", "Environnement de programmation visuelle : script, blocs, lutin, scène, arrière-plan", "Séquence d'instructions et événement déclencheur", "Structure itérative : répéter indéfiniment, répéter un nombre déterminé de fois", "Structure conditionnelle : forme réduite et forme complète"],
  cad_ar=["استعمال بيئة برمجة بصرية بالكتل مثل Scratch", "ربط كل إنتاج رقمي بوضعية-مشكلة", "الاقتصار على الشروط البسيطة دون معاملات منطقية (و، أو)"],
  cad_fr=["Utiliser un environnement de programmation visuelle par blocs tel que Scratch", "Relier toute création numérique à une situation-problème", "Se limiter aux conditions simples, sans opérateur logique (ET, OU)"]),
 8: dict(
  year_ar="السنة الثامنة", year_fr="8e année",
  comp_ar="تطوير استراتيجية لحل المشكلات وترجمتها إلى برنامج مهيكل.",
  comp_fr="Développer une stratégie de résolution de problèmes et la traduire en un programme structuré.",
  parts=[
   ("تحليل مشكلة وتفكيكها", "Analyser et décomposer un problème", ["تحليل مشكلة وتفكيكها إلى مشكلات فرعية وتحديد مراحل حلها", "تمثيل استراتيجية الحل في شكل مخطط أو رسم بياني"], ["Analyser un problème, le décomposer en sous-problèmes et identifier les étapes nécessaires à sa résolution", "Représenter la stratégie de résolution sous forme de schéma ou de diagramme"]),
   ("هيكلة البرنامج", "Structurer le programme", ["تصميم برنامج يتضمن متغيرات ووحدات", "إنشاء وحدات واستدعاؤها"], ["Concevoir un programme intégrant des variables et des modules", "Créer et appeler des modules"]),
   ("اختبار الحل وتحسينه", "Tester et améliorer la solution", ["اختبار برنامج وتحديد الأخطاء وإجراء التصحيحات اللازمة", "تحسين الحل حسب النتائج المحصل عليها"], ["Tester un programme, identifier les erreurs et apporter les corrections nécessaires", "Améliorer la solution en fonction des résultats obtenus"]),
  ],
  know_ar=["التحليل: تفكيك مشكلة، مشكلة فرعية، مرحلة حل", "المعطيات: المتغير (الاسم، القيمة، التهيئة، الزيادة)", "الهيكلة: الوحدة واستدعاء الوحدة ومعاملها"],
  know_fr=["Analyse : décomposition d'un problème, sous-problème, étape de résolution", "Données : variable (nom, valeur, initialisation, incrémentation)", "Structuration : module, appel de module, paramètre d'un module"],
  cad_ar=["عدم تقديم المتغيرات والوحدات بشكل معزول بل استجابة لحاجة", "الحرص على وضوح البرنامج وهيكلته", "إعطاء مكانة صريحة لمراحل الاختبار والتصحيح والتحسين", "الاقتصار على المتغيرات العددية", "الاقتصار على ثلاث وحدات على الأكثر في البرنامج"],
  cad_fr=["Ne pas introduire les variables et les modules de manière isolée, mais en réponse à un besoin", "Veiller à la lisibilité et à la structuration du programme", "Accorder une place explicite aux phases de test, de correction et d'optimisation", "Se limiter aux variables numériques", "Limiter le programme à trois modules au maximum"]),
}
GENERAL_FR = "Recommandation générale : prévoir, pour chaque activité, une version allégée et un prolongement, afin que l'écart de maîtrise initiale ne se creuse pas."
GENERAL_AR = "توصية عامة: توفير نسخة مخففة وامتداد لكل نشاط حتى لا يتسع الفارق في التمكن الأولي."
FICHE = {"quiz": "quiz", "math": "math", "memory": "memory", "order": "order", "reflex": "reflex", "catch": "catch"}

def build():
    projects = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "scratch", "*.sb3"))):
        k = os.path.basename(f)[:-4]; projects["conte_" + k] = dict(kind="conte", **analyse(f))
    for f in sorted(glob.glob(os.path.join(ROOT, "jeux", "jeu_*.sb3"))):
        k = os.path.basename(f)[4:-4]; projects["jeu_" + k] = dict(kind="jeu", **analyse(f))
    data = dict(concepts={k: dict(ar=a, fr=f) for k, (a, f) in CONCEPTS.items()},
                levels={str(n): dict(year_ar=L["year_ar"], year_fr=L["year_fr"], comp_ar=L["comp_ar"], comp_fr=L["comp_fr"],
                                     parts=[dict(t_ar=a, t_fr=b, i_ar=c, i_fr=d) for a, b, c, d in L["parts"]], know_ar=L["know_ar"], know_fr=L["know_fr"], cad_ar=L["cad_ar"], cad_fr=L["cad_fr"]) for n, L in LEVELS.items()},
                general_ar=GENERAL_AR, general_fr=GENERAL_FR, projects=projects)
    json.dump(data, open(os.path.join(HERE, "programme.json"), "w", encoding="utf-8"), ensure_ascii=False)
    return data

if __name__ == "__main__":
    d = build(); P = d["projects"]
    bad = {k: v for k, v in P.items() if v["logic"] or v["lists"] or v["modules"] > 3}
    n7 = sum(1 for v in P.values() if v["level"] == 7); n8 = len(P) - n7
    print("projets analysés :", len(P), "| niveau 7e :", n7, "| niveau 8e :", n8, "| hors cadrage :", bad or "aucun")
