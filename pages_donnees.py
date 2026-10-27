"""Pages construites à partir des données : artistes, fresques, carte, archives, presse."""
from build import *  # noqa: F401,F403
from urllib.parse import quote
from pages_contenu import P, T, MAIL, INSTA, bloc_lieux

CREAPOLIS = "https://www.creapolis.io/tracks/festival-artmada"
REGIONS = {"martinique": ("Martinique", "Martinique"), "caraibe": ("Caraïbe", "Caribbean"), "international": ("International", "International")}
ANNEE = {1: "2024", 2: "2026"}
def credit(p, f):
    if f.get("credit_photo"):
        cp = f["credit_photo"]
        if cp.startswith("Drone"):  # crédit complet déjà écrit (ex. « Drone : Noisz »)
            return cp if p.lang == "fr" else cp.replace("Drone :", "Drone:")
        return "Photo : " + cp if p.lang == "fr" else "Photo: " + cp
    if f["edition"] == 2:
        return T(p, "Photo : Shaman", "Photo: Shaman")
    return "Photo © ARTMADA / NPL MADA PAINT"

def fresques_de(slug):
    # la Jam (fresque collective) n'est pas rangée dans les pages artistes
    return [f for f in FRESQUES if slug in f["artistes"] and not f.get("collectif")]

def signature(f, p=None):
    if p is not None and p.lang == "en" and f.get("signature_en"):
        return f["signature_en"]
    return f.get("signature") or nom_artistes(f)

def dest(f):
    if f.get("gps"):
        return f["gps"].replace(" ", "")
    return quote(f"{f['lieu']}, {f.get('ville', 'Fort-de-France')}, Martinique")

def maps(f):
    """Itinéraire à pied jusqu'à la fresque (Google Maps)."""
    return "https://www.google.com/maps/dir/?api=1&amp;travelmode=walking&amp;destination=" + dest(f)

def parcours_url(etapes):
    pts = [f["gps"].replace(" ", "") for f in etapes]
    u = "https://www.google.com/maps/dir/?api=1&amp;travelmode=walking&amp;origin=" + pts[0] + "&amp;destination=" + pts[-1]
    if len(pts) > 2:
        u += "&amp;waypoints=" + quote("|".join(pts[1:-1]), safe=",")
    return u

def distance_km(etapes):
    import math
    tot = 0
    for a, b in zip(etapes, etapes[1:]):
        la1, lo1 = map(float, a["gps"].split(",")); la2, lo2 = map(float, b["gps"].split(","))
        dla = math.radians(la2 - la1); dlo = math.radians(lo2 - lo1)
        h = math.sin(dla / 2) ** 2 + math.cos(math.radians(la1)) * math.cos(math.radians(la2)) * math.sin(dlo / 2) ** 2
        tot += 6371 * 2 * math.asin(math.sqrt(h))
    return tot * 1.3  # les rues ne vont pas en ligne droite

def liens_artistes(p, f):
    # « avec » : artistes sans page sur le site (nom affiché, pas de lien)
    return " & ".join([f'<a href="{p.u("artistes/" + s + ".html")}">{e(A_PAR_SLUG[s]["nom"])}</a>' for s in f["artistes"]] + [e(n) for n in f.get("avec", [])])

# ------------------------------------------------------------ SEO : titres et données structurées

def lieu_court(f):
    ville = f.get("ville", "Fort-de-France")
    return ville if f["secteur"] == ville else f"{f['secteur']}, {ville}"

def de(nom):
    """« de Xän » / « d'Aurélie »"""
    return ("d'" if nom[:1].lower() in "aeiouyéèêàâîïôûh" else "de ") + nom

def titre_fresque(p, f):
    """Titre unique de la page d'une fresque (ce qui s'affiche dans Google)."""
    if f.get("collectif"):
        return T(p, f"Mur de la Jam, fresque collective · {lieu_court(f)} | ARTMADA",
                 f"The Jam Wall, collective mural · {lieu_court(f)} | ARTMADA")
    sig = signature(f, p)
    if f.get("titre"):
        return T(p, f"« {f['titre']} », fresque {de(sig)} · {f.get('ville', 'Fort-de-France')} | ARTMADA",
                 f"“{f['titre']}”, mural by {sig} · {f.get('ville', 'Fort-de-France')} | ARTMADA")
    return T(p, f"Fresque {de(sig)} · {lieu_court(f)} | ARTMADA", f"Mural by {sig} · {lieu_court(f)} | ARTMADA")

def personne_id(slug):
    return SITE_URL + "artistes/" + slug + ".html#artiste"

def oeuvre_id(f):
    return SITE_URL + "fresques/" + f["slug"] + ".html#oeuvre"

def personne_ld(a):
    d = {"@type": "Person", "@id": personne_id(a["slug"]), "name": a["nom"], "jobTitle": "Street artist", "knowsAbout": ["Street art", "Graffiti", "Muralisme"]}
    liens = []
    if a.get("instagram"):
        liens.append("https://www.instagram.com/" + a["instagram"] + "/")
    if a.get("site"):
        liens.append("https://" + a["site"])
    if liens:
        d["sameAs"] = liens
    return d

def oeuvre_ld(p, f):
    L = p.lang
    nom = f.get("titre") or (T(p, "Mur de la Jam", "The Jam Wall") if f.get("collectif") else T(p, f"Fresque {de(signature(f, p))}", f"Mural by {signature(f, p)}"))
    d = {"@type": "VisualArtwork", "@id": oeuvre_id(f), "name": nom,
         "url": SITE_URL + ("" if L == "fr" else "en/") + "fresques/" + f["slug"] + ".html",
         "artform": T(p, "Fresque murale (street art)", "Mural (street art)"),
         "dateCreated": ANNEE[f["edition"]], "inLanguage": L,
         "creator": [{"@id": personne_id(s), "@type": "Person", "name": A_PAR_SLUG[s]["nom"]} for s in f["artistes"]]
                    + [{"@type": "Person", "name": n} for n in f.get("avec", [])],
         "contentLocation": {"@type": "Place", "name": f["lieu"],
                             "address": {"@type": "PostalAddress", "streetAddress": f["lieu"], "addressLocality": f.get("ville", "Fort-de-France"),
                                         "addressRegion": "Martinique", "addressCountry": "FR"}},
         "isAccessibleForFree": True,
         "description": (champ(f, "description", L).split("\n")[0] or T(p, f"Fresque réalisée pour ARTMADA #{f['edition']} ({ANNEE[f['edition']]}), {f['lieu']}, {f.get('ville', 'Fort-de-France')}.",
                                                                     f"Mural painted for ARTMADA #{f['edition']} ({ANNEE[f['edition']]}), {f['lieu']}, {f.get('ville', 'Fort-de-France')}."))}
    if f.get("gps"):
        la, lo = f["gps"].replace(" ", "").split(",")
        d["contentLocation"]["geo"] = {"@type": "GeoCoordinates", "latitude": float(la), "longitude": float(lo)}
    if f.get("photo"):
        d["image"] = {"@type": "ImageObject", "url": SITE_URL + "assets/" + f["photo"], "creditText": credit(p, f)}
    if f.get("titre"):
        d["alternateName"] = T(p, f"Fresque {de(signature(f, p))}", f"Mural by {signature(f, p)}")
    return d

