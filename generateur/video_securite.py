"""Vidéos explicatives du cours « Sécurité informatique » : videos/securite/securite-<n>-{ar,fr}.mp4 (1280 x 720, une image par scène avec légende et voix de synthèse eSpeak NG).
Scènes et textes : securite.py (champ video). Usage : python3 generateur/video_securite.py   (requiert espeak-ng, ffmpeg, Node et Playwright)"""
import os, sys, json, subprocess, tempfile, html
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
import securite as SE
OUT = os.path.join(ROOT, "videos", "securite"); os.makedirs(OUT, exist_ok=True)
COL = {"S1": ("#fff4d6", "#e8a21c"), "S2": ("#fde8e5", "#c0392b"), "S3": ("#eaf2ff", "#1e4fa8"), "S4": ("#e6f6ec", "#2e9e5b")}
VOICE = {"fr": ["-v", "fr", "-s", "145"], "ar": ["-v", "ar", "-s", "125"]}
def slide(key, lang, i, n, emoji, cap, narr, title):
    bg, ac = COL[key]; rtl = lang == "ar"
    dots = "".join(f'<i style="background:{ac if j == i else "#cfd6e4"}"></i>' for j in range(n))
    return f'''<!doctype html><html lang="{lang}" dir="{"rtl" if rtl else "ltr"}"><meta charset="utf-8"><style>
html,body{{margin:0;width:1280px;height:720px;font-family:"Tajawal","DejaVu Sans","Inter",Arial,sans-serif}}
body{{background:linear-gradient(160deg,{bg},#fff);display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:26px 60px 34px;box-sizing:border-box}}
.top{{align-self:stretch;display:flex;justify-content:space-between;align-items:center;font-size:26px;font-weight:700;color:{ac}}}
.top b{{background:{ac};color:#fff;border-radius:999px;padding:2px 20px}}
.em{{font-family:"Noto Color Emoji";font-size:230px;line-height:1.05}}
h1{{margin:0;font-size:60px;color:#1d2433;text-align:center;line-height:1.2}}
p{{margin:0;font-size:34px;color:#333;text-align:center;line-height:1.45;max-width:1100px}}
.d{{display:flex;gap:10px}}.d i{{display:block;width:16px;height:16px;border-radius:50%}}</style>
<div class="top"><span>{html.escape(title)}</span><b>{i + 1} / {n}</b></div><div class="em">{emoji}</div><h1>{html.escape(cap)}</h1><p>{html.escape(narr)}</p><div class="d">{dots}</div></html>'''
def main():
    tmp = tempfile.mkdtemp(prefix="sec_"); jobs = []; plan = []
    for key, d in SE.SEC.items():
        n = len(d["video"])
        for lang in ("ar", "fr"):
            li = 1 if lang == "ar" else 0
            for i, (emoji, cap, narr) in enumerate(d["video"]):
                base = os.path.join(tmp, f"{key}-{lang}-{i}")
                open(base + ".html", "w", encoding="utf-8").write(slide(key, lang, i, n, emoji, cap[li], narr[li], f'{SE.COURSE_TITLE[li]} · {"الحصة" if lang == "ar" else "Séance"} {key[1]}'))
                subprocess.run(["espeak-ng", *VOICE[lang], "-w", base + ".wav", narr[li]], check=True)
                jobs.append(dict(html=base + ".html", png=base + ".png"))
            plan.append((key, lang, n))
    js = os.path.join(tmp, "shots.js")
    open(js, "w").write("const {chromium}=require('playwright');(async()=>{const jobs=JSON.parse(process.argv[2]);const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});for(const j of jobs){await p.goto('file://'+j.html);await p.waitForTimeout(150);await p.screenshot({path:j.png});}await b.close();})();")
    subprocess.run(["node", js, json.dumps(jobs)], check=True)
    for key, lang, n in plan:
        parts = []
        for i in range(n):
            base = os.path.join(tmp, f"{key}-{lang}-{i}"); out = base + ".mp4"
            dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", base + ".wav"]).decode()) + 1.2
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "10", "-i", base + ".png", "-i", base + ".wav", "-af", "apad", "-t", f"{dur:.2f}", "-c:v", "libx264", "-tune", "stillimage", "-crf", "30", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "64k", "-ar", "44100", "-ac", "1", out], check=True)
            parts.append(out)
        lst = os.path.join(tmp, f"{key}-{lang}.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
        final = os.path.join(OUT, f"securite-{key[1]}-{lang}.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", final], check=True)
        print(final, os.path.getsize(final) // 1024, "Ko")
if __name__ == "__main__": main()
