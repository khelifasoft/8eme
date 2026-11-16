import json, os, shutil, zipfile
from lib import *
import os
REPO = os.environ.get('NEXTJS_REPO', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '8eme-nextjs-postgres')); R = 'res_r'; K = 'requin'
DM, DE, SH1, SH2, P1, P2, BT = f'{R}/decor-mer.svg', f'{R}/decor-menu.svg', f'{R}/requin-1.svg', f'{R}/requin-2.svg', f'{R}/poisson-1.svg', f'{R}/poisson-2.svg', f'{R}/bouton-commencer.svg'
fishes = lambda pts, s=.7: ''.join(place(P1 if i % 2 else P2, x, y, s) for i, (x, y) in enumerate(pts))
FP = [(70, 90), (400, 80), (120, 250), (360, 230), (240, 70), (440, 170), (50, 170), (300, 150), (190, 190), (420, 280)]
def img(lang, n):
    ar = lang == 'ar'; sc = 'النقاط' if ar else 'score'; L = lambda fr, a: a if ar else fr; mon = lambda v: monitor(sc, v)
    if n == 1: return scene(bg(DE), place(SH1, 340, 210, .8), place(BT, 190, 285, 1), mon(0), arrow(120, 200, 150, 270), pill(20, 160, L('1  Menu : bouton Commencer', '1  القائمة: زر ابدأ'), 210))
    if n == 2: return scene(bg(DM), place(SH2, 240, 180, .8), mon(0), arrow(130, 300, 190, 215), pill(20, 300, L('2  Clic : le jeu démarre', '2  النقر: تبدأ اللعبة'), 190))
    if n == 3: return scene(bg(DM), place(SH2, 240, 190, .8), fishes(FP), mon(0), pill(130, 318, L('3  10 poissons apparaissent', '3  تظهر 10 أسماك'), 220))
    if n == 4: return scene(bg(DM), place(SH1, 240, 190, .8), mon(0), arrow(240, 150, 240, 90), arrow(240, 235, 240, 295), arrow(310, 190, 400, 190), arrow(170, 190, 80, 190), pill(262, 100, L('4  Flèches ↑ ↓ ← →', '4  الأسهم ↑ ↓ ← →'), 190))
    if n == 5: return scene(bg(DM), place(SH1, 130, 230, .8), fishes([(330, 110), (400, 220), (260, 280), (60, 100)]), mon(0), arrow(330, 150, 300, 200), pill(150, 60, L('5  Poissons : ils nagent', '5  الأسماك تسبح'), 190))
    if n == 6: return scene(bg(DM), place(SH2, 220, 190, .8), place(P1, 292, 190, .7), fishes([(380, 90), (90, 260)]), mon(1), pill(150, 250, L('6  +1 point et un son', '6  نقطة زائدة وصوت'), 200), arrow(300, 240, 275, 205))
    return scene(bg(DM), place(SH1, 240, 200, .8), mon(10), f'<rect x="150" y="90" width="190" height="44" rx="14" fill="#fff" stroke="{ST}" stroke-width="3"/><text x="245" y="119" text-anchor="middle" font-family="Tajawal,Arial,sans-serif" font-size="17" font-weight="bold" fill="{ST}">{L("Bravo ! 10 poissons mangés", "أحسنت! أكلتَ 10 أسماك")}</text>', pill(150, 300, L('7  But : 10 points', '7  الهدف: 10 نقاط'), 170))
TT = [('Le menu', 'القائمة', "Au début, l'arrière-plan « menu » s'affiche avec le titre du jeu, le requin et le bouton « Commencer ».", 'في البداية تظهر خلفية «القائمة» مع عنوان اللعبة والقرش وزر «ابدأ».'),
      ('Je clique sur Commencer', 'أنقر على ابدأ', "Le bouton se cache et envoie le message « ابدأ » à tous : l'arrière-plan devient la mer et le requin apparaît.", 'يختفي الزر ويرسل رسالة «ابدأ» إلى الجميع: تصبح الخلفية البحر ويظهر القرش.'),
      ('Les poissons apparaissent', 'تظهر الأسماك', "Le lutin poisson met le score à 0 puis crée 10 clones de lui-même, placés au hasard.", 'تجعل السمكة النقاط 0 ثم تصنع 10 نسخ من نفسها في أماكن عشوائية.'),
      ('Je déplace le requin', 'أحرّك القرش', "Avec les flèches, le requin se tourne et avance de 5 pas vers la droite, la gauche, le haut ou le bas.", 'بالأسهم يتجه القرش ويتقدم 5 خطوات نحو اليمين أو اليسار أو الأعلى أو الأسفل.'),
      ('Les poissons nagent', 'الأسماك تسبح', "Chaque clone tourne un peu, avance de 3 pas et rebondit sur les bords : les poissons nagent sans arrêt.", 'تدور كل نسخة قليلا وتتقدم 3 خطوات وترتد عند الحواف: فتسبح الأسماك دون توقف.'),
      ('Le requin mange un poisson', 'القرش يأكل سمكة', "Si le poisson touche le requin : un son retentit, le score augmente de 1 et ce clone est supprimé.", 'إذا لمست السمكة القرش: يُسمع صوت وتزيد النقاط بواحد وتُحذف هذه النسخة.'),
      ('But : 10 points', 'الهدف: 10 نقاط', "Quand le score vaut 10, un son de victoire retentit, le requin dit « Bravo ! » et le jeu s'arrête.", 'عندما تصبح النقاط 10 يُسمع صوت الفوز ويقول القرش «أحسنت!» وتتوقف اللعبة.')]