def vignette(p, f):
    L = p.lang
    titre = f'<span class="gris" style="font-size:14px">{e(f["titre"])}</span>' if f.get("titre") else ""
    return f'''<figure class="fresque" data-tags="e{f['edition']}"><a href="{p.u('fresques/' + f['slug'] + '.html')}">
<div class="photo"><img src="{p.a(f['photo'])}" alt="{e(alt_fresque(f, L))}" loading="lazy" width="1600" height="900"></div>
<span class="legende-f"><span class="nom">{e(signature(f, p))}</span><span class="lieu">{e(f['secteur'])} · #{f['edition']}{T(p, " · disparue", " · gone") if f.get("disparue") else ""}</span></span>{titre}</a></figure>'''

# ============================================================ ARTISTES

def artistes_index(p):
    L = p.lang
    tri = sorted(ARTISTES, key=lambda a: a["nom"].lower().replace("é", "e"))
    cartes = ""
    for a in tri:
        fs = [f for f in fresques_de(a["slug"]) if f.get("photo")]
        tags = a["region"] + " " + " ".join(f"e{x}" for x in a["editions"])
        eds = " · ".join(f"#{x}" for x in a["editions"])
        visuel = (f'<img src="{p.a(fs[0]["photo"])}" alt="{e(alt_fresque(fs[0], L))}" loading="lazy" width="1600" height="900">'
                  if fs else f'<div class="sans-photo">{e(a["nom"])}</div>')
        cartes += f'''<figure class="fresque" data-tags="{tags}"><a href="{p.u('artistes/' + a['slug'] + '.html')}">
<div class="photo">{visuel}</div>
<span class="legende-f"><span class="nom">{e(a['nom'])}</span><span class="lieu">{e(champ(a, 'origine', L))} · {eds}</span></span></a></figure>'''
    filtres = "".join(f'<button type="button" data-f="{k}" aria-pressed="false">{T(p, *v)}</button>' for k, v in REGIONS.items())
    nb = len(ARTISTES)
    corps = f'''
{bloc_tete(p, [(None, T(p, 'Artistes', 'Artists'))], T(p, 'Les artistes', 'The artists'), T(p, f"{nb} artistes ont peint pour ARTMADA : des graffeurs du collectif Mada Paint, des artistes de Martinique, de la Caraïbe et du monde entier. Les artistes de l'édition #3 seront annoncés bientôt.", f"{nb} artists have painted for ARTMADA: graffiti writers from the Mada Paint collective, artists from Martinique, the Caribbean and around the world. Edition #3 artists will be announced soon."), T(p, 'Éditions #1 et #2', 'Editions #1 and #2'))}
<section class="cadre" style="padding-bottom:clamp(64px,8vw,120px)">
  <div class="filtres" data-filtres="grille-artistes" role="group" aria-label="{T(p, 'Filtrer', 'Filter')}">
    <button type="button" data-f="tout" aria-pressed="true">{T(p, 'Tous', 'All')}</button>{filtres}
    <button type="button" data-f="e1" aria-pressed="false">#1 · 2024</button><button type="button" data-f="e2" aria-pressed="false">#2 · 2026</button>
  </div>
  <div class="g4" id="grille-artistes">{cartes}</div>
</section>'''
    ecrire(p, document(p, T(p, "Artistes", "Artists"), T(p, "Les artistes d'ARTMADA Street Festival : Martinique, Caraïbe et international.", "The artists of ARTMADA Street Festival: Martinique, the Caribbean and international."), corps, actif="artistes/index.html"))

def artiste_page(p, a):
    L = p.lang
    fs = fresques_de(a["slug"])
    avec = [f for f in fs if f.get("photo")]
    visuel = ""
    if avec:
        visuel = f'<div class="visuel"><img src="{p.a(avec[0]["photo"])}" alt="{e(alt_fresque(avec[0], L))}" width="1600" height="900" fetchpriority="high"></div><p class="credit">{e(signature(avec[0], p))} · ARTMADA #{avec[0]["edition"]} · {credit(p, avec[0])}</p>'
    else:
        visuel = f'<div class="visuel"><div class="sans-photo" style="aspect-ratio:4/3">{e(a["nom"])}</div></div>'
    lignes = f'<div><dt>{T(p, "Origine", "From")}</dt><dd>{e(champ(a, "origine", L))}</dd></div>'
    lignes += f'<div><dt>{T(p, "Éditions", "Editions")}</dt><dd>{" · ".join(f"ARTMADA #{x} ({ANNEE[x]})" for x in a["editions"])}</dd></div>'
    if a.get("collectif"):
        lignes += f'<div><dt>{T(p, "Collectif", "Collective")}</dt><dd>{e(a["collectif"])}</dd></div>'
    if a.get("instagram"):
        lignes += f'<div><dt>Instagram</dt><dd><a href="https://www.instagram.com/{e(a["instagram"])}/" rel="noopener">@{e(a["instagram"])}</a></dd></div>'
    if a.get("site"):
        lignes += f'<div><dt>{T(p, "Site", "Website")}</dt><dd><a href="https://{e(a["site"])}" rel="noopener">{e(a["site"])}</a></dd></div>'
    autres = "".join(vignette(p, f) for f in avec)
    sans = [f for f in fs if not f.get("photo")]
    liste_sans = ""
    if sans:
        liste_sans = '<ul class="lignes" style="margin-top:24px">' + "".join(
            f'<li><a href="{p.u("fresques/" + f["slug"] + ".html")}">{e(f["lieu"])}</a><span class="meta">ARTMADA #{f["edition"]} · {ANNEE[f["edition"]]}</span></li>' for f in sans) + "</ul>"
    i = ARTISTES.index(a)
    suiv = ARTISTES[(i + 1) % len(ARTISTES)]
    corps = f'''
{bloc_tete(p, [('artistes/index.html', T(p, 'Artistes', 'Artists')), (None, a['nom'])], e(a['nom']), "", T(p, *REGIONS[a['region']]))}
<section class="cadre">
  <div class="fiche-tete">
    <div>{visuel}</div>
    <div class="fiche-infos">
      <p class="bio">{e(champ(a, 'bio', L))}</p>
      <dl class="tableau-infos">{lignes}</dl>
    </div>
  </div>
</section>
<section class="cadre" style="padding-top:clamp(56px,7vw,96px);padding-bottom:clamp(64px,8vw,120px)">
  {(f'<h2 class="titre-moyen" style="margin-bottom:24px">' + T(p, 'Ses fresques ARTMADA', 'ARTMADA murals') + '</h2>') if fs else ''}
  <div class="g2">{autres}</div>{liste_sans}
  <div class="pied-fiche"><a class="lien-fleche" href="{p.u('artistes/index.html')}">← {T(p, 'Tous les artistes', 'All artists')}</a><a class="lien-fleche" href="{p.u('artistes/' + suiv['slug'] + '.html')}">{e(suiv['nom'])} →</a></div>
</section>'''
    desc = champ(a, "bio", L)
    if len(desc) > 155:
        desc = desc[:152].rsplit(" ", 1)[0] + "…"
    orig = champ(a, "origine", L).split(" (")[0]
    titre_page = T(p, f"{a['nom']}, artiste street art · {orig} | ARTMADA", f"{a['nom']}, street artist · {orig} | ARTMADA")
    pers = personne_ld(a)
    pers["description"] = champ(a, "bio", L)
    pers["url"] = SITE_URL + ("" if L == "fr" else "en/") + "artistes/" + a["slug"] + ".html"
    if avec:
        pers["image"] = SITE_URL + "assets/" + avec[0]["photo"]
    pers["subjectOf"] = [{"@id": oeuvre_id(f)} for f in fs]
    ld = [pers, fil_ld(p, [("artistes/index.html", T(p, "Artistes", "Artists")), (None, a["nom"])])]
    ecrire(p, document(p, a["nom"], desc, corps, actif="artistes/index.html", image=avec[0]["photo"] if avec else None, titre_complet=titre_page, ld=ld))

