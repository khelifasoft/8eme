"""Vidéo de démonstration du jeu « Attrape les poissons » (jeux/videos/attrape-poissons.mp4).
La partie est rejouée image par image avec exactement les règles du script Scratch (generateur/jeux.py) :
 - 30 images/s ; le poisson descend de « vitesse » pixels par image (vitesse de départ 3) ;
 - attrapé si |x poisson − x souris| < 55 et y < −90 : son « plouf », +1 point, vitesse +0,25, nouveau poisson en haut ;
 - manqué si y < −165 : −1 vie, nouveau poisson ; à 0 vie : « انتهت اللعبة! » 3 s puis arrêt.
Le joueur suit la souris (x). Les images sont dessinées avec les éléments réels du projet, puis encodées avec ffmpeg.
Usage : python3 generateur/video_jeu.py   (Node + Playwright + ffmpeg requis)"""
import os, sys, json, random, subprocess, tempfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
import fiches_etapes as FE
from xml.sax.saxutils import escape
OUT = os.path.join(ROOT, "jeux", "videos"); os.makedirs(OUT, exist_ok=True)
FPS = 30; CATCH = 6   # nombre de poissons attrapés avant de rater exprès
rnd = random.Random(7)

def simulate():
    speed, score, lives = 3.0, 0, 3; px = 0.0; mouse = 0.0
    ix, iy = rnd.randint(-200, 200), 180.0; frames = []; events = []; say = None; say_left = 4 * FPS; n = 0; end = None
    target_x = lambda: ix if score < CATCH else (-200 if ix > 0 else 200)
    while True:
        # la souris se déplace vers la cible (un peu comme une vraie main), le joueur suit la souris
        tx = target_x(); mouse += max(-14, min(14, (tx - mouse) * 0.22)); px = mouse
        if end is None:
            iy -= speed
            if abs(ix - mouse) < 55 and iy < -90:
                events.append(n); score += 1; speed += 0.25; ix, iy = rnd.randint(-200, 200), 180.0
            if iy < -165:
                lives -= 1; ix, iy = rnd.randint(-200, 200), 180.0
            if lives < 1: end = n; say_left = 3 * FPS; say = "انتهت اللعبة!"
        if say_left > 0 and say is None: say = None
        bubble = ("حرّك الفأرة لتلتقط الأسماك." if n < 4 * FPS and end is None else None) or (say if end is not None and n - end < 3 * FPS else None)
        frames.append(dict(px=px, ix=ix, iy=iy, score=score, lives=lives, bubble=bubble, flash=None)); n += 1
        if end is not None and n - end >= 3 * FPS + 10: break
        if n > FPS * 90: break
    for e in events:  # « +1 » affiché une seconde après chaque prise
        for k in range(e, min(e + FPS, len(frames))): frames[k]["flash"] = ("+1", "#2e9e5b", frames[e]["px"])
    return frames, events, end

def bubble(text, x, y):
    w = 11 * len(text) + 30
    return (f'<g><rect x="{x - w/2}" y="{y}" width="{w}" height="34" rx="14" fill="#fff" stroke="#9aa3b2" stroke-width="2"/>'
            f'<text x="{x}" y="{y + 23}" text-anchor="middle" font-family="Tajawal,Arial,sans-serif" font-size="17" font-weight="bold" fill="#333">{escape(text)}</text></g>')
def monitor(label, value, x, y):
    return (f'<g><rect x="{x}" y="{y}" width="108" height="22" rx="4" fill="#e6f0ff" stroke="#c4d3f0"/><text x="{x + 6}" y="{y + 16}" font-family="Tajawal,Arial,sans-serif" font-size="13" fill="#575e75" font-weight="bold">{label}</text>'
            f'<rect x="{x + 70}" y="{y + 3}" width="34" height="16" rx="3" fill="#ff8c1a"/><text x="{x + 87}" y="{y + 16}" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#fff">{value}</text></g>')
def render(fr, A):
    back, pl, it = A["Stage"], A["اللاعب"], A["الشيء"]
    s = FE.place(back, 0, 0, 100) + FE.place(pl, fr["px"], -125) + FE.place(it, fr["ix"], fr["iy"])
    s += monitor("النقاط", fr["score"], 4, 4) + monitor("الأرواح", fr["lives"], 4, 30)
    if fr["bubble"]: s += bubble(fr["bubble"], 240 + max(-130, min(130, fr["px"])), 175)
    if fr["flash"]: s += FE.tag(fr["flash"][0], int(240 + fr["flash"][2]) - 25, 205, fr["flash"][1])
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">{s}</svg>'

def main():
    frames, events, end = simulate(); A = FE.sb3_art(os.path.join(ROOT, "jeux", "jeu_sindbad.sb3")); tmp = tempfile.mkdtemp(); fd = os.path.join(tmp, "f"); os.makedirs(fd)
    svgs = [render(f, A) for f in frames]
    json.dump(svgs, open(os.path.join(tmp, "frames.json"), "w"))
    open(os.path.join(tmp, "shot.js"), "w").write("""const {chromium}=require('playwright');const fs=require('fs');(async()=>{const S=JSON.parse(fs.readFileSync(process.argv[2]+'/frames.json'));const b=await chromium.launch();
const p=await b.newPage({viewport:{width:480,height:360},deviceScaleFactor:1.5});await p.setContent('<body style="margin:0;background:#fff"></body>');
for(let i=0;i<S.length;i++){await p.evaluate(s=>{document.body.innerHTML=s},S[i]);await p.screenshot({path:process.argv[2]+'/f/'+String(i).padStart(5,'0')+'.png'});}await b.close();})();""")
    subprocess.run(["node", os.path.join(tmp, "shot.js"), tmp], check=True)
    snd = os.path.join(ROOT, "jeux", "ressources", "attrape-poissons")
    dur = len(frames) / FPS; cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(fd, "%05d.png"), "-stream_loop", "-1", "-i", os.path.join(snd, "musique-mer.wav")]
    for e in events: cmd += ["-i", os.path.join(snd, "son-plouf.wav")]
    fc = "[1:a]volume=0.15[m]"; mix = ["[m]"]
    for k, e in enumerate(events):
        ms = int(e / FPS * 1000); fc += f";[{k + 2}:a]adelay={ms}|{ms}[s{k}]"; mix.append(f"[s{k}]")
    fc += ";" + "".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{dur:.2f}[a]"
    cmd += ["-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-t", f"{dur:.2f}", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "26", "-preset", "medium", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "96k", os.path.join(OUT, "attrape-poissons.mp4")]
    subprocess.run(cmd, check=True); shutil.rmtree(tmp)
    print("vidéo :", round(dur, 1), "s,", len(events), "poissons attrapés,", os.path.getsize(os.path.join(OUT, "attrape-poissons.mp4")) // 1024, "Ko")
if __name__ == "__main__": main()
