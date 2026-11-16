import json, hashlib, zipfile, os, shutil
R = 'res'
MSG, MSG_ID = 'خسرت', 'msg_perdu'
VAR, VAR_ID = 'النقاط', 'v_score'
GROUND = '#633f00'

class Sprite:
    def __init__(self): self.b = {}; self.n = 0
    def add(self, op, inputs=None, fields=None, shadow=False, mutation=None):
        self.n += 1; i = f'b{self.n}'
        d = {'opcode': op, 'next': None, 'parent': None, 'inputs': inputs or {}, 'fields': fields or {}, 'shadow': shadow, 'topLevel': False}
        if mutation: d['mutation'] = mutation
        self.b[i] = d; return i
    def num(self, v): return [1, [4, str(v)]]
    def stack(self, ids, top=False, x=20, y=20):
        for a, c in zip(ids, ids[1:]): self.b[a]['next'] = c; self.b[c]['parent'] = a
        if top: self.b[ids[0]].update(topLevel=True, x=x, y=y)
        return ids[0]
    def adopt(self, parent, child):
        self.b[child]['parent'] = parent
    # --- blocs
    def flag(self): return self.add('event_whenflagclicked')
    def recv(self): return self.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': [MSG, MSG_ID]})
    def send(self, wait=False): return self.add('event_broadcastandwait' if wait else 'event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, MSG, MSG_ID]]})
    def setvar(self, v): return self.add('data_setvariableto', {'VALUE': self.num(v)}, {'VARIABLE': [VAR, VAR_ID]})
    def chgvar(self, v): return self.add('data_changevariableby', {'VALUE': self.num(v)}, {'VARIABLE': [VAR, VAR_ID]})
    def goto(self, x, y):
        a = self.num(x) if not isinstance(x, tuple) else self._rand(*x); b = self.num(y)
        i = self.add('motion_gotoxy', {'X': a, 'Y': b})
        if isinstance(x, tuple): self.b[a[1]]['parent'] = i
        return i
    def _rand(self, lo, hi):
        i = self.add('operator_random', {'FROM': self.num(lo), 'TO': self.num(hi)}); return [3, i, [4, '0']]
    def chx(self, v): return self.add('motion_changexby', {'DX': self.num(v)})
    def point(self, d): return self.add('motion_pointindirection', {'DIRECTION': [1, [8, str(d)]]})
    def move(self, n): return self.add('motion_movesteps', {'STEPS': self.num(n)})
    def show(self): return self.add('looks_show')
    def hide(self): return self.add('looks_hide')
    def backdrop(self, name):
        m = self.add('looks_backdrops', fields={'BACKDROP': [name, None]}, shadow=True)
        i = self.add('looks_switchbackdropto', {'BACKDROP': [1, m]}); self.b[m]['parent'] = i; return i
    def play(self, name, until=False):
        m = self.add('sound_sounds_menu', fields={'SOUND_MENU': [name, None]}, shadow=True)
        i = self.add('sound_playuntildone' if until else 'sound_play', {'SOUND_MENU': [1, m]}); self.b[m]['parent'] = i; return i
    def volume(self, v): return self.add('sound_setvolumeto', {'VOLUME': self.num(v)})
    def stopall(self): return self.add('control_stop', fields={'STOP_OPTION': ['all', None]}, mutation={'tagName': 'mutation', 'children': [], 'hasnext': 'false'})
    # --- conditions
    def touching(self, who):
        m = self.add('sensing_touchingobjectmenu', fields={'TOUCHINGOBJECTMENU': [who, None]}, shadow=True)
        i = self.add('sensing_touchingobject', {'TOUCHINGOBJECTMENU': [1, m]}); self.b[m]['parent'] = i; return i
    def touchcolor(self, col): return self.add('sensing_touchingcolor', {'COLOR': [1, [9, col]]})
    def key(self, k):
        m = self.add('sensing_keyoptions', fields={'KEY_OPTION': [k, None]}, shadow=True)
        i = self.add('sensing_keypressed', {'KEY_OPTION': [1, m]}); self.b[m]['parent'] = i; return i
    def or_(self, a, b):
        i = self.add('operator_or', {'OPERAND1': [2, a], 'OPERAND2': [2, b]}); self.b[a]['parent'] = i; self.b[b]['parent'] = i; return i
    # --- structures
    def c(self, op, cond, body):
        inp = {'SUBSTACK': [2, body[0]]} if body else {}
        if cond: inp['CONDITION'] = [2, cond]
        i = self.add(op, inp)
        if cond: self.b[cond]['parent'] = i
        if body: self.stack(body); self.b[body[0]]['parent'] = i
        return i
    def forever(self, body): return self.c('control_forever', None, body)
    def if_(self, cond, body): return self.c('control_if', cond, body)
    def until(self, cond, body): return self.c('control_repeat_until', cond, body)

def asset(path):
    data = open(path, 'rb').read(); h = hashlib.md5(data).hexdigest(); ext = path.rsplit('.', 1)[1]
    return h, ext, data
files = {}
def costume(name, path, cx, cy):
    h, ext, data = asset(path); files[f'{h}.{ext}'] = data
    return {'assetId': h, 'name': name, 'md5ext': f'{h}.{ext}', 'dataFormat': ext, 'rotationCenterX': cx, 'rotationCenterY': cy}
def sound(name, path):
    h, ext, data = asset(path); files[f'{h}.{ext}'] = data
    import wave
    with wave.open(path) as f: rate, n = f.getframerate(), f.getnframes()
    return {'assetId': h, 'name': name, 'dataFormat': 'wav', 'format': '', 'rate': rate, 'sampleCount': n, 'md5ext': f'{h}.{ext}'}

# ---------------- scène
S = Sprite()   # scène : fond, musique, message « perdu »
S.stack([S.flag(), S.backdrop('اللعب'), S.volume(25), S.forever([S.play('موسيقى الغابة', until=True)])], top=True, x=0, y=0)
S.stack([S.recv(), S.backdrop('خسرت'), S.play('صوت الخسارة', until=True)], top=True, x=0, y=400)

# ---------------- القرد (singe)
M = Sprite()
M.stack([M.flag(), M.goto(0, -106), M.show(),
         M.until(M.touching('البرتقالة'), [
             M.if_(M.key('left arrow'), [M.chx(-10)]),
             M.if_(M.key('right arrow'), [M.chx(10)])]),
         M.send()], top=True)

# ---------------- البرتقالة (orange)
def faller(sp, obj, tail):
    cond = sp.or_(sp.touchcolor(GROUND), sp.touching('القرد'))
    return [sp.goto((-200, 200), 170), sp.show(),
            sp.until(cond, [sp.point(180), sp.move(5)]),
            sp.if_(sp.touchcolor(GROUND), [sp.hide()]),
            sp.if_(sp.touching('القرد'), tail)]
Or = Sprite()
Or.stack([Or.flag(), Or.hide(), Or.forever(faller(Or, 'o', [Or.hide(), Or.send(wait=True), Or.stopall()]))], top=True)
# ---------------- الموزة (banane)
Ba = Sprite()
Ba.stack([Ba.flag(), Ba.setvar(0), Ba.hide(), Ba.forever(faller(Ba, 'b', [Ba.hide(), Ba.chgvar(1), Ba.play('صوت الموزة')]))], top=True)

def target(name, sp, costumes, sounds, x, y, layer, rot="don't rotate"):
    return {'isStage': False, 'name': name, 'variables': {}, 'lists': {}, 'broadcasts': {}, 'blocks': sp.b, 'comments': {}, 'currentCostume': 0,
            'costumes': costumes, 'sounds': sounds, 'volume': 100, 'layerOrder': layer, 'visible': name == 'القرد', 'x': x, 'y': y, 'size': 100, 'direction': 90, 'draggable': False, 'rotationStyle': rot}
stage = {'isStage': True, 'name': 'Stage', 'variables': {VAR_ID: [VAR, 0]}, 'lists': {}, 'broadcasts': {MSG_ID: MSG}, 'blocks': S.b, 'comments': {}, 'currentCostume': 0,
         'costumes': [costume('اللعب', f'{R}/decor-jeu.svg', 240, 180), costume('خسرت', f'{R}/decor-perdu.svg', 240, 180)],
         'sounds': [sound('موسيقى الغابة', f'{R}/musique-jungle.wav'), sound('صوت الموزة', f'{R}/son-banane.wav'), sound('صوت الخسارة', f'{R}/son-perdu.wav')],
         'volume': 100, 'layerOrder': 0, 'tempo': 60, 'videoTransparency': 50, 'videoState': 'on', 'textToSpeechLanguage': None}
# la banane joue « صوت الموزة » : le son appartient au lutin banane
banana_sounds = [sound('صوت الموزة', f'{R}/son-banane.wav')]
proj = {'targets': [stage,
        target('القرد', M, [costume('قرد', f'{R}/singe.svg', 32, 52)], [], 0, -106, 1),
        target('البرتقالة', Or, [costume('برتقالة', f'{R}/orange.svg', 18, 20)], [], 0, 170, 2),
        target('الموزة', Ba, [costume('موزة', f'{R}/banane.svg', 26, 23)], banana_sounds, 0, 170, 3)],
        'monitors': [{'id': VAR_ID, 'mode': 'default', 'opcode': 'data_variable', 'params': {'VARIABLE': VAR}, 'spriteName': None, 'value': 0, 'width': 0, 'height': 0, 'x': 5, 'y': 5, 'visible': True, 'sliderMin': 0, 'sliderMax': 100, 'isDiscrete': True}],
        'extensions': [], 'meta': {'semver': '3.0.0', 'vm': '0.2.0', 'agent': 'Mozilla/5.0'}}
# le son de la banane n'est plus dans la scène (mais le fichier reste dans l'archive via le lutin)
stage['sounds'] = [s for s in stage['sounds'] if s['name'] != 'صوت الموزة']
out = 'jeu_singe.sb3'
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('project.json', json.dumps(proj, ensure_ascii=False))
    for k, v in files.items(): z.writestr(k, v)
print(out, os.path.getsize(out), len(files), 'blocs:', {t['name']: len(t['blocks']) for t in proj['targets']})