# ============================================================ FRESQUES

def fresques_index(p):
    L = p.lang
    avec = [f for f in FRESQUES if f.get("photo")]
    grille = "".join(vignette(p, f) for f in avec)
    toutes = ""
    for ed in (2, 1):
        lignes = "".join(f'<li data-tags="e{f["edition"]}"><a href="{p.u("fresques/" + f["slug"] + ".html")}">{e(signature(f, p))}{(" · <i>" + e(f["titre"]) + "</i>") if f.get("titre") else ""}{T(p, " (disparue)", " (gone)") if f.get("disparue") else ""}</a><span class="meta">{e(f["secteur"])}</span></li>'
                         for f in FRESQUES if f["edition"] == ed)
        toutes += f'<div><h3 class="titre-moyen" style="font-size:30px;margin-bottom:12px">ARTMADA #{ed} · {ANNEE[ed]}</h3><ul class="lignes">{lignes}</ul></div>'
    noms = "".join(f'<li><a href="{p.u("artistes/" + a["slug"] + ".html")}">{e(a["nom"])}</a><small>{" ".join("#" + str(x) for x in a["editions"])}</small></li>'
                   for a in sorted(ARTISTES, key=lambda a: a["nom"].lower().replace("é", "e")))
    corps = f'''
{bloc_tete(p, [(None, T(p, 'Fresques', 'Murals'))], T(p, 'Les fresques', 'The murals'), T(p, "Elles restent sur les murs. On peut aller les voir toute l'année, à pied, gratuitement.", "They stay on the walls. You can see them all year round, on foot, for free."), T(p, 'Galerie à ciel ouvert', 'Open-air gallery'))}
<section class="cadre" style="padding-bottom:clamp(40px,5vw,64px)">
  <div class="texte-5-7 trait-haut" style="align-items:end">
    <div class="chiffres">
      <div><b>40</b><span>{T(p, 'fresques', 'murals')}</span></div>
      <div><b>2 650 m²</b><span>{T(p, 'de murs peints', 'painted')}</span></div>
      <div><b>{len(ARTISTES)}</b><span>{T(p, 'artistes', 'artists')}</span></div>
    </div>
    <div class="boutons" style="justify-content:flex-end"><a class="bouton" href="{p.u('carte.html')}">{T(p, 'Voir la carte', 'See the map')}</a><a class="bouton bouton-contour" href="{p.u('visites.html')}">{T(p, 'Visite guidée', 'Guided tour')}</a></div>
  </div>
</section>
<section style="padding:0 clamp(12px,1.5vw,20px) clamp(56px,7vw,96px)">
  <div style="max-width:1400px;margin:0 auto">
    <div class="filtres" data-filtres="grille-fresques" role="group" aria-label="{T(p, 'Filtrer par édition', 'Filter by edition')}" style="padding:0 clamp(8px,1.5vw,20px)">
      <button type="button" data-f="tout" aria-pressed="true">{T(p, 'Toutes', 'All')}</button><button type="button" data-f="e2" aria-pressed="false">#2 · 2026</button><button type="button" data-f="e1" aria-pressed="false">#1 · 2024</button>
    </div>
    <div class="g3" id="grille-fresques">{grille}</div>
  </div>
</section>
<section class="cadre" style="padding-bottom:clamp(56px,7vw,96px)">
  <div class="entete-section"><h2 class="titre-section">{T(p, 'Toutes les fresques', 'Every mural')}</h2><p>{T(p, 'La liste complète, édition par édition. Chaque fresque a sa fiche.', 'The full list, edition by edition. Each mural has its own page.')}</p></div>
  <div class="g2" style="gap:40px">{toutes}</div>
</section>
<section class="cadre" style="padding-bottom:clamp(64px,8vw,120px)">
  <div class="entete-section"><h2 class="titre-moyen">{T(p, 'Par artiste', 'By artist')}</h2></div>
  <ul class="liste-artistes">{noms}</ul>
</section>'''
    ecrire(p, document(p, T(p, "Fresques", "Murals"), T(p, "Toutes les fresques d'ARTMADA à Fort-de-France : photos, lieux, artistes, éditions 2024 et 2026.", "Every ARTMADA mural in Fort-de-France: photos, locations, artists, 2024 and 2026 editions."), corps, actif="fresques/index.html"))

