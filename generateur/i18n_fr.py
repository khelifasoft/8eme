"""Traductions françaises de la page d'accueil (le texte de la page est en arabe, la traduction est faite à l'affichage)."""
import re

STORIES_FR = {
 "cinderella": ("Cendrillon", "Cendrillon vit avec sa belle-mère et ses deux demi-sœurs, qui lui donnent toutes les tâches de la maison.", "Morale : la gentillesse et la patience finissent par être récompensées."),
 "layla": ("Le Petit Chaperon rouge", "Sa mère donne à Layla un panier de nourriture pour sa grand-mère malade et lui conseille de ne pas parler aux inconnus.", "Morale : ne parle pas aux inconnus et ne leur confie rien."),
 "djeha": ("Djeha et l'âne", "Djeha part au marché avec son fils et leur âne.", "Morale : on ne peut jamais contenter tout le monde."),
 "alibaba": ("Ali Baba et les quarante voleurs", "Ali Baba était un pauvre bûcheron.", "Morale : l'intelligence est plus forte que la cupidité."),
 "sindbad": ("Sindbad le marin", "Sindbad décide de partir en bateau pour faire du commerce.", "Morale : le courage et la patience sauvent celui qui les possède."),
 "crow": ("Le corbeau et le renard", "Un corbeau trouve un fromage et va se percher sur une branche pour le manger.", "Morale : ne crois pas tous ceux qui te flattent."),
 "hare": ("Le lièvre et la tortue", "Le lièvre se vante de sa vitesse et se moque de la tortue, trop lente.", "Morale : la patience et la persévérance valent mieux que l'orgueil."),
 "lion": ("Le lion et le rat", "Un lion dormait dans la forêt quand une petite souris lui a couru dessus et l'a réveillé.", "Morale : ne méprise pas les petits, ils peuvent t'aider un jour."),
 "frog": ("La princesse et la grenouille", "La princesse jouait avec sa balle d'or près du puits du jardin quand la balle est tombée dans l'eau et elle s'est mise à pleurer.", "Morale : il faut tenir ses promesses."),
 "shepherd": ("Le berger menteur", "Un jeune berger gardait ses moutons sur la colline.", "Morale : on ne croit pas un menteur, même quand il dit la vérité."),
 "pigs": ("Les trois petits cochons", "Trois petits cochons décident que chacun construira sa maison.", "Morale : le travail bien fait et la patience protègent."),
 "duckling": ("Le vilain petit canard", "Les œufs de la maman cane éclosent, et le dernier petit est grand, gris et différent de ses frères.", "Morale : ne te moque de personne, la vraie beauté se montre avec le temps."),
}
THEMES_FR = {"غابة": "Forêt", "قصر": "Château", "بحر": "Mer", "سفينة": "Navire", "جزيرة": "Île", "صحراء": "Désert", "جبل": "Montagne", "كهف": "Grotte", "كنز وذهب": "Trésor et or",
 "ليل ونجوم": "Nuit étoilée", "ساعة": "Horloge", "سحر ولمعان": "Magie et étincelles", "حفلة ورقص": "Bal et danse", "حديقة": "Jardin", "بئر": "Puits", "مزرعة": "Ferme",
 "مرعى وتلال": "Prairie et collines", "قرية": "Village", "سوق": "Marché", "جسر ونهر": "Pont et rivière", "بيت": "Maison", "مطر": "Pluie", "ثلج وشتاء": "Neige et hiver", "ربيع": "Printemps",
 "نار": "Feu", "ريح": "Vent", "ذئب": "Loup", "أسد": "Lion", "فأر": "Souris", "أرنب": "Lièvre", "سلحفاة": "Tortue", "ثعلب": "Renard", "غراب": "Corbeau", "ضفدع": "Grenouille", "بطة": "Canard",
 "بجعة": "Cygne", "خروف وغنم": "Mouton", "خنزير": "Cochon", "حمار": "Âne", "جمل": "Chameau", "حصان": "Cheval", "فراشة": "Papillon", "عصفور": "Oiseau", "سباق": "Course",
 "شجرة": "Arbre", "شمس وغيوم": "Soleil et nuages", "أطفال يقرؤون": "Enfants qui lisent", "كتاب وقصص": "Livre de contes"}
