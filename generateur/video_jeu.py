"""Vidéos de démonstration des jeux (jeux/videos/<jeu>.mp4) : la partie est VRAIMENT exécutée par scratch-vm (generateur/enregistrer_jeu.js),
image par image, puis dessinée avec les éléments du projet et encodée avec ffmpeg (musique et sons inclus).
Usage : SCRATCH_NODE_MODULES=<dossier node_modules contenant scratch-vm et scratch-storage> python3 generateur/video_jeu.py [catch|course ...]
(Node, Playwright et ffmpeg requis)"""
import os, sys, json, re, zipfile, subprocess, tempfile, shutil
from xml.sax.saxutils import escape
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "jeux", "videos"); os.makedirs(OUT, exist_ok=True)
FPS = 30
GAMES = {"catch": dict(sb3="jeu_sindbad.sb3", mp4="attrape-poissons.mp4", event="score_up", sound_sprite="الشيء", hud=("النقاط", "الأرواح")),
         "course": dict(sb3="jeu_course.sb3", mp4="course.mp4", event="lives_down", sound_sprite="سيارة معاكسة", hud=("النقاط", "الأرواح"))}

def load(sb3):
    z = zipfile.ZipFile(sb3); p = json.loads(z.read("project.json")); T = []
    for t in p["targets"]:
        cs = []
        for c in t["costumes"]:
            svg = re.sub(r'^<\?xml[^>]*>\s*', '', z.read(c["md5ext"]).decode("utf-8").strip())
            m = re.match(r'<svg[^>]*>', svg); w = float(re.search(r'width="([\d.]+)', m.group(0)).group(1)); h = float(re.search(r'height="([\d.]+)', m.group(0)).group(1))
            cs.append(dict(svg=svg.replace("<svg", '<svg x="0" y="0"', 1), w=w, h=h, rcx=c.get("rotationCenterX", w / 2), rcy=c.get("rotationCenterY", h / 2)))
        T.append(dict(name=t["name"], costumes=cs, sounds=[s["md5ext"] for s in t["sounds"]], stage=t["isStage"]))
    return z, T
def place(c, x, y, size):
    s = size / 100; tx, ty = 240 + x - c["rcx"] * s, 180 - y - c["rcy"] * s
    return f'<g transform="translate({tx:.1f},{ty:.1f}) scale({s})">{c["svg"]}</g>'
FONT = "Tajawal,Arial,sans-serif"
def bubble(text, x, y):
    w = 11 * len(text) + 30
    return (f'<g><rect x="{x - w/2}" y="{y}" width="{w}" height="34" rx="14" fill="#fff" stroke="#9aa3b2" stroke-width="2"/>'
            f'<text x="{x}" y="{y + 23}" text-anchor="middle" font-family="{FONT}" font-size="17" font-weight="bold" fill="#333">{escape(text)}</text></g>')
def monitor(label, value, x, y):
    return (f'<g><rect x="{x}" y="{y}" width="108" height="22" rx="4" fill="#e6f0ff" stroke="#c4d3f0"/><text x="{x + 6}" y="{y + 16}" font-family="{FONT}" font-size="13" fill="#575e75" font-weight="bold">{label}</text>'
            f'<rect x="{x + 70}" y="{y + 3}" width="34" height="16" rx="3" fill="#ff8c1a"/><text x="{x + 87}" y="{y + 16}" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#fff">{int(value) if float(value).is_integer() else round(value, 2)}</text></g>')
def tag(txt, x, y, color):
    w = 9 * len(txt) + 18
    return f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="14" fill="{color}"/><text x="{x + w/2}" y="{y + 19}" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="bold" fill="#fff">{escape(txt)}</text>'

def render(frames, T):
    """un SVG par image ; bulle de dialogue : 4 s pour la consigne, 3 s pour le message de fin (comme dans les scripts)"""
    svgs = []; shown = {}; events = []
    prev = None
    for i, fr in enumerate(frames):
        s = ""
        for t in T:   # ordre des calques = ordre du projet
            if t["stage"]: s += place(t["costumes"][0], 0, 0, 100); continue
            d = next(x for x in fr["sp"] if x["name"] == t["name"])
            if d["visible"]: s += place(t["costumes"][min(d["costume"], len(t["costumes"]) - 1)], d["x"], d["y"], d["size"])
        s += monitor("النقاط", fr["score"], 4, 4) + monitor("الأرواح", fr["lives"], 4, 30)
        for d in fr["sp"]:
            if d["say"]:
                key = (d["name"], d["say"]); shown.setdefault(key, i); dur = (3 if d["say"].startswith("انتهت") else 4) * FPS
                if i - shown[key] < dur and d["visible"]: s += bubble(d["say"], 240 + max(-140, min(140, d["x"])), 120 if d["name"] in ("اللاعب", "السيارة") else 20 if False else 120)
        if prev:
            if fr["score"] > prev["score"]: events.append(("score_up", i)); fr["_flash"] = i
            if fr["lives"] < prev["lives"]: events.append(("lives_down", i))
        svgs.append(s); prev = fr
    return svgs, events