def fresque_page(p, f, i):
    L = p.lang
    titre = f.get("titre") or ""
    h1 = e(signature(f, p))
    if f.get("photo"):
        visuel = f'<div class="visuel"><img src="{p.a(f["photo"])}" alt="{e(alt_fresque(f, L))}" width="1600" height="900" fetchpriority="high"></div><p class="credit">{credit(p, f)}</p>'
    else:
        visuel = f'<div class="visuel"><div class="sans-photo" style="aspect-ratio:4/3">{T(p, "Photo à venir", "Photo coming soon")}</div></div>'
    desc = champ(f, "description", L)
    paras = "".join(f"<p>{e(x.strip())}</p>" for x in desc.split("\n") if x.strip())
    if f.get("collectif"):
        infos = f'<div><dt>{T(p, "Artistes", "Artists")}</dt><dd>{T(p, "Tous les artistes martiniquais du festival", "All the festival\'s Martinican artists")}</dd></div>'
        avec_liens = ", ".join('<a href="' + p.u("artistes/" + s + ".html") + '">' + e(A_PAR_SLUG[s]["nom"]) + '</a>' for s in f["artistes"])
        infos += f'<div><dt>{T(p, "Avec", "With")}</dt><dd>{avec_liens}</dd></div>'
    else:
        infos = f'<div><dt>{T(p, "Artiste", "Artist") if len(f["artistes"]) + len(f.get("avec", [])) == 1 else T(p, "Artistes", "Artists")}</dt><dd>{liens_artistes(p, f)}</dd></div>'
    if titre:
        infos += f'<div><dt>{T(p, "Titre", "Title")}</dt><dd><i>{e(titre)}</i></dd></div>'
    infos += f'<div><dt>{T(p, "Édition", "Edition")}</dt><dd>ARTMADA #{f["edition"]} · {ANNEE[f["edition"]]}</dd></div>'
    infos += f'<div><dt>{T(p, "Lieu", "Location")}</dt><dd>{e(f["lieu"])}, {e(f.get("ville", "Fort-de-France"))}</dd></div>'
    infos += f'<div><dt>{T(p, "Quartier", "Area")}</dt><dd>{e(f["secteur"])}</dd></div>'
    if f.get("surface"):
        infos += f'<div><dt>{T(p, "Surface", "Size")}</dt><dd>{e(f["surface"])} m²</dd></div>'
    if f.get("disparue"):
        infos += f'<div><dt>{T(p, "État", "Status")}</dt><dd><b>{T(p, "Fresque disparue", "Mural no longer visible")}</b> · {T(p, "on garde ici sa trace", "we keep a record of it here")}</dd></div>'
    else:
        infos += f'<div><dt>{T(p, "Accès", "Access")}</dt><dd>{T(p, "Visible depuis la rue, gratuit", "Visible from the street, free")}</dd></div>'
    histoire = ""
    if paras:
        source = f'<p class="petit gris">{T(p, "Texte", "Text")} : {e(f["texte_source"])}{T(p, " (parcours Creapolis commandé par ARTMADA)", " (Creapolis trail commissioned by ARTMADA)")}</p>' if f.get("texte_source") else ""
        histoire = f'''<section class="cadre" style="padding-top:clamp(48px,6vw,80px)">
  <div class="texte-5-7 trait-haut">
    <h2 class="titre-moyen">{T(p, "L'histoire de la fresque", "The story of the mural")}</h2>
    <div class="prose" style="font-size:18px">{paras}{source}</div>
  </div>
</section>'''
    bios = ""
    if not f.get("signature"):
        for s_ in f["artistes"]:
            a_ = A_PAR_SLUG[s_]
            bios += f'<div style="display:flex;flex-direction:column;gap:10px"><h3 style="font-size:26px">{e(a_["nom"])}</h3><p>{e(champ(a_, "bio", L))}</p><a class="lien-fleche" style="align-self:flex-start" href="{p.u("artistes/" + s_ + ".html")}">{T(p, "Voir sa page", "See artist page")}</a></div>'
    artiste_bloc = f'''<section class="cadre" style="padding-top:clamp(48px,6vw,80px)">
  <div class="texte-5-7 trait-haut">
    <h2 class="titre-moyen">{T(p, "L'artiste", "The artist") if len(f["artistes"]) == 1 else T(p, "Les artistes", "The artists")}</h2>
    <div style="display:flex;flex-direction:column;gap:28px">{bios}</div>
  </div>
</section>''' if bios else ""
    autres = [x for x in FRESQUES if x["slug"] != f["slug"] and x.get("photo") and (x["secteur"] == f["secteur"] or x["edition"] == f["edition"])][:3]
    suiv = FRESQUES[(i + 1) % len(FRESQUES)]
    prec = FRESQUES[i - 1]
    corps = f'''
{bloc_tete(p, [('fresques/index.html', T(p, 'Fresques', 'Murals')), (None, signature(f, p))], h1, T(p, "Cette fresque n'existe plus. On garde ici sa trace et son histoire.", "This mural no longer exists. We keep its story here.") if f.get("disparue") else "", f"ARTMADA #{f['edition']} · {ANNEE[f['edition']]}" + (T(p, " · disparue", " · gone") if f.get("disparue") else ""))}
<section class="cadre">
  <div class="fiche-tete">
    <div>{visuel}</div>
    <div class="fiche-infos">
      {f'<p style="font-family:var(--titre);font-size:clamp(28px,3vw,40px);line-height:1;text-transform:uppercase">{e(titre)}</p>' if titre else ''}
      <dl class="tableau-infos">{infos}</dl>
      <div class="boutons">{'' if f.get("disparue") else f'<a class="bouton" href="{maps(f)}" rel="noopener" target="_blank">' + T(p, 'Y aller à pied', 'Walk there') + '</a>'}<a class="bouton bouton-contour" href="{p.u('carte.html')}">{T(p, 'La carte des fresques', 'Mural map')}</a></div>
      {f'<a class="lien-fleche" style="align-self:flex-start" href="#histoire">' + T(p, "Lire l'histoire de la fresque ↓", "Read the story of the mural ↓") + '</a>' if paras else ''}
    </div>
  </div>
</section>
<div id="histoire"></div>{histoire}{artiste_bloc}
<section class="cadre" style="padding-top:clamp(56px,7vw,96px);padding-bottom:clamp(64px,8vw,120px)">
  <h2 class="titre-moyen" style="margin-bottom:24px">{T(p, 'À voir aussi', 'See also')}</h2>
  <div class="g3">{"".join(vignette(p, x) for x in autres)}</div>
  <div class="pied-fiche"><a class="lien-fleche" href="{p.u('fresques/' + prec['slug'] + '.html')}">← {e(signature(prec, p))}</a><a class="lien-fleche" href="{p.u('fresques/' + suiv['slug'] + '.html')}">{e(signature(suiv, p))} →</a></div>
</section>'''
    d = T(p, f"Fresque {de(signature(f, p))} pour ARTMADA #{f['edition']} ({ANNEE[f['edition']]}), {f['lieu']}, {f.get('ville', 'Fort-de-France')}.",
          f"Mural by {signature(f, p)} for ARTMADA #{f['edition']} ({ANNEE[f['edition']]}), {f['lieu']}, {f.get('ville', 'Fort-de-France')}.")
    ecrire(p, document(p, "", d, corps, actif="fresques/index.html", image=f.get("photo") or None,
                       titre_complet=titre_fresque(p, f), ld=[oeuvre_ld(p, f), fil_ld(p, [("fresques/index.html", T(p, "Fresques", "Murals")), (None, signature(f, p))])]))

# ============================================================ CARTE

PARCOURS = [
    ("centre", "Pointe Simon et centre-ville", "Pointe Simon & city centre",
     "Du front de mer à la rue Moreau de Jonnès : le Mur de la Jam, les bulles de Tempo Nok, Sitou, Roxane Shade, Jaddict…",
     "From the seafront to rue Moreau de Jonnès: the Jam Wall, Tempo Nok's bubbles, Sitou, Roxane Shade, Jaddict…"),
    ("tom", "Rue Victor Sévère et Terres-Sainville", "Rue Victor Sévère & Terres-Sainville",
     "Le cœur du festival 2026 autour du TOM : Yelow, Curtis Hylton, Doudou Style, Oshea, Mounlan, puis Les Fortes de France de Carole B.",
     "The heart of the 2026 festival around the TOM: Yelow, Curtis Hylton, Doudou Style, Oshea, Mounlan, then Carole B.'s Les Fortes de France."),
    ("est", "Clarac, Sainte-Thérèse et Canal Alaric", "Clarac, Sainte-Thérèse & Canal Alaric",
     "De la cité Clarac au canal : l'ancien cinéma Olympia, Difé Pri d'Oshea, le lettrage de Wuna, Rayza, Al Pacman…",
     "From Cité Clarac to the canal: the old Olympia cinema, Oshea's Difé Pri, Wuna's lettering, Rayza, Al Pacman…"),
]
ETAPES_PARCOURS = {"centre": range(1, 11), "tom": range(11, 18), "est": range(18, 29)}

