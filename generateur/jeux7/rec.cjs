const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const g = process.argv[2], dur = +process.argv[3]; const b = await chromium.launch();
  const t0 = Date.now(); const c = await b.newContext({ viewport: { width: 480, height: 360 }, recordVideo: { dir: 'vid_' + g, size: { width: 480, height: 360 } } }); const p = await c.newPage();
  await p.goto('file://' + process.cwd() + '/demo.html?g=' + g); await p.waitForLoadState('load'); await p.waitForTimeout(800);
  const ts = Date.now(); await p.evaluate(() => window.run());
  await p.waitForFunction(() => window.__ev.some(e => e[1] === 'fin'), null, { timeout: 120000 }); await p.waitForTimeout(400);
  const ev = await p.evaluate(() => window.__ev); fs.writeFileSync(`ev_${g}.json`, JSON.stringify({ ev, offset: (ts - t0) / 1000 }));
  await c.close(); await b.close(); console.log(g, 'événements', ev.length, 'offset', (ts - t0) / 1000); })();
