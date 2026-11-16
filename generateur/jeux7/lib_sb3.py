import json, hashlib, zipfile, os, wave
class Sprite:
    def __init__(self, MSG, MSG_ID, VAR, VAR_ID): self.b = {}; self.n = 0; self.MSG, self.MSG_ID, self.VAR, self.VAR_ID = MSG, MSG_ID, VAR, VAR_ID
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
    def recv(self): return self.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': [self.MSG, self.MSG_ID]})
    def send(self, wait=False): return self.add('event_broadcastandwait' if wait else 'event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, self.MSG, self.MSG_ID]]})
    def setvar(self, v): return self.add('data_setvariableto', {'VALUE': self.num(v)}, {'VARIABLE': [self.VAR, self.VAR_ID]})
    def chgvar(self, v): return self.add('data_changevariableby', {'VALUE': self.num(v)}, {'VARIABLE': [self.VAR, self.VAR_ID]})
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

    # --- ajouts (clones, tourner, rebondir, attendre, dire)
    def clone_start(self): return self.add('control_start_as_clone')
    def clone_make(self):
        m = self.add('control_create_clone_of_menu', fields={'CLONE_OPTION': ['_myself_', None]}, shadow=True)
        i = self.add('control_create_clone_of', {'CLONE_OPTION': [1, m]}); self.b[m]['parent'] = i; return i
    def clone_del(self): return self.add('control_delete_this_clone')
    def goto_random(self):
        m = self.add('motion_goto_menu', fields={'TO': ['_random_', None]}, shadow=True)
        i = self.add('motion_goto', {'TO': [1, m]}); self.b[m]['parent'] = i; return i
    def turnl(self, d): return self.add('motion_turnleft', {'DEGREES': self.num(d)})
    def turnr(self, d): return self.add('motion_turnright', {'DEGREES': self.num(d)})
    def bounce(self): return self.add('motion_ifonedgebounce')
    def rotstyle(self, s): return self.add('motion_setrotationstyle', fields={'STYLE': [s, None]})
    def chy(self, v): return self.add('motion_changeyby', {'DY': self.num(v)})
    def nextcostume(self): return self.add('looks_nextcostume')
    def wait(self, s): return self.add('control_wait', {'DURATION': self.num(s)})
    def repeat(self, n, body):
        i = self.c('control_repeat', None, body); self.b[i]['inputs']['TIMES'] = self.num(n); return i
    def say(self, text, secs):
        return self.add('looks_sayforsecs', {'MESSAGE': [1, [10, text]], 'SECS': self.num(secs)})
    def thisclicked(self): return self.add('event_whenthisspriteclicked')
    def var_eq(self, n):
        v = self.add('data_variable', fields={'VARIABLE': [self.VAR, self.VAR_ID]})
        i = self.add('operator_equals', {'OPERAND1': [3, v, [10, '']], 'OPERAND2': [1, [10, str(n)]]}); self.b[v]['parent'] = i; return i
    def wait_until(self, cond):
        i = self.add('control_wait_until', {'CONDITION': [2, cond]}); self.b[cond]['parent'] = i; return i

def asset(path):
    data = open(path, 'rb').read(); h = hashlib.md5(data).hexdigest(); ext = path.rsplit('.', 1)[1]
    return h, ext, data
files = {}
def costume(name, path, cx, cy):
    h, ext, data = asset(path); files[f'{h}.{ext}'] = data
    return {'assetId': h, 'name': name, 'md5ext': f'{h}.{ext}', 'dataFormat': ext, 'rotationCenterX': cx, 'rotationCenterY': cy}
def sound(name, path):
    h, ext, data = asset(path); files[f'{h}.{ext}'] = data
    with wave.open(path) as f: rate, n = f.getframerate(), f.getnframes()
    return {'assetId': h, 'name': name, 'dataFormat': 'wav', 'format': '', 'rate': rate, 'sampleCount': n, 'md5ext': f'{h}.{ext}'}

