"""9e : activité ou mini-projet de chacune des 8 séances micro:bit (M1-M4) et App Inventor (A1-A4), avec vidéo explicative (la carte ou l'écran de l'application « en marche »,
dessinés et animés par video_objets.py) et ressources à télécharger (programme MakeCode en JavaScript, images, plan des blocs App Inventor), objets/ressources/<séance>.zip.
Tout est simulé (aucun matériel ni compte requis). Textes : couples (français, arabe)."""
from xml.sax.saxutils import escape
FONT = "Tajawal,DejaVu Sans,Arial,sans-serif"
PAT = {"heart": ["01010", "11111", "11111", "01110", "00100"], "sad": ["00000", "01010", "00000", "01110", "10001"], "happy": ["00000", "01010", "00000", "10001", "01110"], "blank": ["00000"] * 5,
       "1": ["00100", "01100", "00100", "00100", "01110"], "2": ["01110", "10001", "00110", "01000", "11111"], "3": ["11110", "00001", "01110", "00001", "11110"],
       "4": ["10010", "10010", "11111", "00010", "00010"], "5": ["11111", "10000", "11110", "00001", "11110"], "6": ["01110", "10000", "11110", "10001", "01110"]}
def L(lang, p): return p[1] if lang == "ar" else p[0]

def microbit(pat="blank", a=False, b=False, tags=(), temp=None, sound=False, shake=False, lang="fr", link=False):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 400" width="560" height="400" style="direction:ltr"><rect x="70" y="20" width="420" height="350" rx="26" fill="#2b2f3a" stroke="#14161c" stroke-width="4"/>'
    s += '<rect x="90" y="344" width="380" height="14" rx="4" fill="#d4af37"/>'
    for r, row in enumerate(PAT[pat]):
        for c, v in enumerate(row):
            x, y = 280 + (c - 2) * 46, 120 + (r - 2) * 46
            s += f'<circle cx="{x}" cy="{y}" r="15" fill="{"#ff3b30" if v == "1" else "#4a2a2e"}"/>' + (f'<circle cx="{x}" cy="{y}" r="24" fill="#ff3b30" opacity=".25"/>' if v == "1" else "")
    for x, name, on in ((130, "A", a), (430, "B", b)):
        s += f'<circle cx="{x}" cy="250" r="32" fill="{"#ffd24d" if on else "#8a909c"}" stroke="#14161c" stroke-width="3"/><text x="{x}" y="260" text-anchor="middle" font-size="28" font-weight="800" fill="#14161c" font-family="Arial">{name}</text>'
    s += '<text x="280" y="305" text-anchor="middle" font-size="22" font-weight="700" fill="#9aa3b2" font-family="Arial">micro:bit</text>'
    if temp is not None: s += f'<rect x="196" y="320" width="168" height="34" rx="10" fill="#fff" opacity=".95"/><text x="280" y="344" text-anchor="middle" font-size="24" font-weight="800" fill="#c0392b" font-family="Arial">{temp} °C</text>'
    if sound: s += '<text x="498" y="90" font-size="44" font-family="Noto Color Emoji">🔊</text>'
    if shake: s += '<path d="M30 110 q-14 20 0 40 M12 100 q-24 30 0 60" fill="none" stroke="#e8861c" stroke-width="6" stroke-linecap="round"/><path d="M530 220 q14 20 0 40 M548 210 q24 30 0 60" fill="none" stroke="#e8861c" stroke-width="6" stroke-linecap="round"/>'
    if link: s += '<text x="280" y="395" text-anchor="middle" font-size="26" font-family="Noto Color Emoji">📶</text>'
    for (txt, x, y, tx, ty) in tags:
        w = 11 * len(L(lang, txt)) + 24
        s += f'<line x1="{x}" y1="{y}" x2="{tx}" y2="{ty}" stroke="#e8861c" stroke-width="3"/><circle cx="{tx}" cy="{ty}" r="6" fill="#e8861c"/><rect x="{x - w / 2}" y="{y - 16}" width="{w}" height="32" rx="16" fill="#e8861c"/><text x="{x}" y="{y + 6}" text-anchor="middle" font-size="17" font-weight="700" fill="#fff" font-family="{FONT}">{escape(L(lang, txt))}</text>'
    return s + "</svg>"

