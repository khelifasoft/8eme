// Fait jouer un projet Scratch (.sb3) dans scratch-vm, sans écran, image par image (30 images/s), et enregistre l'état de la scène.
// Chaque tour de boucle « répéter indéfiniment » correspond à une image, comme dans Scratch avec affichage.
// Usage : NODE_PATH=<node_modules avec scratch-vm et scratch-storage> node enregistrer_jeu.js jeu.sb3 frames.json catch|course [images_max]
const VM = require('scratch-vm'); const _S = require('scratch-storage'); const Storage = _S.default || _S.ScratchStorage || _S; const fs = require('fs');
(async () => {
  const [f, out, mode, maxN] = [process.argv[2], process.argv[3], process.argv[4] || 'catch', +(process.argv[5] || 3600)];
  const vm = new VM(); vm.attachStorage(new Storage()); console.warn = () => {};
  await vm.loadProject(fs.readFileSync(f));
  const rt = vm.runtime, seq = rt.sequencer, orig = seq.stepThread.bind(seq);
  seq.stepThread = t => { orig(t); rt.redrawRequested = true; };       // une seule passe par image
  const stage = rt.getTargetForStage(); const val = n => { const v = Object.values(stage.variables).find(x => x.name === n); return v ? +v.value : 0; };
  const T = n => rt.targets.find(t => t.sprite && t.sprite.name === n);
  const said = {}; rt.on('SAY', (t, type, msg) => { said[t.sprite.name] = msg || ''; });
  const FPS = 30, frames = []; let ended = -1;
  // les durées (« dire pendant n secondes », « attendre ») utilisent l'horloge : on la fait avancer de 1/30 s par image
  let clock = Date.now(); const realNow = Date.now; Date.now = () => clock;
  const rng = (() => { let s = 12345; return () => (s = (s * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff; })();
  const item = T('الشيء') || T('سيارة معاكسة'), player = T('اللاعب') || T('السيارة');
  let mouse = 0, keyL = false, keyR = false;
  const key = (k, down) => vm.postIOData('keyboard', { key: k, isDown: down });
  vm.greenFlag();
  for (let n = 0; n < maxN; n++) {
    const t = n / FPS;
    if (mode === 'catch') {                       // on suit le poisson 12 s, puis on s'écarte pour rater
      const target = t < 12 ? item.x : (item.x > 0 ? -200 : 200);
      mouse += Math.max(-14, Math.min(14, (target - mouse) * 0.22));
      vm.postIOData('mouse', { x: mouse + 240, y: 180, canvasWidth: 480, canvasHeight: 360, isDown: false });
    } else {                                      // course : on évite 8 voitures, puis on fonce dessus
      let want = 0;
      const safe = t < 16 && Math.abs(item.x - player.x) < 70 && item.y < 80 && item.y > -190;
      if (safe) want = item.x > player.x ? -1 : (item.x < player.x ? 1 : (player.x > 0 ? -1 : 1));
      else if (t >= 16) want = Math.abs(item.x - player.x) > 6 ? (item.x > player.x ? 1 : -1) : 0;
      else want = Math.abs(player.x) > 8 ? (player.x > 0 ? -1 : 1) : 0;
      if (want < 0 !== keyL || (want < 0) !== keyL) { }
      const L = want < 0, R = want > 0; if (L !== keyL) { key('ArrowLeft', L); keyL = L; } if (R !== keyR) { key('ArrowRight', R); keyR = R; }
    }
    clock += 1000 / FPS; rt._step();
    const sp = rt.targets.filter(x => x.sprite).map(x => ({ name: x.sprite.name, x: x.x, y: x.y, size: x.size, visible: x.visible, costume: x.currentCostume, say: said[x.sprite.name] || '' }));
    frames.push({ t, sp, score: val('النقاط'), lives: val('الأرواح'), speed: val('السرعة') });
    if (rt.threads.length === 0 && n > FPS && ended < 0) ended = n;
    if (ended >= 0 && n - ended > FPS) break;
  }
  fs.writeFileSync(out, JSON.stringify(frames)); Date.now = realNow;
  const l = frames[frames.length - 1]; console.log('images', frames.length, 'durée', (frames.length / FPS).toFixed(1), 's score', l.score, 'vies', l.lives, 'vitesse', l.speed);
  process.exit(0);
})();
