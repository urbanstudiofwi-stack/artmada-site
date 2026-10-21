/* ARTMADA — l'appli du street art (V1 : carte, fiches, parcours, passeport).
   Une seule page ; chaque écran est dessiné à partir de donnees.json (fabriqué depuis les données du site). */
(function () {
  "use strict";

  var D = null;                 // données
  var F = {};                   // fresques par slug
  var vue = document.getElementById("vue");
  var carteLeaflet = null;      // carte affichée (une à la fois)
  var maPosition = null;        // [lat, lng] si l'utilisateur a accepté
  var etat = { filtre: "toutes", recherche: "", mode: "carte", choisie: null };
  var MODE_TEST = /[?&]test\b/.test(location.search);
  var CENTRE = [14.6055, -61.0665];
  var TUILES = "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png";
  var ATTRIB = '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> © <a href="https://carto.com/attributions">CARTO</a>';
  var SITE = "https://artmadastreetfestival.com/";

  /* ---------- petits outils ---------- */
  function e(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function ico(nom) {
    var p = {
      retour: '<path d="M15 6l-6 6 6 6"/>',
      fleche: '<path d="M9 6l6 6-6 6"/>',
      partager: '<path d="M12 3v12"/><path d="M7 8l5-5 5 5"/><path d="M5 13v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6"/>',
      aller: '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
      artiste: '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
      tampon: '<path d="M9 3h6v5l3 4H6l3-4z"/><path d="M4 16h16v3H4z"/>',
      ok: '<path d="M5 12l5 5 9-10"/>',
      viser: '<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/>',
      liste: '<path d="M8 6h13M8 12h13M8 18h13"/><circle cx="3.5" cy="6" r="1"/><circle cx="3.5" cy="12" r="1"/><circle cx="3.5" cy="18" r="1"/>',
      carte: '<path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2-6-2z"/><path d="M9 4v14M15 6v14"/>',
      chemin: '<circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M8 19h7a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h7"/>',
      chercher: '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
      pinceau: '<path d="M14 4l6 6-8 8H6v-6z"/><path d="M4 20l2-2"/>',
      groupe: '<circle cx="8" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M2 20c.8-3.5 3.2-5.5 6-5.5s5.2 2 6 5.5"/><path d="M14.5 15c2.6-.6 5.6.8 6.5 5"/>',
      insta: '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/>'
    }[nom] || "";
    return '<svg viewBox="0 0 24 24" aria-hidden="true">' + p + "</svg>";
  }
  function stock(cle, val) {
    try {
      if (val === undefined) return JSON.parse(localStorage.getItem(cle) || "null");
      localStorage.setItem(cle, JSON.stringify(val));
    } catch (x) { return null; }
  }
  function toast(txt) {
    var t = document.getElementById("toast");
    t.textContent = txt; t.hidden = false;
    clearTimeout(toast.minuteur);
    toast.minuteur = setTimeout(function () { t.hidden = true; }, 3200);
  }
  function km(a, b) {
    var r = 6371, toR = Math.PI / 180;
    var dLa = (b[0] - a[0]) * toR, dLo = (b[1] - a[1]) * toR;
    var h = Math.sin(dLa / 2) * Math.sin(dLa / 2) + Math.cos(a[0] * toR) * Math.cos(b[0] * toR) * Math.sin(dLo / 2) * Math.sin(dLo / 2);
    return 2 * r * Math.asin(Math.sqrt(h));
  }
  function distanceTexte(f) {
    if (!maPosition || !f.gps) return "";
    var d = km(maPosition, f.gps);
    return d < 1 ? "à " + Math.max(10, Math.round(d * 1000 / 10) * 10) + " m" : "à " + d.toFixed(1).replace(".", ",") + " km";
  }
  function photo(f, petite) {
    return f.photo ? "img/" + f.slug + (petite ? "-v" : "") + ".webp" : "";
  }
  function imgOuVide(f, petite, cls) {
    return f.photo
      ? '<img src="' + photo(f, petite) + '" alt="Fresque de ' + e(f.nom) + '" loading="lazy"' + (cls ? ' class="' + cls + '"' : "") + ">"
      : '<div class="sans-photo' + (cls ? " " + cls : "") + '">' + e(f.nom) + "</div>";
  }
  function edition(f) { return "ARTMADA #" + f.edition + " · " + f.annee; }
  function tampons() { return stock("artmada.tampons") || {}; }
  function tamponnable(f) { return !!f.gps && !f.disparue; }
  function aller(h) { location.hash = h; }

  /* ---------- position ---------- */
  function localiser(apres, silencieux) {
    if (!("geolocation" in navigator)) { if (!silencieux) toast("Ton téléphone ne donne pas sa position."); apres && apres(null); return; }
    navigator.geolocation.getCurrentPosition(function (p) {
      maPosition = [p.coords.latitude, p.coords.longitude];
      apres && apres(maPosition);
    }, function () {
      if (!silencieux) toast("Position refusée. Autorise la localisation dans les réglages du téléphone.");
      apres && apres(null);
    }, { enableHighAccuracy: true, timeout: 9000, maximumAge: 60000 });
  }

  /* ---------- navigation ---------- */
  function route() {
    var h = decodeURIComponent(location.hash.replace(/^#/, "")) || "accueil";
    var parts = h.split("/");
    if (carteLeaflet) { carteLeaflet.remove(); carteLeaflet = null; }
    var onglet = { accueil: "accueil", carte: "carte", f: "carte", parcours: "parcours", p: "parcours", passeport: "passeport" }[parts[0]] || "accueil";
    document.querySelectorAll(".onglets a").forEach(function (a) {
      if (a.dataset.onglet === onglet) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
    });
    if (parts[0] === "carte") pageCarte();
    else if (parts[0] === "f" && F[parts[1]]) pageFresque(F[parts[1]]);
    else if (parts[0] === "parcours") pageParcours();
    else if (parts[0] === "p") pageUnParcours(parts[1]);
    else if (parts[0] === "passeport") pagePasseport();
    else pageAccueil();
    vue.scrollTop = 0;
    if (!(parts[0] === "carte")) vue.focus({ preventScroll: true });
  }

  /* ---------- ACCUEIL ---------- */
  function compteARebours() {
    var auj = new Date(new Date().toLocaleString("en-US", { timeZone: "America/Martinique" }));
    auj.setHours(0, 0, 0, 0);
    var debut = new Date(D.festival.debut + "T00:00:00"), fin = new Date(D.festival.fin + "T00:00:00");
    var j = Math.round((debut - auj) / 86400000);
    if (j > 0) return '<span class="puce direct">J-' + j + "</span>";
    if (auj <= fin) return '<span class="puce direct">EN DIRECT</span>';
    return "";
  }
  function pageAccueil() {
    var une = D.fresques.filter(function (f) { return f.photo && f.edition === 2 && !f.disparue; });
    var star = F["xan-pointe-simon"] || une[0];
    var jour = Math.floor(Date.now() / 86400000);
    var avecTexte = D.fresques.filter(function (f) { return f.photo && f.texte && !f.disparue; });
    var duJour = avecTexte[jour % avecTexte.length];
    var surCarte = D.fresques.filter(function (f) { return f.gps; }).length;
    var tot = D.fresques.filter(tamponnable).length, faits = Object.keys(tampons()).filter(function (s) { return F[s]; }).length;
    var a = D.atelier;
    vue.innerHTML =
      '<div class="page">' +
      '<header class="entete"><div><img src="media/logo.webp" alt="ARTMADA Street Festival" width="150" height="72"><div class="lieu">STREET ART · MARTINIQUE</div></div>' +
      '<a class="rond" href="#passeport" aria-label="Mon passeport">' + ico("artiste") + "</a></header>" +

      '<a class="une" href="' + SITE + 'festival.html" target="_blank" rel="noopener">' +
      '<img src="' + photo(star) + '" alt="Fresque de ' + e(star.nom) + ', Pointe Simon">' +
      '<div class="haut">' + compteARebours() + "</div>" +
      '<div class="bas"><span class="surtitre" style="color:#E6E4DE">Édition #' + D.festival.edition + "</span>" +
      "<h1>ARTMADA #3 · " + e(D.festival.theme) + "</h1>" +
      '<span class="dates">25 janvier → 4 février 2027 · Fort-de-France</span></div></a>' +

      '<div class="duo">' +
      '<a class="tuile" href="#carte"><svg viewBox="0 0 24 24" stroke="#22C4C4" aria-hidden="true"><path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2-6-2z"/><path d="M9 4v14M15 6v14"/></svg>' +
      '<span class="chiffre">' + surCarte + "</span><b>Fresques sur la carte</b><span>Autour de toi</span></a>" +
      '<a class="tuile" href="#parcours"><svg viewBox="0 0 24 24" stroke="#FCD40D" aria-hidden="true"><circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M8 19h7a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h7"/></svg>' +
      '<span class="chiffre">' + D.parcours.length + "</span><b>Parcours à pied</b><span>Gratuits, à ton rythme</span></a>" +
      "</div>" +

      '<section style="display:flex;flex-direction:column;gap:10px"><div class="titre-section"><h2>La fresque du jour</h2><a href="#carte">Toutes</a></div>' +
      '<a class="ligne-carte" href="#f/' + duJour.slug + '">' + imgOuVide(duJour, true) +
      '<div class="txt"><span class="surtitre e' + duJour.edition + '">' + edition(duJour) + "</span><b>" + e(duJour.nom) + (duJour.titre ? " · " + e(duJour.titre) : "") + "</b><span>" + e(duJour.secteur || duJour.lieu) + "</span></div>" +
      '<svg class="fleche" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></a></section>' +

      '<section style="display:flex;flex-direction:column;gap:10px"><div class="titre-section"><h2>Peindre et visiter</h2></div>' +
      '<a class="ligne-carte" href="' + a.lien + '" target="_blank" rel="noopener">' + imgOuVide(F["doudou-style-tom-atlas"] || star, true) +
      '<div class="txt"><b>' + e(a.titre) + "</b><span>" + e(a.quand) + "</span><span>" + e(a.ou) + '</span><span class="prix">' + e(a.prix) + " · " + a.places + " places</span></div>" +
      '<span class="bouton" style="min-height:40px;padding:0 12px;font-size:14px">Réserver</span></a>' +
      '<a class="ligne-carte" href="' + SITE + 'visites.html" target="_blank" rel="noopener">' + imgOuVide(F["curtis-hylton-tom"] || star, true) +
      '<div class="txt"><b>Visite guidée en groupe</b><span>2 h à pied avec un guide</span><span class="prix">250 € le groupe · jusqu\'à 25 pers.</span></div>' +
      '<svg class="fleche" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></a></section>' +

      '<a class="ligne-carte" href="#passeport" style="padding:16px">' +
      '<div class="txt"><span class="surtitre" style="color:var(--turquoise)">Mon passeport</span><b>' + faits + " fresque" + (faits > 1 ? "s" : "") + " tamponnée" + (faits > 1 ? "s" : "") + " sur " + tot + "</b>" +
      '<div class="jauge" style="margin-top:6px"><i style="width:' + Math.round(faits / tot * 100) + '%"></i></div></div>' +
      '<svg class="fleche" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></a>' +

      '<div class="troisieme"><span class="surtitre" style="color:var(--magenta)">Bientôt</span><h2>Les murs d\'ARTMADA #3</h2>' +
      '<p class="petit" style="color:#E6E4DE">Les nouvelles fresques arrivent sur la carte pendant le festival, du 25 janvier au 4 février 2027.</p></div>' +

      '<p class="note">Version de test · ARTMADA Street Festival, porté par l\'association NPL MADA PAINT · <a href="' + SITE + '" target="_blank" rel="noopener">artmadastreetfestival.com</a></p>' +
      "</div>";
  }

  /* ---------- CARTE ---------- */
  function fresquesFiltrees() {
    var q = etat.recherche.trim().toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
    var t = tampons();
    return D.fresques.filter(function (f) {
      if (etat.filtre === "e2" && f.edition !== 2) return false;
      if (etat.filtre === "e1" && f.edition !== 1) return false;
      if (etat.filtre === "atamponner" && (!tamponnable(f) || t[f.slug])) return false;
      if (!q) return true;
      var txt = (f.nom + " " + f.titre + " " + f.lieu + " " + f.secteur + " " + f.ville).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
      return txt.indexOf(q) >= 0;
    });
  }
  function pageCarte() {
    var filtres = [["toutes", "Toutes"], ["e2", "ARTMADA #2 · 2026"], ["e1", "ARTMADA #1 · 2024"], ["atamponner", "Pas encore tamponnées"]];
    var tete =
      '<div class="recherche">' + ico("chercher") + '<label class="sr" for="cherche">Rechercher</label>' +
      '<input id="cherche" type="search" placeholder="Une fresque, un artiste, un quartier" value="' + e(etat.recherche) + '" autocomplete="off"></div>' +
      '<div class="puces" role="group" aria-label="Filtrer">' + filtres.map(function (x) {
        return '<button type="button" class="filtre" data-filtre="' + x[0] + '" aria-pressed="' + (etat.filtre === x[0]) + '">' + x[1] + "</button>";
      }).join("") + "</div>" +
      '<div class="bascule" role="group" aria-label="Affichage"><button type="button" data-mode="carte" aria-pressed="' + (etat.mode === "carte") + '">Carte</button>' +
      '<button type="button" data-mode="liste" aria-pressed="' + (etat.mode === "liste") + '">Liste</button></div>';

    if (etat.mode === "liste") {
      vue.innerHTML = '<div class="page"><h1 style="font-size:36px">Les fresques</h1>' + tete + '<div id="liste" class="liste-fresques"></div></div>';
      dessinerListe();
    } else {
      vue.innerHTML = '<div class="page-carte"><div id="carte" role="application" aria-label="Carte des fresques"></div>' +
        '<div class="carte-haut">' + tete + "</div>" +
        '<div class="carte-actions" id="actions"><button type="button" class="flottant" id="localiser" aria-label="Me localiser">' + ico("viser") + "</button></div>" +
        '<div id="flottante"></div></div>';
      dessinerCarte();
    }
    var champ = document.getElementById("cherche");
    champ.addEventListener("input", function () {
      etat.recherche = champ.value;
      etat.mode === "liste" ? dessinerListe() : dessinerMarqueurs();
    });
    vue.querySelectorAll("[data-filtre]").forEach(function (b) {
      b.addEventListener("click", function () {
        etat.filtre = b.dataset.filtre;
        vue.querySelectorAll("[data-filtre]").forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
        etat.mode === "liste" ? dessinerListe() : dessinerMarqueurs();
      });
    });
    vue.querySelectorAll("[data-mode]").forEach(function (b) {
      b.addEventListener("click", function () { if (etat.mode !== b.dataset.mode) { etat.mode = b.dataset.mode; route(); } });
    });
  }

  function dessinerListe() {
    var liste = fresquesFiltrees(), t = tampons();
    if (maPosition) liste.sort(function (a, b) { return (a.gps ? km(maPosition, a.gps) : 999) - (b.gps ? km(maPosition, b.gps) : 999); });
    var el = document.getElementById("liste");
    el.innerHTML = liste.length ? liste.map(function (f) {
      var info = f.disparue ? "Fresque disparue" : (distanceTexte(f) || (f.gps ? f.secteur || f.ville : "Pas encore sur la carte"));
      return '<a class="vignette" href="#f/' + f.slug + '"><div class="ph">' + imgOuVide(f, false) +
        '<span class="puce e' + f.edition + '">#' + f.edition + "</span>" +
        (t[f.slug] ? '<span class="ok" aria-label="Tamponnée">' + ico("ok") + "</span>" : "") +
        "</div><b>" + e(f.nom) + "</b><span>" + e(info) + "</span></a>";
    }).join("") : '<p class="gris">Aucune fresque ne correspond.</p>';
  }

  var calqueMarqueurs = null;
  function dessinerCarte() {
    carteLeaflet = L.map("carte", { zoomControl: false, attributionControl: true }).setView(CENTRE, 15);
    L.tileLayer(TUILES, { maxZoom: 19, subdomains: "abcd", attribution: ATTRIB, detectRetina: false }).addTo(carteLeaflet);
    calqueMarqueurs = L.layerGroup().addTo(carteLeaflet);
    dessinerMarqueurs(true);
    var pos = null;
    function poserMoi() {
      if (!maPosition) return;
      if (pos) pos.setLatLng(maPosition);
      else pos = L.marker(maPosition, { icon: L.divIcon({ className: "", html: '<div class="moi"></div>', iconSize: [18, 18] }), interactive: false, zIndexOffset: 1000 }).addTo(carteLeaflet);
    }
    poserMoi();
    document.getElementById("localiser").addEventListener("click", function () {
      localiser(function (p) {
        if (!p || !carteLeaflet) return;
        poserMoi();
        carteLeaflet.flyTo(p, 16);
        if (etat.choisie) montrerFlottante(F[etat.choisie]);
      });
    });
    carteLeaflet.on("click", function () { etat.choisie = null; montrerFlottante(null); dessinerMarqueurs(); });
    if (etat.choisie && F[etat.choisie]) montrerFlottante(F[etat.choisie]);
  }

  function dessinerMarqueurs(cadrer) {
    if (!carteLeaflet) return;
    calqueMarqueurs.clearLayers();
    var t = tampons();
    var liste = fresquesFiltrees().filter(function (f) { return f.gps; });
    liste.forEach(function (f) {
      var cls = "pin e" + f.edition + (t[f.slug] ? " tamponne" : "") + (etat.choisie === f.slug ? " choisi" : "");
      var html = '<span class="' + cls + '">' + (f.photo ? '<img src="' + photo(f, true) + '" alt="">' : '<span class="num">' + e(f.nom.charAt(0)) + "</span>") + "</span>";
      var m = L.marker(f.gps, {
        icon: L.divIcon({ className: "", html: html, iconSize: [46, 46], iconAnchor: [23, 23] }),
        title: f.nom, alt: "Fresque de " + f.nom, keyboard: true, riseOnHover: true,
        zIndexOffset: etat.choisie === f.slug ? 500 : 0
      });
      m.on("click", function (ev) {
        L.DomEvent.stopPropagation(ev);
        etat.choisie = f.slug; dessinerMarqueurs(); montrerFlottante(f);
      });
      m.addTo(calqueMarqueurs);
    });
    if (cadrer) {
      var proches = liste.filter(function (f) { return km(CENTRE, f.gps) < 4; });
      if (proches.length > 1) carteLeaflet.fitBounds(L.latLngBounds(proches.map(function (f) { return f.gps; })), { paddingTopLeft: [30, 170], paddingBottomRight: [30, 40] });
    }
  }

  function montrerFlottante(f) {
    var el = document.getElementById("flottante");
    var actions = document.getElementById("actions");
    if (!el) return;
    if (!f) { el.innerHTML = ""; actions.classList.remove("haut"); return; }
    actions.classList.add("haut");
    el.innerHTML = '<a class="ligne-carte fiche-flottante" href="#f/' + f.slug + '">' + imgOuVide(f, true) +
      '<div class="txt"><span class="surtitre e' + f.edition + '">' + edition(f) + '</span><span class="nom">' + e(f.nom) + "</span>" +
      "<span>" + e(f.titre ? f.titre : f.secteur || f.lieu) + (distanceTexte(f) ? " · " + distanceTexte(f) : "") + "</span></div>" +
      '<svg class="fleche" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></a>';
  }

  /* ---------- FICHE D'UNE FRESQUE ---------- */
  function paragraphes(txt) {
    return txt.split(/\n+/).filter(Boolean).map(function (p) { return "<p>" + e(p) + "</p>"; }).join("");
  }
  function pageFresque(f) {
    var t = tampons();
    var artistes = f.artistes.map(function (s) { return [s, D.artistes[s]]; }).filter(function (x) { return x[1]; });
    var lieu = [f.lieu, f.ville].filter(Boolean).join(", ");
    var voisines = f.gps ? D.fresques.filter(function (x) { return x.gps && x.slug !== f.slug && !x.disparue; })
      .sort(function (a, b) { return km(f.gps, a.gps) - km(f.gps, b.gps); }).slice(0, 4) : [];

    vue.innerHTML =
      '<div class="page">' +
      '<div class="fiche-photo">' + (f.photo ? '<img src="' + photo(f) + '" alt="Fresque de ' + e(f.nom) + ", " + e(lieu) + '">' : '<div class="sans-photo">' + e(f.nom) + "</div>") +
      '<div class="boutons"><button type="button" class="rond" id="retour" aria-label="Retour">' + ico("retour") + "</button>" +
      '<button type="button" class="rond" id="partager" aria-label="Partager">' + ico("partager") + "</button></div>" +
      (f.photo && f.credit ? '<span class="credit">Photo : ' + e(f.credit) + "</span>" : "") + "</div>" +

      '<div class="fiche-tete"><span class="surtitre e' + f.edition + '">' + edition(f) + (f.collectif ? " · fresque collective" : "") + "</span>" +
      "<h1>" + e(f.nom) + "</h1>" +
      (f.titre ? '<span class="oeuvre">« ' + e(f.titre) + " »</span>" : "") +
      '<span class="gris">' + e(lieu) + (distanceTexte(f) ? " · " + distanceTexte(f) : "") + "</span>" +
      (f.disparue ? '<span><span class="puce disparue">Fresque disparue</span></span>' : "") + "</div>" +

      '<div class="trio">' +
      '<a href="' + e(f.y_aller) + '" target="_blank" rel="noopener">' + ico("aller") + "Y aller à pied</a>" +
      (artistes.length ? '<button type="button" id="voir-artiste">' + ico("artiste") + (artistes.length > 1 ? "Les artistes" : "L'artiste") + "</button>" : '<a href="#carte">' + ico("carte") + "La carte</a>") +
      '<button type="button" id="partager2">' + ico("partager") + "Partager</button></div>" +

      (tamponnable(f) ? '<button type="button" id="tamponner" class="tamponner' + (t[f.slug] ? " fait" : "") + '"></button>' : "") +

      '<section class="histoire"><span class="surtitre">L\'histoire de la fresque</span>' +
      (f.texte ? '<div id="texte-fr" class="histoire">' + paragraphes(f.texte) + "</div>" +
        (f.texte_en ? '<div id="texte-en" class="histoire" lang="en" hidden>' + paragraphes(f.texte_en) + "</div>" +
          '<button type="button" class="lien-texte" id="langue">Read in English</button>' : "")
        : '<p class="gris">Le texte de cette fresque arrive bientôt.</p>') + "</section>" +

      artistes.map(function (x) {
        var a = x[1];
        return '<section class="bloc artiste" id="artiste-' + x[0] + '"><span class="surtitre">' + (a.collectif ? "Collectif " + e(a.collectif) + " · " : "") + e(a.origine) + "</span>" +
          "<h3>" + e(a.nom) + "</h3>" + (a.bio ? "<p>" + e(a.bio) + "</p>" : "") +
          (a.instagram ? '<a class="bouton contour" style="align-self:flex-start" href="https://www.instagram.com/' + e(a.instagram) + '/" target="_blank" rel="noopener">' + ico("insta") + "@" + e(a.instagram) + "</a>" : "") +
          "</section>";
      }).join("") +

      '<dl class="infos"><dt>Édition</dt><dd>' + edition(f) + "</dd><dt>Lieu</dt><dd>" + e(f.lieu) + "</dd>" +
      (f.secteur && f.secteur !== f.lieu ? "<dt>Quartier</dt><dd>" + e(f.secteur) + "</dd>" : "") +
      "<dt>Ville</dt><dd>" + e(f.ville) + "</dd>" +
      (f.surface ? "<dt>Surface</dt><dd>" + e(f.surface) + " m²</dd>" : "") + "</dl>" +

      (voisines.length ? '<section style="display:flex;flex-direction:column;gap:12px"><div class="titre-section"><h2>Juste à côté</h2></div><div class="liste-fresques">' +
        voisines.map(function (v) {
          var d = km(f.gps, v.gps);
          return '<a class="vignette" href="#f/' + v.slug + '"><div class="ph">' + imgOuVide(v, false) + '<span class="puce e' + v.edition + '">#' + v.edition + "</span></div><b>" + e(v.nom) + "</b><span>" +
            (d < 1 ? Math.max(10, Math.round(d * 100) * 10) + " m" : d.toFixed(1).replace(".", ",") + " km") + " d'ici</span></a>";
        }).join("") + "</div></section>" : "") +
      "</div>";

    document.getElementById("retour").addEventListener("click", function () {
      if (route.precedente) history.back(); else aller("carte");
    });
    function partager() {
      var url = location.href.split("#")[0] + "#f/" + f.slug;
      var data = { title: "ARTMADA · " + f.nom, text: "La fresque de " + f.nom + " à " + f.ville + " (ARTMADA #" + f.edition + ")", url: url };
      if (navigator.share) navigator.share(data).catch(function () {});
      else if (navigator.clipboard) navigator.clipboard.writeText(url).then(function () { toast("Lien copié"); }, function () { toast(url); });
      else toast(url);
    }
    document.getElementById("partager").addEventListener("click", partager);
    document.getElementById("partager2").addEventListener("click", partager);
    var va = document.getElementById("voir-artiste");
    if (va) va.addEventListener("click", function () {
      document.getElementById("artiste-" + artistes[0][0]).scrollIntoView({ behavior: "smooth", block: "start" });
    });
    var lg = document.getElementById("langue");
    if (lg) lg.addEventListener("click", function () {
      var fr = document.getElementById("texte-fr"), en = document.getElementById("texte-en");
      var versEn = en.hidden; en.hidden = !versEn; fr.hidden = versEn;
      lg.textContent = versEn ? "Lire en français" : "Read in English";
    });
    var bt = document.getElementById("tamponner");
    if (bt) { dessinerTampon(bt, f); bt.addEventListener("click", function () { tamponner(bt, f); }); }
  }

  function dessinerTampon(bt, f, message) {
    var t = tampons(), total = D.fresques.filter(tamponnable).length, n = Object.keys(t).filter(function (s) { return F[s]; }).length;
    bt.classList.remove("loin");
    if (t[f.slug]) {
      bt.className = "tamponner fait";
      bt.innerHTML = ico("ok") + "<span><b>Tamponnée ! " + n + " fresque" + (n > 1 ? "s" : "") + " sur " + total + "</b><span>Le " + new Date(t[f.slug]).toLocaleDateString("fr-FR") + " · voir mon passeport</span></span>";
    } else if (message) {
      bt.className = "tamponner loin";
      bt.innerHTML = ico("aller") + "<span><b>" + e(message[0]) + "</b><span>" + e(message[1]) + "</span></span>";
    } else {
      bt.className = "tamponner";
      bt.innerHTML = ico("tampon") + "<span><b>Je suis devant : tamponner</b><span>Ajoute cette fresque à ton passeport</span></span>";
    }
  }
  function tamponner(bt, f) {
    var t = tampons();
    if (t[f.slug]) { aller("passeport"); return; }
    function valider() {
      t[f.slug] = new Date().toISOString(); stock("artmada.tampons", t);
      dessinerTampon(bt, f); toast("Tamponnée !");
    }
    if (MODE_TEST) { valider(); return; }
    bt.innerHTML = ico("viser") + "<span><b>Je vérifie que tu es devant…</b><span>Position en cours</span></span>";
    localiser(function (p) {
      if (!p) { dessinerTampon(bt, f, ["Active ta localisation", "Elle sert seulement à vérifier que tu es devant le mur."]); return; }
      var d = km(p, f.gps);
      if (d <= 0.25) valider();
      else dessinerTampon(bt, f, ["Tu es " + distanceTexte(f), "Approche-toi du mur pour tamponner (moins de 250 m)."]);
    }, true);
  }

  /* ---------- PARCOURS ---------- */
  function mosaique(p) {
    var avec = p.etapes.map(function (s) { return F[s]; }).filter(function (f) { return f.photo; });
    return '<div class="mosaique">' + avec.slice(0, 3).map(function (f) { return '<img src="' + photo(f) + '" alt="" loading="lazy">'; }).join("") + "</div>";
  }
  function pageParcours() {
    var t = tampons();
    vue.innerHTML = '<div class="page"><h1 style="font-size:40px">Parcours</h1>' +
      '<p class="gris" style="margin-top:-8px">Gratuits, à pied, à ton rythme. Suis la carte dans l\'appli ou lance Google Maps.</p>' +
      D.parcours.map(function (p) {
        var faits = p.etapes.filter(function (s) { return t[s]; }).length;
        return '<article class="bloc parcours-carte">' + mosaique(p) + '<div class="corps">' +
          '<span class="surtitre ' + (p.editions.length === 1 ? "e" + p.editions[0] : "") + '">' + p.editions.map(function (x) { return "ARTMADA #" + x; }).join(" + ") + "</span>" +
          "<h2>" + e(p.titre) + "</h2><p>" + e(p.texte) + "</p>" +
          '<div class="pied"><div class="mesures"><span><b>' + p.etapes.length + "</b> fresques</span><span>≈ <b>" + String(p.km).replace(".", ",") + "</b> km</span><span>≈ <b>" + p.minutes + "</b> min</span></div>" +
          '<a class="bouton" href="#p/' + p.cle + '">Partir</a></div>' +
          (faits ? '<span class="petit" style="color:var(--turquoise);font-weight:700">' + faits + " sur " + p.etapes.length + " déjà tamponnée" + (faits > 1 ? "s" : "") + "</span>" : "") +
          "</div></article>";
      }).join("") +
      '<section style="display:flex;flex-direction:column;gap:10px;margin-top:6px"><div class="titre-section"><h2>Avec un guide</h2></div>' +
      '<a class="ligne-carte" href="' + SITE + 'visites.html" target="_blank" rel="noopener"><span class="rond" style="background:var(--beton-clair)">' + ico("groupe") + "</span>" +
      '<div class="txt"><b>Visite guidée en groupe</b><span>2 h à pied</span><span class="prix">250 € le groupe · jusqu\'à 25 pers.</span></div><svg class="fleche" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></a>' +
      '<a class="ligne-carte" href="' + D.atelier.lien + '" target="_blank" rel="noopener"><span class="rond" style="background:var(--beton-clair)">' + ico("pinceau") + "</span>" +
      '<div class="txt"><b>Envie de peindre ?</b><span>' + e(D.atelier.quand) + ' · Urban Studio, Trois-Îlets</span><span class="prix">' + e(D.atelier.prix) + "</span></div><svg class=\"fleche\" viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"M9 6l6 6-6 6\"/></svg></a></section>" +
      "</div>";
  }

  function pageUnParcours(cle) {
    var p = D.parcours.filter(function (x) { return x.cle === cle; })[0];
    if (!p) { aller("parcours"); return; }
    var t = tampons();
    var etapes = p.etapes.map(function (s) { return F[s]; });
    vue.innerHTML = '<div class="page">' +
      '<div style="display:flex;align-items:center;gap:12px"><a class="rond" href="#parcours" aria-label="Retour aux parcours">' + ico("retour") + "</a>" +
      '<span class="surtitre">Parcours à pied</span></div>' +
      '<h1 style="font-size:clamp(32px,9vw,44px)">' + e(p.titre) + "</h1>" +
      '<div class="mesures"><span><b>' + p.etapes.length + "</b> fresques</span><span>≈ <b>" + String(p.km).replace(".", ",") + "</b> km</span><span>≈ <b>" + p.minutes + "</b> min de marche</span></div>" +
      '<div class="carte-parcours"><div id="carte" style="position:absolute;inset:0" role="application" aria-label="Carte du parcours"></div></div>' +
      '<a class="bouton" href="' + e(p.url) + '" target="_blank" rel="noopener">' + ico("chemin") + "Lancer dans Google Maps (à pied)</a>" +
      '<p class="note" style="margin-top:-10px">Sur la carte, le trait relie les étapes dans l\'ordre. Google Maps te donne le vrai chemin dans les rues.</p>' +
      '<ol class="etapes">' + etapes.map(function (f, i) {
        return '<li><span class="n' + (t[f.slug] ? " ok" : "") + '">' + (i + 1) + '</span><a class="ligne-carte" href="#f/' + f.slug + '" style="padding:8px">' + imgOuVide(f, true) +
          '<div class="txt"><b>' + e(f.nom) + "</b><span>" + e(f.titre || f.lieu) + "</span>" +
          (t[f.slug] ? '<span style="color:var(--turquoise);font-weight:700">Tamponnée</span>' : "") + "</div></a></li>";
      }).join("") + "</ol></div>";

    carteLeaflet = L.map("carte", { zoomControl: false, scrollWheelZoom: false }).setView(etapes[0].gps, 15);
    L.tileLayer(TUILES, { maxZoom: 19, subdomains: "abcd", attribution: ATTRIB }).addTo(carteLeaflet);
    L.polyline(etapes.map(function (f) { return f.gps; }), { color: "#EB782F", weight: 4, opacity: .9, dashArray: "2 9", lineCap: "round" }).addTo(carteLeaflet);
    etapes.forEach(function (f, i) {
      L.marker(f.gps, { icon: L.divIcon({ className: "", html: '<span class="pin-etape">' + (i + 1) + "</span>", iconSize: [34, 34], iconAnchor: [17, 17] }), title: f.nom })
        .on("click", function () { aller("f/" + f.slug); }).addTo(carteLeaflet);
    });
    carteLeaflet.fitBounds(L.latLngBounds(etapes.map(function (f) { return f.gps; })), { padding: [34, 34] });
  }

  /* ---------- PASSEPORT ---------- */
  function pagePasseport() {
    var t = tampons();
    var liste = D.fresques.filter(tamponnable);
    var faits = liste.filter(function (f) { return t[f.slug]; });
    liste.sort(function (a, b) { return (t[b.slug] ? 1 : 0) - (t[a.slug] ? 1 : 0) || (t[a.slug] || "").localeCompare(t[b.slug] || ""); });
    vue.innerHTML = '<div class="page"><h1 style="font-size:40px">Mon passeport</h1>' +
      '<div class="bloc passeport-tete"><span class="surtitre" style="color:var(--turquoise)">Fresques tamponnées</span>' +
      '<div style="display:flex;align-items:baseline;gap:8px"><span class="chiffre" style="font-size:52px">' + faits.length + '</span><span class="gris" style="font-size:18px">sur ' + liste.length + "</span></div>" +
      '<div class="jauge"><i style="width:' + Math.round(faits.length / liste.length * 100) + '%"></i></div>' +
      '<p class="petit" style="color:#E6E4DE">Va devant une fresque, ouvre sa fiche et appuie sur « Je suis devant : tamponner ». Ta position sert seulement à vérifier que tu es devant le mur.</p></div>' +
      '<div class="grille-tampons">' + liste.map(function (f) {
        return '<a class="tampon' + (t[f.slug] ? " ok" : "") + '" href="#f/' + f.slug + '" aria-label="' + e(f.nom) + (t[f.slug] ? ", tamponnée" : ", pas encore tamponnée") + '">' +
          (f.photo ? '<img src="' + photo(f, true) + '" alt="" loading="lazy">' : "") + '<span class="q">' + e(f.nom) + "</span></a>";
      }).join("") + "</div>" +
      '<p class="note">Ton passeport est gardé sur ce téléphone. Bientôt : un compte pour le retrouver sur tous tes appareils.</p>' +
      (MODE_TEST && faits.length ? '<button type="button" class="bouton contour" id="raz">Mode test : vider le passeport</button>' : "") +
      "</div>";
    var raz = document.getElementById("raz");
    if (raz) raz.addEventListener("click", function () { stock("artmada.tampons", {}); route(); toast("Passeport vidé"); });
  }

  /* ---------- démarrage ---------- */
  fetch("donnees.json").then(function (r) { return r.json(); }).then(function (d) {
    D = d;
    D.fresques.forEach(function (f) { F[f.slug] = f; });
    window.addEventListener("hashchange", function () { route.precedente = true; route(); });
    route();
    // Position silencieuse si déjà autorisée (pour afficher les distances)
    if (navigator.permissions && navigator.permissions.query) {
      navigator.permissions.query({ name: "geolocation" }).then(function (s) {
        if (s.state === "granted") localiser(function () { if (/^#?(carte|f\/)/.test(location.hash.replace("#", ""))) { /* distances affichées au prochain écran */ } }, true);
      }).catch(function () {});
    }
  }).catch(function () {
    vue.innerHTML = '<div class="page"><h1>Oups</h1><p>Impossible de charger les fresques. Vérifie ta connexion puis rouvre l\'appli.</p></div>';
  });

  if ("serviceWorker" in navigator && location.protocol === "https:") {
    window.addEventListener("load", function () { navigator.serviceWorker.register("sw.js").catch(function () {}); });
  }
})();
