/* Garde l'appli et les photos sur le téléphone : on peut suivre un parcours sans réseau.
   Version __VERSION__ (change toute seule à chaque mise à jour des fresques). */
var CACHE = "artmada-__VERSION__";
var FICHIERS = __FICHIERS__;

self.addEventListener("install", function (ev) {
  ev.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(["./"].concat(FICHIERS).map(function (f) { return new Request(f, { cache: "reload" }); })); }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener("activate", function (ev) {
  ev.waitUntil(caches.keys().then(function (cles) {
    return Promise.all(cles.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener("fetch", function (ev) {
  var url = new URL(ev.request.url);
  if (ev.request.method !== "GET") return;
  if (url.origin !== location.origin) return;
  // Écrans, code et données : réseau d'abord (toujours la dernière version), sinon la copie gardée.
  // Photos, polices, icônes : la copie gardée d'abord (rapide, et marche sans réseau).
  var fixe = /\.(webp|png|jpg|woff2)$/.test(url.pathname);
  if (!fixe) {
    ev.respondWith(fetch(url.href, { cache: "no-cache" }).then(function (rep) {
      if (rep.ok) { var copie = rep.clone(); caches.open(CACHE).then(function (c) { c.put(ev.request, copie); }); }
      return rep;
    }).catch(function () {
      return caches.match(ev.request, { ignoreSearch: true }).then(function (r) { return r || caches.match("./"); });
    }));
    return;
  }
  ev.respondWith(caches.match(ev.request, { ignoreSearch: true }).then(function (r) { return r || fetch(ev.request); }));
});
