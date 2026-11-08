"""Traduction arabe des fiches d'activité « catch » (jeu) et « contes » (couples arabe / français pris dans fiches_programme.py et fiches_etapes.py).
Même ordre que les listes françaises. Le site affiche l'arabe et traduit en français avec le bouton FR."""
AR = {
 "catch": dict(
  title="التقاط الأشياء", duree="حصتان من 45 دقيقة", year="السنة الثامنة",
  situation="كيف نجعل الأشياء تسقط بسرعة متزايدة، ونلتقطها بالفأرة، ونحسب النقاط والأرواح؟",
  steps=["حاجة تُستخلص دون حاسوب (10 د)", "نلعب ونصف (10 د)", "نقرأ السكربتات (15 د)", "نعدّل ونحسّن (20 د)", "نختبر ونصحّح (10 د)"],
  eleve=["العب حتى النهاية ودوّن نتيجتك.", "ابحث عن المتغير الذي يضبط سرعة السقوط. أين تتم تهيئته؟", "غيّر سرعة البداية، واختبر وفسّر الأثر.", "حدّد الشرطين المتداخلين اللذين يكشفان التقاط الشيء، وفسّر كلا منهما.", "تحدٍّ: أضف صوتا مختلفا عندما تخطئ في التقاط شيء."],
  criteres=["تُلاحَظ السرعة المعدّلة عند الاختبار.", "يفسّر التلميذ الشروط المتداخلة.", "يُختبَر تحسين واحد."],
  allegee="تغيير سرعة البداية فقط.",
  prolongement="تجميع «شيء ملتقط» (النقاط، السرعة، الصوت، العودة إلى الأعلى) في وحدة واستدعاؤها بدل الكتل.",
  fr=dict(
   title="Attrape-objets", duree="2 séances de 45 minutes", year="8e année",
   situation="Comment faire tomber des objets de plus en plus vite, les attraper avec la souris et compter les points et les vies ?",
   steps=['Besoin à faire émerger sans ordinateur (10 min)', 'Jouer et décrire (10 min)', 'Lire les scripts (15 min)', 'Modifier et optimiser (20 min)', 'Tester et corriger (10 min)'],
   eleve=["Joue jusqu'à la fin et note ton score.", 'Trouve la variable qui règle la vitesse de chute. Où est-elle initialisée ?', "Change la vitesse de départ, teste et explique l'effet.", 'Repère les deux conditions imbriquées qui détectent un objet attrapé. Explique chacune.', 'Défi : ajoute un son différent quand tu rates un objet.'],
   criteres=['La vitesse modifiée est constatée au test.', "L'élève explique les conditions imbriquées.", 'Une amélioration est testée.'],
   allegee="Changer uniquement la vitesse de départ.",
   prolongement="Regrouper « objet attrapé » (points, vitesse, son, retour en haut) dans un module et l'appeler à la place des blocs.")),
 "course": dict(
  title="سباق السيارات: تفادَ السيارات", duree="حصتان من 45 دقيقة", year="السنة الثامنة",
  situation="كيف نحرّك سيارة بأسهم لوحة المفاتيح، ونجعل سيارات تأتي بسرعة متزايدة، ونحسب النقاط والأرواح؟",
  steps=["حاجة تُستخلص دون حاسوب (10 د)", "نلعب ونصف (10 د)", "نقرأ السكربتات (15 د)", "نعدّل ونحسّن (20 د)", "نختبر ونصحّح (10 د)"],
  eleve=["العب حتى النهاية ودوّن نتيجتك.", "حدّد الكتل التي تحرّك السيارة عند الضغط على سهم.", "ابحث عن المتغير الذي يضبط السرعة. ما الذي يجعله يزيد؟", "غيّر سرعة البداية أو مقدار زيادة السرعة، واختبر وفسّر الأثر.", "تحدٍّ: أضف صوتا عندما تتفادى سيارة."],
  criteres=["يُلاحَظ تغيّر السرعة عند الاختبار.", "يفسّر التلميذ الشرطين المتداخلين للاصطدام.", "يُختبَر تحسين واحد."],
  allegee="تغيير سرعة البداية فقط.",
  prolongement="إنشاء وحدة «سيارة مصدومة» (−1 روح، صوت، العودة إلى الأعلى) واستدعاؤها بدل الكتل.",
  fr=dict(
   title="Course : évite les voitures", duree="2 séances de 45 minutes", year="8e année",
   situation="Comment déplacer une voiture avec les flèches du clavier, faire arriver des voitures de plus en plus vite et compter les points et les vies ?",
   steps=['Besoin à faire émerger sans ordinateur (10 min)', 'Jouer et décrire (10 min)', 'Lire les scripts (15 min)', 'Modifier et optimiser (20 min)', 'Tester et corriger (10 min)'],
   eleve=["Joue jusqu'à la fin et note ton score.", "Repère les blocs qui déplacent la voiture quand on appuie sur une flèche.", "Trouve la variable qui règle la vitesse. Qu'est-ce qui la fait augmenter ?", "Change la vitesse de départ ou l'augmentation de la vitesse, teste et explique l'effet.", "Défi : ajoute un son quand tu évites une voiture."],
   criteres=["Le changement de vitesse est constaté au test.", "L'élève explique les conditions imbriquées de la collision.", "Une amélioration est testée."],
   allegee="Changer uniquement la vitesse de départ.",
   prolongement="Créer un module « voiture touchée » (−1 vie, son, retour en haut) et l'appeler à la place des blocs.")),
 "saut": dict(
  title="الجمل يقفز: تفادَ الشجيرات", duree="حصتان من 45 دقيقة", year="السنة الثامنة",
  situation="كيف نجعل جملا يقفز بالضغط على المسافة، ونجعل شجيرات تأتي بسرعة متزايدة، ونحسب النقاط والأرواح؟",
  steps=["حاجة تُستخلص دون حاسوب (10 د)", "نلعب ونصف (10 د)", "نقرأ السكربتات (15 د)", "نعدّل ونحسّن (20 د)", "نختبر ونصحّح (10 د)"],
  eleve=["العب حتى النهاية ودوّن نتيجتك.", "ابحث عن المتغير الذي يعطي سرعة القفز. أين يتغيّر؟", "غيّر ارتفاع القفزة، واختبر وفسّر الأثر على اللعبة.", "حدّد الشرطين المتداخلين اللذين يكشفان الاصطدام، وفسّر كلا منهما.", "تحدٍّ: أضف صوتا عندما يقفز الجمل."],
  criteres=["يُلاحَظ أثر تغيير الارتفاع عند الاختبار.", "يفسّر التلميذ الشرطين المتداخلين للاصطدام.", "يُختبَر تحسين واحد."],
  allegee="تغيير ارتفاع القفزة فقط.",
  prolongement="إنشاء وحدة «شجيرة ملموسة» (−1 روح، صوت، العودة إلى اليمين) واستدعاؤها بدل الكتل.",
  fr=dict(
   title="Le chameau saute-buissons", duree="2 séances de 45 minutes", year="8e année",
   situation="Comment faire sauter un chameau avec la barre d'espace, faire arriver des buissons de plus en plus vite et compter les points et les vies ?",
   steps=['Besoin à faire émerger sans ordinateur (10 min)', 'Jouer et décrire (10 min)', 'Lire les scripts (15 min)', 'Modifier et optimiser (20 min)', 'Tester et corriger (10 min)'],
   eleve=["Joue jusqu'à la fin et note ton score.", "Trouve la variable qui donne la vitesse du saut. Où est-elle modifiée ?", "Change la hauteur du saut, teste et explique l'effet sur le jeu.", "Repère les deux conditions imbriquées qui détectent la collision. Explique chacune.", "Défi : ajoute un son quand le chameau saute."],
   criteres=["L'effet du changement de hauteur est constaté au test.", "L'élève explique les conditions imbriquées de la collision.", "Une amélioration est testée."],
   allegee="Changer uniquement la hauteur du saut.",
   prolongement="Créer un module « buisson touché » (−1 vie, son, retour à droite) et l'appeler à la place des blocs.")),
 "labyrinthe": dict(
  title="متاهة الفأرة", duree="حصتان من 45 دقيقة", year="السنة الثامنة",
  situation="كيف نحرّك فأرة بالأسهم في متاهة، ونمنعها من اختراق الجدران، ونحسب النقاط والوقت؟",
  steps=["حاجة تُستخلص دون حاسوب (10 د)", "نلعب ونصف (10 د)", "نقرأ السكربتات (15 د)", "نعدّل ونحسّن (20 د)", "نختبر ونصحّح (10 د)"],
  eleve=["العب حتى النهاية ودوّن نتيجتك والوقت المتبقي.", "ابحث عن المتغيرين اللذين يحفظان الموضع السابق. ما فائدتهما؟", "غيّر سرعة الفأرة (القيمة 4) أو المدة الكلية (القيمة 60)، واختبر وفسّر الأثر.", "حدّد الشروط الثلاثة المتداخلة الخاصة بجدار، وفسّر كلا منها.", "تحدٍّ: انقل فتحة جدار إلى الجهة الأخرى وكيّف الشرط."],
  criteres=["يُلاحَظ أثر التغيير عند الاختبار.", "يفسّر التلميذ الشروط المتداخلة الخاصة بجدار.", "يُختبَر تحسين واحد."],
  allegee="تغيير المدة الكلية فقط.",
  prolongement="إضافة جدار رابع بفتحته، ثم تجميع مراقبة الجدار في وحدة.",
  fr=dict(
   title="Le labyrinthe de la souris", duree="2 séances de 45 minutes", year="8e année",
   situation="Comment déplacer une souris avec les flèches dans un labyrinthe, l'empêcher de traverser les murs et compter les points et le temps ?",
   steps=['Besoin à faire émerger sans ordinateur (10 min)', 'Jouer et décrire (10 min)', 'Lire les scripts (15 min)', 'Modifier et optimiser (20 min)', 'Tester et corriger (10 min)'],
   eleve=["Joue jusqu'au bout et note ton score et le temps restant.", "Trouve les variables qui mémorisent la position précédente. À quoi servent-elles ?", "Change la vitesse de la souris (la valeur 4) ou la durée totale (la valeur 60), teste et explique l'effet.", "Repère les trois conditions imbriquées d'un mur. Explique chacune.", "Défi : déplace l'ouverture d'un mur de l'autre côté et adapte la condition."],
   criteres=["L'effet du changement est constaté au test.", "L'élève explique les conditions imbriquées d'un mur.", "Une amélioration est testée."],
   allegee="Changer uniquement la durée totale.",
   prolongement="Ajouter un quatrième mur avec son ouverture, puis regrouper la vérification d'un mur dans un module.")),
 "contes": dict(
  title="نحكي قصة بسكراتش", duree="حصتان من 45 دقيقة", year="السنة السابعة",
  situation="كيف نجعل الشخصيات تمثّل قصة، فتتكلم كل واحدة في دورها وبالترتيب الصحيح، عند النقر على العلم الأخضر؟",
  steps=["وضعية مشكلة دون حاسوب (15 د)", "اكتشاف المشروع (10 د)", "قراءة السكربتات (15 د)", "تعديل موجَّه (20 د)", "اختبار وتصحيح (10 د)", "مشاركة (5 د)"],
  eleve=["افتح سكراتش، ثم «ملف ← تحميل من حاسوبك» واختر مشروع قصة.", "انقر على العلم الأخضر. اكتب بالترتيب ما تفعله الشخصيات.", "ابحث عن السكربت الذي يبدأ المشهد 2. أي كتلة تُطلقه؟", "غيّر جملة (كتلة «قل … لمدة 2 ثانية»)، ثم اختبر.", "أضف زيّا لشخصية واستعمل «بدّل الزي إلى…» في الوقت المناسب.", "تحدٍّ: أضف مشهدا سابعا (خلفية ورسالة «مشهد 7» وسكربت شخصية)."],
  criteres=["يبدأ المشروع بالعلم الأخضر.", "تتتابع المشاهد بالترتيب الصحيح.", "يُختبَر تعديل واحد على الأقل ويُبرَّر.", "يشرح التلميذ دور كتلة «عند استلام…»."],
  allegee="تعديل جملة واحدة فقط، ثم الاختبار والحفظ.",
  prolongement="مستوى السنة الثامنة: إضافة متغير عددي «المشاهد الممثَّلة» يزيد بواحد عند كل مشهد؛ وتجزئة القصة إلى مشكلات فرعية (مشهد = مشكلة فرعية) وتمثيلها بمخطط.",
  fr=dict(
   title="Raconter un conte avec Scratch", duree="2 séances de 45 minutes", year="7e année",
   situation="Comment faire jouer un conte par des personnages qui parlent chacun leur tour, dans le bon ordre, quand on clique sur le drapeau vert ?",
   steps=['Situation-problème sans ordinateur (15 min)', 'Découverte du projet (10 min)', 'Lecture de scripts (15 min)', 'Modification guidée (20 min)', 'Test et correction (10 min)', 'Partage (5 min)'],
   eleve=["Ouvre Scratch, puis « Fichier → Charger depuis votre ordinateur » et choisis le projet d'un conte.", "Clique sur le drapeau vert. Écris, dans l'ordre, ce que font les personnages.", 'Trouve le script qui démarre la scène 2. Quel bloc le déclenche ?', 'Change une réplique (bloc « dire … pendant 2 secondes »), puis teste.', 'Ajoute un costume à un personnage et utilise « basculer sur le costume… » au bon moment.', "Défi : ajoute une scène 7 (un arrière-plan, un message « scène 7 » et le script d'un personnage)."],
   criteres=['Le projet démarre avec le drapeau vert.', "Les scènes s'enchaînent dans le bon ordre.", 'Au moins une modification est testée et justifiée.', "L'élève explique le rôle du bloc « quand je reçois… »."],
   allegee="Ne modifier qu'une seule réplique, puis tester et enregistrer.",
   prolongement="Niveau 8e : ajouter une variable numérique « scènes jouées » qui augmente de 1 à chaque scène ; décomposer le conte en sous-problèmes (une scène = un sous-problème) et le représenter par un diagramme.")),
}
CATCH_STEPS = [  # (titre, légende) en arabe, même ordre que fiches_etapes.CATCH
 ("بداية اللعبة", "أنقر على العلم الأخضر: تصبح النقاط 0 والأرواح 3 والسرعة 3."),
 ("سمكة تسقط", "تظهر سمكة في أعلى المنصة عند موضع يُختار عشوائيا، ثم تسقط."),
 ("أحرّك الفأرة", "أحرّك الفأرة: يتبعها اللاعب ويقف تحت السمكة."),
 ("سمكة ملتقطة", "إذا لمس اللاعب السمكة: تزيد النقاط بواحد وتظهر سمكة جديدة."),
 ("سمكة فائتة", "إذا لمست السمكة أسفل المنصة: تنقص الأرواح بواحد."),
 ("نهاية اللعبة", "عندما تصل الأرواح إلى 0 تتوقف اللعبة: إنها نهاية الجولة.")]