UI = {
 "المراجع": "Références", "مراجع التلميذ": "Références pour l'élève", "مراجع الأستاذ": "Références pour l'enseignant", "فتح المراجع": "Ouvrir les références",
 "مراجع التلميذ ومراجع الأستاذ لهذا المستوى.": "Références pour l'élève et pour l'enseignant de ce niveau.",
 "لم تُضف مراجع بعد لهذا المستوى.": "Aucune référence n'a encore été ajoutée pour ce niveau.",
 "لإضافة مرجع: ضعه في المجلد references وأضف سطرا في الملف references.js.": "Pour ajouter une référence : la déposer dans le dossier references puis ajouter une ligne dans le fichier references.js.",
 "لم تُدرج بعد وثيقة منهاج هذا المستوى. يمكنك الاطلاع على المراجع المتاحة.": "Le document de programme de ce niveau n'a pas encore été ajouté. Tu peux consulter les références disponibles.",
 "المنهاج والمراجع والموارد التعليمية لمادة الإعلامية في تونس، من السنة السابعة إلى السنة التاسعة.": "Programme, références et ressources pédagogiques pour l'enseignement de l'informatique en Tunisie, de la 7e à la 9e année.",
 "PDF": "PDF", "موقع": "Site", "كتاب": "Livre", "أداة": "Outil",

 "الكفايات المراد تنميتها": "Compétences à développer", "الممارسات المنتظرة": "Pratiques envisagées", "مسالك مقترحة": "Pistes à envisager",
 "تفاصيل من المساعدة البيداغوجية (2026)": "Détails de l'Aide pédagogique (2026)", "الكفاية الحياتية المستهدفة:": "Compétence de vie visée :",

 "نظرة عامة": "Aperçu de l'année", "المحاور الدراسية حسب السنة": "Les axes d'étude par année", "اختر سنتك، ثم المحور الذي تريد دراسته.": "Choisis ton année, puis l'axe que tu veux étudier.",
 "اختر سنتك ثم المحور الذي تريد دراسته من القائمة أعلاه.": "Choisis ton année, puis l'axe que tu veux étudier dans le menu ci-dessus.",
 "← الرئيسية": "← Accueil", "المحاور الدراسية": "Axes d'étude", "فتح المحور": "Ouvrir l'axe", "المكوّنات والقدرات": "Composantes et capacités",
 "ستُضاف موارد هذا المحور لاحقا.": "Les ressources de cet axe seront ajoutées plus tard.",
 "في هذا المستوى تُستعمل بيئة تطوير بالكتل مثل App Inventor. لم تُنجَز موارد لهذا المحور بعد.": "À ce niveau, on utilise un environnement de développement par blocs tel qu'App Inventor. Aucune ressource n'est encore réalisée pour cet axe.",
 "٧": "7e", "٨": "8e", "٩": "9e",

 "الربط بالمنهاج: الفكر المنطقي والبرمجة": "Lien avec le programme : pensée logique et programmation", "الربط بالمنهاج:": "Lien avec le programme :", "بطاقة النشاط (بالفرنسية)": "Fiche d'activité (en français)",
 "المعارف المرتبطة": "Savoirs associés", "توجيهات الإطار": "Directives de cadrage",
 "النص منقول من صور الوثيقة الرسمية «المساعدة البيداغوجية: الإعلامية» (سبتمبر 2025)، فيُراجَع مع الوثيقة الأصلية.": "Texte transcrit à partir de photographies du document officiel « Aide pédagogique : Informatique » (septembre 2025) ; à relire avec le document d'origine.",

 "الألعاب": "Jeux", "← كل القصص": "← Tous les contes", "فتح القصة وكل ما يخصها": "Ouvrir le conte et tout ce qui le concerne", "موارد عامة": "Ressources générales",
 "صور وأصوات وحركات تصلح لأي قصة.": "Images, sons et animations qui conviennent à n'importe quel conte.",
 "الصور والأصوات والحركات": "Images, sons et animations", "كل ما يخص هذه القصة. اضغط «تحميل» ثم أضف الملف في سكراتش.": "Tout ce qui concerne ce conte. Clique sur « Télécharger », puis ajoute le fichier dans Scratch.",

 "قصص سكراتش": "Histoires Scratch", "الرئيسية": "Accueil", "كيف أبدأ؟": "Comment commencer ?", "القصص": "Contes", "ألعاب سكراتش": "Jeux Scratch", "فيديوهات": "Vidéos",
 "المكتبة": "Bibliothèque", "صور وفيديوهات جاهزة": "Images et vidéos prêtes à l'emploi", "تحميل سكراتش": "Télécharger Scratch", "مساعدة": "Aide",
 "القائمة": "Menu", "القائمة الرئيسية": "Menu principal",
 "⬇ تحميل برنامج سكراتش": "⬇ Télécharger le programme Scratch", "⬇ اختصار على سطح المكتب": "⬇ Raccourci sur le bureau",
 "كل ما تحتاجه لإنشاء مشروعك في صفحة واحدة: أوراق المشاريع، مشاريع جاهزة، أصوات، صور، أماكن وديكورات. لا حاجة إلى الإنترنت.": "Tout ce qu'il faut pour créer ton projet sur une seule page : fiches de projet, projets prêts, sons, images, lieux et décors. Pas besoin d'Internet.",
 "أربع خطوات بسيطة.": "Quatre étapes simples.", "اختر قصة من القائمة أدناه.": "Choisis un conte dans la liste ci-dessous.",
 "حمّل": "Télécharge", "ورقة المشروع": "la fiche du projet", "واقرأها: فيها الملخص والسيناريو وخطوات العمل.": " et lis-la : elle contient le résumé, le scénario et les étapes du travail.",
 "افتح": "Ouvre", "سكراتش": "Scratch", "حمّله من هنا": "télécharge-le ici",
 ") ثم «ملف ← تحميل من حاسوبك» واختر ملف المشروع (.sb3).": "), puis « Fichier → Charger depuis votre ordinateur » et choisis le fichier du projet (.sb3).",
 "غيّر الصور والأصوات والحوارات من": "Modifie les images, les sons et les dialogues depuis la", "لتصنع مشروعك الخاص.": "pour créer ton propre projet.",
 "تحميل برنامج سكراتش 3": "Télécharger le programme Scratch 3", "لتشغيل المشاريع تحتاج إلى برنامج سكراتش. يمكنك استعماله على الإنترنت أو تثبيته على الحاسوب.": "Pour utiliser les projets, il te faut Scratch. Tu peux l'utiliser en ligne ou l'installer sur l'ordinateur.",
 "⬇ تحميل سكراتش 3 للحاسوب (من الموقع الرسمي)": "⬇ Télécharger Scratch 3 pour ordinateur (site officiel)", "فتح سكراتش على الإنترنت": "Ouvrir Scratch en ligne",
 "النسخة المثبّتة تعمل دون إنترنت وتفتح ملفات المشاريع (.sb3) مباشرة. الروابط تفتح الموقع الرسمي لسكراتش في نافذة جديدة.": "La version installée fonctionne sans Internet et ouvre directement les fichiers de projet (.sb3). Les liens ouvrent le site officiel de Scratch dans un nouvel onglet.",
 "اختر قصتك": "Choisis ton conte", "لكل قصة ورقة مشروع، ومشروع سكراتش جاهز، وحزمة واحدة تجمع كل ما تحتاجه.": "Chaque conte a sa fiche de projet, un projet Scratch prêt et un paquet unique qui rassemble tout ce qu'il te faut.",
 "ألعاب بسيطة وتعليمية: أسئلة وأجوبة، حساب، ذاكرة، وسرعة. حمّل اللعبة وافتحها في سكراتش، ثم عدّلها كما تشاء.": "Des jeux simples et éducatifs : questions-réponses, calcul, mémoire et rapidité. Télécharge le jeu, ouvre-le dans Scratch, puis modifie-le comme tu veux.",
 "اضغط على لقطة الفيديو لمشاهدته هنا دون مغادرة الصفحة.": "Clique sur la capture d'une vidéo pour la regarder ici, sans quitter la page.",
 "صور متحركة وفيديوهات جاهزة": "Images animées et vidéos prêtes à l'emploi", "مواقع مجانية فيها آلاف الصور والفيديوهات. اختر موضوعًا ليفتح لك البحث الجاهز في الموقع الذي تريده.": "Des sites gratuits avec des milliers d'images et de vidéos. Choisis un thème pour ouvrir la recherche déjà prête sur le site de ton choix.",
 "الصور والفيديوهات تبقى في مواقعها الأصلية ولا تُنسخ في هذا المشروع. لكل موقع رخصته الخاصة، فاقرأ شروطه قبل التحميل، ولا تعد نشر الملفات كمكتبة مستقلة. نتائج البحث قد تتغير مع الوقت.": "Les images et les vidéos restent sur leurs sites d'origine et ne sont pas copiées ici. Chaque site a sa propre licence : lis ses conditions avant de télécharger et ne republie pas les fichiers comme une bibliothèque indépendante. Les résultats de recherche peuvent changer avec le temps.",
 "صور وأصوات ورسوم متحركة يمكنك استعمالها في أي قصة. اضغط «تحميل» ثم أضف الملف في سكراتش.": "Images, sons et animations utilisables dans n'importe quel conte. Clique sur « Télécharger », puis ajoute le fichier dans Scratch.",
 "أضيف صورة جديدة": "Ajouter une image", "في سكراتش، اضغط على «اختيار لاعب» ثم «رفع لاعب».": "Dans Scratch, clique sur « Choisir un lutin », puis « Importer un lutin ».", "اختر ملف الصورة (.svg) من المجلد.": "Choisis le fichier image (.svg) dans le dossier.",
 "أضيف مكانًا (خلفية)": "Ajouter un lieu (arrière-plan)", "اضغط على «اختيار خلفية» ثم «رفع خلفية».": "Clique sur « Choisir un arrière-plan », puis « Importer un arrière-plan ».", "اختر ملفًا من «الأماكن».": "Choisis un fichier dans « Lieux ».",
 "أضيف صوتًا": "Ajouter un son", "افتح لسان «الأصوات» في اللاعب.": "Ouvre l'onglet « Sons » du lutin.", "اضغط «رفع صوت» واختر ملف (.wav).": "Clique sur « Importer un son » et choisis un fichier (.wav).", "استعمل الكتلة «ابدأ الصوت».": "Utilise le bloc « démarrer le son ».",
 "أصنع حركة": "Faire une animation", "حمّل «إطارات» الحركة من تبويب الصور المتحركة.": "Télécharge les « images » de l'animation depuis l'onglet Images animées.", "فك الضغط، ثم ارفع الصور كأزياء متتالية للاعب.": "Décompresse, puis importe les images comme costumes successifs du lutin.", "استعمل «التالي الزي» داخل حلقة مع «انتظر».": "Utilise « costume suivant » dans une boucle avec « attendre ».",
 "أسجّل صوتي": "Enregistrer ma voix", "الأصوات الجاهزة المسمّاة «أصوات جاهزة» مولَّدة آليًا. لتسجيل صوتك، افتح لسان «الأصوات» في سكراتش واضغط على الميكروفون.": "Les sons appelés « Voix prêtes » sont générés par ordinateur. Pour enregistrer ta voix, ouvre l'onglet « Sons » dans Scratch et clique sur le micro.",
 "✕ إغلاق": "✕ Fermer", "إغلاق": "Fermer", "اختصار على سطح المكتب": "Raccourci sur le bureau", "حسنًا": "D'accord",
 "الصور مرسومة خصيصًا لهذه الورشة، والأصوات والموسيقى مولَّدة بالحاسوب، ويمكنك استعمالها وتعديلها بحرّية في مشاريعك.": "Les images sont dessinées spécialement pour cet atelier ; les sons et la musique sont générés par ordinateur. Tu peux les utiliser et les modifier librement dans tes projets.",
 "ابحث في الفيديوهات…": "Rechercher dans les vidéos…", "بحث في الفيديوهات": "Rechercher dans les vidéos", "تصفية الفيديوهات حسب القصة": "Filtrer les vidéos par conte",
 "ابحث عن موضوع (غابة، بحر، قصر…)": "Chercher un thème (forêt, mer, château…)", "بحث عن موضوع": "Chercher un thème", "مواضيع حسب القصة": "Thèmes par conte",
 "ابحث بالعربية أو بالفرنسية…": "Rechercher en arabe ou en français…", "بحث": "Recherche", "تصفية حسب القصة": "Filtrer par conte",
 "الأماكن": "Lieux", "خلفيات كاملة للمشاهد": "Arrière-plans complets pour les scènes", "الديكور": "Décors", "أشياء تضعها في المشهد": "Objets à placer dans la scène", "الشخصيات": "Personnages", "الحيوانات": "Animaux", "الأزياء": "Costumes",
 "إكسسوارات": "Accessoires", "ملابس": "Tenues", "نسخ القصص": "Versions des contes", "الصور المتحركة": "Images animées", "الأصوات": "Sons", "مؤثرات صوتية": "Effets sonores", "موسيقى": "Musique", "أصوات جاهزة": "Voix prêtes",
 "Word قديم (.doc)": "Word ancien (.doc)", "للإصدارات القديمة من Word (2003 و2007)": "Pour les anciennes versions de Word (2003 et 2007)", "قراءة الورقة": "Lire la fiche", "مشروع سكراتش": "Projet Scratch", "ورقة المشروع (Word)": "Fiche du projet (Word)", "كل شيء (.zip)": "Tout (.zip)",
 "كل القصص": "Tous les contes", "الكل": "Tout", "لا توجد نتائج. جرّب كلمة أخرى أو اختر «كل القصص».": "Aucun résultat. Essaie un autre mot ou choisis « Tous les contes ».", "تحميل": "Télécharger", "فيديو": "Vidéo",
 "لا توجد فيديوهات مطابقة.": "Aucune vidéo correspondante.", "لا توجد فيديوهات حاليًا.": "Aucune vidéo pour le moment.", "كل المواضيع": "Tous les thèmes", "لا توجد مواضيع مطابقة.": "Aucun thème correspondant.",
 "Pexels صور": "Pexels photos", "Pexels فيديو": "Pexels vidéos", "Pixabay صور": "Pixabay photos", "Pixabay فيديو": "Pixabay vidéos", "Mixkit فيديو": "Mixkit vidéos",
 "في آيفون وآيباد:": "Sur iPhone et iPad :", "اضغط على زر المشاركة في Safari.": "Appuie sur le bouton Partager de Safari.", "اختر «إضافة إلى الشاشة الرئيسية».": "Choisis « Sur l'écran d'accueil ».",
 "في هاتف أندرويد:": "Sur un téléphone Android :", "اضغط على قائمة المتصفح (⋮).": "Appuie sur le menu du navigateur (⋮).", "اسحب الملف إلى سطح المكتب.": "Glisse le fichier sur le bureau.",
 "اسحب الملف إلى سطح المكتب أو إلى الـ Dock.": "Glisse le fichier sur le bureau ou dans le Dock.", "انقله إلى سطح المكتب، ثم انقر عليه بالزر الأيمن واختر «السماح بالتشغيل».": "Déplace-le sur le bureau, puis fais un clic droit et choisis « Autoriser l'exécution ».",
 "عند النقر عليه يفتح الموقع في المتصفح مباشرة. إن ظهر تحذير أثناء التنزيل فاختر «الاحتفاظ بالملف».": "Un clic dessus ouvre directement le site dans le navigateur. Si un avertissement apparaît pendant le téléchargement, choisis « Conserver le fichier ».",
 "ملاحظة: التثبيت كتطبيق مستقل يتطلب HTTPS. على شبكة محلية بدون HTTPS يعمل الاختصار بالشكل الموضّح أعلاه.": "Remarque : l'installation comme application autonome nécessite HTTPS. Sur un réseau local sans HTTPS, le raccourci fonctionne comme décrit ci-dessus.",
 "تحميل اللعبة (.sb3)": "Télécharger le jeu (.sb3)", "العب هنا": "Jouer ici", "فتح في سكراتش": "Ouvrir dans Scratch",
}
RULES = [
 [r"^← (.+)$", "← $1"],
 [r"^(\d+) عنصر$", "$1 éléments"], [r"^(\d+) فيديو$", "$1 vidéos"], [r"^(\d+) موضوع$", "$1 thèmes"],
 [r"^تحميل الإطارات \((\d+)\)$", "Télécharger les images ($1)"], [r"^موارد القصة \((\d+)\)$", "Ressources du conte ($1)"],
 [r"^تحميل كل «(.+)» \(\.zip\)$", "Tout télécharger : « $1 » (.zip)"], [r"^استمع: (.+)$", "Écouter : $1"], [r"^مشاهدة: (.+)$", "Regarder : $1"], [r"^فتح: (.+)$", "Ouvrir : $1"],
 [r"^فتح في الموقع الأصلي \((.+)\)$", "Ouvrir sur le site d'origine ($1)"], [r"^(.+) · ([\d.]+) ث$", "$2 s"], [r"^([\d.]+) ث$", "$1 s"], [r"^نسخة (.+)$", "Version $1"],
 [r"^تم تنزيل ملف الاختصار «(.+)»\. (.+)$", "Le fichier de raccourci « $1 » a été téléchargé. $2"],
]
# ---- noms d'éléments de la bibliothèque (déduits des identifiants français, avec accents)
LEX = {"cendrillon": "Cendrillon", "servante": "servante", "bal": "au bal", "belle": "belle", "mere": "mère", "soeur": "sœur", "fee": "fée", "laila": "Petit Chaperon rouge", "grand": "grand", "bucheron": "bûcheron",
 "djeha": "Djeha", "fils": "fils de", "passant": "passant", "ali": "Ali", "baba": "Baba", "qasim": "Qasim", "morgiane": "Morgiane", "chef": "chef", "voleurs": "des voleurs", "marin": "marin", "capitaine": "capitaine",
 "roi": "roi", "reine": "reine", "arbitre": "arbitre", "garcon": "garçon", "marchand": "marchand", "maitre": "maître", "maitresse": "maîtresse", "vieux": "vieil homme", "pecheur": "pêcheur", "berger": "berger",
 "gueule": "gueule ouverte", "ane": "âne", "piege": "piégé", "bec": "bec", "ouvert": "ouvert", "ouverte": "ouverte", "lievre": "lièvre", "endormi": "endormi", "saut": "saute", "oeuf": "œuf", "oeufs": "œufs",
 "caneton": "caneton", "gris": "gris", "chateau": "château", "fermee": "fermée", "ferme": "fermé", "fenetre": "fenêtre", "ile": "île", "sac": "sac", "or": "d'or", "pieces": "pièces", "gateau": "gâteau",
 "verre": "de verre", "cle": "clé", "trone": "trône", "barriere": "barrière", "etoile": "étoile", "epee": "épée", "echelle": "échelle", "ney": "flûte (ney)", "nenuphar": "nénuphar", "effondree": "effondrée",
 "foret": "forêt", "interieur": "intérieur", "exterieur": "extérieur", "marche": "marché", "riviere": "rivière", "desert": "désert", "etoiles": "étoiles", "arrivee": "arrivée", "ecole": "école", "pature": "pâturage",
 "etang": "étang", "chambre": "chambre", "palais": "palais", "salle": "salle", "dense": "dense", "soir": "du soir", "maisons": "maisons", "bonhomme": "bonhomme", "camp": "de camp", "minuit": "de minuit", "trois": "de trois heures",
 "tete": "tête", "cygne": "cygne", "prince": "prince", "princesse": "princesse"}
