// Fait jouer un projet Scratch (.sb3) dans scratch-vm, sans écran, image par image (30 images/s), et enregistre l'état de la scène.
// Chaque tour de boucle « répéter indéfiniment » correspond à une image, comme dans Scratch avec affichage.
// Usage : NODE_PATH=<node_modules avec scratch-vm et scratch-storage> node enregistrer_jeu.js jeu.sb3 frames.json catch|course|saut|maze [images_max]
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
  const item = T('الشيء') || T('سيارة معاكسة') || T('الشجيرة'), player = T('اللاعب') || T('السيارة') || T('الجمل') || T('الفأرة');
  let mouse = 0, keyL = false, keyR = false, seg = 0, segF = 0; const held = {};
  const key = (k, down) => vm.postIOData('keyboard', { key: k, isDown: down });
  rt.currentStepTime = 1000 / 30;                  // normalement fixé par vm.start() ; nécessaire pour que les scripts s'exécutent
  vm.greenFlag();
  for (let n = 0; n < maxN; n++) {
    const t = n / FPS;
    if (mode === 'catch') {                       // on suit le poisson 18 s, puis on s'écarte pour rater
      const target = t < 18 ? item.x : (item.x > 0 ? -200 : 200);
      mouse += Math.max(-14, Math.min(14, (target - mouse) * 0.22));
      vm.postIOData('mouse', { x: mouse + 240, y: 180, canvasWidth: 480, canvasHeight: 360, isDown: false });
    } else if (mode === 'saut') {                // saut : on appuie sur espace au bon moment pendant 20 s, ensuite on ne saute plus
      const dx = item.x - player.x, onGround = Math.abs(player.y + 95) < 1.5;
      const want = t < 20 && dx > 0 && dx <= 19 * val('السرعة') && onGround;
      if (want !== keyL) { key(' ', want); keyL = want; }
    } else if (mode === 'maze') {                // labyrinthe : pilote automatique (et un essai contre le premier mur)
      const SEG = [['x', -100], ['hold', 'up', 40], ['y', -130], ['x', 195], ['y', -15], ['x', -195], ['y', 75], ['x', 195], ['y', 150]];
      const s = SEG[Math.min(seg, SEG.length - 1)]; let want = null;
      if (s[0] === 'x') { const d = s[1] - player.x; if (Math.abs(d) <= 3) { seg++; segF = 0; } else want = d > 0 ? 'ArrowRight' : 'ArrowLeft'; }
      else if (s[0] === 'y') { const d = s[1] - player.y; if (Math.abs(d) <= 3) { seg++; segF = 0; } else want = d > 0 ? 'ArrowUp' : 'ArrowDown'; }
      else { if (segF++ < s[2]) want = 'ArrowUp'; else { seg++; segF = 0; } }
      for (const k of ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown']) { const on = k === want; if (on !== !!held[k]) { key(k, on); held[k] = on; } }
    } else {                                      // course : on évite des voitures pendant 24 s, puis on fonce dessus
      let want = 0;
      const safe = t < 24 && Math.abs(item.x - player.x) < 70 && item.y < 80 && item.y > -190;
      if (safe) want = item.x > player.x ? -1 : (item.x < player.x ? 1 : (player.x > 0 ? -1 : 1));
      else if (t >= 24) want = Math.abs(item.x - player.x) > 6 ? (item.x > player.x ? 1 : -1) : 0;
      else want = Math.abs(player.x) > 8 ? (player.x > 0 ? -1 : 1) : 0;
      if (want < 0 !== keyL || (want < 0) !== keyL) { }
      const L = want < 0, R = want > 0; if (L !== keyL) { key('ArrowLeft', L); keyL = L; } if (R !== keyR) { key('ArrowRight', R); keyR = R; }
    }
    clock += 1000 / FPS; rt._step();
    const sp = rt.targets.filter(x => x.sprite).map(x => ({ name: x.sprite.name, x: x.x, y: x.y, size: x.size, direction: x.direction, visible: x.visible, costume: x.currentCostume, say: said[x.sprite.name] || '' }));
    frames.push({ t, sp, score: val('النقاط'), lives: val('الأرواح'), speed: val('السرعة'), vars: Object.fromEntries(Object.values(stage.variables).map(v => [v.name, v.value])) });
    const over = mode === 'maze' ? /^(فزت|انتهى الوقت)/.test(said['الفأرة'] || '') : frames[frames.length - 1].lives < 1;
    if (over && n > FPS && ended < 0) ended = n;      // fin : on garde encore 3,5 s (message « انتهت اللعبة! »)
    if (ended >= 0 && n - ended > 3.5 * FPS) break;
  }
  fs.writeFileSync(out, JSON.stringify(frames)); Date.now = realNow;
  const l = frames[frames.length - 1]; console.log('images', frames.length, 'durée', (frames.length / FPS).toFixed(1), 's score', l.score, 'vies', l.lives, 'vitesse', l.speed);
  process.exit(0);
})();
