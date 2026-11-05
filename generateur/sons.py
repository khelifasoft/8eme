"""Synthèse des effets sonores et des musiques (numpy, sans fichiers externes)."""
import numpy as np, wave, math
SR = 22050
rng = np.random.default_rng(7)

def A(*xs):
    n = max(len(x) for x in xs); out = np.zeros(n)
    for x in xs: out[:len(x)] += x
    return out
def tt(d): return np.arange(int(SR * d)) / SR
def env_ar(n, a=0.01, r=0.1):
    e = np.ones(n); na, nr = int(a * SR), int(r * SR)
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e
def osc(f, d, kind="sine"):
    t = tt(d); f = np.broadcast_to(np.asarray(f, float), t.shape) if np.ndim(f) == 0 else np.interp(np.linspace(0, 1, len(t)), np.linspace(0, 1, len(f)), f)
    ph = 2 * np.pi * np.cumsum(f) / SR
    if kind == "sine": return np.sin(ph)
    if kind == "square": return np.sign(np.sin(ph))
    if kind == "saw": return 2 * ((ph / (2 * np.pi)) % 1) - 1
    if kind == "tri": return 2 * np.abs(2 * ((ph / (2 * np.pi)) % 1) - 1) - 1
def noise(d): return rng.uniform(-1, 1, int(SR * d))
def lp(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[f > fc] = 0; return np.fft.irfft(X, len(x))
def hp(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[f < fc] = 0; return np.fft.irfft(X, len(x))
def bp(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def decay(d, k=5): return np.exp(-k * tt(d) / d)
def note(f, d, kind="sine", vol=.5, k=4, a=0.005):
    return osc(f, d, kind) * decay(d, k) * env_ar(int(SR * d), a, 0.02) * vol
def place(total, parts):
    out = np.zeros(int(SR * total))
    for t0, x in parts:
        i = int(SR * t0); out[i:i + len(x)] += x[:max(0, len(out) - i)]
    return out
def seq(freqs, step, d, kind="sine", vol=.5, k=4):
    return place(step * len(freqs) + d, [(i * step, note(f, d, kind, vol, k)) for i, f in enumerate(freqs)])
def save(path, x):
    x = np.asarray(x, float); m = np.max(np.abs(x)) or 1
    x = x / m * 0.85
    n = int(0.01 * SR); x[:n] *= np.linspace(0, 1, n); x[-n:] *= np.linspace(1, 0, n)
    w = wave.open(path, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 32767).astype("<i2").tobytes()); w.close()
    return len(x) / SR

NOTES = {n: 440 * 2 ** ((i - 9) / 12) for i, n in enumerate(["C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4"])}
def nf(name):
    base = name[:-1]; octv = int(name[-1])
    return NOTES[base + "4"] * 2 ** (octv - 4)

# ---------------- effets ----------------
def e_ding(): return A(note(1318, 1.2, "sine", .6, 5), note(2636, 1.2, "sine", .2, 6))
def e_cloche(): return sum(note(392 * m, 2.6, "sine", .5 / (i + 1), 2.2) for i, m in enumerate([1, 1.5, 2.76, 4.1]))
def e_gong(): return sum(note(110 * m, 3.2, "sine", .4 / (i + 1), 1.4) for i, m in enumerate([1, 1.59, 2.14, 2.3, 2.9]))
def e_toctoc(): return place(1.4, [(i * .3, A(lp(noise(.1), 900) * decay(.1, 40), note(170, .12, "sine", .8, 30))) for i in range(3)])
def e_grincement(): return lp(osc(np.concatenate([np.linspace(300, 220, 100), np.linspace(220, 330, 100), np.linspace(330, 250, 100)]) , 1.6, "saw") * (1 + .3 * osc(18, 1.6)) * env_ar(int(1.6 * SR), .1, .2), 2500) * .5
def e_pas(): return place(3, [(i * .4, lp(noise(.09), 700) * decay(.09, 25) * (1 if i % 2 else .8)) for i in range(7)])
def e_course(): return place(2.6, [(i * .17, lp(noise(.06), 900) * decay(.06, 25) * (1 if i % 2 else .85)) for i in range(15)])
def e_vent(): n = lp(noise(3.5), 900) * (0.6 + .4 * osc(.7, 3.5)); return n * env_ar(len(n), .6, .8)
def e_pluie(): n = hp(noise(3.5), 3000) * .6 + hp(noise(3.5), 1000) * .2; return n * env_ar(len(n), .3, .6)
def e_tonnerre(): n = lp(noise(2.6), 220) * decay(2.6, 2.2) * 2; return n * env_ar(len(n), .08, .3)
def e_eau():
    parts = []
    for i in range(22):
        f0 = rng.uniform(400, 900); parts.append((rng.uniform(0, 1.8), note(np.linspace(f0, f0 * 1.8, int(.08 * SR)), .08, "sine", .4, 6)))
    return place(2, parts)
def e_vagues(): n = lp(noise(4.4), 700) * (0.5 + .5 * osc(.45, 4.4)) ; return n * env_ar(len(n), .5, .6)
def e_feu():
    n = lp(noise(3.2), 400) * .4
    for _ in range(40): i = rng.integers(0, len(n) - 400); n[i:i + 200] += hp(noise(200 / SR), 2000) * decay(200 / SR, 20) * rng.uniform(.3, 1)
    return n
def e_magie(): return seq([nf(x) for x in ["C6", "E6", "G6", "C7", "E7", "G7", "C7"]], .09, .7, "sine", .4, 5)
def e_baguette(): return A(note(np.linspace(400, 2400, SR), 1.0, "sine", .5, 1.5), .2 * seq([nf("C7"), nf("E7"), nf("G7")], .15, .3, "sine", .5, 6))
def e_fanfare(): return lp(seq([nf("C5"), nf("C5"), nf("E5"), nf("G5"), nf("C6")], .17, .4, "square", .4, 2.5), 3000)
def e_victoire(): return seq([nf(x) for x in ["C5", "E5", "G5", "C6", "G5", "C6"]], .13, .35, "tri", .5, 3)
def e_echec(): return lp(seq([nf("G4"), nf("F#4"), nf("F4"), nf("E4")], .3, .5, "saw", .4, 2.5), 1500)
def e_tambour():
    parts = []; t0 = 0; gap = .16
    while t0 < 2:
        parts.append((t0, A(lp(noise(.1), 400) * decay(.1, 18), note(110, .15, "sine", .8, 15)))); t0 += gap; gap *= .93
    parts.append((t0 + .1, A(lp(noise(.5), 300) * decay(.5, 8) * 1.5, note(70, .5, "sine", 1, 6))))
    return place(3, parts)
def e_tictac(): return place(3.2, [(i * .5, (hp(noise(.03), 2500) * decay(.03, 30) if i % 2 == 0 else lp(noise(.04), 1500) * decay(.04, 30)) * 1.2) for i in range(6)])
def e_minuit(): return place(8, [(i * .62, note(392 * 0.5, 1.4, "sine", .6, 3) + note(392 * 0.5 * 2.76, 1.4, "sine", .2, 4)) for i in range(12)])
def e_pop(): return A(note(np.linspace(900, 200, 2000), .12, "sine", .8, 10), lp(noise(.12), 3000) * decay(.12, 30) * .3)
def e_boing(): return note(np.concatenate([np.linspace(180, 700, 3000), np.linspace(700, 250, 5000)]) * (1 + .05 * osc(25, 8000 / SR)), 8000 / SR, "sine", .8, 3)
def e_whoosh(): n = bp(noise(.9), 300, 4000); return n * np.sin(np.linspace(0, np.pi, len(n))) ** 1.5
def e_piece(): return place(.8, [(0, note(nf("B5"), .08, "square", .3, 8)), (.08, note(nf("E6"), .7, "square", .3, 6))])
def e_alarme(): return seq([880, 660] * 4, .15, .15, "square", .3, 1)
def e_coeur(): return place(3, [(t, note(np.linspace(80, 50, 3000), .15, "sine", 1, 12)) for t in (0, .22, .9, 1.12, 1.8, 2.02)])
def e_oiseau(): return place(1.4, [(i * .18, note(np.linspace(3000, 4600, 1500), .07, "sine", .5, 3) + note(np.linspace(4600, 3200, 1500), .07, "sine", .4, 3)) for i in range(5)])
def e_grenouille(): return place(1.2, [(t, osc(130, .25, "square") * (0.6 + .4 * osc(35, .25)) * env_ar(int(.25 * SR), .01, .1) * .5) for t in (0, .35)])
def e_loup(): f = np.concatenate([np.linspace(300, 750, 12000), np.linspace(750, 520, 18000)]) * (1 + .015 * osc(6, 30000 / SR)); return lp(note(f, 30000 / SR, "saw", .5, .8, .15), 3000)
def e_rugissement(): return lp((noise(1.8) * .4 + osc(np.linspace(110, 70, int(1.8 * SR)), 1.8, "saw") * .6) * (1 + .6 * osc(28, 1.8)) * env_ar(int(1.8 * SR), .08, .5), 900)
def e_ane(): return lp(place(2.6, [(0, osc(np.linspace(500, 380, 9000), .4, "saw") * env_ar(int(.4 * SR), .02, .05)), (.45, osc(np.linspace(200, 380, 8000), .36, "saw") * env_ar(int(.36 * SR), .02, .05)), (.9, osc(np.linspace(520, 400, 9000), .4, "saw") * env_ar(int(.4 * SR), .02, .05)), (1.4, osc(np.linspace(220, 360, 8000), .36, "saw") * env_ar(int(.36 * SR), .02, .05))]) * .5, 2500)
def e_souris(): return place(.8, [(0, note(np.linspace(2500, 3600, 2000), .1, "sine", .5, 3)), (.17, note(np.linspace(2700, 3800, 2000), .1, "sine", .5, 3))])
def e_corbeau(): return lp(place(1.4, [(i * .4, (osc(380, .22, "saw") + .6 * noise(.22)) * env_ar(int(.22 * SR), .01, .08) * .5) for i in range(3)]), 2200)
def e_rire(): return lp(place(1.6, [(i * .3, osc(np.linspace(240, 190, 4000), .22, "saw") * env_ar(int(.22 * SR), .01, .06) * (1 - i * .1)) for i in range(5)]), 1200)
def e_applaudissements():
    n = np.zeros(int(3.2 * SR))
    for _ in range(150): i = rng.integers(0, len(n) - 800); n[i:i + 600] += hp(noise(600 / SR), 1500) * decay(600 / SR, 15) * rng.uniform(.3, 1)
    return n * env_ar(len(n), .3, .6)
def e_chute(): return A(note(np.linspace(1500, 200, SR), 1.0, "sine", .6, .5), place(1.4, [(1.0, lp(noise(.3), 300) * decay(.3, 10) * 1.2)]))
def e_ronflement(): m = (0.3 + .7 * np.clip(osc(.8, 3.2), 0, 1)); return lp(osc(70, 3.2, "saw"), 600) * m + lp(noise(3.2), 500) * .2 * m
def e_boum(): return A(note(np.linspace(100, 30, 8000), 1.0, "sine", 1, 4), lp(noise(1), 200) * decay(1, 6))
def e_claque(): return A(lp(noise(.4), 900) * decay(.4, 14) * 1.3, note(100, .4, "sine", .8, 10))
def e_coffre(): return np.concatenate([e_grincement()[:int(1.0 * SR)] * .6, e_magie()])
def e_hache(): return place(1.4, [(i * .45, A(hp(noise(.05), 800) * decay(.05, 40), note(np.linspace(260, 120, 1500), .15, "sine", .9, 15))) for i in range(3)])
def e_cles(): return place(1.2, [(rng.uniform(0, .9), note(rng.uniform(3000, 6000), .15, "sine", .3, 12)) for _ in range(16)])
def e_plouf(): return A(lp(noise(.7), 2500) * np.exp(-6 * tt(.7)) * .8, note(np.linspace(600, 200, 5000), .3, "sine", .7, 8))
def e_galop(): return place(2.4, [(i * .3 + (.12 if i % 2 else 0), lp(noise(.06), 1500) * decay(.06, 30) * 1.2) for i in range(8)] + [(i * .3 + .06, lp(noise(.06), 1500) * decay(.06, 30)) for i in range(8)])
def e_sonnette(): return place(1.2, [(0, note(880, .4, "sine", .6, 4)), (.35, note(660, .7, "sine", .6, 4))])
def e_klaxon(): return osc(440, .5, "square") * .4 * env_ar(int(.5 * SR), .01, .05)
def e_etincelle(): return place(1.2, [(rng.uniform(0, 1), note(rng.uniform(4000, 7000), .06, "sine", .4, 10)) for _ in range(22)])
def e_pleurs(): return lp(osc(np.concatenate([np.linspace(500, 380, 4000), np.linspace(380, 500, 4000)] * 2), 1.4, "saw") * (1 + .3 * osc(6, 1.4)) * env_ar(int(1.4 * SR), .1, .3), 1500) * .5
def e_soupir(): return lp(noise(1.2), 1200) * np.sin(np.linspace(0, np.pi, int(1.2 * SR))) ** 2 * .6
def e_mouton(): return lp(place(2.4, [(0, osc(np.concatenate([np.linspace(330, 300, 3000), np.linspace(300, 340, 12000)]) * (1 + .04 * osc(30, 15000 / SR)), 15000 / SR, "saw") * env_ar(15000, .02, .1) * .5), (1.1, osc(np.linspace(320, 280, 12000) * (1 + .04 * osc(30, 12000 / SR)), 12000 / SR, "saw") * env_ar(12000, .02, .1) * .5)]), 2200)
def e_bulle(): return note(np.linspace(300, 1200, 3000), .15, "sine", .8, 6)

EFFETS = [
 ("ding", "جرس صغير", "Clochette", e_ding, []), ("cloche", "ناقوس", "Cloche", e_cloche, ["cinderella"]), ("gong", "قرع الطبل الكبير", "Gong", e_gong, []),
 ("toctoc", "طَرْق على الباب", "Toc toc", e_toctoc, ["layla", "alibaba"]), ("grincement_porte", "صرير الباب", "Porte qui grince", e_grincement, ["alibaba", "layla"]),
 ("pas", "خطوات", "Pas", e_pas, []), ("course", "ركض", "Course", e_course, ["hare"]), ("vent", "ريح", "Vent", e_vent, []), ("pluie", "مطر", "Pluie", e_pluie, []),
 ("tonnerre", "رعد", "Tonnerre", e_tonnerre, ["sindbad"]), ("eau", "ماء يجري", "Eau", e_eau, ["djeha"]), ("vagues", "أمواج البحر", "Vagues", e_vagues, ["sindbad"]),
 ("feu", "نار تشتعل", "Feu", e_feu, []), ("magie", "سحر", "Magie", e_magie, ["cinderella"]), ("baguette", "عصا سحرية", "Baguette magique", e_baguette, ["cinderella"]),
 ("fanfare", "نفير الاحتفال", "Fanfare", e_fanfare, ["cinderella", "frog"]), ("victoire", "فوز", "Victoire", e_victoire, ["hare"]), ("echec", "فشل", "Échec", e_echec, []),
 ("roulement_tambour", "قرع الطبول", "Roulement de tambour", e_tambour, ["hare"]), ("tic_tac", "تك تك الساعة", "Tic-tac", e_tictac, ["cinderella"]), ("minuit", "الساعة تدقّ الثانية عشرة", "Minuit", e_minuit, ["cinderella"]),
 ("pop", "فقاعة", "Pop", e_pop, []), ("boing", "نطّة", "Boing", e_boing, ["frog"]), ("whoosh", "هواء سريع", "Whoosh", e_whoosh, []), ("piece", "قطعة نقود", "Pièce", e_piece, ["alibaba"]),
 ("alarme", "إنذار", "Alarme", e_alarme, []), ("coeur", "نبض القلب", "Cœur", e_coeur, ["layla"]), ("oiseau", "عصفور يغرّد", "Oiseau", e_oiseau, []),
 ("grenouille", "نقيق الضفدع", "Grenouille", e_grenouille, ["frog"]), ("loup", "عواء الذئب", "Loup", e_loup, ["layla", "shepherd"]), ("rugissement", "زئير الأسد", "Rugissement", e_rugissement, ["lion"]),
 ("ane", "نهيق الحمار", "Âne", e_ane, ["djeha"]), ("souris", "صرير الفأر", "Souris", e_souris, ["lion"]), ("corbeau", "نعيق الغراب", "Corbeau", e_corbeau, ["crow"]),
 ("rire", "ضحك", "Rire", e_rire, ["djeha"]), ("applaudissements", "تصفيق", "Applaudissements", e_applaudissements, ["hare", "cinderella"]), ("chute", "سقوط", "Chute", e_chute, ["sindbad", "crow"]),
 ("ronflement", "شخير", "Ronflement", e_ronflement, ["hare", "lion"]), ("boum", "انفجار", "Boum", e_boum, []), ("claquement_porte", "باب يُغلَق بقوة", "Porte qui claque", e_claque, ["alibaba"]),
 ("coffre", "فتح صندوق الكنز", "Coffre", e_coffre, ["alibaba"]), ("hache", "ضرب بالفأس", "Hache", e_hache, ["layla"]), ("cles", "مفاتيح", "Clés", e_cles, []),
 ("plouf", "قفزة في الماء", "Plouf", e_plouf, ["frog", "sindbad"]), ("galop", "عَدْو الحصان", "Galop", e_galop, []), ("sonnette", "جرس الباب", "Sonnette", e_sonnette, []),
 ("klaxon", "منبّه", "Klaxon", e_klaxon, []), ("etincelles", "شرارات", "Étincelles", e_etincelle, ["cinderella"]), ("pleurs", "بكاء", "Pleurs", e_pleurs, ["cinderella"]),
 ("soupir", "تنهيدة", "Soupir", e_soupir, []), ("mouton", "ثغاء الخروف", "Mouton", e_mouton, ["shepherd"]), ("bulle", "فقاعة ماء", "Bulle", e_bulle, ["frog"]),
]

# ---------------- musiques ----------------
def musique(melody, bass, bpm, lead="tri", bassk="sine", vol=.35, loops=1):
    beat = 60 / bpm; total = max(sum(d for _, d in melody), sum(d for _, d in bass)) * beat
    out = np.zeros(int(SR * (total + 1.2)))
    t = 0
    for f, d in melody:
        if f: x = note(f, d * beat * 1.05, lead, vol, 3.5); i = int(SR * t); out[i:i + len(x)] += x
        t += d * beat
    t = 0
    for f, d in bass:
        if f: x = note(f, d * beat * 1.05, bassk, vol * .8, 2.5); i = int(SR * t); out[i:i + len(x)] += x
        t += d * beat
    return out
def m_joyeuse():
    C, D, E, F, G, A = nf("C5"), nf("D5"), nf("E5"), nf("F5"), nf("G5"), nf("A5")
    mel = [(C, 1), (E, 1), (G, 1), (E, 1), (C, 1), (E, 1), (G, 2), (A, 1), (G, 1), (F, 1), (E, 1), (D, 1), (E, 1), (C, 2), (G, 1), (G, 1), (E, 1), (C, 1), (D, 1), (F, 1), (E, 1), (D, 1), (C, 2)]
    bass = [(nf("C3"), 2), (nf("G3"), 2)] * 3 + [(nf("F3"), 2), (nf("G3"), 2)] + [(nf("C3"), 2), (nf("G3"), 2), (nf("C3"), 2)]
    return musique(mel, bass, 130)
def m_triste():
    A, B, C, D, E = nf("A4"), nf("B4"), nf("C5"), nf("D5"), nf("E5")
    mel = [(A, 2), (C, 2), (E, 3), (D, 1), (C, 2), (B, 2), (A, 4), (E, 2), (D, 2), (C, 3), (B, 1), (A, 4)]
    bass = [(nf("A3"), 4), (nf("F3"), 4), (nf("A3"), 4), (nf("E3"), 4)] * 1
    return musique(mel, bass, 66, "sine", "sine", .4)
def m_mystere():
    mel = [(nf("E4"), 3), (nf("G4"), 1), (nf("F#4"), 3), (None, 1), (nf("E4"), 2), (nf("B3"), 2), (nf("C4"), 4), (nf("B3"), 3), (None, 1), (nf("E4"), 2), (nf("D#4"), 2)]
    bass = [(nf("E2"), 4), (nf("B2"), 4), (nf("C3"), 4), (nf("B2"), 4)]
    return musique(mel, bass, 72, "tri", "saw", .3)
def m_aventure():
    mel = [(nf("E5"), 1), (nf("E5"), 1), (nf("G5"), 1), (nf("E5"), 1), (nf("A5"), 2), (nf("G5"), 2), (nf("E5"), 1), (nf("E5"), 1), (nf("G5"), 1), (nf("A5"), 1), (nf("B5"), 2), (nf("A5"), 2), (nf("G5"), 1), (nf("A5"), 1), (nf("B5"), 1), (nf("C6"), 1), (nf("B5"), 2), (nf("E5"), 2)]
    bass = [(nf("E3"), 1), (nf("B3"), 1)] * 12
    return musique(mel, bass, 140, "square", "tri", .25)
def m_mer():
    arp = [nf(x) for x in ["C4", "G4", "E5", "G4", "A3", "E4", "C5", "E4", "F3", "C4", "A4", "C4", "G3", "D4", "B4", "D4"]]
    mel = [(f, .5) for f in arp] * 2
    x = musique(mel, [(nf("C2"), 4), (nf("A2"), 4), (nf("F2"), 4), (nf("G2"), 4)], 100, "sine", "sine", .35)
    w = lp(noise(len(x) / SR), 600) * (0.5 + .5 * osc(.3, len(x) / SR)) * .08
    return x + w
def m_bal():
    mel = [(nf("D5"), 2), (nf("F#5"), 1), (nf("A5"), 2), (nf("F#5"), 1), (nf("D5"), 2), (nf("E5"), 1), (nf("F#5"), 3), (nf("E5"), 2), (nf("D5"), 1), (nf("C#5"), 2), (nf("D5"), 1), (nf("E5"), 3), (nf("A4"), 3), (nf("D5"), 3)]
    bass = []
    for r, c in [("D3", ["F#4", "A4"]), ("D3", ["F#4", "A4"]), ("A2", ["E4", "A4"]), ("D3", ["F#4", "A4"]), ("G2", ["D4", "B4"]), ("A2", ["E4", "A4"]), ("D3", ["F#4", "A4"])]:
        bass += [(nf(r), 1), (nf(c[0]), 1), (nf(c[1]), 1)]
    return musique(mel, bass, 150, "tri", "sine", .3)
def m_orient():
    sc = {"D": 293.66, "Eb": 311.13, "F#": 369.99, "G": 392, "A": 440, "Bb": 466.16, "C": 523.25, "D2": 587.33}
    seqn = ["D", "Eb", "F#", "G", "F#", "Eb", "D", "A", "G", "F#", "Eb", "D", "Eb", "F#", "G", "A", "Bb", "A", "G", "F#", "Eb", "D"]
    mel = [(sc[n], 1 if i % 3 else 1.5) for i, n in enumerate(seqn)]
    bass = [(146.83, 2), (146.83, 1), (220, 1)] * 8
    return musique(mel, bass, 110, "saw", "sine", .18)
def m_souk():
    sc = {"E": 329.63, "F": 349.23, "G#": 415.3, "A": 440, "B": 493.88, "C": 523.25, "D#": 622.25}
    seqn = ["A", "B", "C", "B", "A", "G#", "F", "E", "F", "G#", "A", "A", "C", "D#", "C", "B", "A", "G#", "A"]
    mel = [(sc.get(n, 440), .5 if i % 2 else 1) for i, n in enumerate(seqn)]
    bass = [(110, 1), (None, .5), (110, .5), (165, 1)] * 8
    m = musique(mel, bass, 130, "tri", "tri", .3)
    return m
MUSIQUES = [
 ("joyeuse", "موسيقى مرحة", "Joyeuse", m_joyeuse, []), ("triste", "موسيقى حزينة", "Triste", m_triste, ["cinderella"]), ("mystere", "موسيقى غامضة", "Mystère", m_mystere, ["layla", "alibaba"]),
 ("aventure", "موسيقى مغامرة", "Aventure", m_aventure, ["sindbad"]), ("mer", "موسيقى البحر", "Mer", m_mer, ["sindbad"]), ("bal", "موسيقى الحفلة (فالس)", "Bal", m_bal, ["cinderella"]),
 ("orientale", "موسيقى شرقية", "Orientale", m_orient, ["alibaba", "djeha"]), ("souk", "موسيقى السوق", "Souk", m_souk, ["djeha", "alibaba"]),
]
