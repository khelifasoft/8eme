"""Construit index.html (page d'accueil de l'élève) à partir de manifest.json."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
man = json.load(open(os.path.join(HERE, "manifest.json"), encoding="utf-8"))
import sys; sys.path.insert(0, HERE)
import i18n_fr
games = json.load(open(os.path.join(HERE, "jeux2_manifest.json"), encoding="utf-8"))
games += json.load(open(os.path.join(HERE, "jeux3_manifest.json"), encoding="utf-8"))
for g in json.load(open(os.path.join(HERE, "jeux_manifest.json"), encoding="utf-8")):
    games.append(dict(g, cat="catch", cat_ar="ألعاب سكراتش", cat_fr="Jeux Scratch"))
for _g in json.load(open(os.path.join(HERE, "jeux4_manifest.json"), encoding="utf-8")) + json.load(open(os.path.join(HERE, "jeux5_manifest.json"), encoding="utf-8")) + json.load(open(os.path.join(HERE, "jeux6_manifest.json"), encoding="utf-8")):
    games.append(dict(_g, cat="catch", cat_ar="ألعاب سكراتش", cat_fr="Jeux Scratch"))
_EXTRA = {"labyrinthe": dict(video="jeux/videos/labyrinthe.mp4", fiche="labyrinthe", res="labyrinthe"), "saut": dict(video="jeux/videos/saut.mp4", fiche="saut", res="saut"), "sindbad": dict(video="jeux/videos/attrape-poissons.mp4", fiche="catch", res="catch"), "course": dict(video="jeux/videos/course.mp4", fiche="course", res="course")}
for _g in games:
    if _g["cat"] == "catch": _g.update(_EXTRA.get(_g["key"], {}))
man["games"] = games
man["programme"] = json.load(open(os.path.join(HERE, "programme.json"), encoding="utf-8"))
man["curriculum"] = json.load(open(os.path.join(HERE, "axes.json"), encoding="utf-8"))
import exercices
import secondaire
man["exo"] = {**exercices.EXO, **secondaire.EXO}; man["act"] = exercices.ACT
man["seances"] = json.load(open(os.path.join(HERE, "seances.json"), encoding="utf-8"))
import parcours, fiches_programme as _FP, activites as _ACT
man["activites"], _afr = _ACT.export()
man["fiches"] = {fid: dict(title=F["title"], meta=f'{_FP.PRG["levels"][str(F["level"])]["year_fr"]} · {F["duree"]}', situation=F["situation"], steps=[t for t, _ in F["demarche"]], eleve=F["eleve"], criteres=F["criteres"], allegee=F["allegee"], prolongement=F["prolongement"]) for fid, F in _FP.FAMILIES.items()}
man["ressources"] = json.load(open(os.path.join(HERE, "ressources.json"), encoding="utf-8"))
man["etapes"] = json.load(open(os.path.join(HERE, "etapes.json"), encoding="utf-8"))
import fiches_ar as _AR
_far = {}
for _fid, _d in _AR.AR.items():
    _f = _d["fr"]
    man["fiches"][_fid] = dict(title=_d["title"], meta=_d["year"] + " · " + _d["duree"], situation=_d["situation"], steps=_d["steps"], eleve=_d["eleve"], criteres=_d["criteres"], allegee=_d["allegee"], prolongement=_d["prolongement"])
    _far[_d["title"]] = _f["title"]; _far[_d["year"] + " · " + _d["duree"]] = _f["year"] + " · " + _f["duree"]
    for _k in ("situation", "allegee", "prolongement"): _far[_d[_k]] = _f[_k]
    for _k in ("steps", "eleve", "criteres"):
        for _a, _b in zip(_d[_k], _f[_k]): _far[_a] = _b
for _key, _steps in (("catch", _AR.CATCH_STEPS), ("course", _AR.COURSE_STEPS), ("saut", _AR.SAUT_STEPS), ("labyrinthe", _AR.LABY_STEPS)):
    for _i, (_t, _c) in enumerate(_steps):
        _e = man["etapes"][_key][_i]; _far[_t] = _e["t"]; _far[_c] = _e["c"]; _e["t"], _e["c"] = _t, _c
for _lst in man["etapes"]["contes"].values():
    for _i, _e in enumerate(_lst): _far[f"{_AR.SCENE[0]} {_i + 1}"] = f"{_AR.SCENE[1]} {_i + 1}"; _e["t"] = f"{_AR.SCENE[0]} {_i + 1}"
_far.update({k.strip(): v.strip() for k, v in _AR.HEAD.items()})
man["parcours"], _pfr = parcours.export()
FR = i18n_fr.build(man, games)
FR["map"].update(_pfr)
FR["map"].update(_far)
FR["map"].update(_afr)
import planning as _PL
man["planning"], _pfr2 = _PL.export()
FR["map"].update(_pfr2)
import theorie as _TH, theorie_js as _TH_JS, securite as _SE, securite_js as _SE_JS
man["theorie"], _thfr = _TH.export()
man["securite"], _sefr = _SE.export()
import objets as _OB
man["objets"], _obfr = _OB.export()
for _k, _v in _obfr.items(): FR["map"].setdefault(_k, _v)
for _k, _v in _sefr.items(): FR["map"].setdefault(_k, _v)
for _k, _v in _thfr.items():
    if FR["map"].get(_k, _v) != _v: print("traduction différente (théorie) :", repr(_k), "|", repr(FR["map"][_k]), "|", repr(_v))
    FR["map"].setdefault(_k, _v)
FR["rules"] += [["^ح(\\d+)$", "S$1"], ["^(.+) · ح(\\d+)$", "$1 · S$2"]]   # numéros de séance : ح22 -> S22
FR["map"].update({"تخطيط الحصص": "Planning des séances", "⬇ تثبيت سكراتش على الحاسوب": "⬇ Installer Scratch sur l'ordinateur", "⬇ تثبيت سكراتش على Windows": "⬇ Installer Scratch pour Windows", "⬇ تثبيت سكراتش على macOS": "⬇ Installer Scratch pour macOS", "مقترح لنظامك": "Conseillé pour ton système", "⬇ اختصار هذا الموقع على سطح المكتب": "⬇ Raccourci de ce site sur le bureau", "تخطيط حصص سكراتش": "Planning des séances Scratch", "فتح الكل": "Tout déplier", "طي الكل": "Tout replier", "الاطلاع على تخطيط الحصص": "Voir le planning des séances", "التخطيط حسب الحصص": "Planning par séances", "بطاقة الحصة": "Fiche de séance",
 "حصص مقترحة إضافية: الشيء القابل للبرمجة وتطبيقة الهاتف": "Séances complémentaires proposées : objet programmable et application mobile", "اقتراح غير رسمي (المساعدة البيداغوجية 2026): أربع حصص حول بطاقة micro:bit (اكتشاف، مدخلات ومخرجات، قياس وقرار وفعل، مشروع النرد) ثم أربع حصص حول تطبيقة هاتف بـ App Inventor (الواجهة، الأحداث، الاختبار والتوليد، التحكم في البطاقة). لكل حصة مذكرة في آخر مذكرات 9.": "Proposition non officielle (aide pédagogique 2026) : quatre séances sur la carte micro:bit (découvrir, entrées et sorties, mesurer-décider-agir, mini-projet dé électronique) puis quatre sur une application mobile App Inventor (interface, événements, test et génération, commander la carte). Chaque séance a sa fiche à la fin du cahier 9e.", "حصص إضافية مقترحة (المساعدة البيداغوجية 2026)": "Séances complémentaires proposées (aide pédagogique 2026)", "الشيء القابل للبرمجة (micro:bit) وتطبيقة الهاتف (App Inventor). اقتراح غير رسمي خارج التوزيع السنوي: يُدرج مكان حصص مراجعة أو في مشروع.": "Objet programmable (micro:bit) et application mobile (App Inventor). Proposition non officielle, hors répartition annuelle : à insérer à la place de séances de révision ou en projet.", "الشيء القابل للبرمجة (micro:bit)": "Objet programmable (micro:bit)", "تطبيقة الهاتف (App Inventor)": "Application mobile (App Inventor)",
 "في السنة التاسعة تُبرمج أشياء حقيقية أو محاكاة وتُطوَّر تطبيقات هاتف بسيطة (المساعدة البيداغوجية 2026). لكل موضوع أربع حصص: من الاكتشاف إلى المشروع الصغير.": "En 9e, on programme des objets réels ou simulés et on développe des applications mobiles simples (aide pédagogique 2026). Chaque thème a quatre séances : de la découverte au mini-projet.",
 "سير الحصة (تخطيط السنة التاسعة)": "Démarche de la séance (planning 9e)", "مذكرات الدفتر": "Fiches du cahier", "طباعة البطاقة (PDF)": "Imprimer la fiche (PDF)", "مذكرات الدفتر (للطباعة)": "Fiches du cahier (à imprimer)", "مذكرات الدفتر (للطباعة واللصق في دفتر التلميذ)": "Fiches du cahier (à imprimer et à coller dans le cahier de l'élève)",
 "فتح المذكرات للطباعة": "Ouvrir les fiches (impression)", "PDF بالعربية": "PDF en arabe", "PDF en français": "PDF en français", "PDF بالعربية مع الإجابات": "PDF en arabe avec corrigé", "PDF avec corrigé": "PDF en français avec corrigé", "مذكرة الدفتر لهذه الحصة": "Fiche du cahier pour cette séance",
 "ورقة A4 لكل حصة: جمل ناقصة، أثر مكتوب للإتمام، وسكربت نصف منجز يُنهى في القسم.": "Une feuille A4 par séance : phrases à trous, trace écrite à compléter et script à moitié terminé à finir en classe.",
 "لكل حصة برمجة ورقة واحدة بحجم A4: جمل ناقصة للإتمام، والأثر المكتوب (جدول أو مخطط أو بطاقة)، وسكربت نصف منجز يُنهيه التلاميذ في القسم، وما يجب حفظه. تُطبع الأجزاء الفارغة، ويمكن عرض الإجابات للأستاذ. اقتراح غير رسمي قابل للتعديل.": "Une feuille A4 par séance de programmation : phrases à trous à compléter, trace écrite (tableau, schéma ou carte), script à moitié terminé que les élèves finissent en classe, et ce qu'il faut retenir. Les parties vides s'impriment ; l'enseignant peut afficher le corrigé. Proposition non officielle, à adapter."})
for _l in list({**exercices.EXO, **secondaire.EXO}.values()):
    for _q in _l:
        FR["map"][_q["q"]] = _q["q_fr"]
        for _a, _f in zip(_q["o"], _q["o_fr"]): FR["map"][_a] = _f
for _l in exercices.ACT.values():
    for _a in _l:
        FR["map"][_a["t"]] = _a["t_fr"]; FR["map"][_a["d"]] = _a["d_fr"]
        if _a.get("ex"): FR["map"][_a["ex"]] = _a["ex_fr"]
FR["map"].update({"شاهد فيديو اللعبة": "Regarder la vidéo du jeu", "فتح الفيديو في نافذة جديدة": "Ouvrir la vidéo dans un nouvel onglet","بطاقة النشاط": "Fiche d'activité", "موارد اللعبة": "Ressources du jeu", "موارد لعبة": "Ressources du jeu", "الصور": "Images", "الأصوات": "Sons", "تحميل كل الموارد (.zip)": "Télécharger toutes les ressources (.zip)", "الصور والأصوات المستعملة في اللعبة. حمّلها ثم أضفها في سكراتش (رسم ← رفع، أو صوت ← رفع).": "Les images et sons utilisés dans le jeu. Télécharge-les puis ajoute-les dans Scratch (Costumes → Importer, ou Sons → Importer).","المسار التعليمي: من نشاط إلى آخر": "Parcours : d'une activité à l'autre", "أنهِ كل مستوى قبل الانتقال إلى الذي بعده. كل نشاط صغير يستند إلى لعبة أو قصة جاهزة تفتحها في سكراتش وتعدّلها.": "Termine chaque niveau avant de passer au suivant. Chaque petite activité s'appuie sur un jeu ou un conte prêt à ouvrir dans Scratch et à modifier.",
 "المستوى": "Niveau", "الكفاية": "Compétence", "الأنشطة الصغيرة": "Petites activités", "أنا قادر على…": "Je suis capable de…", "نموذج للتحميل": "Modèle à télécharger", "فتح القصة": "Ouvrir le conte", "مشاريع أساسية للإنجاز": "Projets de base à réaliser", "الصعوبة": "Difficulté", "المطلوب": "Exigences", "نماذج": "Modèles",
 "الألعاب الجاهزة (مكتبة)": "Jeux prêts à l'emploi (bibliothèque)", "القصص الجاهزة (مكتبة)": "Contes prêts à l'emploi (bibliothèque)",
 "التحميلات": "Téléchargements", "كل المستويات": "Tous les niveaux", "⬇ تحميل": "⬇ Télécharger", "⬇ التحميلات: سكراتش وبقية البرمجيات": "⬇ Téléchargements : Scratch et autres logiciels", "حمّله من صفحة التحميلات": "téléchargez-le depuis la page Téléchargements",
 "البرمجيات المستعملة في كل المستويات. الروابط تؤدي إلى المواقع الرسمية للبرمجيات.": "Les logiciels utilisés dans tous les niveaux. Les liens mènent aux sites officiels.", "لإضافة برنامج: عدّل الملف logiciels.js.": "Pour ajouter un logiciel : modifier le fichier logiciels.js.","فضاء التلميذ": "Espace élève", "فضاء الأستاذ": "Espace enseignant", "تمارين تفاعلية": "Exercices interactifs", "أنشطة للإنجاز": "Activités à réaliser",
 "اختر الإجابة الصحيحة. يظهر التصحيح مباشرة.": "Choisis la bonne réponse. La correction s'affiche tout de suite.", "إجابة صحيحة ✓": "Bonne réponse ✓", "إجابة خاطئة ✗": "Mauvaise réponse ✗",
 "إعادة المحاولة": "Recommencer", "للتلميذ: تمارين وأنشطة لإنجازها مع أمثلة وموارد.": "Pour l'élève : exercices et activités à réaliser, avec exemples et ressources.",
 "للأستاذ: التوزيع السنوي المقترح وبطاقات الحصص.": "Pour l'enseignant : répartition annuelle proposée et fiches de séance.",
 "فتح فضاء الأستاذ": "Ouvrir l'espace enseignant", "فتح فضاء التلميذ": "Ouvrir l'espace élève", "مثال: ": "Exemple : ", "الموارد": "Ressources", "فتح الموارد": "Ouvrir les ressources",
 "التوزيع السنوي المقترح": "Répartition annuelle proposée", "اقتراح غير رسمي قابل للتعديل: حصة واحدة مدتها 60 دقيقة في الأسبوع (27 حصة، 9 في كل ثلاثي).": "Proposition non officielle à adapter : une séance de 60 minutes par semaine (27 séances, 9 par trimestre).",
 "طباعة التوزيع وبطاقات الحصص": "Imprimer la répartition et les fiches de séance", "الحصة": "Séance", "الثلاثي": "Trimestre", "المجال": "Module", "العنوان": "Titre", "النوع": "Type", "بطاقة": "Fiche",
 "لم تُدرج بعد وثيقة منهاج هذا المستوى. ستتوفر بطاقات الأستاذ عند إضافتها.": "Le programme de ce niveau n'est pas encore intégré. Les fiches enseignant seront disponibles à son ajout.",
 "لتعديل التوزيع: غيّر الملف generateur/seances.py ثم أعد توليد الصفحات.": "Pour modifier la répartition : éditer le fichier generateur/seances.py puis régénérer les pages.",
 "← الأستاذ": "← Espace enseignant", "تمارين مقترحة غير رسمية: لم تُقدَّم بعد وثيقة منهاج رسمية لهذا المستوى، فالمواضيع عامة وتُكيَّف مع المنهاج الفعلي.": "Exercices proposés à titre non officiel : aucun programme officiel n'a encore été fourni pour ce niveau ; les thèmes sont généraux et à adapter au programme réel."})
TPL = r'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Curriculum Informatique en Tunisie</title>
<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#1f4aa8">
<link rel="icon" href="icones/icone.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icones/icone-192.png">
<style>
:root{--barh:56px;--ink:#1d2433;--muted:#5d6678;--line:#dfe3ec;--soft:#f4f6fb;--blue:#1f4aa8;--orange:#e8861c;--green:#1e8a5a;
 --font:'Segoe UI','Tahoma','Arial','Noto Sans Arabic',sans-serif}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:#fff;color:var(--ink);font-family:var(--font);line-height:1.7;font-size:16px}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left)) 0 max(16px,env(safe-area-inset-right))}
.hero{border-bottom:3px solid var(--orange);padding:24px 0 18px}
.hero h1{margin:0;font-size:clamp(28px,5vw,44px);color:var(--blue);line-height:1.2}
.hero p{margin:6px 0 0;color:var(--muted);font-size:17px}
html{scroll-padding-top:calc(var(--barh) + 12px)}
body{padding-top:var(--barh)}
.topbar{position:fixed;top:0;inset-inline:0;height:56px;background:var(--blue);color:#fff;z-index:50;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:0 max(16px,env(safe-area-inset-left)) 0 max(16px,env(safe-area-inset-right));box-shadow:0 2px 8px rgba(20,40,100,.25)}
.brand{color:#fff;text-decoration:none;font-weight:800;font-size:21px;white-space:nowrap}
.yearnav{display:flex;gap:2px;height:100%;align-items:stretch}
.ydrop{position:relative;display:flex}
.ybtn{font:inherit;font-weight:700;font-size:17px;color:rgba(255,255,255,.9);background:transparent;border:0;border-top:4px solid transparent;border-bottom:4px solid transparent;padding:0 16px;cursor:pointer;display:flex;align-items:center;gap:6px}
.ybtn .ys{display:none}.ybtn .car{font-style:normal;font-size:12px;opacity:.8}
.ybtn:hover,.ybtn:focus-visible,.ydrop[data-open] .ybtn{color:#fff;background:rgba(255,255,255,.14)}
.ydrop[data-current] .ybtn{color:#fff;border-bottom-color:#fff;background:rgba(255,255,255,.12)}
.sub{display:none;position:absolute;top:100%;inset-inline-start:0;min-width:290px;margin:0;padding:6px;list-style:none;background:#fff;color:var(--ink);border:1px solid var(--line);border-radius:0 0 12px 12px;box-shadow:0 10px 24px rgba(20,40,100,.22);z-index:60}
.ydrop[data-open] .sub{display:block}
@media (hover:hover){.ydrop:hover .sub{display:block}}
.sub a{display:block;padding:9px 12px;border-radius:8px;color:var(--ink);text-decoration:none;font-size:16px;line-height:1.35}
.sub a:hover,.sub a:focus-visible{background:var(--soft);color:var(--blue)}
.sub a[aria-current=page]{background:#e6edfb;color:var(--blue);font-weight:700}
.sub li+li{border-top:1px solid var(--line)}
.sub .ov a{font-weight:700;color:var(--blue)}
@media (max-width:1400px){.ybtn .yl{display:none}.ybtn .ys{display:inline}.ybtn{padding:0 11px}}
.refgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;margin-top:10px}
.refcol{border:1px solid var(--line);border-radius:12px;padding:12px 16px;background:#fff}
.refcol h3{margin:0 0 6px;font-size:19px;color:var(--blue)}
.refitem{border-top:1px solid var(--line);padding:8px 0;display:flex;flex-direction:column;gap:2px}.refitem:first-of-type{border-top:0}
.refitem a{font-weight:700;color:var(--blue);text-decoration:none}.refitem a:hover{text-decoration:underline}
.refitem .rt{display:inline-block;font-size:11.5px;border:1px solid var(--line);border-radius:999px;padding:0 8px;color:var(--muted);align-self:flex-start;margin-top:2px}
.refitem p{margin:0;font-size:13.5px;color:var(--muted)}
@media (max-width:640px){:root{--barh:108px}.topbar{height:auto;flex-wrap:wrap;row-gap:0;padding-top:4px;padding-bottom:0}.brand{order:1;font-size:16px}.barbtns{order:2}.yearnav{order:3;width:100%;height:46px;justify-content:space-between}.ydrop{flex:1}.ybtn{width:100%;justify-content:center}.ybtn{padding:0 4px;font-size:15px}.ybtn .yl{display:none}.ybtn .ys{display:inline}.sub{position:fixed;top:var(--barh);inset-inline:8px;min-width:0}}
.yearcards{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}
.ycard{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff;display:flex;flex-direction:column}
.ycard .yh{background:var(--blue);color:#fff;padding:10px 16px;font-size:20px;font-weight:800}
.ycard ul{list-style:none;margin:0;padding:6px 10px 10px}
.ycard li{border-bottom:1px solid var(--line)}.ycard li:last-child{border:0}
.ycard a{display:block;padding:9px 6px;color:var(--ink);text-decoration:none;font-size:16px}
.ycard a:hover,.ycard a:focus-visible{color:var(--blue);background:var(--soft)}
.axcards{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px;margin-top:12px}
.axcard{border:1px solid var(--line);border-radius:12px;padding:12px 16px;display:flex;flex-direction:column;gap:6px;background:#fff}
.axcard h3{margin:0;font-size:18px;color:var(--blue)}.axcard p{margin:0;font-size:14px;color:var(--muted)}
.axhead{border:1px solid var(--line);border-radius:14px;padding:14px 20px;margin:6px 0 10px;background:#fff}
.axhead h2{margin:4px 0 6px;font-size:28px}.axhead .comp{font-size:17px;margin:0 0 6px}
.axhead h3{font-size:17px;margin:12px 0 2px;color:var(--ink)}.axhead ul{margin:2px 0 4px;padding-inline-start:22px}
.axhead details{margin-top:10px;border-top:1px dashed var(--line);padding-top:8px}.axhead summary{cursor:pointer;font-weight:700;color:var(--blue)}
.axhead .pnote{font-size:13px;color:var(--muted)}
.barbtns{display:flex;align-items:center;gap:6px}
.langbtn{font:inherit;font-size:13px;font-weight:700;color:#fff;background:transparent;border:1px solid rgba(255,255,255,.65);border-radius:6px;padding:3px 10px;cursor:pointer}
.langbtn[aria-pressed=true]{background:#fff;color:var(--blue);border-color:#fff}
.back{display:inline-block;margin:16px 0 4px;color:var(--blue);font-weight:700;text-decoration:none}
.back:hover{text-decoration:underline}
.storyhead{border:1px solid var(--line);border-radius:14px;overflow:hidden;margin:8px 0 8px}
.storyhead .sbar{height:10px}
.storyhead .sbody{padding:16px 20px;display:flex;flex-direction:column;gap:8px}
.storyhead h2{margin:0;font-size:30px}
.storyhead p{margin:0;color:var(--muted)}
.helpbox{margin:30px 0 0;border:1px solid var(--line);border-radius:12px;padding:10px 16px}
.helpbox summary{cursor:pointer;font-size:20px;font-weight:700;color:var(--blue)}
.helpbox .help{margin-top:12px}
.hbtns{display:flex;gap:8px;flex-wrap:wrap}
#getscratch{font-size:16px;padding:8px 18px;white-space:nowrap}
.head{display:flex;justify-content:space-between;gap:16px;align-items:flex-start;flex-wrap:wrap}
#install{display:inline-flex;align-items:center;gap:8px;font-size:16px;padding:8px 18px;white-space:nowrap}
#install[hidden]{display:none}
dialog{border:1px solid var(--line);border-radius:14px;max-width:min(520px,92vw);padding:20px 22px;font-family:var(--font);color:var(--ink)}
dialog::backdrop{background:rgba(20,30,50,.45)}
dialog h3{margin:0 0 8px;font-size:20px;color:var(--blue)}
dialog ul{margin:8px 0 14px;padding-inline-start:20px}
dialog li{margin:4px 0}
dialog .small{font-size:14px;color:var(--muted)}
section{padding:30px 0 6px}
h2{font-size:26px;margin:0 0 6px;color:var(--blue)}
h2+.lead{margin:0 0 18px;color:var(--muted)}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;counter-reset:s;padding:0;list-style:none;margin:0}
.steps li{border:1px solid var(--line);border-radius:10px;padding:14px 16px 14px 14px;counter-increment:s;background:var(--soft)}
.steps li::before{content:counter(s);display:inline-grid;place-items:center;width:30px;height:30px;border-radius:50%;background:var(--blue);color:#fff;font-weight:700;margin-inline-end:10px}
.stories{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:16px}
.card{border:1px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;background:#fff}
.card .bar{height:8px}
.card .body{padding:14px 16px;display:flex;flex-direction:column;gap:8px;flex:1}
.card h3{margin:0;font-size:21px}
.card p{margin:0;font-size:15px;color:var(--muted)}
.card .morale{font-size:14px;color:var(--ink);background:var(--soft);padding:4px 10px;border-radius:6px}
.btns{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:auto}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;border:1px solid var(--blue);color:var(--blue);background:#fff;border-radius:8px;padding:6px 8px;font:inherit;font-size:14px;text-decoration:none;cursor:pointer;text-align:center;line-height:1.35}
.btn:hover,.btn:focus-visible{background:var(--blue);color:#fff}
.btn.main{background:var(--blue);color:#fff}
.btn.main:hover{background:#163a86}
.btn.wide{grid-column:1/-1}
.btn.alt{border-color:var(--orange);color:#a85a08}.btn.alt:hover{background:var(--orange);color:#fff}
.tools{position:sticky;top:var(--barh);background:#fff;z-index:5;border-bottom:1px solid var(--line);padding:10px 0;display:flex;flex-direction:column;gap:10px}
.tabs{display:flex;gap:6px;flex-wrap:wrap}
.tab{border:1px solid var(--line);background:#fff;border-radius:999px;padding:5px 16px;font:inherit;font-size:15px;cursor:pointer}
.tab[aria-selected=true]{background:var(--blue);border-color:var(--blue);color:#fff}
.tab small{opacity:.75;margin-inline-start:4px}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.row input[type=search],.row select{font:inherit;font-size:15px;padding:6px 12px;border:1px solid var(--line);border-radius:8px;background:#fff;min-width:0}
.row input[type=search]{flex:1 1 220px}
.subs{display:flex;gap:6px;flex-wrap:wrap}
.chip{border:1px solid var(--line);background:#fff;border-radius:8px;padding:2px 12px;font:inherit;font-size:14px;cursor:pointer}
.chip[aria-pressed=true]{background:var(--soft);border-color:var(--ink);font-weight:700}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;padding:16px 0}
.grid.wideg{grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}
.tile{border:1px solid var(--line);border-radius:10px;padding:8px;display:flex;flex-direction:column;gap:6px;align-items:stretch;background:#fff;min-width:0}
.tile .pv{height:120px;display:grid;place-items:center;background:repeating-conic-gradient(#f4f6fb 0 25%,#fff 0 50%) 0 0/16px 16px;border-radius:6px;overflow:hidden}
.wideg .tile .pv{height:150px}
.tile .pv img{max-width:100%;max-height:100%;object-fit:contain}
.tile .nm{font-size:14px;text-align:center;line-height:1.35;min-height:2.7em;display:grid;place-items:center;overflow-wrap:anywhere}
.tile .fr{font-size:12px;color:var(--muted);text-align:center;margin-top:-4px;direction:ltr}
.tile .dl{font-size:13px;padding:3px 6px}
.sound{flex-direction:row;align-items:center;gap:10px;padding:8px 10px}
.sounds{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px;padding:16px 0}
.play{flex:none;width:42px;height:42px;border-radius:50%;border:0;background:var(--green);color:#fff;font-size:18px;cursor:pointer}
.play[aria-pressed=true]{background:#c0392b}
.sound .nm{flex:1;min-height:0;text-align:right;place-items:start}
.sound .meta{font-size:12px;color:var(--muted)}
.empty{padding:40px 0;color:var(--muted);text-align:center}
.zipbar{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;color:var(--muted);font-size:14px;padding-top:10px}
.help{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.help div{border:1px solid var(--line);border-radius:10px;padding:12px 16px}
.help h3{margin:0 0 4px;font-size:18px}
.help p,.help ol{margin:0;font-size:15px;padding-inline-start:20px}
.help p{padding:0}
footer{margin-top:40px;border-top:1px solid var(--line);padding:18px 0 40px;color:var(--muted);font-size:14px}
[hidden]{display:none!important}
.vtools{margin:8px 0}
.vhint{margin:0;font-size:13px;color:var(--muted)}
.vgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;padding:10px 0 6px}
.vcard{border:1px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;background:#fff}
.vopen{display:block;position:relative;border:0;padding:0;margin:0;cursor:pointer;background:#1d2433;width:100%;aspect-ratio:16/9;text-decoration:none;overflow:hidden}
.vthumb{position:absolute;inset:0;display:grid;place-items:center;background:linear-gradient(135deg,#27324a,#1d2433)}
.vthumb img,.vthumb video{width:100%;height:100%;object-fit:cover;display:block}
.vthumb .vname{position:absolute;bottom:8px;inset-inline-start:10px;color:#e8edf8;font-size:13px;direction:ltr;opacity:.9}
.vplay{position:absolute;inset:0;margin:auto;width:54px;height:54px;border-radius:50%;background:rgba(232,134,28,.95);color:#fff;font-size:22px;display:grid;place-items:center;box-shadow:0 2px 10px rgba(0,0,0,.35);transition:transform .15s}
.vopen:hover .vplay,.vopen:focus-visible .vplay{transform:scale(1.12)}
.vplay.link{background:rgba(31,74,168,.95)}
.vinfo{padding:8px 12px 10px;display:flex;flex-direction:column;gap:3px;flex:1}
.vinfo h3{margin:0;font-size:16px;line-height:1.4}
.vinfo p{margin:0;font-size:13px;color:var(--muted)}
.vbadge{display:inline-block;font-size:12px;background:var(--soft);border:1px solid var(--line);border-radius:999px;padding:0 10px;align-self:flex-start}
.vdel{align-self:flex-start;font:inherit;font-size:13px;color:#a33;background:none;border:0;padding:0;cursor:pointer;text-decoration:underline}
.vdlg{width:min(960px,96vw);max-width:96vw;padding:12px 14px;border-radius:14px}
.vphead{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:8px}
.vphead h3{margin:0;font-size:19px;color:var(--ink)}
.vpbody{aspect-ratio:16/9;background:#000;border-radius:8px;overflow:hidden}
.vpbody iframe,.vpbody video{width:100%;height:100%;border:0;display:block}
.vpfoot{margin:8px 0 0;font-size:14px}
.srcsites{max-width:520px;grid-template-columns:repeat(3,1fr);margin:6px 0 12px}
.srctools{margin:6px 0}
.tgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;padding:10px 0}
.tcard{border:1px solid var(--line);border-radius:12px;padding:10px 12px;display:flex;flex-direction:column;gap:8px;background:#fff}
.tcard h3{margin:0;font-size:17px;display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.tcard h3 small{font-size:12px;color:var(--muted);direction:ltr;font-weight:400}
.tlinks{display:grid;grid-template-columns:1fr 1fr;gap:5px}
.tlinks .btn{font-size:13px;padding:4px 6px}
.tlinks .btn.vid{border-color:var(--orange);color:#a85a08}
.tlinks .btn.vid:hover{background:var(--orange);color:#fff}
.tnote{margin:6px 0 0;font-size:13px;color:var(--muted)}
.gamegrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px;padding:10px 0}
.progbox{margin:10px 0 4px;border:1px solid var(--line);border-radius:12px;padding:10px 16px;background:var(--soft)}
.progbox summary{cursor:pointer;font-size:18px;font-weight:700;color:var(--blue)}
.progbox h4{margin:14px 0 2px;font-size:17px;color:var(--ink)}
.progbox h5{margin:8px 0 2px;font-size:15px}
.progbox ul{margin:2px 0 6px;padding-inline-start:22px}
.progbox .pnote{font-size:13px;color:var(--muted);margin:8px 0 0}
.lvl{display:inline-block;background:var(--blue);color:#fff;border-radius:999px;padding:0 10px;font-size:12px;margin-inline-end:4px}
.chips2{display:flex;flex-wrap:wrap;gap:4px;margin:2px 0}
.chips2 span{font-size:11.5px;border:1px solid var(--line);border-radius:999px;padding:0 8px;background:#fff;color:var(--muted)}
.box2{border-top:1px dashed var(--line);padding-top:8px;margin-top:4px}
.ficheln{font-size:14px;margin-inline-start:12px;font-weight:400}
.gcat{margin:26px 0 4px;font-size:22px;color:var(--blue);border-bottom:2px solid var(--orange);padding-bottom:2px;display:inline-block}
.gcard{border:1px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;background:#fff}
.gcover{aspect-ratio:16/9;background:var(--soft);display:block;width:100%;object-fit:cover}
.gbody{padding:10px 14px 12px;display:flex;flex-direction:column;gap:6px;flex:1}
.gbody h3{margin:0;font-size:18px}
.gbody p{margin:0;font-size:14px;color:var(--muted)}
.gbody .btns{margin-top:auto}
.sr{position:absolute;left:-9999px}
:focus-visible{outline:3px solid var(--orange);outline-offset:2px}
@media (max-width:560px){.btns{grid-template-columns:1fr}}
.spaces{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin:10px 0}
.space{border:1px solid var(--line);border-radius:12px;padding:12px 16px;background:#fff;display:flex;flex-direction:column;gap:8px}.space.t{border-color:#1e6fd6;background:#f4f8ff}
.qz{border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin:8px 0;background:#fff}.qz p{margin:0 0 6px;font-weight:600}
.qz .opts{display:flex;flex-direction:column;gap:6px}.qz button.o{font:inherit;text-align:start;border:1px solid var(--line);background:#fff;border-radius:8px;padding:6px 10px;cursor:pointer}
.qz button.o:disabled{cursor:default}.qz button.o.ok{background:#e4f6e8;border-color:#2e9b4e}.qz button.o.ko{background:#fdeaea;border-color:#d33}.qz .fb{margin-top:6px;font-size:14px}
.score{font-weight:700;color:#1e3a6e;margin:6px 0}.sctable{width:100%;border-collapse:collapse;font-size:14px}.sctable th,.sctable td{border:1px solid var(--line);padding:4px 8px;text-align:start}.sctable th{background:#eaf1fb}.sctable tr.ev td{background:#fde8e8}.sctable tr.pr td{background:#e8f5e9}
.dlchips{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}.chip{font:inherit;border:1px solid var(--line);background:#fff;border-radius:999px;padding:3px 14px;cursor:pointer}.chip[aria-pressed=true]{background:#1e4fa8;color:#fff;border-color:#1e4fa8}
.dlgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}.dlcard{border:1px solid var(--line);border-radius:12px;padding:12px 14px;background:#fff;display:flex;flex-direction:column;gap:6px}.dlcard h4{margin:0;font-size:17px}.dlcard p{margin:0;font-size:14px;flex:1}
.dlmeta{display:flex;flex-wrap:wrap;gap:6px;align-items:center}.dlmeta .os{font-size:12px;color:#666}
.space-d{margin-top:16px;border:1px solid var(--line);border-radius:10px;padding:0 14px}.space-d>summary{cursor:pointer;font-weight:700;font-size:18px;color:#1e3a6e;padding:10px 0}.space-d[open]>summary{border-bottom:1px solid var(--line);margin-bottom:6px}
.step{border:1px solid var(--line);border-radius:10px;margin:8px 0;background:#fff}.step>summary{cursor:pointer;padding:9px 12px;display:flex;align-items:center;gap:10px;font-size:16px}
.step[open]>summary{border-bottom:1px solid var(--line)}.stbody{padding:6px 14px 12px}.stbody h5{margin:10px 0 4px;color:#1e3a6e}.stbody ol,.stbody ul{margin:0;padding-inline-start:22px;display:flex;flex-direction:column;gap:4px}
.badge{background:#1e4fa8;color:#fff;border-radius:999px;min-width:26px;height:26px;display:inline-flex;align-items:center;justify-content:center;font-size:14px;padding:0 8px}.badge.pj{background:#e8a21c;color:#222;letter-spacing:1px}
.stbody .check{list-style:none;padding:0}.stbody .check li::before{content:"";display:inline-block;width:12px;height:12px;border:2px solid #1e4fa8;border-radius:3px;margin-inline-end:8px;vertical-align:-1px}
#games.only-grid>h2,#games.only-grid>.lead,#games.only-grid>.progbox,#games.only-grid>#extGames{display:none}
.fiche h3{margin:16px 0 4px;color:#1e3a6e}.fiche .sit{background:#f4f8ff;border-left:4px solid #1e4fa8;padding:6px 10px;margin:0}.figgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.figgrid figure{margin:0;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:#fff}.figgrid img{width:100%;height:auto;display:block}.figgrid figcaption{padding:8px 10px;display:flex;flex-direction:column;gap:3px;font-size:14px}
.rprev{width:100%;max-height:150px;object-fit:contain;background:#f4f8ff;border-radius:8px}audio.rprev{height:40px}
.blkrow{display:flex;flex-wrap:wrap;gap:5px}.blk{color:#fff;font-weight:600;font-size:13px;line-height:1.3;padding:4px 10px;border-radius:6px;text-shadow:0 1px 0 rgba(0,0,0,.25)}
.blk.ev{background:#c78a00}.blk.mv{background:#3f7ee0}.blk.lk{background:#8a55d7}.blk.sn{background:#b448b0}.blk.ct{background:#d68a00}.blk.se{background:#2a9fc9}.blk.op{background:#3fa854}.blk.va{background:#e0592a}.blk.pen{background:#0f9e7a}
.lvlf{margin-inline-start:auto;font-size:13px;color:#666;border:1px solid var(--line);border-radius:999px;padding:0 10px}.defi{background:#fff6e0;border-radius:6px;padding:4px 10px}.step.lvlbox>summary{font-size:17px}
@media (min-width:761px) and (max-width:1150px){.ybtn{padding:0 9px;font-size:15px}}
.actlevels{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px;margin:10px 0}.actlvl{border:1px solid var(--line);border-radius:12px;padding:12px 14px;background:#fff;display:flex;flex-direction:column;gap:6px}.actlvl h4{margin:0;font-size:16px}.actlvl p{margin:0;font-size:14px}.actlvl .btn{align-self:flex-start}
.acthead{display:flex;align-items:center;gap:10px;flex-wrap:wrap}.actpage h3{margin:18px 0 6px;color:#1e3a6e}.blkhelp{display:flex;align-items:flex-start;gap:10px;margin:6px 0;flex-wrap:wrap}.blkhelp .blk{flex:none}.blkhelp p{margin:0;flex:1;min-width:200px;font-size:15px}
.scriptimg{overflow-x:auto;border:1px solid var(--line);border-radius:10px;padding:8px;background:#fff;text-align:start}.scriptimg img{max-width:100%;height:auto;display:block}
.bigsteps{padding-inline-start:24px;display:flex;flex-direction:column;gap:6px;font-size:16px}.tip{background:#eaf6ff;border-radius:8px;padding:6px 12px;margin:8px 0}
.figpair{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}.figpair figure{margin:0;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:#fff}.figpair img{width:100%;height:auto;display:block}.figpair figcaption{padding:6px 10px;font-weight:700;color:#1e3a6e}
.actnav{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
a.chip{text-decoration:none;color:inherit}a.chip[aria-pressed=true]{color:#fff}
.actcard{position:relative}.actlink{display:flex;flex-direction:column;color:inherit;text-decoration:none;flex:1}
.actdone{display:flex;gap:6px;align-items:center;padding:0 12px 12px;font-size:13px;font-weight:700;color:#555;cursor:pointer;margin-top:auto}
.actcb{width:18px;height:18px;accent-color:#2e9e5b;cursor:pointer;margin:0}.actcard.is-done{border-color:#2e9e5b;box-shadow:0 0 0 2px rgba(46,158,91,.4)}.actcard.is-done .actdone{color:#1d6b3b}
.actprog{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:8px 0 4px}.allprog{font-weight:700;color:#1d6b3b}.actbar{flex:1;min-width:140px;max-width:420px;height:10px;background:#e3eaf6;border-radius:999px;overflow:hidden}.actbar>i{display:block;height:100%;background:#2e9e5b;width:0;transition:width .25s}
.lvlprog{font-size:13px;font-weight:700;color:#1d6b3b;background:#e4f6e8;border-radius:999px;padding:0 10px}.donebtn{margin-inline-start:auto}.donebtn[aria-pressed=true]{background:#2e9e5b;color:#fff;border-color:#2e9e5b}.actcard[data-l="6"]{border-top-color:#0f9e7a}
.blk.my{background:#FF6680}
.actsec{margin:22px 0 8px;scroll-margin-top:calc(var(--barh) + 12px)}.actsec .acthead h3{margin:0;font-size:19px;color:#1e3a6e}.actsec>.pnote{margin:4px 0 10px}
.actgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px}
.actcard{display:flex;flex-direction:column;border:1px solid var(--line);border-top:5px solid #1e4fa8;border-radius:12px;overflow:hidden;background:#fff;text-decoration:none;color:inherit;transition:transform .12s,box-shadow .12s}
.actcard:hover,.actcard:focus-within{transform:translateY(-3px);box-shadow:0 6px 16px rgba(30,58,110,.18)}
.actcard[data-l="1"]{border-top-color:#2e9e5b}.actcard[data-l="2"]{border-top-color:#1e6fd6}.actcard[data-l="3"]{border-top-color:#e8861c}.actcard[data-l="4"]{border-top-color:#c0392b}.actcard[data-l="5"]{border-top-color:#8a55d7}
.actthumb{position:relative;aspect-ratio:4/3;background:#eef3fb}.actthumb img{width:100%;height:100%;object-fit:cover;display:block}.actthumb .badge{position:absolute;top:8px;right:8px;box-shadow:0 1px 4px rgba(0,0,0,.3)}
@media (max-width:600px){.actgrid{grid-template-columns:repeat(2,1fr);gap:10px}.actcard h4{font-size:13.5px;padding:8px 9px 10px}}
.actcard h4{margin:0;padding:10px 12px 12px;font-size:15px;line-height:1.4;color:#1e3a6e;text-align:start}
.planpage h3{margin:20px 0 6px;color:#1e3a6e}.mxwrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:#fff}
.mx{border-collapse:collapse;width:100%;font-size:14px;table-layout:fixed}.mx th:first-child,.mx td:first-child{width:27%}.mx th:nth-child(2):not(:last-child){}.lvlprog,.allprog,[data-sc-acts]{direction:ltr;unicode-bidi:isolate}.mx th,.mx td{border:1px solid var(--line);padding:4px 8px;text-align:center}.mx th{background:#eaf1fb;color:#1e3a6e}.mx td.mxn{text-align:start;font-weight:600;white-space:nowrap}.mx td.mxk{color:#2e9e5b;font-weight:700}
.mx-n{color:#1d6b3b;font-weight:700;background:#e4f6e8}.mx-d{color:#1e4fa8;font-weight:700;background:#e6efff}.mx-r{color:#777;background:#f6f6f6}td.mx-n,td.mx-d,td.mx-r{font-size:16px}.lg{padding:0 6px;border-radius:6px}
.nchip{display:inline-block;border-radius:999px;padding:1px 10px;font-size:13px;margin:2px 0}.nchip.n{background:#e4f6e8;color:#1d6b3b}.nchip.d{background:#e6efff;color:#1e4fa8}.nchip.r{background:#f0f0f0;color:#555}
.autopill{font-size:12px;font-weight:700;border-radius:999px;padding:0 10px;color:#fff}.autopill.guide{background:#6aa9ff}.autopill.semi{background:#2f6fd6}.autopill.auto{background:#1b3a82}
.phases td,.phases th{vertical-align:top;text-align:start}.phases td.n{white-space:nowrap}.gamerow{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:6px 0}.usesrow{margin:6px 0}
.actgrid.mini{grid-template-columns:repeat(auto-fill,minmax(165px,1fr));gap:10px}.rolerow{display:flex;flex-wrap:wrap;gap:6px 22px}.rolegrp{flex:1 1 180px}.actgrid.mini .actcard h4{font-size:13.5px;padding:7px 9px 6px}
@media print{.topbar,#yearnav,#axisBack,.dlchips,.actprog,footer,.hero,.langbtn{display:none!important}body{background:#fff}.planpage .step{break-inside:avoid;page-break-inside:avoid}.actdone,.actcb{display:none}.actgrid.mini{grid-template-columns:repeat(4,1fr)}}
.instbtns{display:flex;flex-direction:column;gap:8px}.instrow{display:flex;flex-wrap:wrap;align-items:center;gap:8px}.instrow .mine{font-size:12px;font-weight:700;color:#1d6b3b;background:#e4f6e8;border-radius:999px;padding:0 10px}
#getinst{font-size:16px;padding:8px 18px;white-space:nowrap}
.cahierbox{border:2px solid #1e4fa8;border-radius:12px;padding:6px 16px 12px;margin:16px 0;background:#f4f8ff}.cahierbox h3{margin:6px 0 4px;color:#1e4fa8;font-size:18px}.cahierbtns{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}.cahierbtns .btn{min-width:150px}
.pdfrow{margin:6px 0}html[lang=fr] .pdf-ar,html:not([lang=fr]) .pdf-fr{display:none}
/*__THEORIE_CSS__*/
</style>
</head>
<body>
<header class="topbar" id="top">
  <a class="brand" href="#home">Curriculum Informatique en Tunisie</a>
  <nav class="yearnav" id="yearnav" aria-label="القائمة الرئيسية"></nav>
  <div class="barbtns">
    <button type="button" class="langbtn" data-lang="ar" aria-label="العربية">AR</button>
    <button type="button" class="langbtn" data-lang="fr" aria-label="Français">FR</button>
  </div>
</header>
<section class="hero" id="hero"><div class="wrap">
  <div class="head"><h1>Curriculum Informatique en Tunisie</h1>
  <div class="hbtns"><a class="btn alt" id="getscratch" href="#downloads">⬇ التحميلات: سكراتش وبقية البرمجيات</a>
  <a class="btn main" id="getinst" href="#downloads">⬇ تثبيت سكراتش على الحاسوب</a>
  <a class="btn" href="https://scratch.mit.edu/projects/editor/" target="_blank" rel="noopener">فتح سكراتش على الإنترنت</a>
  <button type="button" class="btn main" id="install" hidden>⬇ اختصار على سطح المكتب</button></div></div>
  <p>المنهاج والمراجع والموارد التعليمية لمادة الإعلامية في تونس، من السنة السابعة إلى السنة التاسعة.</p>
</div></section>

<main class="wrap">
<div id="viewHome">
<section id="years"><h2>المحاور الدراسية حسب السنة</h2><p class="lead">اختر سنتك، ثم المحور الذي تريد دراسته.</p><div class="yearcards" id="yearCards"></div></section>
<section id="start">
  <h2>كيف أبدأ؟</h2>
  <p class="lead">أربع خطوات بسيطة.</p>
  <ol class="steps">
    <li>اختر سنتك ثم المحور الذي تريد دراسته من القائمة أعلاه.</li>
    <li>حمّل <b>ورقة المشروع</b> واقرأها: فيها الملخص والسيناريو وخطوات العمل.</li>
    <li>افتح <b>سكراتش</b> (<a href="#downloads">حمّله من صفحة التحميلات</a>) ثم «ملف ← تحميل من حاسوبك» واختر ملف المشروع (.sb3).</li>
    <li>غيّر الصور والأصوات والحوارات من <b>المكتبة</b> لتصنع مشروعك الخاص.</li>
  </ol>
</section>
<details class="helpbox" id="help"><summary>مساعدة</summary>
  <div class="help">
    <div><h3>أضيف صورة جديدة</h3><ol><li>في سكراتش، اضغط على «اختيار لاعب» ثم «رفع لاعب».</li><li>اختر ملف الصورة (.svg) من المجلد.</li></ol></div>
    <div><h3>أضيف مكانًا (خلفية)</h3><ol><li>اضغط على «اختيار خلفية» ثم «رفع خلفية».</li><li>اختر ملفًا من «الأماكن».</li></ol></div>
    <div><h3>أضيف صوتًا</h3><ol><li>افتح لسان «الأصوات» في اللاعب.</li><li>اضغط «رفع صوت» واختر ملف (.wav).</li><li>استعمل الكتلة «ابدأ الصوت».</li></ol></div>
    <div><h3>أصنع حركة</h3><ol><li>حمّل «إطارات» الحركة من تبويب الصور المتحركة.</li><li>فك الضغط، ثم ارفع الصور كأزياء متتالية للاعب.</li><li>استعمل «التالي الزي» داخل حلقة مع «انتظر».</li></ol></div>
    <div><h3>أسجّل صوتي</h3><p>الأصوات الجاهزة المسمّاة «أصوات جاهزة» مولَّدة آليًا. لتسجيل صوتك، افتح لسان «الأصوات» في سكراتش واضغط على الميكروفون.</p></div>
  </div>

</details>
</div>
<div id="viewAxis" hidden>
  <a class="back" id="axisBack" href="#home">← الرئيسية</a>
  <section id="axisHead"></section>
  <div id="resArea"></div>
</div>
<div id="viewStory" hidden>
  <a class="back" href="#y7-prog">← كل القصص</a>
  <section id="storyHead"></section>
  <div id="storyRes"></div>
</div>
<div id="pool" hidden>
<section id="theory"></section>
<section id="neuf"></section>
<section id="stories">
  <h2>اختر قصتك</h2>
  <p class="lead">لكل قصة ورقة مشروع، ومشروع سكراتش جاهز، وحزمة واحدة تجمع كل ما تحتاجه.</p>
  <div class="stories" id="storyGrid"></div>
</section>
<section id="games" class="only-grid">
  <h2>ألعاب سكراتش</h2>
  <p class="lead">ألعاب بسيطة وتعليمية: أسئلة وأجوبة، حساب، ذاكرة، وسرعة. حمّل اللعبة وافتحها في سكراتش، ثم عدّلها كما تشاء.</p>
  <details class="progbox" id="progBox"><summary>الربط بالمنهاج: الفكر المنطقي والبرمجة</summary><div id="progBody"></div></details>
  <div id="gameGrid"></div>
  <div class="gamegrid" id="extGames"></div>
</section>
<section id="library">
  <h2>الصور والأصوات والحركات</h2>
  <p class="lead">كل ما يخص هذه القصة. اضغط «تحميل» ثم أضف الملف في سكراتش.</p>
  <div class="tools">
    <div class="tabs" role="tablist" id="tabs"></div>
    <div class="row">
      <input type="search" id="q" placeholder="ابحث بالعربية أو بالفرنسية…" aria-label="بحث">
      <select id="story" hidden aria-label="تصفية حسب القصة"></select>
      <div class="subs" id="subs"></div>
    </div>
  </div>
  <div class="zipbar"><span id="count"></span><span id="zipwrap"></span></div>
  <div id="out"></div>
</section>
<section id="videos">
  <h2>فيديوهات</h2>
  <p class="lead">اضغط على لقطة الفيديو لمشاهدته هنا دون مغادرة الصفحة.</p>
  <div class="row vtools" id="vtools">
    <input type="search" id="vq" placeholder="ابحث في الفيديوهات…" aria-label="بحث في الفيديوهات">
    <select id="vstory" hidden aria-label="تصفية الفيديوهات حسب القصة"></select>
    <span id="vcount" class="small"></span>
  </div>
  <div class="vgrid" id="vgrid"></div>
</section>
<section id="sources">
  <h2>صور متحركة وفيديوهات جاهزة</h2>
  <p class="lead">مواقع مجانية فيها آلاف الصور والفيديوهات. اختر موضوعًا ليفتح لك البحث الجاهز في الموقع الذي تريده.</p>
  <div class="btns srcsites">
    <a class="btn main" href="https://www.pexels.com/fr-fr/" target="_blank" rel="noopener noreferrer">Pexels</a>
    <a class="btn main" href="https://mixkit.co/" target="_blank" rel="noopener noreferrer">Mixkit</a>
    <a class="btn main" href="https://pixabay.com/photos/" target="_blank" rel="noopener noreferrer">Pixabay</a>
  </div>
  <div class="row srctools">
    <input type="search" id="tq" placeholder="ابحث عن موضوع (غابة، بحر، قصر…)" aria-label="بحث عن موضوع">
    <select id="tstory" hidden aria-label="مواضيع حسب القصة"></select>
    <span id="tcount" class="small"></span>
  </div>
  <div class="tgrid" id="tgrid"></div>
  <p class="small tnote">الصور والفيديوهات تبقى في مواقعها الأصلية ولا تُنسخ في هذا المشروع. لكل موقع رخصته الخاصة، فاقرأ شروطه قبل التحميل، ولا تعد نشر الملفات كمكتبة مستقلة. نتائج البحث قد تتغير مع الوقت.</p>
</section>
</div>
</main>
<dialog id="vplayer" aria-labelledby="vpTitle" class="vdlg">
  <div class="vphead"><h3 id="vpTitle"></h3><button type="button" class="btn" id="vpClose" aria-label="إغلاق">✕ إغلاق</button></div>
  <div class="vpbody" id="vpBody"></div>
  <p class="vpfoot"><a id="vpOpen" href="#" target="_blank" rel="noopener"></a></p>
</dialog>
<dialog id="installHelp" aria-labelledby="ihTitle">
  <h3 id="ihTitle">اختصار على سطح المكتب</h3>
  <div id="ihBody"></div>
  <form method="dialog"><button class="btn main" style="margin-top:10px">حسنًا</button></form>
</dialog>
<footer><div class="wrap"><span dir="ltr" style="display:block">__BUILD__</span>الصور مرسومة خصيصًا لهذه الورشة، والأصوات والموسيقى مولَّدة بالحاسوب، ويمكنك استعمالها وتعديلها بحرّية في مشاريعك.</div></footer>

<script src="videos.js"></script>
<script src="jeux.js"></script>
<script src="references.js"></script>
<script src="logiciels.js"></script>
<script>
const DATA = __DATA__;
const FRMAP = __FRMAP__, FRRULES = __FRRULES__.map(([a,b]) => [new RegExp(a), b]);
const CATS = [
  {id:"lieux", name:"الأماكن", wide:true, hint:"خلفيات كاملة للمشاهد"},
  {id:"decors", name:"الديكور", hint:"أشياء تضعها في المشهد"},
  {id:"personnages", name:"الشخصيات"},
  {id:"animaux", name:"الحيوانات"},
  {id:"costumes", name:"الأزياء", subs:{accessoires:"إكسسوارات", tenues:"ملابس", variantes:"نسخ القصص"}},
  {id:"animations", name:"الصور المتحركة"},
  {id:"sons", name:"الأصوات", subs:{effets:"مؤثرات صوتية", musique:"موسيقى", voix:"أصوات جاهزة"}},
];
const $ = s => document.querySelector(s);
const el = (t, a={}, ...kids) => { const e = document.createElement(t); for (const k in a){ if(k==="class") e.className=a[k]; else if(k==="text") e.textContent=a[k]; else e.setAttribute(k,a[k]); } kids.flat(Infinity).forEach(c=>c&&e.append(c)); return e; };
const state = {cat:"lieux", sub:"", q:"", story:""};
// ---- lien avec le programme (Pensée logique et programmation)
const PRG = DATA.programme;
function chipsFor(pk){
  const p = PRG.projects[pk]; if (!p) return null;
  return el("div",{}, el("span",{class:"lvl",text: PRG.levels[String(p.level)].year_ar}), el("div",{class:"chips2"}, p.concepts.map(c => el("span",{text:PRG.concepts[c].ar}))));
}
function renderProgramme(){
  const b = $("#progBody"); b.replaceChildren();
  for (const n of ["7","8"]) {
    const L = PRG.levels[n];
    b.append(el("h4",{text:L.year_ar}), el("p",{text:L.comp_ar}));
    L.parts.forEach(x => b.append(el("h5",{text:x.t_ar}), el("ul",{}, x.i_ar.map(t => el("li",{text:t})))));
    b.append(el("h5",{text:"المعارف المرتبطة"}), el("ul",{}, L.know_ar.map(t => el("li",{text:t}))));
    b.append(el("h5",{text:"توجيهات الإطار"}), el("ul",{}, L.cad_ar.map(t => el("li",{text:t}))));
  }
  b.append(el("p",{class:"pnote",text:PRG.general_ar}), el("p",{class:"pnote",text:"النص منقول من صور الوثيقة الرسمية «المساعدة البيداغوجية: الإعلامية» (سبتمبر 2025)، فيُراجَع مع الوثيقة الأصلية."}));
}
renderProgramme();



// ---- histoires : une carte par conte ; un clic ouvre le conte et tout ce qui le concerne
const GENERAL = {key:"__general", title:"موارد عامة", summary:"صور وأصوات وحركات تصلح لأي قصة.", morale:"", main:"#44506a", accent:"#8a94aa"};
const grid = $("#storyGrid");
DATA.stories.concat([GENERAL]).forEach(s => {
  const link = "#story-" + (s.key === "__general" ? "general" : s.key);
  grid.append(el("article",{class:"card"},
    el("div",{class:"bar",style:`background:${s.accent}`}),
    el("div",{class:"body"},
      el("h3",{text:s.title,style:`color:${s.main}`}),
      el("p",{text:s.summary}),
      s.morale && el("div",{class:"morale",text:s.morale}),
      el("div",{class:"btns"}, el("a",{class:"btn main wide",href:link,text:"فتح القصة وكل ما يخصها"})))));
});

// ---- bibliothèque
const counts = {}; DATA.assets.forEach(a => counts[a.cat] = (counts[a.cat]||0)+1);
const tabs = $("#tabs");
CATS.forEach(c => tabs.append(el("button",{class:"tab",role:"tab",type:"button","data-cat":c.id},c.name,el("small",{text:counts[c.id]||0}))));
tabs.addEventListener("click", e => { const b=e.target.closest("[data-cat]"); if(!b) return; state.cat=b.dataset.cat; state.sub=""; render(); });
const sel = $("#story"); sel.append(el("option",{value:"",text:"كل القصص"})); DATA.stories.forEach(s => sel.append(el("option",{value:s.key,text:s.title})));
sel.addEventListener("change", () => { state.story = sel.value; render(); });
$("#q").addEventListener("input", e => { state.q = e.target.value.trim().toLowerCase(); render(); });

let audio = null, playBtn = null;
function stop(){ if(audio){ audio.pause(); audio=null;} if(playBtn){ playBtn.setAttribute("aria-pressed","false"); playBtn.textContent="▶"; playBtn=null; } }
function play(btn, file){
  if(playBtn===btn){ stop(); return; }
  stop(); audio = new Audio(file); playBtn = btn; btn.setAttribute("aria-pressed","true"); btn.textContent="■";
  audio.addEventListener("ended", stop); audio.play().catch(()=>stop());
}
function fname(a){ return (a.label||a.id).replace(/[\\/:*?"<>|«»؟!]/g,"").slice(0,60) + "." + a.ext; }
let timers = [];
function render(){
  stop(); timers.forEach(clearInterval); timers = [];
  const cat = CATS.find(c=>c.id===state.cat);
  tabs.querySelectorAll(".tab").forEach(b => b.setAttribute("aria-selected", b.dataset.cat===state.cat));
  const subs = $("#subs"); subs.replaceChildren();
  if(cat.subs){ subs.append(el("button",{class:"chip",type:"button","aria-pressed":String(!state.sub),"data-sub":"",text:"الكل"})); for(const k in cat.subs) subs.append(el("button",{class:"chip",type:"button","aria-pressed":String(state.sub===k),"data-sub":k,text:cat.subs[k]})); }
  let items = DATA.assets.filter(a => a.cat===state.cat && (!state.sub || a.sub===state.sub) && (!state.story || (state.story === "__general" ? !a.tags.length : a.tags.includes(state.story))) && (!state.q || (a.label+" "+(a.fr||"")+" "+a.id).toLowerCase().includes(state.q)));
  $("#count").textContent = items.length ? `${items.length} عنصر` : "";
  const zw = $("#zipwrap"); zw.replaceChildren();
  if(DATA.zips[state.cat]) zw.append(el("a",{class:"btn",href:DATA.zips[state.cat],download:`${cat.name}.zip`,text:`تحميل كل «${cat.name}» (.zip)`}));
  const out = $("#out"); out.replaceChildren();
  if(!items.length){ out.append(el("div",{class:"empty",text:"لا توجد نتائج. جرّب كلمة أخرى أو اختر «كل القصص»."})); return; }
  if(state.cat==="sons"){
    const g = el("div",{class:"sounds"});
    items.forEach(a => {
      const b = el("button",{class:"play",type:"button","aria-pressed":"false","aria-label":"استمع: "+a.label,text:"▶"});
      b.addEventListener("click", () => play(b, a.file));
      g.append(el("div",{class:"tile sound"}, b, el("div",{class:"nm"}, el("span",{text:a.label}), el("span",{class:"meta",text:(a.fr?a.fr+" · ":"")+a.dur+" ث"})),
        el("a",{class:"btn dl",href:a.file,download:fname(a),text:"تحميل"})));
    });
    out.append(g); return;
  }
  const g = el("div",{class:"grid"+(cat.wide?" wideg":"")});
  items.forEach(a => {
    const img = el("img",{src:a.file,alt:a.label,loading:"lazy"});
    if(a.frames){ let i=0; timers.push(setInterval(()=>{ i=(i+1)%a.frames.length; img.src=a.frames[i]; }, 1000/a.fps/1.0*1.2)); }
    const t = el("div",{class:"tile"}, el("div",{class:"pv"}, img), el("div",{class:"nm",text:a.label}),
      a.frames ? el("a",{class:"btn dl",href:a.zip,download:`${a.label}.zip`,text:`تحميل الإطارات (${a.frames.length})`}) : el("a",{class:"btn dl",href:a.file,download:fname(a),text:"تحميل"}));
    g.append(t);
  });
  out.append(g);
}
$("#subs").addEventListener("click", e => { const b=e.target.closest("[data-sub]"); if(!b) return; state.sub=b.dataset.sub; render(); });
render();

// ---- فيديوهات : مكتبة لقطات الشاشة، والمشاهدة داخل الصفحة (la vidéo reste chez son hébergeur)
const VOPT = Object.assign({autoThumbnails:true}, window.VIDEOS_OPTIONS||{});
function embedInfo(raw){
  raw = (raw||"").trim();
  const m = raw.match(/<iframe[^>]*\s+src=["']([^"']+)["']/i); if (m) raw = m[1];
  if (raw.startsWith("//")) raw = "https:" + raw;
  let u; try { u = new URL(raw); } catch(e){ return null; }
  if (!/^https?:$/.test(u.protocol)) return null;
  const h = u.hostname.replace(/^(www|m|music)\./,""), p = u.pathname, q = u.searchParams;
  const t = parseInt(q.get("t")||q.get("start")||"0",10) || 0;
  const yt = id => ({kind:"iframe", host:"YouTube", id, thumb:`https://i.ytimg.com/vi/${id}/hqdefault.jpg`, src:`https://www.youtube-nocookie.com/embed/${id}?rel=0${t?`&start=${t}`:""}`});
  if (h === "youtu.be") { const id = p.slice(1).split("/")[0]; return id ? yt(id) : null; }
  if (h === "youtube.com" || h === "youtube-nocookie.com") {
    if (p === "/watch" && q.get("v")) return yt(q.get("v"));
    const mm = p.match(/^\/(embed|shorts|live|v)\/([\w-]{6,})/); if (mm && mm[2] !== "videoseries") return yt(mm[2]);
    if ((p === "/playlist" || mm) && q.get("list")) return {kind:"iframe", host:"YouTube", src:`https://www.youtube-nocookie.com/embed/videoseries?list=${encodeURIComponent(q.get("list"))}`};
    return null;
  }
  if (h === "vimeo.com" || h === "player.vimeo.com") { const id = (p.match(/(\d{5,})/)||[])[1]; return id ? {kind:"iframe", host:"Vimeo", id, oembed:`https://vimeo.com/api/oembed.json?url=${encodeURIComponent("https://vimeo.com/"+id)}`, src:`https://player.vimeo.com/video/${id}`} : null; }
  if (h === "dailymotion.com" || h === "dai.ly") { const id = h === "dai.ly" ? p.slice(1) : (p.match(/\/video\/([a-z0-9]+)/i)||[])[1]; return id ? {kind:"iframe", host:"Dailymotion", id, api:`https://api.dailymotion.com/video/${id}?fields=thumbnail_480_url`, src:`https://www.dailymotion.com/embed/video/${id}`} : null; }
  if (h === "archive.org") { const id = (p.match(/^\/(?:details|embed)\/([^/]+)/)||[])[1]; return id ? {kind:"iframe", host:"Internet Archive", thumb:`https://archive.org/services/img/${id}`, src:`https://archive.org/embed/${id}`} : null; }
  if (h === "drive.google.com") { const id = (p.match(/\/file\/d\/([\w-]+)/)||[])[1] || q.get("id"); return id ? {kind:"iframe", host:"Google Drive", thumb:`https://drive.google.com/thumbnail?id=${id}&sz=w480`, src:`https://drive.google.com/file/d/${id}/preview`} : null; }
  if (h === "ted.com" || h === "embed.ted.com") { const mm = p.match(/\/talks\/([^/?]+)/); return mm ? {kind:"iframe", host:"TED", src:`https://embed.ted.com/talks/${mm[1]}`} : null; }
  if (h === "facebook.com" || h === "fb.watch") return {kind:"iframe", host:"Facebook", src:`https://www.facebook.com/plugins/video.php?href=${encodeURIComponent(u.href)}&show_text=false`};
  if (/\.(mp4|webm|ogv|ogg)$/i.test(p)) return {kind:"video", host:h, src:u.href};
  if (/\/embed\//i.test(p) || /^player\./.test(h)) return {kind:"iframe", host:h, src:u.href};
  return {kind:"link", host:h, src:u.href};
}
const TKEY = "ateliers-contes-thumbs";
const thumbCache = () => { try { return JSON.parse(localStorage.getItem(TKEY)||"{}"); } catch(e){ return {}; } };
const setThumbCache = (k,v) => { try { const c = thumbCache(); c[k] = v; localStorage.setItem(TKEY, JSON.stringify(c)); } catch(e){} };
const vsel = $("#vstory"), vq = $("#vq");
vsel.append(el("option",{value:"",text:"كل القصص"}));
DATA.stories.forEach(s => vsel.append(el("option",{value:s.key,text:s.title})));

// image de couverture : capture fournie > miniature du site > aperçu local > cadre neutre
async function remoteThumb(info){
  if (info.thumb) return info.thumb;
  const key = info.host + ":" + info.id, c = thumbCache(); if (c[key]) return c[key];
  try {
    let url = "";
    if (info.oembed) url = (await (await fetch(info.oembed)).json()).thumbnail_url;
    else if (info.api) url = (await (await fetch(info.api)).json()).thumbnail_480_url;
    if (url) { setThumbCache(key, url); return url; }
  } catch(e){}
  return "";
}
function coverFor(v, info, title){
  const box = el("div",{class:"vthumb"});
  const fallback = () => { box.classList.add("nocover"); box.querySelector("img,video")?.remove(); box.prepend(el("span",{class:"vname",text:info ? info.host : "فيديو"})); };
  if (v.image) { const i = el("img",{src:v.image,alt:title,loading:"lazy"}); i.addEventListener("error", fallback); box.append(i); }
  else if (info && info.kind === "video") box.append(el("video",{src:info.src+"#t=0.6",preload:"metadata",muted:"",playsinline:"","aria-hidden":"true"}));
  else if (info && VOPT.autoThumbnails) {
    remoteThumb(info).then(url => { if (!url) return fallback(); const i = el("img",{src:url,alt:title,loading:"lazy",referrerpolicy:"no-referrer"}); i.addEventListener("error", fallback); box.prepend(i); });
  } else fallback();
  return box;
}
const dlg2 = $("#vplayer");
function openPlayer(v, info, title){
  const body = $("#vpBody"); body.replaceChildren();
  $("#vpTitle").textContent = title;
  if (info.kind === "video") body.append(el("video",{src:info.src,controls:"",autoplay:"",playsinline:"","aria-label":title}));
  else body.append(el("iframe",{src:info.src,title,allow:"autoplay; fullscreen; picture-in-picture; encrypted-media",allowfullscreen:"",referrerpolicy:"strict-origin-when-cross-origin"}));
  const o = $("#vpOpen"); o.href = v.url; o.textContent = "فتح في الموقع الأصلي (" + info.host + ")";
  dlg2.showModal();
}
function closePlayer(){ if (dlg2.open) dlg2.close(); $("#vpBody").replaceChildren(); }
dlg2.addEventListener("close", () => $("#vpBody").replaceChildren());
dlg2.addEventListener("click", e => { if (e.target === dlg2) closePlayer(); });
$("#vpClose").addEventListener("click", closePlayer);

function renderVideos(){
  const g = $("#vgrid"); g.replaceChildren();
  const q = vq.value.trim().toLowerCase();
  const all = (window.VIDEOS||[]).filter(v => (!vsel.value || (vsel.value === "__general" ? !v.story : v.story === vsel.value)) && (!q || ((v.title||"")+" "+(v.note||"")).toLowerCase().includes(q)));
  $("#vcount").textContent = all.length ? `${all.length} فيديو` : "";
  $("#vtools").hidden = !(window.VIDEOS||[]).length;
  if (!all.length) { g.append(el("div",{class:"empty",text: (window.VIDEOS||[]).length ? "لا توجد فيديوهات مطابقة." : "لا توجد فيديوهات حاليًا."})); return; }
  all.forEach(v => {
    const info = embedInfo(v.url); const st = DATA.stories.find(s=>s.key===v.story);
    const title = v.title || (info ? info.host : "فيديو");
    const thumb = coverFor(v, info, title);
    const canPlay = info && info.kind !== "link";
    const trigger = canPlay ? el("button",{class:"vopen",type:"button","aria-label":"مشاهدة: "+title}, thumb, el("span",{class:"vplay",text:"▶"})) : el("a",{class:"vopen",href:v.url,target:"_blank",rel:"noopener","aria-label":"فتح: "+title}, thumb, el("span",{class:"vplay link",text:"↗"}));
    if (canPlay) trigger.addEventListener("click", () => openPlayer(v, info, title));
    const meta = el("div",{class:"vinfo"}, st && el("span",{class:"vbadge",text:st.title}), el("h3",{text:title}), v.note && el("p",{text:v.note}));
    g.append(el("article",{class:"vcard"}, trigger, meta));
  });
}
vsel.addEventListener("change", renderVideos); vq.addEventListener("input", renderVideos);
renderVideos();

// ---- مواضيع جاهزة : روابط بحث نحو Pexels و Mixkit و Pixabay (rien n'est copié ici)
const THEMES = [
 ["غابة","forest",["layla","crow","lion","hare","shepherd"]],["قصر","castle",["cinderella","frog"]],["بحر","sea waves",["sindbad"]],["سفينة","sailing ship",["sindbad"]],
 ["جزيرة","tropical island",["sindbad"]],["صحراء","desert",["alibaba","sindbad"]],["جبل","mountain",["alibaba"]],["كهف","cave",["alibaba"]],["كنز وذهب","gold coins treasure",["alibaba"]],
 ["ليل ونجوم","night sky stars",["cinderella"]],["ساعة","clock",["cinderella"]],["سحر ولمعان","magic sparkles",["cinderella"]],["حفلة ورقص","ball dance",["cinderella"]],
 ["حديقة","garden flowers",["frog","cinderella"]],["بئر","old well",["frog"]],["مزرعة","farm",["pigs","duckling","shepherd"]],["مرعى وتلال","green hills pasture",["shepherd"]],
 ["قرية","village",["djeha","shepherd"]],["سوق","market",["djeha","alibaba"]],["جسر ونهر","bridge river",["djeha"]],["بيت","house",["pigs","layla"]],
 ["مطر","rain",["duckling"]],["ثلج وشتاء","snow winter",["duckling"]],["ربيع","spring blossom",["duckling","hare"]],["نار","fire flames",["alibaba"]],["ريح","wind",["pigs"]],
 ["ذئب","wolf",["layla","pigs","shepherd"]],["أسد","lion",["lion"]],["فأر","mouse",["lion"]],["أرنب","rabbit hare",["hare"]],["سلحفاة","tortoise",["hare"]],
 ["ثعلب","fox",["crow"]],["غراب","crow bird",["crow"]],["ضفدع","frog",["frog"]],["بطة","duck",["duckling"]],["بجعة","swan",["duckling"]],["خروف وغنم","sheep",["shepherd"]],
 ["خنزير","pig",["pigs"]],["حمار","donkey",["djeha"]],["جمل","camel",["alibaba","sindbad"]],["حصان","horse",["cinderella"]],["فراشة","butterfly",[]],["عصفور","bird flying",[]],
 ["سباق","running race",["hare"]],["شجرة","tree",[]],["شمس وغيوم","sun clouds",[]],["أطفال يقرؤون","children reading",[]],["كتاب وقصص","storybook",[]]
];
const tsel = $("#tstory"), tq = $("#tq");
tsel.append(el("option",{value:"",text:"كل المواضيع"})); DATA.stories.forEach(s => tsel.append(el("option",{value:s.key,text:s.title})));
function themeLinks(q){
  const e = encodeURIComponent(q), d = e.replace(/%20/g,"-");
  return [
    ["Pexels صور", `https://www.pexels.com/search/${e}/`, ""], ["Pexels فيديو", `https://www.pexels.com/search/videos/${e}/`, "vid"],
    ["Pixabay صور", `https://pixabay.com/images/search/${e}/`, ""], ["Pixabay فيديو", `https://pixabay.com/videos/search/${e}/`, "vid"],
    ["Mixkit فيديو", `https://mixkit.co/free-stock-video/discover/${d}/`, "vid"]
  ];
}
function renderThemes(){
  const g = $("#tgrid"); g.replaceChildren();
  const q = tq.value.trim().toLowerCase();
  const items = THEMES.filter(t => (!tsel.value || tsel.value === "__general" || t[2].includes(tsel.value)) && (!q || (t[0]+" "+t[1]).toLowerCase().includes(q)));
  $("#tcount").textContent = items.length ? `${items.length} موضوع` : "";
  if (!items.length) { g.append(el("div",{class:"empty",text:"لا توجد مواضيع مطابقة."})); return; }
  items.forEach(t => g.append(el("article",{class:"tcard"}, el("h3",{}, el("span",{text:t[0]}), el("small",{text:t[1]})),
    el("div",{class:"tlinks"}, themeLinks(t[1]).map(([n,u,c]) => el("a",{class:"btn "+c,href:u,target:"_blank",rel:"noopener noreferrer",text:n}))))));
}
tsel.addEventListener("change", renderThemes); tq.addEventListener("input", renderThemes);
renderThemes();

// ---- installation / raccourci sur le bureau
const instBtn = $("#install"), dlg = $("#installHelp");
let deferred = null;
const standalone = () => matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;
const secure = location.protocol === "https:" || location.hostname === "localhost" || location.hostname === "127.0.0.1";
const ua = navigator.userAgent;
const OS = /android/i.test(ua) ? "android" : /iphone|ipad|ipod/i.test(ua) ? "ios" : /windows/i.test(ua) ? "windows" : /mac/i.test(ua) ? "mac" : "linux";
const TITLE = "ورشة القصص", FILE = "Atelier-contes";
if (!standalone()) instBtn.hidden = false;
// bouton d'accueil « installer Scratch » : lien direct vers l'installateur de ton système (Windows ou macOS), sinon vers la page Téléchargements
{ const gi = $("#getinst"), L = (window.LOGICIELS || []).find(s => s.links), m = L && L.links.find(l => l.os === OS);
  if (m) { gi.href = m.url; gi.removeAttribute("target"); gi.textContent = OS === "windows" ? "⬇ تثبيت سكراتش على Windows" : "⬇ تثبيت سكراتش على macOS"; } }
window.addEventListener("beforeinstallprompt", e => { e.preventDefault(); deferred = e; instBtn.hidden = false; });
window.addEventListener("appinstalled", () => { deferred = null; instBtn.hidden = true; });

// Fichier raccourci : fonctionne aussi en HTTP sur un réseau local (pas besoin de HTTPS).
function shortcut(){
  const url = location.href.split("#")[0];
  const esc = x => x.replace(/&/g,"&amp;").replace(/</g,"&lt;");
  if (OS === "windows") return {name: FILE + ".url", type: "application/octet-stream", text: "[InternetShortcut]\r\nURL=" + url + "\r\n"};
  if (OS === "mac") return {name: FILE + ".webloc", type: "application/xml", text: '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0"><dict><key>URL</key><string>' + esc(url) + '</string></dict></plist>\n'};
  return {name: FILE + ".desktop", type: "application/x-desktop", text: "[Desktop Entry]\nVersion=1.0\nType=Application\nName=" + TITLE + "\nExec=xdg-open " + url + "\nTerminal=false\nIcon=applications-education\nCategories=Education;\n"};
}
function download(f){
  const a = el("a",{href:URL.createObjectURL(new Blob([f.text],{type:f.type})),download:f.name}); document.body.append(a); a.click(); a.remove();
}
function showHelp(kids){ const body = $("#ihBody"); body.replaceChildren(...kids); dlg.showModal(); }
instBtn.addEventListener("click", async () => {
  if (deferred) { deferred.prompt(); try { await deferred.userChoice; } catch(e){} deferred = null; return; }
  if (OS === "ios") return showHelp([el("p",{text:"في آيفون وآيباد:"}), el("ul",{}, el("li",{text:"اضغط على زر المشاركة في Safari."}), el("li",{text:"اختر «إضافة إلى الشاشة الرئيسية»."}))]);
  if (OS === "android") return showHelp([el("p",{text:"في هاتف أندرويد:"}), el("ul",{}, el("li",{text:"اضغط على قائمة المتصفح (⋮)."}), el("li",{text:"اختر «إضافة إلى الشاشة الرئيسية»."}))]);
  const f = shortcut(); download(f);
  const where = OS === "windows" ? "اسحب الملف إلى سطح المكتب." : OS === "mac" ? "اسحب الملف إلى سطح المكتب أو إلى الـ Dock." : "انقله إلى سطح المكتب، ثم انقر عليه بالزر الأيمن واختر «السماح بالتشغيل».";
  const kids = [el("p",{text:"تم تنزيل ملف الاختصار «" + f.name + "». " + where}),
    el("p",{text:"عند النقر عليه يفتح الموقع في المتصفح مباشرة. إن ظهر تحذير أثناء التنزيل فاختر «الاحتفاظ بالملف»."})];
  if (!secure) kids.push(el("p",{class:"small",text:"ملاحظة: التثبيت كتطبيق مستقل يتطلب HTTPS. على شبكة محلية بدون HTTPS يعمل الاختصار بالشكل الموضّح أعلاه."}));
  showHelp(kids);
});
if ("serviceWorker" in navigator && secure) {
  const had = !!navigator.serviceWorker.controller;
  navigator.serviceWorker.register("sw.js").catch(() => {});
  navigator.serviceWorker.addEventListener("controllerchange", () => { if (had && !sessionStorage.getItem("sw-reloaded")) { try { sessionStorage.setItem("sw-reloaded","1"); } catch(e){} location.reload(); } });
}
// ---- jeux
/*__THEORIE_JS__*/
// ---- case « Fait » des activités Scratch : progression enregistrée dans ce navigateur (localStorage)
const DONE_KEY = "scratch-activites-faites";
const Done = (() => {
  let mem = []; try { const v = JSON.parse(localStorage.getItem(DONE_KEY) || "[]"); if (Array.isArray(v)) mem = v; } catch (e) {}
  const save = () => { try { localStorage.setItem(DONE_KEY, JSON.stringify(mem)); } catch (e) {} };
  return { has: n => mem.includes(n), toggle(n){ const i = mem.indexOf(n); if (i >= 0) mem.splice(i, 1); else mem.push(n); save(); return i < 0; },
           count: pred => DATA.activites ? DATA.activites.acts.filter(a => mem.includes(a.n) && (!pred || pred(a))).length : 0, reset(){ mem = []; save(); } };
})();
function updateProgress(){
  updateTheoryProgress();
  const D = DATA.activites; if (!D) return;
  document.querySelectorAll("[data-lvl-prog]").forEach(e => { const n = +e.dataset.lvlProg, L = D.levels.find(x => x.n === n); e.textContent = Done.count(a => a.lvl === n) + " / " + L.count; });
  document.querySelectorAll("[data-all-prog]").forEach(e => { e.textContent = Done.count() + " / " + D.total; });
  document.querySelectorAll(".actbar > i").forEach(e => { e.style.width = (100 * Done.count() / D.total) + "%"; });
  document.querySelectorAll("[data-sc-acts]").forEach(e => { const ns = e.dataset.scActs.split(",").filter(Boolean).map(Number); e.textContent = ns.filter(n => Done.has(n)).length + " / " + ns.length; });
  document.querySelectorAll("[data-act]").forEach(e => { const d = Done.has(+e.dataset.act); e.classList.toggle("is-done", d); const cb = e.querySelector("input.actcb"); if (cb) cb.checked = d; });
  document.querySelectorAll("button.donebtn").forEach(b => { const d = Done.has(+b.dataset.n); b.setAttribute("aria-pressed", String(d)); const t = d ? "تم ✓" : "علّم النشاط كمنجز"; if (b.textContent !== t && b.dataset.t !== t) { b.textContent = t; b.dataset.t = t; } });
}
const GAME_CATS = ["catch"];
function watchBtn(x){
  const b = el("button",{type:"button",class:"btn main",text:"شاهد فيديو اللعبة"});
  b.addEventListener("click", () => { openPlayer({url:x.video}, {kind:"video", host:"", src:x.video}, x.title_ar); $("#vpOpen").href = x.video; $("#vpOpen").textContent = "فتح الفيديو في نافذة جديدة"; });
  return b;
}
function resBtn(id){ return el("a",{class:"btn",href:"#ressources-" + id,text:"موارد اللعبة"}); }
function ficheBtn(fid, key){ return el("a",{class:"btn",href:"#fiche-" + fid + (key ? "-" + key : ""),text:"بطاقة النشاط"}); }
function renderGames(){
  const g = $("#gameGrid"); g.replaceChildren();
  GAME_CATS.forEach(cat => {
    const list = (DATA.games||[]).filter(x => x.cat === cat); if (!list.length) return;
    g.append(el("h3",{class:"gcat"}, el("span",{text:list[0].cat_ar}), null));
    const row = el("div",{class:"gamegrid"});
    list.forEach(x => row.append(el("article",{class:"gcard"},
      el("img",{class:"gcover",src:x.cover,alt:x.title_ar,loading:"lazy"}),
      el("div",{class:"gbody"}, el("h3",{text:x.title_ar}), el("p",{text:x.how_ar}),
        el("div",{class:"btns"}, watchBtn(x), x.fiche ? ficheBtn(x.fiche) : null, x.res ? resBtn(x.res) : null)))));
    g.append(row);
  });
  // activités Scratch : rubrique placée sous « Jeux Scratch »
  if (DATA.activites) {
    g.append(el("h3",{class:"gcat",style:"margin-top:28px"}, el("span",{text:"أنشطة سكراتش"}), null),
      el("p",{class:"pnote",text:DATA.activites.intro}),
      el("div",{class:"actlevels"}, DATA.activites.levels.map(L => el("article",{class:"actlvl"}, el("div",{class:"acthead"}, el("span",{class:"badge",text:L.n}), el("span",{class:"lvlf",text:L.diff})),
        el("h4",{text:L.t}), el("p",{text:L.obj}), el("p",{class:"pnote"}, el("span",{text:L.count_t}), " · ", el("b",{"data-lvl-prog":L.n})), el("a",{class:"btn main",href:"#activites-" + L.n,text:"فتح المستوى"})))),
      el("p",{}, el("a",{class:"btn",href:"#activites",text:"فتح المجموعة كاملة"})));
    updateProgress();
  }
  // jeux Scratch publiés sur scratch.mit.edu (liste dans jeux.js) : joués ici, sans quitter la page
  const ext = $("#extGames"); ext.replaceChildren();
  (window.JEUX||[]).forEach(j => {
    const id = ((j.url||"").match(/projects\/(\d+)/)||[])[1]; if (!id) return;
    if (j.fr) FRMAP[j.title] = j.fr;
    const info = {kind:"iframe", host:"Scratch", src:`https://scratch.mit.edu/projects/${id}/embed`};
    const b = el("button",{class:"btn main",type:"button",text:"العب هنا"});
    b.addEventListener("click", () => openPlayer({url:`https://scratch.mit.edu/projects/${id}/`}, info, j.title));
    ext.append(el("article",{class:"gcard"}, el("div",{class:"gbody"}, el("h3",{text:j.title}), j.note && el("p",{text:j.note}),
      el("div",{class:"btns"}, b, el("a",{class:"btn",href:`https://scratch.mit.edu/projects/${id}/`,target:"_blank",rel:"noopener",text:"فتح في سكراتش"})))));
  });
}
renderGames();


// ---- navigation : #home, #y7 / #y8 / #y9, #y7-env … #y9-prog, #story-<clé>
const CUR = DATA.curriculum, YEARS = CUR.order, MENU_YEARS = ["7", "8", "9"];   // menu principal : 7e, 8e et 9e seulement (les autres niveaux restent accessibles depuis l'accueil)
function renderStoryHead(key){
  const h = $("#storyHead"); h.replaceChildren();
  const s = key === "__general" ? GENERAL : DATA.stories.find(x => x.key === key); if (!s) return;
  const kids = [el("h2",{text:s.title,style:`color:${s.main}`}), el("p",{text:s.summary}), s.morale && el("div",{class:"morale",text:s.morale})];
  if (key !== "__general") kids.push(el("div",{class:"btns",style:"grid-template-columns:repeat(auto-fit,minmax(160px,1fr))"},
    el("a",{class:"btn main",href:s.docx,download:`ورقة ${s.title}.docx`,text:"ورقة المشروع (Word)"}),
    el("a",{class:"btn",href:s.doc,download:`ورقة ${s.title}.doc`,title:"للإصدارات القديمة من Word (2003 و2007)",text:"Word قديم (.doc)"}),
    el("a",{class:"btn",href:s.html,target:"_blank",rel:"noopener",text:"قراءة الورقة"}),
    el("a",{class:"btn",href:s.sb3,download:`${s.title}.sb3`,text:"مشروع سكراتش"}),
    el("a",{class:"btn",href:s.pack,download:`حزمة ${s.title}.zip`,text:"كل شيء (.zip)"}), ficheBtn("contes", s.key)));
  h.append(el("div",{class:"storyhead"}, el("div",{class:"sbar",style:`background:${s.accent}`}), el("div",{class:"sbody"}, kids)));
}

function setScope(key, cat){
  state.story = key; state.sub = ""; state.q = ""; $("#q").value = ""; vq.value = ""; tq.value = "";
  sel.value = vsel.value = tsel.value = key; state.cat = cat;
  render(); renderVideos(); renderThemes();
}
function showStory(key){
  const has = c => DATA.assets.some(a => a.cat === c && (key === "__general" ? !a.tags.length : a.tags.includes(key)));
  setScope(key, (CATS.find(c => has(c.id)) || CATS[0]).id);
  renderStoryHead(key);
}
// menu : une entrée par année, avec ses quatre axes
const ynav = $("#yearnav");
MENU_YEARS.forEach(y => {
  const Y = CUR.years[y];
  const ul = el("ul",{class:"sub"}, el("li",{class:"ov"}, el("a",{href:"#y"+y,text:"نظرة عامة"})), CUR.by_year[y].map(k => el("li",{}, el("a",{href:`#y${y}-${k}`,"data-ax":k,text:CUR.pages[`${y}-${k}`].title_ar}))), el("li",{class:"ov"}, el("a",{href:`#y${y}-ens`,text:"فضاء الأستاذ"})), TH.years.includes(y) ? el("li",{class:"ov"}, el("a",{href:"#theorie",text:U.hubTitle})) : null, y === "8" ? el("li",{class:"ov"}, el("a",{href:"#securite",text:SU.title})) : null, el("li",{class:"ov"}, el("a",{href:`#planning-${y}`,text:y === "9" ? "تخطيط الحصص" : "تخطيط حصص سكراتش"})), el("li",{class:"ov"}, el("a",{href:`cahier/cahier-${y}.html`,target:"_blank",rel:"noopener",text:"مذكرات الدفتر"})), el("li",{class:"ov"}, el("a",{href:`#y${y}-refs`,text:"المراجع"})));
  const btn = el("button",{class:"ybtn",type:"button","aria-expanded":"false","aria-haspopup":"true"}, el("span",{class:"yl",text:Y.ar}), el("span",{class:"ys",text:Y.short_ar}), el("i",{class:"car",text:"▾"}));
  const d = el("div",{class:"ydrop","data-year":y}, btn, ul);
  btn.addEventListener("click", e => { e.stopPropagation(); const open = !d.hasAttribute("data-open"); closeMenus(); if (open) { d.setAttribute("data-open",""); btn.setAttribute("aria-expanded","true"); } });
  ynav.append(d);
});
function closeMenus(){ ynav.querySelectorAll(".ydrop").forEach(d => { d.removeAttribute("data-open"); d.querySelector(".ybtn").setAttribute("aria-expanded","false"); }); }
document.addEventListener("click", e => { if (!e.target.closest(".ydrop")) closeMenus(); else if (e.target.closest(".sub a")) closeMenus(); });
document.addEventListener("keydown", e => { if (e.key === "Escape") closeMenus(); });

function axisLinks(y){ return CUR.by_year[y].map(k => el("li",{}, el("a",{href:`#y${y}-${k}`,text:CUR.pages[`${y}-${k}`].title_ar}))).concat(TH.years.includes(y) ? [el("li",{}, el("a",{href:"#theorie",text:U.hubTitle}))] : [], y === "8" ? [el("li",{}, el("a",{href:"#securite",text:SU.title}))] : [], [el("li",{}, el("a",{href:`#y${y}-refs`,style:"font-weight:700",text:"المراجع"}))]); }
function renderHome(){
  const c = $("#yearCards"); c.replaceChildren();
  MENU_YEARS.forEach(y => c.append(el("article",{class:"ycard"}, el("a",{class:"yh",href:"#y"+y,style:"text-decoration:none",text:CUR.years[y].ar}), el("ul",{}, axisLinks(y)))));
}
renderHome();
// ressources proposées dans chaque axe
const RES = {"7-prog":["theory","stories"], "8-prog":["games"], "9-prog":["neuf"], "7-create":["library","sources"], "8-create":["library","videos","sources"], "7-net":["sources"]};
const RESCAT = {"7-create":"personnages", "8-create":"sons"};
function park(){ ["#resArea","#storyRes"].forEach(sl => [...$(sl).children].forEach(n => { if (n.classList && n.classList.contains("tmp")) n.remove(); else if (n.classList && n.classList.contains("libwrap")) { [...n.children].filter(c => c.id).forEach(c => $("#pool").append(c)); n.remove(); } else $("#pool").append(n); })); }
function quiz(list){
  let done = 0, good = 0; const sc = el("p",{class:"score"}); const box = el("div",{});
  const qs = list.map(q => {
    const fb = el("p",{class:"fb"}), ord = q.o.map((_, i) => i).sort(() => Math.random() - .5), opts = ord.map(i => el("button",{type:"button",class:"o",text:q.o[i]}));
    opts.forEach((b, i) => b.addEventListener("click", () => {
      opts.forEach((x, j) => { x.disabled = true; if (ord[j] === q.a) x.classList.add("ok"); });
      if (ord[i] === q.a) { good++; fb.textContent = "إجابة صحيحة ✓"; } else { b.classList.add("ko"); fb.textContent = "إجابة خاطئة ✗"; }
      if (++done === list.length) { sc.textContent = good + " / " + list.length; const rb = el("button",{type:"button",class:"btn",text:"إعادة المحاولة"}); rb.addEventListener("click", () => box.replaceWith(quiz(list))); box.append(rb); }
    }));
    return el("div",{class:"qz"}, el("p",{text:q.q}), el("div",{class:"opts"}, opts), fb);
  });
  box.append(sc, ...qs); return box;
}
function modelLinks(models){
  return (models || []).map(m => {
    const [kind, rest] = m.split(":");
    if (kind === "story") { const s = DATA.stories.find(x => x.key === rest); return s ? el("a",{class:"btn",href:"#story-" + rest,text:"فتح القصة: " + s.title}) : null; }
    const [cat, key] = rest.split("/"), g = (DATA.games || []).find(x => x.cat === cat && x.key === key);
    return g ? el("a",{class:"btn",href:g.file,download:g.key + ".sb3",text:"نموذج للتحميل: " + g.title_ar}) : null;
  });
}
function parcours(y){
  const d = (DATA.parcours || {})[y]; if (!d) return [];
  const out = [el("h3",{text:"المسار التعليمي: من نشاط إلى آخر",style:"margin-top:18px"}), el("p",{class:"pnote",text:"أنهِ كل مستوى قبل الانتقال إلى الذي بعده. كل نشاط صغير يستند إلى لعبة أو قصة جاهزة تفتحها في سكراتش وتعدّلها."})];
  d.steps.forEach((s, i) => out.push(el("details",{class:"step"}, el("summary",{}, el("span",{class:"badge",text:i + 1}), el("b",{text:s.t})),
    el("div",{class:"stbody"}, el("p",{}, el("b",{text:"الكفاية: "}), s.comp), el("h5",{text:"الأنشطة الصغيرة"}), el("ol",{}, s.acts.map(t => el("li",{text:t}))),
      s.models.length ? el("div",{class:"btns"}, modelLinks(s.models)) : null, el("h5",{text:"أنا قادر على…"}), el("ul",{class:"check"}, s.sais.map(t => el("li",{text:t})))))));
  out.push(el("h3",{text:"مشاريع أساسية للإنجاز",style:"margin-top:18px"}));
  d.projets.forEach(p => out.push(el("details",{class:"step proj"}, el("summary",{}, el("span",{class:"badge pj",text:"★".repeat(p.lvl)}), el("b",{text:p.t})),
    el("div",{class:"stbody"}, el("p",{text:p.brief}), el("h5",{text:"المطلوب"}), el("ul",{}, p.req.map(t => el("li",{text:t}))), el("p",{class:"pnote",text:DATA.parcours.livrables}),
      p.models.length ? el("div",{class:"btns"}, modelLinks(p.models)) : null))));
  return out;
}
function axisExtras(y, k){
  const id = `${y}-${k}`, body = [], ex = (DATA.exo || {})[id], ac = (DATA.act || {})[id];
  if (/^s/.test(y)) body.push(el("p",{class:"pnote",text:"تمارين مقترحة غير رسمية: لم تُقدَّم بعد وثيقة منهاج رسمية لهذا المستوى، فالمواضيع عامة وتُكيَّف مع المنهاج الفعلي."}));
  if (ex) body.push(el("h3",{text:"تمارين تفاعلية"}), el("p",{class:"pnote",text:"اختر الإجابة الصحيحة. يظهر التصحيح مباشرة."}), quiz(ex));
  if (ac) { body.push(el("h3",{text:"أنشطة للإنجاز"})); ac.forEach(a => body.push(el("div",{class:"qz"}, el("p",{text:a.t}), el("p",{style:"font-weight:400",text:a.d}), a.ex ? el("p",{class:"pnote",text:a.ex}) : null, a.link ? el("a",{class:"btn",href:a.link,text:"الموارد"}) : null))); }
  return [...(k === "prog" ? parcours(y) : []), el("details",{class:"space-d"}, el("summary",{text:"فضاء التلميذ"}), body)];
}
function renderTeacher(y){
  const Y = CUR.years[y]; $("#axisBack").href = "#y" + y; $("#axisBack").textContent = "← " + Y.ar; park(); $("#resArea").replaceChildren();
  const L = (DATA.seances || {})[y], kids = [el("span",{class:"lvl",text:Y.ar}), el("h2",{text:"فضاء الأستاذ"})];
  if (!L) { kids.push(el("p",{class:"pnote",text:"لم تُدرج بعد وثيقة منهاج هذا المستوى. ستتوفر بطاقات الأستاذ عند إضافتها."})); }
  else {
    kids.push(el("h3",{text:"التوزيع السنوي المقترح"}), el("p",{class:"pnote",text:"اقتراح غير رسمي قابل للتعديل: حصة واحدة مدتها 60 دقيقة في الأسبوع (27 حصة، 9 في كل ثلاثي)."}),
      el("p",{}, el("a",{class:"btn main",href:`enseignant/niveau-${y}.html`,target:"_blank",rel:"noopener",text:"طباعة التوزيع وبطاقات الحصص"}), " ", el("a",{class:"btn main",href:`#planning-${y}`,text:y === "9" ? "تخطيط الحصص" : "تخطيط حصص سكراتش"}), " ", el("a",{class:"btn main",href:`cahier/cahier-${y}.html`,target:"_blank",rel:"noopener",text:"مذكرات الدفتر (للطباعة)"})),
      el("div",{style:"overflow-x:auto",dir:"ltr"}, el("table",{class:"sctable"}, el("tr",{}, ["Séance","Trim.","Module","Titre","Type",""].map(h => el("th",{text:h}))),
        L.map(s => el("tr",{class:s.type === "eval" ? "ev" : s.type === "projet" ? "pr" : ""}, el("td",{text:"S" + s.n}), el("td",{text:"T" + s.tri}), el("td",{text:s.mod_fr}), el("td",{text:s.title}), el("td",{text:s.type}),
          el("td",{}, el("a",{href:`enseignant/niveau-${y}.html#s${s.n}`,target:"_blank",rel:"noopener",text:"Fiche"})))))),
      el("p",{class:"pnote",text:"لتعديل التوزيع: غيّر الملف generateur/seances.py ثم أعد توليد الصفحات."}));
  }
  $("#axisHead").replaceChildren(el("div",{class:"axhead"}, kids));
}
// « Cahier de l'élève » : fiches à imprimer et à coller dans le cahier, une par séance de programmation (cahier/cahier-N.html et PDF)
function cahierLinks(y){
  const a = (href, text, main, dl) => el("a",{class:"btn" + (main ? " main" : ""),href,target:"_blank",rel:"noopener",text,...(dl ? {download:href.split("/").pop()} : {})});
  return [a(`cahier/cahier-${y}.html`, "فتح المذكرات للطباعة", true), a(`cahier/cahier-${y}-ar.pdf`, "PDF بالعربية", false, true), a(`cahier/cahier-${y}-fr.pdf`, "PDF en français", false, true),
          a(`cahier/cahier-${y}-ar-corrige.pdf`, "PDF بالعربية مع الإجابات", false, true), a(`cahier/cahier-${y}-fr-corrige.pdf`, "PDF avec corrigé", false, true)];
}
function cahierBox(y){
  return el("section",{class:"cahierbox tmp"}, el("h3",{text:"مذكرات الدفتر (للطباعة واللصق في دفتر التلميذ)"}),
    el("p",{class:"pnote",text:"لكل حصة برمجة ورقة واحدة بحجم A4: جمل ناقصة للإتمام، والأثر المكتوب (جدول أو مخطط أو بطاقة)، وسكربت نصف منجز يُنهيه التلاميذ في القسم، وما يجب حفظه. تُطبع الأجزاء الفارغة، ويمكن عرض الإجابات للأستاذ. اقتراح غير رسمي قابل للتعديل."}),
    el("div",{class:"btns cahierbtns"}, cahierLinks(y)));
}
// pages dont on ne garde que les ressources (sans en-tête, parcours ni espace élève)
const BARE = new Set(["7-prog", "8-prog", "9-prog"]);
function renderAxis(y, k){
  const P = CUR.pages[`${y}-${k}`], Y = CUR.years[y];
  $("#axisBack").href = "#y" + y; $("#axisBack").textContent = "← " + Y.ar;
  const kids = [el("span",{class:"lvl",text:Y.ar}), el("h2",{text:P.title_ar})];
  if (P.champ_ar) kids.push(el("p",{class:"pnote",text:"ميدان الاعتبار: " + P.champ_ar}));
  kids.push(el("h3",{text:"الكفايات المراد تنميتها"}), el("ul",{}, P.comps_ar.map(t => el("li",{text:t}))));
  if (P.life_ar) kids.push(el("p",{},el("b",{text:"الكفاية الحياتية المستهدفة: "}), P.life_ar));
  if (P.prat_ar.length) kids.push(el("h3",{text:"الممارسات المنتظرة"}), el("ul",{}, P.prat_ar.map(t => el("li",{text:t}))));
  if (P.pist_ar.length) kids.push(el("h3",{text:"مسالك مقترحة"}), el("ul",{}, P.pist_ar.map(t => el("li",{text:t}))));
  if (!/^s/.test(y)) kids.push(el("p",{class:"pnote",text:CUR.src_ar}));
  if (P.aide) {
    const A2 = P.aide, d = [el("summary",{text:"تفاصيل من المساعدة البيداغوجية (2026)"}), el("p",{text:A2.comp_ar})];
    A2.parts.forEach(x => d.push(el("h3",{text:x.t_ar,style:"font-size:16px"}), el("ul",{}, x.i_ar.map(t => el("li",{text:t})))));
    if (A2.know_ar.length) d.push(el("h3",{text:"المعارف المرتبطة"}), el("ul",{}, A2.know_ar.map(t => el("li",{text:t}))));
    if (A2.cad_ar.length) d.push(el("h3",{text:"توجيهات الإطار"}), el("ul",{}, A2.cad_ar.map(t => el("li",{text:t}))));
    d.push(el("p",{class:"pnote",text:CUR.aide_ar}));
    kids.push(el("details",{}, d));
  }
  $("#axisHead").replaceChildren(el("div",{class:"axhead"}, kids));
  const bare = BARE.has(`${y}-${k}`);
  if (bare) $("#axisHead").replaceChildren(); else $("#axisHead").firstChild.append(...axisExtras(y, k));
  park(); const res = $("#resArea"); const list = RES[`${y}-${k}`] || [];
  if (!list.length && !bare && !(k === "prog" && (DATA.parcours || {})[y])) res.append(el("p",{class:"empty",text:"ستُضاف موارد هذا المحور لاحقا."}));
  const lw = k === "prog" && list.length && (DATA.parcours || {})[y] && !bare ? el("details",{class:"space-d libwrap",open:""}, el("summary",{text: y === "7" ? "القصص الجاهزة (مكتبة)" : "الألعاب الجاهزة (مكتبة)"})) : null;
  if (lw) res.append(lw);
  list.forEach(id => (lw || res).append($("#" + id)));
  if (list.includes("theory")) renderTheorySection();
  if (list.includes("neuf")) renderNeuf();
  if (k === "prog" && ["7","8","9"].includes(y)) res.append(cahierBox(y));
  if (k === "env" && y === "8") res.append(secBox());
  if (list.includes("library")) {
    [sel, vsel, tsel].forEach(x => x.hidden = false);
    $("#library .lead").textContent = "صور وأصوات ورسوم متحركة يمكنك استعمالها في أي قصة. اضغط «تحميل» ثم أضف الملف في سكراتش.";
    setScope("", RESCAT[`${y}-${k}`] || "lieux");
  } else if (list.includes("sources")) { [vsel, tsel].forEach(x => x.hidden = false); setScope("", state.cat); }
}
function renderYear(y){
  const Y = CUR.years[y]; $("#axisBack").href = "#home"; $("#axisBack").textContent = "← الرئيسية"; park();
  $("#axisHead").replaceChildren(el("div",{class:"axhead"}, el("span",{class:"lvl",text:Y.ar}), el("h2",{text:"فضاء التلميذ"}), el("p",{class:"pnote",text:"للتلميذ: تمارين وأنشطة لإنجازها مع أمثلة وموارد."}),
    CUR.by_year[y].length ? null : el("p",{class:"pnote",text:"لم تُدرج بعد وثيقة منهاج هذا المستوى. يمكنك الاطلاع على المراجع المتاحة."}),
    el("div",{class:"axcards"}, CUR.by_year[y].map(k => { const P = CUR.pages[`${y}-${k}`]; return el("article",{class:"axcard"}, el("h3",{text:P.title_ar}), el("p",{text:P.comps_ar[0]}), el("div",{class:"btns"}, el("a",{class:"btn main wide",href:`#y${y}-${k}`,text:"فتح المحور"}))); }).concat([el("article",{class:"axcard"}, el("h3",{text:"فضاء الأستاذ"}), el("p",{text:"للأستاذ: التوزيع السنوي المقترح وبطاقات الحصص."}), el("div",{class:"btns"}, el("a",{class:"btn main wide",href:`#y${y}-ens`,text:"فتح فضاء الأستاذ"}))), el("article",{class:"axcard"}, el("h3",{text:"المراجع"}), el("p",{text:"مراجع التلميذ ومراجع الأستاذ لهذا المستوى."}), el("div",{class:"btns"}, el("a",{class:"btn wide",href:`#y${y}-refs`,text:"فتح المراجع"})))]))));
  $("#resArea").replaceChildren();
}
let dlLevel = "all";
// boutons d'installation sur le bureau : le bouton de ton système (Windows ou macOS) passe en premier et en couleur
function instButtons(links){
  const mine = links.find(l => l.os === OS);
  const ordered = mine ? [mine, ...links.filter(l => l !== mine)] : links;
  return el("div",{class:"instbtns"}, ordered.map((l, i) => el("div",{class:"instrow"}, el("a",{class:"btn" + (l === mine ? " main" : ""),href:l.url,rel:"noopener",...(l.direct ? {} : {target:"_blank"}),text:l.ar}),
    l === mine ? el("span",{class:"mine",text:"مقترح لنظامك"}) : null, l.note_ar ? el("small",{class:"os",text:l.note_ar}) : null)));
}
function renderDownloads(){
  $("#axisBack").href = "#home"; $("#axisBack").textContent = "← الرئيسية"; park(); $("#resArea").replaceChildren();
  const L = window.LOGICIELS || [], C = window.LOGICIEL_CATS || {};
  L.forEach(s => { FRMAP[s.ar] = s.desc_fr; (s.links || []).forEach(l => { FRMAP[l.ar] = l.fr; if (l.note_ar) FRMAP[l.note_ar] = l.note_fr; }); });
  Object.values(C).forEach(c => { FRMAP[c[0]] = c[1]; });
  YEARS.forEach(y => { FRMAP[CUR.years[y].short_ar] = CUR.years[y].short_fr; });
  if (dlLevel !== "all" && !MENU_YEARS.includes(dlLevel)) dlLevel = "all";
  // seuls les niveaux du menu (7e, 8e, 9e) sont proposés : les logiciels réservés aux niveaux secondaires restent dans logiciels.js mais ne sont pas affichés
  const shown = s => s.levels === "all" || s.levels.some(y => MENU_YEARS.includes(y));
  const ok = s => shown(s) && (dlLevel === "all" || s.levels === "all" || s.levels.includes(dlLevel));
  const chips = el("div",{class:"dlchips"}, [["all","كل المستويات"], ...MENU_YEARS.map(y => [y, CUR.years[y].ar])].map(([v, t]) => { const b = el("button",{type:"button",class:"chip",text:t,"aria-pressed":String(dlLevel === v)}); b.addEventListener("click", () => { dlLevel = v; renderDownloads(); }); return b; }));
  const groups = Object.keys(C).map(c => { const items = L.filter(s => s.cat === c && ok(s)); if (!items.length) return null;
    return el("section",{}, el("h3",{text:C[c][0]}), el("div",{class:"dlgrid"}, items.map(s => el("article",{class:"dlcard"}, el("h4",{text:s.name}), el("p",{text:s.ar}),
      el("div",{class:"dlmeta"}, s.levels === "all" ? el("span",{class:"lvl",text:"كل المستويات"}) : s.levels.filter(y => MENU_YEARS.includes(y)).map(y => el("span",{class:"lvl",text:CUR.years[y].short_ar})), el("span",{class:"os",dir:"ltr",text:s.os})),
      s.links ? instButtons(s.links) : el("a",{class:"btn main",href:s.url,target:"_blank",rel:"noopener",text:"⬇ تحميل"}))))); });
  const shortcutBtn = el("button",{type:"button",class:"btn",text:"⬇ اختصار هذا الموقع على سطح المكتب"}); shortcutBtn.addEventListener("click", () => $("#install").click());
  $("#axisHead").replaceChildren(el("div",{class:"axhead"}, el("h2",{text:"التحميلات"}), el("p",{class:"pnote",text:"البرمجيات المستعملة في كل المستويات. الروابط تؤدي إلى المواقع الرسمية للبرمجيات."}), el("p",{}, shortcutBtn), chips, groups,
    el("p",{class:"pnote",text:"لإضافة برنامج: عدّل الملف logiciels.js."})));
}
function syncImgs(){ document.querySelectorAll("img[data-fr-src]").forEach(i => { if (!i.dataset.arSrc) i.dataset.arSrc = i.getAttribute("src"); i.setAttribute("src", document.documentElement.lang === "fr" ? i.dataset.frSrc : i.dataset.arSrc); }); }
function actChip(k){ const b = DATA.activites.blocks[k]; return el("span",{class:"blk " + b[0],text:b[1]}); }
function actImg(a, k, alt){ return el("img",{src:a.img[k][1],"data-fr-src":a.img[k][0],alt,loading:"lazy"}); }
// carte d'une activité (image « après exécution », titre dessous, case « Fait ») : grille des niveaux et planning des séances
function actCard(a){
  const cb = el("input",{type:"checkbox",class:"actcb","aria-label":"تم"}); cb.checked = Done.has(a.n); cb.addEventListener("change", () => { Done.toggle(a.n); updateProgress(); });
  return el("div",{class:"actcard","data-l":a.lvl,"data-act":a.n}, el("a",{class:"actlink",href:"#activite-" + a.n,title:a.t}, el("div",{class:"actthumb"}, actImg(a, "apres", a.t), el("span",{class:"badge pj",text:a.n})), el("h4",{text:a.t})),
    el("label",{class:"actdone"}, cb, el("span",{text:"تم"})));
}
function renderActivites(openLevel){
  $("#axisBack").href = "#y8-prog"; $("#axisBack").textContent = "← ألعاب سكراتش"; park(); $("#resArea").replaceChildren();
  const D = DATA.activites;
  // une grille d'images par niveau : pour chaque activité, une image explicative (la scène après exécution), son titre en dessous et une case « Fait »
  const sec = L => el("section",{class:"actsec",id:"lvl-" + L.n,"data-l":L.n}, el("div",{class:"acthead"}, el("span",{class:"badge",text:L.n}), el("h3",{text:L.t}), el("span",{class:"lvlf",text:L.diff}), el("span",{class:"lvlprog","data-lvl-prog":L.n})),
    el("p",{class:"pnote",text:L.obj}), el("div",{class:"actgrid"}, D.acts.filter(a => a.lvl === L.n).map(actCard)));
  const jump = el("div",{class:"dlchips"}, D.levels.map(L => el("a",{class:"chip",href:"#activites-" + L.n,"aria-pressed":String(L.n === openLevel),text:L.t.split(" – ")[0]})));
  const reset = el("button",{type:"button",class:"btn",text:"مسح تقدّمي"});
  reset.addEventListener("click", () => { if (confirm(document.documentElement.lang === "fr" ? "Effacer toute ta progression ?" : "هل تريد مسح كل تقدّمك؟")) { Done.reset(); updateProgress(); } });
  const prog = el("div",{class:"actprog"}, el("b",{text:"تقدّمك:"}), el("span",{class:"allprog","data-all-prog":""}), el("div",{class:"actbar"}, el("i",{})), reset);
  const planLinks = el("p",{}, el("b",{text:"التخطيط حسب الحصص"}), " : ", ["7","8","9"].map(v => [el("a",{class:"btn",href:"#planning-" + v,text:DATA.planning.years[v].label}), " "]));
  $("#axisHead").replaceChildren(el("div",{class:"axhead"}, el("h2",{text:D.title}), el("p",{class:"pnote",text:D.intro}), planLinks, prog, el("p",{class:"pnote",text:"يُحفظ تقدّمك في هذا المتصفح فقط."}), jump, D.levels.map(sec)));
  syncImgs(); updateProgress();
  window.__scrollTo = openLevel ? "lvl-" + openLevel : null;
}
function renderPlanning(y){
  const P = DATA.planning, Y = P.years[y], D = DATA.activites, NOT = {};
  P.notions.forEach(n => NOT[n.id] = n.t);
  $("#axisBack").href = "#y" + y + "-ens"; $("#axisBack").textContent = "← فضاء الأستاذ"; park(); $("#resArea").replaceChildren();
  const act = n => D.acts.find(a => a.n === n);
  const tabs = el("div",{class:"dlchips"}, ["7","8","9"].map(v => el("a",{class:"chip",href:"#planning-" + v,"aria-pressed":String(v === y),text:P.years[v].label})));
  // carte des notions : lignes = notions, colonnes = séances ; ● nouvelle, ◆ approfondie, ○ réinvestie
  const known = new Set(); for (const yy of ["7","8","9"]) { if (yy === y) break; P.years[yy].seances.forEach(s => s.new.forEach(i => known.add(i))); }
  const cols = Y.seances, ids = P.notions.map(n => n.id).filter(id => known.has(id) || cols.some(s => s.new.includes(id)));
  const sym = (s, id) => s.new.includes(id) ? ["n","●"] : s.deep.includes(id) ? ["d","◆"] : s.re.includes(id) ? ["r","○"] : ["","" ];
  const mx = el("div",{class:"mxwrap"}, el("table",{class:"mx"}, el("thead",{}, el("tr",{}, el("th",{text:"المفهوم"}), known.size ? el("th",{text:"مكتسبات السنوات السابقة"}) : null, cols.map(s => el("th",{},"ح" + s.s)))),
    el("tbody",{}, ids.map(id => el("tr",{}, el("td",{class:"mxn",text:NOT[id]}), known.size ? el("td",{class:"mxk",text:known.has(id) ? "✓" : ""}) : null, cols.map(s => { const [c, t] = sym(s, id); return el("td",{class:"mx" + (c ? " mx-" + c : "")}, t); }))))));
  const legend = el("p",{class:"pnote"}, el("span",{class:"mx-n lg",text:"●"}), " ", el("span",{text:"جديد"}), "  ", el("span",{class:"mx-d lg",text:"◆"}), " ", el("span",{text:"معمَّق"}), "  ", el("span",{class:"mx-r lg",text:"○"}), " ", el("span",{text:"موظَّف من جديد"}));
  const chips = (list, cls) => list.map(i => [el("span",{class:"nchip " + cls,text:NOT[i]}), " "]);
  const grid = (ns) => el("div",{class:"actgrid mini"}, ns.map(n => actCard(act(n))));
  const game = g => {
    if (g.kind === "story") { const s = DATA.stories.find(x => x.key === g.key); return s ? el("div",{class:"gamerow"}, el("b",{text:s.title}), el("a",{class:"btn",href:"#story-" + g.key,text:"فتح القصة"})) : null; }
    const x = (DATA.games || []).find(q => q.key === g.key); if (!x) return null;
    return el("div",{class:"gamerow"}, el("b",{text:x.title_ar}), watchBtn(x), x.fiche ? ficheBtn(x.fiche) : null);
  };
  const seance = (s, i) => {
    const ns = [...s.core, ...s.support, ...s.challenge];
    const thy = y === "7" ? (TH.bySeance[s.s] || []).map(k => TH.lessons.find(l => l.n === k)) : [];
    const body = el("div",{class:"stbody"}, el("p",{}, el("b",{text:"الهدف"}), " : ", s.obj),
      thy.length ? el("p",{}, el("b",{text:U.theoryLbl}), " : ", thy.map(l => [el("a",{class:"chip",href:"#cours-" + l.n,text:l.t}), " "])) : null,
      el("p",{}, el("a",{class:"btn",href:`cahier/cahier-${y}.html#s${s.s}`,target:"_blank",rel:"noopener",text:"مذكرة الدفتر لهذه الحصة"})),
      s.new.length ? el("p",{}, el("b",{text:"المفاهيم الجديدة"}), " : ", chips(s.new, "n")) : null, s.deep.length ? el("p",{}, el("b",{text:"المفاهيم المعمَّقة"}), " : ", chips(s.deep, "d")) : null,
      s.re.filter(i => i !== "seq" && i !== "event").length ? el("p",{}, el("b",{text:"المفاهيم الموظَّفة من جديد"}), " : ", chips(s.re.filter(i => i !== "seq" && i !== "event"), "r")) : null,
      el("p",{class:"pnote"}, el("span",{text:"المفاهيم المكتسبة في نهاية الحصة"}), " : ", el("b",{text:s.cum + " / " + P.notions.length})),
      el("h5",{text:"السير (60 دقيقة)"}), el("table",{class:"sctable phases"}, el("thead",{}, el("tr",{}, el("th",{text:"المرحلة"}), el("th",{text:"المدة"}), el("th",{text:"الوصف"}))),
        el("tbody",{}, s.phases.map(p => el("tr",{}, el("td",{text:p.t}), el("td",{class:"n"}, p.min + " ", el("span",{text:"د"})), el("td",{text:p.d}))))),
      ns.length ? el("div",{class:"rolerow"}, [["core","النشاط الرئيسي"],["support","للتدرّب"],["challenge","تحدٍّ"]].filter(([k]) => s[k].length).map(([k, t]) => el("div",{class:"rolegrp"}, el("h5",{text:t}), grid(s[k])))) : null,
      s.games.length ? [el("h5",{text:"الألعاب والقصص"}), s.games.map(game)] : null, s.extra && !s.core.length ? null : null,
      s.acq.length ? [el("h5",{text:"أنا قادر على…"}), el("ul",{class:"check"}, s.acq.map(t => el("li",{text:t})))] : null, el("p",{class:"pnote"}, el("b",{text:"الأثر المكتوب"}), " : ", s.trace));
    return el("details",{class:"step seanc","data-auto":s.auto}, el("summary",{}, el("span",{class:"badge",text:s.s}), el("b",{text:s.t}), el("span",{class:"lvlf",text:s.type}), el("span",{class:"autopill " + s.auto,text:s.auto_t}),
      ns.length ? el("span",{class:"lvlprog","data-sc-acts":ns.join(",")}) : null), body);
  };
  const enr = P.enrich.map(n => actCard(act(n)));
  const bar = el("div",{class:"actprog"}, el("button",{type:"button",class:"btn",text:"فتح الكل"}), el("button",{type:"button",class:"btn",text:"طي الكل"}), el("button",{type:"button",class:"btn main",text:"طباعة التخطيط"}));
  const [bo, bc, bp] = bar.children;
  bo.addEventListener("click", () => document.querySelectorAll("#axisHead details.seanc").forEach(d => d.open = true)); bc.addEventListener("click", () => document.querySelectorAll("#axisHead details.seanc").forEach(d => d.open = false)); bp.addEventListener("click", () => { bo.click(); window.print(); });
  $("#axisHead").replaceChildren(el("div",{class:"axhead planpage"}, el("h2",{}, el("span",{text:y === "9" ? "تخطيط الحصص" : "تخطيط حصص سكراتش"}), " – ", el("span",{text:Y.label})), tabs,
    el("p",{class:"pnote",text:"اقتراح غير رسمي قابل للتعديل: حصة واحدة مدتها 60 دقيقة في الأسبوع، وهي حصص وحدة «البرمجة» من التوزيع السنوي. تتراكم المفاهيم من حصة إلى أخرى وتزداد استقلالية التلاميذ شيئا فشيئا."}),
    el("p",{class:"pnote",text:"موجَّه: الأستاذ يشرح والتلميذ يتبع المراحل. شبه موجَّه: ينطلق التلميذ من الهدف والنتيجة المنتظرة. مستقل: يقرر التلميذ وينجز وحده."}),
    y === "9" ? el("div",{class:"cahierbox"}, el("h3",{text:"حصص مقترحة إضافية: الشيء القابل للبرمجة وتطبيقة الهاتف"}), el("p",{class:"pnote",text:"اقتراح غير رسمي (المساعدة البيداغوجية 2026): أربع حصص حول بطاقة micro:bit (اكتشاف، مدخلات ومخرجات، قياس وقرار وفعل، مشروع النرد) ثم أربع حصص حول تطبيقة هاتف بـ App Inventor (الواجهة، الأحداث، الاختبار والتوليد، التحكم في البطاقة). لكل حصة مذكرة في آخر مذكرات 9."})) : null,
    el("div",{class:"cahierbox"}, el("h3",{text:"مذكرات الدفتر (للطباعة واللصق في دفتر التلميذ)"}), el("p",{class:"pnote",text:"ورقة A4 لكل حصة: جمل ناقصة، أثر مكتوب للإتمام، وسكربت نصف منجز يُنهى في القسم."}), el("div",{class:"btns cahierbtns"}, cahierLinks(y))),
    bar, el("h3",{text:"خريطة المفاهيم"}), mx, legend, el("h3",{text:"السير (60 دقيقة)"}), Y.seances.map(seance), (Y.extra || []).length ? [el("h3",{text:Y.extraT}), el("p",{class:"pnote",text:Y.extraN}), Y.extra.map(seance)] : null,
    P.enrich.length ? [el("h3",{text:"للتوسع (خارج التخطيط)"}), el("p",{class:"pnote",text:"بعضها يستعمل النسخ أو القوائم أو «و» المنطقية: وهي تتجاوز إطار المنهاج."}), el("div",{class:"actgrid mini"}, enr)] : null));
  syncImgs(); updateProgress();
}
function renderActivite(n){
  const D = DATA.activites, a = D.acts.find(x => x.n === n); if (!a) return;
  const L = D.levels.find(x => x.n === a.lvl), prev = D.acts.find(x => x.n === n - 1), next = D.acts.find(x => x.n === n + 1);
  $("#axisBack").href = "#activites-" + a.lvl; $("#axisBack").textContent = "← مجموعة الأنشطة"; park(); $("#resArea").replaceChildren();
  const row = k => el("div",{class:"blkhelp"}, actChip(k), el("p",{text:D.blocks[k][2]}));
  const uses = ((DATA.planning || {}).uses || {})[n] || [];
  const fig = (k, cap) => el("figure",{}, actImg(a, k, cap), el("figcaption",{text:cap}));
  const mkDone = () => { const x = el("button",{type:"button",class:"btn donebtn","data-n":a.n,"aria-pressed":"false"}); x.addEventListener("click", () => { Done.toggle(a.n); updateProgress(); }); return x; };
  const doneBtn = mkDone(), doneBtn2 = mkDone();
  $("#axisHead").replaceChildren(el("div",{class:"axhead actpage"},
    el("div",{class:"acthead"}, el("span",{class:"badge pj",text:a.n}), el("span",{class:"lvlf",text:L.diff}), el("span",{class:"pnote",text:L.t}), doneBtn),
    el("h2",{text:a.t}),
    el("h3",{text:"الهدف"}), el("p",{text:a.obj}),
    uses.length ? el("p",{class:"usesrow"}, el("b",{text:"تُستعمل في الحصة"}), " : ", uses.map(u => [el("a",{class:"chip",href:"#planning-" + u.y,text:DATA.planning.years[u.y].label + " · " + "ح" + u.s}), " "])) : null,
    el("h3",{text:"الكتل المستعملة ودورها"}), a.blocks.map(row),
    el("h3",{text:"السكربت الكامل"}), el("div",{class:"scriptimg"}, actImg(a, "script", a.t)),
    el("h3",{text:"الإنجاز خطوة بخطوة"}), el("ol",{class:"bigsteps"}, a.steps.map(t => el("li",{text:t}))),
    el("p",{class:"tip",text:"نصيحة: اختبر مشروعك بعد كل خطوة بالنقر على العلم الأخضر."}),
    el("h3",{text:"قبل وبعد"}), el("div",{class:"figpair"}, fig("avant", "قبل التنفيذ"), fig("apres", "بعد التنفيذ")),
    el("h3",{text:"النتيجة المنتظرة"}), el("p",{text:a.res}),
    el("h3",{text:"تحدٍّ إضافي"}), el("p",{class:"defi",text:a.defi}),
    el("h3",{text:"نسخة مخففة"}), el("div",{class:"tip lightv"}, el("p",{class:"pnote",text:"للتلاميذ المحتاجين إلى مساعدة: مهمة مخففة تُنجز قبل النشاط الكامل أو بدلا منه."}), el("p",{text:a.light})),
    el("p",{class:"pnote",text:"الصور رسوم توضيحية أُنجزت لهذا الموقع (كتل سكراتش ومشهد المشروع)."}),
    el("div",{class:"btns actnav"}, doneBtn2, prev ? el("a",{class:"btn",href:"#activite-" + prev.n,text:"النشاط السابق"}) : null, el("a",{class:"btn main",href:"#activites-" + a.lvl,text:"كل الأنشطة"}), next ? el("a",{class:"btn",href:"#activite-" + next.n,text:"النشاط التالي"}) : null)));
  syncImgs(); updateProgress();
}
function renderRessources(id){
  $("#axisBack").href = "#y8-prog"; $("#axisBack").textContent = "← " + CUR.years["8"].ar; park(); $("#resArea").replaceChildren();
  const RG = (DATA.ressources || {})[id] || {items:[], zip:""}, R = RG.items, game = (DATA.games || []).find(x => x.res === id) || {title_ar:""}; R.forEach(r => { FRMAP[r.ar] = r.fr; });
  const card = r => el("article",{class:"dlcard"}, r.type === "image" ? el("img",{src:r.file,alt:r.ar,class:"rprev",loading:"lazy"}) : el("audio",{src:r.file,controls:"",preload:"none",class:"rprev"}),
    el("h4",{text:r.ar}), el("a",{class:"btn main",href:r.file,download:r.file.split("/").pop(),text:"⬇ تحميل"}));
  $("#axisHead").replaceChildren(el("div",{class:"axhead"}, el("h2",{}, el("span",{text:"موارد لعبة"}), " «", el("span",{text:game.title_ar}), "»"),
    el("p",{class:"pnote",text:"الصور والأصوات المستعملة في اللعبة. حمّلها ثم أضفها في سكراتش (رسم ← رفع، أو صوت ← رفع)."}),
    el("p",{}, el("a",{class:"btn main",href:RG.zip,download:RG.zip.split("/").pop(),text:"تحميل كل الموارد (.zip)"})),
    el("h3",{text:"الصور"}), el("div",{class:"dlgrid"}, R.filter(r => r.type === "image").map(card)),
    el("h3",{text:"الأصوات"}), el("div",{class:"dlgrid"}, R.filter(r => r.type === "son").map(card))));
}
function renderFiche(fid, key){
  const F = (DATA.fiches || {})[fid]; if (!F) return;
  const isC = fid === "contes", s = isC ? DATA.stories.find(x => x.key === key) : null;
  $("#axisBack").href = isC ? "#story-" + key : "#y8-prog"; $("#axisBack").textContent = isC ? "← " + (s ? s.title : "") : "← " + CUR.years["8"].ar; park(); $("#resArea").replaceChildren();
  const steps = isC ? (DATA.etapes.contes[key] || []) : (DATA.etapes[fid] || []);
  const sec = (t, kids) => [el("h3",{text:t}), kids];
  const li = a => el("ul",{}, a.map(t => el("li",{text:t})));
  const dl = isC ? (s && el("a",{class:"btn main",href:s.sb3,download:`${s.title}.sb3`,text:"تحميل مشروع سكراتش (.sb3)"})) : (() => { const g = (DATA.games || []).find(x => x.fiche === fid); return g && watchBtn(g); })();
  const pdfn = "fiches-activite/pdf/fiche-" + fid + (isC ? "-" + key : "");
  const body = el("div",{class:"fiche"}, el("h2",{}, el("span",{text:"بطاقة النشاط: "}), el("span",{text:isC && s ? s.title : F.title})), el("p",{class:"pnote",text:F.meta}),
    el("p",{class:"pdfrow"}, el("a",{class:"btn main pdf-ar",href:pdfn + "-ar.pdf",target:"_blank",rel:"noopener",text:"طباعة البطاقة (PDF)"}), el("a",{class:"btn main pdf-fr",href:pdfn + "-fr.pdf",target:"_blank",rel:"noopener",text:"Imprimer la fiche (PDF)","data-nofr":""})),
    sec("الوضعية المشكلة", el("p",{class:"sit",text:F.situation})),
    steps.length ? sec("مراحل اللعبة بالصور", el("div",{class:"figgrid"}, steps.map((st, i) => el("figure",{}, el("img",{src:st.img_ar || st.img,"data-fr-src":st.img,alt:st.t,loading:"lazy"}), el("figcaption",{}, el("b",{text:st.t}), st.c ? el("span",{text:st.c}) : null))))) : [],
    sec("سير الحصة", li(F.steps)), sec("أنشطة التلميذ", li(F.eleve)), sec("معايير النجاح", li(F.criteres)),
    sec("التمايز", el("ul",{}, el("li",{}, el("b",{text:"التخفيف: "}), el("span",{text:F.allegee})), el("li",{}, el("b",{text:"التوسيع: "}), el("span",{text:F.prolongement})))),
    dl ? el("p",{}, dl, (DATA.ressources || {})[fid] ? resBtn(fid) : null) : null);
  $("#axisHead").replaceChildren(el("div",{class:"axhead"}, body)); syncImgs();
}
const REFTYPES = {pdf:"PDF", site:"موقع", livre:"كتاب", outil:"أداة"};
function renderRefs(y){
  const Y = CUR.years[y]; $("#axisBack").href = "#y" + y; $("#axisBack").textContent = "← " + Y.ar; park(); $("#resArea").replaceChildren();
  const all = (window.REFERENCES || []).filter(r => r.level === "all" || r.level === y || (Array.isArray(r.level) && r.level.includes(y)));
  const col = (who, title) => {
    const list = all.filter(r => r.for === who);
    return el("div",{class:"refcol"}, el("h3",{text:title}), list.length ? list.map(r => {
      if (r.fr) FRMAP[r.title] = r.fr; if (r.note && r.note_fr) FRMAP[r.note] = r.note_fr;
      const ext = /^https?:/.test(r.url || ""); const a = el("a",{href:r.url,text:r.title}); if (ext) { a.target = "_blank"; a.rel = "noopener"; }
      return el("div",{class:"refitem"}, a, r.type && el("span",{class:"rt",text:REFTYPES[r.type] || r.type}), r.note && el("p",{text:r.note}));
    }) : el("p",{class:"pnote",text:"لم تُضف مراجع بعد لهذا المستوى."}));
  };
  $("#axisHead").replaceChildren(el("div",{class:"axhead"}, el("span",{class:"lvl",text:Y.ar}), el("h2",{text:"المراجع"}),
    el("div",{class:"refgrid"}, col("eleve","مراجع التلميذ"), col("enseignant","مراجع الأستاذ")),
    el("p",{class:"pnote",text:"لإضافة مرجع: ضعه في المجلد references وأضف سطرا في الملف references.js."})));
}
function route(){
  let h = decodeURIComponent(location.hash.replace(/^#/, "")) || "home";
  if (h === "games") h = "y8-prog"; if (h === "stories") h = "y7-prog";
  let view = "home", y = null, k = null, key = null, m;
  if (h === "downloads") view = "dl";
  let am = h.match(/^activites(?:-([1-6]))?$/); if (am) { view = "act"; y = "8"; }
  let ad = h.match(/^activite-(\d+)$/); if (ad) { view = "actd"; y = "8"; }
  let pm = h.match(/^planning-(7|8|9)$/); if (pm) { view = "plan"; y = pm[1]; }
  let rm = h.match(/^ressources-([a-z]+)$/); if (rm) { view = "res"; y = "8"; }
  if (h === "theorie") { view = "th"; y = "7"; }
  if (h === "securite") { view = "sec"; y = "8"; }
  let tl = h.match(/^cours-([1-9])$/); if (tl && TH.lessons.some(l => l.n === +tl[1])) { view = "thl"; y = "7"; }
  let fm = h.match(/^fiche-([a-z]+)(?:-([a-z]+))?$/); if (fm) { view = "fiche"; y = fm[1] === "contes" ? "7" : "8"; }
  if ((m = h.match(/^y(7|8|9|s[1-4])$/))) { view = "year"; y = m[1]; }
  else if ((m = h.match(/^y(7|8|9|s[1-4])-(env|net|create|prog|prod|sa|si|sr|refs|ens)$/))) { view = "axis"; y = m[1]; k = m[2]; }
  else if (h.startsWith("story-")) { key = h.slice(6) === "general" ? "__general" : h.slice(6); if (key === "__general" || DATA.stories.some(s => s.key === key)) { view = "story"; y = "7"; } }
  $("#viewHome").hidden = view !== "home"; $("#hero").hidden = view !== "home";
  $("#viewAxis").hidden = !(view === "year" || view === "axis" || view === "dl" || view === "fiche" || view === "res" || view === "act" || view === "actd" || view === "plan" || view === "th" || view === "thl" || view === "sec"); $("#viewStory").hidden = view !== "story";
  park();
  if (view === "story") { [sel, vsel, tsel].forEach(x => x.hidden = true); const r = $("#storyRes"); ["library","videos","sources"].forEach(id => r.append($("#" + id))); $("#library .lead").textContent = "كل ما يخص هذه القصة. اضغط «تحميل» ثم أضف الملف في سكراتش."; showStory(key); }
  if (view === "dl") renderDownloads();
  if (view === "act") renderActivites(am[1] ? +am[1] : 0);
  if (view === "actd") renderActivite(+ad[1]);
  if (view === "plan") renderPlanning(pm[1]);
  if (view === "th") renderTheoryHub();
  if (view === "sec") renderSecurite();
  if (view === "thl") renderLesson(+tl[1]);
  if (view === "fiche") renderFiche(fm[1], fm[2]);
  if (view === "res") renderRessources(rm[1]);
  if (view === "year") renderYear(y);
  if (view === "axis") { if (k === "refs") renderRefs(y); else if (k === "ens") renderTeacher(y); else renderAxis(y, k); }
  ynav.querySelectorAll(".ydrop").forEach(d => { if (d.dataset.year === y) d.setAttribute("data-current",""); else d.removeAttribute("data-current"); });
  ynav.querySelectorAll(".sub a").forEach(a => { if (a.getAttribute("href") === "#" + h) a.setAttribute("aria-current","page"); else a.removeAttribute("aria-current"); });
  updateProgress();
  const st = window.__scrollTo; window.__scrollTo = null;
  if (st && $("#" + st)) $("#" + st).scrollIntoView(); else window.scrollTo(0, 0);
}
window.addEventListener("hashchange", route);
route();

// ---- اللغة : العربية / Français (traduction de tout le texte de la page)
let LANG = "ar";
const origText = new WeakMap(), origAttr = new WeakMap(), origHTML = new WeakMap(), ATTRS = ["placeholder","aria-label","title","alt"];
function trStr(t){
  const k = t.trim(); if (!k) return null;
  if (FRMAP[k] !== undefined) return t.replace(k, FRMAP[k]);
  for (const [re, rep] of FRRULES) if (re.test(k)) return t.replace(k, k.replace(re, (...m) => rep.replace(/\$(\d)/g, (_, i) => FRMAP[m[+i]] !== undefined ? FRMAP[m[+i]] : m[+i])));
  return null;
}
function trElement(n){
  if (n.hasAttribute("data-fr")) { if (!origHTML.has(n)) origHTML.set(n, n.innerHTML); n.innerHTML = n.getAttribute("data-fr"); return false; }
  for (const a of ATTRS) { const v = n.getAttribute(a); if (v) { const r = trStr(v); if (r !== null && r !== v) { const o = origAttr.get(n) || {}; if (!(a in o)) o[a] = v; origAttr.set(n, o); n.setAttribute(a, r); } } }
  return true;
}
function walk(root, fn){
  const w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, { acceptNode(n){ if (n.nodeType === 1) { if (/^(SCRIPT|STYLE)$/.test(n.tagName) || n.hasAttribute("data-nofr")) return NodeFilter.FILTER_REJECT; return fn(n) === false ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT; } return NodeFilter.FILTER_ACCEPT; } });
  if (root.nodeType === 3) { fn(root); return; }
  if (root.nodeType === 1) { if (fn(root) === false) return; }
  let n; while ((n = w.nextNode())) if (n.nodeType === 3) fn(n);
}
function toFr(n){ if (n.nodeType === 3) { const r = trStr(n.nodeValue); if (r !== null && r !== n.nodeValue) { if (!origText.has(n)) origText.set(n, n.nodeValue); n.nodeValue = r; } return true; } return trElement(n); }
function toAr(n){
  if (n.nodeType === 3) { if (origText.has(n)) n.nodeValue = origText.get(n); return true; }
  if (origHTML.has(n)) { n.innerHTML = origHTML.get(n); origHTML.delete(n); return false; }
  const o = origAttr.get(n); if (o) { for (const a in o) n.setAttribute(a, o[a]); origAttr.delete(n); }
  return true;
}
const obs = new MutationObserver(ms => {
  obs.disconnect();
  for (const m of ms) { if (m.type === "childList") m.addedNodes.forEach(x => walk(x, toFr)); else if (m.type === "characterData") toFr(m.target); else if (m.type === "attributes") trElement(m.target); }
  startObs();
});
function startObs(){ obs.observe(document.body, {childList:true, subtree:true, characterData:true, attributes:true, attributeFilter:ATTRS}); }
function setLang(l){
  if (l === LANG && document.documentElement.lang === l) return;
  obs.disconnect(); LANG = l;
  document.documentElement.lang = l; document.documentElement.dir = l === "fr" ? "ltr" : "rtl";
  if (!document.documentElement.hasAttribute("data-ar-title")) document.documentElement.setAttribute("data-ar-title", document.title);
  if (l === "fr") { walk(document.body, toFr); document.title = FRMAP[document.documentElement.getAttribute("data-ar-title")] || document.title; startObs(); }
  else { walk(document.body, toAr); document.title = document.documentElement.getAttribute("data-ar-title"); }
  document.querySelectorAll(".langbtn").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.lang === l)));
  syncImgs();
  try { localStorage.setItem("ateliers-contes-lang", l); } catch(e){}
}
document.querySelectorAll(".langbtn").forEach(b => b.addEventListener("click", () => setLang(b.dataset.lang)));
let want = "ar";
try { want = new URLSearchParams(location.search).get("lang") || localStorage.getItem("ateliers-contes-lang") || "ar"; } catch(e){}
document.querySelectorAll(".langbtn").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.lang === "ar")));
if (want === "fr") setLang("fr");

</script>
</body>
</html>
'''
import datetime
TPL = TPL.replace("/*__THEORIE_JS__*/", _TH_JS.JS + _SE_JS.JS).replace("/*__THEORIE_CSS__*/", _TH_JS.CSS + _SE_JS.CSS)
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(TPL.replace("__DATA__", json.dumps(man, ensure_ascii=False)).replace("__FRMAP__", json.dumps(FR["map"], ensure_ascii=False)).replace("__FRRULES__", json.dumps(FR["rules"], ensure_ascii=False)).replace("__BUILD__", "نسخة " + datetime.date.today().isoformat()))
print("index.html", os.path.getsize(os.path.join(ROOT, "index.html")) // 1024, "Ko")
