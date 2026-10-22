/* Garde l'appli et les photos sur le téléphone : on peut suivre un parcours sans réseau.
   Version 0d723be2f3 (change toute seule à chaque mise à jour des fresques). */
var CACHE = "artmada-0d723be2f3";
var FICHIERS = ["app.css", "app.js", "donnees.json", "fonts/anton-latin-400-normal.woff2", "fonts/dm-sans-latin-400-normal.woff2", "fonts/dm-sans-latin-500-normal.woff2", "fonts/dm-sans-latin-700-normal.woff2", "img/aurelie-argyre-perrinon-v.webp", "img/aurelie-argyre-perrinon.webp", "img/box-vincent-canal-alaric-v.webp", "img/box-vincent-canal-alaric.webp", "img/carole-b-terres-sainville-v.webp", "img/carole-b-terres-sainville.webp", "img/curtis-hylton-tom-v.webp", "img/curtis-hylton-tom.webp", "img/doudou-style-tom-atlas-v.webp", "img/doudou-style-tom-atlas.webp", "img/jaddict-cour-perrinon-v.webp", "img/jaddict-cour-perrinon.webp", "img/jaddict-mairie-v.webp", "img/jaddict-mairie.webp", "img/james-canal-alaric-v.webp", "img/james-canal-alaric.webp", "img/kaldea-langellier-v.webp", "img/kaldea-langellier.webp", "img/magiic-dillon-v.webp", "img/magiic-dillon.webp", "img/magiic-rman-clarac-v.webp", "img/magiic-rman-clarac.webp", "img/mounlan-floreal-v.webp", "img/mounlan-floreal.webp", "img/mounlan-tom-v.webp", "img/mounlan-tom.webp", "img/mur-de-la-jam-v.webp", "img/mur-de-la-jam.webp", "img/none-maurice-bishop-v.webp", "img/none-maurice-bishop.webp", "img/onine-pointe-simon-v.webp", "img/onine-pointe-simon.webp", "img/oshea-maurice-bishop-v.webp", "img/oshea-maurice-bishop.webp", "img/oshea-tom-v.webp", "img/oshea-tom.webp", "img/pacman-canal-alaric-v.webp", "img/pacman-canal-alaric.webp", "img/rayza-canal-alaric-v.webp", "img/rayza-canal-alaric.webp", "img/roxane-shade-isambert-v.webp", "img/roxane-shade-isambert.webp", "img/saveur-grafikk-perrinon-v.webp", "img/saveur-grafikk-perrinon.webp", "img/sitou-pointe-simon-v.webp", "img/sitou-pointe-simon.webp", "img/socabohm-maurice-bishop-v.webp", "img/socabohm-maurice-bishop.webp", "img/steek-dillon-v.webp", "img/steek-dillon.webp", "img/temponok-pointe-simon-v.webp", "img/temponok-pointe-simon.webp", "img/veneno-saliniere-v.webp", "img/veneno-saliniere.webp", "img/wuna-bo-kannal-v.webp", "img/wuna-bo-kannal.webp", "img/xan-breeze-yoko-olympia-v.webp", "img/xan-breeze-yoko-olympia.webp", "img/xan-pointe-simon-v.webp", "img/xan-pointe-simon.webp", "img/yelow-tom-v.webp", "img/yelow-tom.webp", "img/zeben-clarac-v.webp", "img/zeben-clarac.webp", "index.html", "manifest.webmanifest", "media/apple-touch-icon.png", "media/beton.webp", "media/icon-192.png", "media/icon-512.png", "media/logo.webp", "vendor/leaflet.css", "vendor/leaflet.js"];

self.addEventListener("install", function (ev) {
  ev.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(["./"].concat(FICHIERS)); }).then(function () { return self.skipWaiting(); }));
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
  // Données : réseau d'abord (fresques à jour), sinon la copie gardée.
  if (url.pathname.endsWith("donnees.json")) {
    ev.respondWith(fetch(ev.request).then(function (rep) {
      var copie = rep.clone(); caches.open(CACHE).then(function (c) { c.put(ev.request, copie); }); return rep;
    }).catch(function () { return caches.match(ev.request); }));
    return;
  }
  ev.respondWith(caches.match(ev.request, { ignoreSearch: true }).then(function (r) { return r || fetch(ev.request); }));
});
