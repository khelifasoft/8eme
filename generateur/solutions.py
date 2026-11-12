"""Solutions (code Scratch) de chaque étape des fiches d'activité « jeu » (catch, course, saut, labyrinthe).
Bouton « Solution » sous chaque étape : un modal demande un code (CODE) puis affiche les blocs de l'étape.
Chaque ligne : <indentation>cat:type|français|arabe ; types : flag (chapeau), forever, if, else, repeat… ; les conditions s'écrivent cat:if|condition fr|condition ar.
Export : {"code", "steps": {jeu: [{sprite_ar, tok}]}} + dictionnaire arabe -> français."""
CODE = "123"
import re
PRE = {"if": (("si", "إذا"), ("alors", "فإن"))}

def parse(txt):
    out, fr = [], {}
    for raw in txt.strip("\n").split("\n"):
        d = (len(raw) - len(raw.lstrip(" "))) // 2; c, rest = raw.strip().split(":", 1); k, f, a = rest.split("|")
        fr[a] = f
        if k == "if":
            fr["إذا"] = "si"; fr["فإن"] = "alors"
            out.append(dict(c=c, k=k, t="إذا " + a + " فإن", d=d, pre="إذا", cond=a, post="فإن"))
        elif k == "until":
            fr["كرّر حتى"] = "répéter jusqu'à ce que"
            out.append(dict(c=c, k=k, t="كرّر حتى " + a, d=d, pre="كرّر حتى", cond=a, post=""))
        else: out.append(dict(c=c, k=k, t=a, d=d))
    return out, fr

