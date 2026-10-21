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

// Apparition au défilement : blocs (.rv) et gros titres mot par mot (.anim-titre)
(function () {
  if (!("IntersectionObserver" in window)) return;   // vieux navigateur : tout reste visible
  document.documentElement.classList.add("js");
  document.querySelectorAll(".anim-titre").forEach(function (h) {
    if (h.querySelector(".mot-anim")) return;
    var mots = h.textContent.trim().split(/\s+/);
    h.setAttribute("aria-label", h.textContent.trim());
    h.innerHTML = mots.map(function (m, i) {
      return '<span class="mot-anim" aria-hidden="true" style="transition-delay:' + (i * 0.09) + 's">' + m.replace(/[<>&]/g, "") + "</span>";
    }).join(" ");
  });
  var obs = new IntersectionObserver(function (entrees) {
    entrees.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add("vu"); obs.unobserve(en.target); }
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
  document.querySelectorAll(".rv, .anim-titre").forEach(function (el) { obs.observe(el); });
})();

// Vidéo d'accueil (after movie en noir et blanc) : chargée seulement si utile
(function () {
  var v = document.querySelector(".v3-video");
  if (!v) return;
  var bouton = document.querySelector("[data-video-pause]");
  var calme = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var eco = navigator.connection && (navigator.connection.saveData || /2g/.test(navigator.connection.effectiveType || ""));
  if (calme || eco) { if (bouton) bouton.hidden = true; return; }   // on garde l'image fixe
  v.src = window.innerWidth < 700 ? v.getAttribute("data-src-petit") : v.getAttribute("data-src");
  v.muted = true;
  var p = v.play(); if (p && p.catch) p.catch(function () {});
  if (bouton) bouton.addEventListener("click", function () {
    if (v.paused) { v.play(); bouton.setAttribute("aria-pressed", "false"); }
    else { v.pause(); bouton.setAttribute("aria-pressed", "true"); }
  });
})();

// Newsletter : en attendant un outil d'envoi, l'inscription part par mail
(function () {
  document.querySelectorAll("[data-news]").forEach(function (f) {
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var mail = f.querySelector("input[type=email]").value.trim();
      if (!mail) return;
      window.location.href = "mailto:" + f.getAttribute("data-mail") + "?subject=" + encodeURIComponent(f.getAttribute("data-sujet")) + "&body=" + encodeURIComponent(f.getAttribute("data-corps") + " " + mail);
      if (!f.querySelector(".news-merci")) {
        var m = document.createElement("p"); m.className = "news-merci";
        m.textContent = document.documentElement.lang === "en" ? "Your mail app opens: just press send." : "Ta messagerie s'ouvre : il ne reste qu'à envoyer.";
        f.appendChild(m);
      }
    });
  });
})();

// « Mettre ARTMADA sur l'écran d'accueil »
(function () {
  var invite = null;
  var bouton = document.querySelector("[data-installer]");
  var aide = document.querySelector("[data-installer-aide]");
  if (!bouton) return;
  if (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches) { bouton.hidden = true; return; }
  window.addEventListener("beforeinstallprompt", function (e) { e.preventDefault(); invite = e; });
  bouton.addEventListener("click", function () {
    if (invite) { invite.prompt(); invite = null; }
    else if (aide) { aide.hidden = false; }
  });
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

// Fresques en fond : la photo glisse un peu moins vite que le texte (profondeur)
(function () {
  var fonds = document.querySelectorAll(".fond-mur img");
  if (!fonds.length) return;
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var attente = false;
  function maj() {
    attente = false;
    var h = window.innerHeight;
    fonds.forEach(function (img) {
      var r = img.parentNode.getBoundingClientRect();
      if (r.bottom < -100 || r.top > h + 100) return;
      var d = (r.top + r.height / 2 - h / 2) / h;   // -1 → 1 environ
      img.style.transform = "translateY(" + (-8 - d * 8).toFixed(2) + "%)";
    });
  }
  window.addEventListener("scroll", function () { if (!attente) { attente = true; requestAnimationFrame(maj); } }, { passive: true });
  window.addEventListener("resize", maj);
  maj();
})();