COURSE_STEPS = [
 ("بداية اللعبة", "أنقر على العلم الأخضر: تصبح النقاط 0 والأرواح 3 والسرعة 3."),
 ("أحرّك السيارة", "أضغط على السهم الأيسر أو الأيمن: تتحرك السيارة دون أن تخرج من الطريق."),
 ("سيارة قادمة", "تظهر سيارة معاكسة في الأعلى عند موضع يُختار عشوائيا، وتنزل بسرعة اللعبة."),
 ("سيارة متفادَاة", "إذا مرّت السيارة إلى الأسفل دون أن تصدمني: تزيد النقاط بواحد والسرعة بـ 0٫15."),
 ("سيارة صادمة", "إذا صدمتني السيارة المعاكسة: أفقد روحا (يختفي قلب) ويُسمع صوت الاصطدام."),
 ("نهاية اللعبة", "عندما تصل الأرواح إلى 0 تظهر عبارة «نهاية اللعبة» وتتوقف اللعبة.")]
SAUT_STEPS = [
 ("بداية اللعبة", "أنقر على العلم الأخضر: تصبح النقاط 0 والأرواح 3 والسرعة 3."),
 ("شجيرة قادمة", "تظهر شجيرة في اليمين وتتقدم نحو اليسار بسرعة اللعبة."),
 ("أقفز", "أضغط على المسافة: يصعد الجمل ثم يهبط (تنقص الجاذبية سرعته بواحد في كل صورة)."),
 ("شجيرة متفادَاة", "إذا خرجت الشجيرة من المنصة دون أن تلمسني: تزيد النقاط بواحد والسرعة بـ 0٫15."),
 ("شجيرة ملموسة", "إذا كان الجمل على الأرض عند وصول الشجيرة: أفقد روحا (يختفي قلب) ويُسمع صوت الاصطدام."),
 ("نهاية اللعبة", "عندما تصل الأرواح إلى 0 تظهر عبارة «نهاية اللعبة» وتتوقف اللعبة.")]
