"""Contenu du « cahier de l'élève » : une fiche à coller dans le cahier pour chaque séance de programmation (6 en 7e, 10 en 8e, 14 en 9e).
Une fiche = en-tête (nom, classe, date), objectif, phrases à trous (d'après les notions de la séance : cahier_cards.py), TRACE ÉCRITE de la séance
(tableau, schéma ou carte à compléter : c'est la « trace écrite » prévue par la répartition annuelle, seances.py), script « à moitié terminé »
(l'activité principale de la séance du planning, avec des blocs et des nombres à écrire ; à finir en classe sur l'ordinateur), à retenir et « Je sais… ».
Les textes sont des couples (français, arabe) ; {{mot}} = mot à écrire par l'élève (visible dans le corrigé seulement).
SPEC[(année, séance)] = dict(form=[blocs de la trace écrite], script=SCR(...) ou None, fill=[phrases] (sinon : celles des notions), retain=[phrases] (sinon : celles des notions))."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from cahier_cards import L
from activites_data1 import BLOCKS
import activites_specs as SP
import cahier_img as CI
from activites_img import b, R, F, IF, IFE, UNTIL, WU, LBL

# ----------------------------------------------------------------------------- briques
def bk(key, fr=None, ar=None):
    cat, f, a = BLOCKS[key]; return dict(blk=(cat, fr or f, ar or a))
def BLK(cat, fr, ar): return dict(blk=(cat, fr, ar))
def BLKS(*items): return dict(blks=list(items))
def T(cols, rows, w=None, first=False, rh=None): return dict(k="table", cols=cols, rows=rows, w=w, first=first, rh=rh)
def CARD(fields, w=(1, 2.4)): return dict(k="card", fields=fields, w=w)       # fields : (étiquette, valeur | None, nombre de lignes à écrire)
def FLOW(items): return dict(k="flow", items=items)
def COLS(a, c, w=(1, 1)): return dict(k="cols", items=[a, c], w=w)
def SVGB(kind, **kw): return dict(k="svg", kind=kind, **kw)
def CARDROW(items, legend=None): return dict(k="cards", items=items, legend=legend)
def TXT(pair): return dict(k="text", t=pair)
def SCR(act, parts, q=None, note=None): return dict(act=act, parts=parts, q=q, note=note)
def one(act, g=(), over=None, cnt=None, cond=None, q=None, note=None, nomask=False):
    """script d'une activité du site : version complète et version à moitié terminée"""
    full = SP.SPECS[act]["script"]
    return SCR(act, [dict(full=full, masked=full if nomask else CI.mask(full, g, over, cnt, cond))], q, note)
def ov(fr, ar): return (fr, ar)
DOT = "………"
M = lambda s: L(s)                       # isole un nombre négatif ou un couple dans un texte arabe

# ----------------------------------------------------------------------------- les fiches
SPEC = {}

# ============================================================================= 7e
SPEC[("7", 22)] = dict(
 form=[
  CARD([(("Problème", "المشكل"), ("Conduire le robot de la case de départ jusqu'à l'étoile ★.", "إيصال الروبوت من خانة الانطلاق إلى النجمة ★."), 1),
        (("Données utiles", "المعطيات المفيدة"), ("{{la grille, la case de départ, les cartes-instructions}}", "{{الشبكة وخانة الانطلاق وبطاقات التعليمات}}"), 1),
        (("Résultat attendu", "النتيجة المنتظرة"), ("Le robot {{arrive sur l'étoile}}.", "{{يصل الروبوت إلى النجمة}}."), 1),
        (("Étapes (dans l'ordre)", "المراحل (بالترتيب)"), None, 3)]),
  COLS(SVGB("robot"), dict(k="stack", items=[
        TXT(("Écris les cartes qui mènent le robot jusqu'à ★ (il regarde vers le haut au départ).  ⬆ avancer d'une case · ⟳ tourner à droite · ⟲ tourner à gauche", "اكتب البطاقات التي توصل الروبوت إلى ★ (ينظر إلى الأعلى عند الانطلاق).  ⬆ تقدّم خانة · ⟳ استدر يمينا · ⟲ استدر يسارا")),
        CARDROW([("⬆", True), ("⬆", True), ("⟳", False), ("⬆", False), ("⬆", False), ("⟲", False), ("⬆", False)])]), w=(4, 6)),
 ],
 script=None)

SPEC[("7", 23)] = dict(
 form=[COLS(SVGB("iface"), T([("N°", "الرقم"), ("Nom de la zone", "اسم المنطقة")],
        [[("1", "1"), ("{{Barre de menus}}", "{{شريط القوائم}}")], [("2", "2"), ("{{Onglets Code, Costumes, Sons}}", "{{تبويبات الأكواد والأزياء والأصوات}}")], [("3", "3"), ("{{Palette de blocs}}", "{{لوحة الكتل}}")],
         [("4", "4"), ("{{Zone des scripts}}", "{{منطقة السكربتات}}")], [("5", "5"), ("{{Scène}}", "{{المنصة}}")], [("6", "6"), ("{{Drapeau vert et bouton Stop}}", "{{العلم الأخضر وزر الإيقاف}}")],
         [("7", "7"), ("{{Liste des lutins}}", "{{قائمة اللاعبين}}")], [("8", "8"), ("{{Arrière-plan (décor)}}", "{{الخلفية (الديكور)}}")]], w=(1, 5), first=True), w=(7, 5))],
 script=one(1, g=(1,), note=(("Quel bloc fait avancer le lutin de 100 pas ? Dessine-le (ou cherche-le dans la palette) puis essaie dans Scratch.", "أي كتلة تُقدّم اللاعب 100 خطوة؟ ارسمها (أو ابحث عنها في لوحة الكتل) ثم جرّب في سكراتش."))))

