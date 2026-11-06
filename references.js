// Références de la page « المراجع / Références » de chaque niveau.
// Une ligne par référence. Champs :
//   level : "7", "8", "9", "s1", "s2", "s3", "s4"  (ou une liste, par exemple ["7","8","9"], ou "all")
//           s1 = 1ère année secondaire, s2 = 2e, s3 = 3e, s4 = 4e
//   for   : "eleve" (pour l'élève) ou "enseignant" (pour l'enseignant)
//   title : titre (en arabe ou en français)      fr : titre en français (facultatif)
//   url   : adresse (https://…) OU chemin d'un fichier du dépôt (par exemple references/mon-manuel.pdf)
//   type  : "pdf", "site", "livre", "outil" (facultatif)       note : précision en arabe (facultatif)    note_fr : précision en français (facultatif)
// Pour ajouter un document : le déposer dans le dossier references/ puis ajouter une ligne ci-dessous.
window.REFERENCES = [
  { level: ["7", "8", "9"], for: "enseignant", type: "pdf", title: "منهاج الإعلامية: السنوات 7 و8 و9 من التعليم الأساسي", fr: "Curriculum d'informatique – 7e, 8e et 9e année de base", url: "references/curriculum-informatique-7-8-9.pdf", note: "المجالات والكفايات لكل سنة (السنة 9: المدرسة الرقمية، 2018-2019).", note_fr: "Domaines d'apprentissage et compétences par année (la 9e : École numérique, 2018-2019)." },
  { level: ["7", "8", "9"], for: "eleve", type: "outil", title: "سكراتش: برنامج البرمجة البصرية", fr: "Scratch : programmation visuelle", url: "https://scratch.mit.edu/", note: "لفتح مشاريع .sb3 الموجودة في هذا الموقع.", note_fr: "Pour ouvrir les projets .sb3 de ce site." },
  { level: ["7", "8", "9"], for: "enseignant", type: "outil", title: "سكراتش: برنامج البرمجة البصرية", fr: "Scratch : programmation visuelle", url: "https://scratch.mit.edu/", note: "بيئة البرمجة بالكتل الموصى بها في المنهاج.", note_fr: "Environnement par blocs recommandé par le programme." },
  { level: "7", for: "eleve", type: "site", title: "قصص سكراتش وبطاقات المشاريع (هذا الموقع)", fr: "Contes Scratch et fiches de projet (ce site)", url: "#y7-prog" },
  { level: "8", for: "eleve", type: "site", title: "ألعاب سكراتش التعليمية (هذا الموقع)", fr: "Jeux Scratch éducatifs (ce site)", url: "#y8-prog" },
  { level: "8", for: "enseignant", type: "site", title: "بطاقات الأنشطة بالفرنسية (هذا الموقع)", fr: "Fiches d'activité en français (ce site)", url: "fiches-activite/quiz.html" },
  { level: "9", for: "eleve", type: "outil", title: "App Inventor: تطوير تطبيقات الهاتف بالكتل", fr: "App Inventor : applications mobiles par blocs", url: "https://appinventor.mit.edu/", note: "مذكور في المساعدة البيداغوجية 2025 لبرمجة تطبيقات الهاتف.", note_fr: "Cité dans l'Aide pédagogique 2025 pour la programmation d'applications mobiles." }
];