def carte(p):
    L = p.lang
    par_etape = {f["etape"]: f for f in FRESQUES if f.get("etape")}
    points = []
    for f in FRESQUES:
        if not f.get("gps"):
            continue
        la, lo = f["gps"].split(",")
        points.append({"lat": float(la), "lng": float(lo), "n": signature(f, p), "t": f.get("titre", ""), "e": f["edition"],
                       "u": p.u("fresques/" + f["slug"] + ".html"), "i": p.a(f["photo"]) if f.get("photo") else "",
                       "m": maps(f).replace("&amp;", "&")})
    cartes_parcours = ""
    for mode in ("tout", "e2", "e1"):
        liste = PARCOURS if mode != "e1" else [("2024", "Les fresques de 2024", "The 2024 murals",
            "De Pointe Simon à la cité Dillon : Sitou, Les Fortes de France de Carole B., l'ancien Olympia, Difé Pri d'Oshea et Transmission de Magiic.",
            "From Pointe Simon to Cité Dillon: Sitou, Carole B.'s Les Fortes de France, the old Olympia, Oshea's Difé Pri and Magiic's Transmission.")]
        for cle, fr, en, dfr, den in liste:
            nums = ETAPES_PARCOURS[cle] if cle in ETAPES_PARCOURS else [3, 17, 20, 23, 29]
            etapes = [par_etape[n] for n in nums if n in par_etape]
            if mode != "tout":
                etapes = [f for f in etapes if f["edition"] == int(mode[1])]
            if len(etapes) < 2:
                continue
            km = distance_km(etapes)
            lis = "".join(f'<li><a href="{p.u("fresques/" + f["slug"] + ".html")}">{i+1}. {e(signature(f, p))}</a><span class="meta">#{f["edition"]}{(" · " + e(f["titre"])) if f.get("titre") else ""}</span></li>' for i, f in enumerate(etapes))
            desc = T(p, dfr, den) if mode in ("tout", "e1") else ""
            cache = "" if mode == "tout" else " hidden"
            cartes_parcours += f'''<article class="chaux-offre" data-mode="{mode}"{cache}>
  <p class="surtitre">{len(etapes)} {T(p, "fresques", "murals")} · ≈ {km:.1f} km · ≈ {max(5, round(km / 4 * 60 / 5) * 5)} min {T(p, "de marche", "walk")}</p>
  <h3 style="font-size:30px">{T(p, fr, en)}</h3>
  {f"<p>{desc}</p>" if desc else ""}
  <a class="bouton" style="align-self:flex-start" href="{parcours_url(etapes)}" rel="noopener" target="_blank">{T(p, "Lancer le parcours à pied", "Start the walking route")}</a>
  <ul class="lignes" style="margin-top:8px">{lis}</ul>
</article>'''
    autres = [f for f in FRESQUES if (not f.get("etape") or f["etape"] > 28) and not f.get("disparue")]
    lis_autres = "".join(f'<li><a href="{p.u("fresques/" + f["slug"] + ".html")}">{e(signature(f, p))}</a><span class="meta">{e(f["secteur"])} · <a href="{maps(f)}" rel="noopener" target="_blank" style="font-weight:500">{T(p, "y aller à pied", "walk there")}</a></span></li>' for f in autres)
    import json as _json
    donnees = _json.dumps(points, ensure_ascii=False).replace("</", "<\\/")
    corps = f'''
{bloc_tete(p, [(None, T(p, 'Carte', 'Map'))], T(p, 'La carte des fresques', 'Mural map'), T(p, "Toutes les fresques sur la carte, et trois parcours à pied à suivre avec Google Maps. Clique sur un point pour voir la fresque.", "Every mural on the map, and three walking routes to follow with Google Maps. Tap a point to see the mural."), T(p, 'Parcours libre', 'Self-guided'))}
{bloc_lieux(p)}
<section class="cadre" style="padding-bottom:clamp(40px,5vw,64px)">
  <div class="filtres" id="filtre-edition" role="group" aria-label="{T(p, 'Choisir une édition', 'Choose an edition')}">
    <button type="button" data-m="tout" aria-pressed="true">{T(p, 'Les deux éditions', 'Both editions')}</button><button type="button" data-m="e2" aria-pressed="false">#2 · 2026</button><button type="button" data-m="e1" aria-pressed="false">#1 · 2024</button>
  </div>
  <div class="carte-cadre"><div id="carte" style="position:absolute;inset:0"></div></div>
  <p class="petit" style="margin-top:10px"><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#FCD40D;border:2px solid #1D1E21;box-sizing:border-box;vertical-align:-1px"></span> ARTMADA #2 · 2026 &nbsp; <span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#141414;vertical-align:-1px"></span> ARTMADA #1 · 2024</p>
  <p class="petit gris" style="margin-top:10px">{T(p, "Fond de carte © les contributeurs OpenStreetMap.", "Map data © OpenStreetMap contributors.")}</p>
</section>
<section class="cadre" style="padding-bottom:clamp(56px,7vw,96px)">
  <div class="entete-section"><h2 class="titre-section">{T(p, 'Trois parcours à pied', 'Three walking routes')}</h2><p>{T(p, "Le bouton ouvre Google Maps en mode piéton, avec toutes les étapes dans l'ordre. Distances et durées approximatives.", "The button opens Google Maps in walking mode, with every stop in order. Distances and times are approximate.")}</p></div>
  <div class="g3" style="gap:36px;align-items:start" id="parcours">{cartes_parcours}</div>
</section>
<section class="cadre" style="padding-bottom:clamp(56px,7vw,96px)">
  <div class="texte-5-7 trait-haut">
    <h2 class="titre-moyen">{T(p, 'Plus loin', 'Further afield')}</h2>
    <ul class="lignes">{lis_autres}</ul>
  </div>
</section>
<section class="cadre" style="padding-bottom:clamp(64px,8vw,120px)">
  <a href="{CREAPOLIS}" rel="noopener" target="_blank" class="video-lien carte-cta">
    <img src="{p.a('img/f/a2-jam-b.jpg')}" alt="" loading="lazy" width="1600" height="900">
    <span class="surtitre">Creapolis · Digital Street Art</span>
    <b style="font-size:clamp(28px,3.4vw,48px)">{T(p, 'La visite audio-guidée sur Creapolis', 'The guided tour on Creapolis')}</b>
    <span>{T(p, "30 étapes commentées, gratuit, sur ton téléphone", "30 stops with commentary, free, on your phone")}</span>
  </a>
</section>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script>
(function () {{
  var pts = {donnees};
  if (!window.L) return;
  var carte = L.map("carte", {{ scrollWheelZoom: false }});
  L.tileLayer("https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png", {{ maxZoom: 19, attribution: "© OpenStreetMap" }}).addTo(carte);
  var groupe = [], marqueurs = [];
  pts.forEach(function (q) {{
    var couleur = q.e === 2 ? "#FCD40D" : "#1D1E21";
    var m = L.circleMarker([q.lat, q.lng], {{ radius: 9, color: q.e === 2 ? "#1D1E21" : "#fff", weight: 2, fillColor: couleur, fillOpacity: 1 }}).addTo(carte);
    var html = (q.i ? '<img src="' + q.i + '" alt="" style="width:220px;height:124px;object-fit:cover;display:block;margin-bottom:8px">' : "") +
      "<b>" + q.n + "</b>" + (q.t ? "<br><i>" + q.t + "</i>" : "") + "<br>ARTMADA #" + q.e +
      '<br><a href="' + q.u + '">{T(p, "Voir la fresque", "See the mural")}</a> · <a href="' + q.m + '" target="_blank" rel="noopener">{T(p, "Y aller à pied", "Walk there")}</a>';
    m.bindPopup(html);
    marqueurs.push({{ m: m, e: q.e }});
    groupe.push([q.lat, q.lng]);
  }});
  var fdf = groupe.filter(function (g) {{ return g[0] < 14.7; }});
  carte.fitBounds(fdf, {{ padding: [24, 24] }});
  var boutons = document.querySelectorAll("#filtre-edition button");
  boutons.forEach(function (b) {{
    b.addEventListener("click", function () {{
      var mode = b.getAttribute("data-m");
      boutons.forEach(function (x) {{ x.setAttribute("aria-pressed", x === b ? "true" : "false"); }});
      marqueurs.forEach(function (o) {{
        var voir = mode === "tout" || ("e" + o.e) === mode;
        if (voir) {{ o.m.addTo(carte); }} else {{ carte.removeLayer(o.m); }}
      }});
      document.querySelectorAll("#parcours [data-mode]").forEach(function (a) {{ a.hidden = a.getAttribute("data-mode") !== mode; }});
    }});
  }});
}})();
</script>'''
    ecrire(p, document(p, T(p, "Carte des fresques", "Mural map"), T(p, "La carte des fresques d'ARTMADA à Fort-de-France et trois parcours à pied avec Google Maps.", "Map of ARTMADA murals in Fort-de-France and three walking routes with Google Maps."), corps, actif="fresques/index.html"))

