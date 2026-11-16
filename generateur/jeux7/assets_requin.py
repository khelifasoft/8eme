import math, os, random, struct, wave
O = 'res_r'; os.makedirs(O, exist_ok=True)
ST = '#333333'
def w(n, s): open(f'{O}/{n}', 'w', encoding='utf-8').write(s)
def sea(menu):
    top, bot = ('#1a6fa8', '#06304f') if menu else ('#8fdcff', '#1a7fcf')
    rnd = random.Random(7)
    bub = ''.join(f'<circle cx="{rnd.randint(20, 460)}" cy="{rnd.randint(20, 280)}" r="{rnd.randint(3, 9)}" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="2"/>' for _ in range(14))
    weed = ''.join(f'<path d="M{x} 330 q-14 -30 0 -55 q14 -26 0 -52" fill="none" stroke="{c}" stroke-width="9" stroke-linecap="round"/>' for x, c in [(30, '#2e9a4a'), (58, '#39b45a'), (420, '#2e9a4a'), (448, '#39b45a'), (250, '#2e9a4a')])
    coral = '<g stroke="#333" stroke-width="2.5" stroke-linejoin="round"><path d="M340 336 q-6 -50 10 -56 q6 20 14 4 q2 -30 18 -34 q4 30 -2 86Z" fill="#ff7aa8"/><path d="M110 336 q0 -36 14 -40 q10 12 16 -4 q10 20 6 44Z" fill="#ff9f43"/><ellipse cx="190" cy="338" rx="34" ry="14" fill="#8a8fa8"/></g>'
    rays = '' if menu else ''.join(f'<polygon points="{x},0 {x + 40},0 {x + 10},300 {x - 30},300" fill="#fff" fill-opacity=".10"/>' for x in (80, 220, 360))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360"><defs><linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bot}"/></linearGradient></defs>'
            f'<rect width="480" height="360" fill="url(#sea)"/>{rays}{bub}{weed}<path d="M0 322 Q120 306 240 320 T480 316 L480 360 L0 360Z" fill="#e8d29a" stroke="{ST}" stroke-width="2.5"/>{coral}')
w('decor-mer.svg', sea(False) + '</svg>')
w('decor-menu.svg', sea(True) + f'<text x="240" y="92" text-anchor="middle" font-family="Tajawal,Arial Black,Arial,sans-serif" font-size="46" font-weight="900" font-style="italic" fill="#ff3d8b" stroke="#fff" stroke-width="2" paint-order="stroke">JEU DU REQUIN</text><text x="240" y="126" text-anchor="middle" font-family="Tajawal,Arial,sans-serif" font-size="24" font-weight="bold" fill="#ffe07a">لعبة القرش</text></svg>')
def shark(open_mouth, tail_up):
    ty = -10 if tail_up else 10
    mouth = (f'<path d="M92 40 Q116 52 140 40 Q124 66 100 60Z" fill="#7a1230" stroke="{ST}" stroke-width="2.5" stroke-linejoin="round"/><path d="M100 41 l6 8 l6 -7 l6 8 l6 -7 l6 7" fill="#fff" stroke="{ST}" stroke-width="1.5" stroke-linejoin="round"/>' if open_mouth
             else f'<path d="M94 46 Q118 56 140 46" fill="none" stroke="{ST}" stroke-width="3" stroke-linecap="round"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="160" height="90" viewBox="0 0 160 90"><g stroke="{ST}" stroke-width="3" stroke-linejoin="round">'
            f'<path d="M30 46 L6 {46 + ty - 18} Q16 46 10 {46 + ty + 26}Z" fill="#3b78c0"/><path d="M58 22 Q70 0 88 22Z" fill="#3b78c0"/>'
            f'<path d="M26 46 Q40 18 90 20 Q132 20 152 46 Q132 72 92 70 Q44 72 26 46Z" fill="#4a90d9"/><path d="M52 58 Q92 76 148 50 Q130 70 92 70 Q60 70 52 58Z" fill="#eaf5ff" stroke="none"/>'
            f'<path d="M80 62 Q92 82 70 80Z" fill="#3b78c0"/></g>{mouth}<circle cx="122" cy="34" r="6" fill="#fff" stroke="{ST}" stroke-width="2"/><circle cx="124" cy="34" r="3" fill="{ST}"/><path d="M100 30 q6 6 0 14 M108 30 q6 6 0 14" fill="none" stroke="#2f5f98" stroke-width="2" stroke-linecap="round"/></svg>')
