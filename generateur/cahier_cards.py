"""Fiches de notions du « cahier de l'élève » : pour chacune des 28 notions du planning (planning.py), quelques phrases à trous et un point à retenir.
Chaque texte est un couple (français, arabe) ; {{mot}} marque le mot à écrire par l'élève (il apparaît dans la « boîte à mots » et dans le corrigé).
Les deux langues contiennent le même nombre de trous. Les fiches d'une séance sont assemblées par cahier.py d'après les notions nouvelles ou approfondies de cette séance."""
LRI, PDI = "⁦", "⁩"
def L(s): return LRI + s + PDI        # isole un nombre ou un couple de nombres dans une phrase arabe

CARDS = {
 "seq": dict(
  fill=[("Un {{algorithme}} est une suite d'étapes précises où l'{{ordre}} compte, qui résout un problème.", "{{الخوارزمية}} سلسلة مراحل دقيقة يهمّ فيها {{الترتيب}}، تحلّ مشكلا."),
        ("Un {{programme}} est un algorithme écrit dans un langage que l'{{ordinateur}} comprend.", "{{البرنامج}} خوارزمية مكتوبة بلغة يفهمها {{الحاسوب}}."),
        ("Dans une {{séquence}}, les instructions s'exécutent l'une {{après}} l'autre.", "في {{التسلسل}} تُنفَّذ التعليمات واحدة {{بعد}} الأخرى.")],
  retain=[("Changer l'ordre des instructions change le résultat.", "تغيير ترتيب التعليمات يغيّر النتيجة.")]),
 "event": dict(
  fill=[("Un {{événement}} déclenche l'exécution d'un script.", "{{الحدث}} هو ما يُطلق تنفيذ السكربت."),
        ("Un script commence par un bloc {{chapeau}}, de couleur {{jaune}}.", "يبدأ السكربت بكتلة {{بداية}} لونها {{أصفر}}."),
        ("Exemples d'événements : le {{drapeau vert}}, une {{touche}} pressée, un {{clic}} sur le lutin.", "أمثلة للأحداث: {{العلم الأخضر}}، {{مفتاح}} مضغوط، {{نقرة}} على اللاعب.")],
  retain=[("Sans bloc événement, un script ne démarre pas tout seul.", "السكربت بلا كتلة حدث لا يبدأ من تلقاء نفسه.")]),
 "move": dict(
  fill=[("« avancer de 10 {{pas}} » déplace le lutin dans sa {{direction}}.", "«تحرك 10 {{خطوات}}» ينقل اللاعب في {{اتجاهه}}."),
        ("« tourner ↻ de 90 degrés » fait pivoter le lutin vers la {{droite}}.", "«استدر يمينا 90 درجة» يدير اللاعب نحو {{اليمين}}."),
        ("Un tour complet mesure {{360}} degrés.", "الدورة الكاملة قياسها {{360}} درجة.")],
  retain=[("Tourner avant d'avancer ou avancer avant de tourner : le lutin n'arrive pas au même endroit.", "الاستدارة قبل التحرك أو بعده: لا يصل اللاعب إلى المكان نفسه.")]),
 "look": dict(
  fill=[("« dire … pendant 2 secondes » affiche une {{bulle}} de parole.", "«قل … لمدة 2 ثانية» يُظهر {{فقاعة}} كلام."),
        ("Changer de {{costume}} donne l'impression de {{mouvement}}.", "تبديل {{الزي}} يوهم بوجود {{حركة}}."),
        ("Les arrière-plans de la scène sont les {{décors}}.", "خلفيات المنصة هي {{الديكورات}}.")],
  retain=[("« montrer » et « cacher » font apparaître et disparaître un lutin.", "«أظهر» و«أخفِ» يُظهران اللاعب ويُخفيانه.")]),
 "coord": dict(
  fill=[("Le centre de la scène a pour coordonnées " + L("({{0}}, {{0}})") + ".", "مركز المنصة إحداثياه " + L("({{0}}, {{0}})") + "."),
        ("{{x}} est la position horizontale (gauche ↔ droite) et {{y}} la position verticale (bas ↔ haut).", "الفاصلة {{س}} أفقية (يسار ↔ يمين) والترتيبة {{ص}} عمودية (أسفل ↔ أعلى)."),
        ("Pour aller vers la gauche, on {{diminue}} x ; pour monter, on {{augmente}} y.", "للذهاب نحو اليسار {{ننقص}} س؛ وللصعود {{نزيد}} ص.")],
  retain=[("Pour un point (x, y) : d'abord x (horizontal), puis y (vertical).", "للنقطة (س، ص): أولا س (أفقي) ثم ص (عمودي).")]),
 "msg": dict(
  fill=[("Un lutin peut {{envoyer}} un message à tous les lutins.", "يمكن للاعب أن {{يرسل}} رسالة إلى كل اللاعبين."),
        ("Les lutins qui {{reçoivent}} ce message démarrent un script « quand je reçois ».", "اللاعبون الذين {{يستلمون}} الرسالة يبدؤون سكربت «عند استلام»."),
        ("Les messages servent à enchaîner les {{scènes}} ou à faire {{dialoguer}} des lutins.", "تفيد الرسائل في ربط {{المشاهد}} أو جعل اللاعبين {{يتحاورون}}.")],
  retain=[("Un message est un signal que chaque lutin peut écouter.", "الرسالة إشارة يمكن لكل لاعب أن ينتبه إليها.")]),
 "sound": dict(
  fill=[("Les sons se gèrent dans l'onglet {{Sons}}.", "تُدار الأصوات في تبويب {{الأصوات}}."),
        ("« jouer le son … jusqu'au bout » {{attend}} la fin du son avant de continuer.", "«شغّل الصوت … حتى النهاية» {{ينتظر}} انتهاء الصوت قبل المتابعة.")],
  retain=[("On peut choisir un son dans la bibliothèque, l'enregistrer ou l'importer.", "يمكن اختيار صوت من المكتبة أو تسجيله أو رفعه.")]),
 "repeatn": dict(
  fill=[("« répéter {{n}} fois » répète les blocs qu'il contient un nombre {{connu}} de fois.", "«كرّر {{n}} مرات» يكرّر الكتل التي يحتويها عددا {{معلوما}} من المرات."),
        ("Pour dessiner un carré : répéter {{4}} fois [avancer, tourner de {{90}}°].", "لرسم مربع: كرّر {{4}} مرات [تحرك، استدر " + L("{{90}}°") + "].")],
  retain=[("Un seul bloc « répéter » remplace plusieurs blocs identiques.", "كتلة «كرّر» واحدة تعوّض عدة كتل متماثلة.")]),
 "forever": dict(
  fill=[("« répéter {{indéfiniment}} » ne s'arrête que si on clique sur le bouton {{Stop}}.", "«كرّر {{باستمرار}}» لا تتوقف إلا بالضغط على زر {{الإيقاف}}."),
        ("On l'utilise quand on veut {{surveiller}} sans arrêt une touche ou une collision.", "نستعملها عندما نريد {{مراقبة}} مفتاح أو اصطدام دون توقف.")],
  retain=[("On ne peut rien ajouter sous « répéter indéfiniment » : il ne se termine jamais.", "لا نضيف شيئا تحت «كرّر باستمرار» لأنها لا تنتهي أبدا.")]),
 "pen": dict(
  fill=[("Pour dessiner, on ajoute l'extension {{Stylo}}.", "للرسم نضيف امتداد {{القلم}}."),
        ("« stylo en position d'{{écriture}} » commence à tracer ; « {{relever}} le stylo » arrête de tracer.", "«{{أنزل}} القلم» يبدأ الرسم؛ و«{{ارفع}} القلم» يوقفه."),
        ("« {{effacer}} tout » nettoie la scène.", "«{{امسح}} الكل» ينظّف المنصة.")],
  retain=[("Sans « stylo en position d'écriture », le lutin ne laisse aucune trace.", "بدون «أنزل القلم» لا يترك اللاعب أي أثر.")]),
 "sense": dict(
  fill=[("Un {{capteur}} donne une {{information}} au programme.", "{{المستشعر}} يعطي البرنامج {{معلومة}}."),
        ("Exemples : « touche le bord ? », « touche espace {{pressée}} ? », « {{distance}} de la souris ».", "أمثلة: «هل تلمس الحافة؟»، «هل مفتاح المسافة {{مضغوط}}؟»، «{{المسافة}} إلى الفأرة»."),
        ("Les blocs capteurs sont de couleur {{bleu clair}}.", "كتل الاستشعار لونها {{أزرق فاتح}}.")],
  retain=[("Un capteur lit une information ; c'est la condition qui décide quoi faire.", "المستشعر يقرأ معلومة؛ والشرط هو الذي يقرر ماذا نفعل.")]),
 "if": dict(
  fill=[("Une {{condition}} a pour réponse {{vrai}} ou {{faux}}.", "{{الشرط}} جوابه {{صحيح}} أو {{خطأ}}."),
        ("« si … alors » exécute ses blocs {{seulement}} si la condition est {{vraie}}.", "«إذا … فإن» تنفّذ كتلها {{فقط}} إذا كان الشرط {{صحيحا}}."),
        ("Pour tester une condition sans arrêt, on place le « si » dans un « répéter {{indéfiniment}} ».", "لاختبار شرط باستمرار نضع «إذا» داخل «كرّر {{باستمرار}}».")],
  retain=[("« si … alors » n'a qu'un chemin : si la condition est fausse, il ne se passe rien.", "«إذا … فإن» لها طريق واحد: إذا كان الشرط خطأ فلا يحدث شيء.")]),
 "ifelse": dict(
  fill=[("« si … alors … {{sinon}} » choisit entre {{deux}} chemins.", "«إذا … فإن … {{وإلا}}» تختار بين {{طريقين}}."),
        ("Si la condition est {{fausse}}, les blocs du « sinon » s'exécutent.", "إذا كان الشرط {{خطأ}} نُفِّذت كتل «وإلا».")],
  retain=[("Un seul des deux chemins est exécuté à chaque passage.", "يُنفَّذ طريق واحد فقط من الاثنين في كل مرة.")]),
 "project": dict(
  fill=[("Un projet se réalise en étapes : {{concevoir}}, {{réaliser}}, {{tester}}, {{présenter}}.", "ينجز المشروع على مراحل: {{التصميم}}، {{الإنجاز}}، {{الاختبار}}، {{العرض}}."),
        ("Avant de programmer, j'écris le {{scénario}} : personnages, décors et événements.", "قبل البرمجة أكتب {{السيناريو}}: الشخصيات والخلفيات والأحداث.")],
  retain=[("Je teste mon projet après chaque étape.", "أختبر مشروعي بعد كل مرحلة.")]),
 "decomp": dict(
  fill=[("Décomposer, c'est découper un {{problème}} en {{sous-problèmes}} plus simples.", "التجزئة هي تقسيم {{مشكل}} إلى {{مشكلات فرعية}} أبسط."),
        ("Un {{diagramme}} montre les étapes de la solution ; chaque flèche mène à l'étape {{suivante}}.", "{{المخطط}} يُظهر مراحل الحل؛ وكل سهم يقود إلى المرحلة {{التالية}}.")],
  retain=[("Chaque sous-problème devient un petit script ou un module.", "كل مشكل فرعي يصبح سكربتا صغيرا أو وحدة.")]),
 "read": dict(
  fill=[("Lire un script, c'est {{prévoir}} ce qu'il fait avant de l'exécuter.", "قراءة سكربت تعني {{توقّع}} ما يفعله قبل تنفيذه."),
        ("On lit un script de {{haut}} en {{bas}}, bloc après bloc.", "نقرأ السكربت من {{الأعلى}} إلى {{الأسفل}} كتلة بعد كتلة.")],
  retain=[("Prévoir, exécuter, expliquer : trois temps pour comprendre un script.", "توقّع، نفّذ، فسّر: ثلاث خطوات لفهم سكربت.")]),
 "op": dict(
  fill=[("Les opérateurs sont de couleur {{verte}} : calculs et comparaisons.", "كتل العمليات لونها {{أخضر}}: حسابات ومقارنات."),
        ("« 5 > 3 » est {{vrai}} ; « 2 > 7 » est {{faux}}.", "«5 > 3» {{صحيح}}؛ و«2 > 7» {{خطأ}}."),
        ("Pour comparer deux valeurs, on utilise <, > ou {{=}}.", "لمقارنة قيمتين نستعمل < أو > أو {{=}}.")],
  retain=[("Une comparaison donne toujours vrai ou faux.", "المقارنة تعطي دائما صحيح أو خطأ.")]),
 "var": dict(
  fill=[("Une {{variable}} est une case mémoire qui a un {{nom}}, et qui contient une {{valeur}}.", "{{المتغير}} خانة ذاكرة لها {{اسم}}، وتحمل {{قيمة}}."),
        ("« mettre … à 0 » {{initialise}} la variable ; « ajouter 1 à … » l'{{augmente}} de 1.", "«اجعل … = 0» {{يهيّئ}} المتغير؛ و«غيّر … بمقدار 1» {{يزيده}} بواحد."),
        ("La variable qui compte les points s'appelle souvent « {{score}} ».", "يسمّى المتغير الذي يعدّ النقاط غالبا «{{النقاط}}».")],
  retain=[("J'initialise toujours une variable au début du script.", "أهيّئ المتغير دائما في بداية السكربت.")]),
 "rand": dict(
  fill=[("« nombre aléatoire entre 1 et 10 » donne un nombre {{au hasard}}.", "«عدد عشوائي بين 1 و10» يعطي عددا {{عشوائيا}}."),
        ("Le hasard rend le jeu {{imprévisible}}.", "العشوائية تجعل اللعبة {{غير متوقعة}}.")],
  retain=[("Le hasard permet de placer un objet à des endroits différents à chaque partie.", "العشوائية تتيح وضع شيء في أماكن مختلفة في كل لعبة.")]),
 "input": dict(
  fill=[("« demander … et attendre » pose une {{question}} au joueur.", "«اسأل … وانتظر» يطرح {{سؤالا}} على اللاعب."),
        ("La réponse du joueur est stockée dans le bloc « {{réponse}} ».", "تُخزَّن إجابة اللاعب في كتلة «{{الإجابة}}».")],
  retain=[("On compare la réponse avec la bonne valeur grâce à une condition.", "نقارن الإجابة بالقيمة الصحيحة بواسطة شرط.")]),
 "module": dict(
  fill=[("Un {{module}} (bloc personnalisé) regroupe des blocs sous un {{nom}}.", "{{الوحدة}} (كتلة خاصة) تجمع كتلا تحت {{اسم}}."),
        ("On le {{définit}} une seule fois, puis on l'{{appelle}} autant de fois qu'on veut.", "{{نعرّفها}} مرة واحدة ثم {{نستدعيها}} كلما أردنا.")],
  retain=[("Un module évite de recopier les mêmes blocs.", "الوحدة تجنّبنا إعادة كتابة الكتل نفسها.")]),
 "param": dict(
  fill=[("Un {{paramètre}} est une valeur donnée au module au moment de l'{{appel}}.", "{{المعامل}} قيمة تُعطى للوحدة عند {{الاستدعاء}}."),
        ("Grâce au paramètre, un même module dessine des figures de {{tailles}} différentes.", "بفضل المعامل ترسم الوحدة نفسها أشكالا ذات {{أحجام}} مختلفة.")],
  retain=[("Le paramètre rend le module plus général.", "المعامل يجعل الوحدة أعمّ.")]),
 "debug": dict(
  fill=[("Un {{bug}} est une erreur dans un programme.", "{{الخطأ البرمجي}} (bug) خطأ في برنامج."),
        ("Déboguer, c'est {{tester}}, trouver l'erreur, la {{corriger}}, puis {{retester}}.", "تصحيح الأخطاء هو {{الاختبار}} ثم إيجاد الخطأ ثم {{تصحيحه}} ثم {{إعادة الاختبار}}.")],
  retain=[("Je change une seule chose à la fois, puis je teste.", "أغيّر شيئا واحدا في كل مرة ثم أختبر.")]),
 "until": dict(
  fill=[("« répéter jusqu'à ce que … » répète les blocs jusqu'à ce que la condition devienne {{vraie}}.", "«كرّر حتى …» تكرّر الكتل إلى أن يصبح الشرط {{صحيحا}}."),
        ("Exemple : répéter jusqu'à ce que le chronomètre soit {{supérieur}} à 30.", "مثال: كرّر حتى يصبح المؤقّت {{أكبر}} من 30.")],
  retain=[("La condition est testée avant chaque tour.", "يُختبر الشرط قبل كل دورة.")]),
 "opt": dict(
  fill=[("Optimiser, c'est {{améliorer}} un script : moins de blocs, plus de {{clarté}}.", "التحسين هو {{تجويد}} سكربت: كتل أقل، {{وضوح}} أكبر."),
        ("On remplace des blocs identiques par une {{boucle}} ou un {{module}}.", "للتعويض عن الكتل المتماثلة نستعمل {{حلقة}} أو {{وحدة}}.")],
  retain=[("Après chaque amélioration, je teste que le résultat est resté le même.", "بعد كل تحسين أتأكد بالاختبار أن النتيجة لم تتغير.")]),
 "inout": dict(
  fill=[("Un système a des {{entrées}}, un {{traitement}} et des {{sorties}}.", "لكل نظام: {{مدخلات}}، {{معالجة}}، {{مخرجات}}."),
        ("Exemple : entrée = la réponse du joueur ; traitement = la {{comparaison}} ; sortie = « {{Bravo}} ! ».", "مثال: المدخل = إجابة اللاعب؛ المعالجة = {{المقارنة}}؛ المخرج = «{{أحسنت}}!».")],
  retain=[("Je repère d'abord les entrées et les sorties, puis j'écris le traitement.", "أحدّد أولا المدخلات والمخرجات ثم أكتب المعالجة.")]),
 "sensact": dict(
  fill=[("Un {{capteur}} mesure ; un {{actionneur}} agit.", "{{المستشعر}} يقيس، أما {{المنفّذ}} فيفعل."),
        ("Le principe : {{mesurer}}, {{décider}}, {{agir}}.", "المبدأ: {{القياس}}، {{القرار}}، {{الفعل}}.")],
  retain=[("Sans matériel, on simule les capteurs et les actionneurs avec des variables et des images dans le simulateur.", "عند غياب العتاد نحاكي المستشعرات والمنفّذات بالمتغيرات والصور في المحاكي.")]),
 "share": dict(
  fill=[("Quand je remixe un projet, je {{cite}} son {{auteur}}.", "عندما أعيد صياغة مشروع {{أذكر}} {{صاحبه}}."),
        ("Avant de partager, je vérifie les {{droits}} des images et des sons.", "قبل المشاركة أتحقق من {{حقوق}} الصور والأصوات."),
        ("Je choisis un {{espace}} de partage adapté à mon {{âge}}.", "أختار {{فضاء}} مشاركة يناسب {{سنّي}}.")],
  retain=[("Je ne partage jamais d'informations personnelles.", "لا أشارك أبدا معلومات شخصية.")]),
}
