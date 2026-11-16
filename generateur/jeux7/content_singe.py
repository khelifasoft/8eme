import json, os, shutil, zipfile
from lib import *
import os
REPO = os.environ.get('NEXTJS_REPO', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '8eme-nextjs-postgres'))
R = 'res'; K = 'singe'
D, P, SG, BA, OR = f'{R}/decor-jeu.svg', f'{R}/decor-perdu.svg', f'{R}/singe.svg', f'{R}/banane.svg', f'{R}/orange.svg'
SX, SY = 240, 282          # singe au départ (centre, coordonnées SVG)
# ---------- 6 étapes en images : (fr/ar) titre, légende, calques
def img(lang, n):
    ar = lang == 'ar'; sc = 'النقاط' if ar else 'score'
    mon = lambda v: monitor(sc, v)
    L = lambda fr, a: a if ar else fr
    if n == 1: return scene(bg(D), place(SG, SX, SY), mon(0), arrow(130, 120, 218, 236), pill(40, 82, L('1  Drapeau vert', '1  العلم الأخضر')))
    if n == 2: return scene(bg(D), place(SG, 330, SY), mon(0), arrow(240, 200, 330, 200), arrow(240, 200, 150, 200), pill(150, 160, L('2  Flèches ← →', '2  السهمان ← →')))
    if n == 3: return scene(bg(D), place(SG, SX, SY), place(BA, 150, 120), mon(0), arrow(150, 150, 150, 228), pill(176, 96, L('3  Banane : elle tombe', '3  الموزة تسقط')))
    if n == 4: return scene(bg(D), place(SG, 200, SY), place(BA, 205, 222, .9), mon(1), pill(226, 196, L('4  +1 point', '4  نقطة زائدة'), 120), arrow(330, 140, 232, 210))
    if n == 5: return scene(bg(D), place(SG, SX, SY), place(OR, 300, 150), mon(1), arrow(300, 180, 300, 244), pill(150, 90, L('5  Orange : elle tombe', '5  البرتقالة تسقط')))
    return scene(bg(P), mon(1), pill(140, 290, L('6  Message « perdu »', '6  رسالة «خسرت»'), 200))
TT = [('Début de partie', 'بداية اللعبة', "Je clique sur le drapeau vert : le singe se place au départ, en bas de la scène, et le score est à 0.", 'أنقر على العلم الأخضر: يقف القرد في مكانه الأول أسفل المنصة والنقاط 0.'),
      ('Je déplace le singe', 'أحرّك القرد', "J'appuie sur la flèche gauche ou droite : le singe se déplace de 10 pas dans cette direction, jusqu'à ce qu'il touche une orange.", 'أضغط على السهم الأيسر أو الأيمن: يتحرك القرد 10 خطوات في ذلك الاتجاه إلى أن يلمس برتقالة.'),
      ('Une banane tombe', 'موزة تسقط', "La banane apparaît à une position choisie en haut de la scène, s'oriente vers le bas et avance jusqu'à toucher le sol ou le singe.", 'تظهر الموزة في مكان مختار أعلى المنصة وتتجه نحو الأسفل وتتقدم إلى أن تلمس الأرض أو القرد.'),
      ('Banane attrapée', 'موزة ملتقطة', "Si la banane touche le singe : elle se cache, le score augmente de 1 et un petit son retentit. Si elle touche le sol : elle se cache seulement.", 'إذا لمست الموزة القرد: تختفي وتزيد النقاط بواحد ويُسمع صوت قصير. وإذا لمست الأرض: تختفي فقط.'),
      ('Une orange tombe', 'برتقالة تسقط', "L'orange tombe comme la banane. Si elle touche le sol, elle se cache et le jeu continue.", 'تسقط البرتقالة مثل الموزة. إذا لمست الأرض تختفي وتستمر اللعبة.'),
      ('Perdu !', 'خسرت!', "Si l'orange touche le singe : elle se cache, le message « perdu » est envoyé à tous, l'arrière-plan change et le jeu s'arrête.", 'إذا لمست البرتقالة القرد: تختفي وتُرسل رسالة «خسرت» إلى الجميع، فتتغير الخلفية وتتوقف اللعبة.')]
