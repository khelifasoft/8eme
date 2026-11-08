"""Parcours de programmation par compétences (petites activités Scratch, de niveau en niveau) + projets de base, pour 7e, 8e, 9e.
Chaque texte est un couple (arabe, français). Modèles : "game:<cat>/<clé>" (jeu téléchargeable) ou "story:<clé>" (conte).
Modifier ce fichier puis : python3 generateur/page.py"""
def L(*pairs): return list(pairs)
def step(t, comp, acts, sais, models=()): return dict(t=t, comp=comp, acts=acts, sais=sais, models=list(models))
def proj(t, lvl, brief, req, models=(), out=None): return dict(t=t, lvl=lvl, brief=brief, req=req, models=list(models), out=out)
LIVRABLES = ("المطلوب تسليمه: ملف المشروع (.sb3) + مخطط الحل + ورقة الاختبارات والتصحيحات.", "À rendre : le projet (.sb3), le diagramme de la solution et la feuille de tests et corrections.")
PARC = {
 "7": dict(
  steps=[
   step(("حلّ مشكل دون حاسوب", "Résoudre un problème sans ordinateur"), ("أحدّد المشكل والمعطيات والنتيجة المنتظرة وأرتّب الخطوات.", "Je repère le problème, les données, le résultat attendu et j'ordonne les étapes."),
     [("لعبة الروبوت: أقود زميلي على مربعات بتعليمات مكتوبة على بطاقات.", "Jeu du robot : je guide un camarade sur un quadrillage avec des cartes-instructions."), ("أكتب تعليمات الوصول من الباب إلى السبورة.", "J'écris les instructions pour aller de la porte au tableau."), ("أتحقق من تعليماتي بتجربتها مع زميل وأصححها.", "Je teste mes instructions avec un camarade et je les corrige.")],
     [("أستطيع ذكر خطوات حل مشكل بسيط بالترتيب.", "Je sais écrire dans l'ordre les étapes d'un problème simple."), ("أعرف أن تغيير الترتيب يغيّر النتيجة.", "Je sais que changer l'ordre change le résultat.")]),
   step(("أكتشف سكراتش", "Je découvre Scratch"), ("أتعرف على اللاعب والمنصة والكتل وأنجز تسلسلا من التعليمات.", "Je reconnais le lutin, la scène, les blocs et je construis une séquence."),
     [("أفتح قصة جحا وأضغط على العلم الأخضر وأصف ما يحدث.", "J'ouvre le conte de Jeha, je clique sur le drapeau vert et je décris ce qui se passe."), ("أجد الكتل التي تجعل اللاعب يتكلم وأغيّر جملة.", "Je trouve les blocs qui font parler le lutin et je change une réplique."), ("أضيف كتلة «انزلق» لتحريك الشخصية.", "J'ajoute un bloc « glisser » pour déplacer le personnage.")],
     [("أسمّي أقسام واجهة سكراتش.", "Je sais nommer les parties de l'interface de Scratch."), ("أركّب كتلا لتجعل لاعبا يتكلم ويتحرك.", "Je sais assembler des blocs pour faire parler et bouger un lutin.")], ["story:djeha"]),
   step(("الأحداث: متى يبدأ السكربت؟", "Les événements : quand le script démarre-t-il ?"), ("أُطلق سكربتا انطلاقا من حدث (علم أخضر، نقرة، رسالة).", "Je déclenche un script à partir d'un événement (drapeau vert, clic, message)."),
     [("أجد في قصة ليلى الكتلة «عند استلام رسالة» وأعدّ المشاهد.", "Dans le conte de Layla, je trouve « quand je reçois » et je compte les scènes."), ("أجعل شخصية تتكلم عند النقر عليها.", "Je fais parler un personnage quand on clique dessus."), ("أضيف مشهدا جديدا برسالة جديدة.", "J'ajoute une scène avec un nouveau message.")],
     [("أميّز بين الأحداث الثلاثة.", "Je sais distinguer les trois événements."), ("أضيف مشهدا يعمل في وقته.", "Je sais ajouter une scène qui se joue au bon moment.")], ["story:layla"]),
   step(("التكرار", "Les boucles"), ("أستعمل «كرّر باستمرار» و«كرّر n مرات».", "J'utilise « répéter indéfiniment » et « répéter n fois »."),
     [("أحرّك الأرنب بحلقة بدل نسخ الكتل.", "J'anime le lièvre avec une boucle au lieu de copier les blocs."), ("أغيّر عدد التكرار وألاحظ الفرق.", "Je change le nombre de répétitions et j'observe la différence."), ("أضيف موسيقى تتكرر في الخلفية.", "J'ajoute une musique qui se répète en fond.")],
     [("أعرف الحالة التي أختار فيها كل حلقة.", "Je sais quand choisir chaque boucle."), ("أختصر سكربتا بحلقة.", "Je sais raccourcir un script avec une boucle.")], ["story:hare"]),
   step(("الشرط البسيط: إذا… فإن", "La condition simple : si… alors"), ("أنفّذ تعليمات عند تحقق شرط، دون «و» ولا «أو».", "J'exécute des instructions quand une condition est vraie, sans « et » ni « ou »."),
     [("في قصة علي بابا أجد السؤال والجواب وأقرأ الشرط.", "Dans Ali Baba, je repère la question, la réponse et la condition."), ("أغيّر الكلمة السرية للباب وأختبر.", "Je change le mot de passe de la porte et je teste."), ("أضيف رد فعل إذا كانت الإجابة خاطئة.", "J'ajoute une réaction si la réponse est fausse.")],
     [("أكتب «إذا… فإن» بنفسي.", "Je sais écrire un « si… alors » seul."), ("أختبر حالتين: الشرط محقق وغير محقق.", "Je teste deux cas : condition vraie et fausse.")], ["story:alibaba"]),
  ],
  projets=[
   proj(("قصتي في أربعة مشاهد", "Mon conte en 4 scènes"), 1, ("أحوّل قصة قصيرة إلى مشروع تفاعلي.", "Je transforme un court récit en projet interactif."),
     [("4 مشاهد بديكورات مختلفة", "4 scènes avec des décors différents"), ("رسائل لتسلسل المشاهد", "Des messages pour enchaîner les scènes"), ("كل شخصية تتكلم مرة على الأقل", "Chaque personnage parle au moins une fois")], ["story:cinderella", "story:pigs"]),
   proj(("حوار بسؤال وجواب", "Un dialogue avec question et réponse"), 2, ("شخصية تسأل والمستعمل يجيب ثم تتفاعل.", "Un personnage pose une question, l'utilisateur répond, le personnage réagit."),
     [("شرط بسيط واحد على الأقل", "Au moins une condition simple"), ("ردّان مختلفان", "Deux réactions différentes"), ("اختبار الحالتين", "Test des deux cas")], ["story:alibaba"]),
   proj(("شخصية تمشي وتتكلم", "Un personnage qui marche et parle"), 1, ("أحرّك شخصية بحلقة مع صوت.", "J'anime un personnage avec une boucle et un son."),
     [("حلقة لتغيير الزي", "Une boucle pour changer de costume"), ("صوت أو موسيقى", "Un son ou une musique"), ("بدء بالعلم الأخضر", "Démarrage avec le drapeau vert")], ["story:hare"]),
  ]),
 "8": dict(
  steps=[
   step(("جزّئ المشكل", "Décomposer un problème"), ("أجزّئ مشكلا إلى مشكلات فرعية وأمثّل الحل بمخطط.", "Je décompose un problème en sous-problèmes et je représente la solution par un diagramme."),
     [("ألعب «رتّب المشاهد» وأدوّن مراحل اللعبة.", "Je joue à « Remets les scènes dans l'ordre » et je note les étapes du jeu."), ("أرسم مخططا: عرض ← اختيار ← تحقق ← نقاط.", "Je dessine un diagramme : afficher → choisir → vérifier → points."), ("أنجز في سكراتش المرحلة الأولى فقط.", "Je réalise sur Scratch la première étape seulement.")],
     [("أقسّم مشكلا إلى 3 مراحل على الأقل.", "Je sais découper un problème en au moins 3 étapes."), ("أقرأ مخطط الحل وأصفه.", "Je sais lire et décrire un diagramme.")], ["game:order/ordre_cinderella"]),
   step(("المتغيرات: العدّاد", "Les variables : le score"), ("أستعمل متغيرا عدديا لتلبية حاجة (النقاط).", "J'utilise une variable numérique pour répondre à un besoin (les points)."),
     [("ألعب اللعبة وألاحظ أنها لا تحسب شيئا ثم أحتاج إلى عدّاد.", "Je joue, je constate qu'il manque un compteur, j'exprime le besoin."), ("أنشئ المتغير «نقاط» وأهيّئه إلى 0 عند العلم الأخضر.", "Je crée la variable « points » et je l'initialise à 0 au drapeau vert."), ("أزيد 1 عند كل إجابة صحيحة وأعرض النتيجة.", "J'ajoute 1 à chaque bonne réponse et j'affiche le résultat.")],
     [("أنشئ متغيرا وأهيّئه وأزيده.", "Je sais créer, initialiser et incrémenter une variable."), ("أشرح لماذا نحتاج إلى متغير.", "Je sais expliquer pourquoi une variable est utile.")], ["game:quiz/comptage"]),
   step(("الشرط الكامل: إذا… وإلا", "La condition complète : si… sinon"), ("أبرمج ردّين مختلفين حسب شرط.", "Je programme deux réactions différentes selon une condition."),
     [("أقرأ سكربت التحقق من الإجابة في لعبة الحروف.", "Je lis le script qui vérifie la réponse dans le jeu des lettres."), ("أغيّر الإجابة الصحيحة في سؤال وأختبر.", "Je change la bonne réponse d'une question et je teste."), ("أضيف صوتا لكل من الحالتين.", "J'ajoute un son pour chacun des deux cas.")],
     [("أكتب «إذا… وإلا» بنفسي.", "Je sais écrire un « si… sinon » seul."), ("أستعمل شرطا يقارن متغيرا بعدد.", "Je sais comparer une variable à un nombre.")], ["game:quiz/lettres"]),
   step(("التكرار والعشوائية", "Boucles et hasard"), ("أستعمل حلقة وأعدادا عشوائية لإنتاج لعبة غير متوقعة.", "J'utilise une boucle et le hasard pour un jeu imprévisible."),
     [("ألعب «الخلد والذئب» وأصف كيف يظهر في أمكنة مختلفة.", "Je joue à la taupe et je décris comment elle apparaît à des endroits différents."), ("أجد كتلة «عدد عشوائي» وأغيّر حدوده.", "Je trouve « nombre aléatoire » et je change ses bornes."), ("أغيّر سرعة اللعبة لتصبح أصعب.", "Je change la vitesse pour rendre le jeu plus difficile.")],
     [("أستعمل عددا عشوائيا في موضع.", "Je sais utiliser un nombre aléatoire pour une position."), ("أضبط صعوبة لعبة.", "Je sais régler la difficulté d'un jeu.")], ["game:reflex/taupe_loup", "game:catch/sindbad"]),
   step(("الوحدات: كتلتي", "Les modules : Mon bloc"), ("أنشئ وحدة وأستدعيها لتفادي تكرار الكتل.", "Je crée et j'appelle un module pour éviter de répéter des blocs."),
     [("أجد مجموعة كتل مكررة في لعبة الذاكرة.", "Je repère une suite de blocs répétée dans le jeu de mémoire."), ("أجمعها في «كتلتي» وأعطيها اسما واضحا.", "Je la regroupe dans « Mon bloc » avec un nom clair."), ("أستدعيها بدل النسخ وأتأكد أن اللعبة تعمل.", "Je l'appelle au lieu de copier et je vérifie que le jeu marche.")],
     [("أنشئ وأستدعي وحدة.", "Je sais créer et appeler un module."), ("أبرر لماذا اخترت هذه الوحدة.", "Je sais justifier mon choix de module.")], ["game:memory/memoire_animaux"]),
   step(("اختبر وصحّح وحسّن", "Tester, corriger, optimiser"), ("أختبر حلاّ وأجد أخطاءه وأحسّنه.", "Je teste une solution, je trouve ses erreurs et je l'améliore."),
     [("ألعب لعبة الصخور بإجابات صحيحة كلها ثم خاطئة كلها.", "Je joue au jeu des rochers avec toutes les bonnes puis toutes les mauvaises réponses."), ("أدوّن خطأين وأصححهما.", "Je note deux erreurs et je les corrige."), ("أقترح تحسينا وأبرره (صوت، توازن، وضوح).", "Je propose une amélioration et je la justifie (son, équilibre, lisibilité).")],
     [("أنجز جدول اختبارات.", "Je sais tenir un tableau de tests."), ("أصحح خطأ وأتحقق من التصحيح.", "Je sais corriger une erreur et vérifier la correction.")], ["game:reflex/rochers"]),
  ],
  projets=[
   proj(("اختبار من تأليفي", "Un quiz de mon choix"), 1, ("أنجز اختبارا من 5 أسئلة حول موضوع أحبه.", "Je réalise un quiz de 5 questions sur un sujet que j'aime."),
     [("متغير للنقاط", "Une variable pour les points"), ("شرط «إذا… وإلا» لكل سؤال", "Un « si… sinon » par question"), ("رسالة نهائية بحسب النتيجة", "Un message final selon le résultat")], ["game:quiz/contes"]),
   proj(("لعبة التقاط الأشياء", "Un jeu d'attrape-objets"), 2, ("أنجز لعبة يلتقط فيها اللاعب أشياء ويتفادى أخرى.", "Je crée un jeu où l'on attrape des objets et où l'on en évite d'autres."),
     [("متغير للنقاط وآخر للأرواح", "Une variable pour les points et une pour les vies"), ("وحدة «خسارة روح»", "Un module « perdre une vie »"), ("مواقع عشوائية", "Des positions aléatoires")], ["game:catch/sindbad"]),
   proj(("الحساب الذهني", "Le calcul mental"), 2, ("لعبة أسئلة حسابية بأعداد عشوائية.", "Un jeu de questions de calcul avec des nombres aléatoires."),
     [("أعداد عشوائية", "Des nombres aléatoires"), ("طلب الإجابة والتحقق منها", "Demander la réponse et la vérifier"), ("وحدة «اطرح سؤالا»", "Un module « poser une question »")], ["game:math/addition", "game:math/devine"]),
   proj(("لعبة الذاكرة", "Un jeu de mémoire"), 3, ("أنجز لعبة تقلب فيها البطاقات لإيجاد الأزواج.", "Je réalise un jeu où l'on retourne des cartes pour trouver les paires."),
     [("ثلاث وحدات على الأكثر", "Trois modules au maximum"), ("متغير لعدد الأزواج", "Une variable pour le nombre de paires"), ("جدول اختبارات", "Un tableau de tests")], ["game:memory/memoire_personnages"]),
   proj(("رتّب مشاهد قصتي", "Les scènes de mon histoire dans l'ordre"), 2, ("أنجز لعبة ترتيب مشاهد من اختيارك.", "Je crée un jeu d'ordonnancement de scènes de mon choix."),
     [("4 مشاهد على الأقل", "Au moins 4 scènes"), ("متغير للمحاولات", "Une variable pour les essais"), ("تغذية راجعة عند الخطأ", "Un retour en cas d'erreur")], ["game:order/ordre_djeha"]),
  ]),
 "9": dict(
  steps=[
   step(("اختيار بيئة العمل", "Choisir un environnement"), ("أقارن بيئات البرمجة وأبرر اختياري.", "Je compare des environnements de programmation et je justifie mon choix."),
     [("أقارن سكراتش ومبرمج آخر لنفس المشكل.", "Je compare Scratch et un autre outil pour le même problème."), ("أملأ جدول مقارنة (سهولة، إمكانات، أجهزة).", "Je remplis un tableau (facilité, possibilités, matériel).")],
     [("أبرر اختيار بيئة.", "Je sais justifier le choix d'un environnement.")]),
   step(("تحليل مشكل: مدخلات ومعالجة ومخرجات", "Analyser : entrées, traitement, sorties"), ("أحلل مشكلا وأحدد مدخلاته ومخرجاته.", "J'analyse un problème et j'identifie ses entrées et sorties."),
     [("ألعب لعبة التخمين وأحدد المدخلات والمخرجات.", "Je joue au jeu de devinette et je repère entrées et sorties."), ("أرسم مخطط «مدخلات ← معالجة ← مخرجات».", "Je dessine le schéma entrées → traitement → sorties.")],
     [("أنجز مخطط تحليل كامل.", "Je sais faire un schéma d'analyse complet.")], ["game:math/devine"]),
   step(("المتغيرات والوحدات", "Variables et modules"), ("أهيكل برنامجا بمتغيرات ووحدات.", "Je structure un programme avec variables et modules."),
     [("أعيد برمجة لعبة بمتغير للنقاط ووحدة.", "Je reprends un jeu : variable de score et un module."), ("أبرر تقسيم البرنامج إلى وحدات.", "Je justifie le découpage en modules.")],
     [("أهيكل برنامجا بوضوح.", "Je sais structurer un programme clairement.")], ["game:math/multiplication"]),
   step(("المستشعرات والمنفذات (محاكاة)", "Capteurs et actionneurs (simulation)"), ("أحاكي بسكراتش مستشعرا (نقرة، مسافة) ومنفذا (لاعب يتحرك أو يضيء).", "Je simule avec Scratch un capteur (clic, distance) et un actionneur (lutin qui bouge ou s'allume)."),
     [("أجعل لاعبا يتغير زيّه حسب قيمة متغير (المستشعر).", "Je change le costume d'un lutin selon une variable (le capteur)."), ("أنشئ قاعدة: إذا القيمة > عتبة فعّل المنفذ.", "J'écris la règle : si valeur > seuil alors activer l'actionneur.")],
     [("أميّز المستشعر من المنفذ.", "Je sais distinguer capteur et actionneur.")], ["game:reflex/taupe_renard"]),
   step(("اختبر وحسّن وبرّر", "Tester, optimiser, argumenter"), ("أختبر حلاّ وأحسّنه وأدافع عن اختياراتي.", "Je teste une solution, je l'optimise et j'argumente mes choix."),
     [("أقارن حلّين لنفس المشكل.", "Je compare deux solutions au même problème."), ("أقدّم اختياري بحجتين.", "Je présente mon choix avec deux arguments.")],
     [("أبرر حلاّ بحجج.", "Je sais défendre une solution avec des arguments.")]),
  ],
  projets=[
   proj(("لعبة تخمين بعدّاد محاولات", "Une devinette avec compteur d'essais"), 2, ("برنامج يخمّن فيه المستعمل عددا مخفيا.", "Un programme où l'utilisateur devine un nombre caché."),
     [("عدد عشوائي", "Un nombre aléatoire"), ("متغير لعدد المحاولات", "Une variable pour les essais"), ("رسالة «أكبر / أصغر»", "Un message « plus grand / plus petit »")], ["game:math/devine"]),
   proj(("إشارة مرور محاكاة", "Un feu tricolore simulé"), 2, ("أحاكي مستشعرا ومنفذا بلاعبين.", "Je simule un capteur et un actionneur avec des lutins."),
     [("زرّ (مستشعر) يغيّر الأضواء", "Un bouton (capteur) qui change les feux"), ("ثلاثة أزياء للمنفذ", "Trois costumes pour l'actionneur"), ("وحدة لتغيير الضوء", "Un module pour changer la lumière")]),
   proj(("تطبيق هاتف بسيط", "Une application mobile simple"), 3, ("أنجز تطبيقا بـ App Inventor (اختبار أو حاسبة).", "Je réalise une application avec App Inventor (quiz ou calculatrice)."),
     [("شاشة وأزرار", "Un écran et des boutons"), ("حدث عند النقر", "Un événement au clic"), ("اختبار على الهاتف أو المحاكي", "Un test sur téléphone ou émulateur")]),
  ]),
}
LABELS = {"أحاكي": 0}  # (réservé)
def export():
    """-> (données JSON pour la page, dictionnaire AR->FR)."""
    fr = {}
    def P(pair): fr[pair[0]] = pair[1]; return pair[0]
    def PL(lst): return [P(x) for x in lst]
    out = {}
    for y, d in PARC.items():
        steps = [dict(t=P(s["t"]), comp=P(s["comp"]), acts=PL(s["acts"]), sais=PL(s["sais"]), models=s["models"]) for s in d["steps"]]
        pr = [dict(t=P(p["t"]), lvl=p["lvl"], brief=P(p["brief"]), req=PL(p["req"]), models=p["models"]) for p in d["projets"]]
        out[y] = dict(steps=steps, projets=pr)
    P(LIVRABLES); out["livrables"] = LIVRABLES[0]
    return out, fr
if __name__ == "__main__":
    o, f = export(); print({y: (len(o[y]["steps"]), len(o[y]["projets"])) for y in "789"}, len(f))