ANIM_FR = {"oiseau_vole": "Oiseau qui vole", "poisson_nage": "Poisson qui nage", "grenouille_saute": "Grenouille qui saute", "baleine_plonge": "Baleine qui plonge", "papillon": "Papillon", "porte_s_ouvre": "Porte qui s'ouvre",
 "feu": "Feu qui brûle", "vagues": "Vagues", "horloge_tourne": "Horloge qui tourne", "piece_tourne": "Pièce qui tourne", "etoile_scintille": "Étoile qui scintille", "soleil_tourne": "Soleil qui brille", "pluie": "Pluie",
 "neige": "Neige", "bateau_tangue": "Bateau qui tangue", "baguette_magique": "Baguette magique", "coeur_bat": "Cœur qui bat", "nuage_passe": "Nuage qui passe", "maison_s_effondre": "Maison qui s'écroule",
 "oeuf_eclot": "Œuf qui éclot", "cygne_nage": "Cygne qui nage"}
HATS = {"turban": "turban", "crown": "couronne", "tiara": "diadème", "hood": "capuchon rouge", "cap": "casquette", "fez": "fez", "sailor": "bonnet de marin", "mask": "masque de voleur", "bonnet": "bonnet de grand-mère", "scarf": "foulard", "helmet": "casque"}
OBJ = {"wand": "baguette magique", "basket": "panier", "axe": "hache", "sack": "sac", "whistle": "sifflet", "sword": "épée", "ball": "balle dorée", "cane": "canne", "bag": "sacoche"}
ACC = {"ailes_fee": "Ailes de fée", "lunettes": "Lunettes", "cape_rouge": "Cape rouge", "robe_bal": "Robe de bal", "robe_servante": "Robe de servante"}
COL = ["rouge", "bleu", "vert", "jaune", "violet", "orange", "rose", "noir"]

