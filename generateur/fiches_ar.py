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
SCENE = ("المشهد", "Scène")
HEAD = {"الوضعية المشكلة": "Situation-problème", "مراحل اللعبة بالصور": "Les étapes en images", "سير الحصة": "Déroulement", "أنشطة التلميذ": "Activités de l'élève", "معايير النجاح": "Critères de réussite", "التمايز": "Différenciation",
        "التخفيف: ": "Allègement : ", "التوسيع: ": "Prolongement : ", "بطاقة النشاط: ": "Fiche d'activité : ", "تحميل مشروع سكراتش (.sb3)": "Télécharger le projet Scratch (.sb3)"}