SPEC[("7", 24)] = dict(
 form=[
  T([("Bloc événement", "كتلة الحدث"), ("Effet", "الأثر")],
    [[bk("flag"), ("{{Le script démarre}} quand on clique sur le drapeau vert.", "{{يبدأ السكربت}} عند النقر على العلم الأخضر.")],
     [bk("arrowr"), ("Le script démarre quand on {{appuie sur la flèche droite}}.", "يبدأ السكربت عند {{ضغط السهم الأيمن}}.")],
     [bk("click"), ("Le script démarre quand on {{clique sur le lutin}}.", "يبدأ السكربت عند {{النقر على اللاعب}}.")],
     [bk("recv"), ("Le script démarre quand le lutin {{reçoit le message}}.", "يبدأ السكربت عندما {{يستلم اللاعب الرسالة}}.")]], w=(5, 6)),
  COLS(SVGB("plane", pts=[("A", -120, 60), ("B", 90, -90), ("C", 0, 120)]),
       T([("Point", "النقطة"), ("x", "س"), ("y", "ص")], [[("A", "A"), (M("{{−120}}"), M("{{−120}}")), ("{{60}}", "{{60}}")], [("B", "B"), ("{{90}}", "{{90}}"), (M("{{−90}}"), M("{{−90}}"))], [("C", "C"), ("{{0}}", "{{0}}"), ("{{120}}", "{{120}}")]], first=True), w=(6, 4)),
 ],
 script=one(9, over={1: ov("ajouter ……… à x", "غيّر س بمقدار ………")}, note=(("Complète le nombre pour que le lutin avance vers la droite quand on appuie sur la flèche, puis essaie.", "أكمل العدد ليتقدم اللاعب نحو اليمين عند الضغط على السهم ثم جرّب."))))

SPEC[("7", 25)] = dict(
 form=[T([("", ""), ("« répéter n fois »", "«كرّر n مرات»"), ("« répéter indéfiniment »", "«كرّر باستمرار»")],
         [[("Nombre de tours", "عدد الدورات"), ("{{connu : n}}", "{{معلوم: n}}"), ("{{non limité}}", "{{غير محدود}}")],
          [("Elle s'arrête…", "تتوقف…"), ("{{après n tours}}", "{{بعد n دورات}}"), ("{{quand on clique sur Stop}}", "{{عند الضغط على زر الإيقاف}}")],
          [("Exemple d'emploi", "مثال للاستعمال"), ("{{dessiner un carré}}", "{{رسم مربع}}"), ("{{surveiller une collision}}", "{{مراقبة اصطدام}}")]], w=(3, 4, 4), first=True)],
 script=one(10, g=(1,), cnt={0: DOT}, over={3: ov("tourner ↻ de ……… degrés", "استدر يمينا ……… درجة")},
            note=(("Complète le script pour dessiner un carré (4 côtés de 100 pas), puis essaie.", "أكمل السكربت لرسم مربع (4 أضلاع طول كل منها 100 خطوة) ثم جرّب."))))

SPEC[("7", 26)] = dict(
 form=[T([("", ""), ("« si … alors »", "«إذا … فإن»"), ("« si … alors … sinon »", "«إذا … فإن … وإلا»")],
         [[("Nombre de chemins", "عدد الطرق"), ("{{1}}", "{{1}}"), ("{{2}}", "{{2}}")],
          [("Si la condition est fausse…", "إذا كان الشرط خطأ…"), ("{{rien ne se passe}}", "{{لا يحدث شيء}}"), ("{{les blocs du « sinon » s'exécutent}}", "{{تُنفَّذ كتل «وإلا»}}")],
          [("Exemple", "مثال"), ("{{si touche la pomme alors jouer un son}}", "{{إذا لمست التفاحة فشغّل صوتا}}"),
           ("{{si touche la pomme alors dire « Miam ! » sinon dire « Je cherche… »}}", "{{إذا لمست التفاحة فقل «لذيذ!» وإلا فقل «أبحث…»}}")]], w=(3, 4, 5), first=True)],
 script=one(14, cond={0: ov("touche ………… ?", "هل تلمس …………؟")}, note=(("Écris la condition qui permet de jouer le son quand le chat touche la pomme, puis essaie.", "اكتب الشرط الذي يُشغّل الصوت عندما تلمس القطة التفاحة ثم جرّب."))))

SPEC[("7", 27)] = dict(
 form=[
  CARD([(("Titre du projet", "عنوان المشروع"), None, 1), (("Personnages et décors", "الشخصيات والخلفيات"), None, 1), (("Événements utilisés", "الأحداث المستعملة"), None, 1),
        (("Ce qui se répète (boucle)", "ما يتكرر (حلقة)"), None, 1), (("Condition utilisée", "الشرط المستعمل"), None, 1), (("Étapes de réalisation", "مراحل الإنجاز"), None, 2)]),
  T([("Test", "الاختبار"), ("Résultat observé", "النتيجة الملاحظة"), ("Correction", "التصحيح")],
    [[("J'appuie sur le drapeau vert", "أضغط على العلم الأخضر"), ("Le lutin ne bouge pas", "لا يتحرك اللاعب"), ("{{Ajouter « quand le drapeau vert est cliqué »}}", "{{إضافة «عند النقر على العلم الأخضر»}}")], [None, None, None], [None, None, None], [None, None, None]], w=(4, 4, 5)),
 ],
 script=None,
 fill=None)