def pretty(i):
    r = " ".join(LEX.get(t, t) for t in i.split("_")); r = r[:1].upper() + r[1:]
    for a, b in (("Belle mère", "Belle-mère"), ("rand mère", "rand-mère"), ("Petit chaperon rouge", "Petit Chaperon rouge")): r = r.replace(a, b)
    return r
def fr_label(a):
    i, cat, sub = a["id"], a["cat"], a.get("sub", "")
    if a.get("fr"): return a["fr"]
    if cat == "animations":
        if i in ANIM_FR: return ANIM_FR[i]
        m = re.match(r"(marche|parle)_(.+)", i)
        if m: return f"{pretty(m.group(2))} {'marche' if m.group(1) == 'marche' else 'parle'}"
    if cat == "costumes":
        if sub == "accessoires":
            if i in ACC: return ACC[i]
            if i.startswith("chapeau_"): return "Chapeau : " + HATS.get(i[8:], i[8:])
            if i.startswith("objet_"): return "Accessoire : " + OBJ.get(i[6:], i[6:])
        if sub == "tenues":
            m = re.match(r"(garcon|fille|djellaba|femme)_(\d)", i)
            if m:
                c = COL[int(m.group(2)) - 1]
                return {"garcon": f"Garçon en {c}", "fille": f"Fille en {c}", "djellaba": f"Homme en djellaba {c}", "femme": f"Femme en robe {c}"}[m.group(1)]
        if sub == "variantes": return pretty(i[4:])
    return pretty(i)