# ============================================================ ARCHIVES

def archives(p):
    L = p.lang
    ed = ARCHIVES
    blocs = ""
    for cle in ("e2", "e1"):
        x = ed[cle]
        fs = [f for f in FRESQUES if f["edition"] == x["num"] and f.get("photo")][:3]
        chiffres = "".join(f'<div><b>{e(c[0])}</b><span>{e(T(p, c[1], c[2]))}</span></div>' for c in x["chiffres"])
        forts = "".join(f"<li>{e(T(p, a, b))}</li>" for a, b in x["temps_forts"])
        noms = ", ".join(f'<a href="{p.u("artistes/" + a["slug"] + ".html")}">{e(a["nom"])}</a>' for a in ARTISTES if x["num"] in a["editions"])
        blocs += f'''<article class="cadre" style="padding-bottom:clamp(56px,7vw,96px)" id="edition-{x['num']}">
  <div class="texte-5-7 trait-haut">
    <div style="display:flex;flex-direction:column;gap:14px">
      <span class="etiquette">{e(T(p, x['dates'], x['dates_en']))}</span>
      <h2 class="titre-section">ARTMADA #{x['num']}</h2>
      <p style="font-size:20px">{e(T(p, x['theme'], x['theme_en']))}</p>
    </div>
    <div style="display:flex;flex-direction:column;gap:22px">
      <p style="font-size:19px">{e(T(p, x['texte'], x['texte_en']))}</p>
      <div class="chiffres">{chiffres}</div>
      <div><p class="surtitre" style="margin-bottom:8px">{T(p, 'Temps forts', 'Highlights')}</p><ul style="padding-left:20px;display:flex;flex-direction:column;gap:4px">{forts}</ul></div>
      <div><p class="surtitre" style="margin-bottom:8px">{T(p, 'Les artistes', 'The artists')}</p><p>{noms}</p></div>
      <a class="lien-fleche" style="align-self:flex-start" href="{p.u('temps-forts-' + ANNEE[x['num']] + '.html')}">{T(p, 'Revivre les temps forts ' + ANNEE[x['num']] + ' en vidéo', 'Relive the ' + ANNEE[x['num']] + ' highlights on video')}</a>
    </div>
  </div>
  <div class="g3" style="margin-top:32px">{"".join(vignette(p, f) for f in fs)}</div>
</article>'''
    videos = "".join(f'''<a class="video-lien" href="{v['url']}" rel="noopener"><img src="{p.a(v['image'])}" alt="" loading="lazy" width="1600" height="900"><span class="lecture" aria-hidden="true"></span><span class="surtitre">{e(T(p, v['source'], v['source_en']))}</span><b>{e(T(p, v['titre'], v['titre_en']))}</b></a>''' for v in ed["videos"])
    corps = f'''
{bloc_tete(p, [(None, T(p, 'Archives', 'Archive'))], T(p, 'Archives', 'Archive'), T(p, "Deux éditions, des dizaines de murs, des centaines de bénévoles et de visiteurs. Ce qui s'est passé depuis 2024.", "Two editions, dozens of walls, hundreds of volunteers and visitors. Everything since 2024."), T(p, 'Depuis 2024', 'Since 2024'))}
{blocs}
<section class="nuit">
  <div class="cadre section">
    <div class="entete-section"><h2 class="titre-section">{T(p, 'Vidéos', 'Videos')}</h2><p class="doux">{T(p, "L'aftermovie, le documentaire, et les réels du festival sur Instagram.", "The aftermovie, the documentary, and the festival reels on Instagram.")}</p></div>
    <div class="g3">{videos}</div>
  </div>
</section>
<section class="cadre section">
  <div class="texte-5-7 trait-haut">
    <h2 class="titre-moyen">{T(p, 'Au pied du mur', 'Au pied du mur')}</h2>
    <div class="prose">
      <p style="font-size:19px">{e(T(p, ed['doc']['texte'], ed['doc']['texte_en']))}</p>
      <p class="gris">{e(T(p, ed['doc']['meta'], ed['doc']['meta_en']))}</p>
    </div>
  </div>
</section>'''
    ecrire(p, document(p, T(p, "Archives", "Archive"), T(p, "Les éditions passées d'ARTMADA Street Festival : 2024 et 2026, chiffres, artistes, vidéos.", "Past editions of ARTMADA Street Festival: 2024 and 2026, figures, artists, videos."), corps, actif="archives.html"))

# ============================================================ TEMPS FORTS

TEMPS_FORTS = charger("temps_forts.json", {})

def _moment_html(p, x, m, credit_video):
    L = p.lang
    lieu = f'<p class="gris">{e(m["lieu"])}</p>' if m.get("lieu") else ""
    photo = ""
    if m.get("photo"):
        if m.get("credit_photo"):
            cr = credit(p, {"credit_photo": m["credit_photo"], "edition": x["num"]})
        else:
            cr = T(p, "Photo : Shaman", "Photo: Shaman") if x["num"] == 2 else "Photo © ARTMADA / NPL MADA PAINT"
        photo = (f'<figure style="margin:0"><img src="{p.a(m["photo"])}" alt="{e(champ(m, "photo_alt", L))}" width="1600" height="900" '
                 f'style="width:100%;aspect-ratio:16/9;object-fit:cover"><figcaption class="petit gris" style="margin-top:8px">{cr}</figcaption></figure>')
    vids = ""
    if m.get("videos"):
        lis = "".join(
            f'<li><a href="{v["url"]}" rel="noopener">{e(champ(v, "titre", L))}</a>'
            f'<span class="meta">{T(p, "Vidéo", "Video")} : {e(credit_video)} · {e(v["vues"])} {T(p, "vues", "views")}</span></li>'
            for v in m["videos"])
        vids = (f'<div><p class="surtitre" style="margin-bottom:8px">{T(p, "Voir la vidéo sur Instagram", "Watch on Instagram")}</p>'
                f'<ul class="lignes">{lis}</ul></div>')
    lien = (f'<a class="lien-fleche" style="align-self:flex-start" href="{p.u(m["page"])}">{e(champ(m, "page_titre", L))}</a>'
            if m.get("page") else "")
    return (f'<article class="cadre" style="padding-bottom:clamp(48px,6vw,80px)" id="{m["id"]}">\n'
            f'  <div class="texte-5-7 trait-haut">\n'
            f'    <div style="display:flex;flex-direction:column;gap:12px">\n'
            f'      <span class="etiquette">{e(champ(m, "quand", L))}</span>\n'
            f'      <h2 class="titre-moyen">{e(champ(m, "titre", L))}</h2>\n'
            f'      {lieu}\n'
            f'    </div>\n'
            f'    <div style="display:flex;flex-direction:column;gap:20px">\n'
            f'      <p style="font-size:19px">{e(champ(m, "texte", L))}</p>\n'
            f'      {photo}{vids}{lien}\n'
            f'    </div>\n'
            f'  </div>\n'
            f'</article>')