# ============================================================================= 8e
SPEC[("8", 18)] = dict(
 form=[
  FLOW([("start", ("Début", "البداية")), ("box", ("{{Montrer}} le lutin", "{{أظهر}} اللاعب")), ("box", ("{{Dire}} « Bonjour ! »", "{{قل}} «مرحبا!»")),
        ("box", ("{{Avancer}} de 100 pas", "{{تحرك}} 100 خطوة")), ("box", ("{{Cacher}} le lutin", "{{أخفِ}} اللاعب")), ("end", ("Fin", "النهاية"))]),
  CARD([(("Mon jeu « attrape-objets » : sous-problème 1", "لعبتي «التقاط الأشياء»: المشكل الفرعي 1"), None, 1), (("Sous-problème 2", "المشكل الفرعي 2"), None, 1), (("Sous-problème 3", "المشكل الفرعي 3"), None, 1)], w=(1, 1.6)),
 ],
 script=one(58, g=(2, 4), note=(("Traduis le diagramme en blocs : complète les deux blocs manquants, puis essaie.", "ترجم المخطط إلى كتل: أكمل الكتلتين الناقصتين ثم جرّب."))))

SPEC[("8", 19)] = dict(
 form=[
  T([("Structure", "البنية"), ("Rôle", "الدور"), ("Exemple de bloc", "مثال لكتلة")],
    [[("Séquence", "التسلسل"), ("{{exécuter les blocs dans l'ordre}}", "{{تنفيذ الكتل بالترتيب}}"), bk("move")],
     [("Événement", "الحدث"), ("{{déclencher un script}}", "{{إطلاق سكربت}}"), bk("flag")],
     [("Boucle", "الحلقة"), ("{{répéter des blocs}}", "{{تكرار كتل}}"), bk("repeat")],
     [("Condition", "الشرط"), ("{{choisir selon vrai ou faux}}", "{{الاختيار حسب صحيح أو خطأ}}"), bk("if")]], w=(3, 6, 5), first=True),
  T([("Symbole", "الرمز"), ("Signification", "المعنى"), ("Vrai ou faux ?", "صحيح أم خطأ؟")],
    [[("<", "<"), ("{{plus petit que}}", "{{أصغر من}}"), ("« 2 < 5 » : {{vrai}}", "«2 < 5»: {{صحيح}}")], [(">", ">"), ("{{plus grand que}}", "{{أكبر من}}"), ("« 2 > 5 » : {{faux}}", "«2 > 5»: {{خطأ}}")], [("=", "="), ("{{égal à}}", "{{يساوي}}"), ("« 3 = 3 » : {{vrai}}", "«3 = 3»: {{صحيح}}")]], w=(2, 5, 5), first=True),
 ],
 script=one(56, nomask=True, q=[(("Combien de fois le lutin avance-t-il ? {{4}} fois", "كم مرة يتقدم اللاعب؟ {{4}} مرات"), ), (("De combien de pas avance-t-il en tout ? {{320}} pas", "كم خطوة يتقدم في المجموع؟ {{320}} خطوة"), ),
                                  (("Que dit-il à la fin ? « {{Fini !}} »", "ماذا يقول في النهاية؟ «{{انتهيت!}}»"), )]))

SPEC[("8", 20)] = dict(
 form=[CARD([(("Nom de la variable", "اسم المتغير"), ("{{score}}", "{{النقاط}}"), 1), (("Rôle", "دوره"), ("{{compter les points du joueur}}", "{{عدّ نقاط اللاعب}}"), 1),
             (("Valeur au départ", "القيمة عند البداية"), ("{{0}}", "{{0}}"), 1), (("Quand augmente-t-elle ?", "متى تزداد؟"), ("{{quand le lutin touche la pomme}}", "{{عندما يلمس اللاعب التفاحة}}"), 1),
             (("Blocs utilisés", "الكتل المستعملة"), BLKS(("va", "mettre score à 0", "اجعل النقاط = 0"), ("va", "ajouter 1 à score", "غيّر النقاط بمقدار 1")), 0)])],
 script=one(18, over={1: ov("mettre score à ………", "اجعل النقاط = ………"), 2: ov("ajouter ……… à score", "غيّر النقاط بمقدار ………")},
            note=(("Complète les deux blocs de la variable, puis essaie : le score doit monter de 1 à chaque pomme attrapée.", "أكمل كتلتي المتغير ثم جرّب: يجب أن ترتفع النقاط بواحد عند كل تفاحة."))))

SPEC[("8", 21)] = dict(
 form=[T([("Bloc du programme", "كتلة البرنامج"), ("Explication (commentaire)", "الشرح (تعليق)")],
         [[BLK("va", "mettre score à 0", "اجعل النقاط = 0"), ("{{Initialise le score}}", "{{يهيّئ النقاط}}")], [BLK("mv", "ajouter -5 à y", "غيّر ص بمقدار -5"), ("{{Fait tomber le fruit}}", "{{يُنزل الفاكهة}}")],
          [BLK("ct", "si touche le panier ?", "إذا لمس السلة؟"), ("{{Teste si le fruit est attrapé}}", "{{يختبر هل التُقطت الفاكهة}}")],
          [BLK("mv", "aller à x : (aléatoire) y : 170", "اذهب إلى س: (عشوائي) ص: 170"), ("{{Remet le fruit en haut, à un endroit pris au hasard}}", "{{يعيد الفاكهة إلى الأعلى في مكان عشوائي}}")]], w=(6, 6)),
       CARD([(("Question posée au joueur", "السؤال المطروح على اللاعب"), None, 1), (("Réponse attendue", "الإجابة المنتظرة"), None, 1)], w=(1, 2))],
 script=one(21, cond={0: ov("touche ………… ?", "هل تلمس …………؟")}, over={4: ov("aller à x : ……………… y : 170", "اذهب إلى س: ……………… ص: 170")},
            note=(("Complète la condition et la position de départ du fruit (au hasard), puis essaie.", "أكمل الشرط وموضع بداية الفاكهة (عشوائيا) ثم جرّب."))))

