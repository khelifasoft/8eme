// Logiciels à télécharger. Pour ajouter un logiciel : copier un bloc et adapter.
// levels : "all" ou liste de niveaux ["7","8","9","s1","s2","s3","s4"]. Les liens pointent vers les sites officiels.
window.LOGICIELS = [
 {cat:"prog", name:"Scratch 3 (version hors ligne)", fr:"Scratch 3 (version hors ligne)", levels:["7","8","9"], url:"https://scratch.mit.edu/download",
  ar:"بيئة البرمجة المرئية لإنجاز القصص والألعاب. تعمل دون اتصال بالإنترنت. اضغط على الزر المناسب لنظامك: يبدأ التنزيل مباشرة.", desc_fr:"Environnement de programmation visuelle pour créer contes et jeux, utilisable hors ligne. Clique sur le bouton de ton système : le téléchargement démarre directement.", os:"Windows · macOS",
  // boutons d'installation sur le bureau : liens directs vers les installateurs officiels (redirigés vers la dernière version) ; vérifiés le 09/11/2026 (Scratch 3.32.1)
  links:[
   {os:"windows", direct:true, url:"https://downloads.scratch.mit.edu/desktop/Scratch%20Setup.exe", ar:"⬇ تثبيت على Windows (.exe)", fr:"⬇ Installer pour Windows (.exe)", note_ar:"حوالي 200 ميغابايت", note_fr:"environ 200 Mo"},
   {os:"mac", direct:true, url:"https://downloads.scratch.mit.edu/desktop/Scratch.dmg", ar:"⬇ تثبيت على macOS (.dmg)", fr:"⬇ Installer pour macOS (.dmg)", note_ar:"حوالي 340 ميغابايت", note_fr:"environ 340 Mo"},
   {url:"https://scratch.mit.edu/download", ar:"صفحة التحميل الرسمية (أنظمة أخرى)", fr:"Page officielle de téléchargement (autres systèmes)"}]},
 {cat:"prog", name:"Scratch 3 en ligne (lien direct)", fr:"Scratch 3 en ligne (lien direct)", levels:["7","8","9"], url:"https://scratch.mit.edu/projects/editor/",
  ar:"محرر سكراتش داخل المتصفح دون تثبيت.", desc_fr:"Éditeur Scratch dans le navigateur, sans installation.", os:"Web"},
 {cat:"prog", name:"MIT App Inventor", fr:"MIT App Inventor", levels:["9"], url:"https://appinventor.mit.edu/",
  ar:"إنشاء تطبيقات للهاتف بالكتل البرمجية.", desc_fr:"Création d'applications mobiles par blocs.", os:"Web"},
 {cat:"prog", name:"mBlock", fr:"mBlock", levels:["9"], url:"https://mblock.makeblock.com/en-us/download/",
  ar:"برمجة بالكتل للروبوتات والمتحكمات.", desc_fr:"Programmation par blocs de robots et de cartes électroniques.", os:"Windows · macOS"},
 {cat:"prog", name:"Arduino IDE", fr:"Arduino IDE", levels:["9","s3","s4"], url:"https://www.arduino.cc/en/software",
  ar:"بيئة برمجة لوحات أردوينو.", desc_fr:"Environnement de programmation des cartes Arduino.", os:"Windows · macOS · Linux"},
 {cat:"prog", name:"Python", fr:"Python", levels:["s1","s2","s3","s4"], url:"https://www.python.org/downloads/",
  ar:"لغة البرمجة المستعملة في المرحلة الثانوية.", desc_fr:"Le langage de programmation utilisé au secondaire.", os:"Windows · macOS · Linux"},
 {cat:"prog", name:"Thonny", fr:"Thonny", levels:["s1","s2","s3","s4"], url:"https://thonny.org/",
  ar:"محرر بايثون بسيط للمبتدئين.", desc_fr:"Éditeur Python simple pour débutants.", os:"Windows · macOS · Linux"},
 {cat:"prog", name:"Visual Studio Code", fr:"Visual Studio Code", levels:["s3","s4"], url:"https://code.visualstudio.com/download",
  ar:"محرر نصوص وأكواد متقدم.", desc_fr:"Éditeur de code avancé.", os:"Windows · macOS · Linux"},
 {cat:"bureau", name:"LibreOffice", fr:"LibreOffice", levels:"all", url:"https://www.libreoffice.org/download/download-libreoffice/",
  ar:"مجموعة مكتبية مجانية: معالج نصوص وعروض وجداول بيانات.", desc_fr:"Suite bureautique libre : traitement de texte, présentations, tableur.", os:"Windows · macOS · Linux"},
 {cat:"media", name:"Audacity", fr:"Audacity", levels:["8"], url:"https://www.audacityteam.org/download/",
  ar:"تسجيل الصوت وتعديله.", desc_fr:"Enregistrement et édition audio.", os:"Windows · macOS · Linux"},
 {cat:"media", name:"Shotcut", fr:"Shotcut", levels:["8"], url:"https://shotcut.org/download/",
  ar:"مونتاج الفيديو.", desc_fr:"Montage vidéo.", os:"Windows · macOS · Linux"},
 {cat:"media", name:"GIMP", fr:"GIMP", levels:["7","8"], url:"https://www.gimp.org/downloads/",
  ar:"تحرير الصور.", desc_fr:"Retouche d'images.", os:"Windows · macOS · Linux"},
 {cat:"media", name:"Inkscape", fr:"Inkscape", levels:["7","8"], url:"https://inkscape.org/release/",
  ar:"الرسم المتجهي (SVG).", desc_fr:"Dessin vectoriel (SVG).", os:"Windows · macOS · Linux"},
 {cat:"data", name:"DB Browser for SQLite", fr:"DB Browser for SQLite", levels:["s3","s4"], url:"https://sqlitebrowser.org/dl/",
  ar:"إنشاء قواعد البيانات والاستعلام عنها بلغة SQL.", desc_fr:"Création et interrogation de bases de données en SQL.", os:"Windows · macOS · Linux"},
 {cat:"net", name:"Filius", fr:"Filius", levels:["s2","s4"], url:"https://www.lernsoftware-filius.de/Herunterladen",
  ar:"محاكاة الشبكات الحاسوبية.", desc_fr:"Simulation de réseaux informatiques.", os:"Windows · macOS · Linux"},
 {cat:"util", name:"7-Zip", fr:"7-Zip", levels:"all", url:"https://www.7-zip.org/download.html",
  ar:"فك ضغط الملفات (مثل ملفات zip المحملة من الموقع).", desc_fr:"Décompression de fichiers (par exemple les zip téléchargés sur ce site).", os:"Windows"}
];
window.LOGICIEL_CATS = {prog:["البرمجة والروبوتيك","Programmation et robotique"], bureau:["المكتبية","Bureautique"], media:["الصوت والصورة والفيديو","Audio, image et vidéo"], data:["قواعد البيانات","Bases de données"], net:["الشبكات","Réseaux"], util:["أدوات مساعدة","Utilitaires"]};