def build(man, games):
    M = dict(UI)
    cur = man.get("curriculum")
    if cur:
        for a in cur["axes"].values(): M[a["ar"]] = a["fr"]
        for y in cur["years"].values(): M[y["ar"]] = y["fr"]
        M[cur["src_ar"]] = cur["src_fr"]; M[cur["aide_ar"]] = cur["aide_fr"]
        for pg in cur["pages"].values():
            M[pg["title_ar"]] = pg["title_fr"]
            for k in ("comps", "prat", "pist"):
                for a, b in zip(pg[k + "_ar"], pg[k + "_fr"]): M[a] = b
            if pg["life_ar"]: M[pg["life_ar"]] = pg["life_fr"]
            if pg["champ_ar"]: M["ميدان الاعتبار: " + pg["champ_ar"]] = "Champ : " + pg["champ_fr"]
            ad = pg.get("aide")
            if ad:
                M[ad["comp_ar"]] = ad["comp_fr"]
                for a, b in zip(ad["know_ar"], ad["know_fr"]): M[a] = b
                for a, b in zip(ad["cad_ar"], ad["cad_fr"]): M[a] = b
                for x in ad["parts"]:
                    M[x["t_ar"]] = x["t_fr"]
                    for a, b in zip(x["i_ar"], x["i_fr"]): M[a] = b
        M = {k: v for k, v in M.items() if v is not None}
    prg = man.get("programme")
    if prg:
        for c in prg["concepts"].values(): M[c["ar"]] = c["fr"]
        for L in prg["levels"].values():
            M[L["year_ar"]] = L["year_fr"]; M[L["comp_ar"]] = L["comp_fr"]
            for a, b in zip(L["know_ar"], L["know_fr"]): M[a] = b
            for a, b in zip(L["cad_ar"], L["cad_fr"]): M[a] = b
            for x in L["parts"]:
                M[x["t_ar"]] = x["t_fr"]
                for a, b in zip(x["i_ar"], x["i_fr"]): M[a] = b
        M[prg["general_ar"]] = prg["general_fr"]
    for k, (t, s, m) in STORIES_FR.items(): pass
    for st in man["stories"]:
        t, s, m = STORIES_FR[st["key"]]
        M[st["title"]] = t; M[st["summary"]] = s; M[st["morale"]] = m
    M.update(THEMES_FR)
    for a in man["assets"]:
        if a["label"] not in M: M[a["label"]] = fr_label(a)
    for g in games:
        M[g["title_ar"]] = g["title_fr"]; M[g["how_ar"]] = g["how_fr"]; M[g["cat_ar"]] = g["cat_fr"]
    return {"map": M, "rules": RULES}