w('requin-1.svg', shark(False, True)); w('requin-2.svg', shark(True, False))
def fish(tail_up):
    ty = -6 if tail_up else 6
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="64" height="44" viewBox="0 0 64 44"><g stroke="{ST}" stroke-width="2.5" stroke-linejoin="round"><path d="M16 22 L3 {22 + ty - 12} Q8 22 3 {22 + ty + 14}Z" fill="#ff9f1c"/><path d="M22 10 Q34 -2 46 10Z" fill="#ff9f1c"/>'
            f'<path d="M12 22 Q26 2 46 8 Q62 14 62 22 Q62 30 46 36 Q26 42 12 22Z" fill="#ffd93b"/></g><path d="M30 8 Q36 22 30 38 M40 8 Q46 22 40 36" fill="none" stroke="{ST}" stroke-width="3" stroke-linecap="round"/><circle cx="52" cy="19" r="4.2" fill="#fff" stroke="{ST}" stroke-width="2"/><circle cx="53" cy="19" r="2" fill="{ST}"/></svg>')
w('poisson-1.svg', fish(True)); w('poisson-2.svg', fish(False))
w('bouton-commencer.svg', f'<svg xmlns="http://www.w3.org/2000/svg" width="170" height="54" viewBox="0 0 170 54"><rect x="3" y="3" width="164" height="48" rx="24" fill="#ff8a1c" stroke="#d9480f" stroke-width="4"/><text x="85" y="24" text-anchor="middle" font-family="Tajawal,Arial,sans-serif" font-size="19" font-weight="bold" fill="#fff" stroke="#8a3a00" stroke-width=".8">Commencer</text><text x="85" y="44" text-anchor="middle" font-family="Tajawal,Arial,sans-serif" font-size="14" font-weight="bold" fill="#fff6c8">ابدأ</text></svg>')
SR = 22050
def wav(n, s):
    with wave.open(f'{O}/{n}', 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes(b''.join(struct.pack('<h', max(-32767, min(32767, int(x * 32767)))) for x in s))
def tone(fr, d, v=.4, dec=3, f2=None):
    n = int(SR * d); out = []; ph = 0
    for i in range(n):
        f = fr if f2 is None else fr + (f2 - fr) * i / n; ph += 2 * math.pi * f / SR
        out.append(math.sin(ph) * min(1, i / 150) * math.exp(-dec * i / n) * v)
    return out
def put(buf, st, snd):
    for i, x in enumerate(snd):
        if st + i < len(buf): buf[st + i] += x
# musique de la mer : arpèges doux + bulles
notes = [261.63, 329.63, 392.0, 523.25, 392.0, 329.63, 293.66, 349.23, 440.0, 587.33, 440.0, 349.23] * 3
beat = .42; song = [0.0] * int(SR * beat * len(notes))
for i, f in enumerate(notes): put(song, int(i * beat * SR), tone(f, beat * 1.5, .28, 2.5))
for i in range(0, len(notes), 3): put(song, int(i * beat * SR), tone(130.81 if (i // 3) % 2 == 0 else 146.83, beat * 3, .22, 1.2))
rnd = random.Random(3)
for i in range(18): put(song, int(rnd.random() * len(song) * .95), tone(rnd.choice([700, 900, 1100]), .08, .12, 4, f2=1500))
wav('musique-mer.wav', song)
wav('son-glouglou.wav', tone(300, .12, .5, 3, 700) + tone(250, .12, .5, 3, 600) + tone(400, .16, .5, 4, 900))
wav('son-victoire.wav', tone(523, .15, .45, 2) + tone(659, .15, .45, 2) + tone(784, .15, .45, 2) + tone(1047, .5, .45, 3))
print(sorted(os.listdir(O)))
