// Service worker : permet l'installation et l'utilisation hors connexion.
// Les fichiers déjà ouverts sont gardés en mémoire pour les prochaines fois.
const VERSION = "v1";
const CACHE = "ateliers-contes-" + VERSION;
const CORE = ["./", "./index.html", "./manifest.webmanifest", "./icones/icone-192.png", "./icones/icone-512.png"];

self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("ateliers-contes-") && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const r = e.request;
  if (r.method !== "GET" || new URL(r.url).origin !== location.origin || r.headers.has("range")) return;
  e.respondWith(caches.match(r, {ignoreSearch: true}).then(hit => {
    const net = fetch(r).then(res => { if (res.ok && res.status === 200) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(r, copy)); } return res; }).catch(() => hit);
    return hit || net;
  }));
});