os.makedirs(f'{REPO}/public/img/etapes', exist_ok=True)
etapes = []
for i, (tf, ta, cf, ca) in enumerate(TT, 1):
    for lang, name in (('fr', f'{K}-{i}.svg'), ('ar', f'{K}-ar-{i}.svg')): open(f'{REPO}/public/img/etapes/{name}', 'w', encoding='utf-8').write(img(lang, i))
    etapes.append({'img': {'fr': f'/img/etapes/{K}-{i}.svg', 'ar': f'/img/etapes/{K}-ar-{i}.svg'}, 't': {'ar': ta, 'fr': tf}, 'c': {'ar': ca, 'fr': cf}})
# ---------- couverture
open(f'{REPO}/public/jeux/couvertures/{K}.svg', 'w', encoding='utf-8').write(scene(bg(D), place(SG, 250, 270, 1.15), place(BA, 120, 110, 1.2), place(OR, 370, 140, 1.2)))
# ---------- solutions (un script par étape)
F = lambda f, a: (f, a)
sing = [T('ev', 'flag', 0, 'quand le drapeau vert est cliqué', 'عند النقر على العلم الأخضر'), T('mv', 'goto', 0, 'aller à x : 0 y : -106', 'اذهب إلى س: 0 ص: -106'), T('lk', 'show', 0, 'montrer', 'أظهر')]
sing2 = [UNTIL(0, 'touche orange ?', 'ألمس البرتقالة؟'),
         IF(1, 'touche flèche gauche pressée ?', 'هل المفتاح السهم الأيسر مضغوط؟'), T('mv', 'chx', 2, 'ajouter -10 à x', 'أضف -10 إلى س'),
         IF(1, 'touche flèche droite pressée ?', 'هل المفتاح السهم الأيمن مضغوط؟'), T('mv', 'chx', 2, 'ajouter 10 à x', 'أضف 10 إلى س'),
         T('ev', 'send', 0, 'envoyer à tous « perdu »', 'أرسل إلى الجميع «خسرت»')]
ban_start = [T('ev', 'flag', 0, 'quand le drapeau vert est cliqué', 'عند النقر على العلم الأخضر'), T('va', 'set', 0, 'mettre score à 0', 'اجعل النقاط 0'), T('lk', 'hide', 0, 'cacher', 'أخف'),
             T('ct', 'forever', 0, 'répéter indéfiniment', 'كرّر باستمرار'), T('mv', 'goto', 1, 'aller à x : (nombre aléatoire entre -200 et 200) y : 170', 'اذهب إلى س: (عدد عشوائي بين -200 و200) ص: 170'), T('lk', 'show', 1, 'montrer', 'أظهر')]
fall = lambda who_fr, who_ar: [UNTIL(0, 'touche le sol ou touche le singe ?', 'ألمس الأرض أو ألمس القرد؟'), T('mv', 'dir', 1, "s'orienter à 180", 'اتجه نحو 180'), T('mv', 'move', 1, 'avancer de 5 pas', 'تقدم 5 خطوات')]
ban_hit = [IF(0, 'touche le sol ?', 'ألمس الأرض؟'), T('lk', 'hide', 1, 'cacher', 'أخف'),
           IF(0, 'touche le singe ?', 'ألمس القرد؟'), T('lk', 'hide', 1, 'cacher', 'أخف'), T('va', 'chg', 1, 'ajouter 1 à score', 'أضف 1 إلى النقاط'), T('sn', 'play', 1, 'jouer le son « banane »', 'شغّل صوت «الموزة»')]
