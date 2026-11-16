import json, zipfile, os
import lib_sb3 as L
from lib_sb3 import Sprite, costume, sound
R = 'res_r'; MSG, MSG_ID, VAR, VAR_ID = 'ابدأ', 'msg_start', 'النقاط', 'v_score'
mk = lambda: Sprite(MSG, MSG_ID, VAR, VAR_ID)
# --- scène : fonds, musique
S = mk()
S.stack([S.flag(), S.backdrop('القائمة')], top=True, x=0, y=0)
S.stack([S.recv(), S.backdrop('البحر')], top=True, x=0, y=200)
S.stack([S.flag(), S.volume(30), S.forever([S.play('موسيقى البحر', until=True)])], top=True, x=0, y=400)
# --- القرش (requin)
Sh = mk()
Sh.stack([Sh.flag(), Sh.rotstyle('left-right'), Sh.forever([
    Sh.if_(Sh.key('right arrow'), [Sh.point(90), Sh.chx(5)]), Sh.if_(Sh.key('left arrow'), [Sh.point(-90), Sh.chx(-5)]),
    Sh.if_(Sh.key('up arrow'), [Sh.point(0), Sh.chy(5)]), Sh.if_(Sh.key('down arrow'), [Sh.point(180), Sh.chy(-5)])])], top=True, x=0, y=0)
Sh.stack([Sh.flag(), Sh.forever([Sh.wait(0.3), Sh.nextcostume()])], top=True, x=400, y=0)
Sh.stack([Sh.flag(), Sh.hide()], top=True, x=400, y=300)
Sh.stack([Sh.recv(), Sh.show(), Sh.wait_until(Sh.var_eq(10)), Sh.play('صوت الفوز', until=True), Sh.say('أحسنت! أكلتَ 10 أسماك', 3), Sh.stopall()], top=True, x=400, y=500)
# --- السمكة (poisson)
F = mk()
F.stack([F.flag(), F.hide(), F.setvar(0)], top=True, x=0, y=0)
F.stack([F.recv(), F.setvar(0), F.show(), F.repeat(10, [F.clone_make(), F.goto_random(), F.nextcostume()]), F.hide()], top=True, x=0, y=200)
F.stack([F.clone_start(), F.forever([F.turnl(3), F.move(3), F.turnr(2), F.bounce(), F.rotstyle('left-right'),
    F.if_(F.touching('القرش'), [F.play('صوت الأكل'), F.chgvar(1), F.clone_del()])])], top=True, x=400, y=0)
# --- زر البدء (bouton)
Bt = mk()
Bt.stack([Bt.flag(), Bt.show(), Bt.goto(-16, -118)], top=True, x=0, y=0)
Bt.stack([Bt.thisclicked(), Bt.hide(), Bt.send()], top=True, x=0, y=300)

def target(name, sp, cs, ss, x, y, layer, size, vis, rot):
    return {'isStage': False, 'name': name, 'variables': {}, 'lists': {}, 'broadcasts': {}, 'blocks': sp.b, 'comments': {}, 'currentCostume': 0, 'costumes': cs, 'sounds': ss, 'volume': 100,
            'layerOrder': layer, 'visible': vis, 'x': x, 'y': y, 'size': size, 'direction': 90, 'draggable': False, 'rotationStyle': rot}
stage = {'isStage': True, 'name': 'Stage', 'variables': {VAR_ID: [VAR, 0]}, 'lists': {}, 'broadcasts': {MSG_ID: MSG}, 'blocks': S.b, 'comments': {}, 'currentCostume': 0,
         'costumes': [costume('القائمة', f'{R}/decor-menu.svg', 240, 180), costume('البحر', f'{R}/decor-mer.svg', 240, 180)],
         'sounds': [sound('موسيقى البحر', f'{R}/musique-mer.wav')], 'volume': 100, 'layerOrder': 0, 'tempo': 60, 'videoTransparency': 50, 'videoState': 'on', 'textToSpeechLanguage': None}
proj = {'targets': [stage,
    target('القرش', Sh, [costume('قرش 1', f'{R}/requin-1.svg', 80, 45), costume('قرش 2', f'{R}/requin-2.svg', 80, 45)], [sound('صوت الفوز', f'{R}/son-victoire.wav')], -173, 119, 1, 70, False, 'left-right'),
    target('السمكة', F, [costume('سمكة 1', f'{R}/poisson-1.svg', 32, 22), costume('سمكة 2', f'{R}/poisson-2.svg', 32, 22)], [sound('صوت الأكل', f'{R}/son-glouglou.wav')], 158, -76, 2, 60, False, 'left-right'),
    target('زر البدء', Bt, [costume('زر', f'{R}/bouton-commencer.svg', 85, 27)], [], -16, -118, 3, 100, True, 'all around')],
    'monitors': [{'id': VAR_ID, 'mode': 'default', 'opcode': 'data_variable', 'params': {'VARIABLE': VAR}, 'spriteName': None, 'value': 0, 'width': 0, 'height': 0, 'x': 5, 'y': 5, 'visible': True, 'sliderMin': 0, 'sliderMax': 100, 'isDiscrete': True}],
    'extensions': [], 'meta': {'semver': '3.0.0', 'vm': '0.2.0', 'agent': 'Mozilla/5.0'}}
out = 'jeu_requin.sb3'
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('project.json', json.dumps(proj, ensure_ascii=False))
    for k, v in L.files.items(): z.writestr(k, v)
print(out, os.path.getsize(out), {t['name']: len(t['blocks']) for t in proj['targets']})