SPEC[("8", 22)] = dict(
 form=[CARD([(("Nom du module", "اسم الوحدة"), ("{{carré}}", "{{مربع}}"), 1), (("Rôle", "دورها"), ("{{dessiner un carré}}", "{{رسم مربع}}"), 1),
             (("Blocs contenus", "الكتل التي تحتويها"), ("{{répéter 4 fois [avancer de 60 pas, tourner de 90 degrés]}}", "{{كرّر 4 مرات [تحرك 60 خطوة، استدر يمينا 90 درجة]}}"), 1),
             (("Où l'appelle-t-on ?", "أين نستدعيها؟"), ("{{dans le script principal, sous « quand le drapeau vert est cliqué »}}", "{{في السكربت الرئيسي تحت «عند النقر على العلم الأخضر»}}"), 1),
             (("Avantage", "الفائدة"), ("{{on écrit les blocs une seule fois}}", "{{نكتب الكتل مرة واحدة فقط}}"), 1)])],
 script=one(59, g=(7,), over={0: ov("définir ………", "عرّف ………")}, note=(("Donne un nom au module, puis appelle-le une deuxième fois (bloc manquant). Essaie : deux carrés doivent apparaître.", "أعطِ الوحدة اسما ثم استدعها مرة ثانية (الكتلة الناقصة). جرّب: يجب أن يظهر مربعان."))))

SPEC[("8", 23)] = dict(
 form=[T([("Appel du module", "استدعاء الوحدة"), ("Figure dessinée", "الشكل المرسوم"), ("Angle à chaque coin", "الزاوية عند كل ركن")],
         [[BLK("my", "polygone 3", "مضلع 3"), ("{{un triangle}}", "{{مثلث}}"), ("{{120}}°", "{{120}}°")], [BLK("my", "polygone 4", "مضلع 4"), ("{{un carré}}", "{{مربع}}"), ("{{90}}°", "{{90}}°")],
          [BLK("my", "polygone 5", "مضلع 5"), ("{{un pentagone}}", "{{مخمّس}}"), ("{{72}}°", "{{72}}°")], [BLK("my", "polygone 6", "مضلع 6"), ("{{un hexagone}}", "{{مسدّس}}"), ("{{60}}°", "{{60}}°")]], w=(4, 5, 4)),
       TXT(("L'angle de rotation vaut 360 ÷ {{côtés}} (le paramètre du module).", "زاوية الدوران = 360 ÷ {{الأضلاع}} (معامل الوحدة)."))],
 script=one(60, over={2: ov("tourner ↻ de (……… ÷ côtés) degrés", "استدر يمينا (……… ÷ أضلاع) درجة")},
            note=(("Complète la formule de l'angle pour que le module dessine n'importe quel polygone régulier, puis essaie.", "أكمل صيغة الزاوية لترسم الوحدة أي مضلع منتظم ثم جرّب."))))

SPEC[("8", 24)] = dict(
 form=[T([("Test effectué", "الاختبار المنجز"), ("Résultat attendu", "النتيجة المنتظرة"), ("Résultat obtenu", "النتيجة المحصَّلة"), ("Correction", "التصحيح")],
         [[("Je clique sur le drapeau vert", "أضغط على العلم الأخضر"), ("Le lutin avance de 100 pas", "يتقدم اللاعب 100 خطوة"), ("Il ne bouge pas", "لا يتحرك"), ("{{Ajouter « quand le drapeau vert est cliqué »}}", "{{إضافة «عند النقر على العلم الأخضر»}}")],
          [None, None, None, None], [None, None, None, None], [None, None, None, None]], w=(4, 4, 4, 5))],
 script=SCR(57, [dict(t=None, full=SP.SPECS[57]["script"][0], masked=SP.SPECS[57]["script"][0]), dict(t=None, full=SP.SPECS[57]["script"][1], masked=None)],
            note=(("Entoure les erreurs du premier script, puis écris le script corrigé dans le cadre (les blocs viennent de la palette).", "حدّد الأخطاء في السكربت الأول ثم اكتب السكربت المصحَّح في الإطار (الكتل من لوحة الكتل)."))))

SPEC[("8", 25)] = dict(
 form=[T([("Amélioration", "التحسين"), ("Pourquoi ?", "لماذا؟")],
         [[("{{Remplacer 4 blocs identiques par « répéter 4 fois »}}", "{{تعويض 4 كتل متماثلة بـ«كرّر 4 مرات»}}"), ("{{le script est plus court et plus facile à modifier}}", "{{السكربت أقصر وأسهل تعديلا}}")],
          [("{{Regrouper des blocs dans un module}}", "{{جمع كتل في وحدة}}"), ("{{on peut le réutiliser}}", "{{يمكن إعادة استعمالها}}")], [None, None], [None, None]], w=(6, 6))],
 script=SCR(61, [dict(t=None, full=SP.SPECS[61]["script"][0], masked=SP.SPECS[61]["script"][0]),
                 dict(t=None, full=SP.SPECS[61]["script"][1], masked=CI.mask(SP.SPECS[61]["script"][1], cnt={0: DOT}, over={2: ov("avancer de ……… pas", "تحرك ……… خطوة"), 3: ov("tourner ↻ de ……… degrés", "استدر يمينا ……… درجة")}))],
            note=(("Le premier script utilise 10 blocs. Complète le second (5 blocs) pour obtenir le même dessin, puis essaie.", "السكربت الأول يستعمل 10 كتل. أكمل الثاني (5 كتل) للحصول على الرسم نفسه ثم جرّب."))))

