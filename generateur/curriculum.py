"""Programme d'informatique 7e / 8e / 9e année (Aide pédagogique – Informatique, Ministère de l'Éducation, Tunisie, septembre 2025).
Quatre domaines d'apprentissage par année. Texte transcrit à partir de photographies : à relire avec le document officiel.
Chaque élément : (français, arabe). Usage : python3 generateur/curriculum.py  -> generateur/axes.json"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
import programme as prg

AX = {  # domaines (menu)
 "env": ("Environnement informatique de travail", "بيئة العمل المعلوماتية"),
 "net": ("Technologies : Internet", "التكنولوجيات: الإنترنت"),
 "create": ("Création de contenus numériques", "إنتاج المحتويات الرقمية"),
 "prog": ("Pensée logique et programmation", "الفكر المنطقي والبرمجة"),
}
YEARS = {7: ("7e année", "السنة السابعة", "7e", "٧"), 8: ("8e année", "السنة الثامنة", "8e", "٨"), 9: ("9e année", "السنة التاسعة", "9e", "٩"),
         "s1": ("1ère année secondaire", "السنة الأولى ثانوي", "1S", "١ث"), "s2": ("2e année secondaire", "السنة الثانية ثانوي", "2S", "٢ث"),
         "s3": ("3e année secondaire", "السنة الثالثة ثانوي", "3S", "٣ث"), "s4": ("4e année secondaire", "السنة الرابعة ثانوي", "4S", "٤ث")}

def part(t, items): return dict(t_fr=t[0], t_ar=t[1], i_fr=[x[0] for x in items], i_ar=[x[1] for x in items])
def axis(comp, parts, know, cad, note=None):
    return dict(comp_fr=comp[0], comp_ar=comp[1], parts=[part(t, i) for t, i in parts], know_fr=[k[0] for k in know], know_ar=[k[1] for k in know],
                cad_fr=[c[0] for c in cad], cad_ar=[c[1] for c in cad], note=note)

A = {}
# ----------------------------------------------------------------------------- 7e
A[(7, "env")] = axis(
 ("Exploiter un environnement informatique de travail et gérer ses ressources de manière organisée.", "استغلال بيئة عمل معلوماتية وتسيير مواردها بصفة منظمة."),
 [(("Identifier les composants d'un environnement informatique", "تحديد مكوّنات بيئة معلوماتية"), [("Distinguer les périphériques d'entrée des périphériques de sortie", "التمييز بين وحدات الإدخال ووحدات الإخراج"), ("Identifier les principaux composants internes d'un ordinateur", "تحديد أهم المكوّنات الداخلية للحاسوب"), ("Identifier les supports de stockage et leur capacité", "تحديد وسائط التخزين وسعتها"), ("Associer chaque composant à sa fonction", "ربط كل مكوّن بوظيفته")]),
  (("Exploiter un système d'exploitation", "استغلال نظام تشغيل"), [("Reconnaître un système d'exploitation pour ordinateur et mobile", "التعرف على نظام تشغيل للحاسوب وللهاتف"), ("Gérer et organiser les fichiers et les dossiers sous forme d'arborescence", "تسيير الملفات والمجلدات وتنظيمها في شكل شجرة")])],
 [("Périphériques d'entrée (clavier, souris, micro, scanner) et de sortie (écran, imprimante, haut-parleur)", "وحدات الإدخال (لوحة المفاتيح، الفأرة، الميكروفون، الماسح) ووحدات الإخراج (الشاشة، الطابعة، مكبّر الصوت)"), ("Composants internes : processeur, mémoire RAM, carte graphique", "المكوّنات الداخلية: المعالج، الذاكرة الحية، بطاقة الرسوم"), ("Stockage : supports (disque dur, clé USB, carte mémoire) et unités de capacité (octet, Ko, Mo, Go, To)", "التخزين: الوسائط (القرص الصلب، المفتاح الذاكري، بطاقة الذاكرة) ووحدات السعة (بايت، Ko، Mo، Go، To)"), ("Système et fichiers : système d'exploitation, fichier, dossier, arborescence, nom et extension d'un fichier", "النظام والملفات: نظام التشغيل، الملف، المجلد، الشجرة، اسم الملف وامتداده")],
 [("Se limiter aux unités octet, Ko, Mo, Go et To, sans effectuer de conversions", "الاقتصار على الوحدات بايت وKo وMo وGo وTo دون إجراء تحويلات"), ("Ne pas approfondir les caractéristiques techniques des composants à ce niveau", "عدم التعمق في الخصائص التقنية للمكوّنات في هذا المستوى"), ("Favoriser des activités sollicitant la réflexion et la compréhension", "تفضيل الأنشطة التي تستدعي التفكير والفهم"), ("Présenter le périphérique multifonction comme un cas particulier", "تقديم الوحدة المتعددة الوظائف كحالة خاصة")])
A[(7, "net")] = axis(
 ("Exploiter Internet pour rechercher, télécharger, réutiliser et partager des informations de manière responsable.", "استغلال الإنترنت للبحث عن المعلومات وتحميلها وإعادة استعمالها ومشاركتها بصفة مسؤولة."),
 [(("Rechercher des informations", "البحث عن المعلومات"), [("Identifier les mots-clés pertinents et formuler une requête à l'aide d'un moteur de recherche ou d'un outil d'IA", "تحديد الكلمات المفاتيح المناسبة وصياغة طلب بحث بمحرك بحث أو بأداة ذكاء اصطناعي"), ("Affiner une requête", "تدقيق طلب البحث"), ("Comparer les résultats de recherche selon leur source, leur date et leur fiabilité", "مقارنة نتائج البحث حسب مصدرها وتاريخها ومدى موثوقيتها")]),
  (("Télécharger, réutiliser et partager une ressource", "تحميل مورد وإعادة استعماله ومشاركته"), [("Télécharger et réutiliser une ressource dans le respect de l'éthique et des droits d'auteur", "تحميل مورد وإعادة استعماله مع احترام الأخلاقيات وحقوق المؤلف"), ("Partager un contenu numérique de manière responsable", "مشاركة محتوى رقمي بصفة مسؤولة")])],
 [("Recherche : moteur de recherche, mots-clés, requête, adresse URL, source, date, fiabilité", "البحث: محرك البحث، الكلمات المفاتيح، طلب البحث، عنوان URL، المصدر، التاريخ، الموثوقية"), ("Téléchargement et partage : droits d'auteur, licence, citation, espace de partage, document partagé", "التحميل والمشاركة: حقوق المؤلف، الرخصة، الاقتباس، فضاء المشاركة، الوثيقة المشتركة")],
 [("Développer la recherche d'information tout au long des apprentissages", "تنمية البحث عن المعلومة طيلة التعلّمات"), ("Limiter l'utilisation de l'IA générative à la formulation d'instructions simples et contextualisées, sans aborder les techniques avancées", "حصر استعمال الذكاء الاصطناعي التوليدي في صياغة تعليمات بسيطة وملائمة للسياق دون التطرق إلى التقنيات المتقدمة"), ("Vérifier systématiquement la fiabilité des sources et respecter les droits d'auteur", "التثبت دائما من موثوقية المصادر واحترام حقوق المؤلف")])
A[(7, "create")] = axis(
 ("Produire une création numérique associant texte et image pour communiquer une idée.", "إنتاج عمل رقمي يجمع بين النص والصورة لتبليغ فكرة."),
 [(("Réaliser une production", "إنجاز إنتاج"), [("Produire une création numérique intégrant du texte et des images", "إنتاج عمل رقمي يدمج نصوصا وصورا"), ("Exporter la production dans un format adapté", "تصدير الإنتاج في صيغة ملائمة")]),
  (("Enrichir et améliorer une production", "إثراء إنتاج وتحسينه"), [("Utiliser un outil d'IA pour enrichir une production réalisée", "استعمال أداة ذكاء اصطناعي لإثراء إنتاج منجز"), ("Comparer la production avant et après enrichissement et justifier ce qui a été retenu", "مقارنة الإنتاج قبل الإثراء وبعده وتبرير ما تم الاحتفاظ به")])],
 [("Texte, image, format d'enregistrement, format d'exportation", "النص، الصورة، صيغة الحفظ، صيغة التصدير")],
 [("Privilégier l'intégration d'objets cohérents, lisibles et pertinents au regard de l'objectif de la production", "تفضيل إدماج عناصر متناسقة ومقروءة وملائمة لهدف الإنتاج"), ("Utiliser l'IA comme aide à l'amélioration et non comme substitut au travail de l'apprenant", "استعمال الذكاء الاصطناعي كمساعد على التحسين وليس بديلا عن عمل المتعلم"), ("N'utiliser que des images libres de droits ou produites par l'apprenant", "عدم استعمال إلا الصور الحرة الحقوق أو التي ينتجها المتعلم")])
# ----------------------------------------------------------------------------- 8e
A[(8, "env")] = axis(
 ("Identifier les risques qui menacent un environnement informatique et adopter des comportements de protection.", "تحديد المخاطر التي تهدد بيئة معلوماتية واعتماد سلوكيات للحماية."),
 [(("Identifier les risques qui menacent un environnement informatique", "تحديد المخاطر التي تهدد بيئة معلوماتية"), [("Reconnaître les principaux logiciels malveillants", "التعرف على أهم البرمجيات الخبيثة"), ("Reconnaître les risques liés aux communautés virtuelles", "التعرف على المخاطر المرتبطة بالمجتمعات الافتراضية"), ("Repérer des indicateurs d'une menace de sécurité", "رصد مؤشرات تهديد أمني")]),
  (("Adopter des comportements de protection", "اعتماد سلوكيات للحماية"), [("Utiliser des mots de passe robustes pour protéger ses données personnelles", "استعمال كلمات سر قوية لحماية المعطيات الشخصية"), ("Utiliser des outils de sécurité informatique pour protéger son environnement informatique", "استعمال أدوات الأمن المعلوماتي لحماية بيئته المعلوماتية"), ("Appliquer des mesures de confidentialité pour protéger des données en ligne", "تطبيق إجراءات السرية لحماية المعطيات على الإنترنت")])],
 [("Menaces : logiciel malveillant (virus, ver, cheval de Troie), hameçonnage, vol d'identité, cyberharcèlement ; menace de sécurité", "التهديدات: البرمجية الخبيثة (فيروس، دودة، حصان طروادة)، التصيّد، انتحال الهوية، التنمّر الإلكتروني؛ التهديد الأمني"), ("Protection : antivirus, pare-feu, confidentialité, mot de passe, fermeture de session", "الحماية: مضاد الفيروسات، جدار الحماية، السرية، كلمة السر، غلق الجلسة")],
 [("Traiter principalement les indicateurs visibles (ralentissement, suppression de fichiers, messages suspects, demandes d'informations)", "التركيز على المؤشرات الظاهرة (البطء، حذف الملفات، الرسائل المشبوهة، طلب معلومات)"), ("Sensibiliser aux risques liés à la divulgation des données personnelles", "التحسيس بمخاطر الكشف عن المعطيات الشخصية"), ("Ne jamais demander à un apprenant de saisir un mot de passe personnel réel dans une activité", "عدم مطالبة المتعلم بإدخال كلمة سر شخصية حقيقية في أي نشاط"), ("Aucune manipulation de logiciel malveillant réel, même à titre de démonstration", "عدم التعامل مع برمجية خبيثة حقيقية ولو للعرض"), ("Traiter le cyberharcèlement à partir de cas fictifs ; ne jamais exposer une situation vécue par un apprenant de la classe", "معالجة التنمّر الإلكتروني انطلاقا من حالات خيالية دون التعرض لوضعية يعيشها متعلم من القسم")])
A[(8, "net")] = axis(
 ("Communiquer, collaborer et préserver son identité numérique dans les espaces en ligne.", "التواصل والتعاون والحفاظ على هويته الرقمية في الفضاءات على الإنترنت."),
 [(("Communiquer et collaborer en ligne", "التواصل والتعاون عبر الإنترنت"), [("Exploiter un outil de communication en ligne", "استغلال أداة تواصل عبر الإنترنت"), ("Respecter les règles de la nétiquette", "احترام قواعد السلوك على الشبكة"), ("Utiliser un dispositif d'écriture collaborative pour coproduire un contenu", "استعمال أداة كتابة تشاركية لإنتاج محتوى مشترك")]),
  (("Préserver son identité numérique", "الحفاظ على الهوية الرقمية"), [("Préserver son identité et sa réputation numériques", "المحافظة على هويته وسمعته الرقميتين")])],
 [("Communication en ligne : nétiquette, écriture collaborative", "التواصل عبر الإنترنت: قواعد السلوك على الشبكة، الكتابة التشاركية"), ("Identité numérique : données personnelles, identité numérique, réputation numérique", "الهوية الرقمية: المعطيات الشخصية، الهوية الرقمية، السمعة الرقمية")],
 [("Insister sur le respect des personnes, de la vie privée et des droits d'auteur", "التأكيد على احترام الأشخاص والحياة الخاصة وحقوق المؤلف"), ("Ne pas demander aux apprenants de publier des données personnelles réelles", "عدم مطالبة المتعلمين بنشر معطيات شخصية حقيقية")])
A[(8, "create")] = axis(
 ("Exploiter un outil de production multimédia pour communiquer des idées de manière visuelle et sonore.", "استغلال أداة إنتاج متعددة الوسائط لتبليغ الأفكار بصريا وسمعيا."),
 [(("Produire et monter l'audio", "إنتاج الصوت ومونتاجه"), [("Créer et modifier un fichier audio", "إنشاء ملف صوتي وتعديله"), ("Appliquer des effets et des fondus adaptés et mixer des pistes", "تطبيق مؤثرات وتدرّجات مناسبة ومزج المسارات")]),
  (("Produire et monter la vidéo", "إنتاج الفيديو ومونتاجه"), [("Concevoir et modifier une courte vidéo", "تصميم فيديو قصير وتعديله"), ("Ajouter des titres, un générique, des transitions et une bande sonore", "إضافة عناوين وشارة وانتقالات وشريط صوتي")]),
  (("Enrichir et diffuser", "الإثراء والنشر"), [("Utiliser l'IA pour enrichir une production numérique", "استعمال الذكاء الاصطناعي لإثراء إنتاج رقمي"), ("Exporter la production dans un format adapté à sa diffusion", "تصدير الإنتاج في صيغة ملائمة لنشره")])],
 [("Audio : effet, fondu, mixage, piste, volume", "الصوت: مؤثر، تدرّج، مزج، مسار، مستوى الصوت"), ("Vidéo : titre, générique, transition, bande sonore, importation, découpage, assemblage", "الفيديو: عنوان، شارة، انتقال، شريط صوتي، استيراد، قصّ، تجميع"), ("Diffusion : format d'exportation", "النشر: صيغة التصدير")],
 [("Privilégier la pertinence du mixage plutôt que la multiplication des effets", "تفضيل ملاءمة المزج على كثرة المؤثرات"), ("Pour l'audio : enregistrement, découpage, réglage du volume et musique de fond", "في الصوت: التسجيل والقصّ وضبط مستوى الصوت وموسيقى الخلفية"), ("Pour la vidéo : importation, découpage, assemblage, titres, son et exportation", "في الفيديو: الاستيراد والقصّ والتجميع والعناوين والصوت والتصدير"), ("L'IA ne doit pas générer intégralement le contenu à la place de l'apprenant", "ألا يولّد الذكاء الاصطناعي المحتوى كليا بدل المتعلم"), ("Limiter la production à deux minutes", "حصر الإنتاج في دقيقتين"), ("N'utiliser que des ressources sonores et visuelles libres de droits ou produites par la classe", "عدم استعمال إلا موارد سمعية وبصرية حرة الحقوق أو من إنتاج القسم")])
# ----------------------------------------------------------------------------- 9e
A[(9, "env")] = axis(
 ("Comprendre le fonctionnement d'un objet communicant et le commander.", "فهم طريقة عمل شيء متواصل والتحكم فيه."),
 [(("Identifier un objet communicant et ses constituants", "تحديد شيء متواصل ومكوّناته"), [("Distinguer un objet communicant d'un objet connecté", "التمييز بين الشيء المتواصل والشيء المتصل"), ("Préciser le rôle des capteurs, des actionneurs et des interfaces de communication", "تحديد دور الملتقطات والمحرّكات وواجهات الاتصال"), ("Reconnaître les principales technologies de communication", "التعرف على أهم تقنيات الاتصال"), ("Identifier des domaines d'application des objets communicants", "تحديد مجالات استعمال الأشياء المتواصلة")]),
  (("Commander un objet communicant", "التحكم في شيء متواصل"), [("Connecter et commander un objet communicant à partir d'une application mobile", "ربط شيء متواصل والتحكم فيه انطلاقا من تطبيقة هاتف")])],
 [("Objets : objet communicant, objet connecté ; capteur, actionneur", "الأشياء: شيء متواصل، شيء متصل؛ ملتقط، محرّك"), ("Communication : interface de communication, ports, broches, module de communication", "الاتصال: واجهة الاتصال، المنافذ، الأطراف، وحدة الاتصال"), ("Technologies de communication : Wi-Fi, Bluetooth, radio", "تقنيات الاتصال: Wi-Fi، البلوتوث، الراديو")],
 [("Privilégier des situations d'apprentissage simples, observables et adaptées aux apprenants", "تفضيل وضعيات تعلّم بسيطة وقابلة للملاحظة وملائمة للمتعلمين"), ("En l'absence de matériel, exploiter des applications ou des simulations adaptées", "عند غياب العتاد، استغلال تطبيقات أو محاكاة ملائمة"), ("Ne pas confondre l'interface de communication (composant matériel) avec la technologie de communication (procédé employé)", "عدم الخلط بين واجهة الاتصال (مكوّن مادي) وتقنية الاتصال (الأسلوب المستعمل)")])
A[(9, "net")] = axis(
 ("Collaborer en ligne et gérer de manière responsable les traces liées à ses usages numériques.", "التعاون عبر الإنترنت وتسيير الآثار المرتبطة باستعمالاته الرقمية بصفة مسؤولة."),
 [(("Collaborer en ligne", "التعاون عبر الإنترنت"), [("Utiliser un dispositif d'écriture collaborative pour coproduire un contenu", "استعمال أداة كتابة تشاركية لإنتاج محتوى مشترك"), ("Adopter un comportement respectueux et responsable dans un espace collaboratif", "اعتماد سلوك محترم ومسؤول في فضاء تشاركي")]),
  (("Gérer ses traces numériques", "تسيير آثاره الرقمية"), [("Comprendre les traces générées au cours des interactions numériques", "فهم الآثار الناتجة عن التفاعلات الرقمية"), ("Distinguer une trace volontaire d'une trace involontaire", "التمييز بين أثر إرادي وأثر غير إرادي"), ("Appliquer des mesures simples pour limiter la collecte et la diffusion de ses données et traces numériques", "تطبيق إجراءات بسيطة للحدّ من جمع معطياته وآثاره الرقمية ونشرها")])],
 [("Collaboration en ligne : écriture collaborative, droits des contributeurs", "التعاون عبر الإنترنت: الكتابة التشاركية، حقوق المساهمين"), ("Traces numériques : trace volontaire, trace involontaire, identité numérique, historique de navigation, cookie", "الآثار الرقمية: أثر إرادي، أثر غير إرادي، هوية رقمية، سجل التصفح، ملف تعريف الارتباط")],
 [("Privilégier des plateformes sécurisées et adaptées au contexte scolaire", "تفضيل منصات آمنة وملائمة للسياق المدرسي"), ("Ne pas publier de données personnelles réelles", "عدم نشر معطيات شخصية حقيقية"), ("Mettre l'accent sur le respect de soi, des autres et des règles de communication", "التركيز على احترام الذات والآخرين وقواعد التواصل"), ("Ne pas observer ni exploiter les traces réelles d'un apprenant identifiable", "عدم ملاحظة أو استغلال الآثار الحقيقية لمتعلم يمكن التعرف عليه")])
A[(9, "create")] = dict(comp_fr="", comp_ar="", parts=[], know_fr=[], know_ar=[], cad_fr=[], cad_ar=[], note=("Cette page du programme n'apparaît pas dans les photographies reçues.", "صفحة هذا المحور من المنهاج غير موجودة في الصور المرسلة."))
A[(9, "prog")] = axis(
 ("Résoudre des problèmes en programmant des objets et en développant des applications mobiles.", "حل المشكلات ببرمجة الأشياء وتطوير تطبيقات الهاتف."),
 [(("Analyser le problème", "تحليل المشكلة"), [("Analyser un problème en identifiant ses entrées, ses sorties et les étapes de traitement", "تحليل مشكلة بتحديد مدخلاتها ومخرجاتها ومراحل المعالجة")]),
  (("Programmer un objet", "برمجة شيء"), [("Programmer un objet en exploitant les données des capteurs et en contrôlant les actionneurs", "برمجة شيء باستغلال معطيات الملتقطات والتحكم في المحرّكات"), ("Tester et optimiser une solution", "اختبار حل وتحسينه")]),
  (("Développer une application mobile", "تطوير تطبيقة هاتف"), [("Concevoir l'interface utilisateur d'une application mobile", "تصميم واجهة المستعمل لتطبيقة هاتف"), ("Coder, tester et générer une application mobile simple", "برمجة تطبيقة هاتف بسيطة واختبارها وتوليدها")])],
 [("Objet programmable : actionneur, capteur, carte à microcontrôleur (type BBC micro:bit)", "الشيء القابل للبرمجة: محرّك، ملتقط، بطاقة بمتحكم دقيق (مثل BBC micro:bit)"), ("Objet connecté : interface de connexion, communication Bluetooth bidirectionnelle", "الشيء المتصل: واجهة الربط، اتصال بلوتوث ثنائي الاتجاه"), ("Application mobile : composants d'interface (bouton, zone de texte, image, étiquette, liste), événement associé à un composant, génération et installation de l'application", "تطبيقة الهاتف: مكوّنات الواجهة (زر، خانة نص، صورة، عنوان، قائمة)، الحدث المرتبط بمكوّن، توليد التطبيقة وتثبيتها")],
 [("Prévoir uniquement des applications mobiles basiques", "الاقتصار على تطبيقات هاتف بسيطة"), ("Concevoir une interface simple, lisible et facile à programmer", "تصميم واجهة بسيطة ومقروءة وسهلة البرمجة"), ("Ne pas confier à l'apprenant la conception complexe du montage électronique", "عدم تكليف المتعلم بتصميم التركيب الإلكتروني المعقد"), ("Utiliser un environnement de développement par blocs tel que App Inventor ou équivalent", "استعمال بيئة تطوير بالكتل مثل App Inventor أو ما يعادلها"), ("Limiter l'interface à cinq composants au maximum", "حصر الواجهة في خمسة مكوّنات على الأكثر")])
# programmation 7e / 8e : reprise des données de programme.py
for n in (7, 8):
    L = prg.LEVELS[n]
    A[(n, "prog")] = dict(comp_fr=L["comp_fr"], comp_ar=L["comp_ar"], parts=[dict(t_fr=b, t_ar=a, i_fr=d, i_ar=c) for a, b, c, d in L["parts"]], know_fr=L["know_fr"], know_ar=L["know_ar"], cad_fr=L["cad_fr"], cad_ar=L["cad_ar"], note=None)

# ---------------------------------------------------------------------------------------------
# Curriculum officiel (PDF « Curriculum d'informatique – 7ème, 8ème et 9ème année de base ») : domaines et compétences
def L(*pairs): return [(f, a) for f, a in pairs]
CF = ("Communication et collaboration", "التواصل والتعاون"); CI = ("Créativité et innovation", "الإبداع والابتكار"); RP = ("Résolution de problèmes", "حل المشكلات")
MEDIA = ("Acquérir une éducation aux médias et à l'information.", "اكتساب تربية على وسائل الإعلام والمعلومات.")
PDF = {
 (7, "env"): dict(comps=L(("Se familiariser avec l'environnement informatique de travail.", "التآلف مع بيئة العمل المعلوماتية."), ("Exploiter à bon escient l'environnement informatique de travail.", "استغلال بيئة العمل المعلوماتية استغلالا حسنا.")), life=None),
 (7, "net"): dict(comps=L(("Exploiter des outils, des services de communication et des technologies Internet.", "استغلال أدوات وخدمات التواصل وتقنيات الإنترنت."), MEDIA, ("Tenir compte des enjeux civiques de l'usage de l'informatique et de l'Internet.", "مراعاة الرهانات المدنية لاستعمال الإعلامية والإنترنت."), ("Adopter une attitude avertie face aux résultats obtenus suite à une recherche.", "اعتماد موقف واعٍ إزاء النتائج المتحصل عليها بعد البحث.")), life=CF),
 (7, "create"): dict(comps=L(("Produire et partager en ligne des créations numériques en respectant l'e-réputation.", "إنتاج أعمال رقمية ومشاركتها عبر الإنترنت مع احترام السمعة الرقمية.")), life=CI),
 (7, "prog"): dict(comps=L(("Développer une stratégie logique de résolution de problème.", "تطوير استراتيجية منطقية لحل مشكلة."), ("Découvrir des notions de base de la programmation.", "اكتشاف مفاهيم أساسية في البرمجة."), ("Résoudre des problèmes faisant appel à la logique en manipulant des objets.", "حل مشكلات تستدعي المنطق بمعالجة أشياء.")), life=RP),
 (8, "env"): dict(comps=L(("Identifier les risques qui menacent l'environnement informatique de travail.", "تحديد المخاطر التي تهدد بيئة العمل المعلوماتية."), ("Acquérir des comportements de vigilance numérique.", "اكتساب سلوكيات اليقظة الرقمية.")), life=None),
 (8, "net"): dict(comps=L(("S'approprier des outils de l'e-communication et de l'e-partage.", "التمكن من أدوات التواصل والمشاركة الإلكترونيين."), ("Identifier les risques relatifs aux communautés virtuelles.", "تحديد المخاطر المتعلقة بالمجتمعات الافتراضية."), ("Adopter une pratique éclairée sur Internet.", "اعتماد ممارسة واعية على الإنترنت.")), life=CF),
 (8, "create"): dict(comps=L(("S'exprimer par le biais des médias numériques et technologiques.", "التعبير بواسطة الوسائط الرقمية والتكنولوجية."), ("Exploiter des outils de création de contenus numériques.", "استغلال أدوات إنشاء المحتويات الرقمية."), ("Modifier et combiner des ressources existantes pour créer de nouveaux contenus.", "تعديل موارد موجودة ودمجها لإنشاء محتويات جديدة."), MEDIA), life=CI),
 (8, "prog"): dict(comps=L(("Développer une stratégie de raisonnement logique pour résoudre un problème.", "تطوير استراتيجية تفكير منطقي لحل مشكلة."), ("Produire un programme à l'aide d'un langage de programmation.", "إنتاج برنامج باستعمال لغة برمجة.")), life=RP),
 (9, "prog"): dict(title=("Initiation à la logique et à la programmation", "مدخل إلى المنطق والبرمجة"), champ=("Programmation visuelle et robotique", "البرمجة البصرية والروبوتية"),
   comps=L(("Résoudre des problèmes en développant une stratégie de raisonnement logique.", "حل مشكلات بتطوير استراتيجية تفكير منطقي."), ("Développer l'esprit critique et créatif.", "تنمية الحس النقدي والإبداعي."), ("S'approprier des notions fondamentales de la programmation robotique.", "التمكن من مفاهيم أساسية في البرمجة الروبوتية."), ("Communiquer à travers des langages de programmation et des objets contrôlés.", "التواصل بواسطة لغات البرمجة والأشياء المتحكَّم فيها.")), life=None,
   prat=L(("Faire un choix réfléchi sur l'environnement de travail.", "اختيار بيئة العمل عن روية."), ("Appliquer les notions fondamentales de la programmation.", "تطبيق المفاهيم الأساسية للبرمجة."), ("Exploiter un environnement de travail.", "استغلال بيئة عمل."), ("Commander des objets via un programme.", "التحكم في أشياء بواسطة برنامج."), ("Argumenter les choix des solutions.", "تبرير اختيارات الحلول.")),
   pist=L(("Valoriser les initiatives créatives et innovantes.", "تثمين المبادرات الإبداعية والمبتكرة."), ("Avantager les débats tout au long de la réalisation du projet.", "تفضيل النقاشات طيلة إنجاز المشروع."), ("Inciter les apprenants à la collaboration et à la publication de leurs projets.", "تشجيع المتعلمين على التعاون ونشر مشاريعهم."), ("Choisir un espace adéquat de partage de données.", "اختيار فضاء مناسب لمشاركة المعطيات."))),
 (9, "prod"): dict(title=("Production numérique", "الإنتاج الرقمي"), champ=("Tableur", "الجدول الحاسوبي"),
   comps=L(("Rationnaliser l'utilisation d'un tableur pour l'aide à la prise de décision.", "ترشيد استعمال الجدول الحاسوبي للمساعدة على اتخاذ القرار."), ("Développer l'esprit créatif et critique lors de la production numérique.", "تنمية الحس الإبداعي والنقدي عند الإنتاج الرقمي.")), life=None,
   prat=L(("Faire un choix réfléchi pour répondre à un besoin donné.", "القيام باختيار مدروس لتلبية حاجة معينة."), ("Produire un document en utilisant convenablement un tableur.", "إنتاج وثيقة باستعمال الجدول الحاسوبي بشكل ملائم."), ("Analyser les données d'une feuille de calcul.", "تحليل معطيات ورقة حساب."), ("Faire un choix réfléchi lors de l'intégration des formules de calcul et des fonctions de base.", "القيام باختيار مدروس عند إدماج صيغ الحساب والدوال الأساسية."), ("Créer et analyser des graphiques.", "إنشاء رسوم بيانية وتحليلها."), ("Argumenter le choix des graphiques.", "تبرير اختيار الرسوم البيانية.")),
   pist=L(("Favoriser des débats à partir de situations significatives amenant l'apprenant à analyser des données.", "تفضيل النقاشات انطلاقا من وضعيات ذات دلالة تدفع المتعلم إلى تحليل المعطيات."), ("Inciter les apprenants à la créativité et à l'innovation.", "تشجيع المتعلمين على الإبداع والابتكار."), ("Inviter les apprenants à la collaboration et à la publication de leurs projets.", "دعوة المتعلمين إلى التعاون ونشر مشاريعهم."))),
}
SRC = ("Source : Curriculum d'informatique – 7ème, 8ème et 9ème année de base (9ème : École numérique, année scolaire 2018-2019).", "المصدر: منهاج الإعلامية – السنوات 7 و8 و9 من التعليم الأساسي (السنة 9: المدرسة الرقمية، السنة الدراسية 2018-2019).")
AIDE_SRC = ("Aide pédagogique – Informatique (Ministère de l'Éducation, septembre 2026) : détails transcrits des photographies, à relire avec le document.", "المساعدة البيداغوجية: الإعلامية (وزارة التربية، سبتمبر 2026): تفاصيل منقولة من الصور، تُراجَع مع الوثيقة.")
# 9e : domaines « Environnement » et « Internet » ajoutés d'après l'aide pédagogique de septembre 2026
PDF[(9, "env")] = dict(comps=L((A[(9, "env")]["comp_fr"], A[(9, "env")]["comp_ar"])), life=None)
PDF[(9, "net")] = dict(comps=L((A[(9, "net")]["comp_fr"], A[(9, "net")]["comp_ar"])), life=None)
AXES_BY_YEAR = {7: ["env", "net", "create", "prog"], 8: ["env", "net", "create", "prog"], 9: ["env", "net", "prog", "prod"]}

def build():
    pages = {}
    for y, keys in AXES_BY_YEAR.items():
        for k in keys:
            d = PDF[(y, k)]; t = d.get("title") or AX[k]; aide = A.get((y, k)) if (y, k) in A and k != "create" or (y, k) in A and y != 9 else None
            if y == 9 and k == "prod": aide = None
            pg = dict(year=y, axis=k, title_fr=t[0], title_ar=t[1], comps_fr=[c[0] for c in d["comps"]], comps_ar=[c[1] for c in d["comps"]],
                      life_fr=(d["life"] or ("", ""))[0], life_ar=(d["life"] or ("", ""))[1], champ_fr=(d.get("champ") or ("", ""))[0], champ_ar=(d.get("champ") or ("", ""))[1],
                      prat_fr=[c[0] for c in d.get("prat", [])], prat_ar=[c[1] for c in d.get("prat", [])], pist_fr=[c[0] for c in d.get("pist", [])], pist_ar=[c[1] for c in d.get("pist", [])],
                      aide=({kk: aide[kk] for kk in ("comp_fr", "comp_ar", "parts", "know_fr", "know_ar", "cad_fr", "cad_ar")} if aide and aide.get("parts") else None))
            pages[f"{y}-{k}"] = pg
    by_year = {str(y): v for y, v in AXES_BY_YEAR.items()}
    import secondaire as S
    for y in ("s1", "s2", "s3", "s4"):
        by_year[y] = list(S.DOM)
        for k, t in S.DOM.items():
            c = S.COMPS[y][k]
            pages[f"{y}-{k}"] = dict(year=y, axis=k, title_fr=t[0], title_ar=t[1], comps_fr=[c[0]], comps_ar=[c[1]], life_fr="", life_ar="", champ_fr="", champ_ar="", prat_fr=[], prat_ar=[], pist_fr=[], pist_ar=[], aide=None)
    data = dict(order=["7", "8", "9", "s1", "s2", "s3", "s4"], axes={k: dict(fr=v[0], ar=v[1]) for k, v in {**AX, **__import__("secondaire").DOM}.items()}, by_year=by_year,
                years={str(y): dict(fr=v[0], ar=v[1], short_fr=v[2], short_ar=v[3]) for y, v in YEARS.items()}, pages=pages,
                src_fr=SRC[0], src_ar=SRC[1], aide_fr=AIDE_SRC[0], aide_ar=AIDE_SRC[1])
    json.dump(data, open(os.path.join(HERE, "axes.json"), "w", encoding="utf-8"), ensure_ascii=False)
    return data
if __name__ == "__main__":
    d = build(); print("pages :", len(d["pages"]), sorted(d["pages"]), "| avec détails 2025 :", sorted(k for k, v in d["pages"].items() if v["aide"]))
