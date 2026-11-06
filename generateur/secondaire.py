"""Niveaux secondaires : domaines et exercices PROPOSÉS (non officiels : aucun programme officiel n'a été fourni).
Les thèmes sont généraux (algorithmique/Python, information et données, systèmes et réseaux) et à adapter au programme réel."""
from exercices import Q
DOM = {"sa": ("Algorithmique et programmation", "الخوارزميات والبرمجة"), "si": ("Information et données", "المعلومة والمعطيات"), "sr": ("Systèmes et réseaux", "الأنظمة والشبكات")}
COMPS = {
 "s1": {"sa": ("Écrire des algorithmes simples et les traduire en Python.", "كتابة خوارزميات بسيطة وترجمتها إلى بايثون."),
        "si": ("Représenter et organiser l'information (binaire, texte, fichiers).", "تمثيل المعلومة وتنظيمها (النظام الثنائي، النص، الملفات)."),
        "sr": ("Comprendre le fonctionnement d'un ordinateur et d'Internet.", "فهم عمل الحاسوب والإنترنت.")},
 "s2": {"sa": ("Utiliser conditions, boucles, fonctions et tableaux.", "استعمال الشروط والحلقات والدوال والجداول."),
        "si": ("Traiter des données avec un tableur.", "معالجة المعطيات بجدول بيانات."),
        "sr": ("Connaître l'architecture d'un réseau et les protocoles de base.", "معرفة بنية الشبكة والبروتوكولات الأساسية.")},
 "s3": {"sa": ("Concevoir des programmes modulaires et analyser leur efficacité.", "تصميم برامج نمطية وتحليل نجاعتها."),
        "si": ("Modéliser et interroger une base de données.", "نمذجة قاعدة بيانات والاستعلام عنها."),
        "sr": ("Comprendre la sécurité et le chiffrement des données.", "فهم أمن المعطيات وتشفيرها.")},
 "s4": {"sa": ("Résoudre des problèmes par des algorithmes avancés (tris, recherche, récursivité).", "حل المشكلات بخوارزميات متقدمة (الفرز، البحث، العودية)."),
        "si": ("Concevoir et exploiter une base de données relationnelle (SQL).", "تصميم قاعدة بيانات علائقية واستغلالها (SQL)."),
        "sr": ("Maîtriser les notions de réseaux, de web et de sécurité.", "التحكم في مفاهيم الشبكات والويب والأمن.")},
}
EXO = {
 "s1-sa": [
  Q("ماذا يطبع: x = 3 ; x = x + 2 ; print(x)؟", "Que affiche : x = 3 ; x = x + 2 ; print(x) ?", [("5", "5"), ("3", "3"), ("2", "2")], 0),
  Q("أي كلمة تستعمل لتكرار تعليمات عدة مرات في بايثون؟", "Quel mot sert à répéter des instructions en Python ?", [("for", "for"), ("print", "print"), ("def", "def")], 0),
  Q("ما نوع القيمة 3.5 ؟", "Quel est le type de la valeur 3.5 ?", [("عدد عشري (float)", "un flottant (float)"), ("نص (str)", "une chaîne (str)"), ("عدد صحيح (int)", "un entier (int)")], 0),
  Q("ما الخوارزمية؟", "Qu'est-ce qu'un algorithme ?", [("سلسلة منتهية من التعليمات لحل مشكل", "Une suite finie d'instructions pour résoudre un problème"), ("لغة برمجة", "Un langage de programmation"), ("جهاز", "Un appareil")], 0),
  Q("ما نتيجة 7 % 3 في بايثون؟", "Quel est le résultat de 7 % 3 en Python ?", [("1", "1"), ("2", "2"), ("0", "0")], 0)],
 "s1-si": [
  Q("ما العدد 101 في النظام العشري؟ (101 ثنائي)", "Que vaut 101 (en binaire) en décimal ?", [("5", "5"), ("3", "3"), ("101", "101")], 0),
  Q("كم بتا في البايت؟", "Combien de bits dans un octet ?", [("8", "8"), ("4", "4"), ("16", "16")], 0),
  Q("أي امتداد لملف نصي؟", "Quelle extension correspond à un fichier texte ?", [(".txt", ".txt"), (".mp3", ".mp3"), (".exe", ".exe")], 0),
  Q("ما معنى كيلوبايت (Ko) تقريبا؟", "Que représente environ 1 Ko ?", [("ألف بايت", "mille octets"), ("ألف بت فقط", "mille bits seulement"), ("مليون بايت", "un million d'octets")], 0)],
 "s1-sr": [
  Q("ما دور المعالج؟", "Quel est le rôle du processeur ?", [("تنفيذ التعليمات", "Exécuter les instructions"), ("تخزين الملفات دائما", "Stocker les fichiers définitivement"), ("عرض الصورة", "Afficher l'image")], 0),
  Q("ما البروتوكول المستعمل لصفحات الويب المؤمنة؟", "Quel protocole sert aux pages web sécurisées ?", [("HTTPS", "HTTPS"), ("FTP", "FTP"), ("SMTP", "SMTP")], 0),
  Q("ما نظام أسماء النطاقات (DNS)؟", "À quoi sert le DNS ?", [("ترجمة اسم موقع إلى عنوان IP", "Traduire un nom de site en adresse IP"), ("حماية الحاسوب", "Protéger l'ordinateur"), ("تسريع الطابعة", "Accélérer l'imprimante")], 0),
  Q("ما نظام التشغيل؟", "Qu'est-ce qu'un système d'exploitation ?", [("برنامج يدير موارد الحاسوب", "Un logiciel qui gère les ressources de l'ordinateur"), ("جهاز إدخال", "Un périphérique d'entrée"), ("موقع ويب", "Un site web")], 0)],
 "s2-sa": [
  Q("ماذا يطبع: for i in range(3): print(i) ؟", "Que affiche : for i in range(3): print(i) ?", [("0 1 2", "0 1 2"), ("1 2 3", "1 2 3"), ("0 1 2 3", "0 1 2 3")], 0),
  Q("ما فائدة الدالة؟", "À quoi sert une fonction ?", [("تجميع تعليمات تُستدعى باسمها", "Regrouper des instructions appelées par leur nom"), ("حذف المتغيرات", "Supprimer des variables"), ("تغيير الشاشة", "Changer d'écran")], 0),
  Q("ما فهرس العنصر الأول في قائمة بايثون؟", "Quel est l'indice du premier élément d'une liste Python ?", [("0", "0"), ("1", "1"), ("-1", "-1")], 0),
  Q("ماذا تعيد len([4, 5, 6]) ؟", "Que renvoie len([4, 5, 6]) ?", [("3", "3"), ("6", "6"), ("4", "4")], 0),
  Q("أي شرط يتحقق عندما x أكبر من 10 ؟", "Quelle condition est vraie quand x est supérieur à 10 ?", [("x > 10", "x > 10"), ("x == 10", "x == 10"), ("x < 10", "x < 10")], 0)],
 "s2-si": [
  Q("أي صيغة تجمع الخلايا من A1 إلى A5 ؟", "Quelle formule additionne les cellules de A1 à A5 ?", [("=SOMME(A1:A5)", "=SOMME(A1:A5)"), ("=A1+A5", "=A1+A5"), ("=A1:A5", "=A1:A5")], 0),
  Q("ما المرجع النسبي؟", "Que fait une référence relative ?", [("تتغير عند نسخ الصيغة", "Elle change quand on recopie la formule"), ("تبقى ثابتة", "Elle reste fixe"), ("تحذف الخلية", "Elle efface la cellule")], 0),
  Q("أي رسم يناسب تطور قيمة عبر الزمن؟", "Quel graphique convient pour une évolution dans le temps ?", [("المنحنى", "La courbe"), ("الدائري", "Le secteur"), ("لا شيء", "Aucun")], 0),
  Q("ما فائدة الفرز في جدول؟", "À quoi sert le tri dans un tableau ?", [("ترتيب الأسطر حسب عمود", "Ordonner les lignes selon une colonne"), ("حذف الجدول", "Supprimer le tableau"), ("تلوين الخلايا فقط", "Seulement colorer les cellules")], 0)],
 "s2-sr": [
  Q("أي جهاز يربط عدة حواسيب في شبكة محلية؟", "Quel appareil relie plusieurs ordinateurs dans un réseau local ?", [("المبدّل (Switch)", "Le commutateur (switch)"), ("الطابعة", "L'imprimante"), ("الميكروفون", "Le microphone")], 0),
  Q("ما عنوان IP؟", "Qu'est-ce qu'une adresse IP ?", [("معرّف جهاز في الشبكة", "L'identifiant d'un appareil sur le réseau"), ("اسم مستخدم", "Un nom d'utilisateur"), ("كلمة سر", "Un mot de passe")], 0),
  Q("ما البروتوكول المستعمل لإرسال البريد؟", "Quel protocole sert à envoyer du courrier ?", [("SMTP", "SMTP"), ("HTTP", "HTTP"), ("DNS", "DNS")], 0),
  Q("ما المتصفح؟", "Qu'est-ce qu'un navigateur ?", [("برنامج لعرض صفحات الويب", "Un logiciel pour afficher les pages web"), ("محرك بحث", "Un moteur de recherche"), ("شبكة", "Un réseau")], 0)],
 "s3-sa": [
  Q("ما نتيجة [x*2 for x in range(3)] ؟", "Quel est le résultat de [x*2 for x in range(3)] ?", [("[0, 2, 4]", "[0, 2, 4]"), ("[2, 4, 6]", "[2, 4, 6]"), ("[0, 1, 2]", "[0, 1, 2]")], 0),
  Q("ما تعقيد البحث الخطي في قائمة من n عنصرا؟", "Quelle est la complexité d'une recherche linéaire dans n éléments ?", [("خطي O(n)", "linéaire O(n)"), ("ثابت O(1)", "constante O(1)"), ("O(n²)", "O(n²)")], 0),
  Q("ما فائدة تقسيم برنامج إلى دوال؟", "Pourquoi découper un programme en fonctions ?", [("لتسهيل القراءة والاختبار وإعادة الاستعمال", "Pour faciliter la lecture, les tests et la réutilisation"), ("لإبطائه", "Pour le ralentir"), ("لا فائدة", "Aucun intérêt")], 0),
  Q("ما نوع الخطأ عند كتابة 'print(' بلا إغلاق؟", "Quel type d'erreur pour « print( » sans fermeture ?", [("خطأ في الصياغة", "Une erreur de syntaxe"), ("خطأ في المنطق", "Une erreur de logique"), ("لا خطأ", "Aucune erreur")], 0)],
 "s3-si": [
  Q("ما المفتاح الأولي في جدول؟", "Qu'est-ce qu'une clé primaire ?", [("حقل يحدد كل سطر بصفة فريدة", "Un champ qui identifie chaque ligne de façon unique"), ("كلمة سر", "Un mot de passe"), ("عمود مخفي", "Une colonne cachée")], 0),
  Q("أي أمر SQL يختار أعمدة من جدول؟", "Quelle commande SQL sélectionne des colonnes ?", [("SELECT", "SELECT"), ("DELETE", "DELETE"), ("DROP", "DROP")], 0),
  Q("ما فائدة الشرط WHERE؟", "À quoi sert la clause WHERE ?", [("تصفية الأسطر", "Filtrer les lignes"), ("ترتيب الأعمدة", "Ordonner les colonnes"), ("حذف الجدول", "Supprimer la table")], 0),
  Q("ما العلاقة بين جدولين؟", "Comment relie-t-on deux tables ?", [("بمفتاح أجنبي", "Par une clé étrangère"), ("باللون", "Par la couleur"), ("بالحجم", "Par la taille")], 0)],
 "s3-sr": [
  Q("ما التشفير؟", "Qu'est-ce que le chiffrement ?", [("تحويل المعطيات لجعلها غير مقروءة دون مفتاح", "Transformer des données pour les rendre illisibles sans clé"), ("ضغط الملف", "Compresser un fichier"), ("حذف الملف", "Supprimer un fichier")], 0),
  Q("ما الفرق الرئيسي بين التشفير المتماثل وغير المتماثل؟", "Quelle différence entre chiffrement symétrique et asymétrique ?", [("مفتاح واحد مقابل مفتاحين", "Une seule clé contre deux clés"), ("السرعة فقط", "Seulement la vitesse"), ("لا فرق", "Aucune")], 0),
  Q("ما جدار الحماية؟", "Qu'est-ce qu'un pare-feu ?", [("يراقب حركة الشبكة ويصفيها", "Il surveille et filtre le trafic réseau"), ("يسرع الحاسوب", "Il accélère l'ordinateur"), ("محرك بحث", "Un moteur de recherche")], 0),
  Q("ما الاحتيال بانتحال الصفة (Phishing)؟", "Qu'est-ce que l'hameçonnage ?", [("خداع لسرقة بيانات المستخدم", "Une tromperie pour voler les données de l'utilisateur"), ("تحديث للنظام", "Une mise à jour du système"), ("نوع حاسوب", "Un type d'ordinateur")], 0)],
 "s4-sa": [
  Q("ما تعقيد الفرز بالفقاعات (Tri à bulles) في الحالة العامة؟", "Quelle est la complexité du tri à bulles dans le cas général ?", [("O(n²)", "O(n²)"), ("O(n)", "O(n)"), ("O(1)", "O(1)")], 0),
  Q("ما شرط التوقف في دالة عودية؟", "Que faut-il toujours prévoir dans une fonction récursive ?", [("حالة توقف", "Un cas d'arrêt"), ("متغيرا عاما", "Une variable globale"), ("حلقة for", "Une boucle for")], 0),
  Q("ما البحث الثنائي يتطلب؟", "Que demande la recherche dichotomique ?", [("قائمة مرتبة", "Une liste triée"), ("قائمة عشوائية", "Une liste quelconque"), ("نصا فقط", "Seulement du texte")], 0),
  Q("ما فائدة اختبار البرنامج بقيم حدّية؟", "Pourquoi tester un programme avec des valeurs limites ?", [("لاكتشاف أخطاء الحالات القصوى", "Pour détecter les erreurs aux cas extrêmes"), ("لتجميله", "Pour l'embellir"), ("لا فائدة", "Aucun intérêt")], 0)],
 "s4-si": [
  Q("ماذا يفعل الأمر INSERT INTO؟", "Que fait la commande INSERT INTO ?", [("يضيف سطرا إلى جدول", "Ajoute une ligne à une table"), ("يحذف جدولا", "Supprime une table"), ("يغير اسم عمود", "Renomme une colonne")], 0),
  Q("ماذا تفعل JOIN؟", "Que fait une jointure (JOIN) ?", [("تجمع معطيات جدولين مرتبطين", "Combine les données de deux tables liées"), ("تحذف المكرر", "Supprime les doublons"), ("تنسخ قاعدة", "Copie une base")], 0),
  Q("ما فائدة التطبيع (Normalisation)؟", "À quoi sert la normalisation ?", [("تقليل التكرار وتجنب التناقض", "Réduire la redondance et éviter les incohérences"), ("تسريع الشاشة", "Accélérer l'écran"), ("تلوين الجداول", "Colorier les tables")], 0),
  Q("ما نتيجة SELECT COUNT(*) FROM eleves ؟", "Que renvoie SELECT COUNT(*) FROM eleves ?", [("عدد الأسطر", "Le nombre de lignes"), ("اسم الجدول", "Le nom de la table"), ("أول سطر", "La première ligne")], 0)],
 "s4-sr": [
  Q("ما دور بروتوكول TCP؟", "Quel est le rôle du protocole TCP ?", [("نقل موثوق للمعطيات", "Transporter les données de façon fiable"), ("تلوين الصفحات", "Colorier les pages"), ("حماية الجهاز", "Protéger l'appareil")], 0),
  Q("ما HTML؟", "Qu'est-ce que le HTML ?", [("لغة وصف بنية صفحات الويب", "Un langage de description de la structure des pages web"), ("نظام تشغيل", "Un système d'exploitation"), ("قاعدة بيانات", "Une base de données")], 0),
  Q("ما التوقيع الرقمي؟", "Qu'est-ce qu'une signature numérique ?", [("إثبات هوية المرسل وسلامة الوثيقة", "Preuve de l'identité de l'émetteur et de l'intégrité du document"), ("صورة التوقيع", "L'image d'une signature"), ("كلمة سر", "Un mot de passe")], 0),
  Q("ما الخادم (Serveur)؟", "Qu'est-ce qu'un serveur ?", [("حاسوب يقدم خدمات لحواسيب أخرى", "Un ordinateur qui fournit des services à d'autres"), ("طابعة", "Une imprimante"), ("شاشة", "Un écran")], 0)],
}