SPEC[("8", 26)] = dict(
 form=[CARD([(("Titre du jeu", "عنوان اللعبة"), None, 1), (("But du jeu", "هدف اللعبة"), None, 1), (("Lutins", "اللاعبون"), None, 1), (("Variable : nom et rôle", "المتغير: الاسم والدور"), None, 1),
             (("Modules (3 au plus) : noms et rôles", "الوحدات (3 على الأكثر): الأسماء والأدوار"), None, 2), (("Diagramme de ma solution", "مخطط حلّي"), None, 5)], w=(1, 2.2)),
       T([("Test", "الاختبار"), ("Résultat", "النتيجة"), ("Correction", "التصحيح")], [[None, None, None], [None, None, None]], w=(4, 4, 5))],
 script=None)

SPEC[("8", 27)] = dict(
 form=[T([("Critère", "المعيار"), ("Très bien", "جيد جدا"), ("Bien", "جيد"), ("À améliorer", "يحتاج إلى تحسين")],
         [[("Mon projet fonctionne", "مشروعي يشتغل"), ("☐", "☐"), ("☐", "☐"), ("☐", "☐")], [("J'ai utilisé une variable", "استعملت متغيرا"), ("☐", "☐"), ("☐", "☐"), ("☐", "☐")],
          [("J'ai utilisé un ou plusieurs modules", "استعملت وحدة أو عدة وحدات"), ("☐", "☐"), ("☐", "☐"), ("☐", "☐")], [("J'ai testé et corrigé mon projet", "اختبرت مشروعي وصحّحته"), ("☐", "☐"), ("☐", "☐"), ("☐", "☐")],
          [("Je sais expliquer mes choix", "أعرف شرح اختياراتي"), ("☐", "☐"), ("☐", "☐"), ("☐", "☐")]], w=(7, 2, 2, 3), first=True),
       CARD([(("Ce que j'ai le mieux réussi", "أحسن ما أنجزته"), None, 1), (("Ce que je dois améliorer", "ما يجب أن أحسّنه"), None, 1), (("Remarque de l'enseignant", "ملاحظة الأستاذ"), None, 2)], w=(1, 2.2))],
 script=None,
 fill=[("Pour présenter mon projet, j'explique : le {{but}} du jeu, la {{variable}}, les {{modules}} et comment je l'ai {{testé}}.", "عند عرض مشروعي أشرح: {{هدف}} اللعبة، {{المتغير}}، {{الوحدات}}، وكيف {{اختبرته}}.")])

# ============================================================================= 9e
SPEC[("9", 1)] = dict(
 form=[T([("Critère", "المعيار"), ("Scratch", "Scratch"), ("mBlock", "mBlock"), ("App Inventor", "App Inventor")],
         [[("Type de projet", "نوع المشروع"), ("{{jeux et animations}}", "{{ألعاب ورسوم متحركة}}"), ("{{programmer un robot ou une carte}}", "{{برمجة روبوت أو بطاقة}}"), ("{{applications pour téléphone}}", "{{تطبيقات للهاتف}}")],
          [("Matériel nécessaire", "العتاد اللازم"), ("{{un ordinateur}}", "{{حاسوب}}"), ("{{ordinateur + robot ou carte}}", "{{حاسوب + روبوت أو بطاقة}}"), ("{{ordinateur + téléphone}}", "{{حاسوب + هاتف}}")],
          [("Facilité d'utilisation", "سهولة الاستعمال"), ("{{très facile}}", "{{سهل جدا}}"), ("{{facile}}", "{{سهل}}"), ("{{moyenne}}", "{{متوسطة}}")],
          [("Mon choix et pourquoi", "اختياري ولماذا"), None, None, None]], w=(3, 4, 4, 4), first=True, rh=[0, 0, 0, 2])],
 script=one(56, nomask=True, q=[(("Que fait ce script ? Le lutin {{avance}} puis {{tourne}} quatre fois, puis il {{parle}}.", "ماذا يفعل هذا السكربت؟ {{يتقدم}} اللاعب ثم {{يستدير}} أربع مرات ثم {{يتكلم}}."), )]),
 fill=[("Je choisis l'environnement selon le {{projet}} à réaliser et le {{matériel}} disponible.", "اختيار بيئة العمل يتوقف على {{المشروع}} وعلى {{العتاد}} المتوفر."),
       ("Scratch sert aux {{jeux}} et animations ; mBlock pilote un {{robot}} ; App Inventor crée des applications pour {{téléphone}}.", "يناسب سكراتش إنجاز {{الألعاب}} والرسوم المتحركة، ويتيح mBlock التحكم في {{روبوت}}، وينشئ App Inventor تطبيقات {{الهاتف}}.")])