def phone(widgets, lang="fr", title=("Convertisseur", "المحوّل"), pressed=None, status=None):
    s = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 560" width="300" height="560" style="direction:ltr"><rect x="4" y="4" width="292" height="552" rx="34" fill="#1d2433"/><rect x="18" y="44" width="264" height="468" rx="6" fill="#fff"/>'
    s += f'<rect x="18" y="44" width="264" height="40" fill="#3f7ee0"/><text x="150" y="70" text-anchor="middle" font-size="18" font-weight="700" fill="#fff" font-family="{FONT}">{escape(L(lang, title))}</text>'
    y = 100
    for w in widgets:
        k = w[0]
        if k == "label": s += f'<text x="150" y="{y + 22}" text-anchor="middle" font-size="{w[2] if len(w) > 2 else 20}" font-weight="700" fill="#1d2433" font-family="{FONT}">{escape(L(lang, w[1]))}</text>'; y += 46
        elif k == "textbox": s += f'<rect x="40" y="{y}" width="220" height="44" rx="6" fill="#fff" stroke="#8a909c" stroke-width="2"/><text x="52" y="{y + 29}" font-size="20" fill="{"#999" if len(w) > 2 and w[2] else "#1d2433"}" font-family="{FONT}">{escape(L(lang, w[1]))}</text>'; y += 62
        elif k == "button": s += f'<rect x="60" y="{y}" width="180" height="46" rx="10" fill="{"#1e4fa8" if len(w) > 2 and w[2] else "#3f7ee0"}"/><text x="150" y="{y + 30}" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" font-family="{FONT}">{escape(L(lang, w[1]))}</text>'; y += 62
        elif k == "image": s += f'<text x="150" y="{y + 70}" text-anchor="middle" font-size="64" font-family="Noto Color Emoji">{w[1]}</text>'; y += 90
        elif k == "status": s += f'<rect x="40" y="{y}" width="220" height="36" rx="18" fill="{w[2]}"/><text x="150" y="{y + 25}" text-anchor="middle" font-size="17" font-weight="700" fill="#fff" font-family="{FONT}">{escape(L(lang, w[1]))}</text>'; y += 52
        elif k == "gap": y += w[1]
    if status: s += f'<text x="150" y="530" text-anchor="middle" font-size="14" fill="#9aa3b2" font-family="{FONT}">{escape(L(lang, status))}</text>'
    return s + "</svg>"

