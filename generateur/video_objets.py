"""Vidéos et ressources des séances micro:bit (M1-M4) et App Inventor (A1-A4) de la 9e : videos/objets/<séance>-{ar,fr}.mp4 et objets/ressources/<séance>.zip
(programme MakeCode en JavaScript ou plan des blocs, images de la carte ou des écrans, notice). Scènes et textes : objets.py. Vidéos silencieuses (animation avec légendes, sans voix) et capture d'écran de présentation : objets/captures/<séance>-{ar,fr}.jpg.
Usage : python3 generateur/video_objets.py   (espeak-ng, ffmpeg, Node et Playwright requis)"""
import os, sys, json, subprocess, tempfile, html, zipfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
import objets as O
VID = os.path.join(ROOT, "videos", "objets"); ZIP = os.path.join(ROOT, "objets", "ressources"); os.makedirs(VID, exist_ok=True); os.makedirs(ZIP, exist_ok=True)
VOICE = {"fr": ["-v", "fr", "-s", "145"], "ar": ["-v", "ar", "-s", "125"]}
ACC = {"M": "#6a4fc7", "A": "#1e4fa8"}
def slide(key, lang, i, n, vis, cap, narr):
    ac = ACC[key[0]]; rtl = lang == "ar"
    dots = "".join(f'<i style="background:{ac if j == i else "#cfd6e4"}"></i>' for j in range(n))
    return f'''<!doctype html><html lang="{lang}" dir="{"rtl" if rtl else "ltr"}"><meta charset="utf-8"><style>
html,body{{margin:0;width:1280px;height:720px;font-family:"Tajawal","DejaVu Sans",Arial,sans-serif}}body{{background:linear-gradient(160deg,#eef3fb,#fff);display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:18px 60px 28px;box-sizing:border-box}}
.top{{align-self:stretch;display:flex;justify-content:space-between;font-size:24px;font-weight:700;color:{ac}}}.top b{{background:{ac};color:#fff;border-radius:999px;padding:0 18px}}
.v{{height:400px;display:flex;align-items:center}}.v svg{{height:400px;width:auto}}h1{{margin:0;font-size:46px;color:#1d2433;text-align:center}}p{{margin:0;font-size:29px;color:#333;text-align:center;line-height:1.4;max-width:1120px}}
.d{{display:flex;gap:10px}}.d i{{display:block;width:14px;height:14px;border-radius:50%}}</style>
<div class="top"><span>{html.escape("micro:bit" if key[0] == "M" else "App Inventor")} · {key}</span><b>{i + 1} / {n}</b></div><div class="v">{vis}</div><h1>{html.escape(cap)}</h1><p>{html.escape(narr)}</p><div class="d">{dots}</div></html>'''
def main():
    tmp = tempfile.mkdtemp(prefix="obj_"); jobs = []; plan = []
    for key, d in O.OBJ.items():
        n = len(d["scenes"])
        for lang in ("ar", "fr"):
            li = 1 if lang == "ar" else 0
            for i, (spec, cap, narr) in enumerate(d["scenes"]):
                base = os.path.join(tmp, f"{key}-{lang}-{i}")
                open(base + ".html", "w", encoding="utf-8").write(slide(key, lang, i, n, O.visual(spec, lang), cap[li], narr[li]))
                words = len(narr[li].split()); open(base + ".dur", "w").write(str(max(5.0, 0.42 * words) + 1.0))
                jobs.append(dict(html=base + ".html", png=base + ".png"))
            plan.append((key, lang, n))
        # images à télécharger : une image par scène (français et arabe)
        for lang in ("ar", "fr"):
            for i, (spec, cap, narr) in enumerate(d["scenes"]):
                base = os.path.join(tmp, f"img-{key}-{lang}-{i}")
                open(base + ".html", "w", encoding="utf-8").write(f'<!doctype html><meta charset="utf-8"><body style="margin:0;background:#fff">{O.visual(spec, lang)}</body>')
                jobs.append(dict(html=base + ".html", png=base + ".png", clip=True))
    js = os.path.join(tmp, "shots.js")
    open(js, "w").write("const {chromium}=require('playwright');(async()=>{const jobs=JSON.parse(process.argv[2]);const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});for(const j of jobs){await p.goto('file://'+j.html);await p.waitForTimeout(120);if(j.clip){const e=await p.$('svg');await e.screenshot({path:j.png,omitBackground:false});}else await p.screenshot({path:j.png});}await b.close();})();")
    subprocess.run(["node", js, json.dumps(jobs)], check=True)
    for key, lang, n in plan:
        parts = []
        for i in range(n):
            base = os.path.join(tmp, f"{key}-{lang}-{i}"); out = base + ".mp4"
            dur = float(open(base + ".dur").read())
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "10", "-i", base + ".png", "-t", f"{dur:.2f}", "-an", "-c:v", "libx264", "-tune", "stillimage", "-crf", "30", "-pix_fmt", "yuv420p", out], check=True)
            parts.append(out)
        lst = os.path.join(tmp, f"{key}-{lang}.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", os.path.join(VID, f"{key}-{lang}.mp4")], check=True)
    POST = os.path.join(ROOT, "objets", "captures"); os.makedirs(POST, exist_ok=True)
    for key, d in O.OBJ.items():       # capture d'écran de présentation (une scène représentative), sans son
        for lang in ("ar", "fr"):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(tmp, f"{key}-{lang}-{min(1, len(d['scenes']) - 1)}.png"), "-q:v", "4", os.path.join(POST, f"{key}-{lang}.jpg")], check=True)
    for key, d in O.OBJ.items():
        z = os.path.join(ZIP, f"{key}.zip")
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            if key in O.CODE: zf.writestr(O.CODE[key][0], O.CODE[key][1])
            for lang in ("fr", "ar"):
                for i in range(len(d["scenes"])): zf.write(os.path.join(tmp, f"img-{key}-{lang}-{i}.png"), f"images-{lang}/{key}-{i + 1}.png")
            how = ("Coller le contenu du fichier .ts dans MakeCode (makecode.microbit.org) : nouveau projet, bouton « JavaScript » en haut, remplacer le code." if key[0] == "M" and key in O.CODE else
                   "Utiliser le plan des blocs pour construire les blocs dans App Inventor (appinventor.mit.edu)." if key in O.CODE else "Les images montrent la carte ou l'écran à chaque étape.")
            howa = ("الصق محتوى ملف .ts في MakeCode (makecode.microbit.org): مشروع جديد ثم زرّ «JavaScript» في الأعلى واستبدل الشفرة." if key[0] == "M" and key in O.CODE else
                    "استعمل مخطط الكتل لبناء الكتل في App Inventor (appinventor.mit.edu)." if key in O.CODE else "تُظهر الصور البطاقة أو الشاشة في كل مرحلة.")
            zf.writestr("LISEZMOI.txt", f"{d['t'][0]}\n\n{how}\nImages : dossier images-fr (français) et images-ar (arabe). Les images PNG peuvent être importées dans App Inventor (Médias).\nAucun matériel ni compte n'est nécessaire (simulateur / émulateur).\n\n{d['t'][1]}\n\n{howa}\n")
        print(z, os.path.getsize(z) // 1024, "Ko")
if __name__ == "__main__": main()