SPEC[("9", 2)] = dict(
 form=[T([("Entrées", "المدخلات"), ("Traitement", "المعالجة"), ("Sorties", "المخرجات")],
         [[("{{la réponse du joueur}}", "{{إجابة اللاعب}}"), ("{{comparer la réponse avec 4}}", "{{مقارنة الإجابة بـ 4}}"), ("{{dire « Bravo ! » ou « Essaie encore »}}", "{{قول «أحسنت!» أو «حاول مرة أخرى»}}")],
          [("Mon exemple : ", "مثالي: "), None, None]], w=(1, 1, 1), rh=[0, 2]),
       TXT(("Exemple ci-dessus : le quiz « 2 + 2 = ? ». Dans la dernière ligne, décris un autre système (distributeur, calculatrice, porte automatique…).", "المثال أعلاه: اختبار «2 + 2 = ؟». في السطر الأخير صِف نظاما آخر (موزّع آلي، آلة حاسبة، باب آلي…)."))],
 script=one(20, cond={0: ov("réponse = ………", "الإجابة = ………")}, g=(2,), note=(("Complète la condition et le message de réussite (bloc manquant), puis essaie.", "أكمل الشرط ورسالة النجاح (الكتلة الناقصة) ثم جرّب."))))

SPEC[("9", 3)] = dict(
 form=[T([("Notion", "المفهوم"), ("Définition", "التعريف"), ("Bloc exemple", "كتلة مثال")],
         [[("Séquence", "التسلسل"), ("{{instructions exécutées l'une après l'autre}}", "{{تعليمات تُنفَّذ الواحدة بعد الأخرى}}"), bk("move")],
          [("Événement", "الحدث"), ("{{ce qui déclenche un script}}", "{{ما يُطلق السكربت}}"), bk("space")],
          [("Condition", "الشرط"), ("{{question vrai ou faux qui choisit une action}}", "{{سؤال صحيح أو خطأ يختار فعلا}}"), bk("if")],
          [("Boucle", "الحلقة"), ("{{répétition de blocs}}", "{{تكرار كتل}}"), bk("repeat")]], w=(3, 7, 5), first=True)],
 script=one(11, over={3: ov("ajouter ……… à y", "غيّر ص بمقدار ………")}, note=(("Le lutin monte de 100 pas puis redescend. Complète le deuxième nombre pour qu'il revienne à sa place, puis essaie.", "يصعد اللاعب 100 خطوة ثم ينزل. أكمل العدد الثاني ليعود إلى مكانه ثم جرّب."))),
 fill=[("Pour résoudre un problème, je combine {{séquence}}, {{événement}}, {{condition}} et {{boucle}}.", "لحل مشكل أجمع بين {{التسلسل}}، {{الحدث}}، {{الشرط}}، {{الحلقة}}."),
       ("Une {{boucle}} répète des blocs ; une {{condition}} choisit une action selon vrai ou faux.", "{{الحلقة}} تكرّر كتلا، أما {{الشرط}} فيختار فعلا حسب صحيح أو خطأ.")])

SPEC[("9", 4)] = dict(
 form=[T([("", ""), ("Nom", "الاسم"), ("Rôle", "الدور")],
         [[("Variable", "المتغير"), ("{{vies}}", "{{الأرواح}}"), ("{{compter les vies restantes}}", "{{عدّ الأرواح المتبقية}}")], [("Variable", "المتغير"), None, None],
          [("Module", "الوحدة"), None, None], [("Script principal", "السكربت الرئيسي"), ("{{initialiser, répéter, tester les collisions}}", "{{التهيئة، التكرار، اختبار الاصطدام}}"), None]], w=(3, 4, 6), first=True)],
 script=one(28, over={1: ov("mettre vies à ………", "اجعل الأرواح = ………")}, cond={1: ov("vies = ………", "الأرواح = ………")}, note=(("Complète le nombre de vies de départ et la condition de fin du jeu, puis essaie.", "أكمل عدد الأرواح عند البداية وشرط نهاية اللعبة ثم جرّب."))))

SPEC[("9", 5)] = dict(
 form=[T([("Capteur", "المستشعر"), ("Ce qu'il mesure", "ما يقيسه"), ("Donnée obtenue", "المعطى المحصَّل عليه")],
         [[("Température", "الحرارة"), ("{{la chaleur}}", "{{درجة السخونة}}"), ("{{un nombre (en °C)}}", "{{عدد (بالدرجة المئوية)}}")], [("Lumière", "الإضاءة"), ("{{la luminosité}}", "{{شدة الضوء}}"), ("{{un nombre}}", "{{عدد}}")],
          [("Distance (ultrasons)", "المسافة (فوق صوتية)"), ("{{l'éloignement d'un objet}}", "{{بعد شيء}}"), ("{{un nombre (en cm)}}", "{{عدد (بالسنتيمتر)}}")], [("Bouton", "الزر"), ("{{un appui}}", "{{ضغطة}}"), ("{{vrai ou faux}}", "{{صحيح أو خطأ}}")]], w=(4, 5, 5), first=True)],
 script=one(62, cond={0: ov("distance de Personne < ………", "المسافة إلى الشخص < ………")}, g=(1,), note=(("Complète la distance de détection et le costume quand la porte s'ouvre, puis essaie.", "أكمل مسافة الكشف وزي الباب عند الانفتاح ثم جرّب."))))

