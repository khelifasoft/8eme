"""Résumés PDF (une page, en points) des fiches d'activité : fiches-activite/pdf/<famille>.pdf
Usage : python3 generateur/fiches_resume.py   (nécessite Node + Playwright pour la conversion PDF)"""
import os, sys, subprocess, tempfile, shutil
from html import escape as E
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
import fiches_programme as FP
OUT = os.path.join(ROOT, "fiches-activite", "pdf"); os.makedirs(OUT, exist_ok=True)
CSS = """body{font:12.5px/1.45 'Segoe UI',Arial,sans-serif;color:#222;margin:0}h1{font-size:21px;color:#1e3a6e;margin:0 0 2px}.meta{color:#555;margin:0 0 10px}
h2{font-size:14px;color:#fff;background:#1e4fa8;margin:12px 0 4px;padding:2px 8px;border-radius:4px}ul{margin:2px 0 0;padding-left:20px}li{margin:1px 0}.sit{background:#f4f8ff;border-left:4px solid #1e4fa8;padding:5px 9px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:0 18px}@page{size:A4;margin:14mm}"""
def ul(items): return "<ul>" + "".join(f"<li>{E(x)}</li>" for x in items) + "</ul>"
def page(fid, F):
    lvl = FP.PRG["levels"][str(F["level"])]
    caps = [i for p in F["parts"] for i in lvl["parts"][p]["i_fr"]][:6]
    steps = [t for t, _ in F["demarche"]]
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{E(F["title"])}</title><style>{CSS}</style></head><body>
<h1>{E(F["title"])}</h1><p class="meta">{E(lvl["year_fr"])} · {E(F["duree"])} · fiche d'activité (résumé)</p>
<h2>Situation-problème</h2><p class="sit">{E(F["situation"])}</p>
<div class="cols"><div><h2>Capacités visées</h2>{ul(caps)}</div><div><h2>Déroulement</h2>{ul(steps)}</div></div>
<h2>Activités de l'élève</h2>{ul(F["eleve"])}
<div class="cols"><div><h2>Critères de réussite</h2>{ul(F["criteres"])}</div><div><h2>Différenciation</h2><ul><li><b>Allègement :</b> {E(F["allegee"])}</li><li><b>Prolongement :</b> {E(F["prolongement"])}</li></ul></div></div>
</body></html>'''
tmp = tempfile.mkdtemp(); js = os.path.join(tmp, "pdf.js")
open(js, "w").write("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();for(const [i,o] of JSON.parse(process.argv[2])){await p.goto('file://'+i);await p.pdf({path:o,format:'A4',printBackground:true});}await b.close();})();")
jobs = []
for fid, F in FP.FAMILIES.items():
    h = os.path.join(tmp, fid + ".html"); open(h, "w", encoding="utf-8").write(page(fid, F)); jobs.append([h, os.path.join(OUT, fid + ".pdf")])
import json
subprocess.run(["node", js, json.dumps(jobs)], check=True); shutil.rmtree(tmp)
print("PDF :", sorted(os.listdir(OUT)))