etapes = []
for i, (tf, ta, cf, ca) in enumerate(TT, 1):
    for lang, name in (('fr', f'{K}-{i}.svg'), ('ar', f'{K}-ar-{i}.svg')): open(f'{REPO}/public/img/etapes/{name}', 'w', encoding='utf-8').write(img(lang, i))
    etapes.append({'img': {'fr': f'/img/etapes/{K}-{i}.svg', 'ar': f'/img/etapes/{K}-ar-{i}.svg'}, 't': {'ar': ta, 'fr': tf}, 'c': {'ar': ca, 'fr': cf}})
open(f'{REPO}/public/jeux/couvertures/{K}.svg', 'w', encoding='utf-8').write(scene(bg(DM), place(SH2, 220, 190, 1.3), place(P1, 340, 160, 1.1), place(P2, 90, 280, 1.1), place(P1, 400, 270, 1)))
FLAG = lambda: T('ev', 'flag', 0, 'quand le drapeau vert est cliqué', 'عند النقر على العلم الأخضر')
RECV = lambda: T('ev', 'recv', 0, 'quand je reçois « ابدأ »', 'عند استقبال «ابدأ»')
sols = []
S = lambda fr, ar, tok: {'sprite': {'ar': ar, 'fr': fr}, 'tok': tok}
sols.append(S('Lutin « bouton Commencer »', 'الكائن «زر البدء»', [FLAG(), T('lk', 'show', 0, 'montrer', 'أظهر'), T('mv', 'goto', 0, 'aller à x : -16 y : -118', 'اذهب إلى س: -16 ص: -118'),
    T('ev', 'click', 0, 'quand ce lutin est cliqué', 'عند النقر على هذا الكائن'), T('lk', 'hide', 0, 'cacher', 'أخف'), T('ev', 'send', 0, 'envoyer à tous « ابدأ »', 'أرسل إلى الجميع «ابدأ»')]))
sols.append(S('Scène et lutin « requin »', 'المنصة والكائن «القرش»', [RECV(), T('lk', 'backdrop', 0, "basculer sur l'arrière-plan « mer »", 'بدّل الخلفية إلى «البحر»'),
    FLAG(), T('lk', 'hide', 0, 'cacher', 'أخف'), RECV(), T('lk', 'show', 0, 'montrer', 'أظهر')]))
sols.append(S('Lutin « poisson »', 'الكائن «السمكة»', [RECV(), T('va', 'set', 0, 'mettre score à 0', 'اجعل النقاط 0'), T('lk', 'show', 0, 'montrer', 'أظهر'), T('ct', 'repeat', 0, 'répéter 10 fois', 'كرّر 10 مرات'),
    T('ct', 'clone', 1, 'créer un clone de moi-même', 'أنشئ نسخة من نفسي'), T('mv', 'goto', 1, 'aller à position aléatoire', 'اذهب إلى موقع عشوائي'), T('lk', 'next', 1, 'costume suivant', 'الزي التالي'), T('lk', 'hide', 0, 'cacher', 'أخف')]))
