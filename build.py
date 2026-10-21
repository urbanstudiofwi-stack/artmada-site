#!/usr/bin/env python3
"""Génère le site ARTMADA (FR à la racine, EN dans /en/) à partir de data/*.json.

python3 build.py  ->  dist/
"""
import json, os, shutil, html, re
from pathlib import Path

ICI = Path(__file__).parent
DIST = ICI / "dist"
DATA = ICI / "data"

def charger(nom, defaut):
    p = DATA / nom
    return json.loads(p.read_text("utf-8")) if p.exists() else defaut

SITE = charger("site.json", {})
ARTISTES = charger("artistes.json", [])
FRESQUES = charger("fresques.json", [])
PROGRAMME = charger("programme.json", {})
PRESSE = charger("presse.json", {})
ARCHIVES = charger("archives.json", {})

A_PAR_SLUG = {a["slug"]: a for a in ARTISTES}
F_PAR_SLUG = {f["slug"]: f for f in FRESQUES}

e = html.escape

def t(lang, fr, en):
    return fr if lang == "fr" else en

def champ(obj, cle, lang):
    """obj[cle] en FR, obj[cle+'_en'] en EN (repli FR)."""
    if lang == "en" and obj.get(cle + "_en"):
        return obj[cle + "_en"]
    return obj.get(cle, "")

# ------------------------------------------------------------------ chemins

class Page:
    def __init__(self, lang, chemin):
        self.lang = lang
        self.chemin = chemin            # ex. "artistes/xan.html" (relatif à la langue)
        prof = chemin.count("/") + (1 if lang == "en" else 0)
        self.racine = "../" * prof      # vers la racine du site (assets)
        self.base = "../" * chemin.count("/")  # vers la racine de la langue

    def u(self, chemin):
        """Lien interne dans la même langue."""
        return self.base + chemin

    def a(self, chemin):
        return self.racine + "assets/" + chemin

    def autre_langue(self):
        if self.lang == "fr":
            return self.racine + "en/" + self.chemin
        return self.racine + self.chemin

# ------------------------------------------------------------------ gabarit

MENU = [
    ("festival.html", "Le festival", "The festival"),
    ("programme.html", "Programme", "Programme"),
    ("artistes/index.html", "Artistes", "Artists"),
    ("fresques/index.html", "Fresques & carte", "Murals & map"),
    ("visites.html", "Visites & ateliers", "Tours & workshops"),
    ("boutique.html", "Boutique", "Shop"),
]
MENU_DROITE = [
    ("archives.html", "Archives", "Archive"),
    ("presse.html", "Presse", "Press"),
]

MENU_COMPLET = [
    ("Le festival", "The festival", [("festival.html", "Édition #3", "Edition #3"), ("programme.html", "Programme", "Programme"),
                                      ("artistes/index.html", "Artistes", "Artists"), ("temps-forts-2026.html", "Temps forts 2026", "2026 highlights"),
                                      ("temps-forts-2024.html", "Temps forts 2024", "2024 highlights"), ("archives.html", "Archives", "Archive")]),
    ("Les fresques", "The murals", [("fresques/index.html", "Toutes les fresques", "All murals"), ("carte.html", "La carte", "The map"),
                                    ("visites.html", "Visites & ateliers", "Tours & workshops")]),
    ("Participer", "Get involved", [("benevoles.html", "Devenir bénévole", "Volunteer"), ("partenaires.html", "Partenaires", "Partners"),
                                    ("boutique.html", "Boutique", "Shop"),
                                    ("https://www.bizouk.com/events/details/atelier-graffiti-a-lurban-studio-avec-do/131478", "Réserver l'atelier", "Book the workshop")]),
    ("Infos", "Info", [("presse.html", "Presse", "Press"), ("infos.html", "Infos pratiques", "Practical info"), ("infos.html#contact", "Contact", "Contact")]),
]

