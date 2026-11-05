"""Correspondance entre les projets Scratch et la bibliothèque d'images et de sons."""
import re
import personnages as pe, animaux as an, decors as de, lieux as li
CAT = pe.catalogue()

def art_svg(kind, key, tint=None):
    if kind == "p": return pe.render_person(CAT[key][1])
    if kind == "a":
        if key == "cochon": return an.cochon(0, tint or "#f4a8b8")
        return an.ANIMAUX[key][1]()
    if kind == "d": return de.objet_svg(key)
    if kind == "l": return li.lieu_svg(key)
    raise KeyError(kind)
def svg_size(svg):
    m = re.search(r'width="(\d+)" height="(\d+)"', svg); return int(m.group(1)), int(m.group(2))

# lieux (fonds)
BACK = {
 "cinderella": {"البيت": "maison_interieur", "القصر": "salle_bal", "الطريق": "village_route"},
 "layla": {"بيت ليلى": "maison_interieur", "الغابة": "foret", "بيت الجدة": "chambre"},
 "djeha": {"الطريق": "village_route", "الجسر والنهر": "pont_riviere"},
 "alibaba": {"الجبل": "montagne", "المغارة": "grotte_interieur", "البيت": "maison_interieur"},
 "sindbad": {"الميناء": "port", "البحر": "mer", "الجزيرة": "ile", "الشاطئ": "plage"},
 "crow": {"الغابة": "foret", "تحت الشجرة": "foret_dense"},
 "hare": {"خط البداية": "piste_course", "الطريق والشجرة": "piste_course", "خط النهاية": "ligne_arrivee"},
 "lion": {"الغابة": "foret", "مكان الفخ": "foret_dense"},
 "frog": {"الحديقة والبئر": "jardin_puits", "القصر": "palais_exterieur"},
 "shepherd": {"التل": "colline_pature", "التل في المساء": "colline_soir"},
 "pigs": {"المرج": "colline_pature", "أمام بيت الآجر": "colline_pature"},
 "duckling": {"المزرعة والبركة": "etang_ferme", "البركة في الشتاء": "etang_hiver", "البركة في الربيع": "etang_printemps"},
}
# lutins : nom -> (genre, clé, taille %, retourner à gauche ?, {nom du costume: (genre, clé)})
P_, A_, D_ = "p", "a", "d"
ART = {
 "cinderella": {"سندريلا": (P_, "cendrillon_servante", 42, False, {"سندريلا · فستان": (P_, "cendrillon_bal")}), "زوجة الأب": (P_, "belle_mere", 42, False, {}),
   "الأختان": (P_, "soeur_1", 42, False, {}), "الجنية": (P_, "fee", 42, False, {}), "الأمير": (P_, "prince", 42, False, {}), "الحذاء": (D_, "soulier_verre", 45, False, {})},
 "layla": {"ليلى": (P_, "laila", 42, False, {}), "الأم": (P_, "mere", 42, False, {}), "الذئب": (A_, "loup", 55, True, {"الذئب · جدة": (A_, "loup_grand_mere")}),
   "الجدة": (P_, "grand_mere", 42, False, {}), "الحطاب": (P_, "bucheron", 42, False, {}), "السلة": (D_, "panier", 45, False, {})},
 "djeha": {"جحا": (P_, "djeha", 42, False, {}), "الابن": (P_, "fils_djeha", 38, False, {}), "الحمار": (A_, "ane", 55, True, {}),
   "المارة 1": (P_, "passant_1", 42, False, {}), "المارة 2": (P_, "passant_2", 42, False, {})},
 "alibaba": {"علي بابا": (P_, "ali_baba", 42, False, {}), "قاسم": (P_, "qasim", 42, False, {}), "مرجانة": (P_, "morgiane", 42, False, {}),
   "رئيس اللصوص": (P_, "chef_voleurs", 42, False, {}), "اللصوص": (P_, "voleur", 42, False, {}),
   "باب المغارة": (D_, "grotte_fermee", 55, False, {"باب المغارة · مفتوح": (D_, "grotte_ouverte")})},
 "sindbad": {"السندباد": (P_, "sindbad", 38, False, {}), "البحارة": (P_, "marin", 38, False, {}), "السفينة": (D_, "bateau", 75, True, {}),
   "الجزيرة": (D_, "ile", 80, False, {"حوت": (A_, "baleine")}), "اللوح": (D_, "planche", 60, True, {})},
 "crow": {"الغراب": (A_, "corbeau", 50, True, {"الغراب · فم مفتوح": (A_, "corbeau_bec_ouvert")}), "الثعلب": (A_, "renard", 55, True, {}), "الجبن": (D_, "fromage", 35, False, {})},
 "hare": {"الأرنب": (A_, "lievre", 55, True, {"الأرنب · نائم": (A_, "lievre_endormi")}), "السلحفاة": (A_, "tortue", 50, True, {}), "الحكم": (P_, "arbitre", 42, False, {})},
 "lion": {"الأسد": (A_, "lion", 60, True, {"الأسد · محبوس": (A_, "lion_piege")}), "الفأر": (A_, "souris", 45, True, {}), "الصياد": (P_, "chasseur", 42, False, {}), "الشبكة": (D_, "filet", 90, False, {})},
 "frog": {"الأميرة": (P_, "princesse", 42, False, {}), "الضفدع": (A_, "grenouille", 45, True, {"أمير": (P_, "prince")}), "الملك": (P_, "roi", 42, False, {}), "الكرة": (D_, "balle_or", 45, False, {})},
 "shepherd": {"الراعي": (P_, "berger", 42, False, {}), "الغنم": (A_, "mouton", 55, True, {}), "الذئب": (A_, "loup", 55, True, {}), "القرويون": (P_, "villageois", 42, False, {})},
 "pigs": {"الخنزير الأول": (A_, "cochon", 45, True, {}), "الخنزير الثاني": (A_, "cochon", 45, True, {}), "الخنزير الثالث": (A_, "cochon", 45, True, {}),
   "الذئب": (A_, "loup", 55, True, {}), "البيت": (D_, "maison_paille", 80, False, {"بيت القش": (D_, "maison_paille"), "بيت الخشب": (D_, "maison_bois"), "بيت الآجر": (D_, "maison_brique"), "بيت منهار": (D_, "maison_effondree")})},
 "duckling": {"البطة الأم": (A_, "canard", 50, True, {}), "الإخوة": (A_, "caneton", 50, True, {}), "البطة الصغيرة": (A_, "caneton_gris", 50, True, {"بجعة": (A_, "cygne")}),
   "البجعات": (A_, "cygne", 55, True, {})},
}
TINT = {("pigs", "الخنزير الأول"): "#f4a8b8", ("pigs", "الخنزير الثاني"): "#f2c4a0", ("pigs", "الخنزير الثالث"): "#e690ae"}
MUSIC = {"cinderella": "bal", "layla": "mystere", "djeha": "souk", "alibaba": "orientale", "sindbad": "mer", "crow": "joyeuse", "hare": "aventure",
         "lion": "joyeuse", "frog": "joyeuse", "shepherd": "joyeuse", "pigs": "joyeuse", "duckling": "triste"}
# effets sonores : à l'apparition d'un lutin, ou au changement de costume
SFX_SHOW = {("layla", "الذئب"): "loup", ("shepherd", "الذئب"): "loup", ("pigs", "الذئب"): "loup", ("lion", "الأسد"): "rugissement", ("djeha", "الحمار"): "ane",
            ("crow", "الغراب"): "corbeau", ("frog", "الضفدع"): "grenouille", ("shepherd", "الغنم"): "mouton", ("duckling", "البطة الأم"): "canard",
            ("duckling", "البجعات"): "cygne", ("cinderella", "الجنية"): "magie", ("lion", "الفأر"): "souris", ("hare", "الحكم"): "tic_tac", ("pigs", "الخنزير الأول"): "cochon"}
SFX_COSTUME = {("alibaba", "باب المغارة · مفتوح"): "grincement_porte", ("cinderella", "سندريلا · فستان"): "magie", ("frog", "أمير"): "magie",
               ("pigs", "بيت منهار"): "effondrement", ("lion", "الأسد · محبوس"): "rugissement", ("duckling", "بجعة"): "cygne", ("sindbad", "حوت"): "tonnerre"}
