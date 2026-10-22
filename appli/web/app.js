/* ARTMADA — l'appli du street art.
   V1 : carte des fresques, fiches, parcours à pied, passeport à tampons, festival #3 (+ aperçu du mode direct),
   inscription bénévole, français / anglais.
   Une seule page ; chaque écran est dessiné à partir de donnees.json (fabriqué depuis les données du site). */
(function () {
  "use strict";

  var D = null;                 // données
  var F = {};                   // fresques par slug
  var vue = document.getElementById("vue");
  var carteLeaflet = null;      // carte affichée (une à la fois)
  var maPosition = null;        // [lat, lng] si l'utilisateur a accepté
  var etat = { filtre: "toutes", recherche: "", mode: "carte", choisie: null, jourDirect: 0, texteTheme: false };
  var MODE_TEST = /[?&]test\b/.test(location.search);
  var CENTRE = [14.6055, -61.0665];
  var TUILES = "https://tile.openstreetmap.org/{z}/{x}/{y}.png";
  var ATTRIB = '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>';
  var SITE = "https://artmadastreetfestival.com/";
  var invitationInstall = null; // Android : proposition d'installation

  /* ---------- langue ---------- */
  var LANGUE = (function () {
    var l = null;
    try { l = localStorage.getItem("artmada.langue"); } catch (x) {}
    var p = location.search.match(/[?&]lang=(fr|en)/);
    if (p) l = p[1];
    if (l !== "fr" && l !== "en") l = /^fr/i.test(navigator.language || "fr") ? "fr" : "en";
    return l;
  })();
  function T(fr, en) { return LANGUE === "en" ? en : fr; }
  function C(obj, cle) { return (LANGUE === "en" && obj[cle + "_en"]) ? obj[cle + "_en"] : (obj[cle] || ""); }
  function changerLangue() {
    LANGUE = LANGUE === "fr" ? "en" : "fr";
    try { localStorage.setItem("artmada.langue", LANGUE); } catch (x) {}
    document.documentElement.lang = LANGUE;
    dessinerOnglets(); route();
  }

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
      carte: '<path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2-6-2z"/><path d="M9 4v14M15 6v14"/>',
      chemin: '<circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M8 19h7a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h7"/>',
      chercher: '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
      pinceau: '<path d="M14 4l6 6-8 8H6v-6z"/><path d="M4 20l2-2"/>',
      groupe: '<circle cx="8" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M2 20c.8-3.5 3.2-5.5 6-5.5s5.2 2 6 5.5"/><path d="M14.5 15c2.6-.6 5.6.8 6.5 5"/>',
      insta: '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/>',
      accueil: '<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z"/>',
      passeport: '<rect x="5" y="3" width="14" height="18" rx="2"/><circle cx="12" cy="10" r="3"/><path d="M9 17h6"/>',
      festival: '<path d="M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.4 6.7 19.4l1.2-6L3.4 9.3l6-.7z"/>',
      main: '<path d="M7 11V6a2 2 0 0 1 4 0v4"/><path d="M11 10V4a2 2 0 0 1 4 0v6"/><path d="M15 10V6a2 2 0 0 1 4 0v8a7 7 0 0 1-7 7h-1a6 6 0 0 1-5-2.7L3.5 14a2 2 0 0 1 3.2-2.4L7 12"/>',
      ajouter: '<rect x="4" y="4" width="16" height="16" rx="4"/><path d="M12 8v8M8 12h8"/>',
      fermer: '<path d="M6 6l12 12M18 6L6 18"/>',
      mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
      copier: '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"/>'
    }[nom] || "";
    return '<svg viewBox="0 0 24 24" aria-hidden="true">' + p + "</svg>";
  }
  var FLECHE = '<svg class="fleche" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>';
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
  function nombre(x, dec) {
    var s = x.toFixed(dec);
    return LANGUE === "fr" ? s.replace(".", ",") : s;
  }
  function distanceBrute(d) {
    return d < 1 ? Math.max(10, Math.round(d * 100) * 10) + " m" : nombre(d, 1) + " km";
  }
  function distanceTexte(f) {
    if (!maPosition || !f.gps) return "";
    var d = distanceBrute(km(maPosition, f.gps));
    return T("à " + d, d + " away");
  }
  function photo(f, petite) {
    return f.photo ? "img/" + f.slug + (petite ? "-v" : "") + ".webp" : "";
  }
  function altFresque(f) { return T("Fresque de ", "Mural by ") + f.nom; }
  function imgOuVide(f, petite) {
    return f.photo
      ? '<img src="' + photo(f, petite) + '" alt="' + e(altFresque(f)) + '" loading="lazy">'
      : '<div class="sans-photo">' + e(f.nom) + "</div>";
  }
  function edition(f) { return "ARTMADA #" + f.edition + " · " + f.annee; }
  function tampons() { return stock("artmada.tampons") || {}; }
  function tamponnable(f) { return !!f.gps && !f.disparue; }
  function nbTampons() { var t = tampons(); return Object.keys(t).filter(function (s) { return F[s] && tamponnable(F[s]); }).length; }
  function aller(h) { location.hash = h; }
  function pluriel(n, fr, frs, en, ens) { return n + " " + (n > 1 ? T(frs, ens) : T(fr, en)); }
  function dateCourte(iso) {
    return new Date(iso).toLocaleDateString(LANGUE === "en" ? "en-GB" : "fr-FR", { day: "numeric", month: "long", year: "numeric" });
  }

  /* ---------- position ---------- */
  function localiser(apres, silencieux) {
    if (!("geolocation" in navigator)) { if (!silencieux) toast(T("Ton téléphone ne donne pas sa position.", "Your phone does not share its location.")); apres && apres(null); return; }
    navigator.geolocation.getCurrentPosition(function (p) {
      maPosition = [p.coords.latitude, p.coords.longitude];
      apres && apres(maPosition);
    }, function () {
      if (!silencieux) toast(T("Position refusée. Autorise la localisation dans les réglages du téléphone.", "Location refused. Allow location in your phone settings."));
      apres && apres(null);
    }, { enableHighAccuracy: true, timeout: 9000, maximumAge: 60000 });
  }

  /* ---------- barre du bas ---------- */
  function dessinerOnglets() {
    var o = [["accueil", "accueil", T("Accueil", "Home")], ["carte", "carte", T("Carte", "Map")], ["parcours", "chemin", T("Parcours", "Walks")],
      ["festival", "festival", "Festival"], ["passeport", "passeport", T("Passeport", "Passport")]];
    var nav = document.querySelector(".onglets");
    nav.setAttribute("aria-label", T("Menu principal", "Main menu"));
    nav.innerHTML = o.map(function (x) { return '<a href="#' + x[0] + '" data-onglet="' + x[0] + '">' + ico(x[1]) + x[2] + "</a>"; }).join("");
  }

  /* ---------- navigation ---------- */
  function route() {
    var h = decodeURIComponent(location.hash.replace(/^#/, "")) || "accueil";
    var parts = h.split("/");
    if (carteLeaflet) { carteLeaflet.remove(); carteLeaflet = null; }
    var onglet = { accueil: "accueil", carte: "carte", f: "carte", parcours: "parcours", p: "parcours", passeport: "passeport",
      festival: "festival", direct: "festival", benevoles: "festival" }[parts[0]] || "accueil";
    document.querySelectorAll(".onglets a").forEach(function (a) {
      if (a.dataset.onglet === onglet) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
    });
    if (parts[0] === "carte") pageCarte();
    else if (parts[0] === "f" && F[parts[1]]) pageFresque(F[parts[1]]);
    else if (parts[0] === "parcours") pageParcours();
    else if (parts[0] === "p") pageUnParcours(parts[1]);
    else if (parts[0] === "passeport") pagePasseport();
    else if (parts[0] === "festival") pageFestival();
    else if (parts[0] === "direct") pageDirect();
    else if (parts[0] === "benevoles") pageBenevoles();
    else pageAccueil();
    vue.scrollTop = 0;
    if (parts[0] !== "carte") vue.focus({ preventScroll: true });
  }

  /* ---------- compte à rebours ---------- */
  function joursAvant() {
    var auj = new Date(new Date().toLocaleString("en-US", { timeZone: "America/Martinique" }));
    auj.setHours(0, 0, 0, 0);
    var debut = new Date(D.festival.debut + "T00:00:00"), fin = new Date(D.festival.fin + "T00:00:00");
    return { j: Math.round((debut - auj) / 86400000), enCours: auj >= debut && auj <= fin };
  }
  function puceCompte() {
    var c = joursAvant();
    if (c.j > 0) return '<span class="puce direct">' + T("J-", "D-") + c.j + "</span>";
    if (c.enCours) return '<span class="puce direct">' + T("EN DIRECT", "LIVE") + "</span>";
    return "";
  }
  function datesFestival() { return T("25 janvier → 4 février 2027", "25 January → 4 February 2027"); }

  /* ---------- installation sur l'écran d'accueil ---------- */
  function estInstallee() {
    return window.navigator.standalone === true || (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches);
  }
  function blocInstallation() {
    if (estInstallee() || stock("artmada.install-ferme")) return "";
    var ios = /iphone|ipad|ipod/i.test(navigator.userAgent);
    var comment = invitationInstall ? T("Un seul bouton, et ARTMADA s'ouvre comme une vraie appli.", "One tap, and ARTMADA opens like a real app.")
      : ios ? T("Dans Safari : touche Partager, puis « Sur l'écran d'accueil ».", "In Safari: tap Share, then “Add to Home Screen”.")
        : T("Dans le menu du navigateur (⋮) : « Installer l'appli » ou « Ajouter à l'écran d'accueil ».", "In the browser menu (⋮): “Install app” or “Add to Home screen”.");
    return '<div class="bloc installer" id="installer"><span class="rond" style="background:var(--orange);color:var(--encre)">' + ico("ajouter") + "</span>" +
      '<div class="txt"><b>' + T("Garde ARTMADA sur ton téléphone", "Keep ARTMADA on your phone") + "</b><span>" + comment + "</span>" +
      (invitationInstall ? '<button type="button" class="bouton" id="installer-ok" style="align-self:flex-start;min-height:40px;margin-top:6px">' + T("Installer", "Install") + "</button>" : "") +
      '</div><button type="button" class="fermer" id="installer-ferme" aria-label="' + T("Fermer", "Close") + '">' + ico("fermer") + "</button></div>";
  }
  function brancherInstallation() {
    var f = document.getElementById("installer-ferme");
    if (f) f.addEventListener("click", function () { stock("artmada.install-ferme", true); document.getElementById("installer").remove(); });
    var ok = document.getElementById("installer-ok");
    if (ok) ok.addEventListener("click", function () {
      invitationInstall.prompt();
      invitationInstall.userChoice.finally(function () { invitationInstall = null; route(); });
    });
  }

  /* ---------- ACCUEIL ---------- */
  function pageAccueil() {
    var star = F["xan-pointe-simon"] || D.fresques.filter(function (f) { return f.photo; })[0];
    var jour = Math.floor(Date.now() / 86400000);
    var avecTexte = D.fresques.filter(function (f) { return f.photo && f.texte && !f.disparue; });
    var duJour = avecTexte[jour % avecTexte.length];
    var surCarte = D.fresques.filter(function (f) { return f.gps; }).length;
    var tot = D.fresques.filter(tamponnable).length, faits = nbTampons();
    var a = D.atelier;
    vue.innerHTML =
      '<div class="page">' +
      '<header class="entete"><div><img src="media/logo.webp" alt="ARTMADA Street Festival" width="150" height="72"><div class="lieu">STREET ART · MARTINIQUE</div></div>' +
      '<div style="display:flex;gap:10px"><button type="button" class="rond langue" id="langue-btn" aria-label="' + T("Read in English", "Lire en français") + '">' + T("EN", "FR") + "</button>" +
      '<a class="rond" href="#passeport" aria-label="' + T("Mon passeport", "My passport") + '">' + ico("passeport") + "</a></div></header>" +

      '<a class="une" href="#festival">' +
      '<img src="' + photo(star) + '" alt="' + e(altFresque(star)) + ', Pointe Simon">' +
      '<div class="haut">' + puceCompte() + "</div>" +
      '<div class="bas"><span class="surtitre" style="color:#E6E4DE">' + T("Édition #3", "Edition #3") + "</span>" +
      "<h1>ARTMADA #3 · " + e(D.festival.theme) + "</h1>" +
      '<span class="dates">' + datesFestival() + " · Fort-de-France</span></div></a>" +

      blocInstallation() +

      '<div class="duo">' +
      '<a class="tuile" href="#carte"><svg viewBox="0 0 24 24" stroke="#22C4C4" aria-hidden="true"><path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2-6-2z"/><path d="M9 4v14M15 6v14"/></svg>' +
      '<span class="chiffre">' + surCarte + "</span><b>" + T("Fresques sur la carte", "Murals on the map") + "</b><span>" + T("Autour de toi", "Around you") + "</span></a>" +
      '<a class="tuile" href="#parcours"><svg viewBox="0 0 24 24" stroke="#FCD40D" aria-hidden="true"><circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M8 19h7a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h7"/></svg>' +
      '<span class="chiffre">' + D.parcours.length + "</span><b>" + T("Parcours à pied", "Walking routes") + "</b><span>" + T("Gratuits, à ton rythme", "Free, at your own pace") + "</span></a>" +
      "</div>" +

      '<section class="pile"><div class="titre-section"><h2>' + T("La fresque du jour", "Mural of the day") + '</h2><a href="#carte">' + T("Toutes", "All") + "</a></div>" +
      '<a class="ligne-carte" href="#f/' + duJour.slug + '">' + imgOuVide(duJour, true) +
      '<div class="txt"><span class="surtitre e' + duJour.edition + '">' + edition(duJour) + "</span><b>" + e(duJour.nom) + (duJour.titre ? " · " + e(duJour.titre) : "") + "</b><span>" + e(duJour.secteur || duJour.lieu) + "</span></div>" + FLECHE + "</a></section>" +

      '<section class="pile"><div class="titre-section"><h2>' + T("Peindre et visiter", "Paint & visit") + "</h2></div>" +
      '<a class="ligne-carte" href="' + a.lien + '" target="_blank" rel="noopener">' + imgOuVide(F["doudou-style-tom-atlas"] || star, true) +
      '<div class="txt"><b>' + e(C(a, "titre")) + "</b><span>" + e(C(a, "quand")) + "</span><span>" + e(a.ou) + '</span><span class="prix">' + e(C(a, "prix")) + " · " + a.places + T(" places", " spots") + "</span></div>" +
      '<span class="bouton" style="min-height:40px;padding:0 12px;font-size:14px">' + T("Réserver", "Book") + "</span></a>" +
      '<a class="ligne-carte" href="' + SITE + (LANGUE === "en" ? "en/" : "") + 'visites.html" target="_blank" rel="noopener">' + imgOuVide(F["curtis-hylton-tom"] || star, true) +
      '<div class="txt"><b>' + T("Visite guidée en groupe", "Guided group tour") + "</b><span>" + T("2 h à pied avec un membre du collectif", "2 hours on foot with a member of the collective") + '</span><span class="prix">' + T("250 € le groupe · jusqu'à 25 pers.", "€250 per group · up to 25 people") + "</span></div>" + FLECHE + "</a></section>" +

      '<div class="duo">' +
      '<a class="tuile" href="#passeport"><svg viewBox="0 0 24 24" stroke="#22C4C4" aria-hidden="true"><rect x="5" y="3" width="14" height="18" rx="2"/><circle cx="12" cy="10" r="3"/><path d="M9 17h6"/></svg>' +
      '<span class="chiffre">' + faits + '<small class="gris" style="font-family:var(--texte);font-size:15px"> / ' + tot + "</small></span><b>" + T("Mon passeport", "My passport") + "</b>" +
      '<div class="jauge"><i style="width:' + Math.round(faits / tot * 100) + '%"></i></div></a>' +
      '<a class="tuile" href="#benevoles"><svg viewBox="0 0 24 24" stroke="#E3138B" aria-hidden="true"><path d="M7 11V6a2 2 0 0 1 4 0v4"/><path d="M11 10V4a2 2 0 0 1 4 0v6"/><path d="M15 10V6a2 2 0 0 1 4 0v8a7 7 0 0 1-7 7h-1a6 6 0 0 1-5-2.7L3.5 14a2 2 0 0 1 3.2-2.4L7 12"/></svg>' +
      "<b>" + T("Devenir bénévole", "Volunteer") + "</b><span>" + T("Pour ARTMADA #3", "For ARTMADA #3") + "</span></a>" +
      "</div>" +

      '<p class="note">' + T("Version de test · ARTMADA Street Festival, porté par l'association NPL MADA PAINT", "Test version · ARTMADA Street Festival, run by the NPL MADA PAINT association") +
      ' · <a href="' + SITE + (LANGUE === "en" ? "en/" : "") + '" target="_blank" rel="noopener">artmadastreetfestival.com</a></p>' +
      "</div>";
    document.getElementById("langue-btn").addEventListener("click", changerLangue);
    brancherInstallation();
  }

  /* ---------- CARTE ---------- */
  function sansAccents(s) { return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function fresquesFiltrees() {
    var q = sansAccents(etat.recherche.trim());
    var t = tampons();
    return D.fresques.filter(function (f) {
      if (etat.filtre === "e2" && f.edition !== 2) return false;
      if (etat.filtre === "e1" && f.edition !== 1) return false;
      if (etat.filtre === "atamponner" && (!tamponnable(f) || t[f.slug])) return false;
      if (!q) return true;
      return sansAccents(f.nom + " " + f.titre + " " + f.lieu + " " + f.secteur + " " + f.ville).indexOf(q) >= 0;
    });
  }
  function pageCarte() {
    var filtres = [["toutes", T("Toutes", "All")], ["e2", "ARTMADA #2 · 2026"], ["e1", "ARTMADA #1 · 2024"], ["atamponner", T("Pas encore tamponnées", "Not stamped yet")]];
    var tete =
      '<div class="recherche">' + ico("chercher") + '<label class="sr" for="cherche">' + T("Rechercher", "Search") + "</label>" +
      '<input id="cherche" type="search" placeholder="' + T("Une fresque, un artiste, un quartier", "A mural, an artist, a neighbourhood") + '" value="' + e(etat.recherche) + '" autocomplete="off"></div>' +
      '<div class="puces" role="group" aria-label="' + T("Filtrer", "Filter") + '">' + filtres.map(function (x) {
        return '<button type="button" class="filtre" data-filtre="' + x[0] + '" aria-pressed="' + (etat.filtre === x[0]) + '">' + x[1] + "</button>";
      }).join("") + "</div>" +
      '<div class="bascule" role="group" aria-label="' + T("Affichage", "View") + '"><button type="button" data-mode="carte" aria-pressed="' + (etat.mode === "carte") + '">' + T("Carte", "Map") + "</button>" +
      '<button type="button" data-mode="liste" aria-pressed="' + (etat.mode === "liste") + '">' + T("Liste", "List") + "</button></div>";

    if (etat.mode === "liste") {
      vue.innerHTML = '<div class="page"><h1 style="font-size:36px">' + T("Les fresques", "The murals") + "</h1>" + tete + '<div id="liste" class="liste-fresques"></div></div>';
      dessinerListe();
    } else {
      vue.innerHTML = '<div class="page-carte"><div id="carte" role="application" aria-label="' + T("Carte des fresques", "Mural map") + '"></div>' +
        '<div class="carte-haut">' + tete + "</div>" +
        '<div class="carte-actions" id="actions"><button type="button" class="flottant" id="localiser" aria-label="' + T("Me localiser", "Find me") + '">' + ico("viser") + "</button></div>" +
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
      var info = f.disparue ? T("Fresque disparue", "Mural gone") : (distanceTexte(f) || (f.gps ? f.secteur || f.ville : T("Pas encore sur la carte", "Not on the map yet")));
      return '<a class="vignette" href="#f/' + f.slug + '"><div class="ph">' + imgOuVide(f, false) +
        '<span class="puce e' + f.edition + '">#' + f.edition + "</span>" +
        (t[f.slug] ? '<span class="ok" aria-label="' + T("Tamponnée", "Stamped") + '">' + ico("ok") + "</span>" : "") +
        "</div><b>" + e(f.nom) + "</b><span>" + e(info) + "</span></a>";
    }).join("") : '<p class="gris">' + T("Aucune fresque ne correspond.", "No mural matches.") + "</p>";
  }

  var calqueMarqueurs = null;
  function fondDeCarte(carte) {
    L.tileLayer(TUILES, { maxZoom: 19, attribution: ATTRIB }).addTo(carte);
  }
  function dessinerCarte() {
    carteLeaflet = L.map("carte", { zoomControl: false }).setView(CENTRE, 15);
    fondDeCarte(carteLeaflet);
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
        title: f.nom, alt: altFresque(f), keyboard: true, riseOnHover: true,
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
    var d = distanceTexte(f);
    el.innerHTML = '<a class="ligne-carte fiche-flottante" href="#f/' + f.slug + '">' + imgOuVide(f, true) +
      '<div class="txt"><span class="surtitre e' + f.edition + '">' + edition(f) + '</span><span class="nom">' + e(f.nom) + "</span>" +
      "<span>" + e(f.titre ? f.titre : f.secteur || f.lieu) + (d ? " · " + d : "") + "</span></div>" + FLECHE + "</a>";
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
    // Texte dans la langue choisie, l'autre langue à un bouton.
    var principal = LANGUE === "en" && f.texte_en ? f.texte_en : f.texte;
    var second = principal === f.texte ? f.texte_en : f.texte;
    var d = distanceTexte(f);

    vue.innerHTML =
      '<div class="page">' +
      '<div class="fiche-photo">' + (f.photo ? '<img src="' + photo(f) + '" alt="' + e(altFresque(f)) + ", " + e(lieu) + '">' : '<div class="sans-photo">' + e(f.nom) + "</div>") +
      '<div class="boutons"><button type="button" class="rond" id="retour" aria-label="' + T("Retour", "Back") + '">' + ico("retour") + "</button>" +
      '<button type="button" class="rond" id="partager" aria-label="' + T("Partager", "Share") + '">' + ico("partager") + "</button></div>" +
      (f.photo && f.credit ? '<span class="credit">' + T("Photo : ", "Photo: ") + e(f.credit) + "</span>" : "") + "</div>" +

      '<div class="fiche-tete"><span class="surtitre e' + f.edition + '">' + edition(f) + (f.collectif ? T(" · fresque collective", " · collective mural") : "") + "</span>" +
      "<h1>" + e(f.nom) + "</h1>" +
      (f.titre ? '<span class="oeuvre">' + T("« ", "“") + e(f.titre) + T(" »", "”") + "</span>" : "") +
      '<span class="gris">' + e(lieu) + (d ? " · " + d : "") + "</span>" +
      (f.disparue ? '<span><span class="puce disparue">' + T("Fresque disparue", "Mural gone") + "</span></span>" : "") + "</div>" +

      '<div class="trio">' +
      '<a href="' + e(f.y_aller) + '" target="_blank" rel="noopener">' + ico("aller") + T("Y aller à pied", "Walk there") + "</a>" +
      (artistes.length ? '<button type="button" id="voir-artiste">' + ico("artiste") + (artistes.length > 1 ? T("Les artistes", "The artists") : T("L'artiste", "The artist")) + "</button>" : '<a href="#carte">' + ico("carte") + T("La carte", "The map") + "</a>") +
      '<button type="button" id="partager2">' + ico("partager") + T("Partager", "Share") + "</button></div>" +

      (tamponnable(f) ? '<button type="button" id="tamponner" class="tamponner' + (t[f.slug] ? " fait" : "") + '"></button>' : "") +

      '<section class="histoire"><span class="surtitre">' + T("L'histoire de la fresque", "The story of the mural") + "</span>" +
      (principal ? '<div id="texte-1" class="histoire">' + paragraphes(principal) + "</div>" +
        (second ? '<div id="texte-2" class="histoire" lang="' + (principal === f.texte ? "en" : "fr") + '" hidden>' + paragraphes(second) + "</div>" +
          '<button type="button" class="lien-texte" id="autre-langue">' + (principal === f.texte ? "Read in English" : "Lire en français") + "</button>" : "")
        : '<p class="gris">' + T("Le texte de cette fresque arrive bientôt.", "The story of this mural is coming soon.") + "</p>") + "</section>" +

      artistes.map(function (x) {
        var a = x[1];
        return '<section class="bloc artiste" id="artiste-' + x[0] + '"><span class="surtitre">' + (a.collectif ? T("Collectif ", "") + e(a.collectif) + T("", " crew") + " · " : "") + e(C(a, "origine")) + "</span>" +
          "<h3>" + e(a.nom) + "</h3>" + (C(a, "bio") ? "<p>" + e(C(a, "bio")) + "</p>" : "") +
          (a.instagram ? '<a class="bouton contour" style="align-self:flex-start" href="https://www.instagram.com/' + e(a.instagram) + '/" target="_blank" rel="noopener">' + ico("insta") + "@" + e(a.instagram) + "</a>" : "") +
          "</section>";
      }).join("") +

      '<dl class="infos"><dt>' + T("Édition", "Edition") + "</dt><dd>" + edition(f) + "</dd><dt>" + T("Lieu", "Place") + "</dt><dd>" + e(f.lieu) + "</dd>" +
      (f.secteur && f.secteur !== f.lieu ? "<dt>" + T("Quartier", "Area") + "</dt><dd>" + e(f.secteur) + "</dd>" : "") +
      "<dt>" + T("Ville", "Town") + "</dt><dd>" + e(f.ville) + "</dd>" +
      (f.surface ? "<dt>" + T("Surface", "Size") + "</dt><dd>" + e(f.surface) + " m²</dd>" : "") + "</dl>" +

      (voisines.length ? '<section class="pile"><div class="titre-section"><h2>' + T("Juste à côté", "Close by") + '</h2></div><div class="liste-fresques">' +
        voisines.map(function (v) {
          var dd = distanceBrute(km(f.gps, v.gps));
          return '<a class="vignette" href="#f/' + v.slug + '"><div class="ph">' + imgOuVide(v, false) + '<span class="puce e' + v.edition + '">#' + v.edition + "</span></div><b>" + e(v.nom) + "</b><span>" +
            T(dd + " d'ici", dd + " away") + "</span></a>";
        }).join("") + "</div></section>" : "") +
      "</div>";

    document.getElementById("retour").addEventListener("click", function () {
      if (route.precedente) history.back(); else aller("carte");
    });
    function partager() {
      var url = location.href.split("#")[0].replace(/[?&]test\b/, "") + "#f/" + f.slug;
      var data = { title: "ARTMADA · " + f.nom, text: T("La fresque de " + f.nom + " à " + f.ville + " (ARTMADA #" + f.edition + ")", "The mural by " + f.nom + " in " + f.ville + " (ARTMADA #" + f.edition + ")"), url: url };
      if (navigator.share) navigator.share(data).catch(function () {});
      else if (navigator.clipboard) navigator.clipboard.writeText(url).then(function () { toast(T("Lien copié", "Link copied")); }, function () { toast(url); });
      else toast(url);
    }
    document.getElementById("partager").addEventListener("click", partager);
    document.getElementById("partager2").addEventListener("click", partager);
    var va = document.getElementById("voir-artiste");
    if (va) va.addEventListener("click", function () {
      document.getElementById("artiste-" + artistes[0][0]).scrollIntoView({ behavior: "smooth", block: "start" });
    });
    var lg = document.getElementById("autre-langue");
    if (lg) lg.addEventListener("click", function () {
      var t1 = document.getElementById("texte-1"), t2 = document.getElementById("texte-2");
      var montre = t2.hidden; t2.hidden = !montre; t1.hidden = montre;
      var premierEstFr = principal === f.texte;
      lg.textContent = (montre === premierEstFr) ? "Lire en français" : "Read in English";
    });
    var bt = document.getElementById("tamponner");
    if (bt) { dessinerTampon(bt, f); bt.addEventListener("click", function () { tamponner(bt, f); }); }
  }

  function dessinerTampon(bt, f, message) {
    var t = tampons(), total = D.fresques.filter(tamponnable).length, n = nbTampons();
    if (t[f.slug]) {
      bt.className = "tamponner fait";
      bt.innerHTML = ico("ok") + "<span><b>" + T("Tamponnée ! ", "Stamped! ") + n + T(" sur ", " of ") + total + "</b><span>" +
        T("Le ", "On ") + dateCourte(t[f.slug]) + T(" · voir mon passeport", " · see my passport") + "</span></span>";
    } else if (message) {
      bt.className = "tamponner loin";
      bt.innerHTML = ico("aller") + "<span><b>" + e(message[0]) + "</b><span>" + e(message[1]) + "</span></span>";
    } else {
      bt.className = "tamponner";
      bt.innerHTML = ico("tampon") + "<span><b>" + T("Je suis devant : tamponner", "I'm here: stamp it") + "</b><span>" + T("Ajoute cette fresque à ton passeport", "Add this mural to your passport") + "</span></span>";
    }
  }
  function tamponner(bt, f) {
    var t = tampons();
    if (t[f.slug]) { aller("passeport"); return; }
    function valider() {
      t[f.slug] = new Date().toISOString(); stock("artmada.tampons", t);
      dessinerTampon(bt, f); toast(T("Tamponnée !", "Stamped!"));
    }
    if (MODE_TEST) { valider(); return; }
    bt.innerHTML = ico("viser") + "<span><b>" + T("Je vérifie que tu es devant…", "Checking you're there…") + "</b><span>" + T("Position en cours", "Getting your location") + "</span></span>";
    localiser(function (p) {
      if (!p) { dessinerTampon(bt, f, [T("Active ta localisation", "Turn on location"), T("Elle sert seulement à vérifier que tu es devant le mur.", "It's only used to check you're at the wall.")]); return; }
      if (km(p, f.gps) <= 0.25) valider();
      else dessinerTampon(bt, f, [T("Tu es ", "You're ") + distanceTexte(f).replace(/^à /, "à "), T("Approche-toi du mur pour tamponner (moins de 250 m).", "Get closer to the wall to stamp it (under 250 m).")]);
    }, true);
  }

  /* ---------- PARCOURS ---------- */
  function mosaique(p) {
    var avec = p.etapes.map(function (s) { return F[s]; }).filter(function (f) { return f.photo; });
    return '<div class="mosaique">' + avec.slice(0, 3).map(function (f) { return '<img src="' + photo(f) + '" alt="" loading="lazy">'; }).join("") + "</div>";
  }
  function mesures(p, long) {
    return '<div class="mesures"><span><b>' + p.etapes.length + "</b> " + T("fresques", "murals") + "</span><span>≈ <b>" + nombre(p.km, 1) + "</b> km</span><span>≈ <b>" + p.minutes + "</b> min" + (long ? T(" de marche", " walk") : "") + "</span></div>";
  }
  function pageParcours() {
    var t = tampons();
    vue.innerHTML = '<div class="page"><h1 style="font-size:40px">' + T("Parcours", "Walks") + "</h1>" +
      '<p class="gris" style="margin-top:-8px">' + T("Gratuits, à pied, à ton rythme. Suis la carte dans l'appli ou lance Google Maps.", "Free, on foot, at your own pace. Follow the map in the app or open Google Maps.") + "</p>" +
      D.parcours.map(function (p) {
        var faits = p.etapes.filter(function (s) { return t[s]; }).length;
        return '<article class="bloc parcours-carte">' + mosaique(p) + '<div class="corps">' +
          '<span class="surtitre ' + (p.editions.length === 1 ? "e" + p.editions[0] : "") + '">' + p.editions.map(function (x) { return "ARTMADA #" + x; }).join(" + ") + "</span>" +
          "<h2>" + e(C(p, "titre")) + "</h2><p>" + e(C(p, "texte")) + "</p>" +
          '<div class="pied">' + mesures(p) + '<a class="bouton" href="#p/' + p.cle + '">' + T("Partir", "Go") + "</a></div>" +
          (faits ? '<span class="petit" style="color:var(--turquoise);font-weight:700">' + faits + T(" sur ", " of ") + p.etapes.length + T(faits > 1 ? " déjà tamponnées" : " déjà tamponnée", " already stamped") + "</span>" : "") +
          "</div></article>";
      }).join("") +
      '<section class="pile" style="margin-top:6px"><div class="titre-section"><h2>' + T("Avec un guide", "With a guide") + "</h2></div>" +
      '<a class="ligne-carte" href="' + SITE + (LANGUE === "en" ? "en/" : "") + 'visites.html" target="_blank" rel="noopener"><span class="rond" style="background:var(--beton-clair)">' + ico("groupe") + "</span>" +
      '<div class="txt"><b>' + T("Visite guidée en groupe", "Guided group tour") + "</b><span>" + T("2 h à pied", "2 hours on foot") + '</span><span class="prix">' + T("250 € le groupe · jusqu'à 25 pers.", "€250 per group · up to 25 people") + "</span></div>" + FLECHE + "</a>" +
      '<a class="ligne-carte" href="' + D.atelier.lien + '" target="_blank" rel="noopener"><span class="rond" style="background:var(--beton-clair)">' + ico("pinceau") + "</span>" +
      '<div class="txt"><b>' + T("Envie de peindre ?", "Want to paint?") + "</b><span>" + e(C(D.atelier, "quand")) + ' · Urban Studio, Trois-Îlets</span><span class="prix">' + e(C(D.atelier, "prix")) + "</span></div>" + FLECHE + "</a></section>" +
      "</div>";
  }

  function pageUnParcours(cle) {
    var p = D.parcours.filter(function (x) { return x.cle === cle; })[0];
    if (!p) { aller("parcours"); return; }
    var t = tampons();
    var etapes = p.etapes.map(function (s) { return F[s]; });
    vue.innerHTML = '<div class="page">' +
      '<div style="display:flex;align-items:center;gap:12px"><a class="rond" href="#parcours" aria-label="' + T("Retour aux parcours", "Back to walks") + '">' + ico("retour") + "</a>" +
      '<span class="surtitre">' + T("Parcours à pied", "Walking route") + "</span></div>" +
      '<h1 style="font-size:clamp(32px,9vw,44px)">' + e(C(p, "titre")) + "</h1>" + mesures(p, true) +
      '<div class="carte-parcours"><div id="carte" style="position:absolute;inset:0" role="application" aria-label="' + T("Carte du parcours", "Route map") + '"></div></div>' +
      '<a class="bouton" href="' + e(p.url) + '" target="_blank" rel="noopener">' + ico("chemin") + T("Lancer dans Google Maps (à pied)", "Open in Google Maps (walking)") + "</a>" +
      '<p class="note" style="margin-top:-10px">' + T("Sur la carte, le trait relie les étapes dans l'ordre. Google Maps te donne le vrai chemin dans les rues.", "On the map, the line links the stops in order. Google Maps gives you the actual route through the streets.") + "</p>" +
      '<ol class="etapes">' + etapes.map(function (f, i) {
        return '<li><span class="n' + (t[f.slug] ? " ok" : "") + '">' + (i + 1) + '</span><a class="ligne-carte" href="#f/' + f.slug + '" style="padding:8px">' + imgOuVide(f, true) +
          '<div class="txt"><b>' + e(f.nom) + "</b><span>" + e(f.titre || f.lieu) + "</span>" +
          (t[f.slug] ? '<span style="color:var(--turquoise);font-weight:700">' + T("Tamponnée", "Stamped") + "</span>" : "") + "</div></a></li>";
      }).join("") + "</ol></div>";

    carteLeaflet = L.map("carte", { zoomControl: false, scrollWheelZoom: false }).setView(etapes[0].gps, 15);
    fondDeCarte(carteLeaflet);
    L.polyline(etapes.map(function (f) { return f.gps; }), { color: "#EB782F", weight: 4, opacity: .95, dashArray: "2 9", lineCap: "round" }).addTo(carteLeaflet);
    etapes.forEach(function (f, i) {
      L.marker(f.gps, { icon: L.divIcon({ className: "", html: '<span class="pin-etape">' + (i + 1) + "</span>", iconSize: [34, 34], iconAnchor: [17, 17] }), title: f.nom })
        .on("click", function () { aller("f/" + f.slug); }).addTo(carteLeaflet);
    });
    carteLeaflet.fitBounds(L.latLngBounds(etapes.map(function (f) { return f.gps; })), { padding: [34, 34] });
  }

  /* ---------- FESTIVAL ---------- */
  function pageFestival() {
    var c = joursAvant(), fe = D.festival;
    var fond = F["magiic-rman-clarac"] || F["mur-de-la-jam"];
    var texte = (LANGUE === "en" && fe.texte_en.length ? fe.texte_en : fe.texte);
    var citation = texte.filter(function (p) { return /fatalisme|fatalism/.test(p); })[0] || "";
    vue.innerHTML = '<div class="page">' +
      '<div class="fiche-photo festival-photo">' + (fond && fond.photo ? '<img src="' + photo(fond) + '" alt="' + e(altFresque(fond)) + '">' : "") +
      '<div class="boutons"><span></span>' + puceCompte() + "</div></div>" +
      '<div class="fiche-tete"><span class="surtitre" style="color:var(--magenta)">' + T("Édition #3 · Fort-de-France", "Edition #3 · Fort-de-France") + "</span>" +
      "<h1>ARTMADA #3</h1>" +
      '<span class="oeuvre">' + datesFestival() + "</span></div>" +

      (c.j > 0 ? '<div class="bloc compte-bloc"><span class="compte-geant">' + c.j + "</span><span>" + T("jours avant le festival", "days to go") + "</span></div>" : "") +

      '<section class="bloc theme"><span class="surtitre e2">' + T("Le thème", "The theme") + "</span>" +
      "<h2>" + e(fe.theme) + '</h2><span class="gris">' + T("Un autre chemin · texte de Xän pour le collectif Mada Paint", "Another way · text by Xän for the Mada Paint collective") + "</span>" +
      (citation ? '<p class="citation">' + e(citation) + "</p>" : "") +
      '<div id="theme-texte" class="histoire"' + (etat.texteTheme ? "" : " hidden") + ">" + texte.map(function (p) { return "<p>" + e(p) + "</p>"; }).join("") + "</div>" +
      '<button type="button" class="lien-texte" id="theme-btn">' + (etat.texteTheme ? T("Fermer le texte", "Close the text") : T("Lire le texte en entier", "Read the full text")) + "</button></section>" +

      '<dl class="infos grand"><dt>' + T("Dates", "Dates") + "</dt><dd>" + T("Du lundi 25 janvier au jeudi 4 février 2027", "Monday 25 January to Thursday 4 February 2027") + "</dd>" +
      "<dt>" + T("Quartiers", "Areas") + "</dt><dd>" + e(C(fe, "quartiers")) + "</dd>" +
      "<dt>" + T("Artistes", "Artists") + "</dt><dd>" + T("Annoncés bientôt", "Coming soon") + "</dd>" +
      "<dt>" + T("Prix", "Price") + "</dt><dd>" + T("Les fresques se regardent gratuitement, dans la rue", "The murals are free to see, in the street") + "</dd>" +
      "<dt>" + T("Organisation", "Organised by") + "</dt><dd>" + T("Association NPL MADA PAINT (collectif Mada Paint), avec la Ville de Fort-de-France", "NPL MADA PAINT association (Mada Paint collective), with the City of Fort-de-France") + "</dd></dl>" +

      '<section class="pile"><div class="titre-section"><h2>' + T("Pendant le festival", "During the festival") + "</h2></div>" +
      '<p class="gris">' + T("Du 25 janvier au 4 février, l'appli passe en mode direct.", "From 25 January to 4 February, the app goes live.") + "</p>" +
      '<ul class="avantages">' +
      "<li>" + ico("festival") + "<span><b>" + T("Le programme du jour", "Today's programme") + "</b>" + T("Fresques, ateliers, soirées : ce qui se passe aujourd'hui, et où.", "Murals, workshops, parties: what's on today, and where.") + "</span></li>" +
      "<li>" + ico("carte") + "<span><b>" + T("Les murs en train d'être peints", "Walls being painted") + "</b>" + T("Sur la carte, pour venir voir les artistes au travail.", "On the map, so you can watch the artists at work.") + "</span></li>" +
      "<li>" + ico("tampon") + "<span><b>" + T("Le passeport des nouvelles fresques", "A passport for the new murals") + "</b>" + T("Chaque fresque finie rejoint la carte et le passeport.", "Every finished mural joins the map and the passport.") + "</span></li>" +
      "</ul>" +
      '<a class="bouton" href="#direct">' + T("Voir l'aperçu du mode direct", "Preview live mode") + "</a></section>" +

      '<a class="ligne-carte" href="#benevoles" style="padding:16px"><span class="rond" style="background:var(--magenta);color:#fff">' + ico("main") + "</span>" +
      '<div class="txt"><b>' + T("Deviens bénévole", "Become a volunteer") + "</b><span>" + T("75 bénévoles ont fait vivre ARTMADA #2. Même quelques heures comptent.", "75 volunteers brought ARTMADA #2 to life. Even a few hours make a difference.") + "</span></div>" + FLECHE + "</a>" +

      '<section class="pile"><div class="titre-section"><h2>' + T("ARTMADA #2 en chiffres", "ARTMADA #2 in numbers") + "</h2></div>" +
      '<div class="chiffres3"><div><b>26</b><span>' + T("fresques en 2026", "murals in 2026") + "</span></div><div><b>1 500</b><span>" + T("personnes à la block party", "people at the block party") + "</span></div><div><b>1,2 M</b><span>" + T("vues en ligne", "online views") + "</span></div></div></section>" +
      "</div>";
    document.getElementById("theme-btn").addEventListener("click", function () { etat.texteTheme = !etat.texteTheme; var y = vue.scrollTop; pageFestival(); vue.scrollTop = y; });
  }

  /* ---------- APERÇU DU MODE DIRECT ---------- */
  var COULEUR_TYPE = { fresques: "e2", soiree: "magenta", atelier: "jaune", expo: "turquoise", visite: "vert" };
  var NOM_TYPE = { fresques: ["Fresques", "Murals"], soiree: ["Soirée", "Party"], atelier: ["Atelier", "Workshop"], expo: ["Expo", "Exhibition"], visite: ["Visite", "Tour"] };
  function pageDirect() {
    var P = D.programme_exemple, jours = P.jours;
    var i = Math.min(etat.jourDirect, jours.length - 1), j = jours[i];
    vue.innerHTML = '<div class="page">' +
      '<div style="display:flex;align-items:center;gap:12px"><a class="rond" href="#festival" aria-label="' + T("Retour au festival", "Back to the festival") + '">' + ico("retour") + "</a>" +
      '<span class="puce direct"><span class="point-direct"></span>' + T("EN DIRECT", "LIVE") + "</span></div>" +
      '<div class="apercu">' + T("Aperçu : voici à quoi ressemblera l'appli pendant le festival, avec le vrai programme d'ARTMADA #2 (2026). Le programme 2027 arrive bientôt.",
        "Preview: this is how the app will look during the festival, using the real ARTMADA #2 programme (2026). The 2027 programme is coming soon.") + "</div>" +
      '<h1 style="font-size:40px">' + T("Aujourd'hui", "Today") + "</h1>" +
      '<div class="puces jours" role="group" aria-label="' + T("Choisir le jour", "Choose the day") + '">' + jours.map(function (x, k) {
        return '<button type="button" class="jour" data-jour="' + k + '" aria-pressed="' + (k === i) + '"><small>' + e(C(x, "nom").slice(0, 3)) + "</small><b>" + e(x.jour) + "</b></button>";
      }).join("") + "</div>" +
      '<div class="jour-titre"><span class="surtitre">' + T("Jour ", "Day ") + (i + 1) + T(" sur ", " of ") + jours.length + " · " + e(C(j, "nom")) + " " + e(j.jour) + T(" février 2026", " February 2026") + "</span><h2>" + e(C(j, "titre")) + "</h2></div>" +
      '<ol class="programme">' + j.evenements.map(function (ev) {
        var coul = COULEUR_TYPE[ev.type] || "e2", nomT = NOM_TYPE[ev.type] || ["", ""];
        return '<li class="bloc evenement"><div class="ev-haut"><span class="heure">' + e(C(ev, "heure")) + '</span><span class="puce type ' + coul + '">' + T(nomT[0], nomT[1]) + "</span></div>" +
          "<b>" + e(C(ev, "titre")) + "</b>" + (ev.lieu ? '<span class="gris petit">' + ico("aller") + e(ev.lieu) + "</span>" : "") +
          (C(ev, "description") ? "<p>" + e(C(ev, "description")) + "</p>" : "") + "</li>";
      }).join("") + "</ol>" +
      '<a class="bouton second" href="#carte">' + ico("carte") + T("Voir les murs sur la carte", "See the walls on the map") + "</a>" +
      "</div>";
    vue.querySelectorAll("[data-jour]").forEach(function (b) {
      b.addEventListener("click", function () { etat.jourDirect = +b.dataset.jour; var x = vue.querySelector(".jours").scrollLeft; pageDirect(); vue.querySelector(".jours").scrollLeft = x; });
    });
  }

  /* ---------- BÉNÉVOLES ---------- */
  function joursFestival() {
    var out = [], d = new Date(D.festival.debut + "T12:00:00"), fin = new Date(D.festival.fin + "T12:00:00");
    while (d <= fin) { out.push(new Date(d)); d.setDate(d.getDate() + 1); }
    return out;
  }
  function pageBenevoles() {
    var b = stock("artmada.benevole") || { missions: [], jours: [], nom: "", tel: "", mail: "", mot: "" };
    var jours = joursFestival();
    function iso(d) { return d.toISOString().slice(0, 10); }
    function libJour(d) { return d.toLocaleDateString(LANGUE === "en" ? "en-GB" : "fr-FR", { weekday: "short", day: "numeric", month: "short" }); }
    vue.innerHTML = '<div class="page">' +
      '<div style="display:flex;align-items:center;gap:12px"><a class="rond" href="#festival" aria-label="' + T("Retour au festival", "Back to the festival") + '">' + ico("retour") + "</a>" +
      '<span class="surtitre" style="color:var(--magenta)">ARTMADA #3</span></div>' +
      '<h1 style="font-size:clamp(36px,10vw,48px)">' + T("Deviens bénévole", "Become a volunteer") + "</h1>" +
      '<p style="color:#E6E4DE">' + T("75 bénévoles ont fait vivre ARTMADA #2. Pour l'édition #3, on cherche à nouveau des bras, des sourires et des chauffeurs. Même quelques heures comptent.",
        "75 volunteers brought ARTMADA #2 to life. For edition #3, we need hands, smiles and drivers again. Even a few hours make a difference.") + "</p>" +
      '<ul class="petits-plus"><li>' + T("Pas besoin de savoir peindre", "No painting skills needed") + "</li><li>" + T("T-shirt du festival offert", "Festival T-shirt included") + "</li><li>" + T("Repas pendant les missions", "Meals during your shifts") + "</li></ul>" +

      '<form id="form-benevole" class="pile" novalidate>' +
      '<fieldset class="pile"><legend class="etape">1 · ' + T("Ce qui te tente", "What you'd like to do") + "</legend>" +
      '<div class="missions">' + D.missions.map(function (m, k) {
        var on = b.missions.indexOf(m.titre) >= 0;
        return '<button type="button" class="mission" data-mission="' + e(m.titre) + '" aria-pressed="' + on + '"><b>' + e(C(m, "titre")) + "</b><span>" + e(C(m, "texte")) + '</span><i class="coche">' + ico("ok") + "</i></button>";
      }).join("") + "</div></fieldset>" +

      '<fieldset class="pile"><legend class="etape">2 · ' + T("Tes disponibilités", "When you're free") + "</legend>" +
      '<div class="dispos">' + jours.map(function (d) {
        var on = b.jours.indexOf(iso(d)) >= 0;
        return '<button type="button" class="dispo" data-jour="' + iso(d) + '" aria-pressed="' + on + '">' + e(libJour(d)) + "</button>";
      }).join("") + "</div></fieldset>" +

      '<fieldset class="pile"><legend class="etape">3 · ' + T("Comment te joindre", "How to reach you") + "</legend>" +
      '<label class="champ" for="b-nom"><span>' + T("Prénom et nom", "First and last name") + '</span><input id="b-nom" autocomplete="name" value="' + e(b.nom) + '" required></label>' +
      '<label class="champ" for="b-tel"><span>' + T("Téléphone", "Phone") + '</span><input id="b-tel" type="tel" autocomplete="tel" inputmode="tel" value="' + e(b.tel) + '" required></label>' +
      '<label class="champ" for="b-mail"><span>' + T("Email (si tu veux)", "Email (optional)") + '</span><input id="b-mail" type="email" autocomplete="email" value="' + e(b.mail) + '"></label>' +
      '<label class="champ" for="b-mot"><span>' + T("Un mot pour l'équipe (si tu veux)", "A note for the team (optional)") + '</span><textarea id="b-mot" rows="3">' + e(b.mot) + "</textarea></label></fieldset>" +

      '<p class="erreur" id="b-erreur" role="alert" hidden></p>' +
      '<button type="submit" class="bouton">' + ico("mail") + T("Envoyer ma candidature", "Send my application") + "</button>" +
      '<p class="note">' + T("Le bouton ouvre ton application mail avec tout rempli, adressé à ", "The button opens your email app with everything filled in, addressed to ") + "<b>" + e(D.contact) + "</b>" +
      T(". Tu n'as plus qu'à envoyer. Bientôt : ton espace bénévole dans l'appli, avec tes missions et ton planning.", ". Just press send. Coming soon: your own volunteer space in the app, with your shifts and schedule.") + "</p>" +
      '<div id="b-resume" class="bloc resume" hidden></div>' +
      "</form></div>";

    function sauver() {
      b.nom = document.getElementById("b-nom").value; b.tel = document.getElementById("b-tel").value;
      b.mail = document.getElementById("b-mail").value; b.mot = document.getElementById("b-mot").value;
      stock("artmada.benevole", b);
    }
    vue.querySelectorAll("[data-mission]").forEach(function (x) {
      x.addEventListener("click", function () {
        var m = x.dataset.mission, k = b.missions.indexOf(m);
        if (k >= 0) b.missions.splice(k, 1); else b.missions.push(m);
        x.setAttribute("aria-pressed", k < 0); sauver();
      });
    });
    vue.querySelectorAll("[data-jour]").forEach(function (x) {
      x.addEventListener("click", function () {
        var j = x.dataset.jour, k = b.jours.indexOf(j);
        if (k >= 0) b.jours.splice(k, 1); else b.jours.push(j);
        b.jours.sort(); x.setAttribute("aria-pressed", k < 0); sauver();
      });
    });
    ["b-nom", "b-tel", "b-mail", "b-mot"].forEach(function (id) { document.getElementById(id).addEventListener("input", sauver); });

    document.getElementById("form-benevole").addEventListener("submit", function (ev) {
      ev.preventDefault(); sauver();
      var err = document.getElementById("b-erreur"), manque = [];
      if (!b.missions.length) manque.push(T("une mission", "a role"));
      if (!b.jours.length) manque.push(T("au moins un jour", "at least one day"));
      if (!b.nom.trim()) manque.push(T("ton nom", "your name"));
      if (!b.tel.trim()) manque.push(T("ton téléphone", "your phone number"));
      if (manque.length) { err.textContent = T("Il manque : ", "Missing: ") + manque.join(", ") + "."; err.hidden = false; return; }
      err.hidden = true;
      var lignesJours = b.jours.map(function (j) { return "- " + libJour(new Date(j + "T12:00:00")); }).join("\n");
      var corps = T("Bonjour l'équipe ARTMADA,\n\nJe veux être bénévole pour ARTMADA #3.\n\n", "Hello ARTMADA team,\n\nI'd like to volunteer for ARTMADA #3.\n\n") +
        T("Nom : ", "Name: ") + b.nom + "\n" + T("Téléphone : ", "Phone: ") + b.tel + "\n" + (b.mail ? "Email : " + b.mail + "\n" : "") +
        "\n" + T("Missions : ", "Roles: ") + b.missions.join(", ") + "\n\n" + T("Disponible :\n", "Available:\n") + lignesJours + "\n" +
        (b.mot ? "\n" + b.mot + "\n" : "") + T("\nEnvoyé depuis l'appli ARTMADA.", "\nSent from the ARTMADA app.");
      var sujet = T("Je deviens bénévole ARTMADA #3", "Volunteer ARTMADA #3") + " · " + b.nom;
      var res = document.getElementById("b-resume");
      res.hidden = false;
      res.innerHTML = "<b>" + T("Ton application mail va s'ouvrir.", "Your email app will open.") + "</b><span>" +
        T("Si rien ne s'ouvre, copie ce message et envoie-le à ", "If nothing opens, copy this message and send it to ") + e(D.contact) + ".</span><pre>" + e(corps) + "</pre>" +
        '<button type="button" class="bouton second" id="b-copier">' + ico("copier") + T("Copier le message", "Copy the message") + "</button>";
      document.getElementById("b-copier").addEventListener("click", function () {
        if (navigator.clipboard) navigator.clipboard.writeText(corps).then(function () { toast(T("Message copié", "Message copied")); }, function () {});
      });
      location.href = "mailto:" + D.contact + "?subject=" + encodeURIComponent(sujet) + "&body=" + encodeURIComponent(corps);
    });
  }

  /* ---------- PASSEPORT ---------- */
  function pagePasseport() {
    var t = tampons();
    var liste = D.fresques.filter(tamponnable);
    var faits = liste.filter(function (f) { return t[f.slug]; });
    liste.sort(function (a, b) { return (t[b.slug] ? 1 : 0) - (t[a.slug] ? 1 : 0) || (t[a.slug] || "").localeCompare(t[b.slug] || ""); });
    vue.innerHTML = '<div class="page"><h1 style="font-size:40px">' + T("Mon passeport", "My passport") + "</h1>" +
      '<div class="bloc passeport-tete"><span class="surtitre" style="color:var(--turquoise)">' + T("Fresques tamponnées", "Stamped murals") + "</span>" +
      '<div style="display:flex;align-items:baseline;gap:8px"><span class="chiffre" style="font-size:52px">' + faits.length + '</span><span class="gris" style="font-size:18px">' + T("sur ", "of ") + liste.length + "</span></div>" +
      '<div class="jauge"><i style="width:' + Math.round(faits.length / liste.length * 100) + '%"></i></div>' +
      '<p class="petit" style="color:#E6E4DE">' + T("Va devant une fresque, ouvre sa fiche et appuie sur « Je suis devant : tamponner ». Ta position sert seulement à vérifier que tu es devant le mur.",
        "Go to a mural, open its page and tap “I'm here: stamp it”. Your location is only used to check you're at the wall.") + "</p></div>" +
      '<div class="grille-tampons">' + liste.map(function (f) {
        return '<a class="tampon' + (t[f.slug] ? " ok" : "") + '" href="#f/' + f.slug + '" aria-label="' + e(f.nom) + (t[f.slug] ? T(", tamponnée", ", stamped") : T(", pas encore tamponnée", ", not stamped yet")) + '">' +
          (f.photo ? '<img src="' + photo(f, true) + '" alt="" loading="lazy">' : "") + '<span class="q">' + e(f.nom) + "</span></a>";
      }).join("") + "</div>" +
      '<p class="note">' + T("Ton passeport est gardé sur ce téléphone. Bientôt : un compte pour le retrouver sur tous tes appareils.", "Your passport is kept on this phone. Coming soon: an account to find it on all your devices.") + "</p>" +
      '<button type="button" class="bouton contour" id="langue-btn2">' + T("Read the app in English", "Lire l'appli en français") + "</button>" +
      (MODE_TEST && faits.length ? '<button type="button" class="bouton contour" id="raz">' + T("Mode test : vider le passeport", "Test mode: empty the passport") + "</button>" : "") +
      "</div>";
    document.getElementById("langue-btn2").addEventListener("click", changerLangue);
    var raz = document.getElementById("raz");
    if (raz) raz.addEventListener("click", function () { stock("artmada.tampons", {}); route(); toast(T("Passeport vidé", "Passport emptied")); });
  }

  /* ---------- démarrage ---------- */
  document.documentElement.lang = LANGUE;
  dessinerOnglets();
  window.addEventListener("beforeinstallprompt", function (ev) {
    ev.preventDefault(); invitationInstall = ev;
    if (D && /^#?(accueil)?$/.test(location.hash)) route();
  });
  fetch("donnees.json").then(function (r) { return r.json(); }).then(function (d) {
    D = d;
    D.fresques.forEach(function (f) { F[f.slug] = f; });
    window.addEventListener("hashchange", function () { route.precedente = true; route(); });
    route();
    // Position silencieuse si déjà autorisée (pour afficher les distances).
    if (navigator.permissions && navigator.permissions.query) {
      navigator.permissions.query({ name: "geolocation" }).then(function (s) {
        if (s.state === "granted") localiser(null, true);
      }).catch(function () {});
    }
  }).catch(function () {
    vue.innerHTML = '<div class="page"><h1>Oups</h1><p>' + T("Impossible de charger les fresques. Vérifie ta connexion puis rouvre l'appli.", "Couldn't load the murals. Check your connection and reopen the app.") + "</p></div>";
  });

  if ("serviceWorker" in navigator && location.protocol === "https:") {
    window.addEventListener("load", function () { navigator.serviceWorker.register("sw.js").catch(function () {}); });
    // Nouvelle version en ligne : on recharge une fois pour l'afficher tout de suite.
    var dejaRecharge = false, avaitUneVersion = !!navigator.serviceWorker.controller;
    navigator.serviceWorker.addEventListener("controllerchange", function () {
      if (dejaRecharge || !avaitUneVersion) return; dejaRecharge = true; location.reload();
    });
  }
})();