def entete(p, actif):
    L = p.lang
    def lien(c, fr, en):
        cur = ' aria-current="page"' if actif == c else ""
        return f'<a href="{p.u(c)}"{cur}>{t(L, fr, en)}</a>'
    nav = "".join(lien(*m) for m in MENU)
    colonnes = ""
    for titre_fr, titre_en, liens in MENU_COMPLET:
        lis = ""
        for c, fr, en in liens:
            href = c if c.startswith("http") else p.u(c)
            ext = ' rel="noopener"' if c.startswith("http") else ""
            cur = ' aria-current="page"' if actif == c else ""
            lis += f'<li><a href="{href}"{ext}{cur}>{t(L, fr, en)}</a></li>'
        colonnes += f'<div class="gm-col"><p class="gm-titre">{t(L, titre_fr, titre_en)}</p><ul>{lis}</ul></div>'
    langue = t(L, "EN", "FR")
    langue_titre = t(L, "English version", "Version française")
    return f'''<a class="evitement" href="#contenu">{t(L, "Aller au contenu", "Skip to content")}</a>
<header class="entete">
  <div class="entete-in">
    <nav class="nav" aria-label="{t(L, 'Menu principal', 'Main menu')}">{nav}</nav>
    <a class="entete-logo" href="{p.u('index.html')}" aria-label="{t(L, 'ARTMADA Street Festival, accueil', 'ARTMADA Street Festival, home')}"><img src="{p.a('img/da/logo-400.webp')}" alt="ARTMADA Street Festival" width="400" height="132"></a>
    <div class="entete-droite">
      <a class="langue" href="{p.autre_langue()}" hreflang="{t(L, 'en', 'fr')}" lang="{t(L, 'en', 'fr')}" title="{langue_titre}">{langue}</a>
      <a class="bouton bouton-orange bouton-petit masque-petit" href="{p.u('benevoles.html')}">{t(L, 'Devenir bénévole', 'Volunteer')}</a>
      <button class="menu-bouton" id="menu-bouton" type="button" aria-expanded="false" aria-controls="grand-menu"><span class="burger" aria-hidden="true"></span>Menu</button>
    </div>
  </div>
</header>
<div class="grand-menu" id="grand-menu" role="dialog" aria-modal="true" aria-label="Menu" hidden>
  <div class="gm-haut">
    <a href="{p.u('index.html')}" class="gm-logo"><img src="{p.a('img/da/logo-400.webp')}" alt="ARTMADA Street Festival" width="400" height="132"></a>
    <div style="display:flex;gap:12px;align-items:center">
      <a class="langue langue-claire" href="{p.autre_langue()}" hreflang="{t(L, 'en', 'fr')}" lang="{t(L, 'en', 'fr')}" title="{langue_titre}">{langue}</a>
      <button class="gm-fermer" id="menu-fermer" type="button"><span aria-hidden="true">✕</span> {t(L, 'Fermer', 'Close')}</button>
    </div>
  </div>
  <nav class="gm-corps" aria-label="{t(L, 'Plan du site', 'Site map')}">{colonnes}</nav>
  <div class="gm-bas">
    <span class="gm-dates">{t(L, 'Édition #3 · 25 janv. → 4 févr. 2027 · Fort-de-France', 'Edition #3 · 25 Jan → 4 Feb 2027 · Fort-de-France')}</span>
    <span><a href="https://www.instagram.com/artmadastreetfestival972/" rel="noopener">Instagram</a> · <a href="mailto:contact@artmadastreetfestival.com">contact@artmadastreetfestival.com</a></span>
  </div>
</div>'''