SPEC[("9", 6)] = dict(
 form=[T([("Actionneur", "المنفّذ"), ("Effet", "الأثر"), ("Simulation dans Scratch", "المحاكاة في سكراتش")],
         [[("Diode (LED)", "الصمّام الضوئي (LED)"), ("{{elle s'allume}}", "{{يُضيء}}"), ("{{changer de costume}}", "{{تبديل الزي}}")], [("Moteur", "المحرّك"), ("{{il tourne}}", "{{يدور}}"), ("{{tourner le lutin}}", "{{تدوير اللاعب}}")],
          [("Buzzer", "الجرس الإلكتروني"), ("{{il émet un son}}", "{{يُصدر صوتا}}"), ("{{jouer un son}}", "{{تشغيل صوت}}")], [("Servomoteur (porte)", "المحرّك المؤازر (باب)"), ("{{la porte s'ouvre ou se ferme}}", "{{ينفتح الباب أو ينغلق}}"), ("{{changer de costume}}", "{{تبديل الزي}}")]], w=(4, 5, 5), first=True)],
 script=one(64, g=(4,), over={5: ov("attendre ……… secondes", "انتظر ……… ثوان")}, note=(("Complète le costume manquant et la durée du feu rouge (3 secondes), puis essaie.", "أكمل الزي الناقص ومدة الضوء الأحمر (3 ثوان) ثم جرّب."))),
 fill=[("Un {{actionneur}} agit : il allume, fait tourner ou {{émet un son}}.", "{{المنفّذ}} يفعل: يُضيء أو يُدير أو {{يُصدر صوتا}}."),
       ("Dans Scratch, un actionneur se simule avec un {{costume}} ou un {{son}}.", "في سكراتش نحاكي المنفّذ باستعمال {{زي}} أو {{صوت}}.")])

SPEC[("9", 7)] = dict(
 form=[T([("Ligne du programme", "سطر البرنامج"), ("Commentaire", "التعليق")],
         [[BLK("va", "mettre humidité à 60", "اجعل الرطوبة = 60"), ("{{valeur de départ du capteur simulé}}", "{{القيمة الأولى للمستشعر المُحاكى}}")], [BLK("va", "ajouter -1 à humidité", "غيّر الرطوبة بمقدار -1"), ("{{le sol sèche peu à peu}}", "{{تجفّ التربة شيئا فشيئا}}")],
          [BLK("ct", "si humidité < 30", "إذا الرطوبة < 30"), ("{{le capteur indique que le sol est sec}}", "{{المستشعر يدل على أن التربة جافة}}")], [BLK("lk", "costume arrosage en marche", "زي السقي مشتغل"), ("{{l'actionneur s'active}}", "{{يشتغل المنفّذ}}")]], w=(6, 7))],
 script=one(65, cond={0: ov("humidité < ………", "الرطوبة < ………")}, over={3: ov("ajouter ……… à humidité", "غيّر الرطوبة بمقدار ………")}, note=(("Complète le seuil d'arrosage et l'augmentation d'humidité, puis essaie : l'humidité doit remonter quand l'arrosage est en marche.", "أكمل عتبة السقي وزيادة الرطوبة ثم جرّب: يجب أن ترتفع الرطوبة عند اشتغال السقي."))),
 fill=[("Un système complet : le capteur {{mesure}}, le programme {{décide}}, l'actionneur {{agit}}.", "نظام كامل: المستشعر {{يقيس}}، البرنامج {{يقرر}}، المنفّذ {{يفعل}}."),
       ("Un commentaire {{explique}} le rôle d'une ligne du programme.", "التعليق {{يشرح}} دور سطر من البرنامج.")])

SPEC[("9", 8)] = SPEC[("8", 24)] | dict(form=[T([("Test effectué", "الاختبار المنجز"), ("Résultat attendu", "النتيجة المنتظرة"), ("Résultat obtenu", "النتيجة المحصَّلة"), ("Correction ou amélioration", "التصحيح أو التحسين")],
         [[("Je joue au jeu pendant 30 secondes", "ألعب 30 ثانية"), ("Le score augmente", "تزداد النقاط"), ("Il ne change pas", "لا تتغير"), ("{{Vérifier la condition « touche » et le bloc « ajouter 1 au score »}}", "{{فحص شرط «لمس» وكتلة «زد 1 على النقاط»}}")],
          [None, None, None, None], [None, None, None, None], [None, None, None, None]], w=(4, 4, 4, 5))],
 script=SCR(61, [dict(t=None, full=SP.SPECS[61]["script"][0], masked=SP.SPECS[61]["script"][0]),
                 dict(t=None, full=SP.SPECS[61]["script"][1], masked=CI.mask(SP.SPECS[61]["script"][1], cnt={0: DOT}, over={2: ov("avancer de ……… pas", "تحرك ……… خطوة"), 3: ov("tourner ↻ de ……… degrés", "استدر يمينا ……… درجة")}))],
            note=(("Optimise : complète le second script (5 blocs) pour obtenir le même dessin que le premier (10 blocs), puis teste.", "حسّن: أكمل السكربت الثاني (5 كتل) للحصول على الرسم نفسه للأول (10 كتل) ثم اختبر."))))

SPEC[("9", 9)] = dict(
 form=[T([("Critère", "المعيار"), ("Solution A", "الحل A"), ("Solution B", "الحل B")],
         [[("Lisibilité du script", "وضوح السكربت"), None, None], [("Nombre de blocs", "عدد الكتل"), None, None], [("Facilité de jeu", "سهولة اللعب"), None, None], [("Ma décision", "قراري"), None, None]], w=(5, 5, 5), first=True, rh=[1, 1, 1, 2]),
       CARD([(("Je choisis la solution…", "أختار الحل…"), None, 1), (("car…", "لأنّ…"), None, 2)], w=(1, 2.4))],
 script=None,
 fill=[("Je compare deux solutions avec des {{critères}} : lisibilité, nombre de {{blocs}}, facilité de {{jeu}}.", "أقارن بين حلّين بواسطة {{معايير}}: الوضوح وعدد {{الكتل}} وسهولة {{اللعب}}."),
       ("Pour {{justifier}} mon choix, je donne une {{raison}} précise.", "{{لتبرير}} اختياري أذكر {{سببا}} دقيقا.")])