def _evenement_ld(p, x):
    L = p.lang
    def lieu(nom):
        return {"@type": "Place", "name": nom,
                "address": {"@type": "PostalAddress", "addressLocality": "Fort-de-France", "addressRegion": "Martinique", "addressCountry": "FR"}}
    subs = []
    for m in x["moments"]:
        if m.get("sans_date"):
            continue
        ev = {"@type": "Event", "name": champ(m, "titre", L), "startDate": m["date"], "description": champ(m, "texte", L),
              "eventStatus": "https://schema.org/EventScheduled",
              "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
              "location": lieu(m.get("lieu") or "Fort-de-France"), "organizer": {"@id": ORGA["@id"]}}
        if m.get("fin"):
            ev["endDate"] = m["fin"]
        subs.append(ev)
    photo = next((m["photo"] for m in x["moments"] if m.get("photo")), "img/partage.jpg")
    return {"@type": ["Festival", "VisualArtsEvent"], "@id": SITE_URL + f"temps-forts-{x['annee']}.html#artmada-{x['num']}",
            "name": f"ARTMADA Street Festival #{x['num']}", "startDate": x["debut"], "endDate": x["fin"],
            "eventStatus": "https://schema.org/EventScheduled",
            "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "description": champ(x, "intro", L), "image": SITE_URL + "assets/" + photo,
            "location": lieu("Fort-de-France"), "organizer": {"@id": ORGA["@id"]}, "isAccessibleForFree": True,
            "url": SITE_URL + ("" if L == "fr" else "en/") + f"temps-forts-{x['annee']}.html", "subEvent": subs}

def _bloc_aftermovie(p):
    from pages_contenu import AFTERMOVIE_EMBED, AFTERMOVIE_URL
    return (f'<section class="cadre" style="padding-bottom:clamp(48px,6vw,80px)" aria-labelledby="titre-am">\n'
            f'  <div class="entete-section" style="margin-bottom:20px">\n'
            f'    <h2 class="titre-section" id="titre-am">{T(p, "L’after movie", "The after movie")}</h2>\n'
            f'    <p>{T(p, "Le film de l’édition 2026, réalisé par JoBlackProd.", "The film of the 2026 edition, by JoBlackProd.")}</p>\n'
            f'  </div>\n'
            f'  <div class="video" data-video="{AFTERMOVIE_EMBED}">\n'
            f'    <button type="button" class="video-lien video-facade" data-titre="{T(p, "After movie d’ARTMADA #2", "ARTMADA #2 after movie")}">\n'
            f'      <img src="{p.a("img/f/a2-curtis.jpg")}" alt="" width="1600" height="900"><span class="lecture" aria-hidden="true"></span>\n'
            f'      <span class="surtitre">{T(p, "Vidéo : JoBlackProd", "Video: JoBlackProd")}</span><b>{T(p, "Lancer l’after movie · ARTMADA #2", "Play the after movie · ARTMADA #2")}</b>\n'
            f'    </button>\n'
            f'  </div>\n'
            f'  <p class="petit gris" style="margin-top:10px">{T(p, "La vidéo se charge depuis YouTube quand tu cliques.", "The video loads from YouTube when you click.")} '
            f'<a href="{AFTERMOVIE_URL}" rel="noopener">{T(p, "La voir sur YouTube", "Watch on YouTube")}</a></p>\n'
            f'</section>')

def temps_forts(p, cle):
    from pages_contenu import aftermovie_ld
    L = p.lang
    x = TEMPS_FORTS[cle]
    autre = TEMPS_FORTS["e1" if cle == "e2" else "e2"]
    titre = T(p, f"Temps forts {x['annee']}", f"{x['annee']} highlights")
    fil = [("archives.html", T(p, "Archives", "Archive")), (None, titre)]
    corps = bloc_tete(p, fil, e(titre), e(champ(x, "intro", L)), f"ARTMADA #{x['num']} · {champ(x, 'dates', L)}")
    sommaire = " · ".join(f'<a href="#{m["id"]}">{e(champ(m, "titre", L))}</a>' for m in x["moments"])
    corps += (f'<section class="cadre" style="padding-bottom:clamp(32px,4vw,56px)"><p>'
              f'{T(p, "Sur cette page", "On this page")} : {sommaire}</p></section>')
    ld = [fil_ld(p, fil), _evenement_ld(p, x)]
    if cle == "e2":
        corps += _bloc_aftermovie(p)
        ld.append(aftermovie_ld(L))
    corps += "".join(_moment_html(p, x, m, x["credit_video"]) for m in x["moments"])
    if x.get("jours"):
        lis = "".join(f'<li><a href="{j["url"]}" rel="noopener">{T(p, "Jour", "Day")} {j["jour"]} · {e(champ(j, "titre", L))}</a>'
                      f'<span class="meta">{e(champ(j, "date", L))} · {T(p, "Vidéo", "Video")} : {e(x["credit_video"])} · {e(j["vues"])} {T(p, "vues", "views")}</span></li>'
                      for j in x["jours"])
        corps += (f'<section class="cadre" style="padding-bottom:clamp(48px,6vw,80px)" id="jour-par-jour">\n'
                  f'  <div class="texte-5-7 trait-haut">\n'
                  f'    <div style="display:flex;flex-direction:column;gap:12px"><h2 class="titre-moyen">{T(p, "Le festival jour par jour", "The festival day by day")}</h2>\n'
                  f'      <p class="gris">{T(p, "Chaque soir, une vidéo racontait la journée sur Instagram.", "Every evening, a video told the story of the day on Instagram.")}</p></div>\n'
                  f'    <ul class="lignes">{lis}</ul>\n'
                  f'  </div>\n'
                  f'</section>')
    if x.get("aussi"):
        items = "".join(f"<li>{e(T(p, a, b))}</li>" for a, b in x["aussi"])
        corps += (f'<section class="cadre" style="padding-bottom:clamp(48px,6vw,80px)">\n'
                  f'  <div class="texte-5-7 trait-haut"><h2 class="titre-moyen">{T(p, "Et aussi", "Also")}</h2>\n'
                  f'    <ul style="padding-left:20px;display:flex;flex-direction:column;gap:6px;font-size:18px">{items}</ul></div>\n'
                  f'</section>')
    if x.get("bilan"):
        b = x["bilan"]
        fin = ""
        if x.get("fin_video"):
            v = x["fin_video"]
            fin = (f'<p><a href="{v["url"]}" rel="noopener">{e(champ(v, "titre", L))}</a> '
                   f'<span class="doux">· {T(p, "Vidéo", "Video")} : {e(x["credit_video"])} · {e(v["vues"])} {T(p, "vues", "views")}</span></p>')
        corps += (f'<section class="nuit">\n'
                  f'  <div class="cadre section texte-5-7">\n'
                  f'    <h2 class="titre-section">{e(champ(b, "titre", L))}</h2>\n'
                  f'    <div class="prose"><p style="font-size:19px">{e(champ(b, "texte", L))}</p>'
                  f'<p class="doux petit">{T(p, "Source", "Source")} : {e(champ(b, "source", L))}</p>{fin}</div>\n'
                  f'  </div>\n'
                  f'</section>')
    autre_titre = T(p, f"Temps forts {autre['annee']}", f"{autre['annee']} highlights")
    corps += (f'<section class="cadre section">\n'
              f'  <div class="boutons">\n'
              f'    <a class="bouton" href="{p.u("temps-forts-" + autre["annee"] + ".html")}">{autre_titre}</a>\n'
              f'    <a class="bouton bouton-contour" href="{p.u("archives.html")}">{T(p, "Toutes les archives", "Full archive")}</a>\n'
              f'    <a class="bouton bouton-contour" href="{p.u("fresques/index.html")}">{T(p, "Voir les fresques", "See the murals")}</a>\n'
              f'  </div>\n'
              f'</section>')
    noms_fr = ", ".join(m["titre"][0].lower() + m["titre"][1:] for m in x["moments"][:4])
    noms_en = ", ".join(m["titre_en"][0].lower() + m["titre_en"][1:] for m in x["moments"][:4])
    desc = T(p, f"Les temps forts d'ARTMADA #{x['num']} ({x['annee']}), festival de street art de Fort-de-France, en vidéo : {noms_fr}…",
             f"ARTMADA #{x['num']} ({x['annee']}) highlights, Fort-de-France's street art festival, on video: {noms_en}…")
    if len(desc) > 158:
        desc = desc[:155].rsplit(" ", 1)[0].rstrip(",") + "…"
    titre_page = T(p, f"Temps forts {x['annee']} · ARTMADA #{x['num']}, street art à Fort-de-France",
                   f"{x['annee']} highlights · ARTMADA #{x['num']}, street art in Fort-de-France")
    photo = next((m["photo"] for m in x["moments"] if m.get("photo")), None)
    ecrire(p, document(p, "", desc, corps, actif="archives.html", image=photo, titre_complet=titre_page, ld=ld))


