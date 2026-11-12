"""Planning des séances Scratch : progression cumulative des notions sur les trois années (7e, 8e, 9e).
Les séances sont celles du module « programmation » de la répartition annuelle (seances.py : 6 séances en 7e, 10 en 8e, 14 en 9e, de 60 minutes).
Chaque séance : notions nouvelles / approfondies / réinvesties (calculées), activités de la collection (principale, entraînement, défi), jeux, niveau d'autonomie
(guidé -> semi-guidé -> autonome), démarche minutée sur 60 minutes, acquis et trace écrite.
Contrôle de cohérence : aucune activité ni aucun jeu proposé à « jouer / programmer » ne demande une notion pas encore introduite (validate()).
Chaque texte est un couple (français, arabe).   Usage : python3 generateur/planning.py  (contrôle + résumé)"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import seances as S, activites as A, activites_specs as SP

# ----------------------------------------------------------------------------- notions (ordre d'apparition)
NOTIONS = [
 ("seq", "Séquence d'instructions", "تسلسل التعليمات"), ("event", "Événements déclencheurs", "الأحداث المطلِقة"), ("move", "Déplacements et rotations", "الحركة والدوران"),
 ("look", "Apparence : dire, costumes, décors", "المظهر: الكلام والأزياء والخلفيات"), ("coord", "Coordonnées x et y", "الإحداثيان س وص"), ("msg", "Messages entre lutins", "الرسائل بين اللاعبين"),
 ("sound", "Sons", "الأصوات"), ("repeatn", "Répéter n fois", "التكرار عددا محددا"), ("forever", "Répéter indéfiniment", "التكرار باستمرار"), ("pen", "Dessiner avec le stylo", "الرسم بالقلم"),
 ("sense", "Capteurs : toucher, souris, distance, touches", "المستشعرات: اللمس والفأرة والمسافة والمفاتيح"), ("if", "Condition simple (si… alors)", "الشرط البسيط (إذا… فإن)"), ("ifelse", "Condition complète (si… sinon)", "الشرط الكامل (إذا… وإلا)"),
 ("project", "Projet : concevoir, réaliser, présenter", "المشروع: التصميم والإنجاز والعرض"),
 ("decomp", "Décomposer un problème (diagramme)", "تجزئة مشكل (مخطط)"), ("read", "Lire et prévoir le comportement d'un script", "قراءة سكربت وتوقّع سلوكه"), ("op", "Opérateurs et comparaisons", "المعاملات والمقارنات"),
 ("var", "Variable numérique", "المتغير العددي"), ("rand", "Nombre aléatoire", "العدد العشوائي"), ("input", "Demander et utiliser une réponse", "طلب إجابة واستعمالها"),
 ("module", "Module (bloc personnalisé)", "الوحدة (كتلة خاصة)"), ("param", "Paramètre d'un module", "معامل وحدة"), ("debug", "Tester et corriger", "الاختبار والتصحيح"),
 ("until", "Répéter jusqu'à ce que…", "التكرار حتى يتحقق شرط"), ("opt", "Améliorer et optimiser", "التحسين والتجويد"),
 ("inout", "Entrées, traitement, sorties", "المدخلات والمعالجة والمخرجات"), ("sensact", "Capteurs et actionneurs d'un objet", "مستشعرات ومنفّذات شيء"), ("share", "Remixer, citer et partager", "إعادة الصياغة والاعتماد والمشاركة"),
]
NID = [n[0] for n in NOTIONS]; NT = {n[0]: (n[1], n[2]) for n in NOTIONS}

# ----------------------------------------------------------------------------- notions techniques d'une activité, lues dans son script dessiné
B2N = {}
for k in "flag arrowr space click".split(): B2N[k] = "event"
for k in "recv send".split(): B2N[k] = "msg"
for k in "move turnr turnl bounce pointmouse pointdir".split(): B2N[k] = "move"
for k in "goto glide chx chy setx sety".split(): B2N[k] = "coord"
for k in "say costume backdrop show hide size ghost bdover".split(): B2N[k] = "look"
for k in "play playwait".split(): B2N[k] = "sound"
for k in "keyd touching touchcolor mousex dist timer resett".split(): B2N[k] = "sense"
for k in "ask answer".split(): B2N[k] = "input"
for k in "eq gt lt join".split(): B2N[k] = "op"
B2N.update(rand="rand", setv="var", chv="var", define="module", callmod="module", clone="clone", whenclone="clone", delclone="clone", listadd="list", listitem="list")
for k in "pendown penup clear pensize pencolor stamp".split(): B2N[k] = "pen"
VARW = r"score|vies|niveau|état|sauts|mission|faim|\bor\b|soldats|clés|humidité|vitesse|meilleur"
def tags_text(t, acc):
    t = t.lower()
    if re.search(r"touche|pressée|distance|chronomètre|couleur|souris", t): acc.add("sense")
    if re.search(r"[<>=÷×]", t): acc.add("op")
    if "réponse" in t: acc.add("input")
    if re.search(VARW, t): acc.add("var")
    if re.search(r"\bx\b|\by\b", t): acc.add("coord")
    if "aléatoire" in t: acc.add("rand")
def walk(items, acc):
    for it in items:
        if isinstance(it, list): walk(it, acc); continue
        k = it[0]
        if k == "B":
            if it[1] in B2N: acc.add(B2N[it[1]])
            fr = it[2] or ""
            if fr: tags_text(fr, acc) if re.search(r"aléatoire|÷|×|" + VARW, fr.lower()) else None
        elif k == "F": acc.add("forever"); walk(it[1], acc)
        elif k == "R": acc.add("repeatn"); walk(it[2], acc)
        elif k == "IF": acc.add("if"); tags_text(it[1][0], acc); walk(it[2], acc)
        elif k == "IFE": acc |= {"if", "ifelse"}; tags_text(it[1][0], acc); walk(it[2], acc); walk(it[3], acc)
        elif k == "U": acc.add("until"); tags_text(it[1][0], acc); walk(it[2], acc)
        elif k == "WU": acc.add("until"); tags_text(it[1][0], acc)
def act_notions(n):
    acc = {"seq"}; walk(SP.SPECS[n]["script"], acc); return acc
ACT = {a["n"]: a for a in A.ACTS}
ACT_N = {n: act_notions(n) for n in ACT}
GAMES = {  # clé -> (titre fr, titre ar, notions techniques, id de fiche)
 "sindbad": ("Attrape les poissons", "اصطد الأسماك", {"event", "forever", "if", "sense", "var", "op", "rand", "coord", "look", "sound"}, "catch"),
 "course": ("Course : évite les voitures", "سباق السيارات: تفادَ السيارات", {"event", "forever", "if", "sense", "var", "op", "rand", "coord", "look", "sound"}, "course"),
 "saut": ("Le chameau saute-buissons", "الجمل يقفز: تفادَ الشجيرات", {"event", "forever", "if", "sense", "var", "op", "rand", "coord", "look", "sound"}, "saut"),
 "labyrinthe": ("Le labyrinthe de la souris", "متاهة الفأرة", {"event", "forever", "if", "sense", "var", "op", "coord", "look", "sound"}, "labyrinthe")}
STORY_N = {"event", "look", "msg", "move", "sound", "seq"}
STORIES = {"djeha": ("Jeha et l'âne", "جحا والحمار"), "cinderella": ("Cendrillon", "سندريلا"), "layla": ("Layla et le loup", "ليلى والذئب")}

# ----------------------------------------------------------------------------- libellés
TYPES = {"decouverte": ("Découverte", "اكتشاف"), "manip": ("Manipulation", "تطبيق"), "projet": ("Projet", "مشروع"), "eval": ("Évaluation", "تقييم")}
AUTO = {"guide": ("Guidé", "موجَّه"), "semi": ("Semi-guidé", "شبه موجَّه"), "auto": ("Autonome", "مستقل")}
YEARLBL = {"7": ("7e année", "السنة السابعة"), "8": ("8e année", "السنة الثامنة"), "9": ("9e année", "السنة التاسعة")}
def Q(fr, ar): return (fr, ar)

# ----------------------------------------------------------------------------- le planning : (année, n° de séance de la répartition annuelle) -> contenu
def P(new=(), deep=(), core=(), support=(), challenge=(), games=(), auto="semi", acq=None, extra=None, hook=None):
    return dict(new=list(new), deep=list(deep), core=list(core), support=list(support), challenge=list(challenge), games=list(games), auto=auto, acq=acq, extra=extra, hook=hook)
PLAN = {
 "7": {
  22: P(new=["seq"], auto="guide", hook=Q("Un élève doit aller de la porte au tableau en suivant uniquement des cartes-instructions : que se passe-t-il si l'on change l'ordre des cartes ?", "على تلميذ أن يذهب من الباب إلى السبورة بالاعتماد على بطاقات التعليمات فقط: ماذا يحدث إذا غيّرنا ترتيب البطاقات؟"),
     extra=Q("Jeu du robot : un élève « robot » exécute les cartes-instructions écrites par ses camarades sur un quadrillage tracé au sol ; on corrige les suites qui échouent.", "لعبة الروبوت: تلميذ «روبوت» ينفّذ بطاقات التعليمات التي كتبها زملاؤه على شبكة مرسومة على الأرض، ونصحّح السلاسل الفاشلة."),
     acq=[Q("Je sais décrire un problème par ses données, son résultat et ses étapes dans l'ordre.", "أستطيع وصف مشكل بمعطياته ونتيجته ومراحله بالترتيب.")]),
  23: P(new=["event", "move", "look"], core=[1], support=[2, 3], challenge=[4], auto="guide",
     acq=[Q("Je sais assembler des blocs pour faire avancer, tourner et parler un lutin.", "أستطيع تركيب كتل لتحريك لاعب وإدارته وجعله يتكلم.")]),
  24: P(new=["coord", "msg", "sound"], core=[9], support=[6, 5], challenge=[19], games=[("story", "djeha", "play")], auto="guide",
     acq=[Q("Je sais choisir l'événement qui déclenche un script (drapeau, clic, touche, message).", "أستطيع اختيار الحدث الذي يطلق سكربتا (العلم والنقر والمفتاح والرسالة).")]),
  25: P(new=["repeatn", "forever", "pen"], core=[8], support=[7, 10, 16], challenge=[12, 11], auto="semi",
     acq=[Q("Je sais choisir entre « répéter n fois » et « répéter indéfiniment » et raccourcir un script avec une boucle.", "أستطيع الاختيار بين «كرّر n مرات» و«كرّر باستمرار» وتقصير سكربت بحلقة.")]),
  26: P(new=["sense", "if", "ifelse"], core=[14], support=[34], challenge=[23], auto="semi",
     extra=Q("Défi complémentaire : transformer le « si… alors » de l'activité « Détecter une collision » en « si… alors… sinon » (si le chat ne touche pas la pomme, il dit « Cherche ! »).", "تحدٍّ إضافي: حوّل «إذا… فإن» في نشاط «كشف الاصطدام» إلى «إذا… فإن… وإلا» (إذا لم تلمس القطة التفاحة تقول «ابحث!»)."),
     acq=[Q("Je sais utiliser « si… alors » avec un capteur (toucher) et je connais la forme « si… sinon ».", "أستطيع استعمال «إذا… فإن» مع مستشعر (اللمس) وأعرف صيغة «إذا… وإلا».")]),
  27: P(new=["project"], core=[51], games=[("story", "cinderella", "play"), ("story", "layla", "play")], auto="auto",
     acq=[Q("Je sais réaliser un petit projet interactif et le présenter.", "أستطيع إنجاز مشروع تفاعلي صغير وعرضه.")]),
 },
 "8": {
  18: P(new=["decomp"], core=[58], games=[("game", "sindbad", "watch")], auto="guide",
     acq=[Q("Je sais découper un problème en étapes et les représenter par un diagramme.", "أستطيع تجزئة مشكل إلى مراحل وتمثيلها بمخطط.")]),
  19: P(new=["read", "op"], core=[56], support=[15, 13], challenge=[62], auto="guide",
     acq=[Q("Je sais lire un script et prévoir ce qu'il fait ; je sais comparer deux valeurs dans une condition.", "أستطيع قراءة سكربت وتوقّع ما يفعله، وأقارن قيمتين في شرط.")]),
  20: P(new=["var"], core=[18], support=[28], challenge=[22], auto="guide",
     acq=[Q("Je sais créer une variable, l'initialiser et l'augmenter (compter des points).", "أستطيع إنشاء متغير وتهيئته وزيادته (عدّ النقاط).")]),
  21: P(new=["rand", "input"], core=[21], support=[20], challenge=[32], games=[("game", "sindbad", "play")], auto="semi",
     acq=[Q("Je sais utiliser un nombre aléatoire et la réponse du joueur dans un programme avec variable.", "أستطيع استعمال عدد عشوائي وإجابة اللاعب في برنامج بمتغير.")]),
  22: P(new=["module"], core=[59], support=[10], auto="semi",
     acq=[Q("Je sais regrouper des blocs dans un module et l'appeler.", "أستطيع جمع كتل في وحدة واستدعاءها.")]),
  23: P(new=["param"], core=[60], support=[59], challenge=[55], auto="semi",
     acq=[Q("Je sais ajouter un paramètre à un module pour le rendre plus général.", "أستطيع إضافة معامل إلى وحدة لجعلها أعمّ.")]),
  24: P(new=["debug"], core=[57], support=[56], challenge=[25], games=[("game", "course", "play")], auto="semi",
     acq=[Q("Je sais tester un programme, repérer une erreur, la corriger puis retester.", "أستطيع اختبار برنامج وتحديد خطأ وتصحيحه ثم إعادة الاختبار.")]),
  25: P(new=["opt", "until"], core=[61], support=[17, 29], challenge=[35], games=[("game", "saut", "play")], auto="semi",
     acq=[Q("Je sais améliorer une solution (moins de blocs, plus de fonctions) et justifier mon choix.", "أستطيع تحسين حل (كتل أقل ووظائف أكثر) وتبرير اختياري.")]),
  26: P(deep=["project"], support=[30, 33], challenge=[24, 27], games=[("game", "labyrinthe", "play")], auto="auto",
     acq=[Q("Je sais concevoir un petit jeu avec une variable et au plus trois modules.", "أستطيع تصميم لعبة صغيرة بمتغير وثلاث وحدات على الأكثر.")]),
  27: P(auto="auto", acq=[Q("Je sais présenter mon projet et expliquer mes choix.", "أستطيع عرض مشروعي وشرح اختياراتي.")]),
 },
 "9": {
  1: P(core=[56], auto="guide", extra=Q("Comparer Scratch, mBlock et App Inventor pour un même problème (tableau : facilité, possibilités, matériel).", "مقارنة سكراتش وmBlock وApp Inventor لمشكل واحد (جدول: السهولة والإمكانات والعتاد)."),
     acq=[Q("Je sais comparer deux environnements de programmation et justifier mon choix.", "أستطيع مقارنة بيئتي برمجة وتبرير اختياري.")]),
  2: P(new=["inout"], core=[20], support=[58], challenge=[52], auto="guide",
     acq=[Q("Je sais décrire un problème par ses entrées, son traitement et ses sorties.", "أستطيع وصف مشكل بمدخلاته ومعالجته ومخرجاته.")]),
  3: P(core=[11], support=[12, 16], challenge=[24], auto="semi",
     acq=[Q("Je sais combiner séquence, événement, condition et boucle pour résoudre un problème.", "أستطيع الجمع بين التسلسل والحدث والشرط والحلقة لحل مشكل.")]),
  4: P(deep=["var", "module"], core=[28], support=[59, 60], challenge=[29], auto="semi",
     acq=[Q("Je sais structurer un programme avec des variables et des modules.", "أستطيع هيكلة برنامج بمتغيرات ووحدات.")]),
  5: P(new=["sensact"], core=[62], support=[17, 15], auto="semi",
     acq=[Q("Je sais lire la valeur d'un capteur (simulé) et décider selon cette valeur.", "أستطيع قراءة قيمة مستشعر (مُحاكى) واتخاذ قرار بحسبها.")]),
  6: P(core=[64], support=[62], auto="semi",
     acq=[Q("Je sais contrôler un actionneur (simulé) : feu, porte, arrosage.", "أستطيع التحكم في منفّذ (مُحاكى): ضوء أو باب أو سقي.")]),
  7: P(core=[65], support=[64], auto="semi",
     extra=Q("Défi complémentaire : réunir un capteur et un actionneur de ton choix dans un petit système (mesurer, décider, agir) et le présenter.", "تحدٍّ إضافي: اجمع مستشعرا ومنفّذا من اختيارك في نظام صغير (قياس وقرار وفعل) واعرضه."),
     acq=[Q("Je sais relier un capteur à un actionneur : mesurer, décider, agir.", "أستطيع ربط مستشعر بمنفّذ: القياس والقرار والفعل.")]),
  8: P(deep=["debug", "opt"], core=[61], support=[57, 56], games=[("game", "course", "play")], auto="semi",
     acq=[Q("Je sais tester une solution, la corriger et l'optimiser.", "أستطيع اختبار حل وتصحيحه وتحسينه.")]),
  9: P(games=[("game", "saut", "watch"), ("game", "course", "watch")], auto="auto",
     extra=Q("Comparer deux solutions du site selon des critères (lisibilité, nombre de blocs, jouabilité) et défendre son choix devant la classe.", "مقارنة حلّين من الموقع بحسب معايير (الوضوح وعدد الكتل وسهولة اللعب) والدفاع عن الاختيار أمام القسم."),
     acq=[Q("Je sais argumenter le choix d'une solution avec des critères.", "أستطيع تبرير اختيار حل بمعايير.")]),
  10: P(deep=["project"], core=[58], support=[50], challenge=[31, 36, 45, 46, 49, 54], games=[("game", "labyrinthe", "watch")], auto="auto",
     acq=[Q("Je sais choisir un problème et concevoir ma solution (diagramme, cahier des charges).", "أستطيع اختيار مشكل وتصميم حلّي (مخطط وكراس شروط).")]),
  11: P(deep=["project"], core=[57], support=[30], challenge=[37, 38, 39, 47], auto="auto",
     acq=[Q("Je sais réaliser mon projet par étapes et le tester.", "أستطيع إنجاز مشروعي على مراحل واختباره.")]),
  12: P(deep=["project", "opt"], core=[61], support=[41, 35], auto="auto",
     acq=[Q("Je sais améliorer mon projet et argumenter mes choix.", "أستطيع تحسين مشروعي وتبرير اختياراتي.")]),
  13: P(auto="auto", acq=[Q("Je sais mobiliser mes acquis de programmation visuelle et d'objets.", "أستطيع توظيف مكتسباتي في البرمجة المرئية والأشياء.")]),
  14: P(new=["share"], core=[63], support=[30], auto="auto",
     acq=[Q("Je sais partager un projet en citant son auteur et choisir un espace adapté.", "أستطيع مشاركة مشروع مع ذكر صاحبه واختيار فضاء مناسب.")]),
 },
}
# 9e : pas de Scratch (aide pédagogique 2026 : objets programmables et applications mobiles) -> plus d'activités ni de jeux Scratch dans le planning de la 9e
for _s, _p in PLAN["9"].items(): _p["core"] = []; _p["support"] = []; _p["challenge"] = []; _p["games"] = []
PLAN["9"][1]["extra"] = Q("Comparer MakeCode (micro:bit), mBlock et App Inventor pour un même problème (tableau : facilité, possibilités, matériel).", "مقارنة MakeCode (micro:bit) وmBlock وApp Inventor لمشكل واحد (جدول: السهولة والإمكانات والعتاد).")
# ----------------------------------------------------------------------------- traductions arabes des séances de la répartition annuelle
AR_TXT = {
 ("7", 22): ("حلّ مشكل دون حاسوب", "تحديد المشكل والمعطيات المفيدة والنتيجة المنتظرة واستخراج المراحل", "مراحل الحل (المشكل، المعطيات، النتيجة، المراحل)."),
 ("7", 23): ("اكتشاف سكراتش: اللاعب والمنصة والكتل", "التعرف على بيئة البرمجة المرئية وبناء تسلسل من التعليمات", "رسم واجهة سكراتش."),
 ("7", 24): ("إطلاق سكربت: الأحداث", "إطلاق سكربت انطلاقا من حدث", "جدول: الحدث ← الأثر."),
 ("7", 25): ("التكرار: الحلقات", "استعمال «كرّر باستمرار» و«كرّر n مرات»", "البنيتان التكراريتان."),
 ("7", 26): ("اتخاذ القرار: الشروط البسيطة", "استعمال «إذا… فإن» و«إذا… فإن… وإلا» دون معامل منطقي", "الصيغة المختصرة والصيغة الكاملة للشرط."),
 ("7", 27): ("مشروع: إنشاء قصة تفاعلية وعرضها", "إنجاز مشروع يضم شخصيات وخلفيات وأحداثا وشروطا وتكرارات، واختباره وتصحيحه", "بطاقة المشروع (المراحل، الاختبارات، التصحيحات)."),
 ("8", 18): ("تحليل مشكل وتجزئته", "تجزئة مشكل إلى مشكلات فرعية وتمثيل الاستراتيجية بمخطط", "مخطط الحل."),
 ("8", 19): ("تذكير بسكراتش: السكربتات والأحداث والحلقات والشروط", "تدعيم مكتسبات البرمجة المرئية", "بطاقة ملخصة للبنى."),
 ("8", 20): ("المتغيرات: الاسم والقيمة والتهيئة والزيادة", "استعمال متغير عددي لتلبية حاجة (النقاط)", "بطاقة «المتغير»."),
 ("8", 21): ("برنامج بمتغير: اللعبة", "تصميم برنامج يتضمن متغيرا", "برنامج موثَّق."),
 ("8", 22): ("الوحدات: الإنشاء والاستدعاء", "إنشاء وحدة («كتلتي») واستدعاؤها", "بطاقة «الوحدة»."),
 ("8", 23): ("الوحدات والمعاملات", "استعمال معامل في وحدة", "مثال لوحدة بمعامل."),
 ("8", 24): ("الاختبار وتحديد الأخطاء وتصحيحها", "اختبار برنامج وتحديد الأخطاء وتصحيحها", "سجل الاختبارات والتصحيحات."),
 ("8", 25): ("تحسين الحل", "تحسين الحل بحسب النتائج المحصَّل عليها", "قائمة التحسينات المبرَّرة."),
 ("8", 26): ("مشروع: تصميم لعبة منظَّمة", "تصميم برنامج بمتغير ووحدة (ثلاث وحدات على الأكثر)", "ملف المشروع."),
 ("8", 27): ("تقييم المشروع", "عرض المشروع وتقييمه", "شبكة تقييم المشروع."),
 ("9", 1): ("اختيار بيئة العمل", "اختيار مدروس بين بيئة برمجة مرئية وبيئة روبوتيك", "جدول مقارنة."),
 ("9", 2): ("تحليل مشكل: المدخلات والمخرجات والمعالجة", "تحليل مشكل بمدخلاته ومخرجاته ومراحل معالجته", "مخطط: مدخلات / معالجة / مخرجات."),
 ("9", 3): ("المفاهيم الأساسية: التسلسل والأحداث والشروط والحلقات", "تطبيق المفاهيم الأساسية للبرمجة", "بطاقة ملخصة."),
 ("9", 4): ("المتغيرات والوحدات", "هيكلة برنامج بمتغيرات ووحدات", "برنامج منظَّم."),
 ("9", 5): ("برمجة شيء: المستشعرات", "استغلال معطيات مستشعر", "جدول: المستشعر ← المعطى."),
 ("9", 6): ("برمجة شيء: المنفّذات", "التحكم في منفّذ", "جدول: المنفّذ ← الأثر."),
 ("9", 7): ("التحكم في شيء انطلاقا من برنامج", "التحكم في شيء بواسطة برنامج", "برنامج معلَّق عليه."),
 ("9", 8): ("اختبار حل وتحسينه", "اختبار حل وتحسينه", "سجل الاختبارات."),
 ("9", 9): ("تبرير اختيارات الحلول", "تبرير اختيار حل", "بطاقة الحجج."),
 ("9", 10): ("مشروع: تصميم مشروع برمجة", "اختيار مشكل وتصميم حل", "كراس الشروط."),
 ("9", 11): ("مشروع: الإنجاز والاختبار", "إنجاز مشروعه واختباره", "البرنامج وسجل الاختبارات."),
 ("9", 12): ("مشروع: التحسين والتبرير", "تحسين مشروعه وتبرير اختياراته", "ملف المشروع."),
 ("9", 13): ("تقييم: البرمجة المرئية والأشياء", "توظيف مكتسبات البرمجة", "حصيلة المكتسبات والعلاج."),
 ("9", 14): ("نشر المشروع ومشاركته", "اختيار فضاء مناسب لمشاركة مشاريعه", "شبكة تقييم ورابط المشاركة."),
}
YEAR_ORDER = ["7", "8", "9"]
def order(y): return sorted(PLAN[y])

# ----------------------------------------------------------------------------- démarche d'une séance (60 minutes), en deux langues
def ql(pairs): return ", ".join(f"« {a} »" for a, _ in pairs), "، ".join(f"«{b}»" for _, b in pairs)
def atitle(n): return (ACT[n]["title"][0], ACT[n]["title"][1])
def gtitle(kind, key): return ((GAMES[key][0], GAMES[key][1]) if kind == "game" else STORIES[key])
def nlist(ids): return ", ".join(NT[i][0] for i in ids), "، ".join(NT[i][1] for i in ids)
PH3 = {"guide": ("Découverte guidée", "اكتشاف موجَّه"), "semi": ("Réalisation semi-guidée", "إنجاز شبه موجَّه"), "auto": ("Réalisation autonome", "إنجاز مستقل")}
def phases(y, s, p, typ, new, deep, re_, trace, obj):
    """-> [(titre fr, titre ar, minutes, texte fr, texte ar)] ; la somme des durées est toujours 60"""
    core = p["core"]; sup = p["support"]; chal = p["challenge"]; games = p["games"]
    c = atitle(core[0]) if core else None
    if typ == "eval" and not core:
        return [("Installation et consignes", "التهيئة والتعليمات", 5, "Distribuer la grille d'évaluation et lire les consignes.", "توزيع شبكة التقييم وقراءة التعليمات."),
                ("Présentation ou épreuve individuelle", "العرض أو الاختبار الفردي", 40, "Chaque élève présente son travail (2 minutes) et explique un choix, ou réalise l'épreuve seul ; l'enseignant remplit la grille : fonctionnement, notions utilisées, tests, clarté.", "يعرض كل تلميذ عمله (دقيقتان) ويشرح اختيارا، أو ينجز الاختبار وحده؛ ويملأ الأستاذ الشبكة: الاشتغال والمفاهيم المستعملة والاختبارات والوضوح."),
                ("Correction collective", "التصحيح الجماعي", 10, "Corriger avec la classe : repérer les erreurs fréquentes et les réussites.", "التصحيح مع القسم: تحديد الأخطاء الشائعة والنجاحات."),
                ("Remédiation", "العلاج", 5, "Identifier les élèves à accompagner et prévoir une activité de remédiation (voir la collection d'activités).", "تحديد التلاميذ المحتاجين إلى مرافقة وبرمجة نشاط علاجي (انظر مجموعة الأنشطة).")]
    if typ == "projet":
        insp = [x for x in sup + chal]; gl = [gtitle(k, g) for k, g, m in games]
        ideas_fr = ("Idées et inspirations : " + ql([atitle(n) for n in insp])[0] + ".") if insp else ""
        ideas_ar = ("أفكار وإلهام: " + ql([atitle(n) for n in insp])[1] + ".") if insp else ""
        mod_fr = (" Modèles : " + ql(gl)[0] + ".") if gl else ""; mod_ar = (" نماذج: " + ql(gl)[1] + ".") if gl else ""
        if y == "7": d2 = ("Écrire le scénario : les scènes, les personnages, les événements et ce qui doit se répéter ou dépendre d'une condition.", "كتابة السيناريو: المشاهد والشخصيات والأحداث وما يجب أن يتكرر أو يتوقف على شرط.")
        else: d2 = ("Dessiner le diagramme de la solution (étapes, variables, modules) et choisir un projet de base (quiz, attrape-objets, calcul mental, mémoire, scènes à ordonner).", "رسم مخطط الحل (المراحل والمتغيرات والوحدات) واختيار مشروع أساسي (اختبار، التقاط أشياء، حساب ذهني، ذاكرة، ترتيب مشاهد).")
        return [("Rappel et cahier des charges", "تذكير وكراس الشروط", 10, "Rappeler les notions acquises et le cahier des charges du projet." + mod_fr, "تذكير بالمفاهيم المكتسبة وبكراس شروط المشروع." + mod_ar),
                ("Conception", "التصميم", 10, *d2),
                ("Réalisation", "الإنجاز", 25, "Chaque élève ou binôme réalise son projet ; l'enseignant accompagne par des questions plutôt que par des solutions." + (f" Activité d'appui : « {c[0]} »." if c else "") + (" " + ideas_fr if ideas_fr else ""),
                 "ينجز كل تلميذ أو ثنائي مشروعه؛ ويرافق الأستاذ بالأسئلة لا بالحلول." + (f" نشاط مساند: «{c[1]}»." if c else "") + (" " + ideas_ar if ideas_ar else "")),
                ("Tests croisés", "اختبارات متبادلة", 10, "Échanger les projets : un camarade teste avec une grille et note une erreur ou une amélioration.", "تبادل المشاريع: يختبر زميل بواسطة شبكة ويدوّن خطأ أو تحسينا."),
                ("Bilan", "الحصيلة", 5, f"Noter ce qui est réussi et ce qui reste à faire ; trace écrite : {trace[0]}", f"تدوين ما نجح وما بقي إنجازه؛ الأثر المكتوب: {trace[1]}")]
    out = []
    # 1. rappel
    if re_:
        r = nlist(re_); out.append(("Rappel", "تذكير", 5, f"Réactiver les notions des séances précédentes : {r[0]}. Question flash : prévoir le résultat d'un petit script déjà vu.", f"تنشيط مكتسبات الحصص السابقة: {r[1]}. سؤال سريع: توقّع نتيجة سكربت صغير سبق أن رأيناه."))
    else: out.append(("Rappel", "تذكير", 5, "Accueil, rappel des règles de travail sur ordinateur et présentation de l'objectif de la séance.", "استقبال التلاميذ وتذكير بقواعد العمل على الحاسوب وتقديم هدف الحصة."))
    # 2. situation déclenchante
    watch = [gtitle(k, g) for k, g, m in games if m == "watch"]
    if p["hook"]: out.append(("Situation déclenchante", "وضعية الانطلاق", 10, *p["hook"]))
    elif watch: out.append(("Situation déclenchante", "وضعية الانطلاق", 10, f"Regarder la vidéo du jeu « {watch[0][0]} » et demander : que doit faire le programme ? Lister les étapes au tableau.", f"مشاهدة فيديو اللعبة «{watch[0][1]}» ثم السؤال: ماذا يجب أن يفعل البرنامج؟ إحصاء المراحل على السبورة."))
    elif c: out.append(("Situation déclenchante", "وضعية الانطلاق", 10, f"Montrer l'image « après exécution » de l'activité « {c[0]} » et demander : comment l'obtenir avec des blocs ? Recueillir les idées sans les corriger.", f"عرض صورة «بعد التنفيذ» للنشاط «{c[1]}» والسؤال: كيف نحصل عليها بالكتل؟ جمع الأفكار دون تصحيحها."))
    else: out.append(("Situation déclenchante", "وضعية الانطلاق", 10, f"Poser le problème de la séance : {obj[0]}.", f"طرح مشكل الحصة: {obj[1]}."))
    # 3. découverte / réalisation
    t3 = PH3[p["auto"]]
    if c:
        d = {"guide": (f"Réaliser ensemble l'activité « {c[0]} » en suivant les étapes de sa page ; l'enseignant modélise au vidéoprojecteur.", f"إنجاز النشاط «{c[1]}» جماعيا باتباع مراحل صفحته؛ يشرح الأستاذ على جهاز العرض."),
             "semi": (f"Chaque élève réalise « {c[0]} » à partir de l'objectif et du résultat attendu ; les étapes ne sont ouvertes qu'à la demande.", f"ينجز كل تلميذ «{c[1]}» انطلاقا من الهدف والنتيجة المنتظرة؛ ولا تُفتح المراحل إلا عند الحاجة."),
             "auto": (f"Chaque élève réalise « {c[0]} » seul, à partir du seul résultat attendu ; l'enseignant observe et ne donne que des indices.", f"ينجز كل تلميذ «{c[1]}» وحده انطلاقا من النتيجة المنتظرة فقط؛ يلاحظ الأستاذ ولا يقدّم إلا تلميحات.")}[p["auto"]]
        out.append((t3[0], t3[1], 15, *d))
    elif p["extra"]: out.append(("Activité de la séance", "نشاط الحصة", 15, *p["extra"]))
    else: out.append((t3[0], t3[1], 15, f"Travail guidé sur le sujet de la séance : {obj[0]}.", f"عمل موجَّه حول موضوع الحصة: {obj[1]}."))
    # 4. entraînement
    fr, ar = [], []
    if sup: q = ql([atitle(n) for n in sup]); fr.append(f"Pour s'entraîner : {q[0]}."); ar.append(f"للتدرّب: {q[1]}.")
    if chal: q = ql([atitle(n) for n in chal]); fr.append(f"Défi : {q[0]}."); ar.append(f"تحدٍّ: {q[1]}.")
    for k, g, m in games:
        if m == "play":
            t = gtitle(k, g)
            if k == "game": fr.append(f"Jeu : jouer à « {t[0]} », puis lire et modifier son script."); ar.append(f"لعبة: اللعب «{t[1]}» ثم قراءة سكربتها وتعديله.")
            else: fr.append(f"Conte : ouvrir « {t[0]} » et repérer les scripts de la séance."); ar.append(f"قصة: فتح «{t[1]}» وتحديد سكربتات الحصة.")
    if p["extra"] and c: fr.append(p["extra"][0]); ar.append(p["extra"][1])
    if not fr:
        if p["extra"] and not c: fr.append("Variantes : changer le trajet ou les cartes, échanger les suites d'instructions entre binômes, tester et corriger."); ar.append("متغيرات: تغيير المسار أو البطاقات وتبادل سلاسل التعليمات بين الثنائيات واختبارها وتصحيحها.")
        else: fr.append("Reformuler la démarche, échanger les productions entre binômes, tester et corriger."); ar.append("إعادة صياغة السير وتبادل الإنجازات بين الثنائيات واختبارها وتصحيحها.")
    if core or sup or chal: fr.append("Chaque élève coche « Fait » à son rythme."); ar.append("يعلّم كل تلميذ «تم» بحسب وتيرته.")
    out.append(("Entraînement différencié", "تدريب متمايز", 20, " ".join(fr), " ".join(ar)))
    # 5. mise en commun
    if new: n_ = nlist(new); out.append(("Mise en commun et trace écrite", "المقاسمة والأثر المكتوب", 10, f"Faire expliquer avec leurs mots : {n_[0]}. Institutionnaliser, puis écrire la trace : {trace[0]}", f"جعل التلاميذ يشرحون بكلماتهم: {n_[1]}. ثم الصياغة النهائية فالأثر المكتوب: {trace[1]}"))
    elif deep: n_ = nlist(deep); out.append(("Mise en commun et trace écrite", "المقاسمة والأثر المكتوب", 10, f"Faire expliquer ce qui a été approfondi : {n_[0]}. Institutionnaliser, puis écrire la trace : {trace[0]}", f"جعل التلاميذ يشرحون ما تم تعميقه: {n_[1]}. ثم الصياغة النهائية فالأثر المكتوب: {trace[1]}"))
    else: out.append(("Mise en commun et trace écrite", "المقاسمة والأثر المكتوب", 10, f"Faire le bilan de la séance avec la classe ; trace écrite : {trace[0]}", f"حصيلة الحصة مع القسم؛ الأثر المكتوب: {trace[1]}"))
    return out

# ----------------------------------------------------------------------------- construction + contrôle de cohérence
def build():
    known, rows, uses = set(), {}, {n: [] for n in ACT}
    for y in YEAR_ORDER:
        rows[y] = []
        for k, s in enumerate(order(y), 1):
            p = PLAN[y][s]; base = S.SEANCES[y][s - 1]; ar = AR_TXT[(y, s)]
            assert base["module"] in ("prog",) , (y, s)
            title, obj, trace = (base["title"], ar[0]), (base["obj"], ar[1]), (base["trace"], ar[2])
            tech = set()
            for n in p["core"] + p["support"] + p["challenge"]: tech |= ACT_N[n]
            for kind, key, mode in p["games"]:
                if mode == "play": tech |= (GAMES[key][2] if kind == "game" else STORY_N)
            new, deep = [i for i in NID if i in p["new"]], [i for i in NID if i in p["deep"]]
            after = known | set(new)
            miss = tech - after
            if miss: raise ValueError(f"{y}e séance {s} : notions demandées mais pas encore introduites : {sorted(miss)}")
            for i in deep: assert i in after, (y, s, i)
            re_all = [i for i in NID if i in (tech & known) and i not in new and i not in deep]
            pri = [i for i in re_all if i not in ("seq", "event")] or re_all[:1]
            re_show = sorted(pri, key=NID.index, reverse=True)[:4]
            typ = base["type"]
            ph = phases(y, s, p, typ, new, deep, re_show, trace, (base["obj"], ar[1]))
            assert sum(x[2] for x in ph) == 60, (y, s)
            for role in ("core", "support", "challenge"):
                for n in p[role]: uses[n].append((y, s, role))
            rows[y].append(dict(y=y, s=s, k=k, title=title, obj=obj, trace=trace, type=typ, auto=p["auto"], new=new, deep=deep, re=[i for i in NID if i in re_all], core=p["core"], support=p["support"], challenge=p["challenge"],
                                games=p["games"], acq=p["acq"], extra=p["extra"], phases=ph, cum=len(after)))
            known = after
    # notions de la liste jamais introduites ?
    never = [i for i in NID if i not in known]
    assert not never, never
    used = {n for n, u in uses.items() if u}
    enrich = [n for n in sorted(ACT) if n not in used]
    return rows, uses, enrich

def check():
    rows, uses, enrich = build()
    print("séances :", {y: len(r) for y, r in rows.items()}, "| activités utilisées :", len(ACT) - len(enrich), "/", len(ACT), "| enrichissement :", enrich)
    for y in YEAR_ORDER:
        for r in rows[y]: print(f"  {y}e S{r['s']:>2} [{r['auto']:5}] cumul {r['cum']:>2} nouvelles={r['new']} approf.={r['deep']} réinv.(affichées)={[i for i in r['re'] if i not in ('seq','event')][:5]}")
    return rows, uses, enrich
if __name__ == "__main__": check()

# ----------------------------------------------------------------------------- exports
UI = [
 ("Planning des séances Scratch", "تخطيط حصص سكراتش"),
 ("Proposition non officielle à adapter : une séance de 60 minutes par semaine, celles du module « programmation » de la répartition annuelle. Les notions s'accumulent d'une séance à l'autre et l'autonomie des élèves augmente peu à peu.",
  "اقتراح غير رسمي قابل للتعديل: حصة واحدة مدتها 60 دقيقة في الأسبوع، وهي حصص وحدة «البرمجة» من التوزيع السنوي. تتراكم المفاهيم من حصة إلى أخرى وتزداد استقلالية التلاميذ شيئا فشيئا."),
 ("Carte des notions", "خريطة المفاهيم"), ("nouvelle", "جديد"), ("approfondie", "معمَّق"), ("réinvestie", "موظَّف من جديد"), ("Acquis des années précédentes", "مكتسبات السنوات السابقة"), ("Notion", "المفهوم"), ("Séance", "الحصة"),
 ("Guidé : l'enseignant modélise, l'élève suit les étapes. Semi-guidé : l'élève part de l'objectif et du résultat attendu. Autonome : l'élève décide et réalise seul.", "موجَّه: الأستاذ يشرح والتلميذ يتبع المراحل. شبه موجَّه: ينطلق التلميذ من الهدف والنتيجة المنتظرة. مستقل: يقرر التلميذ وينجز وحده."),
 ("Démarche (60 minutes)", "السير (60 دقيقة)"), ("Phase", "المرحلة"), ("Durée", "المدة"), ("Description", "الوصف"), ("min", "د"),
 ("Activité principale", "النشاط الرئيسي"), ("Pour s'entraîner", "للتدرّب"), ("Défi", "تحدٍّ"), ("Jeux et contes", "الألعاب والقصص"), ("Je sais…", "أنا قادر على…"), ("Trace écrite", "الأثر المكتوب"), ("Objectif", "الهدف"),
 ("Notions nouvelles", "المفاهيم الجديدة"), ("Notions approfondies", "المفاهيم المعمَّقة"), ("Notions acquises à la fin de la séance", "المفاهيم المكتسبة في نهاية الحصة"), ("Autonomie", "الاستقلالية"),
 ("Pour aller plus loin (hors planning)", "للتوسع (خارج التخطيط)"), ("Certaines utilisent des clones, des listes ou le « et » : elles dépassent le cadrage du programme.", "بعضها يستعمل النسخ أو القوائم أو «و» المنطقية: وهي تتجاوز إطار المنهاج."),
 ("Imprimer le planning", "طباعة التخطيط"), ("Ouvrir le planning", "فتح التخطيط"), ("Voir le planning des séances", "الاطلاع على تخطيط الحصص"), ("Utilisée en séance", "تُستعمل في الحصة"), ("← Espace enseignant", "← فضاء الأستاذ"),
 ("Ouvrir le conte", "فتح القصة"), ("Regarder", "مشاهدة"), ("Jouer", "اللعب"), ("Notions réinvesties", "المفاهيم الموظَّفة من جديد"), ("Tout déplier", "فتح الكل"), ("Tout replier", "طي الكل"),
]
def _pairs_for(fr):
    for a, b in UI: fr[b] = a
def export():
    rows, uses, enrich = build(); fr = {}
    def P_(pair): fr[pair[1]] = pair[0]; return pair[1]
    _pairs_for(fr)
    data = dict(notions=[dict(id=i, t=P_((NT[i][0], NT[i][1]))) for i in NID], years={}, enrich=enrich, uses={})
    for y in YEAR_ORDER:
        ys = []
        for r in rows[y]:
            ys.append(dict(y=y, s=r["s"], k=r["k"], t=P_(r["title"]), obj=P_(r["obj"]), trace=P_(r["trace"]), type=P_(TYPES[r["type"]]), tk=r["type"], auto=r["auto"], auto_t=P_(AUTO[r["auto"]]),
                           new=r["new"], deep=r["deep"], re=r["re"], core=r["core"], support=r["support"], challenge=r["challenge"], games=[dict(kind=k, key=g, mode=m) for k, g, m in r["games"]],
                           acq=[P_(a) for a in (r["acq"] or [])], extra=(P_(r["extra"]) if r["extra"] else None), phases=[dict(t=P_((a, b)), min=m, d=P_((c, d))) for a, b, m, c, d in r["phases"]], cum=r["cum"]))
        data["years"][y] = dict(label=P_(YEARLBL[y]), seances=ys)
    for n, u in uses.items():
        data["uses"][n] = [dict(y=y, s=s, role=role) for y, s, role in u]
    # séances complémentaires proposées (cahier_extra.py) : 9e objet programmable / application mobile ; 8e cours « Sécurité informatique »
    import cahier_extra as CE
    TXT = {"9": (("Séances complémentaires proposées (aide pédagogique 2026)", "حصص إضافية مقترحة (المساعدة البيداغوجية 2026)"),
                 ("Objet programmable (micro:bit) et application mobile (App Inventor). Proposition non officielle, hors répartition annuelle : à insérer à la place de séances de révision ou en projet.", "الشيء القابل للبرمجة (micro:bit) وتطبيقة الهاتف (App Inventor). اقتراح غير رسمي خارج التوزيع السنوي: يُدرج مكان حصص مراجعة أو في مشروع.")),
           "8": (("Cours « Sécurité informatique » en 4 séances (domaine Environnement informatique)", "درس «أمن المعلوميات» في 4 حصص (مجال بيئة العمل المعلوماتية)"),
                 ("Menaces et protection : indicateurs, logiciels malveillants et piratage, communautés virtuelles, protection des données. Chaque séance a son cas d'introduction, sa vidéo (page « Sécurité informatique ») et sa fiche du cahier. Proposition non officielle, hors répartition annuelle.", "التهديدات والحماية: المؤشرات، البرمجيات الخبيثة والقرصنة، المجتمعات الافتراضية، حماية المعطيات. لكل حصة حالة انطلاق وفيديو (صفحة «أمن المعلوميات») ومذكرة دفتر. اقتراح غير رسمي خارج التوزيع السنوي."))}
    for yy, keys in CE.YEAR_EXTRA.items():
        ex = []
        for i, key in enumerate(keys, 1):
            e = CE.EXTRA[key]; ph = CE.PHASES[key]
            ex.append(dict(y=yy, s=key, k=i, t=P_(e["title"]), obj=P_(e["obj"]), trace=P_(e["trace"]), type=P_(("Proposition", "اقتراح")), tk="manip", auto="semi", auto_t=P_(AUTO["semi"]),
                           new=[], deep=[], re=[], core=[], support=[], challenge=[], games=[], acq=[P_(a) for a in e["acq"]], extra=None, cum=len(NID),
                           phases=[dict(t=P_(a), min=m, d=P_(d)) for a, m, d in ph]))
        data["years"][yy]["extra"] = ex; data["years"][yy]["extraT"] = P_(TXT[yy][0]); data["years"][yy]["extraN"] = P_(TXT[yy][1])
    for k, g in GAMES.items(): P_((g[0], g[1]))
    for k, g in STORIES.items(): P_(g)
    for role in ("core", "support", "challenge"): pass
    return data, fr
def french_year(y):
    """version française d'une année, pour les fiches imprimables des enseignants (enseignant.py) : {n° de séance : infos}"""
    rows, uses, enrich = build(); out = {}
    import theorie_data as TD                      # leçons de « Théorie Scratch » à lire pour chaque séance (7e seulement)
    th = {}
    if y == "7":
        for L in TD.LESSONS: th.setdefault(L["seance"], []).append((L["n"], L["title"][0]))
    for r in rows[y]:
        out[r["s"]] = dict(theory=th.get(r["s"], []), k=r["k"], auto=AUTO[r["auto"]][0], new=[NT[i][0] for i in r["new"]], deep=[NT[i][0] for i in r["deep"]], re=[NT[i][0] for i in r["re"] if i not in ("seq", "event")], cum=r["cum"],
                           acts=[(role, n, ACT[n]["title"][0]) for role in ("core", "support", "challenge") for n in r[role]], games=[(k, gtitle(k, g)[0], m) for k, g, m in r["games"]],
                           phases=[(a, m, c) for a, b, m, c, d in r["phases"]], acq=[a[0] for a in (r["acq"] or [])], extra=(r["extra"][0] if r["extra"] else None))
    return out
def matrix(y):
    """pour les fiches imprimables : lignes = notions connues à la fin de l'année y ; colonnes = séances de l'année ; cellule N / A / R"""
    rows, uses, enrich = build(); known = set(); cols = []
    for yy in YEAR_ORDER:
        for r in rows[yy]:
            if yy == y: cols.append(r)
            else:
                if YEAR_ORDER.index(yy) < YEAR_ORDER.index(y): known |= set(r["new"])
    lines = []
    seen = set(known)
    for i in NID:
        last = [r for r in cols if i in r["new"]]
        if i not in known and not last: continue
        cells = []
        for r in cols:
            cells.append("N" if i in r["new"] else ("A" if i in r["deep"] else ("R" if i in r["re"] else "")))
        lines.append((NT[i][0], i in known, cells))
    return [r["s"] for r in cols], lines