def kif(d, key, fr, ar, body): return [IF(d, f'touche {key} pressée ?', f'هل المفتاح {ar} مضغوط؟')] + body
sols.append(S('Lutin « requin »', 'الكائن «القرش»', [FLAG(), T('mv', 'rot', 0, 'fixer le sens de rotation gauche-droite', 'اضبط نمط الدوران يمين-يسار'), T('ct', 'forever', 0, 'répéter indéfiniment', 'كرّر باستمرار')]
    + kif(1, 'flèche droite', '', 'السهم الأيمن', [T('mv', 'dir', 2, "s'orienter à 90", 'اتجه نحو 90'), T('mv', 'chx', 2, 'ajouter 5 à x', 'أضف 5 إلى س')])
    + kif(1, 'flèche gauche', '', 'السهم الأيسر', [T('mv', 'dir', 2, "s'orienter à -90", 'اتجه نحو -90'), T('mv', 'chx', 2, 'ajouter -5 à x', 'أضف -5 إلى س')])
    + kif(1, 'flèche haut', '', 'السهم الأعلى', [T('mv', 'dir', 2, "s'orienter à 0", 'اتجه نحو 0'), T('mv', 'chy', 2, 'ajouter 5 à y', 'أضف 5 إلى ص')])
    + kif(1, 'flèche bas', '', 'السهم الأسفل', [T('mv', 'dir', 2, "s'orienter à 180", 'اتجه نحو 180'), T('mv', 'chy', 2, 'ajouter -5 à y', 'أضف -5 إلى ص')])))
sols.append(S('Lutin « poisson » — clone', 'الكائن «السمكة» — النسخة', [T('ev', 'whenclone', 0, 'quand je commence comme un clone', 'عندما أبدأ كنسخة'), T('ct', 'forever', 0, 'répéter indéfiniment', 'كرّر باستمرار'),
    T('mv', 'turnl', 1, 'tourner ↺ de 3 degrés', 'دُر ↺ بمقدار 3 درجات'), T('mv', 'move', 1, 'avancer de 3 pas', 'تقدم 3 خطوات'), T('mv', 'turnr', 1, 'tourner ↻ de 2 degrés', 'دُر ↻ بمقدار 2 درجة'),
    T('mv', 'bounce', 1, 'rebondir si le bord est atteint', 'ارتدّ إذا لمست الحافة'), T('mv', 'rot', 1, 'fixer le sens de rotation gauche-droite', 'اضبط نمط الدوران يمين-يسار')]))
sols.append(S('Lutin « poisson » — clone, dans la boucle « répéter indéfiniment »', 'الكائن «السمكة» — النسخة، داخل حلقة «كرّر باستمرار»', [IF(0, 'touche requin ?', 'ألمس القرش؟'),
    T('sn', 'play', 1, 'jouer le son « glouglou »', 'شغّل صوت «الأكل»'), T('va', 'chg', 1, 'ajouter 1 à score', 'أضف 1 إلى النقاط'), T('ct', 'delclone', 1, 'supprimer ce clone', 'احذف هذه النسخة')]))
sols.append(S('Lutin « requin » — quand je reçois « ابدأ »', 'الكائن «القرش» — عند استقبال «ابدأ»', [RECV(), T('lk', 'show', 0, 'montrer', 'أظهر'), T('ct', 'waituntil', 0, 'attendre jusqu\'à ce que score = 10', 'انتظر حتى تصبح النقاط = 10'),
    T('sn', 'play', 0, 'jouer le son « victoire » jusqu\'au bout', 'شغّل صوت «الفوز» حتى النهاية'), T('lk', 'say', 0, 'dire « Bravo ! 10 poissons mangés » pendant 3 secondes', 'قل «أحسنت! أكلتَ 10 أسماك» لمدة 3 ثوان'), T('ct', 'stop', 0, 'stop tout', 'أوقف الكل')]))
