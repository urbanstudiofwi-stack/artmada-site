/* Garde l'appli et les photos sur le téléphone : on peut suivre un parcours sans réseau.
   Version __VERSION__ (change toute seule à chaque mise à jour des fresques). */
var CACHE = "artmada-__VERSION__";
var FICHIERS = __FICHIERS__;
var CARTE = "artmada-tuiles";

self.addEventListener("install", function (ev) {
  ev.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(["./"].concat(FICHIERS)); }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener("activate", function (ev) {
  ev.waitUntil(caches.keys().then(function (cles) {
    return Promise.all(cles.filter(function (k) { return k !== CACHE && k !== CARTE; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener("fetch", function (ev) {
  var url = new URL(ev.request.url);
  if (ev.request.method !== "GET") return;
  // Fonds de carte : on garde ceux déjà vus (500 max), pour la promenade sans réseau.
  if (url.hostname.indexOf("basemaps.cartocdn.com") >= 0) {
    ev.respondWith(caches.open(CARTE).then(function (c) {
      return c.match(ev.request).then(function (r) {
        var reseau = fetch(ev.request).then(function (rep) {
          c.put(ev.request, rep.clone());
          c.keys().then(function (k) { if (k.length > 500) c.delete(k[0]); });
          return rep;
        });
        return r || reseau;
      });
    }));
    return;
  }
  if (url.origin !== location.origin) return;
  // Données : réseau d'abord (fresques à jour), sinon la copie gardée.
  if (url.pathname.endsWith("donnees.json")) {
    ev.respondWith(fetch(ev.request).then(function (rep) {
      var copie = rep.clone(); caches.open(CACHE).then(function (c) { c.put(ev.request, copie); }); return rep;
    }).catch(function () { return caches.match(ev.request); }));
    return;
  }
  ev.respondWith(caches.match(ev.request, { ignoreSearch: true }).then(function (r) { return r || fetch(ev.request); }));
});