FLAG = "ev:flag|quand le drapeau vert est cliqué|عند النقر على العلم الأخضر"
# --------------------------------------------------------------------------- jeu « Attrape » (le poisson tombe, le joueur le rattrape)
CATCH = [
 ("الشيء (السمكة)", "Lutin « poisson »", f"""{FLAG}
va:set|mettre score à 0|اجعل النقاط 0
va:set|mettre vies à 3|اجعل الأرواح 3
va:set|mettre vitesse à 3|اجعل السرعة 3
mv:goto|aller à x : (nombre aléatoire entre -200 et 200) y : 180|اذهب إلى س: (عدد عشوائي بين -200 و200) ص: 180
lk:show|montrer|أظهر"""),
 ("الشيء (السمكة)", "Lutin « poisson » (à la suite du script)", """ct:forever|répéter indéfiniment|كرّر باستمرار
  mv:chy|changer y de (0 − vitesse)|غيّر ص بمقدار (0 − السرعة)"""),
 ("اللاعب", "Lutin « joueur »", f"""{FLAG}
mv:goto|aller à x : 0 y : -125|اذهب إلى س: 0 ص: -125
lk:show|montrer|أظهر
ct:forever|répéter indéfiniment|كرّر باستمرار
  mv:goto|aller à x : (x de la souris) y : -125|اذهب إلى س: (س الفأرة) ص: -125"""),
 ("الشيء (السمكة)", "Lutin « poisson » (dans la boucle « répéter indéfiniment »)", """ct:if|valeur absolue de (x − x de la souris) < 50|القيمة المطلقة لـ (س − س الفأرة) < 50
  ct:if|y < -90|ص < -90
    sn:play|jouer le son|ابدأ الصوت
    va:chg|ajouter 1 à score|غيّر النقاط بمقدار 1
    va:chg|ajouter 0,25 à vitesse|غيّر السرعة بمقدار 0.25
    mv:goto|aller à x : (nombre aléatoire entre -200 et 200) y : 180|اذهب إلى س: (عدد عشوائي بين -200 و200) ص: 180"""),
 ("الشيء (السمكة)", "Lutin « poisson » (dans la boucle « répéter indéfiniment »)", """ct:if|y < -165|ص < -165
  va:chg|ajouter -1 à vies|غيّر الأرواح بمقدار -1
  mv:goto|aller à x : (nombre aléatoire entre -200 et 200) y : 180|اذهب إلى س: (عدد عشوائي بين -200 و200) ص: 180"""),
 ("الشيء (السمكة)", "Lutin « poisson » (dans la boucle « répéter indéfiniment »)", """ct:if|vies < 1|الأرواح < 1
  lk:say|dire « Fin de partie ! » pendant 3 secondes|قل «انتهت اللعبة!» لمدة 3 ثوان
  ct:stop|stop tout|أوقف الكل"""),
]
# --------------------------------------------------------------------------- jeu « Course » (éviter les voitures)
COURSE = [
 ("العقبة (السيارة)", "Lutin « voiture adverse »", f"""{FLAG}
va:set|mettre score à 0|اجعل النقاط 0
va:set|mettre vies à 3|اجعل الأرواح 3
va:set|mettre vitesse à 3|اجعل السرعة 3
mv:goto|aller à x : (nombre aléatoire entre -200 et 200) y : 190|اذهب إلى س: (عدد عشوائي بين -200 و200) ص: 190
lk:show|montrer|أظهر"""),
 ("البطل (السيارة)", "Lutin « ma voiture »", f"""{FLAG}
mv:goto|aller à x : 0 y : -125|اذهب إلى س: 0 ص: -125
lk:show|montrer|أظهر
ct:forever|répéter indéfiniment|كرّر باستمرار
  ct:if|touche flèche gauche pressée ?|هل المفتاح السهم الأيسر مضغوط؟
    mv:chx|ajouter -11 à x|غيّر س بمقدار -11
    mv:dir|s'orienter à -90|اتجه نحو -90
  ct:if|touche flèche droite pressée ?|هل المفتاح السهم الأيمن مضغوط؟
    mv:chx|ajouter 11 à x|غيّر س بمقدار 11
    mv:dir|s'orienter à 90|اتجه نحو 90
  ct:if|x > 215|س > 215
    mv:setx|mettre x à 215|اجعل س 215
  ct:if|x < -215|س < -215
    mv:setx|mettre x à -215|اجعل س -215"""),
 ("العقبة (السيارة)", "Lutin « voiture adverse » (script du drapeau vert, dans la boucle)", """ct:forever|répéter indéfiniment|كرّر باستمرار
  mv:chy|changer y de (0 − vitesse)|غيّر ص بمقدار (0 − السرعة)"""),
 ("العقبة (السيارة)", "Lutin « voiture adverse » (dans la boucle « répéter indéfiniment »)", """ct:if|y < -170|ص < -170
  va:chg|ajouter 1 à score|غيّر النقاط بمقدار 1
  va:chg|ajouter 0,15 à vitesse|غيّر السرعة بمقدار 0.15
  mv:goto|aller à x : (nombre aléatoire entre -200 et 200) y : 190|اذهب إلى س: (عدد عشوائي بين -200 و200) ص: 190"""),
 ("العقبة (السيارة)", "Lutin « voiture adverse » (dans la boucle « répéter indéfiniment »)", """ct:if|valeur absolue de (x − x de ma voiture) < 48|القيمة المطلقة لـ (س − س سيارتي) < 48
  ct:if|y < -95|ص < -95
    va:chg|ajouter -1 à vies|غيّر الأرواح بمقدار -1
    sn:play|jouer le son de choc|ابدأ صوت الاصطدام
    mv:goto|aller à x : (nombre aléatoire entre -200 et 200) y : 190|اذهب إلى س: (عدد عشوائي بين -200 و200) ص: 190"""),
 ("العقبة (السيارة)", "Lutin « voiture adverse » (dans la boucle « répéter indéfiniment »)", """ct:if|vies < 1|الأرواح < 1
  lk:say|dire (joindre « Fin de partie ! Score : » score) pendant 3 secondes|قل (اضمم «انتهت اللعبة! نقاطك: » النقاط) لمدة 3 ثوان
  ct:stop|stop tout|أوقف الكل"""),
]
# --------------------------------------------------------------------------- jeu « Saut » (le chameau saute les buissons)
SAUT = [
 ("الشجيرة", "Lutin « buisson »", f"""{FLAG}
va:set|mettre score à 0|اجعل النقاط 0
va:set|mettre vies à 3|اجعل الأرواح 3
va:set|mettre vitesse à 3|اجعل السرعة 3
mv:goto|aller à x : (nombre aléatoire entre 270 et 370) y : -120|اذهب إلى س: (عدد عشوائي بين 270 و370) ص: -120
lk:show|montrer|أظهر"""),
 ("الشجيرة", "Lutin « buisson » (à la suite du script)", """ct:forever|répéter indéfiniment|كرّر باستمرار
  mv:chx|changer x de (0 − vitesse)|غيّر س بمقدار (0 − السرعة)"""),
 ("الجمل", "Lutin « chameau »", f"""{FLAG}
va:set|mettre vitesse verticale à 0|اجعل السرعة العمودية 0
mv:goto|aller à x : -120 y : -95|اذهب إلى س: -120 ص: -95
lk:show|montrer|أظهر
ct:forever|répéter indéfiniment|كرّر باستمرار
  ct:if|touche espace pressée ?|هل المفتاح المسافة مضغوط؟
    ct:if|y < -90|ص < -90
      va:set|mettre vitesse verticale à 19|اجعل السرعة العمودية 19
  mv:chy|changer y de (vitesse verticale)|غيّر ص بمقدار (السرعة العمودية)
  va:chg|ajouter -1 à vitesse verticale|غيّر السرعة العمودية بمقدار -1
  ct:if|y < -95|ص < -95
    mv:sety|mettre y à -95|اجعل ص -95
    va:set|mettre vitesse verticale à 0|اجعل السرعة العمودية 0"""),
 ("الشجيرة", "Lutin « buisson » (dans la boucle « répéter indéfiniment »)", """ct:if|x < -270|س < -270
  va:chg|ajouter 1 à score|غيّر النقاط بمقدار 1
  va:chg|ajouter 0,15 à vitesse|غيّر السرعة بمقدار 0.15
  mv:goto|aller à x : (nombre aléatoire entre 270 et 370) y : -120|اذهب إلى س: (عدد عشوائي بين 270 و370) ص: -120"""),
 ("الشجيرة", "Lutin « buisson » (dans la boucle « répéter indéfiniment »)", """ct:if|valeur absolue de (x + 120) < 45|القيمة المطلقة لـ (س + 120) < 45
  ct:if|y du chameau < -45|ص الجمل < -45
    va:chg|ajouter -1 à vies|غيّر الأرواح بمقدار -1
    sn:play|jouer le son de choc|ابدأ صوت الاصطدام
    mv:goto|aller à x : (nombre aléatoire entre 270 et 370) y : -120|اذهب إلى س: (عدد عشوائي بين 270 و370) ص: -120"""),
 ("الشجيرة", "Lutin « buisson » (dans la boucle « répéter indéfiniment »)", """ct:if|vies < 1|الأرواح < 1
  lk:say|dire (joindre « Fin de partie ! Score : » score) pendant 3 secondes|قل (اضمم «انتهت اللعبة! نقاطك: » النقاط) لمدة 3 ثوان
  ct:stop|stop tout|أوقف الكل"""),
]
# --------------------------------------------------------------------------- jeu « Labyrinthe » (la souris et le fromage)
LABY = [
 ("الفأرة", "Lutin « souris »", f"""{FLAG}
va:set|mettre score à 0|اجعل النقاط 0
va:set|mettre frames à 0|اجعل الإطارات 0
va:set|mettre temps à 60|اجعل الوقت 60
lk:size|mettre la taille à 22 %|اجعل الحجم 22 %
mv:goto|aller à x : -200 y : -130|اذهب إلى س: -200 ص: -130
lk:show|montrer|أظهر"""),
 ("الفأرة", "Lutin « souris » (script du drapeau vert, dans la boucle « répéter indéfiniment »)", """ct:forever|répéter indéfiniment|كرّر باستمرار
  va:set|mettre x précédent à (x)|اجعل س السابق (س)
  va:set|mettre y précédent à (y)|اجعل ص السابق (ص)
  ct:if|touche flèche gauche pressée ?|هل المفتاح السهم الأيسر مضغوط؟
    mv:chx|ajouter -4 à x|غيّر س بمقدار -4
    mv:dir|s'orienter à -90|اتجه نحو -90
  ct:if|touche flèche droite pressée ?|هل المفتاح السهم الأيمن مضغوط؟
    mv:chx|ajouter 4 à x|غيّر س بمقدار 4
    mv:dir|s'orienter à 90|اتجه نحو 90
  ct:if|touche flèche haut pressée ?|هل المفتاح السهم الأعلى مضغوط؟
    mv:chy|ajouter 4 à y|غيّر ص بمقدار 4
  ct:if|touche flèche bas pressée ?|هل المفتاح السهم الأسفل مضغوط؟
    mv:chy|ajouter -4 à y|غيّر ص بمقدار -4"""),
 ("الفأرة", "Lutin « souris » (dans la boucle « répéter indéfiniment », après les déplacements)", """ct:if|y > -90|ص > -90
  ct:if|y < -30|ص < -30
    ct:if|x < 156|س < 156
      mv:goto|aller à x : (x précédent) y : (y précédent)|اذهب إلى س: (س السابق) ص: (ص السابق)"""),
 ("الفأرة", "Lutin « souris » (dans la boucle « répéter indéfiniment », mur n° 2 : ouverture à gauche)", """ct:if|y > 0|ص > 0
  ct:if|y < 60|ص < 60
    ct:if|x > -156|س > -156
      mv:goto|aller à x : (x précédent) y : (y précédent)|اذهب إلى س: (س السابق) ص: (ص السابق)"""),
 ("نجمة 1", "Lutin « étoile 1 »", f"""{FLAG}
mv:goto|aller à x : 0 y : -130|اذهب إلى س: 0 ص: -130
lk:size|mettre la taille à 25 %|اجعل الحجم 25 %
lk:show|montrer|أظهر
ct:forever|répéter indéfiniment|كرّر باستمرار
  ct:if|valeur absolue de (x − x de la souris) < 30|القيمة المطلقة لـ (س − س الفأرة) < 30
    ct:if|valeur absolue de (y − y de la souris) < 30|القيمة المطلقة لـ (ص − ص الفأرة) < 30
      va:chg|ajouter 1 à score|غيّر النقاط بمقدار 1
      sn:play|jouer le son « ding »|ابدأ الصوت «ding»
      lk:hide|cacher|أخفِ
      ct:stop|stop ce script|أوقف هذا السكربت"""),
 ("الفأرة", "Lutin « souris » (dans la boucle « répéter indéfiniment »)", """va:chg|ajouter 1 à frames|غيّر الإطارات بمقدار 1
va:set|mettre temps à (60 − arrondi de (frames / 30))|اجعل الوقت (60 − تقريب (الإطارات / 30))
ct:if|y > 140|ص > 140
  lk:say|dire (joindre « Gagné ! Score : » score) pendant 3 secondes|قل (اضمم «فزت! نقاطك: » النقاط) لمدة 3 ثوان
  ct:stop|stop tout|أوقف الكل
ct:if|temps < 1|الوقت < 1
  lk:say|dire « Temps écoulé ! » pendant 3 secondes|قل «انتهى الوقت!» لمدة 3 ثوان
  ct:stop|stop tout|أوقف الكل"""),
]
SPR_FR = {}
def export():
    steps, fr = {}, {}
    for key, lst in (("catch", CATCH), ("course", COURSE), ("saut", SAUT), ("labyrinthe", LABY)):
        steps[key] = []
        for spr, spr_fr, code in lst:
            ctx = "boucle" if ("boucle" in spr_fr) else ("suite" if "suite" in spr_fr else "")
            base = re.sub(r" \(.*\)$", "", spr_fr); lab = "الكائن «" + spr + "»" + {"": "", "boucle": " — داخل حلقة «كرّر باستمرار»", "suite": " — تتمة السكربت"}[ctx]
            fr[lab] = base + {"": "", "boucle": " — dans la boucle « répéter indéfiniment »", "suite": " — suite du script"}[ctx]
            tok, f = parse(code); fr.update(f); steps[key].append(dict(sprite=lab, tok=tok))
        assert len(steps[key]) == 6
    return dict(code=CODE, steps=steps), fr
if __name__ == "__main__":
    e, f = export(); print({k: [len(s["tok"]) for s in v] for k, v in e["steps"].items()}, len(f))
