// ARTMADA Street Festival — petits comportements du site
(function () {
  "use strict";

  // Grand menu (plein écran)
  var bouton = document.getElementById("menu-bouton");
  var menu = document.getElementById("grand-menu");
  var fermer = document.getElementById("menu-fermer");
  function ouvrir() {
    menu.hidden = false;
    document.body.classList.add("menu-ouvert");
    bouton.setAttribute("aria-expanded", "true");
    var premier = menu.querySelector(".gm-col a");
    if (premier) premier.focus();
  }
  function refermer() {
    menu.hidden = true;
    document.body.classList.remove("menu-ouvert");
    bouton.setAttribute("aria-expanded", "false");
    bouton.focus();
  }
  if (bouton && menu) {
    bouton.addEventListener("click", ouvrir);
    if (fermer) fermer.addEventListener("click", refermer);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !menu.hidden) refermer(); });
    menu.addEventListener("click", function (e) { if (e.target.tagName === "A") { document.body.classList.remove("menu-ouvert"); } });
  }

  // Trait sous l'en-tête quand on descend
  var entete = document.querySelector(".entete");
  if (entete) {
    var maj = function () { entete.classList.toggle("defile", window.scrollY > 8); };
    window.addEventListener("scroll", maj, { passive: true });
    maj();
  }

  // Filtres (fresques, artistes)
  document.querySelectorAll("[data-filtres]").forEach(function (groupe) {
    var cible = document.getElementById(groupe.getAttribute("data-filtres"));
    if (!cible) return;
    var boutons = groupe.querySelectorAll("button[data-f]");
    boutons.forEach(function (b) {
      b.addEventListener("click", function () {
        var f = b.getAttribute("data-f");
        boutons.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        cible.querySelectorAll("[data-tags]").forEach(function (el) {
          var tags = " " + el.getAttribute("data-tags") + " ";
          el.hidden = !(f === "tout" || tags.indexOf(" " + f + " ") > -1);
        });
      });
    });
  });
})();

// After movie : la vidéo (Google Drive) ne se charge qu'au clic
(function () {
  document.querySelectorAll(".video[data-video] .video-facade").forEach(function (b) {
    b.addEventListener("click", function () {
      var boite = b.parentNode;
      var f = document.createElement("iframe");
      f.src = boite.getAttribute("data-video");
      f.title = b.getAttribute("data-titre");
      f.allow = "autoplay; fullscreen";
      f.allowFullscreen = true;
      boite.innerHTML = "";
      boite.appendChild(f);
    });
  });
})();

// V2 : les éléments apparaissent quand on arrive dessus en défilant
(function () {
  var els = document.querySelectorAll(".rv");
  if (!els.length) return;
  if (!("IntersectionObserver" in window)) return;   // vieux navigateur : tout reste visible
  document.documentElement.classList.add("js");
  var obs = new IntersectionObserver(function (entrees) {
    entrees.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add("vu"); obs.unobserve(en.target); }
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
  els.forEach(function (el) { obs.observe(el); });
})();

// Boutique : le t-shirt qui tourne (Il tourne / Face / Dos) et le choix de la taille
(function () {
  document.querySelectorAll("[data-ts-vue]").forEach(function (b) {
    b.addEventListener("click", function () {
      var groupe = b.parentNode;
      var scene = groupe.previousElementSibling;
      if (!scene || !scene.hasAttribute("data-ts")) return;
      scene.setAttribute("data-vue", b.getAttribute("data-ts-vue"));
      groupe.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
    });
  });
  document.querySelectorAll("[data-produit]").forEach(function (prod) {
    var lien = prod.querySelector("[data-reserver]");
    var affiche = prod.querySelector("[data-taille-choisie]");
    var corps = prod.getAttribute("data-corps") || "";
    prod.querySelectorAll(".ts-taille").forEach(function (b) {
      b.addEventListener("click", function () {
        var t = b.getAttribute("data-taille");
        prod.querySelectorAll(".ts-taille").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        if (affiche) affiche.textContent = t;
        if (lien) {
          var texte = corps.replace(/(taille|size) M\b/, "$1 " + t);
          lien.href = "mailto:" + prod.getAttribute("data-mail") + "?subject=" + encodeURIComponent(prod.getAttribute("data-sujet")) + "&body=" + encodeURIComponent(texte);
        }
      });
    });
  });
})();
