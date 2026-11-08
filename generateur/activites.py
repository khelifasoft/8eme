"""Rubrique « Activités » : collection de 54 astuces et activités Scratch (50 astuces en 4 niveaux + 4 projets créatifs).
Données : activites_data1.py (niveaux 1-2, blocs) et activites_data2.py (niveaux 3-5). Chaque texte est un couple (français, arabe).
export() -> (données JSON pour la page en arabe, dictionnaire arabe -> français)"""
import activites_data1 as d1, activites_data2 as d2
ACTS = d1.ACTS1 + d1.ACTS2 + d2.ACTS3 + d2.ACTS4 + d2.ACTS5
def export():
    fr = {}
    def P(pair): fr[pair[1]] = pair[0]; return pair[1]
    levels = [dict(n=l["n"], t=l["ar"], diff=P(l["diff"]), obj=P(l["obj"])) for l in d1.LEVELS]
    for l in d1.LEVELS: fr[l["ar"]] = l["fr"]
    blocks = {k: [v[0], v[2]] for k, v in d1.BLOCKS.items()}
    for k, v in d1.BLOCKS.items(): fr[v[2]] = v[1]
    acts = [dict(n=a["n"], lvl=a["lvl"], t=P(a["title"]), obj=P(a["obj"]), blocks=a["blocks"], steps=[P(s) for s in a["steps"]], res=P(a["result"]), defi=P(a["defi"])) for a in ACTS]
    for ui in [("Collection : 50 astuces et activités Scratch", "مجموعة: 50 فكرة ونشاطا في سكراتش"), ("Activités", "الأنشطة"),
               ("50 astuces classées en quatre niveaux, puis des projets créatifs. Chaque activité suit la même fiche : objectif, blocs nécessaires, réalisation, résultat attendu et défi.", "50 فكرة مصنّفة في أربعة مستويات، ثم مشاريع إبداعية. لكل نشاط البطاقة نفسها: الهدف والكتل اللازمة والإنجاز والنتيجة المنتظرة وتحدٍّ إضافي."),
               ("Objectif", "الهدف"), ("Blocs nécessaires", "الكتل اللازمة"), ("Réalisation", "الإنجاز"), ("Résultat attendu", "النتيجة المنتظرة"), ("Défi supplémentaire", "تحدٍّ إضافي"),
               ("Ces activités permettent aux élèves de combiner plusieurs astuces.", "تتيح هذه الأنشطة للتلاميذ الجمع بين عدة أفكار.")]:
        P(ui)
    return dict(levels=levels, blocks=blocks, acts=acts), fr
if __name__ == "__main__":
    d, f = export(); print(len(d["acts"]), "activités,", len(f), "traductions")