CODE = {
 "M2": ("m2-programme.ts", "input.onButtonPressed(Button.A, function () {\n    basic.showIcon(IconNames.Heart)\n    basic.pause(1000)\n    basic.clearScreen()\n})\ninput.onButtonPressed(Button.B, function () {\n    basic.showIcon(IconNames.Happy)\n    basic.pause(1000)\n    basic.clearScreen()\n})\n"),
 "M3": ("m3-alarme.ts", "basic.forever(function () {\n    if (input.temperature() > 30) {\n        basic.showIcon(IconNames.Sad)\n        music.playTone(262, music.beat(BeatFraction.Whole))\n    } else {\n        basic.showIcon(IconNames.Happy)\n    }\n})\n"),
 "M4": ("m4-de.ts", "let de = 0\ninput.onGesture(Gesture.Shake, function () {\n    de = randint(1, 6)\n    basic.showNumber(de)\n})\n"),
 "A2": ("a2-plan-des-blocs.txt", "quand BoutonCalculer.Clic\n    si est vide ( ZoneDT.Texte )\n        alors  mettre EtiquetteResultat.Texte à « Entre un nombre »\n        sinon  mettre EtiquetteResultat.Texte à ( ZoneDT.Texte ÷ 3 )\n\nquand BoutonEffacer.Clic\n    mettre ZoneDT.Texte à « »\n    mettre EtiquetteResultat.Texte à « »\n"),
 "A4": ("a4-plan-des-blocs.txt", "quand BoutonAllumer.Clic\n    appeler Bluetooth.EnvoyerTexte( « ON » )\nquand BoutonEteindre.Clic\n    appeler Bluetooth.EnvoyerTexte( « OFF » )\n\n(côté carte micro:bit, MakeCode)\nbluetooth.onUartDataReceived(serial.delimiters(Delimiters.NewLine), function () {\n    if (bluetooth.uartReadUntil(serial.delimiters(Delimiters.NewLine)) == \"ON\") { basic.showIcon(IconNames.Heart) } else { basic.clearScreen() }\n})\n"),
}
Q = lambda fr, ar: (fr, ar)
# scènes : (visuel, légende, commentaire) ; visuel = ("mb", kwargs) ou ("ph", kwargs)
OBJ = {
 "M1": dict(t=Q("Activité : explorer la carte sur le simulateur", "نشاط: استكشاف البطاقة على المحاكي"),
  steps=[Q("Ouvre le simulateur MakeCode micro:bit dans le navigateur (makecode.microbit.org), sans carte.", "افتح محاكي MakeCode micro:bit في المتصفح (makecode.microbit.org) دون بطاقة."), Q("Clique sur les boutons A et B, secoue la carte et change la température.", "اضغط على الزرّين A وB وهزّ البطاقة وغيّر الحرارة."), Q("Complète le tableau des composants de la fiche : capteur ou actionneur ?", "أكمل جدول المكوّنات في المذكرة: ملتقط أم محرّك؟")],
  res=Q("Tu sais nommer les composants et dire s'ils mesurent ou agissent.", "تعرف تسمية المكوّنات وتقول هل تقيس أم تفعل."),
  scenes=[(("mb", dict(tags=[(Q("Écran de 25 LED", "شاشة 25 صمّاما"), 280, 40, 280, 100), (Q("Bouton A", "الزر A"), 130, 330, 130, 280), (Q("Bouton B", "الزر B"), 430, 330, 430, 280)])), Q("La carte micro:bit", "بطاقة micro:bit"), Q("La carte micro:bit est un petit ordinateur. Elle a un écran de vingt-cinq LED et deux boutons, A et B.", "بطاقة micro:bit حاسوب صغير. لها شاشة من خمسة وعشرين صمّاما وزرّان A وB.")),
          (("mb", dict(a=True, pat="heart")), Q("Un capteur mesure", "الملتقط يقيس"), Q("Les boutons sont des capteurs : ils détectent un appui. L'écran est un actionneur : il affiche.", "الزرّان ملتقطان: يكشفان الضغط. والشاشة محرّك: تعرض.")),
          (("mb", dict(shake=True, temp=24)), Q("D'autres capteurs", "ملتقطات أخرى"), Q("La carte contient aussi un thermomètre et un accéléromètre qui détecte les secousses.", "تحتوي البطاقة أيضا على مقياس حرارة ومقياس تسارع يكشف الاهتزاز.")),
          (("mb", dict(sound=True, pat="happy")), Q("Les actionneurs agissent", "المحرّكات تفعل"), Q("Les LED et le haut-parleur sont des actionneurs : ils affichent et font du bruit.", "الصمّامات ومكبّر الصوت محرّكان: يعرضان ويُصدران صوتا."))]),
 "M2": dict(t=Q("Activité : un cœur quand j'appuie sur A", "نشاط: قلب عند الضغط على A"),
  steps=[Q("Dans MakeCode, ajoute le bloc « quand le bouton A est pressé ».", "في MakeCode أضف كتلة «عند ضغط الزر A»."), Q("Dedans : « afficher l'icône cœur », « mettre en pause 1000 ms », « effacer l'écran ».", "بداخلها: «اعرض أيقونة القلب» و«توقف 1000 مللي ثانية» و«امسح الشاشة»."), Q("Ajoute la même chose pour le bouton B avec une autre icône, puis teste sur le simulateur.", "أضف الشيء نفسه للزر B بأيقونة أخرى ثم اختبر على المحاكي.")],
  res=Q("Le cœur apparaît une seconde quand on appuie sur A.", "يظهر القلب ثانية واحدة عند الضغط على A."),
  scenes=[(("mb", dict()), Q("Écran éteint", "الشاشة مطفأة"), Q("Au départ, l'écran est éteint et le programme attend un événement.", "في البداية الشاشة مطفأة والبرنامج ينتظر حدثا.")),
          (("mb", dict(a=True, pat="heart")), Q("J'appuie sur A", "أضغط على A"), Q("Quand on appuie sur le bouton A, le bloc se déclenche et le cœur s'affiche.", "عند الضغط على الزر A تُطلق الكتلة ويظهر القلب.")),
          (("mb", dict(pat="blank")), Q("Pause puis effacer", "توقف ثم مسح"), Q("Après une seconde de pause, l'écran est effacé.", "بعد توقف ثانية واحدة تُمسح الشاشة.")),
          (("mb", dict(b=True, pat="happy")), Q("Et le bouton B", "والزر B"), Q("Le bouton B déclenche un autre bloc : un visage content.", "الزر B يطلق كتلة أخرى: وجه مبتهج."))]),
 "M3": dict(t=Q("Activité : l'alarme de température", "نشاط: إنذار الحرارة"),
  steps=[Q("Utilise « boucle toujours » avec « si température > 30 alors … sinon … ».", "استعمل «دائما» مع «إذا الحرارة > 30 فإن … وإلا …»."), Q("Si trop chaud : icône triste et un son. Sinon : visage content.", "إذا كان الجو حارا: أيقونة حزينة وصوت. وإلا: وجه مبتهج."), Q("Teste avec 20, 35 et une valeur limite (30). Note les résultats dans le tableau de tests.", "اختبر بـ20 و35 وقيمة حدّية (30). دوّن النتائج في جدول الاختبارات.")],
  res=Q("L'alarme sonne seulement au-dessus de 30 °C.", "يرنّ الإنذار فقط فوق 30 درجة."),
  scenes=[(("mb", dict(temp=20, pat="happy")), Q("20 °C : tout va bien", "20 درجة: كل شيء على ما يرام"), Q("À vingt degrés, la condition est fausse : la carte affiche un visage content.", "عند عشرين درجة الشرط خطأ: تعرض البطاقة وجها مبتهجا.")),
          (("mb", dict(temp=28, pat="happy")), Q("La température monte", "الحرارة ترتفع"), Q("La carte mesure en continu grâce à la boucle toujours.", "تقيس البطاقة باستمرار بفضل حلقة دائما.")),
          (("mb", dict(temp=35, pat="sad", sound=True)), Q("35 °C : alarme !", "35 درجة: إنذار!"), Q("Au-dessus de trente degrés, la condition est vraie : visage triste et son d'alarme.", "فوق ثلاثين درجة الشرط صحيح: وجه حزين وصوت إنذار.")),
          (("mb", dict(temp=30, pat="happy")), Q("Valeur limite", "قيمة حدّية"), Q("À trente degrés pile, la condition « supérieur à 30 » est fausse. Il faut toujours tester les limites.", "عند ثلاثين درجة بالضبط يكون شرط «أكبر من 30» خطأ. يجب دائما اختبار الحدود."))]),
 "M4": dict(t=Q("Mini-projet : le dé électronique", "مشروع صغير: النرد الإلكتروني"),
  steps=[Q("Écris le cahier des charges : entrée = secousse, traitement = nombre au hasard de 1 à 6, sortie = affichage.", "اكتب كراس الشروط: المدخل = الاهتزاز والمعالجة = عدد عشوائي من 1 إلى 6 والمخرج = العرض."), Q("Programme : « quand la carte est secouée », « mettre dé à nombre aléatoire entre 1 et 6 », « afficher le nombre dé ».", "برمج: «عند هزّ البطاقة» و«اجعل نرد = عدد عشوائي بين 1 و6» و«اعرض العدد نرد»."), Q("Teste plusieurs lancers puis présente ton dé à la classe.", "اختبر عدة رميات ثم اعرض نردك على القسم.")],
  res=Q("Chaque secousse affiche un nombre de 1 à 6.", "كل اهتزاز يعرض عددا من 1 إلى 6."),
  scenes=[(("mb", dict()), Q("Le cahier des charges", "كراس الشروط"), Q("Notre objet : un dé électronique. Entrée : la secousse. Sortie : un nombre de un à six.", "شيئنا: نرد إلكتروني. المدخل: الاهتزاز. المخرج: عدد من واحد إلى ستة.")),
          (("mb", dict(shake=True, pat="3")), Q("Première secousse : 3", "الاهتزاز الأول: 3"), Q("On secoue la carte : le programme choisit un nombre au hasard et l'affiche.", "نهزّ البطاقة: يختار البرنامج عددا عشوائيا ويعرضه.")),
          (("mb", dict(shake=True, pat="6")), Q("Deuxième secousse : 6", "الاهتزاز الثاني: 6"), Q("Une autre secousse, un autre nombre : le hasard donne des valeurs différentes.", "اهتزاز آخر وعدد آخر: العشوائية تعطي قيما مختلفة.")),
          (("mb", dict(shake=True, pat="1")), Q("Je teste plusieurs fois", "أختبر عدة مرات"), Q("On teste plusieurs lancers pour vérifier que les nombres restent entre un et six.", "نختبر عدة رميات للتأكد من أن الأعداد تبقى بين واحد وستة."))]),
 "A1": dict(t=Q("Activité : l'interface du convertisseur", "نشاط: واجهة المحوّل"),
  steps=[Q("Dans App Inventor (appinventor.mit.edu), ouvre un nouveau projet et la fenêtre Concepteur.", "في App Inventor (appinventor.mit.edu) افتح مشروعا جديدا ونافذة المصمّم."), Q("Glisse une étiquette (titre), une zone de texte (dinars), un bouton « Calculer » et une étiquette de résultat : 5 composants au plus.", "اسحب عنوانا وخانة نص (دينار) وزرّ «احسب» وعنوان نتيجة: 5 مكوّنات على الأكثر."), Q("Renomme chaque composant clairement (ZoneDT, BoutonCalculer…).", "أعد تسمية كل مكوّن بوضوح (ZoneDT وBoutonCalculer …).")],
  res=Q("L'écran du convertisseur est dessiné et prêt à être programmé.", "شاشة المحوّل مرسومة وجاهزة للبرمجة."),
  scenes=[(("ph", dict(widgets=[])), Q("Un écran vide", "شاشة فارغة"), Q("Dans App Inventor, on commence par un écran vide : le Concepteur.", "في App Inventor نبدأ بشاشة فارغة: المصمّم.")),
          (("ph", dict(widgets=[("label", Q("Convertisseur DT → €", "محوّل دينار ← أورو"), 18), ("textbox", Q("Montant en DT", "المبلغ بالدينار"), True)])), Q("Étiquette et zone de texte", "عنوان وخانة نص"), Q("On glisse une étiquette pour le titre et une zone de texte pour le montant.", "نسحب عنوانا للعنوان وخانة نص للمبلغ.")),
          (("ph", dict(widgets=[("label", Q("Convertisseur DT → €", "محوّل دينار ← أورو"), 18), ("textbox", Q("Montant en DT", "المبلغ بالدينار"), True), ("button", Q("Calculer", "احسب")), ("label", Q("Résultat", "النتيجة"), 22)])), Q("Bouton et résultat", "زر ونتيجة"), Q("On ajoute le bouton Calculer et une étiquette pour afficher le résultat. Quatre composants : l'interface reste simple.", "نضيف زرّ احسب وعنوانا لعرض النتيجة. أربعة مكوّنات: الواجهة تبقى بسيطة.")),
          (("ph", dict(widgets=[("label", Q("Convertisseur DT → €", "محوّل دينار ← أورو"), 18), ("textbox", Q("Montant en DT", "المبلغ بالدينار"), True), ("button", Q("Calculer", "احسب")), ("label", Q("Résultat", "النتيجة"), 22)], status=Q("Noms : ZoneDT · BoutonCalculer · EtiquetteResultat", "الأسماء: ZoneDT · BoutonCalculer · EtiquetteResultat"))), Q("Des noms clairs", "أسماء واضحة"), Q("On renomme chaque composant avec un nom clair pour s'y retrouver dans les blocs.", "نعيد تسمية كل مكوّن باسم واضح لنتمكن من التعرف عليه في الكتل."))]),
 "A2": dict(t=Q("Activité : faire calculer le bouton", "نشاط: جعل الزر يحسب"),
  steps=[Q("Passe à l'onglet Blocs et prends « quand BoutonCalculer.Clic ».", "انتقل إلى لسان الكتل وخذ «عند النقر على BoutonCalculer»."), Q("Dedans : mettre le texte de l'étiquette à (montant ÷ 3) (taux fictif : 1 € = 3 DT).", "بداخلها: اجعل نص العنوان = (المبلغ ÷ 3) (سعر خيالي: 1 أورو = 3 دنانير)."), Q("Ajoute le bouton Effacer qui vide la zone de texte et le résultat.", "أضف زرّ المسح الذي يُفرغ خانة النص والنتيجة.")],
  res=Q("Un clic sur Calculer affiche le montant en euros.", "نقرة على احسب تعرض المبلغ بالأورو."),
  scenes=[(("ph", dict(widgets=[("label", Q("Convertisseur DT → €", "محوّل دينار ← أورو"), 18), ("textbox", Q("30", "30")), ("button", Q("Calculer", "احسب")), ("label", Q("Résultat", "النتيجة"), 22)])), Q("J'écris 30", "أكتب 30"), Q("L'utilisateur écrit trente dinars dans la zone de texte.", "يكتب المستعمل ثلاثين دينارا في خانة النص.")),
          (("ph", dict(widgets=[("label", Q("Convertisseur DT → €", "محوّل دينار ← أورو"), 18), ("textbox", Q("30", "30")), ("button", Q("Calculer", "احسب"), True), ("label", Q("Résultat", "النتيجة"), 22)])), Q("Je touche Calculer", "ألمس احسب"), Q("Il touche le bouton : l'événement Clic déclenche le bloc.", "يلمس الزر: حدث النقر يطلق الكتلة.")),
          (("ph", dict(widgets=[("label", Q("Convertisseur DT → €", "محوّل دينار ← أورو"), 18), ("textbox", Q("30", "30")), ("button", Q("Calculer", "احسب")), ("label", Q("10 €", "10 €"), 26)])), Q("Le résultat : 10 €", "النتيجة: 10 €"), Q("Le bloc divise le montant par trois, avec un taux fictif, et affiche dix euros.", "تقسم الكتلة المبلغ على ثلاثة بسعر خيالي وتعرض عشرة أورو.")),
          (("ph", dict(widgets=[("label", Q("Convertisseur DT → €", "محوّل دينار ← أورو"), 18), ("textbox", Q("Montant en DT", "المبلغ بالدينار"), True), ("button", Q("Calculer", "احسب")), ("label", Q("Résultat", "النتيجة"), 22)])), Q("Le bouton Effacer", "زر المسح"), Q("Le bouton Effacer vide la zone de texte et le résultat pour recommencer.", "زر المسح يُفرغ خانة النص والنتيجة للبدء من جديد."))]),
 "A3": dict(t=Q("Activité : tester puis générer l'application", "نشاط: اختبار التطبيقة ثم توليدها"),
  steps=[Q("Connecte l'émulateur ou l'application compagnon et teste trois cas : valeur normale, zone vide, grand nombre.", "اربط المحاكي أو التطبيقة المرافقة واختبر ثلاث حالات: قيمة عادية وخانة فارغة وعدد كبير."), Q("Corrige le cas de la zone vide avec un message « Entre un nombre ».", "صحّح حالة الخانة الفارغة برسالة «أدخل عددا»."), Q("Menu Construire : génère l'application (fichier) puis installe-la sur le téléphone. Aucune donnée personnelle réelle.", "قائمة بناء: ولّد التطبيقة (ملف) ثم ثبّتها على الهاتف. دون أي معطيات شخصية حقيقية.")],
  res=Q("Le journal de test est rempli et l'application est générée.", "سجل الاختبار مملوء والتطبيقة مولَّدة."),
  scenes=[(("ph", dict(widgets=[("label", Q("Convertisseur DT → €", "محوّل دينار ← أورو"), 18), ("textbox", Q("30", "30")), ("button", Q("Calculer", "احسب")), ("label", Q("10 €", "10 €"), 26)], status=Q("Test 1 : 30 → 10 € ✔", "الاختبار 1: 30 ← 10 € ✔"))), Q("Test 1 : valeur normale", "الاختبار 1: قيمة عادية"), Q("Premier test : trente dinars donnent dix euros. Résultat conforme.", "الاختبار الأول: ثلاثون دينارا تعطي عشرة أورو. النتيجة مطابقة.")),
          (("ph", dict(widgets=[("label", Q("Convertisseur DT → €", "محوّل دينار ← أورو"), 18), ("textbox", Q("Montant en DT", "المبلغ بالدينار"), True), ("button", Q("Calculer", "احسب"), True), ("label", Q("Erreur !", "خطأ!"), 24)], status=Q("Test 2 : zone vide ✘", "الاختبار 2: خانة فارغة ✘"))), Q("Test 2 : zone vide", "الاختبار 2: خانة فارغة"), Q("Deuxième test : zone vide. Le résultat est incorrect, on a trouvé un bug.", "الاختبار الثاني: خانة فارغة. النتيجة غير صحيحة، وجدنا خطأ برمجيا.")),
          (("ph", dict(widgets=[("label", Q("Convertisseur DT → €", "محوّل دينار ← أورو"), 18), ("textbox", Q("Montant en DT", "المبلغ بالدينار"), True), ("button", Q("Calculer", "احسب")), ("label", Q("Entre un nombre", "أدخل عددا"), 20)], status=Q("Test 2 corrigé ✔", "الاختبار 2 بعد التصحيح ✔"))), Q("Je corrige", "أصحّح"), Q("On ajoute un test : si la zone est vide, on affiche un message. Puis on reteste.", "نضيف اختبارا: إذا كانت الخانة فارغة نعرض رسالة. ثم نعيد الاختبار.")),
          (("ph", dict(widgets=[("image", "📦"), ("label", Q("Application générée", "التطبيقة مولَّدة"), 20), ("label", Q("Construire → fichier .apk", "بناء ← ملف .apk"), 16)])), Q("Générer et installer", "التوليد والتثبيت"), Q("Enfin, le menu Construire génère un fichier que l'on installe sur le téléphone.", "أخيرا تولّد قائمة بناء ملفا نثبّته على الهاتف."))]),
 "A4": dict(t=Q("Mini-projet : commander la carte depuis le téléphone", "مشروع صغير: التحكم في البطاقة من الهاتف"),
  steps=[Q("Dessine le schéma : application → Bluetooth → carte. Distingue l'interface de communication et la technologie.", "ارسم المخطط: تطبيقة ← بلوتوث ← بطاقة. ميّز بين واجهة الاتصال والتقنية."), Q("Dans App Inventor : deux boutons, Allumer et Éteindre, qui envoient « ON » ou « OFF » par Bluetooth.", "في App Inventor: زرّان «تشغيل» و«إطفاء» يرسلان «ON» أو «OFF» عبر البلوتوث."), Q("Sur la carte (MakeCode) : afficher un cœur si le message est ON, effacer sinon. Sans matériel : simulation.", "على البطاقة (MakeCode): اعرض قلبا إذا كانت الرسالة ON وإلا امسح. دون عتاد: محاكاة.")],
  res=Q("Le bouton du téléphone allume ou éteint les LED de la carte.", "زر الهاتف يشغّل صمّامات البطاقة أو يطفئها."),
  scenes=[(("ph", dict(widgets=[("label", Q("Télécommande", "جهاز التحكم"), 20), ("status", Q("Bluetooth : connecté", "البلوتوث: متصل"), "#2e9e5b"), ("button", Q("Allumer", "تشغيل")), ("button", Q("Éteindre", "إطفاء"))], title=("Télécommande", "جهاز التحكم"))), Q("L'application", "التطبيقة"), Q("L'application du téléphone a deux boutons et affiche l'état de la liaison Bluetooth.", "لتطبيقة الهاتف زرّان وتعرض حالة رابط البلوتوث.")),
          (("ph", dict(widgets=[("label", Q("Télécommande", "جهاز التحكم"), 20), ("status", Q("Bluetooth : connecté", "البلوتوث: متصل"), "#2e9e5b"), ("button", Q("Allumer", "تشغيل"), True), ("button", Q("Éteindre", "إطفاء"))], title=("Télécommande", "جهاز التحكم"))), Q("Je touche Allumer", "ألمس تشغيل"), Q("Le bouton envoie la commande ON par Bluetooth.", "يرسل الزر الأمر ON عبر البلوتوث.")),
          (("mb", dict(pat="heart", link=True)), Q("La carte reçoit ON", "البطاقة تستلم ON"), Q("La carte reçoit le message et affiche un cœur : l'actionneur agit.", "تستلم البطاقة الرسالة وتعرض قلبا: المحرّك يفعل.")),
          (("mb", dict(pat="blank", link=True)), Q("Éteindre", "إطفاء"), Q("Le bouton Éteindre envoie OFF : la carte efface l'écran.", "زر إطفاء يرسل OFF: تمسح البطاقة الشاشة."))]),
}
def visual(spec, lang):
    kind, kw = spec; kw = dict(kw)
    if kind == "mb":
        if "tags" in kw: kw["tags"] = kw["tags"]
        return microbit(lang=lang, **kw)
    ws = kw.pop("widgets"); return phone(ws, lang=lang, **kw)