def pied(p):
    L = p.lang
    def li(c, fr, en):
        return f'<li><a href="{p.u(c)}">{t(L, fr, en)}</a></li>'
    return f'''<footer class="pied">
  <div class="pied-in">
    <div style="display:flex;flex-direction:column;gap:14px">
      <span class="pied-logo"><img src="{p.a('img/da/logo-400.webp')}" alt="ARTMADA" width="400" height="132" loading="lazy"><img src="{p.a('img/da/street-festival.webp')}" alt="Street Festival" width="1000" height="199" loading="lazy" class="pied-script"></span>
      <p class="petit" style="max-width:340px">{t(L, "Le festival de street art de Fort-de-France, Martinique. Organisé par l'association NPL MADA PAINT, avec la Ville de Fort-de-France.", "The street art festival of Fort-de-France, Martinique. Organised by the NPL MADA PAINT association, with the City of Fort-de-France.")}</p>
    </div>
    <div><h2>{t(L, 'Le festival', 'The festival')}</h2><ul>
      {li('festival.html', 'Édition #3', 'Edition #3')}{li('programme.html', 'Programme', 'Programme')}{li('artistes/index.html', 'Artistes', 'Artists')}{li('fresques/index.html', 'Fresques & carte', 'Murals & map')}{li('archives.html', 'Archives', 'Archive')}
    </ul></div>
    <div><h2>{t(L, 'Participer', 'Get involved')}</h2><ul>
      {li('visites.html', 'Visites & ateliers', 'Tours & workshops')}{li('benevoles.html', 'Bénévoles', 'Volunteer')}{li('boutique.html', 'Boutique', 'Shop')}{li('partenaires.html', 'Partenaires', 'Partners')}{li('presse.html', 'Presse', 'Press')}{li('infos.html', 'Infos pratiques', 'Practical info')}
    </ul></div>
    <div><h2>Contact</h2><ul>
      <li><a href="mailto:contact@artmadastreetfestival.com">contact@<wbr>artmadastreetfestival.com</a></li>
      <li><a href="https://www.instagram.com/artmadastreetfestival972/" rel="noopener">Instagram</a></li>
      <li><a href="https://www.facebook.com/artmadastreetfestival" rel="noopener">Facebook</a></li>
      <li><a href="https://www.youtube.com/channel/UCjXDQ---HEdjzB3rwDdRp8Q" rel="noopener">YouTube</a></li>
    </ul></div>
  </div>
  <div class="pied-bas">
    <span>© 2027 NPL MADA PAINT · {t(L, 'Association loi 1901', 'Non-profit association')} · Fort-de-France, Martinique</span>
    <span><a href="{p.u('mentions-legales.html')}">{t(L, 'Mentions légales', 'Legal notice')}</a> · <a href="{p.u('confidentialite.html')}">{t(L, 'Confidentialité', 'Privacy')}</a></span>
  </div>
</footer>'''

SITE_URL = "https://artmadastreetfestival.com/"

# --- données structurées (schema.org) communes, réutilisées par les pages
ORGA = {
    "@type": "Organization", "@id": SITE_URL + "#npl-mada-paint",
    "name": "NPL MADA PAINT", "alternateName": "Mada Paint",
    "url": SITE_URL, "logo": SITE_URL + "assets/img/logo-noir.png",
    "email": "contact@artmadastreetfestival.com",
    "address": {"@type": "PostalAddress", "addressLocality": "Fort-de-France", "addressRegion": "Martinique", "addressCountry": "FR"},
    "sameAs": ["https://www.instagram.com/artmadastreetfestival972/", "https://www.facebook.com/artmadastreetfestival", "https://www.youtube.com/channel/UCjXDQ---HEdjzB3rwDdRp8Q"],
}
FESTIVAL_ID = SITE_URL + "#artmada-3"

def festival_ld(lang):
    """L'édition #3 (Festival + événement d'arts visuels)."""
    return {
        "@type": ["Festival", "VisualArtsEvent"], "@id": FESTIVAL_ID,
        "name": "ARTMADA Street Festival #3 · An Lot Chimen",
        "description": t(lang, "Troisième édition du festival de street art de Fort-de-France : fresques peintes en direct, ateliers, visites, soirées et block party.",
                         "Third edition of Fort-de-France's street art festival: murals painted live, workshops, tours, parties and a block party."),
        "startDate": "2027-01-25", "endDate": "2027-02-04",
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "isAccessibleForFree": True,
        "inLanguage": ["fr", "en"],
        "image": [SITE_URL + "assets/img/hd/a2-doudou.jpg", SITE_URL + "assets/img/partage.jpg"],
        "url": SITE_URL + ("" if lang == "fr" else "en/") + "festival.html",
        "location": {"@type": "Place", "name": "Fort-de-France",
                     "address": {"@type": "PostalAddress", "addressLocality": "Fort-de-France", "addressRegion": "Martinique", "postalCode": "97200", "addressCountry": "FR"}},
        "organizer": {"@id": ORGA["@id"]},
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR", "availability": "https://schema.org/InStock",
                   "url": SITE_URL + ("" if lang == "fr" else "en/") + "programme.html", "validFrom": "2026-10-19"},
    }

