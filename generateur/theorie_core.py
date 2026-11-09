"""Briques communes de la rubrique « Théorie Scratch » : enregistrement des traductions, blocs Scratch, questions de QCM et activités interactives.
Chaque texte est un couple (français, arabe). P(fr, ar) enregistre la traduction (arabe -> français) et renvoie le texte arabe, celui que la page affiche ;
la page le retraduit en français avec le dictionnaire exporté (voir theorie.py). Deux textes français différents pour le même texte arabe font échouer la génération."""

FRM = {}          # texte arabe -> texte français (traductions de toute la rubrique)


def P(fr, ar):
    if ar in FRM and FRM[ar] != fr:
        raise ValueError(f"traduction en conflit pour {ar!r} : {FRM[ar]!r} / {fr!r}")
    FRM[ar] = fr
    return ar


# ----------------------------------------------------------------------------- accords arabes des nombres
def steps_ar(n): return {1: "خطوة واحدة", 2: "خطوتين"}.get(n) or (f"{n} خطوات" if 3 <= n <= 10 else f"{n} خطوة")
def times_ar(n): return {2: "مرتين"}.get(n) or (f"{n} مرات" if 3 <= n <= 10 else f"{n} مرة")
def secs_fr(n): return "1 seconde" if n == 1 else f"{n} secondes"


# ----------------------------------------------------------------------------- blocs : c = famille (ev mv lk sn ct se op va my pen), t = texte affiché (arabe)
def N(c, fr, ar, **kw):
    d = dict(c=c, t=P(fr, ar))
    d.update(kw)
    return d


def flag(): return N("ev", "quand le drapeau vert est cliqué", "عند النقر على العلم الأخضر", op="hat", hat=True)
def key_space(): return N("ev", "quand la touche espace est pressée", "عند ضغط مفتاح المسافة", op="hat", hat=True)
def clicked(): return N("ev", "quand ce lutin est cliqué", "عند النقر على هذا اللاعب", op="hat", hat=True)
def recv(fr, ar): return N("ev", f"quand je reçois {fr}", f"عند استلام {ar}", op="hat", hat=True)
def send(fr, ar): return N("ev", f"envoyer à tous {fr}", f"أرسل {ar} إلى الجميع", op="send")
def move(n): return N("mv", f"avancer de {n} pas", f"تحرك {steps_ar(n)}", op="move", n=n)
def turn_r(d): return N("mv", f"tourner ↻ de {d} degrés", f"استدر يمينا {d} درجة", op="turn", d=d)
def turn_l(d): return N("mv", f"tourner ↺ de {d} degrés", f"استدر يسارا {d} درجة", op="turn", d=-d)
def goto(x, y): return N("mv", f"aller à x : {x} y : {y}", f"اذهب إلى س: {x} ص: {y}", op="goto", x=x, y=y)
def say(fr, ar): return N("lk", f"dire {fr}", f"قل {ar}", op="say", text=P(fr, ar), s=0)
def say_for(fr, ar, s): return N("lk", f"dire {fr} pendant {secs_fr(s)}", f"قل {ar} لمدة {s} ثانية", op="say", text=P(fr, ar), s=s)
def next_costume(): return N("lk", "basculer sur le costume suivant", "بدّل إلى الزي التالي", op="costume")
def play(fr, ar): return N("sn", f"jouer le son {fr}", f"شغّل الصوت {ar}", op="play")
def pen_down(): return N("pen", "stylo en position d'écriture", "أنزل القلم", op="pendown")
def pen_up(): return N("pen", "relever le stylo", "ارفع القلم", op="penup")
def repeat(n, body): return dict(N("ct", f"répéter {n} fois", f"كرّر {times_ar(n)}", op="repeat", n=n), body=body)
def forever(body): return dict(N("ct", "répéter indéfiniment", "كرّر باستمرار", op="forever"), body=body)
def touching(fr, ar, obj): return N("se", f"touche {fr} ?", f"هل تلمس {ar}؟", op="touch", obj=obj)
def cmp_gt(fr, ar): return N("op", fr, ar, op="cmp")
def if_(cond, body): return dict(c="ct", t=P("si … alors", "إذا … فإن"), pre=P("si", "إذا"), post=P("alors", "فإن"), op="if", cond=cond, body=body)
def if_else(cond, a, b):
    d = if_(cond, a)
    d.update(op="ifelse", els=b, else_t=P("sinon", "وإلا"))
    return d
# cartes du jeu du robot (séance 22, sans ordinateur)
def fwd(): return N("mv", "⬆ avancer d'une case", "⬆ تقدّم خانة واحدة", op="fwd")
def right(): return N("mv", "⟳ tourner à droite", "⟳ استدر إلى اليمين", op="right")
def left(): return N("mv", "⟲ tourner à gauche", "⟲ استدر إلى اليسار", op="left")


# ----------------------------------------------------------------------------- QCM : q = (fr, ar), opts = couples de textes ou blocs, ans = indice de la bonne réponse ; les réponses sont mélangées à l'affichage
def QZ(q, opts, ans, why=None, blk=None):
    return dict(q=P(*q), o=[o if isinstance(o, dict) else P(*o) for o in opts], a=ans, why=P(*why) if why else None, blk=blk)


# ----------------------------------------------------------------------------- activités interactives
def W_order(title, prompt, goal, items):
    """remettre dans l'ordre : items = bonne réponse (le premier élément est mélangé avec les autres à l'affichage)"""
    return dict(k="order", t=P(*title), p=P(*prompt), goal=P(*goal), items=[i if isinstance(i, dict) else dict(c="", t=P(*i)) for i in items])


def W_trace(title, prompt, script, world="stage", init=None, coords=False, scenarios=None, predict=None, grid=None, objects=None, end=None):
    """exécution pas à pas : script = liste de blocs (voir ci-dessus) ; predict = (question, options, indice) ; scenarios = [(texte, init)] ;
    objects = objets fixes de la scène [{art, x, y}] ; end = phrase affichée à la fin de l'exécution"""
    d = dict(k="trace", t=P(*title), p=P(*prompt), world=world, script=script, init=init or dict(x=0, y=0, dir=90), coords=coords, grid=grid, objects=objects or [])
    if scenarios: d["scenarios"] = [dict(t=P(*t), init=i) for t, i in scenarios]
    if predict: d["predict"] = dict(q=P(*predict[0]), o=[P(*o) for o in predict[1]], a=predict[2], ok=P(*predict[3]), ko=P(*predict[4]))
    if end: d["end"] = P(*end)
    return d


def W_coord(title, prompt, targets): return dict(k="coord", t=P(*title), p=P(*prompt), targets=targets)
def W_iface(title, prompt): return dict(k="iface", t=P(*title), p=P(*prompt))
def W_quiz(title, prompt, qs): return dict(k="quiz", t=P(*title), p=P(*prompt), qs=qs)