SPEC[("9", 10)] = dict(
 form=[CARD([(("Titre du projet", "عنوان المشروع"), None, 1), (("Problème à résoudre", "المشكل المراد حلّه"), None, 1), (("Entrées → traitement → sorties", "المدخلات ← المعالجة ← المخرجات"), None, 2),
             (("Fonctions demandées", "الوظائف المطلوبة"), None, 2), (("Contraintes (temps, matériel)", "القيود (الوقت والعتاد)"), None, 1), (("Diagramme de la solution", "مخطط الحل"), None, 4)], w=(1, 2.2))],
 script=None,
 fill=[("Le {{cahier des charges}} dit ce que le projet doit faire.", "{{كراس الشروط}} يحدد ما يجب أن يفعله المشروع."),
       ("Je dessine le {{diagramme}} avant de programmer : {{entrées}}, {{traitement}}, {{sorties}}.", "أرسم {{المخطط}} قبل البرمجة: {{المدخلات}}، {{المعالجة}}، {{المخرجات}}.")])

SPEC[("9", 11)] = dict(
 form=[T([("Étape de réalisation", "مرحلة الإنجاز"), ("Fait ?", "أُنجزت؟"), ("Test et résultat", "الاختبار والنتيجة")],
         [[None, ("☐", "☐"), None], [None, ("☐", "☐"), None], [None, ("☐", "☐"), None], [None, ("☐", "☐"), None], [None, ("☐", "☐"), None]], w=(6, 2, 7), rh=[1, 1, 1, 1, 1]),
       CARD([(("Problème rencontré", "الصعوبة التي واجهتها"), None, 1), (("Comment je l'ai résolu", "كيف تجاوزتها"), None, 2)], w=(1, 2))],
 script=None,
 fill=[("Je réalise mon projet par {{étapes}} et je {{teste}} après chaque étape.", "أنجز مشروعي على {{مراحل}}، ثم {{أختبر}} بعد كل مرحلة.")])

SPEC[("9", 12)] = dict(
 form=[T([("Amélioration réalisée", "التحسين المنجز"), ("Pourquoi ?", "لماذا؟"), ("Preuve (test)", "الدليل (اختبار)")], [[None, None, None], [None, None, None], [None, None, None]], w=(5, 5, 5), rh=[2, 2, 2]),
       CARD([(("Les points forts de mon projet", "نقاط قوة مشروعي"), None, 2), (("Ce que je ferais ensuite", "ما سأفعله لاحقا"), None, 1)], w=(1, 2.2))],
 script=None,
 fill=[("Améliorer, c'est rendre le projet plus {{clair}}, plus {{court}} ou plus agréable à jouer.", "التحسين هو جعل المشروع أكثر {{وضوحا}} أو {{اختصارا}} أو متعة في اللعب."),
       ("Je {{justifie}} chaque amélioration avec un {{test}}.", "{{أبرّر}} كل تحسين بواسطة {{اختبار}}.")])

SPEC[("9", 13)] = dict(
 form=[T([("Compétence", "الكفاية"), ("Acquis ✓", "مكتسب ✓"), ("En cours ~", "في طور الاكتساب ~"), ("À revoir ✗", "يحتاج إلى مراجعة ✗"), ("Ce que je fais pour progresser", "ما سأفعله للتقدم")],
         [[("Séquence et événements", "التسلسل والأحداث"), ("☐", "☐"), ("☐", "☐"), ("☐", "☐"), None], [("Conditions", "الشروط"), ("☐", "☐"), ("☐", "☐"), ("☐", "☐"), None], [("Boucles", "الحلقات"), ("☐", "☐"), ("☐", "☐"), ("☐", "☐"), None],
          [("Variables et modules", "المتغيرات والوحدات"), ("☐", "☐"), ("☐", "☐"), ("☐", "☐"), None], [("Capteurs et actionneurs", "المستشعرات والمنفّذات"), ("☐", "☐"), ("☐", "☐"), ("☐", "☐"), None],
          [("Tester et corriger", "الاختبار والتصحيح"), ("☐", "☐"), ("☐", "☐"), ("☐", "☐"), None]], w=(5, 2, 2, 2, 6), first=True, rh=[1, 1, 1, 1, 1, 1])],
 script=None,
 fill=[("Je fais le {{bilan}} de mes acquis pour savoir ce que je dois {{revoir}}.", "أُعدّ {{حصيلة}} مكتسباتي لأعرف ما يجب أن {{أراجعه}}.")])

SPEC[("9", 14)] = dict(
 form=[CARD([(("Titre du projet", "عنوان المشروع"), None, 1), (("Auteur(s)", "الصاحب أو الأصحاب"), None, 1), (("Crédits (images, sons, projets remixés)", "المصادر (صور وأصوات ومشاريع معاد صياغتها)"), None, 2),
             (("Espace de partage choisi", "فضاء المشاركة المختار"), None, 1), (("Lien du projet", "رابط المشروع"), None, 1)], w=(1, 2.2)),
       T([("Avant de partager, je vérifie…", "قبل المشاركة أتحقق من…"), ("Oui", "نعم"), ("Non", "لا")],
         [[("J'ai cité l'auteur des éléments que j'ai réutilisés", "ذكرت صاحب العناصر التي أعدت استعمالها"), ("☐", "☐"), ("☐", "☐")], [("Je n'ai écrit aucune information personnelle", "لم أكتب أي معلومة شخصية"), ("☐", "☐"), ("☐", "☐")],
          [("Mon projet a un titre et des instructions claires", "لمشروعي عنوان وتعليمات واضحة"), ("☐", "☐"), ("☐", "☐")], [("J'ai testé mon projet avant de le partager", "اختبرت مشروعي قبل مشاركته"), ("☐", "☐"), ("☐", "☐")]], w=(9, 2, 2))],
 script=None)
