// Service worker : permet l'installation et l'utilisation hors connexion.
// Les pages sont chargées depuis le réseau d'abord (la dernière version s'affiche toujours),
// puis depuis la mémoire si la connexion manque. Les autres fichiers sont gardés après leur première ouverture.
const VERSION = "v47";
const CACHE = "ateliers-contes-" + VERSION;
const CORE = ["./", "./index.html", "./manifest.webmanifest", "./videos.js", "./jeux.js", "./references.js", "./logiciels.js", "./icones/icone-192.png", "./icones/icone-512.png"];

self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("ateliers-contes-") && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
function save(r, res) { if (res.ok && res.status === 200) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(r, copy)); } return res; }
self.addEventListener("fetch", e => {
  const r = e.request;
  if (r.method !== "GET" || new URL(r.url).origin !== location.origin || r.headers.has("range")) return;
  const page = r.mode === "navigate" || /(\.html|\.js|\.webmanifest)$/.test(new URL(r.url).pathname) || new URL(r.url).pathname.endsWith("/");
  if (page) {
    e.respondWith(fetch(r, {cache: "no-cache"}).then(res => save(r, res)).catch(() => caches.match(r, {ignoreSearch: true})));
    return;
  }
  e.respondWith(caches.match(r, {ignoreSearch: true}).then(hit => hit || fetch(r).then(res => save(r, res))));
});
