// Imprime les pages cahier-N.html en PDF (A4, une fiche par page) : cahier-N-ar.pdf, cahier-N-fr.pdf, cahier-N-ar-corrige.pdf, cahier-N-fr-corrige.pdf
// Contrôle aussi qu'aucune fiche ne dépasse la page (le contenu qui déborde serait coupé).  Usage : node cahier_pdf.js <dossier cahier> [--check]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = process.argv[2], checkOnly = process.argv.includes('--check');
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 794, height: 1123 } });
  const p = await ctx.newPage();
  let bad = 0;
  for (const y of ['7', '8', '9']) for (const lang of ['ar', 'fr']) for (const corr of [0, 1]) {
    if (checkOnly && corr) continue;
    const url = 'file://' + path.join(dir, 'cahier-' + y + '.html') + '?lang=' + lang + (corr ? '&corrige=1' : '');
    await p.goto(url); await p.waitForTimeout(350);
    await p.emulateMedia({ media: 'print' });
    const over = await p.evaluate(() => [...document.querySelectorAll('.fiche')].map(f => [f.dataset.s, f.scrollHeight - f.clientHeight]).filter(x => x[1] > 1));
    if (over.length) { bad++; console.log('DÉBORDEMENT', y + 'e', lang, corr ? 'corrigé' : '', JSON.stringify(over)); }
    if (!checkOnly) { const out = path.join(dir, 'cahier-' + y + '-' + lang + (corr ? '-corrige' : '') + '.pdf'); await p.pdf({ path: out, format: 'A4', printBackground: true, margin: { top: '0', bottom: '0', left: '0', right: '0' }, preferCSSPageSize: true }); }
    await p.emulateMedia({ media: 'screen' });
  }
  console.log(bad ? bad + ' combinaison(s) avec débordement' : 'aucun débordement : toutes les fiches tiennent sur une page A4');
  await b.close();
  process.exit(bad ? 1 : 0);
})();
