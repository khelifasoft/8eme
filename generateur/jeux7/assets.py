# Génère les ressources du jeu « Le singe et les bananes » : décors, lutins, sons.
import math, wave, struct, os, random
O = 'res'; os.makedirs(O, exist_ok=True)
ST = '#333333'
def w(name, s): open(f'{O}/{name}', 'w', encoding='utf-8').write(s)

# ---- décor de jeu (480x360) : ciel, collines, sol brun (couleur utilisée par « touche la couleur »)
GROUND = '#633f00'
w('decor-jeu.svg', f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360"><defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fe9ff"/><stop offset="1" stop-color="#c9f6ff"/></linearGradient></defs><rect width="480" height="360" fill="url(#sk)"/><g fill="#fff" stroke="{ST}" stroke-width="2.5"><path d="M50 78 q-18 0 -18 -14 q0 -14 18 -14 q6 -16 26 -12 q14 -10 30 2 q20 -2 20 14 q0 16 -20 16Z"/><path d="M330 118 q-14 0 -14 -11 q0 -11 14 -11 q5 -12 20 -9 q11 -8 24 1 q16 -1 16 11 q0 12 -16 12Z"/></g><path d="M0 330 L0 292 Q20 270 50 276 Q80 238 140 240 Q200 238 220 276 Q260 252 320 262 Q350 270 360 280 Q400 262 440 276 Q462 280 480 296 L480 338 L0 338Z" fill="#00cc50" stroke="{ST}" stroke-width="3" stroke-linejoin="round"/><path d="M70 300 q10 -14 22 0 M300 308 q12 -16 26 0 M410 296 q8 -12 18 0" fill="none" stroke="#009a3c" stroke-width="4" stroke-linecap="round"/><rect x="0" y="338" width="480" height="22" fill="{GROUND}"/><line x1="0" y1="338" x2="480" y2="338" stroke="{ST}" stroke-width="2"/></svg>''')

# ---- décor « perdu » : tunnel sombre et mot « perdu »
rects = ''.join(f'<rect x="{x}" y="{y}" width="{480-2*x}" height="{360-2*y}" fill="none" stroke="#c46bff" stroke-opacity="{o}" stroke-width="3"/>' for x, y, o in [(30, 22, .35), (62, 46, .5), (92, 68, .65), (118, 88, .85), (150, 112, 1)])
w('decor-perdu.svg', f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360"><rect width="480" height="360" fill="#0b6aa8"/><g stroke="#073e66" stroke-width="3"><line x1="0" y1="0" x2="180" y2="112"/><line x1="480" y1="0" x2="300" y2="112"/><line x1="0" y1="360" x2="180" y2="248"/><line x1="480" y1="360" x2="300" y2="248"/><line x1="0" y1="120" x2="150" y2="150"/><line x1="480" y1="120" x2="330" y2="150"/><line x1="0" y1="240" x2="150" y2="210"/><line x1="480" y1="240" x2="330" y2="210"/><line x1="160" y1="0" x2="200" y2="112"/><line x1="320" y1="0" x2="280" y2="112"/><line x1="160" y1="360" x2="200" y2="248"/><line x1="320" y1="360" x2="280" y2="248"/></g>{rects}<rect x="178" y="130" width="124" height="100" fill="#06151f" stroke="#e7b3ff" stroke-width="3"/><text x="240" y="188" text-anchor="middle" font-family="Tajawal,Arial,sans-serif" font-size="34" font-weight="bold" fill="#fff">perdu</text><text x="240" y="216" text-anchor="middle" font-family="Tajawal,Arial,sans-serif" font-size="20" fill="#ffe07a">خسرت</text></svg>''')

# ---- singe (60x100)
w('singe.svg', f'''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="104" viewBox="0 0 64 104"><path d="M46 84 Q62 84 60 66 Q58 56 52 60" fill="none" stroke="{ST}" stroke-width="9" stroke-linecap="round"/><path d="M46 84 Q62 84 60 66 Q58 56 52 60" fill="none" stroke="#c47a2c" stroke-width="5" stroke-linecap="round"/><g stroke="{ST}" stroke-width="3" stroke-linejoin="round"><rect x="20" y="86" width="10" height="14" rx="5" fill="#c47a2c"/><rect x="34" y="86" width="10" height="14" rx="5" fill="#c47a2c"/><ellipse cx="32" cy="72" rx="17" ry="18" fill="#c47a2c"/><ellipse cx="32" cy="76" rx="10" ry="12" fill="#f3d5a0" stroke="none"/><ellipse cx="14" cy="70" rx="6" ry="13" fill="#c47a2c" transform="rotate(14 14 70)"/><ellipse cx="50" cy="70" rx="6" ry="13" fill="#c47a2c" transform="rotate(-14 50 70)"/><circle cx="8" cy="30" r="9" fill="#c47a2c"/><circle cx="56" cy="30" r="9" fill="#c47a2c"/><circle cx="8" cy="30" r="4.5" fill="#f3d5a0" stroke="none"/><circle cx="56" cy="30" r="4.5" fill="#f3d5a0" stroke="none"/><ellipse cx="32" cy="34" rx="22" ry="24" fill="#c47a2c"/><ellipse cx="32" cy="42" rx="16" ry="14" fill="#f3d5a0"/></g><g fill="#fff" stroke="{ST}" stroke-width="2"><circle cx="24" cy="32" r="6"/><circle cx="40" cy="32" r="6"/></g><circle cx="25" cy="33" r="2.6" fill="{ST}"/><circle cx="39" cy="33" r="2.6" fill="{ST}"/><ellipse cx="32" cy="42" rx="3" ry="2" fill="{ST}"/><path d="M24 49 Q32 56 40 49" fill="none" stroke="{ST}" stroke-width="2.5" stroke-linecap="round"/></svg>''')