def fil_ld(p, fil):
    """Fil d'Ariane lisible par Google. fil = [(chemin ou None, nom), …] (le dernier = page courante)."""
    base = SITE_URL + ("" if p.lang == "fr" else "en/")
    items = [{"@type": "ListItem", "position": 1, "name": t(p.lang, "Accueil", "Home"), "item": base}]
    for i, (c, n) in enumerate(fil, start=2):
        it = {"@type": "ListItem", "position": i, "name": n}
        it["item"] = base + (c or p.chemin).replace("index.html", "")
        items.append(it)
    return {"@type": "BreadcrumbList", "itemListElement": items}

def bloc_ld(objets):
    if not objets:
        return ""
    data = {"@context": "https://schema.org", "@graph": objets}
    txt = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/ld+json">{txt}</script>\n'

def document(p, titre, description, corps, actif=None, image=None, titre_complet=None, ld=None, noindex=False):
    L = p.lang
    if not titre_complet:
        titre_complet = f"{titre} · ARTMADA Street Festival" if titre else t(L, "ARTMADA · Festival de street art de Fort-de-France, Martinique", "ARTMADA · Street art festival in Fort-de-France, Martinique")
    url_fr = SITE_URL + p.chemin.replace("index.html", "")
    url_en = SITE_URL + "en/" + p.chemin.replace("index.html", "")
    canon = url_fr if L == "fr" else url_en
    img = SITE_URL + "assets/" + (image or "img/partage.jpg")
    liens_langue = "" if noindex else f'''<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="fr" href="{url_fr}">
<link rel="alternate" hreflang="en" href="{url_en}">
<link rel="alternate" hreflang="x-default" href="{url_fr}">
'''
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    objets = [dict(ORGA)] + (ld or [])
    return f'''<!doctype html>
<html lang="{L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titre_complet)}</title>
<meta name="description" content="{e(description)}">
<meta name="google-site-verification" content="_sMru8SpsG50XIsu-UqVL83WAhu-A-Bk16MKLVzs-jw">
{robots}{liens_langue}<meta property="og:title" content="{e(titre_complet)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{img}">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="ARTMADA Street Festival">
<meta property="og:type" content="website">
<meta property="og:locale" content="{t(L, 'fr_FR', 'en_GB')}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#232427">
<link rel="icon" type="image/png" href="{p.a('favicon.png')}">
<link rel="apple-touch-icon" href="{p.a('apple-touch-icon.png')}">
<link rel="preload" href="{p.a('fonts/anton-latin-400-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p.a('css/style.css')}">
{bloc_ld(objets)}</head>
<body>
{entete(p, actif)}
<main id="contenu">
{corps}
</main>
{pied(p)}
<script src="{p.a('js/main.js')}" defer></script>
</body>
</html>
'''

PAGES = []   # (lang, chemin, html)

IMG_RE = re.compile(r'<img src="([^"]+?)\.(jpg|jpeg|png)"([^>]*)>')

def optimiser_images(html_txt):
    """Chaque photo JPG est servie en WebP (plus léger) avec repli JPG,
    et chargée en différé sauf si elle est marquée prioritaire."""
    def rempl(m):
        src, ext, reste = m.group(1), m.group(2), m.group(3)
        if "loading=" not in reste and "fetchpriority" not in reste and "logo" not in src:
            reste = ' loading="lazy"' + reste
        if "decoding=" not in reste:
            reste += ' decoding="async"'
        img = f'<img src="{src}.{ext}"{reste}>'
        if ext == "png":
            return img
        return f'<picture><source srcset="{src}.webp" type="image/webp">{img}</picture>'
    return IMG_RE.sub(rempl, html_txt)

def ecrire(p, contenu, indexer=True):
    dest = DIST / ("en" if p.lang == "en" else "") / p.chemin
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(optimiser_images(contenu), "utf-8")
    if indexer:
        PAGES.append(str(dest.relative_to(DIST)))

# ------------------------------------------------------------------ morceaux

