"""Accès élève : exercices auto-corrigés (QCM) et activités à créer, par niveau et par module. Bilingue AR/FR.
Q(ar, fr, [(ar, fr), ...], index_bonne_réponse)"""
def Q(ar, fr, opts, a): return dict(q=ar, q_fr=fr, o=[x[0] for x in opts], o_fr=[x[1] for x in opts], a=a)
def A(t, t_fr, d, d_fr, link=None, ex=None, ex_fr=None): return dict(t=t, t_fr=t_fr, d=d, d_fr=d_fr, link=link, ex=ex, ex_fr=ex_fr)
EXO = {
 "7-env": [
  Q("أي هذه الأجهزة هو وحدة إدخال؟", "Lequel de ces appareils est un périphérique d'entrée ?", [("الطابعة", "L'imprimante"), ("لوحة المفاتيح", "Le clavier"), ("مكبر الصوت", "Le haut-parleur")], 1),
  Q("ما وظيفة الذاكرة الحية (RAM)؟", "À quoi sert la mémoire vive (RAM) ?", [("حفظ الملفات بصفة دائمة", "Conserver les fichiers définitivement"), ("حفظ ما يشتغل به الحاسوب مؤقتا", "Garder temporairement ce que l'ordinateur utilise"), ("عرض الصور على الشاشة", "Afficher les images à l'écran")], 1),
  Q("أي وحدة أكبر؟", "Quelle unité est la plus grande ?", [("ميغابايت", "Mo"), ("كيلوبايت", "Ko"), ("غيغابايت", "Go")], 2),
  Q("ما امتداد الملف في «صورة.png»؟", "Quelle est l'extension du fichier « photo.png » ?", [("photo", "photo"), ("png", "png"), ("photo.png", "photo.png")], 1),
  Q("أي عملية تنقل ملفا من مجلد إلى آخر دون ترك نسخة؟", "Quelle opération déplace un fichier sans laisser de copie ?", [("نسخ", "Copier"), ("قص ولصق", "Couper puis coller"), ("إعادة تسمية", "Renommer")], 1)],
 "7-net": [
  Q("ما الأنسب للبحث عن «حياة الدلافين»؟", "Quelle requête convient pour chercher des infos sur la vie des dauphins ?", [("كلمات مفتاحية: دلافين، حياة، تغذية", "Mots-clés : dauphins, vie, alimentation"), ("حرف واحد", "Une seule lettre"), ("جملة طويلة جدا بلا معنى", "Une très longue phrase sans sens")], 0),
  Q("ما الذي يجب التحقق منه في مصدر معلومة؟", "Que faut-il vérifier dans la source d'une information ?", [("لون الصفحة", "La couleur de la page"), ("المصدر والتاريخ", "La source et la date"), ("عدد الصور", "Le nombre d'images")], 1),
  Q("هل يمكن نسخ صورة من الإنترنت دون ذكر صاحبها؟", "Peut-on copier une image d'Internet sans citer son auteur ?", [("نعم دائما", "Oui, toujours"), ("لا، يجب احترام حقوق المؤلف", "Non, il faut respecter les droits d'auteur"), ("نعم إذا كانت جميلة", "Oui si elle est belle")], 1),
  Q("ماذا نفعل قبل نشر وثيقة في فضاء القسم؟", "Que fait-on avant de publier un document dans l'espace de la classe ?", [("نتأكد أنه لا يحتوي بيانات خاصة", "On vérifie qu'il ne contient pas de données personnelles"), ("ننشره فورا", "On le publie tout de suite"), ("نحذف اسمه فقط", "On supprime seulement son nom")], 0)],
 "7-create": [
  Q("ما الخطوة الأولى لإنجاز ملصق؟", "Quelle est la première étape pour réaliser une affiche ?", [("اختيار الخط", "Choisir la police"), ("تخطيط الفكرة والمحتوى", "Planifier l'idée et le contenu"), ("طباعته", "L'imprimer")], 1),
  Q("أي صيغة تصلح لتصدير ملصق للطباعة؟", "Quel format convient pour exporter une affiche à imprimer ?", [("PDF", "PDF"), ("MP3", "MP3"), ("EXE", "EXE")], 0),
  Q("أي صور يمكن استعمالها بأمان؟", "Quelles images peut-on utiliser sans risque ?", [("أي صورة من الإنترنت", "N'importe quelle image d'Internet"), ("صور حرة الحقوق مع ذكر المصدر", "Des images libres de droits avec la source citée"), ("صور الآخرين دون إذن", "Des images d'autres personnes sans autorisation")], 1),
  Q("ماذا نفعل بعد استعمال أداة ذكاء اصطناعي في إنتاج؟", "Que fait-on après avoir utilisé un outil d'IA pour une production ?", [("نقبل كل شيء", "On accepte tout"), ("نراجع النتيجة ونبرر ما احتفظنا به", "On relit le résultat et on justifie ce qu'on garde"), ("نخفي استعمالها", "On cache son utilisation")], 1)],
 "7-prog": [
  Q("ما الكتلة التي تبدأ السكربت عند الضغط على العلم الأخضر؟", "Quel bloc démarre le script quand on clique sur le drapeau vert ?", [("«عند النقر على العلم الأخضر»", "« quand le drapeau vert est cliqué »"), ("«انتظر ثانية»", "« attendre 1 seconde »"), ("«قل مرحبا»", "« dire Bonjour »")], 0),
  Q("أي كتلة تكرر التعليمات دون توقف؟", "Quel bloc répète des instructions sans s'arrêter ?", [("كرر 10 مرات", "répéter 10 fois"), ("كرر باستمرار", "répéter indéfiniment"), ("إذا… فإن", "si… alors")], 1),
  Q("«إذا كانت الإجابة صحيحة فإن… وإلا…» هي:", "« si la réponse est juste alors… sinon… » est :", [("شرط كامل", "une condition complète"), ("حلقة", "une boucle"), ("حدث", "un événement")], 0),
  Q("ما دور «عند استلام رسالة»؟", "Quel est le rôle de « quand je reçois un message » ?", [("بدء سكربت عند استلام رسالة", "Démarrer un script à la réception d'un message"), ("تغيير الخلفية", "Changer le décor"), ("إيقاف المشروع", "Arrêter le projet")], 0),
  Q("ماذا نفعل إذا لم يعمل البرنامج كما نريد؟", "Que fait-on si le programme ne marche pas comme prévu ?", [("نتخلى عنه", "On abandonne"), ("نختبر ونجد الخطأ ونصححه", "On teste, on trouve l'erreur et on la corrige"), ("نحذف كل شيء", "On supprime tout")], 1)],
 "8-env": [
  Q("برنامج يتنكر في شكل ملف عادي ويفتح بابا للمتسلل يسمى:", "Un logiciel qui se cache dans un fichier normal et ouvre la porte à un pirate s'appelle :", [("حصان طروادة", "un cheval de Troie"), ("مضاد فيروسات", "un antivirus"), ("متصفح", "un navigateur")], 0),
  Q("أي كلمة سر هي الأقوى؟", "Quel mot de passe est le plus robuste ?", [("123456", "123456"), ("اسمك", "ton prénom"), ("جملة طويلة بحروف وأرقام ورموز", "une longue phrase avec lettres, chiffres et symboles")], 2),
  Q("وصلتك رسالة تطلب كلمة سرك بدعوى ربح جائزة. إنها:", "Un message demande ton mot de passe pour un prix gagné. C'est :", [("تصيد احتيالي", "de l'hameçonnage"), ("هدية حقيقية", "un vrai cadeau"), ("تحديث للنظام", "une mise à jour")], 0),
  Q("ما الذي يحمي الحاسوب من الدخول غير المرخص عبر الشبكة؟", "Qu'est-ce qui protège l'ordinateur des accès non autorisés par le réseau ?", [("جدار الحماية", "Le pare-feu"), ("الطابعة", "L'imprimante"), ("الفأرة", "La souris")], 0)],
 "8-net": [
  Q("ما معنى «آداب التواصل عبر الشبكة» (Nétiquette)؟", "Que signifie la « nétiquette » ?", [("قواعد الاحترام في التواصل عبر الإنترنت", "Les règles de respect dans la communication en ligne"), ("اسم برنامج", "Le nom d'un logiciel"), ("نوع حاسوب", "Un type d'ordinateur")], 0),
  Q("أي هذه معطيات شخصية؟", "Laquelle est une donnée personnelle ?", [("عنوان بيتك ورقم هاتفك", "Ton adresse et ton numéro de téléphone"), ("لون سماء", "La couleur du ciel"), ("اسم حيوان خيالي", "Le nom d'un animal imaginaire")], 0),
  Q("ما فائدة الكتابة التعاونية؟", "À quoi sert l'écriture collaborative ?", [("إنتاج وثيقة بمساهمة عدة أشخاص", "Produire un document à plusieurs"), ("حذف الملفات", "Supprimer des fichiers"), ("حماية الحاسوب", "Protéger l'ordinateur")], 0),
  Q("نشرت معلومة كاذبة عن زميل. ماذا يمكن أن يحدث؟", "Tu as publié une fausse information sur un camarade. Que peut-il arriver ?", [("لا شيء", "Rien"), ("ضرر لسمعته وعقوبات", "Du tort à sa réputation et des sanctions"), ("يصبح مشهورا فقط", "Il devient célèbre")], 1)],
 "8-create": [
  Q("ما أول خطوة في إنتاج بودكاست؟", "Quelle est la première étape pour produire un podcast ?", [("التسجيل مباشرة", "Enregistrer tout de suite"), ("كتابة السيناريو", "Écrire le scénario"), ("نشره", "Le publier")], 1),
  Q("ما «الاختفاء التدريجي» (fondu) في الصوت؟", "Qu'est-ce qu'un fondu en audio ?", [("ارتفاع أو انخفاض تدريجي للصوت", "Une montée ou baisse progressive du volume"), ("حذف المقطع", "Supprimer le morceau"), ("تسجيل جديد", "Un nouvel enregistrement")], 0),
  Q("ماذا نضيف في بداية فيديو؟", "Que ajoute-t-on au début d'une vidéo ?", [("عنوان", "Un titre"), ("فيروسا", "Un virus"), ("ملف مضغوط", "Un fichier compressé")], 0),
  Q("لماذا نختار صيغة تصدير مناسبة؟", "Pourquoi choisir un format d'export adapté ?", [("لتناسب طريقة العرض", "Pour qu'il convienne à sa diffusion"), ("لنجعله أثقل", "Pour l'alourdir"), ("لا فائدة", "Aucune utilité")], 0)],
 "8-prog": [
  Q("متى نحتاج إلى متغير في لعبة؟", "Quand a-t-on besoin d'une variable dans un jeu ?", [("لحفظ قيمة تتغير مثل النقاط", "Pour garder une valeur qui change, comme le score"), ("لتغيير الخلفية", "Pour changer le décor"), ("لإنهاء اللعبة فقط", "Seulement pour finir le jeu")], 0),
  Q("ما معنى «تهيئة» المتغير؟", "Que veut dire « initialiser » une variable ?", [("إعطاؤه قيمة البداية", "Lui donner sa valeur de départ"), ("حذفه", "La supprimer"), ("تسميته فقط", "Seulement la nommer")], 0),
  Q("«غيّر النقاط بـ 1» تسمى:", "« ajouter 1 aux points » s'appelle :", [("زيادة (Incrémentation)", "une incrémentation"), ("حلقة", "une boucle"), ("حدث", "un événement")], 0),
  Q("ما فائدة الوحدة (Mon bloc)؟", "À quoi sert un module (« Mon bloc ») ?", [("تجميع تعليمات متكررة تحت اسم واحد", "Regrouper des instructions répétées sous un nom"), ("تغيير الزي", "Changer de costume"), ("تسجيل صوت", "Enregistrer un son")], 0),
  Q("بعد اكتشاف خطأ في البرنامج نقوم بـ:", "Après avoir trouvé une erreur dans le programme, on :", [("نصححه ثم نختبر من جديد", "la corrige puis on teste à nouveau"), ("نتجاهله", "l'ignore"), ("نغلق البرنامج", "ferme le programme")], 0)],
 "9-prog": [
  Q("ما المستشعر؟", "Qu'est-ce qu'un capteur ?", [("عنصر يقيس معطيات من المحيط", "Un élément qui mesure une donnée de l'environnement"), ("عنصر يحرك محركا", "Un élément qui actionne un moteur"), ("شاشة", "Un écran")], 0),
  Q("ما المنفّذ (Actionneur)؟", "Qu'est-ce qu'un actionneur ?", [("عنصر ينفذ فعلا مثل محرك أو مصباح", "Un élément qui agit, comme un moteur ou une lampe"), ("برنامج حماية", "Un antivirus"), ("ذاكرة", "Une mémoire")], 0),
  Q("لتحليل مشكل نحدد:", "Pour analyser un problème, on identifie :", [("المدخلات والمعالجة والمخرجات", "les entrées, le traitement et les sorties"), ("اللون فقط", "seulement la couleur"), ("اسم البرنامج فقط", "seulement le nom du programme")], 0),
  Q("أي إجراء يحسّن حلا؟", "Quelle démarche permet d'améliorer une solution ?", [("اختباره ومقارنة النتائج", "Le tester et comparer les résultats"), ("تركه كما هو", "Le laisser tel quel"), ("حذفه", "Le supprimer")], 0)],
 "9-prod": [
  Q("ما هي «الخلية» في الجدول؟", "Qu'est-ce qu'une cellule dans un tableur ?", [("تقاطع عمود وسطر", "L'intersection d'une colonne et d'une ligne"), ("اسم ملف", "Un nom de fichier"), ("نوع رسم", "Un type de graphique")], 0),
  Q("ماذا تبدأ به الصيغة في الجدول؟", "Par quoi commence une formule dans un tableur ?", [("=", "="), ("#", "#"), ("?", "?")], 0),
  Q("أي دالة تحسب المعدل؟", "Quelle fonction calcule la moyenne ?", [("MOYENNE / AVERAGE", "MOYENNE / AVERAGE"), ("MAX", "MAX"), ("SI", "SI")], 0),
  Q("أي رسم مناسب لمقارنة أجزاء من كل؟", "Quel graphique convient pour comparer des parts d'un tout ?", [("الدائري", "Le secteur (camembert)"), ("المنحنى", "La courbe"), ("لا شيء", "Aucun")], 0),
  Q("ما المرجع المطلق (مثل $A$1) ؟", "Que fait une référence absolue (comme $A$1) ?", [("تبقى ثابتة عند النسخ", "Elle reste fixe quand on recopie"), ("تتغير دائما", "Elle change toujours"), ("تحذف الخلية", "Elle supprime la cellule")], 0)],
}
ACT = {
 "7-env": [A("خريطة حاسوبي", "La carte de mon ordinateur", "ارسم حاسوبا وأشر بأسهم إلى أجزائه وكتب وظيفة كل جزء.", "Dessine un ordinateur et indique avec des flèches ses parties et leur fonction.")],
 "7-net": [A("دليل البحث الجيد", "Mon guide pour bien chercher", "اكتب خمس قواعد للبحث الجيد مع مثال لكل قاعدة.", "Écris cinq règles pour bien chercher, avec un exemple pour chacune.")],
 "7-create": [A("ملصق عن مدرستي", "Une affiche sur mon école", "صمم ملصقا فيه عنوان ونص وصورتان حرتان مع ذكر المصدر.", "Crée une affiche avec un titre, un texte et deux images libres, source citée.", "#library")],
 "7-prog": [A("مثّل قصة بسكراتش", "Joue un conte avec Scratch", "افتح مشروعا من قصص الموقع، غيّر جملة وأضف زيّا ثم اختبر وقدّم عملك.", "Ouvre un conte du site, modifie une réplique, ajoute un costume, teste et présente.", "#y7-prog", "مثال: غيّر جملة جحا في المشهد 1.", "Exemple : change la réplique de Jeha à la scène 1.")],
 "8-env": [A("دليل الحماية", "Mon guide de protection", "ألّف دليلا من سبع نصائح للحماية مع كلمة سر نموذجية وهمية.", "Rédige un guide de sept conseils de protection avec un mot de passe fictif en exemple.")],
 "8-net": [A("ميثاق القسم الرقمي", "La charte numérique de la classe", "اكتب بالتعاون مع زملائك ميثاقا لآداب التواصل.", "Écris avec tes camarades une charte de bonne conduite en ligne.")],
 "8-create": [A("حلقة بودكاست قصيرة", "Un court podcast", "سجّل حلقة من دقيقتين على الأكثر مع موسيقى خلفية.", "Enregistre un épisode de deux minutes maximum avec une musique de fond.", "#library")],
 "8-prog": [A("أكمل لعبة بمتغير", "Complète un jeu avec une variable", "افتح لعبة من الموقع، أضف متغيرا للنقاط ووحدة، ثم اختبر وحسّن.", "Ouvre un jeu du site, ajoute une variable pour les points et un module, teste et améliore.", "#y8-prog", "مثال: زد النقاط عند كل إجابة صحيحة.", "Exemple : ajoute 1 point à chaque bonne réponse.")],
 "9-prog": [A("مشروع برمجة بكائن", "Un projet avec un objet", "حدد مشكلا، حلّله (مدخلات، معالجة، مخرجات)، برمجه واختبره.", "Choisis un problème, analyse-le (entrées, traitement, sorties), programme-le et teste-le.", "#y9-prog")],
 "9-prod": [A("جدول قرار", "Un tableau d'aide à la décision", "أنشئ جدول بيانات بصيغ ودالة وتمثيل بياني لتساعد على اتخاذ قرار.", "Crée un tableau avec formules, une fonction et un graphique pour aider à décider.")],
}
