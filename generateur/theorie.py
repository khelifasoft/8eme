"""Rubrique « Théorie Scratch » : sept mini-leçons pour que les élèves de 7e comprennent Scratch avant de programmer.
Placée sur la page 7e (« Programmation »), juste avant les contes ; pas de théorie sur la page 8e (choix de l'enseignant).
Pour l'ajouter à une autre année : YEARS ci-dessous (la page affiche alors les mêmes leçons) -- le contenu des leçons est celui de la 7e.

Gabarit identique pour chaque leçon (theorie_data.py) : accroche, vie courante, rappel, l'essentiel (2 phrases), image, activités interactives (remettre en ordre,
exécution pas à pas, schéma cliquable, coordonnées, QCM), vocabulaire arabe / français / anglais, erreurs fréquentes, « À retenir », « Teste-toi » (5 questions),
activités liées du planning et case « Fait » (progression enregistrée dans le navigateur).
Le découpage suit le planning de la 7e (planning.py) : leçon 1 -> séance 22, leçons 2 à 4 -> séance 23, leçon 5 -> séance 24, leçon 6 -> séance 25, leçon 7 -> séance 26.

Fichiers : theorie_core.py (briques) · theorie_data.py (leçons) · theorie_img.py (images dans theorie/) · theorie_js.py (JavaScript et CSS de la page) · theorie.py (ce fichier : export et contrôles).
Chaque texte est un couple (français, arabe). export() -> (données JSON pour la page en arabe, dictionnaire arabe -> français).
Usage : python3 generateur/theorie.py  (contrôles de cohérence)"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from theorie_core import P, FRM
import theorie_data as D
import theorie_img as IMG
import scratch_art as art

YEARS = ["7"]
IMGDIR = "theorie"
ACTIMG = "fiches-activite/activites/a{n}-{k}{s}.svg"

UI = dict(
 hubTitle=("Théorie Scratch", "نظرية سكراتش"),
 hubIntro=("Sept petites leçons pour comprendre Scratch avant de programmer : lis, essaie, teste-toi, puis passe aux activités.", "سبعة دروس صغيرة لفهم سكراتش قبل البرمجة: اقرأ وجرّب واختبر نفسك ثم انتقل إلى الأنشطة."),
 progress=("Ta progression :", "تقدّمك:"), openAll=("Ouvrir toute la théorie", "فتح النظرية كاملة"), seePlanning=("Voir le planning des séances", "الاطلاع على تخطيط الحصص"),
 lesson=("Leçon", "الدرس"), min=("min", "د"), objective=("Objectif", "الهدف"), hook=("Question d'accroche", "سؤال الانطلاق"), life=("Dans la vie courante", "في الحياة اليومية"),
 essential=("L'essentiel", "الأساسي"), figures=("En images", "بالصور"), activities=("Activités interactives", "أنشطة تفاعلية"), vocab=("Vocabulaire", "المفردات"),
 mistakes=("Erreurs fréquentes", "أخطاء شائعة"), retain=("À retenir", "ما يجب تذكّره"), testYou=("Teste-toi", "اختبر نفسك"), practice=("Pour s'entraîner", "للتدرّب"), challenge=("Défi", "تحدٍّ"),
 markDone=("Marquer la leçon comme faite", "علّم الدرس كمنجز"), done=("Fait ✓", "تم ✓"), doneShort=("Fait", "تم"), prevLesson=("Leçon précédente", "الدرس السابق"), nextLesson=("Leçon suivante", "الدرس التالي"),
 allLessons=("Toutes les leçons", "كل الدروس"), seanceLinked=("Séance liée", "الحصة المرتبطة"), theoryLbl=("Théorie à lire", "نظرية للقراءة"), bestScore=("Meilleur score :", "أفضل نتيجة:"),
 check=("Vérifier", "تحقّق"), shuffle=("Mélanger", "اخلط"), retry=("Recommencer", "إعادة المحاولة"), next=("Suivant", "التالي"), prev=("Précédent", "السابق"), runAll=("Tout exécuter", "تنفيذ الكل"),
 up=("Monter", "إلى الأعلى"), down=("Descendre", "إلى الأسفل"), goal=("À faire", "ما عليك فعله"), bravo=("Bravo !", "أحسنت!"), notYet=("Pas encore tout à fait.", "ليس بعد تماما."),
 wellPlaced=("bien placés", "في مكانها الصحيح"), score=("Ton score :", "نتيجتك:"), perfect=("Parfait ! Tu peux passer à la suite.", "ممتاز! يمكنك الانتقال إلى ما بعده."),
 good=("Très bien ! Relis l'explication de l'erreur.", "جيد جدا! أعد قراءة تفسير الخطأ."), again=("Relis « À retenir » puis recommence.", "أعد قراءة «ما يجب تذكّره» ثم حاول من جديد."),
 explore=("Explorer", "استكشاف"), game=("Jeu : où est… ?", "لعبة: أين…؟"), clickOn=("Clique sur :", "اضغط على:"), good1=("Bonne réponse !", "إجابة صحيحة!"), wrongZone=("Ce n'est pas ici. Réessaie.", "ليس هنا. أعد المحاولة."),
 pickZone=("Clique sur une zone du schéma.", "اضغط على منطقة من المخطط."), zonesList=("Les huit zones", "المناطق الثماني"),
 clickStage=("Clique sur la scène pour lire x et y.", "اضغط على المنصة لتقرأ س وص."), placeAt=("Place le lutin en", "ضع اللاعب في"), youClicked=("Tu as cliqué en", "ضغطت على"), tooFar=("Trop loin : essaie encore.", "بعيد جدا: حاول مجددا."),
 wellPlacedOne=("Bravo, bien placé !", "أحسنت، مكان صحيح!"), challengesDone=("Tous les défis sont réussis !", "نجحت في كل التحديات!"), challengeN=("Défi", "التحدي"), xName=("x", "س"), yName=("y", "ص"),
 myGuess=("Mon pronostic :", "توقّعي:"), guessOk=("Ton pronostic était juste.", "كان توقّعك صحيحا."), guessKo=("Ton pronostic était différent : compare avec ce que tu viens de voir.", "كان توقّعك مختلفا: قارنه بما رأيته للتو."),
 script=("Script", "السكربت"), stage=("Scène", "المنصة"), step=("Étape", "الخطوة"), direction=("Direction", "الاتجاه"), turnN=("Tour", "الدورة"), condLbl=("Condition", "الشرط"), isTrue=("vrai", "صحيح"), isFalse=("faux", "خطأ"),
 notRun=("Pas encore exécuté.", "لم يُنفَّذ بعد."), endScript=("Fin du script.", "انتهى السكربت."), startState=("Position de départ", "وضع الانطلاق"), chooseCase=("Choisis un cas :", "اختر حالة:"),
 memoTitle=("Aide-mémoire : Scratch en une page", "بطاقة تذكير: سكراتش في صفحة"), words=("Les 12 mots de Scratch", "كلمات سكراتش الاثنتا عشرة"), rulesTitle=("Les six règles d'or du programmeur", "القواعد الذهبية الست للمبرمج"),
 printMemo=("Imprimer l'aide-mémoire", "طباعة بطاقة التذكير"), reset=("Effacer ma progression", "مسح تقدّمي"), saved=("Ta progression est enregistrée dans ce navigateur seulement.", "يُحفظ تقدّمك في هذا المتصفح فقط."),
 moreActs=("Voir toutes les activités", "عرض كل الأنشطة"), openLesson=("Ouvrir la leçon", "فتح الدرس"), word=("Mot", "الكلمة"), meaning=("Sens", "المعنى"),
)

GLOSSARY = [
 ("لاعب", "lutin", "sprite", ("Un personnage ou un objet de la scène, avec ses scripts, ses costumes et ses sons.", "شخصية أو شيء في المنصة له سكربتاته وأزياؤه وأصواته.")),
 ("المنصة", "scène", "stage", ("La zone où l'on voit le résultat du programme.", "المنطقة التي نرى فيها نتيجة البرنامج.")),
 ("زي", "costume", "costume", ("Une apparence d'un lutin ; en changer donne l'impression de mouvement.", "مظهر من مظاهر اللاعب؛ وتبديله يعطي انطباعا بالحركة.")),
 ("كتلة", "bloc", "block", ("Une instruction que l'on assemble avec d'autres.", "تعليمة نركّبها مع تعليمات أخرى.")),
 ("سكربت", "script", "script", ("Un empilement de blocs qui commence par un événement.", "تراصّ من الكتل يبدأ بحدث.")),
 ("تسلسل", "séquence", "sequence", ("Des instructions exécutées l'une après l'autre.", "تعليمات تُنفَّذ الواحدة بعد الأخرى.")),
 ("حدث", "événement", "event", ("Ce qui déclenche un script : drapeau vert, touche, clic, message.", "ما يُطلق السكربت: العلم الأخضر أو مفتاح أو نقرة أو رسالة.")),
 ("حلقة", "boucle", "loop", ("Des blocs répétés plusieurs fois ou sans arrêt.", "كتل تتكرر عدة مرات أو دون توقف.")),
 ("شرط", "condition", "condition", ("Une question dont la réponse est vrai ou faux.", "سؤال جوابه صحيح أو خطأ.")),
 ("إحداثيات", "coordonnées", "coordinates", ("Les nombres x et y qui donnent la position d'un lutin.", "العددان س وص اللذان يحدّدان مكان اللاعب.")),
 ("رسالة", "message", "message", ("Un signal envoyé par un lutin pour en réveiller d'autres.", "إشارة يرسلها لاعب لإيقاظ لاعبين آخرين.")),
 ("خطأ برمجي", "bug", "bug", ("Une erreur dans un programme ; la corriger s'appelle déboguer.", "خطأ في برنامج؛ وتصحيحه يسمى تنقيحا.")),
]
RULES = [
 ("Je lis bien l'objectif avant de commencer.", "أقرأ الهدف جيدا قبل أن أبدأ."), ("Je découpe le travail en petites étapes.", "أقسّم العمل إلى مراحل صغيرة."),
 ("Je teste après chaque bloc ajouté.", "أختبر بعد كل كتلة أضيفها."), ("Je change une seule chose à la fois, puis je teste.", "أغيّر شيئا واحدا في كل مرة ثم أختبر."),
 ("Je donne des noms clairs à mes lutins et à mes projets.", "أعطي أسماء واضحة للاعبيّ ومشاريعي."), ("Je cherche, j'essaie, puis je demande de l'aide.", "أبحث وأجرّب ثم أطلب المساعدة."),
]
# zones du schéma de l'écran de Scratch (numéros = ceux de theorie_img.py)
ZONES = [
 (1, ("Barre de menus", "شريط القوائم"), ("Elle contient le menu Fichier (enregistrer, ouvrir) et le globe pour changer la langue.", "فيه قائمة «ملف» (حفظ وفتح) والكرة الأرضية لتغيير اللغة.")),
 (2, ("Onglets Code, Costumes et Sons", "تبويبات الأكواد والأزياء والأصوات"), ("Code : les scripts du lutin. Costumes : ses images. Sons : ses sons.", "الأكواد: سكربتات اللاعب. الأزياء: صوره. الأصوات: أصواته.")),
 (3, ("Palette de blocs", "لوحة الكتل"), ("Toutes les familles de blocs. On prend un bloc ici et on le glisse vers la zone des scripts.", "كل فئات الكتل. نأخذ كتلة من هنا ونسحبها إلى منطقة السكربتات.")),
 (4, ("Zone des scripts", "منطقة السكربتات"), ("C'est l'espace de construction : on y assemble les blocs du lutin sélectionné.", "هي فضاء البناء: نركّب فيها كتل اللاعب المحدّد.")),
 (5, ("Scène", "المنصة"), ("Elle montre le résultat : les lutins bougent, parlent et jouent ici.", "تعرض النتيجة: تتحرك فيها اللاعبون وتتكلم وتلعب.")),
 (6, ("Drapeau vert et bouton Stop", "العلم الأخضر وزر الإيقاف"), ("Le drapeau vert lance le programme ; le bouton rouge l'arrête.", "العلم الأخضر يشغّل البرنامج والزر الأحمر يوقفه.")),
 (7, ("Liste des lutins", "قائمة اللاعبين"), ("Tous les personnages et objets du projet. Le lutin sélectionné reçoit les blocs.", "كل شخصيات المشروع وأشيائه. اللاعب المحدّد هو الذي يتلقى الكتل.")),
 (8, ("Arrière-plan (décor)", "الخلفية (الديكور)"), ("Le décor de la scène : on peut en ajouter et lui donner aussi des scripts.", "ديكور المنصة: يمكن إضافة خلفيات وإعطاؤها سكربتات أيضا.")),
]


def export():
    ui = {k: P(*v) for k, v in UI.items()}
    lessons = []
    for L in D.LESSONS:
        fig = []
        for f in L["fig"]:
            if f.get("shapes"): fig.append(dict(img=[f"{IMGDIR}/formes.svg", f"{IMGDIR}/formes-ar.svg"], cap=P("Les cinq formes de blocs", "الأشكال الخمسة للكتل")))
            else: fig.append(dict(img=[ACTIMG.format(n=f["n"], k=f["k"], s=""), ACTIMG.format(n=f["n"], k=f["k"], s="-ar")], cap=P(*f["cap"])))
        lessons.append(dict(n=L["n"], seance=L["seance"], min=L["min"], color=L["color"], t=P(*L["title"]), obj=P(*L["obj"]), hook=P(*L["hook"]), life=P(*L["life"]), recall=P(*L["recall"]) if L["recall"] else None,
                            idea=[P(*s) for s in L["idea"]], fig=fig, widgets=L["widgets"], vocab=[list(v) for v in L["vocab"]], mistakes=[P(*m) for m in L["mistakes"]], retain=[P(*m) for m in L["retain"]],
                            quiz=L["quiz"], acts=L["acts"], defi=P(*L["defi"]), img=[f"{IMGDIR}/c{L['n']}.svg", f"{IMGDIR}/c{L['n']}-ar.svg"]))
    glossary = [dict(ar=a, fr=f, en=e, d=P(*d)) for a, f, e, d in GLOSSARY]
    rules = [P(*r) for r in RULES]
    zones = [dict(id=i, name=P(*n), desc=P(*d)) for i, n, d in ZONES]
    by_seance = {}
    for L in D.LESSONS: by_seance.setdefault(str(L["seance"]), []).append(L["n"])
    sprites = {"cat": art.art_svg("a", "chat"), "apple": art.art_svg("d", "pomme")}
    iface_svg = IMG.iface_svg("ar")          # le texte arabe du schéma est retraduit par la page ; ses traductions sont enregistrées par P() pendant le dessin
    data = dict(years=YEARS, ui=ui, lessons=lessons, glossary=glossary, rules=rules, iface=dict(svg=iface_svg, zones=zones), sprites=sprites, bySeance=by_seance, total=len(lessons),
                memoImg=[f"{IMGDIR}/c2.svg", f"{IMGDIR}/c2-ar.svg"])
    return data, dict(FRM)


def check():
    import planning as PL
    data, fr = export()
    plan = PL.PLAN["7"]
    for L in D.LESSONS:
        assert L["seance"] in plan, ("séance inconnue", L["n"], L["seance"])
        assert len(L["quiz"]) == 5, ("cinq questions par leçon", L["n"])
        for q in L["quiz"]:
            assert 0 <= q["a"] < len(q["o"]), ("réponse hors liste", L["n"], q["q"])
        for w in L["widgets"]:
            if w["k"] == "quiz":
                for q in w["qs"]: assert 0 <= q["a"] < len(q["o"]), ("réponse hors liste", L["n"], q["q"])
        used = set()                                    # une activité liée doit être proposée dans le planning, à cette séance ou avant
        for s in sorted(plan):
            if s <= L["seance"]: used |= set(plan[s]["core"] + plan[s]["support"] + plan[s]["challenge"])
        for n in L["acts"]:
            assert n in PL.ACT, ("activité inconnue", n)
        # notions : les activités liées n'utilisent que des notions déjà introduites à cette séance
        known = set()
        for s in sorted(plan):
            if s <= L["seance"]: known |= set(plan[s]["new"])
        for n in L["acts"]:
            miss = PL.ACT_N[n] - known
            assert not miss, (f"leçon {L['n']} : l'activité {n} demande des notions pas encore introduites à la séance {L['seance']}", miss)
        for g in ("vocab", "mistakes", "retain"): assert L[g], (L["n"], g)
    # tous les textes arabes ont une traduction ; aucune traduction vide
    assert all(k and v for k, v in fr.items())
    # les clés de texte utilisées par le JavaScript existent
    import theorie_js as JS
    used_keys = set(re.findall(r"\bU\.(\w+)", JS.JS))
    missing = used_keys - set(UI)
    assert not missing, ("clés U.xxx absentes de UI :", sorted(missing))
    print(f"{len(D.LESSONS)} leçons · {sum(len(L['quiz']) + sum(len(w['qs']) for w in L['widgets'] if w['k'] == 'quiz') for L in D.LESSONS)} questions · {len(fr)} traductions · séances liées :", {k: v for k, v in data['bySeance'].items()})
    return data, fr


if __name__ == "__main__":
    check()
    print(IMG.render_all(), "images dans", IMGDIR)
