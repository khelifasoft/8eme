// Fait jouer un projet « attrape-objets » (.sb3) dans scratch-vm sans écran et enregistre l'état de la scène 30 fois par seconde.
// Usage : NODE_PATH=<dossier node_modules avec scratch-vm et scratch-storage> node enregistrer_jeu.js jeu.sb3 frames.json [secondes_a_attraper]
const VM = require('scratch-vm'); const _S = require('scratch-storage'); const Storage = _S.default || _S.ScratchStorage || _S; const fs = require('fs');
(async () => {
  const [f, out, catchSec] = [process.argv[2], process.argv[3], +(process.argv[4] || 14)];
  const vm = new VM(); vm.attachStorage(new Storage()); console.warn = () => {};
  await vm.loadProject(fs.readFileSync(f));
  const stage = vm.runtime.getTargetForStage(); const val = n => { const v = Object.values(stage.variables).find(x => x.name === n); return v && v.value; };
  const T = n => vm.runtime.targets.find(t => t.sprite && t.sprite.name === n);
  const item = T('الشيء'), player = T('اللاعب'); const frames = [];
  // pas à pas (30 images par seconde), sans attendre le temps réel : enregistrement rapide et reproductible
  vm.greenFlag(); const FPS = 30; let end = 0;
  for (let n = 0; n < FPS * 120; n++) {
    const t = n / FPS; const mx = t < catchSec ? item.x : (item.x > 0 ? -200 : 200);   // d'abord on attrape, ensuite on rate exprès
    vm.postIOData('mouse', { x: mx + 240, y: 180, canvasWidth: 480, canvasHeight: 360, isDown: false });
    vm.runtime._step();
    frames.push({ t, px: player.x, py: player.y, ps: player.size, ix: item.x, iy: item.y, iv: item.visible, is: item.size, score: +val('النقاط'), lives: +val('الأرواح'), speed: +val('السرعة') });
    if (vm.runtime.threads.length === 0 && n > FPS) { if (++end > FPS * 1.5) break; }
  }
  frames.forEach((f, i) => { if (i >= frames.length - FPS * 1.5) f.end = true; });
  fs.writeFileSync(out, JSON.stringify(frames)); console.log('images', frames.length, 'durée', (frames.length / FPS).toFixed(1), 's score', frames[frames.length - 1].score, 'vies', frames[frames.length - 1].lives);
  process.exit(0);
})();