LABY_STEPS = [
 ("بداية اللعبة", "أنقر على العلم الأخضر: تنطلق الفأرة من أسفل اليسار، ويبدأ الوقت من 60."),
 ("أحرّك الفأرة", "أستعمل الأسهم: في كل صورة يتغير س أو ص بمقدار 4 بعد حفظ الموضع السابق."),
 ("جدار يمنعني", "إذا دخلت منطقة جدار خارج الفتحة: أعود إلى الموضع السابق فلا أخترق الجدار."),
 ("أمرّ من الفتحة", "عند الفتحة يكون س خارج منطقة الجدار، فأواصل الصعود إلى الممر التالي."),
 ("نجمة ملتقطة", "إذا اقتربت الفأرة من نجمة (فرق صغير في س وفي ص): تزيد النقاط بواحد وتختفي النجمة."),
 ("الوصول إلى الجبن", "عندما يتجاوز ص القيمة 140: تظهر عبارة «فزت!» وتتوقف اللعبة. وإذا انتهى الوقت قبل ذلك تتوقف أيضا.")]
SCENE = ("المشهد", "Scène")
HEAD = {"الوضعية المشكلة": "Situation-problème", "مراحل اللعبة بالصور": "Les étapes en images", "سير الحصة": "Déroulement", "أنشطة التلميذ": "Activités de l'élève", "معايير النجاح": "Critères de réussite", "التمايز": "Différenciation",
        "التخفيف: ": "Allègement : ", "التوسيع: ": "Prolongement : ", "بطاقة النشاط: ": "Fiche d'activité : ", "تحميل مشروع سكراتش (.sb3)": "Télécharger le projet Scratch (.sb3)"}