ora = [T('ev', 'flag', 0, 'quand le drapeau vert est cliqué', 'عند النقر على العلم الأخضر'), T('lk', 'hide', 0, 'cacher', 'أخف'), T('ct', 'forever', 0, 'répéter indéfiniment', 'كرّر باستمرار'),
       T('mv', 'goto', 1, 'aller à x : (nombre aléatoire entre -200 et 200) y : 170', 'اذهب إلى س: (عدد عشوائي بين -200 و200) ص: 170'), T('lk', 'show', 1, 'montrer', 'أظهر'),
       UNTIL(1, 'touche le sol ou touche le singe ?', 'ألمس الأرض أو ألمس القرد؟'), T('mv', 'dir', 2, "s'orienter à 180", 'اتجه نحو 180'), T('mv', 'move', 2, 'avancer de 5 pas', 'تقدم 5 خطوات'),
       IF(1, 'touche le sol ?', 'ألمس الأرض؟'), T('lk', 'hide', 2, 'cacher', 'أخف'),
       IF(1, 'touche le singe ?', 'ألمس القرد؟'), T('lk', 'hide', 2, 'cacher', 'أخف'), T('ev', 'send', 2, 'envoyer à tous « perdu » et attendre', 'أرسل إلى الجميع «خسرت» وانتظر'), T('ct', 'stop', 2, 'stop tout', 'أوقف الكل')]
end = [T('ev', 'recv', 0, 'quand je reçois « perdu »', 'عند استقبال «خسرت»'), T('lk', 'backdrop', 0, "basculer sur l'arrière-plan « perdu »", 'بدّل الخلفية إلى «خسرت»'), T('sn', 'play', 0, 'jouer le son « perdu » jusqu\'au bout', 'شغّل صوت «الخسارة» حتى النهاية')]
S = lambda fr, ar, tok: {'sprite': {'ar': ar, 'fr': fr}, 'tok': tok}
sols = [S('Lutin « singe »', 'الكائن «القرد»', sing), S('Lutin « singe » — dans la boucle', 'الكائن «القرد» — تتمة السكربت', sing2),
        S('Lutin « banane »', 'الكائن «الموزة»', ban_start + [T(*[x for x in (u['c'], u['k'], u['d'] + 1, '', '')], cond=(u['cond']['ar'], u['cond']['fr']), pre=(u['pre']['ar'], u['pre']['fr']), post=None) if u['k'] == 'until' else {**u, 'd': u['d'] + 1} for u in fall('', '')]),
        S('Lutin « banane » — dans la boucle « répéter indéfiniment »', 'الكائن «الموزة» — داخل حلقة «كرّر باستمرار»', [{**u, 'd': u['d']} for u in ban_hit]),
        S('Lutin « orange »', 'الكائن «البرتقالة»', ora), S('Scène (arrière-plan)', 'المنصة (الخلفية)', end)]
# ---------- fiche pédagogique
B = lambda fr, ar: {'ar': ar, 'fr': fr}
fi = {'title': B('Le singe et les bananes', 'القرد والموز'), 'meta': B('8eme année · 2 séances de 45 minutes', 'السنة الثامنة · حصتان من 45 دقيقة'),
      'situation': B("Comment faire déplacer un singe avec les flèches du clavier, faire tomber des bananes et des oranges, compter les points et arrêter le jeu quand le singe touche une orange ?", 'كيف نحرّك قردا بأسهم لوحة المفاتيح، ونُسقط موزا وبرتقالا، ونحسب النقاط، ونوقف اللعبة عندما يلمس القرد برتقالة؟'),
      'steps': [B('Besoin à faire émerger sans ordinateur (10 min)', 'حاجة تُستخلص دون حاسوب (10 د)'), B('Jouer et décrire (10 min)', 'نلعب ونصف (10 د)'), B('Lire les scripts (15 min)', 'نقرأ السكربتات (15 د)'), B('Modifier et optimiser (20 min)', 'نعدّل ونحسّن (20 د)'), B('Tester et corriger (10 min)', 'نختبر ونصحّح (10 د)')],
      'eleve': [B('Joue jusqu\'à ce que tu perdes et note ton score.', 'العب حتى تخسر ودوّن نتيجتك.'), B('Décris le rôle des trois lutins (singe, banane, orange).', 'صف دور الكائنات الثلاثة (القرد والموزة والبرتقالة).'),
                B('Repère le bloc qui met le score à 0 et celui qui ajoute 1. Dans quel lutin sont-ils ?', 'ابحث عن الكتلة التي تجعل النقاط 0 وتلك التي تضيف 1. في أي كائن توجد؟'),
                B('Change le nombre de pas de la banane (5) : teste et explique l\'effet sur la difficulté.', 'غيّر عدد خطوات الموزة (5): اختبر وفسّر الأثر على صعوبة اللعبة.'),
                B('Défi : ajoute un lutin « citron » qui retire 1 point au singe.', 'تحدٍّ: أضف كائن «ليمونة» ينقص من القرد نقطة.')],
      'criteres': [B('L\'élève distingue les rôles des trois lutins.', 'يميّز التلميذ أدوار الكائنات الثلاثة.'), B('Il identifie la condition « touche le sol ou touche le singe » dans la boucle.', 'يحدّد الشرط «ألمس الأرض أو ألمس القرد» داخل الحلقة.'), B('Une amélioration est testée.', 'يُختبَر تحسين واحد.')],
      'allegee': B('Changer uniquement la vitesse de chute des fruits.', 'تغيير سرعة سقوط الفاكهة فقط.'),
      'prolongement': B('Faire gagner le joueur à 10 points (message « gagné ») et afficher une vie en moins pour chaque orange touchée.', 'جعل اللاعب يفوز عند 10 نقاط (رسالة «فزت») وإظهار خسارة روح عند كل برتقالة.')}