def pp(p): return p

UI = dict(act=("Activité", "النشاط"), res=("Résultat attendu", "النتيجة المنتظرة"), video=("Vidéo explicative", "فيديو توضيحي"), files=("Ressources à télécharger", "موارد للتحميل"),
          zip=("⬇ Télécharger les ressources (.zip)", "⬇ تحميل الموارد (.zip)"), note=("Tout est simulé : aucun matériel ni compte n'est nécessaire. Les vidéos sont des animations silencieuses ; proposition non officielle.", "كل شيء محاكى: لا عتاد ولا حساب مطلوب. الفيديوهات رسوم متحركة صامتة؛ اقتراح غير رسمي."), play=("▶ Regarder la vidéo explicative", "▶ شاهد الفيديو التوضيحي"), shot=("Capture d'écran : ce que l'on va réaliser", "لقطة شاشة: ما سننجزه"),
          inzip_m=("Dans le fichier : le programme MakeCode (à coller en mode JavaScript, quand il existe), les images de la carte à chaque étape (français et arabe) et une notice.", "في الملف: برنامج MakeCode (يُلصق في وضع JavaScript عند وجوده) وصور البطاقة في كل مرحلة (بالفرنسية والعربية) ومذكرة."),
          inzip_a=("Dans le fichier : le plan des blocs (quand il existe), les images des écrans (PNG, importables dans App Inventor) et une notice.", "في الملف: مخطط الكتل (عند وجوده) وصور الشاشات (PNG قابلة للاستيراد في App Inventor) ومذكرة."))
def export():
    from theorie_core import P, FRM
    ui = {k: P(*v) for k, v in UI.items()}
    d = {k: dict(t=P(*v["t"]), steps=[P(*s) for s in v["steps"]], res=P(*v["res"]), video=dict(ar=f"videos/objets/{k}-ar.mp4", fr=f"videos/objets/{k}-fr.mp4"), img=[f"objets/captures/{k}-ar.jpg", f"objets/captures/{k}-fr.jpg"], zip=f"objets/ressources/{k}.zip",
                 code=(O_CODE[k][0] if k in O_CODE else None)) for k, v in OBJ.items()}
    return dict(ui=ui, items=d), dict(FRM)
O_CODE = CODE