def make(name):
    G = GAMES[name]; tmp = tempfile.mkdtemp(); sb3 = os.path.join(ROOT, "jeux", G["sb3"]); frames_json = os.path.join(tmp, "rec.json")
    node_mod = os.environ.get("SCRATCH_NODE_MODULES")
    if not node_mod: sys.exit("Définir SCRATCH_NODE_MODULES (dossier node_modules avec scratch-vm et scratch-storage)")
    subprocess.run(["node", os.path.join(HERE, "enregistrer_jeu.js"), sb3, frames_json, name], check=True, env=dict(os.environ, NODE_PATH=node_mod), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    frames = json.load(open(frames_json)); z, T = load(sb3); body, events = render(frames, T)
    # « +1 » une seconde après chaque prise (jeu du poisson)
    flash = {}
    if name == "catch":
        for kind, i in events:
            if kind == "score_up":
                p = next(x for x in frames[i]["sp"] if x["name"] == "اللاعب")["x"]
                for k in range(i, min(i + FPS, len(frames))): flash[k] = ("+1", "#2e9e5b", p)
    svgs = [f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">{b}' + (tag(*flash[i][:2][:1], int(240 + flash[i][2]) - 25, 205, flash[i][1]) if i in flash else "") + "</svg>" for i, b in enumerate(body)]
    json.dump(svgs, open(os.path.join(tmp, "frames.json"), "w")); os.makedirs(os.path.join(tmp, "f"))
    open(os.path.join(tmp, "shot.js"), "w").write("""const {chromium}=require('playwright');const fs=require('fs');(async()=>{const S=JSON.parse(fs.readFileSync(process.argv[2]+'/frames.json'));const b=await chromium.launch();
const p=await b.newPage({viewport:{width:480,height:360},deviceScaleFactor:1.5});await p.setContent('<body style="margin:0;background:#fff"></body>');
for(let i=0;i<S.length;i++){await p.evaluate(s=>{document.body.innerHTML=s},S[i]);await p.screenshot({path:process.argv[2]+'/f/'+String(i).padStart(5,'0')+'.png'});}await b.close();})();""")
    subprocess.run(["node", os.path.join(tmp, "shot.js"), tmp], check=True)
    # sons : musique de la scène + son du lutin à chaque événement
    stage = next(t for t in T if t["stage"]); sprite = next(t for t in T if t["name"] == G["sound_sprite"])
    open(os.path.join(tmp, "music.wav"), "wb").write(z.read(stage["sounds"][0])); open(os.path.join(tmp, "sfx.wav"), "wb").write(z.read(sprite["sounds"][0]))
    hits = [i for kind, i in events if kind == G["event"]]; dur = len(frames) / FPS
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "f", "%05d.png"), "-stream_loop", "-1", "-i", os.path.join(tmp, "music.wav")]
    for _ in hits: cmd += ["-i", os.path.join(tmp, "sfx.wav")]
    fc = "[1:a]volume=0.15[m]"; mix = ["[m]"]
    for k, i in enumerate(hits): ms = int(i / FPS * 1000); fc += f";[{k + 2}:a]adelay={ms}|{ms}[s{k}]"; mix.append(f"[s{k}]")
    fc += ";" + "".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{dur:.2f}[a]"
    mp4 = os.path.join(OUT, G["mp4"])
    subprocess.run(cmd + ["-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-t", f"{dur:.2f}", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "26", "-preset", "medium", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "96k", mp4], check=True)
    shutil.rmtree(tmp); print(name, ":", round(dur, 1), "s,", len(hits), "événements sonores,", os.path.getsize(mp4) // 1024, "Ko")
if __name__ == "__main__":
    for n in (sys.argv[1:] or list(GAMES)): make(n)