B = lambda fr, ar: {'ar': ar, 'fr': fr}
fi = {'title': B('Le jeu du requin', 'لعبة القرش'), 'meta': B('8eme année · 2 séances de 45 minutes', 'السنة الثامنة · حصتان من 45 دقيقة'),
      'situation': B("Comment créer un menu avec un bouton, déplacer un requin avec les flèches, faire nager dix poissons (clones) et gagner en atteignant 10 points ?", 'كيف ننشئ قائمة بزر، ونحرّك قرشا بالأسهم، ونجعل عشر أسماك (نسخ) تسبح، ونفوز ببلوغ 10 نقاط؟'),
      'steps': [B('Besoin à faire émerger sans ordinateur (10 min)', 'حاجة تُستخلص دون حاسوب (10 د)'), B('Jouer et décrire (10 min)', 'نلعب ونصف (10 د)'), B('Lire les scripts (15 min)', 'نقرأ السكربتات (15 د)'), B('Modifier et optimiser (20 min)', 'نعدّل ونحسّن (20 د)'), B('Tester et corriger (10 min)', 'نختبر ونصحّح (10 د)')],
      'eleve': [B('Complète la carte mentale du jeu (décors, personnages, sons, score, but, commandes).', 'أكمل الخريطة الذهنية للعبة (الخلفيات والشخصيات والأصوات والنقاط والهدف والتحكم).'), B('Trouve le script qui change l\'arrière-plan : quel message le déclenche ?', 'ابحث عن السكربت الذي يغيّر الخلفية: أي رسالة تُطلقه؟'),
                B('Explique la différence entre le lutin « poisson » et ses clones.', 'اشرح الفرق بين الكائن «السمكة» ونسخه.'), B('Change le nombre de clones (10) et le but (10) : teste et explique.', 'غيّر عدد النسخ (10) والهدف (10): اختبر وفسّر.'),
                B('Défi : ajoute un « poisson-piège » qui retire 1 point.', 'تحدٍّ: أضف «سمكة فخ» تنقص نقطة.')],
      'criteres': [B('L\'élève explique le rôle du message « ابدأ » entre le bouton, la scène et les lutins.', 'يشرح التلميذ دور رسالة «ابدأ» بين الزر والمنصة والكائنات.'), B('Il distingue le lutin d\'origine de ses clones.', 'يميّز الكائن الأصلي عن نسخه.'), B('Une amélioration est testée.', 'يُختبَر تحسين واحد.')],
      'allegee': B('Changer uniquement le nombre de poissons ou la vitesse du requin.', 'تغيير عدد الأسماك أو سرعة القرش فقط.'),
      'prolongement': B('Ajouter un chronomètre : le joueur doit manger les 10 poissons en moins de 30 secondes.', 'إضافة مؤقّت: على اللاعب أن يأكل الأسماك العشر في أقل من 30 ثانية.')}
item = lambda f, ty, a, b: {'file': f'/jeux/ressources/{K}/{f}', 'type': ty, 't': B(b, a)}
resitems = [item('decor-menu.svg', 'image', 'الخلفية: القائمة', 'Décor : le menu'), item('decor-mer.svg', 'image', 'الخلفية: البحر', 'Décor : la mer'), item('requin-1.svg', 'image', 'القرش: الزي 1', 'Le requin : costume 1'), item('requin-2.svg', 'image', 'القرش: الزي 2', 'Le requin : costume 2'),
            item('poisson-1.svg', 'image', 'السمكة: الزي 1', 'Le poisson : costume 1'), item('poisson-2.svg', 'image', 'السمكة: الزي 2', 'Le poisson : costume 2'), item('bouton-commencer.svg', 'image', 'زر «ابدأ»', 'Le bouton « Commencer »'),
            item('musique-mer.wav', 'son', 'موسيقى الخلفية: البحر', 'Musique de fond : la mer'), item('son-glouglou.wav', 'son', 'صوت أكل القرش لسمكة', 'Son quand le requin mange'), item('son-victoire.wav', 'son', 'صوت الفوز', 'Son de victoire')]
game = {'key': K, 'cat': 'catch', 'title': B('Le jeu du requin', 'لعبة القرش'), 'how': B('Clique sur « Commencer », puis déplace le requin avec les flèches du clavier pour manger les 10 poissons.', 'انقر على «ابدأ» ثم حرّك القرش بأسهم لوحة المفاتيح ليأكل الأسماك العشر.'),
        'cover': f'/jeux/couvertures/{K}.svg', 'sb3': f'/api/jeu/{K}', 'video': None, 'fiche': K, 'ressources': {'zip': f'/jeux/ressources/ressources-{K}.zip', 'items': resitems}, 'fi': fi, 'etapes': etapes}
dst = f'{REPO}/public/jeux/ressources/{K}'; shutil.rmtree(dst, ignore_errors=True); shutil.copytree(R, dst)
with zipfile.ZipFile(f'{REPO}/public/jeux/ressources/ressources-{K}.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir(R)): z.write(f'{R}/{f}', f)
shutil.copy('jeu_requin.sb3', f'{REPO}/content/private/jeux/jeu_{K}.sb3')
jp = f'{REPO}/content/public/jeux.json'; d = json.load(open(jp, encoding='utf-8')); d['games'] = [g for g in d['games'] if g['key'] != K] + [game]
open(jp, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, separators=(',', ':')))
sp = f'{REPO}/content/private/jeux-solutions.json'; s = json.load(open(sp, encoding='utf-8')); s[K] = sols
open(sp, 'w', encoding='utf-8').write(json.dumps(s, ensure_ascii=False, separators=(',', ':')))
print('ok', len(etapes), len(sols))