def img_fresque(p, f, taille="", charge="lazy"):
    if f.get("photo"):
        return f'<img src="{p.a(f["photo"])}" alt="{e(alt_fresque(f, p.lang))}" loading="{charge}" width="960" height="720">'
    return f'<div class="sans-photo">{e(nom_artistes(f))}</div>'

def nom_artistes(f):
    noms = [A_PAR_SLUG[s]["nom"] if s in A_PAR_SLUG else s for s in f.get("artistes", [])] + f.get("avec", [])
    return " & ".join(noms) or f.get("artiste_libre", "")

def alt_fresque(f, lang):
    return t(lang, f"Fresque de {nom_artistes(f)}, ARTMADA #{f['edition']}, {f.get('lieu','Fort-de-France')}",
             f"Mural by {nom_artistes(f)}, ARTMADA #{f['edition']}, {f.get('lieu','Fort-de-France')}")

def vignette_fresque(p, f, lien=True):
    L = p.lang
    lieu = f.get("lieu") or "Fort-de-France"
    tags = f"e{f['edition']} " + " ".join("q-" + q for q in [f.get("quartier_slug", "")] if q)
    contenu = f'''<div class="photo">{img_fresque(p, f)}</div>
<span class="legende-f"><span class="nom">{e(nom_artistes(f))}</span><span class="lieu">{e(lieu)} · #{f['edition']}</span></span>'''
    if lien:
        contenu = f'<a href="{p.u("fresques/" + f["slug"] + ".html")}">{contenu}</a>'
    return f'<figure class="fresque" data-tags="{tags.strip()}">{contenu}</figure>'

def bloc_tete(p, fil, titre, chapo="", etiquette=""):
    L = p.lang
    fil_html = ""
    if fil:
        morceaux = [f'<a href="{p.u("index.html")}">{t(L, "Accueil", "Home")}</a>'] + [
            (f'<a href="{p.u(c)}">{e(n)}</a>' if c else e(n)) for c, n in fil]
        fil_html = f'<nav class="fil" aria-label="{t(L, "Fil d’Ariane", "Breadcrumb")}">' + " / ".join(morceaux) + "</nav>"
    et = f'<span class="etiquette" style="margin-bottom:18px">{e(etiquette)}</span>' if etiquette else ""
    ch = f'<p class="chapo">{chapo}</p>' if chapo else ""
    return f'<section class="cadre tete-page">{fil_html}<div style="display:flex;flex-direction:column">{et}<h1>{titre}</h1></div>{ch}</section>'

# ------------------------------------------------------------------ pages

def construire():
    import sys
    sys.modules.setdefault("build", sys.modules[__name__])
    import pages_contenu as PC
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copytree(ICI / "assets", DIST / "assets")
    # version WebP de chaque photo (même nom, extension .webp)
    from PIL import Image
    for jpg in (DIST / "assets" / "img").rglob("*.jpg"):
        Image.open(jpg).save(jpg.with_suffix(".webp"), "WEBP", quality=78, method=6)
    (DIST / "CNAME").write_text("artmadastreetfestival.com\n")
    (DIST / ".nojekyll").write_text("")
    for lang in ("fr", "en"):
        PC.toutes_les_pages(lang)
    (DIST / "404.html").write_text(optimiser_images(PC.page_404()), "utf-8")
    # sitemap : chaque page avec sa date de mise à jour et sa version dans l'autre langue
    import datetime
    jour = datetime.date.today().isoformat()
    urls = ""
    for x in PAGES:
        rel = x.replace("index.html", "")
        fr = rel[3:] if rel.startswith("en/") else rel
        urls += (f"<url><loc>{SITE_URL}{rel}</loc><lastmod>{jour}</lastmod>"
                 f'<xhtml:link rel="alternate" hreflang="fr" href="{SITE_URL}{fr}"/>'
                 f'<xhtml:link rel="alternate" hreflang="en" href="{SITE_URL}en/{fr}"/></url>')
    (DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">' + urls + "</urlset>", "utf-8")
    (DIST / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://artmadastreetfestival.com/sitemap.xml\n")
    print(f"{len(PAGES)} pages générées dans {DIST}")

if __name__ == "__main__":
    construire()
