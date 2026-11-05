"""Rend les fichiers .docx lisibles par Word 2007 (et produit une version .doc).
- alignement « start/end » (Word 2010+) -> « left/right » ;
- suppression des réglages de compatibilité propres à Word 2010+ ;
- conversion en .doc (Word 97-2003) avec LibreOffice, si disponible.
Usage : python3 generateur/word_compat.py word"""
import sys, os, re, zipfile, shutil, subprocess, glob, tempfile
d = sys.argv[1]
def fix(xml, name):
    if name == "word/settings.xml":
        xml = re.sub(r"<w:compat>.*?</w:compat>", "<w:compat/>", xml, flags=re.S)
        xml = xml.replace("<w:displayBackgroundShape/>", "")
    if name in ("word/document.xml", "word/numbering.xml", "word/styles.xml"):
        xml = xml.replace('w:jc w:val="start"', 'w:jc w:val="left"').replace('w:jc w:val="end"', 'w:jc w:val="right"')
        xml = xml.replace('w:lvlJc w:val="start"', 'w:lvlJc w:val="left"').replace('w:lvlJc w:val="end"', 'w:lvlJc w:val="right"')
    return xml
for f in sorted(glob.glob(os.path.join(d, "*.docx"))):
    tmp = f + ".tmp"
    with zipfile.ZipFile(f) as zi, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
        for it in zi.infolist():
            data = zi.read(it.filename)
            if it.filename.endswith(".xml"): data = fix(data.decode("utf-8"), it.filename).encode("utf-8")
            zo.writestr(it, data)
    os.replace(tmp, f)
print("docx corrigés :", len(glob.glob(os.path.join(d, "*.docx"))))
so = shutil.which("soffice") or shutil.which("libreoffice")
if so:
    for f in sorted(glob.glob(os.path.join(d, "*.docx"))):
        with tempfile.TemporaryDirectory() as td:
            subprocess.run([so, "--headless", "--convert-to", "doc:MS Word 97", "--outdir", td, f], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            shutil.move(os.path.join(td, os.path.basename(f)[:-5] + ".doc"), f[:-5] + ".doc")
    print(".doc générés :", len(glob.glob(os.path.join(d, "*.doc"))))
else:
    print("LibreOffice absent : pas de versions .doc")