# ---- banane (52x46)
w('banane.svg', f'''<svg xmlns="http://www.w3.org/2000/svg" width="52" height="46" viewBox="0 0 52 46"><path d="M8 10 Q4 34 26 40 Q40 42 48 30 Q40 34 30 30 Q16 24 16 8Z" fill="#ffd93b" stroke="{ST}" stroke-width="3" stroke-linejoin="round"/><path d="M14 12 Q14 28 28 34" fill="none" stroke="#e5a900" stroke-width="2.5" stroke-linecap="round"/><path d="M8 10 Q9 4 13 3 L17 8" fill="#7a5a1a" stroke="{ST}" stroke-width="2.5" stroke-linejoin="round"/><circle cx="47" cy="30" r="2.6" fill="#7a5a1a" stroke="{ST}" stroke-width="1.5"/></svg>''')

# ---- orange (34x38)
w('orange.svg', f'''<svg xmlns="http://www.w3.org/2000/svg" width="36" height="40" viewBox="0 0 36 40"><circle cx="18" cy="23" r="15" fill="#ff8a1c" stroke="{ST}" stroke-width="3"/><path d="M10 17 Q12 12 17 11" fill="none" stroke="#ffc680" stroke-width="3" stroke-linecap="round"/><path d="M18 8 Q22 0 30 3 Q26 11 18 9Z" fill="#43a047" stroke="{ST}" stroke-width="2.5" stroke-linejoin="round"/><line x1="18" y1="8" x2="18" y2="12" stroke="{ST}" stroke-width="2.5" stroke-linecap="round"/></svg>''')

# ---- sons (WAV 22,05 kHz mono)
SR = 22050
def wav(name, samples):
    with wave.open(f'{O}/{name}', 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes(b''.join(struct.pack('<h', max(-32767, min(32767, int(s * 32767)))) for s in samples))
def tone(freq, dur, vol=.5, kind='sine', decay=3.0):
    n = int(SR * dur); out = []
    for i in range(n):
        t = i / SR; env = min(1, i / 200) * math.exp(-decay * t / dur)
        if kind == 'sine': v = math.sin(2 * math.pi * freq * t)
        elif kind == 'tri': v = 2 / math.pi * math.asin(math.sin(2 * math.pi * freq * t))
        else: v = math.sin(2 * math.pi * freq * t) + .4 * math.sin(4 * math.pi * freq * t)
        out.append(v * env * vol)
    return out
def mix(a, b):
    n = max(len(a), len(b)); a = a + [0] * (n - len(a)); b = b + [0] * (n - len(b)); return [x + y for x, y in zip(a, b)]
# musique « jungle » : mélodie pentatonique joyeuse + basse, ~19 s, boucle
N = {'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'G4': 392.0, 'A4': 440.0, 'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'G5': 783.99, 'A3': 220.0, 'G3': 196.0, 'C3': 130.81, 'F3': 174.61}
mel = ['E4', 'G4', 'A4', 'G4', 'E4', 'D4', 'C4', 'D4', 'E4', 'G4', 'C5', 'A4', 'G4', 'E4', 'D4', 'E4',
       'G4', 'A4', 'C5', 'D5', 'E5', 'D5', 'C5', 'A4', 'G4', 'E4', 'G4', 'A4', 'G4', 'E4', 'D4', 'C4'] * 2
bass = ['C3', 'C3', 'F3', 'G3'] * 4
beat = .3; total = int(SR * beat * len(mel)); song = [0.0] * total
def put(buf, start, snd):
    for i, v in enumerate(snd):
        if start + i < len(buf): buf[start + i] += v
for i, n in enumerate(mel): put(song, int(i * beat * SR), tone(N[n], beat * .95, .32, 'tri', 2.2))
for i, n in enumerate(bass * 2 if len(bass) * 4 * beat * 4 < len(mel) * beat else bass): put(song, int(i * beat * 4 * SR), tone(N[n], beat * 3.6, .22, 'sine', 1.6))
for i in range(len(mel)):   # petite percussion (bruit filtré) sur chaque temps
    rnd = random.Random(i); put(song, int(i * beat * SR), [(rnd.random() * 2 - 1) * .06 * math.exp(-40 * k / SR) for k in range(int(SR * .05))])
wav('musique-jungle.wav', song)
wav('son-banane.wav', mix(tone(784, .12, .5, 'sine', 2), [0] * int(SR * .08) + tone(1175, .22, .5, 'sine', 3)))
wav('son-perdu.wav', tone(392, .22, .55, 'saw', 2) + tone(330, .22, .55, 'saw', 2) + tone(262, .22, .55, 'saw', 2) + tone(196, .6, .55, 'saw', 4))
print(sorted(os.listdir(O)))