item = lambda f, ty, a, b: {'file': f'/jeux/ressources/{K}/{f}', 'type': ty, 't': B(b, a)}
resitems = [item('decor-jeu.svg', 'image', 'الخلفية: الغابة والعشب', 'Décor : la prairie'), item('decor-perdu.svg', 'image', 'الخلفية عند الخسارة', 'Décor : perdu'), item('singe.svg', 'image', 'اللاعب: القرد', 'Joueur : le singe'),
            item('banane.svg', 'image', 'الشيء الذي نلتقطه: الموزة', 'Objet à attraper : la banane'), item('orange.svg', 'image', 'الشيء الذي نتفاداه: البرتقالة', 'Objet à éviter : l\'orange'),
            item('musique-jungle.wav', 'son', 'موسيقى الخلفية: الغابة', 'Musique de fond : jungle'), item('son-banane.wav', 'son', 'صوت التقاط موزة', 'Son quand on attrape une banane'), item('son-perdu.wav', 'son', 'صوت الخسارة', 'Son quand on perd')]
game = {'key': K, 'cat': 'catch', 'title': B('Le singe et les bananes', 'القرد والموز'), 'how': B("Déplace le singe avec les flèches ← → pour attraper les bananes. Attention : si une orange touche le singe, c'est perdu !", 'حرّك القرد بالسهمين ← → لتلتقط الموز. انتبه: إذا لمست برتقالة القرد فقد خسرت!'),
        'cover': f'/jeux/couvertures/{K}.svg', 'sb3': f'/api/jeu/{K}', 'video': None, 'fiche': K, 'ressources': {'zip': f'/jeux/ressources/ressources-{K}.zip', 'items': resitems}, 'fi': fi, 'etapes': etapes}
# ---------- écriture
dst = f'{REPO}/public/jeux/ressources/{K}'; shutil.rmtree(dst, ignore_errors=True); shutil.copytree(R, dst)
with zipfile.ZipFile(f'{REPO}/public/jeux/ressources/ressources-{K}.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir(R)): z.write(f'{R}/{f}', f)
shutil.copy('jeu_singe.sb3', f'{REPO}/content/private/jeux/jeu_{K}.sb3')
jp = f'{REPO}/content/public/jeux.json'; d = json.load(open(jp, encoding='utf-8')); d['games'] = [g for g in d['games'] if g['key'] != K] + [game]
open(jp, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, separators=(',', ':')))
sp = f'{REPO}/content/private/jeux-solutions.json'; s = json.load(open(sp, encoding='utf-8')); s[K] = sols
open(sp, 'w', encoding='utf-8').write(json.dumps(s, ensure_ascii=False, separators=(',', ':')))
print('ok', len(etapes), len(sols))
