import json, wave, struct, subprocess, glob, sys
SR = 22050
def rd(p):
    with wave.open(p) as f: return list(struct.unpack('<%dh' % f.getnframes(), f.readframes(f.getnframes())))
def build(g, music, vol_music, sounds, resdir):
    d = json.load(open(f'ev_{g}.json')); ev = d['ev']; end = ev[-1][0] + .3; n = int(end * SR); out = [0.0] * n
    m = rd(f'{resdir}/{music}'); start = 0.0 if g == 'singe' else 0.0
    for i in range(n): out[i] += m[i % len(m)] * vol_music
    for t, k in ev:
        if k in sounds:
            s = rd(f'{resdir}/{sounds[k]}'); o = int(t * SR)
            for i, x in enumerate(s):
                if o + i < n: out[o + i] += x * .8
    with wave.open(f'audio_{g}.wav', 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(b''.join(struct.pack('<h', max(-32767, min(32767, int(x)))) for x in out))
    vid = glob.glob(f'vid_{g}/*.webm')[0]
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(d['offset']), '-i', vid, '-i', f'audio_{g}.wav', '-t', str(end), '-vf', 'scale=720:540:flags=lanczos,fps=30', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '23', '-c:a', 'aac', '-b:a', '96k', '-shortest', '-movflags', '+faststart', f'{g}.mp4'], check=True)
build('singe', 'musique-jungle.wav', .35, {'banane': 'son-banane.wav', 'perdu': 'son-perdu.wav'}, 'res')
build('requin', 'musique-mer.wav', .35, {'glou': 'son-glouglou.wav', 'victoire': 'son-victoire.wav'}, 'res_r')