# ============================================================ PRESSE

def presse(p):
    L = p.lang
    pr = PRESSE
    arts = "".join(f'<li>{(f"<a href=\"{a["url"]}\" rel=\"noopener\">{e(a["titre"])}</a>" if a.get("url") else f"<span style=\"font-weight:700\">{e(a["titre"])}</span>")}<span class="meta">{e(a["media"])}{" · " + e(a["date"]) if a.get("date") else ""}</span></li>' for a in pr["articles"])
    chif = "".join(f'<div><b>{e(c[0])}</b><span>{e(T(p, c[1], c[2]))}</span></div>' for c in pr["chiffres"])
    ress = "".join(f'<li><a href="{r["url"]}" rel="noopener">{e(T(p, r["titre"], r["titre_en"]))}</a><span class="meta">{e(T(p, r["meta"], r["meta_en"]))}</span></li>' for r in pr["ressources"])
    corps = f'''
{bloc_tete(p, [(None, T(p, 'Presse', 'Press'))], T(p, 'Espace presse', 'Press area'), "", T(p, 'Journalistes', 'Journalists'))}
<section class="cadre" style="padding-bottom:clamp(56px,7vw,96px)">
  <div class="texte-5-7 trait-haut">
    <h2 class="titre-moyen">{T(p, 'Le festival en bref', 'At a glance')}</h2>
    <div class="prose">
      <p style="font-size:20px">{e(T(p, pr['court'], pr['court_en']))}</p>
      {"".join(f"<p>{e(x)}</p>" for x in T(p, pr['long'], pr['long_en']))}
    </div>
  </div>
</section>
<section class="cadre" style="padding-bottom:clamp(56px,7vw,96px)">
  <div class="texte-5-7 trait-haut">
    <h2 class="titre-moyen">{T(p, 'Chiffres clés · édition #2', 'Key figures · edition #2')}</h2>
    <div class="chiffres">{chif}</div>
  </div>
</section>
<section class="nuit">
  <div class="cadre section texte-5-7">
    <div style="display:flex;flex-direction:column;gap:16px"><span class="etiquette">{T(p, 'Contact presse', 'Press contact')}</span><h2 class="titre-section">{T(p, 'Une interview, des photos ?', 'Interview or photos?')}</h2></div>
    <div style="display:flex;flex-direction:column;gap:18px">
      <p style="font-size:19px">{T(p, "Interviews d'artistes, accès aux murs pendant le festival, photos HD, dossier de presse : écris-nous, on répond vite.", "Artist interviews, access to the walls during the festival, HD photos, press kit: write to us, we reply quickly.")}</p>
      <a class="bouton bouton-jaune-v" style="align-self:flex-start" href="mailto:{MAIL}?subject={T(p, 'Presse%20ARTMADA', 'ARTMADA%20press')}">{MAIL}</a>
      <ul class="lignes" style="border-top-color:var(--nuit-trait)">{ress}</ul>
    </div>
  </div>
</section>
<section class="cadre section">
  <div class="entete-section"><h2 class="titre-section">{T(p, 'Ils en parlent', 'In the press')}</h2><p>{T(p, 'Articles, reportages et émissions sur ARTMADA et le collectif Mada Paint.', 'Articles, reports and broadcasts about ARTMADA and the Mada Paint collective.')}</p></div>
  <ul class="lignes">{arts}</ul>
  <p class="petit gris" style="margin-top:24px">{T(p, "Chaque fresque appartient à son artiste. Pour publier une photo, cite l'artiste et ARTMADA.", "Each mural belongs to its artist. When publishing a photo, credit the artist and ARTMADA.")}</p>
</section>'''
    ecrire(p, document(p, T(p, "Presse", "Press"), T(p, "Espace presse d'ARTMADA Street Festival : présentation, chiffres clés, contact, photos, revue de presse.", "ARTMADA Street Festival press area: overview, key figures, contact, photos, press coverage."), corps, actif="presse.html"))

# ============================================================ ensemble

def toutes(lang):
    artistes_index(P(lang, "artistes/index.html"))
    for a in ARTISTES:
        artiste_page(P(lang, f"artistes/{a['slug']}.html"), a)
    fresques_index(P(lang, "fresques/index.html"))
    for i, f in enumerate(FRESQUES):
        fresque_page(P(lang, f"fresques/{f['slug']}.html"), f, i)
    carte(P(lang, "carte.html"))
    archives(P(lang, "archives.html"))
    temps_forts(P(lang, "temps-forts-2026.html"), "e2")
    temps_forts(P(lang, "temps-forts-2024.html"), "e1")
    presse(P(lang, "presse.html"))
