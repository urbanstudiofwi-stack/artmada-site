"""Les pages du site ARTMADA. Chaque fonction écrit une page dans une langue."""
from build import *  # noqa: F401,F403
import build as B

BIZOUK = "https://www.bizouk.com/events/details/atelier-graffiti-a-lurban-studio-avec-do/131478"
MAIL = "contact@artmadastreetfestival.com"
INSTA = "https://www.instagram.com/artmadastreetfestival972/"

PARTENAIRES = [
    ("Ville de Fort-de-France", "Partenaire principal", "Main partner"),
    ("Collectivité Territoriale de Martinique", "Institution", "Institution"),
    ("CACEM", "Institution", "Institution"),
    ("DAC Martinique", "Ministère de la Culture", "Ministry of Culture"),
    ("Comité Martiniquais du Tourisme", "Institution", "Institution"),
    ("Ozanam", "Bailleur", "Social housing"),
    ("SOAME", "Mur & partenaire", "Wall & partner"),
    ("Régie des Transports de Martinique", "Transport", "Transport"),
    ("Caribloc", "Nacelles", "Aerial lifts"),
    ("Seigneurie Martinique", "Peinture", "Paint"),
    ("Papeterie Discount", "Fournitures", "Supplies"),
    ("ARTI", "Impression", "Printing"),
    ("RED by SFR", "Partenaire", "Partner"),
    ("NRJ", "Média", "Media"),
    ("CIS Martinique", "Partenaire", "Partner"),
    ("Urban Studio", "Galerie & ateliers", "Gallery & workshops"),
]

AFTERMOVIE_ID = "156J3jTFjBwcTbKLKKREeGRhYG16AjRGk"   # « 🎥 After Movie !!.mp4 », Drive ARTMADA, JoBlackProd 2026
AFTERMOVIE_YT = "UAhXATqQ1Ys"   # YouTube, chaîne ARTMADA Street Festival (ex NPL MADA PAINT), publiée le 19/10/2026
AFTERMOVIE_EMBED = f"https://www.youtube-nocookie.com/embed/{AFTERMOVIE_YT}?autoplay=1&rel=0"
AFTERMOVIE_URL = f"https://www.youtube.com/watch?v={AFTERMOVIE_YT}"

def aftermovie_ld(lang):
    return {"@type": "VideoObject", "@id": SITE_URL + "#aftermovie-2",
            "name": t(lang, "After movie ARTMADA #2 (2026)", "ARTMADA #2 after movie (2026)"),
            "description": t(lang, "Le film de la deuxième édition d'ARTMADA Street Festival à Fort-de-France (Martinique) : fresques, jam, block party. Réalisation : JoBlackProd.",
                             "The film of the second ARTMADA Street Festival in Fort-de-France, Martinique: murals, jam, block party. Directed by JoBlackProd."),
            "thumbnailUrl": SITE_URL + "assets/img/aftermovie-miniature.jpg", "uploadDate": "2026-04-18",
            "embedUrl": f"https://www.youtube.com/embed/{AFTERMOVIE_YT}", "url": AFTERMOVIE_URL, "duration": "PT2M55S", "inLanguage": "fr",
            "creator": {"@type": "Organization", "name": "JoBlackProd"},
            "publisher": {"@id": ORGA["@id"]}}

def P(lang, chemin):
    return Page(lang, chemin)

def T(p, fr, en):
    return t(p.lang, fr, en)

# ============================================================ ACCUEIL

URBAN_STUDIO = "Urban Studio, Village de la Poterie, Les Trois-Îlets"
HORAIRES_FR = "Du mardi au vendredi : 9h – 12h et 13h30 – 17h30 · Samedi : 10h – 17h"
HORAIRES_EN = "Tuesday to Friday: 9am – 12pm and 1:30pm – 5:30pm · Saturday: 10am – 5pm"

LIEUX = [
    ("Teat Otonom Mawon (TOM)", "Rue Victor Sévère", "Rue Victor Sévère", "Teat Otonom Mawon, Fort-de-France"),
    ("Langellier", "Quartier", "Neighbourhood", "Langellier, Fort-de-France"),
    ("Mongérald", "Quartier", "Neighbourhood", "Mongérald, Fort-de-France"),
    ("Tocade", "Quartier", "Neighbourhood", "Tocade, Fort-de-France"),
    ("Centre-ville", "Fort-de-France", "Fort-de-France", "Centre-ville, Fort-de-France"),
]

PARTENAIRES_LOGOS = [
    ("ville-fort-de-france", "Ville de Fort-de-France"), ("ctm", "Collectivité Territoriale de Martinique"),
    ("dac-martinique", "Préfet de la Martinique — DAC"), ("cmt-la-martinique", "Comité Martiniquais du Tourisme"),
    ("cacem", "CACEM"), ("rtm", "Régie des Transports de Martinique"), ("ozanam", "Ozanam — Groupe Action Logement"),
    ("soame", "SOAME"), ("cis-martinique", "CIS Martinique"), ("caribloc", "Caribloc"), ("seigneurie", "Seigneurie"),
    ("papeterie-discount", "Papeterie Discount"), ("nrj-antilles", "NRJ Antilles"), ("red-by-sfr", "RED by SFR Caraïbe"),
    ("arti", "ARTI Martinique"),
]

MEDIAS = ["Martinique la 1ère", "France-Antilles", "RCI", "Madinin'Art", "Street Art Utopia", "Outremers360",
          "Zitata TV", "Juno7", "HPN Info", "BuzzMag", "Prikay", "RBR Laradio"]

PRINTS = [
    ("01", "xan-et-breeze", "Xän & Breeze", 1, "paysage"), ("02", "kaldea", "Kaldéa", 1, "paysage"),
    ("03", "magiic", "Magiic", 1, "paysage"), ("04", "sitou", "Sitou", 1, "paysage"),
    ("05", "doudou-style", "Doudou Style", 2, "portrait"), ("06", "la-jam", "La Jam", 2, "paysage"),
    ("07", "veneno", "Veneno", 2, "portrait"), ("08", "curtis-hylton", "Curtis Hylton", 2, "paysage"),
    ("09", "yelow", "Yelow", 2, "paysage"), ("10", "jaddict", "Jaddict", 2, "portrait"),
    ("11", "rayza", "Rayza", 2, "portrait"), ("12", "box-vincent", "Box Vincent", 2, "portrait"),
    ("13", "wuna", "Wuna", 2, "paysage"), ("14", "temponok", "Tempo Nok", 2, "paysage"),
]

def produits():
    """Tout ce que vend la boutique (vendeur : Urban Studio FWI)."""
    lst = [
        dict(id="tshirt", cat="textile", nom=("T-shirt officiel ARTMADA", "Official ARTMADA T-shirt"), ligne=("Blanc · du S au XXL", "White · S to XXL"),
             prix=("30 €", "€30"), img="img/da/tshirt-face.webp", dispo=True),
        dict(id="casquette", cat="textile", nom=("Casquette ARTMADA", "ARTMADA cap"), ligne=("Photo à venir", "Photo coming soon"),
             prix=("20 €", "€20"), img=None, dispo=True),
        dict(id="tote-artmada", cat="accessoires", nom=("Tote bag ARTMADA", "ARTMADA tote bag"), ligne=("Logo ARTMADA Street Festival", "ARTMADA Street Festival logo"),
             prix=None, img="img/shop/tote-artmada.webp", dispo=False),
    ]
    for n, slug, artiste, ed, sens in PRINTS:
        lst.append(dict(id=f"print-{n}", cat="prints", nom=(artiste, artiste), ligne=(f"Print A3 · ARTMADA #{ed}", f"A3 print · ARTMADA #{ed}"),
                        prix=("30 € · 50 € encadré", "€30 · €50 framed"), img=f"img/shop/print-{n}-{slug}.webp", dispo=False, print_=sens))
    lst += [
        dict(id="tote-urban", cat="accessoires", nom=("Tote bag Urban Studio", "Urban Studio tote bag"), ligne=("Logo Urban Studio · Doudou Style", "Urban Studio logo · Doudou Style"),
             prix=None, img="img/shop/tote-urban-studio.webp", dispo=False),
        dict(id="tote-funky", cat="accessoires", nom=("Tote bag Funky Charly", "Funky Charly tote bag"), ligne=("Doudou Style", "Doudou Style"),
             prix=None, img="img/shop/tote-funky-charly.webp", dispo=False),
        dict(id="serviette-shou", cat="accessoires", nom=("Serviette « femme + loup »", "“Woman + wolf” towel"), ligne=("Shou · 70 × 140 cm", "Shou · 70 × 140 cm"),
             prix=None, img="img/shop/serviette-shou.webp", dispo=False),
    ]
    return lst

def mailto_resa(lang, produit, taille=""):
    from urllib.parse import quote
    sujet = t(lang, f"Réservation — {produit}", f"Reservation — {produit}")
    corps = t(lang, f"Bonjour, je voudrais réserver : {produit}{(' en taille ' + taille) if taille else ''}. Je viendrai le chercher à l'Urban Studio.",
              f"Hello, I would like to reserve: {produit}{(' in size ' + taille) if taille else ''}. I will pick it up at Urban Studio.")
    return f"mailto:{MAIL}?subject={quote(sujet)}&body={quote(corps)}"

def carte_produit(p, pr):
    L = p.lang
    nom = t(L, *pr["nom"]); ligne = t(L, *pr["ligne"])
    if pr["img"]:
        cls = "produit-img" + (" produit-print " + pr["print_"] if pr.get("print_") else "")
        visuel = f'<span class="{cls}"><img src="{p.a(pr["img"])}" alt="{e(nom)} — {e(ligne)}" loading="lazy" decoding="async"></span>'
    else:
        visuel = f'<span class="produit-img produit-attente"><img src="{p.a("img/da/bombe-mains-600.webp")}" alt="" loading="lazy" decoding="async"><span>{t(L, "Photo à venir", "Photo coming soon")}</span></span>'
    prix = f'<p class="produit-prix">{t(L, *pr["prix"])}</p>' if pr.get("prix") else ""
    if pr["dispo"]:
        action = f'<a class="produit-action" href="{e(mailto_resa(L, nom))}">{t(L, "Réserver", "Reserve")} {ICONES["fleche"]}</a>'
    else:
        action = f'<span class="produit-bientot">{t(L, "Bientôt disponible", "Coming soon")}</span>'
    return f'''<article class="produit rv" data-tags="{pr["cat"]}" id="{pr["id"]}">{visuel}<h3>{e(nom)}</h3><p class="produit-ligne">{e(ligne)}</p>{prix}{action}</article>'''

def tshirt_3d(p, controles=False):
    """Le t-shirt officiel qui tourne sur lui-même (face, puis dos)."""
    boutons = ""
    if controles:
        boutons = f'''<div class="ts-boutons" role="group" aria-label="{T(p, 'Voir le t-shirt', 'View the T-shirt')}">
  <button type="button" data-ts-vue="tourne" aria-pressed="true">{T(p, 'Il tourne', 'Spin')}</button>
  <button type="button" data-ts-vue="face" aria-pressed="false">{T(p, 'Face', 'Front')}</button>
  <button type="button" data-ts-vue="dos" aria-pressed="false">{T(p, 'Dos', 'Back')}</button>
</div>'''
    return f'''<div class="ts-scene" data-ts data-vue="tourne">
  <div class="ts-carte">
    <img class="ts-face" src="{p.a('img/da/tshirt-face.webp')}" alt="{T(p, "T-shirt officiel ARTMADA, face : logo et main tenant une bombe de peinture", "Official ARTMADA T-shirt, front: logo and hand holding a spray can")}" width="785" height="900" decoding="async">
    <img class="ts-dos" src="{p.a('img/da/tshirt-dos.webp')}" alt="{T(p, "T-shirt officiel ARTMADA, dos : petit logo et tag Lyannaj Karayib", "Official ARTMADA T-shirt, back: small logo and Lyannaj Karayib tag")}" width="784" height="900" decoding="async">
  </div>
  <span class="ts-ombre" aria-hidden="true"></span>
</div>{boutons}'''

def bloc_lieux(p, titre_h="h2"):
    L = p.lang
    from urllib.parse import quote_plus
    cartes = ""
    for nom, sous_fr, sous_en, q in LIEUX:
        cartes += f'''<li class="lieu rv"><span class="lieu-ico">{ICONES["lieu"]}</span><span class="lieu-txt"><b>{e(nom)}</b><span>{t(L, sous_fr, sous_en)}</span></span><a href="https://www.google.com/maps/search/?api=1&amp;query={quote_plus(q)}" rel="noopener" target="_blank">{t(L, "Itinéraire", "Directions")}</a></li>'''
    return f'''<section class="v3-section v3-blanc" id="lieux" aria-labelledby="titre-lieux">
  <div class="cadre">
    <div class="v3-entete">
      <{titre_h} class="v3-titre anim-titre" id="titre-lieux">{t(L, "Les lieux du festival", "Festival venues")}</{titre_h}>
      <p>{t(L, "Les murs de l'édition #3 seront annoncés au fur et à mesure. En attendant, voici les quartiers où le festival se passera.", "Edition #3 walls will be announced step by step. Meanwhile, here are the neighbourhoods where the festival will take place.")}</p>
    </div>
    <ul class="lieux">{cartes}</ul>
    <p class="v3-note">{t(L, "Adresses exactes des murs : bientôt.", "Exact wall addresses: coming soon.")} <a href="{p.u('carte.html')}">{t(L, "Voir les 40 fresques déjà peintes sur la carte", "See the 40 murals already painted on the map")}</a></p>
  </div>
</section>'''

def fond_mur(p, fichier):
    """Fresque en noir et blanc, foncée, derrière le gros titre d'une bande sombre."""
    petit = fichier.replace(".webp", "-1200.webp")
    return f'<div class="fond-mur" aria-hidden="true"><img src="{p.a("img/fonds/" + fichier)}" srcset="{p.a("img/fonds/" + petit)} 1200w, {p.a("img/fonds/" + fichier)} 2400w" sizes="100vw" alt="" width="2400" height="1050" loading="lazy" decoding="async"></div>'

def accueil(lang):
    p = P(lang, "index.html")
    a = p.a
    L = lang
    une = [f for f in FRESQUES if f.get("une") and f.get("photo")][:6]
    if len(une) < 6:
        une += [f for f in FRESQUES if f not in une and f.get("photo")][:6 - len(une)]
    murs = "".join(f'''<a class="mur rv" href="{p.u('fresques/' + f['slug'] + '.html')}">{img_fresque(p, f)}<span><b>{e(nom_artistes(f))}</b>{e(f.get('lieu') or 'Fort-de-France')}</span></a>''' for f in une)
    vitrine = [pr for pr in produits() if pr["id"] in ("tshirt", "print-08", "tote-artmada", "print-11")]
    vitrine_html = "".join(carte_produit(p, pr) for pr in vitrine)
    logos = "".join(f'<li><img src="{a("img/partenaires/" + f + ".webp")}" alt="{e(n)}" loading="lazy" decoding="async"></li>' for f, n in PARTENAIRES_LOGOS)
    medias = "".join(f"<li>{e(m)}</li>" for m in MEDIAS)
    corps = f'''
<section class="v3-hero" aria-labelledby="titre-accueil">
  <video class="v3-video" muted loop playsinline preload="none" poster="{a('img/aftermovie-fond.jpg')}" data-src="{a('video/aftermovie-boucle.mp4')}" data-src-petit="{a('video/aftermovie-boucle-640.mp4')}" aria-hidden="true"></video>
  <span class="v3-voile" aria-hidden="true"></span>
  <div class="v3-hero-centre">
    <div class="bombe-anim" aria-hidden="true">
      <img class="bombe-img" src="{a('img/da/bombe-mains-600.webp')}" srcset="{a('img/da/bombe-mains-600.webp')} 600w, {a('img/da/bombe-mains.webp')} 1100w" sizes="(max-width: 700px) 54vw, 300px" alt="" width="1100" height="1131" fetchpriority="high">
      <span class="bombe-nuage"><i></i><i></i><i></i><i></i><i></i></span>
    </div>
    <h1 id="titre-accueil" class="v3-h1"><span class="mot">ARTMADA</span> <span class="mot">Street</span> <span class="mot">Festival</span></h1>
    <p class="v3-dates">{t(L, '25 janv.', '25 Jan')} <span>›</span> {t(L, '4 févr. 2027', '4 Feb 2027')}</p>
    <p class="v3-lieu">{t(L, 'Édition #3 · Fort-de-France, Martinique', 'Edition #3 · Fort-de-France, Martinique')}</p>
  </div>
  <a class="v3-souris" href="#edition" aria-label="{t(L, 'Descendre', 'Scroll down')}"><span></span></a>
  <button type="button" class="v3-pause" data-video-pause aria-label="{t(L, 'Mettre la vidéo en pause', 'Pause the video')}" aria-pressed="false"><svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true" fill="currentColor"><rect x="2" y="1" width="3.5" height="12"/><rect x="8.5" y="1" width="3.5" height="12"/></svg></button>
</section>

<section class="v3-section v3-blanc" id="edition" aria-labelledby="titre-edition">
  <div class="cadre v3-deux">
    <div>
      <p class="v3-surtitre">{t(L, "Le thème de l'édition #3", 'The theme of edition #3')}</p>
      <h2 class="v3-geant anim-titre" id="titre-edition">An Lot Chimen</h2>
    </div>
    <div class="v3-texte">
      <p class="v3-citation">{t(L, "« À l'heure d'un certain fatalisme social, guerrier, climatique et numérique, un autre chemin est-il possible ? »", "“In a time of social, military, climate and digital fatalism, is another way possible?”")}</p>
      <p>{t(L, "Pendant 11 jours, des artistes de Martinique, de la Caraïbe et d'ailleurs peignent les murs de Fort-de-France, en direct, devant les habitants. Ateliers, soirées avec DJ, block party : la ville change de visage.", "For 11 days, artists from Martinique, the Caribbean and beyond paint the walls of Fort-de-France, live, in front of residents. Workshops, DJ nights, block party: the city changes its face.")}</p>
      <p class="v3-petit">{t(L, "Texte du thème : Xän, pour le collectif Mada Paint.", "Theme text: Xän, for the Mada Paint collective.")} <a href="{p.u('festival.html')}">{t(L, "Tout sur l'édition #3", "All about edition #3")}</a></p>
    </div>
  </div>
</section>

<section class="v3-section v3-nuit a-fond" id="programme" aria-labelledby="titre-programme">
  {fond_mur(p, "xan-breeze.webp")}
  <div class="cadre">
    <div class="v3-entete">
      <h2 class="v3-titre anim-titre" id="titre-programme">{t(L, 'Programme', 'Programme')}</h2>
      <p>{t(L, 'Du 25 janvier au 4 février 2027, à Fort-de-France.', '25 January to 4 February 2027, in Fort-de-France.')}</p>
    </div>
    <div class="v3-bientot rv">
      <p class="v3-bientot-titre">{t(L, 'Programme bientôt disponible', 'Programme coming soon')}</p>
      <p>{t(L, "Fresques en direct, ateliers, soirées et block party : le programme jour par jour arrive très vite. Inscris-toi en bas de page pour le recevoir dès sa sortie.", "Live murals, workshops, parties and block party: the day-by-day programme is coming very soon. Sign up at the bottom of the page to get it first.")}</p>
      <div class="boutons"><a class="bouton-jaune" href="#news-mail-{L}">{t(L, 'Me prévenir', 'Notify me')} {ICONES["fleche"]}</a><a class="bouton-ligne" href="{p.u('programme.html')}">{t(L, "Revoir le programme 2026", "See the 2026 programme")}</a></div>
    </div>
    <ul class="v3-quoi">
      <li class="rv"><b>{t(L, 'Fresques en direct', 'Live murals')}</b><span>{t(L, 'Dans les quartiers', 'In the neighbourhoods')}</span></li>
      <li class="rv"><b>{t(L, 'Ateliers', 'Workshops')}</b><span>{t(L, 'Pour tous les âges', 'For all ages')}</span></li>
      <li class="rv"><b>{t(L, 'Soirées', 'Parties')}</b><span>{t(L, 'Avec DJ', 'With DJs')}</span></li>
      <li class="rv"><b>Block party</b><span>{t(L, 'Pour finir en beauté', 'The grand finale')}</span></li>
    </ul>
  </div>
</section>

{bloc_lieux(p)}

<section class="v3-section v3-nuit a-fond" aria-labelledby="titre-murs">
  {fond_mur(p, "clarac-colibri.webp")}
  <div class="cadre">
    <div class="v3-entete">
      <h2 class="v3-titre anim-titre" id="titre-murs">{t(L, 'Les murs restent', 'The walls stay')}</h2>
      <p>{t(L, "40 fresques peintes depuis 2024, à voir toute l'année, à pied, gratuitement.", "40 murals painted since 2024, to see all year round, on foot, for free.")}</p>
    </div>
    <div class="murs">{murs}</div>
    <div class="boutons" style="margin-top:36px"><a class="bouton-jaune" href="{p.u('carte.html')}">{t(L, 'Ouvrir la carte', 'Open the map')} {ICONES["fleche"]}</a><a class="bouton-ligne" href="{p.u('fresques/index.html')}">{t(L, 'Toutes les fresques', 'All the murals')}</a></div>
  </div>
</section>

<section class="v3-section v3-nuit v3-film a-fond" aria-labelledby="titre-aftermovie">
  {fond_mur(p, "doudou-style.webp")}
  <div class="cadre">
    <div class="v3-entete">
      <h2 class="v3-titre anim-titre" id="titre-aftermovie">{t(L, "L'after movie", "The after movie")}</h2>
      <p>{t(L, "ARTMADA #2, février 2026. Réalisation : JoBlackProd.", "ARTMADA #2, February 2026. Directed by JoBlackProd.")}</p>
    </div>
    <div class="video v3-lecteur rv" data-video="{AFTERMOVIE_EMBED}">
      <button type="button" class="video-lien video-facade" data-titre="{t(L, "After movie d'ARTMADA #2", "ARTMADA #2 after movie")}">
        <img src="{a('img/aftermovie-miniature-site.jpg')}" alt="" width="1280" height="720" loading="lazy"><span class="lecture" aria-hidden="true"></span>
        <b>{t(L, "Lancer l'after movie", "Play the after movie")}</b>
      </button>
    </div>
    <p class="v3-petit" style="margin-top:12px">{t(L, "La vidéo se charge depuis YouTube quand tu cliques.", "The video loads from YouTube when you click.")} <a href="{AFTERMOVIE_URL}" rel="noopener">YouTube</a></p>
  </div>
</section>

<section class="v3-section v3-blanc" aria-labelledby="titre-shop">
  <div class="cadre">
    <div class="v3-entete">
      <h2 class="v3-titre anim-titre" id="titre-shop">{t(L, 'Nouveau dans la boutique', 'New in the shop')}</h2>
      <a class="bouton-jaune" href="{p.u('boutique.html')}">{t(L, 'Tout le shop', 'Visit the shop')} {ICONES["fleche"]}</a>
    </div>
    <div class="produits">{vitrine_html}</div>
  </div>
</section>

<section class="v3-blanc v3-logos" aria-labelledby="titre-partenaires">
  <div class="cadre">
    <h2 class="v3-surtitre" id="titre-partenaires">{t(L, 'Ils soutiennent le festival', 'They support the festival')}</h2>
    <ul class="logos">{logos}</ul>
  </div>
</section>

<section class="v3-blanc v3-medias" aria-labelledby="titre-medias">
  <div class="cadre">
    <h2 class="v3-surtitre" id="titre-medias">{t(L, 'Ils parlent de nous', 'In the press')}</h2>
    <ul class="medias">{medias}</ul>
    <a class="v3-lien" href="{p.u('presse.html')}">{t(L, 'Lire les articles', 'Read the articles')} {ICONES["fleche"]}</a>
  </div>
</section>

<section class="v3-jaune" aria-labelledby="titre-benevoles">
  <div class="cadre v3-jaune-in">
    <h2 class="v3-titre anim-titre" id="titre-benevoles">{t(L, 'Le festival se fait ensemble', 'We make it together')}</h2>
    <div>
      <p>{t(L, "75 bénévoles ont fait vivre ARTMADA #2. Conduire les artistes, accueillir le public, aider sur les murs : même quelques heures comptent.", "75 volunteers brought ARTMADA #2 to life. Driving artists, welcoming visitors, helping on the walls: even a few hours make a difference.")}</p>
      <a class="bouton-noir" href="{p.u('benevoles.html')}">{t(L, 'Je deviens bénévole', 'Become a volunteer')} {ICONES["fleche"]}</a>
    </div>
  </div>
</section>
'''
    ecrire(p, document(p, "", t(L, "ARTMADA Street Festival, le festival de street art de Fort-de-France (Martinique). Édition #3 « An Lot Chimen » du 25 janvier au 4 février 2027 : programme, lieux, carte des fresques et shop officiel.", "ARTMADA Street Festival, the street art festival of Fort-de-France, Martinique. Edition #3 “An Lot Chimen”, 25 January to 4 February 2027: programme, venues, mural map and official shop."),
                       corps, actif="index.html", image="img/hd/a2-doudou.jpg", sur_video=True,
                       ld=[{"@type": "WebSite", "@id": SITE_URL + "#site", "name": "ARTMADA Street Festival", "url": SITE_URL, "inLanguage": ["fr", "en"], "publisher": {"@id": ORGA["@id"]}},
                           festival_ld(p.lang), aftermovie_ld(p.lang)]))

# ============================================================ BOUTIQUE

def boutique(lang):
    p = P(lang, "boutique.html")
    L = lang
    tailles = "".join(f'<button type="button" class="ts-taille" data-taille="{n}" aria-pressed="{"true" if n == "M" else "false"}">{n}</button>' for n in ["S", "M", "L", "XL", "XXL"])
    nom_ts = t(L, "T-shirt officiel ARTMADA", "Official ARTMADA T-shirt")
    filtres = "".join(f'<button type="button" data-f="{k}" aria-pressed="{"true" if k == "tout" else "false"}">{t(L, fr, en)}</button>'
                      for k, fr, en in [("tout", "Tout", "All"), ("textile", "Textile", "Clothing"), ("prints", "Prints", "Prints"), ("accessoires", "Accessoires", "Accessories")])
    cartes = "".join(carte_produit(p, pr) for pr in produits())
    corps = f'''
<section class="cadre shop-tete">
  <nav class="fil" aria-label="{t(L, 'Fil d’Ariane', 'Breadcrumb')}"><a href="{p.u('index.html')}">{t(L, 'Accueil', 'Home')}</a> / Shop</nav>
  <h1 class="v3-geant anim-titre">{t(L, 'La boutique', 'The shop')}</h1>
  <p class="shop-chapo">{t(L, "Le merch officiel d'ARTMADA Street Festival et les éditions des artistes. Chaque achat aide le festival à peindre de nouveaux murs.", "Official ARTMADA Street Festival merch and artist editions. Every purchase helps the festival paint new walls.")}</p>
  <div class="shop-infos">
    <p>{ICONES["lieu"]}<span><b>{t(L, "Boutique officielle à l'Urban Studio", "Official shop at Urban Studio")}</b>{URBAN_STUDIO}</span></p>
    <p>{ICONES["calendrier"]}<span><b>{t(L, "Horaires", "Opening hours")}</b>{t(L, HORAIRES_FR, HORAIRES_EN)}</span></p>
    <p>{ICONES["sac"]}<span><b>{t(L, "Pas de livraison pour le moment", "No delivery for now")}</b>{t(L, "Tu réserves ici, tu récupères ta commande sur place.", "Reserve here, pick up your order in store.")}</span></p>
  </div>
</section>

<section class="cadre shop-vedette" aria-labelledby="titre-tshirt" data-produit data-mail="{MAIL}" data-sujet="{e(t(L, 'Réservation — ' + nom_ts, 'Reservation — ' + nom_ts))}" data-corps="{e(t(L, 'Bonjour, je voudrais réserver : ' + nom_ts + ' en taille M. Je viendrai le chercher à l’Urban Studio.', 'Hello, I would like to reserve: ' + nom_ts + ' in size M. I will pick it up at Urban Studio.'))}">
  <div class="shop-vedette-visuel">{tshirt_3d(p, controles=True)}</div>
  <div class="shop-vedette-infos">
    <p class="v3-surtitre">{t(L, 'Édition officielle', 'Official edition')}</p>
    <h2 class="v3-titre" id="titre-tshirt">{nom_ts}</h2>
    <p>{t(L, "T-shirt blanc. Au recto, le logo ARTMADA et la main qui tient la bombe, dessinée par Xän. Au dos, le tag « Lyannaj Karayib ».", "White T-shirt. On the front, the ARTMADA logo and the hand holding the spray can, drawn by Xän. On the back, the “Lyannaj Karayib” tag.")}</p>
    <p class="shop-prix">{t(L, '30 €', '€30')}</p>
    <p class="shop-taille-lib">{t(L, 'Taille', 'Size')} : <b data-taille-choisie>M</b> · {t(L, 'du S au XXL, toutes disponibles', 'S to XXL, all available')}</p>
    <div class="ts-tailles" role="group" aria-label="{t(L, 'Choisir la taille', 'Choose a size')}">{tailles}</div>
    <a class="bouton-noir" data-reserver href="{e(mailto_resa(L, nom_ts, 'M'))}">{t(L, 'Je le réserve', 'Reserve it')} {ICONES["fleche"]}</a>
    <p class="v3-petit">{t(L, "À récupérer à l'Urban Studio, aux horaires d'ouverture.", "Pick it up at Urban Studio during opening hours.")}</p>
  </div>
</section>

<section class="cadre shop-tout" aria-labelledby="titre-tout">
  <div class="v3-entete">
    <h2 class="v3-titre anim-titre" id="titre-tout">{t(L, 'Toute la boutique', 'Everything')}</h2>
    <div class="shop-filtres" data-filtres="grille-shop" role="group" aria-label="{t(L, 'Filtrer', 'Filter')}">{filtres}</div>
  </div>
  <div class="produits" id="grille-shop">{cartes}</div>
  <p class="v3-petit" style="margin-top:32px">{t(L, "« Bientôt disponible » : l'objet arrive à la boutique, ou attend encore l'accord de l'artiste. Vendeur : Urban Studio FWI.", "“Coming soon”: the item is on its way, or still awaiting the artist's agreement. Seller: Urban Studio FWI.")} <a href="{p.u('cgv.html')}">{t(L, 'Conditions de vente', 'Terms of sale')}</a> · <a href="mailto:{MAIL}">{MAIL}</a></p>
</section>
'''
    offres = []
    for pr in produits():
        nom = t(L, *pr["nom"])
        o = {"@type": "Product", "name": nom, "brand": {"@type": "Brand", "name": "ARTMADA Street Festival"}, "description": t(L, *pr["ligne"])}
        if pr["img"]:
            o["image"] = SITE_URL + "assets/" + pr["img"]
        if pr["dispo"] and pr.get("prix"):
            o["offers"] = {"@type": "Offer", "price": pr["prix"][0].split(" ")[0], "priceCurrency": "EUR", "availability": "https://schema.org/InStoreOnly",
                           "seller": {"@type": "Organization", "name": "Urban Studio FWI"}, "url": SITE_URL + ("" if L == "fr" else "en/") + "boutique.html#" + pr["id"]}
        offres.append(o)
    ecrire(p, document(p, t(L, "Shop officiel : t-shirt, casquette, prints", "Official shop: T-shirt, cap, prints"),
                       t(L, "Le shop officiel d'ARTMADA Street Festival : t-shirt (30 €, du S au XXL), casquette (20 €), prints A3 des fresques. Retrait à l'Urban Studio, Les Trois-Îlets, Martinique.", "The official ARTMADA Street Festival shop: T-shirt (€30, S to XXL), cap (€20), A3 mural prints. Pick-up at Urban Studio, Les Trois-Îlets, Martinique."),
                       corps, actif="boutique.html", image="img/da/tshirt-face.webp",
                       ld=offres + [fil_ld(p, [(None, "Shop")])]))

# ============================================================ PAGES LÉGALES (en plus des mentions et de la confidentialité)

def page_legale(p, titre, description, txt):
    corps = f'{bloc_tete(p, [(None, titre)], titre)}<section class="cadre" style="padding-bottom:clamp(64px,8vw,120px)"><div class="prose">{txt}</div></section>'
    ecrire(p, document(p, titre, description, corps))

def legales_plus(lang):
    L = lang
    p = P(lang, "cgu.html")
    txt = t(L, f'''<p>Ces conditions expliquent comment utiliser le site artmadastreetfestival.com. En le consultant, tu les acceptes.</p>
<h2>À quoi sert le site</h2><p>Le site présente le festival ARTMADA Street Festival : programme, lieux, fresques, artistes, shop, presse. Il est gratuit et sans compte.</p>
<h2>Les contenus</h2><p>Les fresques, photos, vidéos, textes, logos et visuels appartiennent à leurs auteurs (artistes, photographes, vidéastes) et à l'association NPL MADA PAINT. Tu peux partager les liens du site. Pour réutiliser un contenu (presse, publication, produit), demande d'abord l'accord écrit : {MAIL}.</p>
<h2>Les informations</h2><p>On fait de notre mieux pour que les infos soient justes et à jour. Le programme, les lieux et les murs peuvent changer (météo, autorisations, sécurité). En cas de doute, écris-nous.</p>
<h2>Les liens vers d'autres sites</h2><p>Le site renvoie vers d'autres services (Google Maps, YouTube, Instagram, Bizouk, médias). Ils ont leurs propres règles et l'association n'en est pas responsable.</p>
<h2>La sécurité</h2><p>Le site est servi uniquement en connexion sécurisée (https), sans compte, sans mot de passe et sans paiement en ligne. Si tu vois un problème, écris à {MAIL}.</p>
<h2>Le droit applicable</h2><p>Ces conditions sont soumises au droit français.</p>
<p class="petit gris">Mis à jour le 20 octobre 2026.</p>''', f'''<p>These terms explain how to use artmadastreetfestival.com. By browsing it, you accept them.</p>
<h2>Purpose</h2><p>The site presents ARTMADA Street Festival: programme, venues, murals, artists, shop, press. It is free and requires no account.</p>
<h2>Content</h2><p>Murals, photos, videos, texts, logos and visuals belong to their authors (artists, photographers, videographers) and to the NPL MADA PAINT association. You may share links to the site. To reuse any content (press, publication, product), first ask for written permission: {MAIL}.</p>
<h2>Information</h2><p>We do our best to keep information accurate and up to date. The programme, venues and walls may change (weather, permits, safety). If in doubt, write to us.</p>
<h2>Links to other sites</h2><p>The site links to other services (Google Maps, YouTube, Instagram, Bizouk, media). They have their own rules and the association is not responsible for them.</p>
<h2>Security</h2><p>The site is served only over a secure connection (https), with no account, no password and no online payment. If you spot a problem, write to {MAIL}.</p>
<h2>Applicable law</h2><p>These terms are governed by French law.</p>
<p class="petit gris">Last updated 20 October 2026.</p>''')
    page_legale(p, t(L, "Conditions d'utilisation", "Terms of use"), t(L, "Conditions générales d'utilisation du site ARTMADA Street Festival.", "Terms of use of the ARTMADA Street Festival website."), txt)

    p = P(lang, "cgv.html")
    txt = t(L, f'''<p>Ces conditions s'appliquent aux objets présentés dans le shop du site (t-shirts, casquettes, prints, tote bags, serviettes).</p>
<h2>Qui vend</h2><ul><li><b>Urban Studio FWI</b>, SAS, SIREN 932 230 592</li><li>Boutique : {URBAN_STUDIO}, Martinique</li><li>Contact : {MAIL}</li></ul>
<p>L'association NPL MADA PAINT, qui édite le site, ne vend pas ces objets.</p>
<h2>Comment commander</h2><p>Le site ne prend pas de paiement. Tu réserves un objet par mail (bouton « Réserver »), on te confirme qu'il est disponible, puis tu viens le récupérer à la boutique, aux horaires d'ouverture : {HORAIRES_FR}.</p>
<h2>Prix</h2><p>Les prix sont en euros, toutes taxes comprises : t-shirt officiel 30 €, casquette 20 €, print A3 30 € (50 € avec cadre). Les objets marqués « Bientôt disponible » ne peuvent pas encore être réservés.</p>
<h2>Livraison</h2><p>Pas de livraison pour le moment : retrait en boutique uniquement.</p>
<h2>Réservation</h2><p>Une réservation est gardée 15 jours après notre confirmation. Passé ce délai, l'objet peut être remis en vente.</p>
<h2>Échange</h2><p>Un objet abîmé ou une mauvaise taille ? Reviens à la boutique avec ton ticket : on cherche une solution (échange selon le stock).</p>
<h2>Litiges</h2><p>Écris d'abord à {MAIL}. Ces conditions sont soumises au droit français.</p>
<p class="petit gris">Mis à jour le 20 octobre 2026.</p>''', f'''<p>These terms apply to items shown in the site's shop (T-shirts, caps, prints, tote bags, towels).</p>
<h2>Seller</h2><ul><li><b>Urban Studio FWI</b>, SAS, SIREN 932 230 592</li><li>Shop: {URBAN_STUDIO}, Martinique</li><li>Contact: {MAIL}</li></ul>
<p>The NPL MADA PAINT association, which publishes the site, does not sell these items.</p>
<h2>How to order</h2><p>The site takes no payment. Reserve an item by email (“Reserve” button), we confirm it is available, then you pick it up at the shop during opening hours: {HORAIRES_EN}.</p>
<h2>Prices</h2><p>Prices are in euros, all taxes included: official T-shirt €30, cap €20, A3 print €30 (€50 framed). Items marked “Coming soon” cannot be reserved yet.</p>
<h2>Delivery</h2><p>No delivery for now: in-store pick-up only.</p>
<h2>Reservations</h2><p>A reservation is held for 15 days after our confirmation. After that, the item may go back on sale.</p>
<h2>Exchanges</h2><p>Damaged item or wrong size? Come back to the shop with your receipt: we will find a solution (exchange subject to stock).</p>
<h2>Disputes</h2><p>Write to {MAIL} first. These terms are governed by French law.</p>
<p class="petit gris">Last updated 20 October 2026.</p>''')
    page_legale(p, t(L, "Conditions de vente", "Terms of sale"), t(L, "Conditions de vente du shop ARTMADA (vendeur : Urban Studio FWI).", "Terms of sale of the ARTMADA shop (seller: Urban Studio FWI)."), txt)

    p = P(lang, "accessibilite.html")
    txt = t(L, f'''<p>On veut que le site soit facile à utiliser pour tout le monde, y compris avec un lecteur d'écran, au clavier ou sur un petit téléphone.</p>
<h2>Ce qu'on a fait</h2><ul><li>Toutes les photos ont un texte qui les décrit.</li><li>Le site se lit au clavier, avec un lien « Aller au contenu » en haut de page.</li><li>Les textes sont assez contrastés et grossissent avec le zoom du navigateur.</li><li>Les animations s'arrêtent si ton téléphone ou ton ordinateur est réglé sur « réduire les animations ». La vidéo d'accueil a un bouton pause.</li><li>Le site existe en français et en anglais.</li></ul>
<h2>Ce qui peut encore gêner</h2><ul><li>La carte interactive est plus difficile à utiliser au clavier : la liste des fresques et les liens « Itinéraire » donnent les mêmes infos.</li><li>L'after movie n'a pas encore de sous-titres.</li></ul>
<h2>Un problème ?</h2><p>Écris à {MAIL} : on te répond et on corrige.</p>
<p class="petit gris">Mis à jour le 20 octobre 2026.</p>''', f'''<p>We want the site to be easy to use for everyone, including with a screen reader, a keyboard or a small phone.</p>
<h2>What we did</h2><ul><li>Every photo has a text describing it.</li><li>The site works with a keyboard, with a “Skip to content” link at the top.</li><li>Texts have good contrast and scale with browser zoom.</li><li>Animations stop if your device is set to “reduce motion”. The home video has a pause button.</li><li>The site exists in French and English.</li></ul>
<h2>Known limits</h2><ul><li>The interactive map is harder to use with a keyboard: the mural list and “Directions” links give the same information.</li><li>The after movie has no subtitles yet.</li></ul>
<h2>A problem?</h2><p>Write to {MAIL}: we will reply and fix it.</p>
<p class="petit gris">Last updated 20 October 2026.</p>''')
    page_legale(p, t(L, "Accessibilité", "Accessibility"), t(L, "Accessibilité du site ARTMADA Street Festival.", "Accessibility of the ARTMADA Street Festival website."), txt)

def bloc_visites(p):
    return f'''
<section class="nuit">
  <div class="cadre section" style="display:flex;flex-direction:column;gap:48px">
    <div style="display:flex;flex-direction:column;gap:16px">
      <span class="etiquette">{T(p, "Toute l'année", 'All year round')}</span>
      <h2 class="titre-section">{T(p, 'Voir, comprendre, peindre', 'See, understand, paint')}</h2>
    </div>
    <div class="g3" style="gap:40px">
      <article class="offre">
        <h3>{T(p, 'Parcours libre', 'Self-guided walk')}</h3>
        <p class="doux">{T(p, "Les fresques des éditions #1 et #2, à pied, à ton rythme, avec la carte. Gratuit.", "The murals of editions #1 and #2, on foot, at your own pace, with the map. Free.")}</p>
        <a href="{p.u('carte.html')}" style="font-weight:700">{T(p, 'Ouvrir la carte', 'Open the map')}</a>
      </article>
      <article class="offre">
        <h3>{T(p, 'Visite guidée · 250 €', 'Guided tour · €250')}</h3>
        <p class="doux">{T(p, "2 heures avec un membre du collectif, pour un groupe jusqu'à 25 personnes : écoles, associations, entreprises.", "2 hours with a member of the collective, for a group of up to 25: schools, associations, companies.")}</p>
        <a href="{p.u('visites.html')}" style="font-weight:700">{T(p, 'Demander une date', 'Request a date')}</a>
      </article>
      <article class="offre forte">
        <h3>{T(p, 'Atelier · 49,90 €', 'Workshop · €49.90')}</h3>
        <p class="doux">{T(p, "Le samedi, de 10h à 12h, 8 places. Initiation sur un vrai mur, puis ton œuvre sur panneau. Avec Doudou Style, à l'Urban Studio, Village de la Poterie, Les Trois-Îlets.", "Saturdays, 10am to 12pm, 8 places. Try it on a real wall, then paint your own panel. With Doudou Style, at Urban Studio, Village de la Poterie, Les Trois-Îlets.")}</p>
        <a class="bouton bouton-jaune-v bouton-petit" href="{BIZOUK}" rel="noopener">{T(p, 'Réserver', 'Book')}</a>
      </article>
    </div>
  </div>
</section>'''

# ============================================================ LE FESTIVAL

def festival(lang):
    p = P(lang, "festival.html")
    if lang == "fr":
        texte = '''<p>On vient tous (artistes, bénévoles, public) d'endroits différents ; pourtant, nous sommes au même endroit, au même moment, durant le festival : sur un mur, sur une île, dans la Caraïbe, sur la planète… Un point sur un globe, et c'est pourtant ici et maintenant que nos routes se croisent. À la croisée des chemins, des cultures et de nos vies, au carrefour des possibles.</p>
<p>Mais <i>« O la nou kay ? »</i> Où allons-nous ? Vers quoi ? Dans quelle direction ? Et quel chemin prendre pour y parvenir ? L'itinéraire classique ? Le raccourci ? La déviation ? Le détour ? Le <i>chimen chien</i> ? Le <i>chimen krochi</i> ? Devrons-nous nous frayer un passage pour atteindre notre but ? Plus que la destination, n'est-ce pas le cheminement le plus important ?</p>
<p><b>À l'heure d'un certain fatalisme social, guerrier, climatique et numérique, un autre chemin est-il possible ?</b></p>
<p>On a choisi un milieu artistique qui n'était pas vraiment un choix de carrière envisageable à l'époque où l'on a commencé la peinture. On a pris un autre chemin que celui que prennent, de façon classique ou académique, ceux qui aiment l'art ou la peinture.</p>
<p>On a appris le graffiti hors des sentiers battus et balisés, sans la reconnaissance des critiques et des institutions de l'époque. Ce chemin nous a (ra)menés à Clément, où l'on a abordé cette notion devenue le titre de l'exposition <i>Mawonaj Piktural</i> : s'évader, trouver une issue, s'échapper des codes de ce monde hermétique, froid et rigide qu'est l'art contemporain.</p>
<p>On a choisi de marronner par la peinture. Pour aller dans la direction voulue, on a choisi de prendre un autre chemin : celui où les murs sont des tableaux, les rues des galeries, et la ville un musée. Mais ce bout de chemin qu'on fait ensemble, cette trace commune qu'on laisse, devient elle-même un autre chemin pour les générations futures.</p>
<p><i>Faire de Fort-de-France la plaque tournante de l'art urbain, du street art et du graffiti dans la Caraïbe ?</i></p>'''
    else:
        texte = '''<p>We all come (artists, volunteers, visitors) from different places; and yet, during the festival, we are in the same place at the same time: on a wall, on an island, in the Caribbean, on the planet… A dot on a globe, and yet it is here and now that our paths cross. At the crossroads of paths, cultures and lives, where everything is possible.</p>
<p>But <i>“O la nou kay?”</i> Where are we going? Towards what? In which direction? And which path should we take to get there? The usual route? The shortcut? The diversion? The detour? The <i>chimen chien</i> (the side path)? The <i>chimen krochi</i> (the crooked path)? Will we have to clear our own way to reach our goal? More than the destination, isn't the journey what matters most?</p>
<p><b>In a time of social, military, climate and digital fatalism, is another way possible?</b></p>
<p>We chose an artistic world that was not really a career option back when we started painting. We took a different path from the classic, academic one taken by those who love art or painting.</p>
<p>We learned graffiti off the beaten track, without the recognition of critics or institutions. That path led us (back) to Clément, where we explored the idea that became the title of the exhibition <i>Mawonaj Piktural</i>: to break away, find a way out, escape the codes of the closed, cold and rigid world of contemporary art.</p>
<p>We chose to run away (<i>marronner</i>) through painting. To go where we wanted, we chose another way: one where walls are canvases, streets are galleries, and the city is a museum. And this stretch of road we travel together, this shared trace we leave behind, becomes another way for future generations.</p>
<p><i>Making Fort-de-France the hub of urban art, street art and graffiti in the Caribbean?</i></p>'''
    corps = f'''
{bloc_tete(p, [(None, T(p, 'Le festival', 'The festival'))], 'ARTMADA #3', T(p, "Du 25 janvier au 4 février 2027, la troisième édition d'ARTMADA Street Festival investit Fort-de-France : de nouvelles fresques, des ateliers, des visites et une block party.", "From 25 January to 4 February 2027, the third edition of ARTMADA Street Festival takes over Fort-de-France: new murals, workshops, tours and a block party."), T(p, 'Édition #3', 'Edition #3'))}

<section class="cadre" style="padding-bottom:clamp(48px,6vw,80px)">
  <dl class="tableau-infos">
    <div><dt>{T(p, 'Dates', 'Dates')}</dt><dd>{T(p, 'Du lundi 25 janvier au jeudi 4 février 2027', 'Monday 25 January to Thursday 4 February 2027')}</dd></div>
    <div><dt>{T(p, 'Thème', 'Theme')}</dt><dd>An Lot Chimen · {T(p, 'Un autre chemin', 'Another way')}</dd></div>
    <div><dt>{T(p, 'Quartiers', 'Neighbourhoods')}</dt><dd>{T(p, 'Langellier, Mongérald, Tocade et le centre-ville de Fort-de-France', 'Langellier, Mongérald, Tocade and Fort-de-France city centre')}</dd></div>
    <div><dt>{T(p, 'Artistes', 'Artists')}</dt><dd>{T(p, 'Annoncés bientôt', 'Coming soon')}</dd></div>
    <div><dt>{T(p, 'Prix', 'Price')}</dt><dd>{T(p, 'Les fresques se regardent gratuitement, dans la rue', 'The murals are free to see, in the street')}</dd></div>
    <div><dt>{T(p, 'Organisation', 'Organised by')}</dt><dd>{T(p, "Association NPL MADA PAINT (collectif Mada Paint), avec la Ville de Fort-de-France", "NPL MADA PAINT association (Mada Paint collective), with the City of Fort-de-France")}</dd></div>
  </dl>
</section>

<section class="cadre" style="padding-bottom:clamp(64px,8vw,120px)">
  <div class="texte-5-7 trait-haut">
    <div style="display:flex;flex-direction:column;gap:12px">
      <h2 class="titre-section">An lot chimen</h2>
      <p class="gris">{T(p, 'Un autre chemin · texte de Xän pour le collectif Mada Paint', 'Another way · text by Xän for the Mada Paint collective')}</p>
    </div>
    <div class="prose" style="font-size:18px">{texte}</div>
  </div>
</section>

<section class="cadre" style="padding-bottom:clamp(64px,8vw,120px)">
  <div class="texte-5-7 trait-haut">
    <h2 class="titre-moyen">{T(p, 'Qui organise', 'Who we are')}</h2>
    <div class="prose">
      <p style="font-size:19px">{T(p, "ARTMADA est porté par Mada Paint, un collectif d'artistes graffeurs martiniquais, réuni dans l'association NPL MADA PAINT. Le festival est né en 2024 avec une idée simple : faire de Fort-de-France une galerie à ciel ouvert, et donner aux artistes de la Caraïbe des murs à la hauteur de leur talent.", "ARTMADA is run by Mada Paint, a collective of Martinican graffiti artists, through the NPL MADA PAINT association. The festival was born in 2024 with a simple idea: turn Fort-de-France into an open-air gallery, and give Caribbean artists walls worthy of their talent.")}</p>
      <div class="boutons"><a class="bouton bouton-contour" href="{p.u('archives.html')}">{T(p, 'Les éditions passées', 'Past editions')}</a><a class="bouton bouton-contour" href="{p.u('artistes/index.html')}">{T(p, 'Les artistes', 'The artists')}</a></div>
    </div>
  </div>
</section>
'''
    ecrire(p, document(p, T(p, 'Le festival · Édition #3', 'The festival · Edition #3'), T(p, "ARTMADA #3 « An Lot Chimen » : dates, thème, quartiers et organisation de la troisième édition du festival de street art de Fort-de-France.", "ARTMADA #3 “An Lot Chimen”: dates, theme, neighbourhoods and organisers of the third edition of Fort-de-France's street art festival."), corps, actif="festival.html", titre_complet=T(p, "ARTMADA #3 · 25 janv. → 4 févr. 2027 | Festival de street art", "ARTMADA #3 · 25 Jan → 4 Feb 2027 | Street art festival"),
                       ld=[festival_ld(p.lang), fil_ld(p, [(None, T(p, "Le festival", "The festival"))])]))

# ============================================================ PROGRAMME

TYPES = {"fresques": ("Fresques", "Murals"), "atelier": ("Atelier", "Workshop"), "soiree": ("Soirée", "Night"),
         "expo": ("Expo", "Exhibition"), "visite": ("Visite", "Tour"), "autre": ("Autre", "Other")}

def evenement_html(p, ev):
    ty = ev.get("type", "autre")
    nom_type = T(p, *TYPES.get(ty, TYPES["autre"]))
    gratuit = f' · <b>{T(p, "Gratuit", "Free")}</b>' if ev.get("gratuit") else ""
    return f'''<li class="evenement">
  <span class="heure">{e(champ(ev, 'heure', p.lang))}</span>
  <div><h3>{e(champ(ev, 'titre', p.lang))}</h3><p class="ou">{e(ev.get('lieu', ''))}{gratuit}</p><p style="margin-top:4px">{e(champ(ev, 'description', p.lang))}</p></div>
  <span class="type t-{ty}">{nom_type}</span>
</li>'''

def programme(lang):
    p = P(lang, "programme.html")
    pr = PROGRAMME
    mois = T(p, "févr.", "Feb")
    nav = "".join(f'<a href="#j{j["jour"]}"><b>{j["jour"]}</b><span>{mois}</span></a>' for j in pr["jours"])
    avant = ""
    for bloc in pr.get("avant", []):
        avant += f'''<article class="jour" id="avant">
  <h2>{e(champ(bloc, 'titre', lang))}<small>{e(bloc['jour'])} {e(champ(bloc, 'mois', lang))} 2026</small></h2>
  <ul class="evenements">{"".join(evenement_html(p, ev) for ev in bloc['evenements'])}</ul>
</article>'''
    jours = ""
    for j in pr["jours"]:
        jours += f'''<article class="jour" id="j{j['jour']}">
  <h2>{e(champ(j, 'nom', lang))} {j['jour']} {mois}<small>{e(champ(j, 'titre', lang))}</small></h2>
  <ul class="evenements">{"".join(evenement_html(p, ev) for ev in j['evenements'])}</ul>
</article>'''
    corps = f'''
{bloc_tete(p, [(None, 'Programme')], T(p, 'Programme', 'Programme'), "", T(p, 'Jour par jour', 'Day by day'))}
<section class="cadre" style="padding-bottom:36px">
  <div class="v3-bientot v3-bientot-clair">
    <p class="v3-bientot-titre">{T(p, 'Programme 2027 bientôt disponible', '2027 programme coming soon')}</p>
    <p>{T(p, "Édition #3 du 25 janvier au 4 février 2027 à Fort-de-France. Le programme jour par jour arrive très vite : inscris-toi en bas de page pour le recevoir dès sa sortie.", "Edition #3 from 25 January to 4 February 2027 in Fort-de-France. The day-by-day programme is coming very soon: sign up at the bottom of the page to get it first.")}</p>
    <div class="boutons"><a class="bouton-noir" href="#news-mail-{lang}">{T(p, 'Me prévenir', 'Notify me')}</a><a class="bouton-ligne-sombre" href="#lieux">{T(p, 'Les lieux du festival', 'Festival venues')}</a></div>
  </div>
</section>
{bloc_lieux(p)}
<section class="cadre" style="padding-top:56px;padding-bottom:20px">
  <h2 class="v3-titre" style="margin-bottom:14px">{T(p, "Pour te donner une idée : l'édition #2", "To give you an idea: edition #2")}</h2>
  <p class="avertissement">{e(champ(pr, 'intro', lang))}</p>
</section>
<section class="cadre" style="padding-bottom:clamp(64px,8vw,120px)">
  <p class="surtitre" style="margin-bottom:12px">ARTMADA #2 · {T(p, 'février 2026', 'February 2026')}</p>
  <nav class="jours-nav" aria-label="{T(p, 'Aller au jour', 'Jump to day')}">{nav}</nav>
  {avant}{jours}
  <div class="boutons" style="margin-top:24px">
    <a class="bouton" href="{INSTA}" rel="noopener">{T(p, "Suivre l'annonce du programme 2027 sur Instagram", "Follow the 2027 programme announcement on Instagram")}</a>
  </div>
</section>
'''
    ecrire(p, document(p, T(p, "Programme", "Festival programme"), T(p, "Le programme jour par jour d'ARTMADA Street Festival : fresques en direct, ateliers, vernissage, open mic, visites et block party à Fort-de-France.", "ARTMADA Street Festival day-by-day programme: live murals, workshops, exhibition, open mic, tours and block party in Fort-de-France."), corps, actif="programme.html", ld=[fil_ld(p, [(None, "Programme")])]))

# ============================================================ VISITES & ATELIERS

def visites(lang):
    p = P(lang, "visites.html")
    corps = f'''
{bloc_tete(p, [(None, T(p, 'Visites & ateliers', 'Tours & workshops'))], T(p, 'Visites & ateliers', 'Tours & workshops'), T(p, "Les fresques restent sur les murs toute l'année. Trois façons de les découvrir, et une façon de prendre la bombe toi-même.", "The murals stay on the walls all year round. Three ways to discover them, and one way to pick up a spray can yourself."), T(p, "Toute l'année", 'All year round'))}
<section class="cadre" style="padding-bottom:clamp(64px,8vw,120px)">
  <div class="g3" style="gap:40px">
    <article class="chaux-offre">
      <h2 class="titre-moyen" style="font-size:30px">{T(p, 'Parcours libre', 'Self-guided walk')}</h2>
      <p>{T(p, "Les fresques des éditions #1 et #2 sont réparties dans Fort-de-France : Canal Alaric, Pointe Simon, rue Victor Sévère, Perrinon, Clarac, Ozanam… Prends la carte et marche à ton rythme.", "The murals of editions #1 and #2 are spread across Fort-de-France: Canal Alaric, Pointe Simon, rue Victor Sévère, Perrinon, Clarac, Ozanam… Take the map and walk at your own pace.")}</p>
      <dl class="tableau-infos"><div><dt>{T(p, 'Prix', 'Price')}</dt><dd>{T(p, 'Gratuit', 'Free')}</dd></div><div><dt>{T(p, 'Durée', 'Duration')}</dt><dd>{T(p, '1 h 30 à 3 h, à pied', '1.5 to 3 hours, on foot')}</dd></div></dl>
      <a class="bouton bouton-contour" href="{p.u('carte.html')}">{T(p, 'Ouvrir la carte', 'Open the map')}</a>
    </article>
    <article class="chaux-offre">
      <h2 class="titre-moyen" style="font-size:30px">{T(p, 'Visite guidée', 'Guided tour')}</h2>
      <p>{T(p, "Un membre du collectif te raconte les murs : les artistes, les techniques, les histoires derrière chaque fresque. Pour les écoles, les associations, les entreprises, les groupes de touristes.", "A member of the collective tells you the story of the walls: the artists, the techniques, the stories behind each mural. For schools, associations, companies and tourist groups.")}</p>
      <dl class="tableau-infos"><div><dt>{T(p, 'Prix', 'Price')}</dt><dd>{T(p, '250 € par groupe', '€250 per group')}</dd></div><div><dt>{T(p, 'Durée', 'Duration')}</dt><dd>{T(p, '2 heures', '2 hours')}</dd></div><div><dt>{T(p, 'Groupe', 'Group')}</dt><dd>{T(p, "Jusqu'à 25 personnes", 'Up to 25 people')}</dd></div></dl>
      <a class="bouton" href="mailto:{MAIL}?subject={T(p, 'Visite%20guid%C3%A9e%20ARTMADA', 'ARTMADA%20guided%20tour')}">{T(p, 'Demander une date', 'Request a date')}</a>
    </article>
    <article class="chaux-offre forte">
      <h2 class="titre-moyen" style="font-size:30px">{T(p, 'Atelier graffiti', 'Graffiti workshop')}</h2>
      <p>{T(p, "Une initiation sur un vrai mur, puis tu repars avec ton œuvre sur panneau. Avec l'artiste Doudou Style, à la galerie Urban Studio.", "Try it on a real wall, then take home your own painted panel. With the artist Doudou Style, at the Urban Studio gallery.")}</p>
      <dl class="tableau-infos"><div><dt>{T(p, 'Prix', 'Price')}</dt><dd>{T(p, '49,90 € tout compris', '€49.90 all included')}</dd></div><div><dt>{T(p, 'Quand', 'When')}</dt><dd>{T(p, 'Le samedi, 10h–12h', 'Saturdays, 10am–12pm')}</dd></div><div><dt>{T(p, 'Places', 'Places')}</dt><dd>8</dd></div><div><dt>{T(p, 'Où', 'Where')}</dt><dd>Urban Studio, Village de la Poterie, Les Trois-Îlets</dd></div></dl>
      <a class="bouton bouton-jaune-v" href="{BIZOUK}" rel="noopener">{T(p, 'Réserver sur Bizouk', 'Book on Bizouk')}</a>
    </article>
  </div>
  <p class="petit gris" style="margin-top:40px">{T(p, "Groupe, école, entreprise, anniversaire : l'atelier se fait aussi sur devis. Écris-nous à", "Group, school, company, birthday: the workshop is also available on request. Write to us at")} <a href="mailto:{MAIL}">{MAIL}</a>.</p>
</section>
'''
    ecrire(p, document(p, T(p, 'Visites & ateliers', 'Tours & workshops'), T(p, "Découvrir les fresques d'ARTMADA à Fort-de-France : parcours libre gratuit, visite guidée pour les groupes, atelier graffiti le samedi.", "Discover ARTMADA's murals in Fort-de-France: free self-guided walk, guided tours for groups, Saturday graffiti workshop."), corps, actif="visites.html", ld=[fil_ld(p, [(None, T(p, "Visites & ateliers", "Tours & workshops"))])]))

# ============================================================ BÉNÉVOLES

def benevoles(lang):
    p = P(lang, "benevoles.html")
    missions = [
        ("Accueil", "Welcome", "Accueillir le public, orienter, répondre aux questions sur les murs.", "Welcome visitors, give directions, answer questions about the walls."),
        ("Logistique", "Logistics", "Préparer le matériel, aider sur les murs, ranger en fin de journée.", "Prepare equipment, help on the walls, tidy up at the end of the day."),
        ("Chauffeur", "Driver", "Conduire les artistes entre leur logement, les murs et les soirées.", "Drive the artists between their lodging, the walls and the events."),
        ("Photo & vidéo", "Photo & video", "Garder la trace du festival, jour après jour.", "Capture the festival, day after day."),
        ("Soirées", "Events", "Bar, entrée, installation pendant les soirées et la block party.", "Bar, entrance and set-up during the parties and the block party."),
        ("Ateliers", "Workshops", "Encadrer les participants aux côtés des artistes.", "Support participants alongside the artists."),
    ]
    cartes = "".join(f'<article class="chaux-offre"><h2 style="font-size:28px">{T(p, a, b)}</h2><p>{T(p, c, d)}</p></article>' for a, b, c, d in missions)
    corps = f'''
{bloc_tete(p, [(None, T(p, 'Bénévoles', 'Volunteers'))], T(p, 'Le festival se fait ensemble', 'We make it together'), T(p, "75 bénévoles ont fait vivre ARTMADA #2. Pour l'édition #3, on cherche à nouveau des bras, des sourires et des chauffeurs. Même quelques heures comptent.", "75 volunteers brought ARTMADA #2 to life. For edition #3, we need hands, smiles and drivers again. Even a few hours make a difference."), T(p, 'Bénévoles', 'Volunteers'))}
<section class="cadre" style="padding-bottom:clamp(48px,6vw,80px)"><div class="g3" style="gap:32px">{cartes}</div></section>
<section class="cadre" style="padding-bottom:clamp(64px,8vw,120px)">
  <div class="texte-5-7 trait-haut">
    <h2 class="titre-moyen">{T(p, "Comment s'inscrire", 'How to sign up')}</h2>
    <div class="prose">
      <p style="font-size:19px">{T(p, "Envoie-nous un mail avec ton nom, ton téléphone, tes disponibilités entre le 25 janvier et le 4 février 2027 et les missions qui te tentent. On te recontacte avant le festival.", "Send us an email with your name, phone number, your availability between 25 January and 4 February 2027 and the missions you'd like. We'll get back to you before the festival.")}</p>
      <ul><li>{T(p, "Pas besoin de savoir peindre.", "No painting skills needed.")}</li><li>{T(p, "T-shirt du festival offert, repas pendant les missions.", "Festival T-shirt included, meals during your shifts.")}</li><li>{T(p, "Bientôt : l'inscription directement dans l'appli ARTMADA.", "Coming soon: sign up directly in the ARTMADA app.")}</li></ul>
      <div class="boutons"><a class="bouton" href="mailto:{MAIL}?subject={T(p, 'Je%20deviens%20b%C3%A9n%C3%A9vole%20ARTMADA%20%233', 'Volunteer%20ARTMADA%20%233')}">{T(p, 'Je deviens bénévole', 'Become a volunteer')}</a></div>
    </div>
  </div>
</section>
'''
    ecrire(p, document(p, T(p, 'Bénévoles', 'Volunteers'), T(p, "Deviens bénévole pour ARTMADA #3, du 25 janvier au 4 février 2027 à Fort-de-France : accueil, logistique, chauffeur, photo, soirées, ateliers.", "Volunteer for ARTMADA #3, 25 January to 4 February 2027 in Fort-de-France: welcome, logistics, driving, photo, events, workshops."), corps, actif="benevoles.html", ld=[fil_ld(p, [(None, T(p, "Bénévoles", "Volunteers"))])]))

# ============================================================ PARTENAIRES

def partenaires(lang):
    p = P(lang, "partenaires.html")
    liste = "".join(f'<li>{e(n)}<small>{T(p, a, b)}</small></li>' for n, a, b in PARTENAIRES)
    corps = f'''
{bloc_tete(p, [(None, T(p, 'Partenaires', 'Partners'))], T(p, 'Merci', 'Thank you'), T(p, "ARTMADA #2 a existé grâce à eux : des institutions, des entreprises de Martinique, des médias, et tous ceux qui ont prêté un mur, une nacelle ou des pots de peinture.", "ARTMADA #2 happened thanks to them: institutions, Martinican companies, media, and everyone who lent a wall, an aerial lift or tins of paint."), T(p, 'Partenaires', 'Partners'))}
<section class="cadre" style="padding-bottom:clamp(48px,6vw,80px)">
  <p class="surtitre" style="margin-bottom:14px">{T(p, 'Partenaires de l’édition #2', 'Edition #2 partners')}</p>
  <ul class="partenaires-liste">{liste}</ul>
</section>
<section class="nuit">
  <div class="cadre section texte-5-7">
    <h2 class="titre-section">{T(p, 'Devenir partenaire de l’édition #3', 'Partner with edition #3')}</h2>
    <div style="display:flex;flex-direction:column;gap:18px">
      <p style="font-size:19px">{T(p, "Associer ton nom à un festival vu par plus d'un million de personnes en ligne, offrir un mur, une nacelle, de la peinture, un hébergement, ou soutenir un quartier : il y a plusieurs façons d'en être.", "Link your name to a festival seen by over a million people online, offer a wall, an aerial lift, paint or accommodation, or support a neighbourhood: there are many ways to be part of it.")}</p>
      <div class="chiffres"><div><b>1,2 M</b><span class="doux" style="color:var(--nuit-texte)">{T(p, 'vues en ligne (2026)', 'online views (2026)')}</span></div><div><b>1 500</b><span style="color:var(--nuit-texte)">{T(p, 'personnes à la block party', 'people at the block party')}</span></div><div><b>26</b><span style="color:var(--nuit-texte)">{T(p, 'fresques en 2026', 'murals in 2026')}</span></div></div>
      <a class="bouton bouton-jaune-v" style="align-self:flex-start" href="mailto:{MAIL}?subject={T(p, 'Partenariat%20ARTMADA%20%233', 'ARTMADA%20%233%20partnership')}">{T(p, 'Nous écrire', 'Get in touch')}</a>
    </div>
  </div>
</section>
'''
    ecrire(p, document(p, T(p, 'Partenaires', 'Partners'), T(p, "Les partenaires d'ARTMADA Street Festival, et comment soutenir l'édition #3.", "ARTMADA Street Festival's partners, and how to support edition #3."), corps, actif="partenaires.html", ld=[fil_ld(p, [(None, T(p, "Partenaires", "Partners"))])]))

# ============================================================ INFOS PRATIQUES

def infos(lang):
    p = P(lang, "infos.html")
    faq = [
        ("C'est payant ?", "Does it cost anything?", "Non. Les fresques se regardent gratuitement, dans la rue, pendant et après le festival. Les ateliers gratuits du festival sont sur inscription. Seuls l'atelier du samedi à l'Urban Studio (49,90 €) et les visites guidées de groupe (250 €) sont payants.", "No. The murals are free to see, in the street, during and after the festival. The festival's free workshops require registration. Only the Saturday workshop at Urban Studio (€49.90) and group guided tours (€250) are paid."),
        ("Où voir les fresques ?", "Where can I see the murals?", "Dans Fort-de-France : Canal Alaric, Pointe Simon, rue Victor Sévère, Perrinon, Clarac, Ozanam… et, pour l'édition #3, Langellier, Mongérald et Tocade. Tout est sur la carte.", "In Fort-de-France: Canal Alaric, Pointe Simon, rue Victor Sévère, Perrinon, Clarac, Ozanam… and, for edition #3, Langellier, Mongérald and Tocade. Everything is on the map."),
        ("Peut-on regarder les artistes peindre ?", "Can I watch the artists paint?", "Oui, c'est tout l'intérêt ! Pendant le festival, les artistes peignent en journée. Reste derrière les barrières de sécurité et n'hésite pas à leur parler pendant leurs pauses.", "Yes, that's the whole point! During the festival, the artists paint during the day. Stay behind the safety barriers and feel free to chat with them during their breaks."),
        ("Comment venir ?", "How do I get there?", "Les murs du centre-ville se font à pied. Pour les quartiers, le bus et le BHNS de la RTM passent tout près. Évite la voiture en centre-ville les soirs de fête.", "City-centre walls are best on foot. For the neighbourhoods, RTM buses and the BHNS rapid bus stop close by. Avoid driving in the city centre on party nights."),
        ("Je suis artiste, comment participer ?", "I'm an artist, how can I take part?", "Les artistes sont choisis par le collectif Mada Paint. Envoie ton portfolio et ton Instagram à contact@artmadastreetfestival.com : on regarde tout.", "Artists are selected by the Mada Paint collective. Send your portfolio and Instagram to contact@artmadastreetfestival.com: we look at everything."),
        ("J'ai un mur à proposer", "I have a wall to offer", "Écris-nous avec l'adresse, une photo et les dimensions du mur. Pour une fresque en dehors du festival, l'Urban Studio peut aussi te faire un devis.", "Write to us with the address, a photo and the wall's dimensions. For a mural outside the festival, Urban Studio can also give you a quote."),
        ("Les photos, je peux les utiliser ?", "Can I use the photos?", "Pour un usage personnel, oui, en citant l'artiste. Pour la presse ou un usage commercial, demande d'abord : chaque fresque appartient à son artiste.", "For personal use, yes, credit the artist. For press or commercial use, ask first: each mural belongs to its artist."),
    ]
    items = "".join(f'<details><summary>{T(p, q, qe)}</summary><div><p>{T(p, r, re_)}</p></div></details>' for q, qe, r, re_ in faq)
    corps = f'''
{bloc_tete(p, [(None, T(p, 'Infos pratiques', 'Practical info'))], T(p, 'Infos pratiques', 'Practical info'), "", T(p, 'Questions fréquentes', 'FAQ'))}
<section class="cadre" style="padding-bottom:clamp(48px,6vw,80px)"><div class="faq">{items}</div></section>
<section class="cadre" style="padding-bottom:clamp(64px,8vw,120px)" id="contact">
  <div class="texte-5-7 trait-haut">
    <h2 class="titre-moyen">Contact</h2>
    <dl class="tableau-infos">
      <div><dt>Mail</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
      <div><dt>Instagram</dt><dd><a href="{INSTA}" rel="noopener">@artmadastreetfestival972</a></dd></div>
      <div><dt>{T(p, 'Presse', 'Press')}</dt><dd><a href="{p.u('presse.html')}">{T(p, 'Espace presse', 'Press area')}</a></dd></div>
      <div><dt>{T(p, 'Association', 'Association')}</dt><dd>NPL MADA PAINT · Fort-de-France, Martinique</dd></div>
    </dl>
  </div>
</section>
'''
    ecrire(p, document(p, T(p, 'Infos pratiques', 'Practical info'), T(p, "Questions fréquentes et contact d'ARTMADA Street Festival à Fort-de-France.", "FAQ and contact for ARTMADA Street Festival in Fort-de-France."), corps, actif="infos.html", ld=[fil_ld(p, [(None, T(p, "Infos pratiques", "Practical info"))]),
                       {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": T(p, q, qe), "acceptedAnswer": {"@type": "Answer", "text": T(p, r, re_)}} for q, qe, r, re_ in faq]}]))

# ============================================================ PAGES LÉGALES

def legales(lang):
    p = P(lang, "mentions-legales.html")
    if lang == "fr":
        txt = f'''<h2>Qui édite ce site</h2>
<p>Le site artmadastreetfestival.com est édité par l'association <b>NPL MADA PAINT</b>, association loi 1901.</p>
<ul><li>Numéro RNA : W9M1010969</li><li>SIREN : 897 410 858 · SIRET du siège : 897 410 858 00012</li><li>Siège : Résidence Aigue Marine, bâtiment 2, appartement 29, rue de la Dorsale, 97200 Fort-de-France, Martinique</li><li>Contact : {MAIL}</li><li>Présidente de l'association : Jennifer Monlouis Bonnaire</li><li>Responsable de la publication et du site : Thibault Mauconduit</li></ul>
<h2>Qui héberge ce site</h2>
<p>Le site est hébergé par <b>GitHub, Inc.</b> (service GitHub Pages), 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis · github.com.</p>
<p>Le nom de domaine est enregistré chez <b>OVH SAS</b>, 2 rue Kellermann, 59100 Roubaix, France.</p>
<h2>Les œuvres et les photos</h2>
<p>Chaque fresque montrée sur ce site est l'œuvre de l'artiste nommé avec sa photo. Les fresques, leurs photos, les textes et le logo ARTMADA sont protégés par le droit d'auteur.</p>
<p>Pour utiliser une photo ou une œuvre (presse, publication, produit), demande d'abord l'accord écrit de l'association et de l'artiste : {MAIL}.</p>
<h2>Tes données</h2>
<p>Ce site ne dépose aucun cookie et ne mesure pas ton audience. Tout est expliqué dans la page <a href="{p.u('confidentialite.html')}">Confidentialité</a>.</p>
<p class="petit gris">Mis à jour le 19 octobre 2026.</p>'''
    else:
        txt = f'''<h2>Publisher</h2>
<p>The website artmadastreetfestival.com is published by <b>NPL MADA PAINT</b>, a French non-profit association (loi 1901).</p>
<ul><li>RNA number: W9M1010969</li><li>SIREN: 897 410 858 · SIRET: 897 410 858 00012</li><li>Registered office: Résidence Aigue Marine, bâtiment 2, appartement 29, rue de la Dorsale, 97200 Fort-de-France, Martinique</li><li>Contact: {MAIL}</li><li>President of the association: Jennifer Monlouis Bonnaire</li><li>Publication and website manager: Thibault Mauconduit</li></ul>
<h2>Hosting</h2>
<p>The site is hosted by <b>GitHub, Inc.</b> (GitHub Pages), 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA · github.com.</p>
<p>The domain name is registered with <b>OVH SAS</b>, 2 rue Kellermann, 59100 Roubaix, France.</p>
<h2>Artworks and photos</h2>
<p>Each mural shown on this site is the work of the artist named with its photo. The murals, their photos, the texts and the ARTMADA logo are protected by copyright.</p>
<p>To use a photo or an artwork (press, publication, product), first ask for written permission from the association and the artist: {MAIL}.</p>
<h2>Your data</h2>
<p>This site sets no cookies and does not track its audience. See the <a href="{p.u('confidentialite.html')}">Privacy</a> page.</p>
<p class="petit gris">Last updated 19 October 2026.</p>'''
    corps = f'{bloc_tete(p, [(None, T(p, "Mentions légales", "Legal notice"))], T(p, "Mentions légales", "Legal notice"))}<section class="cadre" style="padding-bottom:clamp(64px,8vw,120px)"><div class="prose">{txt}</div></section>'
    ecrire(p, document(p, T(p, "Mentions légales", "Legal notice"), T(p, "Mentions légales du site ARTMADA Street Festival.", "Legal notice of the ARTMADA Street Festival website."), corps))

    p = P(lang, "confidentialite.html")
    if lang == "fr":
        txt = f'''<p>Cette page explique quelles informations l'association NPL MADA PAINT reçoit quand tu utilises le site ARTMADA ou l'appli ARTMADA, à quoi elles servent, et comment les faire effacer. Elle s'applique au site artmadastreetfestival.com et à l'appli mobile ARTMADA (iPhone et Android).</p>
<h2>Qui est responsable</h2>
<p>L'association <b>NPL MADA PAINT</b> (SIREN 897 410 858), Résidence Aigue Marine, bâtiment 2, appartement 29, rue de la Dorsale, 97200 Fort-de-France, Martinique. Pour toute question sur tes données : <b>{MAIL}</b>.</p>
<h2>Sur ce site</h2>
<ul><li>Pas de compte, pas de cookie, pas de publicité, pas de mesure d'audience.</li><li>L'inscription à la newsletter et les réservations du shop ouvrent un mail vers {MAIL} depuis ta propre messagerie : rien n'est enregistré par le site.</li><li>La vidéo de la page d'accueil est servie par le site lui-même.</li><li>Les polices d'écriture et les images sont chargées depuis le site lui-même.</li><li>Sur la page « Carte », le fond de carte vient d'OpenStreetMap et l'outil de carte de cdnjs (Cloudflare) : ces services reçoivent ton adresse IP pour afficher la carte. Les liens « Y aller à pied » t'emmènent sur Google Maps, et le parcours guidé sur Creapolis ; ces services ont leurs propres règles.</li><li>L'hébergeur (GitHub) enregistre l'adresse IP des visiteurs dans ses journaux techniques, pour la sécurité du service. L'association n'y a pas accès.</li><li>Les liens vers Instagram, YouTube ou Bizouk t'emmènent sur ces services, qui ont leurs propres règles.</li><li>L'after movie de la page d'accueil est hébergé sur YouTube (mode « confidentialité renforcée ») : rien n'est chargé depuis YouTube tant que tu ne cliques pas sur la vidéo.</li></ul>
<h2>Quand tu nous écris</h2>
<p>Si tu nous écris (bénévolat, partenariat, visite, presse), on garde ton nom, ton adresse mail, ton téléphone et ce que tu nous dis, uniquement pour te répondre et organiser le festival. On les garde au plus 3 ans après notre dernier échange.</p>
<h2>Dans l'appli ARTMADA</h2>
<p>L'appli est gratuite. Une partie marche sans compte (la carte, les fresques, les parcours). Si tu crées un compte ou si tu utilises certaines fonctions, voici ce que l'appli utilise :</p>
<ul><li><b>Ton compte</b> : nom, prénom, adresse mail. Pour te connecter, garder ton passeport à tampons et tes réservations.</li><li><b>Tes réservations</b> (ateliers, visites) : date, nombre de personnes, montant. Les ateliers de la galerie Urban Studio sont vendus par Urban Studio FWI, qui reçoit ta réservation.</li><li><b>Le paiement</b> : il est fait par <b>Stripe</b>. Ton numéro de carte va directement chez Stripe : ni l'association ni l'appli ne le voient ni ne le gardent.</li><li><b>Ta position</b> : seulement si tu l'autorises, pour montrer les fresques près de toi. Elle reste sur ton téléphone.</li><li><b>Les notifications</b> : seulement si tu les autorises.</li><li><b>L'espace bénévoles</b> : nom, téléphone, disponibilités et missions choisies, visibles seulement par l'équipe d'organisation.</li></ul>
<p>On ne vend pas tes données, on ne fait pas de publicité, et on ne te suit pas d'une appli à l'autre.</p>
<h2>Qui d'autre les voit</h2>
<p>Seulement les services techniques qui font marcher le site et l'appli (hébergement, base de données, envoi de mails et de notifications, paiement par Stripe), et Urban Studio FWI pour les ateliers qu'elle organise. Chacun ne reçoit que ce dont il a besoin.</p>
<h2>Combien de temps</h2>
<ul><li>Compte de l'appli : tant que tu le gardes. Tu peux le supprimer à tout moment depuis l'appli, rubrique « Moi », ou en nous écrivant. Tout est alors effacé sous 30 jours.</li><li>Réservations et paiements : 10 ans, parce que la loi oblige à garder les pièces comptables.</li><li>Bénévoles : jusqu'à 2 ans après ta dernière participation.</li></ul>
<h2>Tes droits</h2>
<p>Tu peux à tout moment voir les données qu'on a sur toi, les corriger, les faire effacer, les récupérer, ou refuser qu'on s'en serve. Écris à <b>{MAIL}</b> : on te répond sous un mois. Si tu n'es pas d'accord avec notre réponse, tu peux te plaindre auprès de la CNIL : cnil.fr.</p>
<h2>Les enfants</h2>
<p>L'appli n'est pas faite pour les enfants de moins de 15 ans sans l'accord de leurs parents. Pour un enfant, c'est un parent qui crée le compte et fait les réservations.</p>
<p class="petit gris">Mis à jour le 19 octobre 2026. Si cette page change, la date ci-dessus change aussi.</p>'''
    else:
        txt = f'''<p>This page explains what information the NPL MADA PAINT association receives when you use the ARTMADA website or the ARTMADA app, what it is used for, and how to have it deleted. It applies to artmadastreetfestival.com and to the ARTMADA mobile app (iPhone and Android).</p>
<h2>Who is responsible</h2>
<p><b>NPL MADA PAINT</b> (SIREN 897 410 858), Résidence Aigue Marine, bâtiment 2, appartement 29, rue de la Dorsale, 97200 Fort-de-France, Martinique. For any question about your data: <b>{MAIL}</b>.</p>
<h2>On this website</h2>
<ul><li>No account, no cookies, no advertising, no audience tracking.</li><li>Newsletter sign-up and shop reservations open an email to {MAIL} from your own mail app: nothing is stored by the site.</li><li>The home page video is served by the site itself.</li><li>Fonts and images are served from the site itself.</li><li>On the “Map” page, map tiles come from OpenStreetMap and the map library from cdnjs (Cloudflare): these services receive your IP address to display the map. “Walk there” links take you to Google Maps, and the guided tour to Creapolis; these services have their own rules.</li><li>The host (GitHub) records visitors' IP addresses in its technical logs for security. The association has no access to them.</li><li>Links to Instagram, YouTube or Bizouk take you to those services, which have their own rules.</li><li>The after movie on the home page is hosted on YouTube (privacy-enhanced mode): nothing loads from YouTube until you click the video.</li></ul>
<h2>When you write to us</h2>
<p>If you write to us (volunteering, partnership, tour, press), we keep your name, email address, phone number and what you tell us, only to reply and organise the festival. We keep it for up to 3 years after our last exchange.</p>
<h2>In the ARTMADA app</h2>
<p>The app is free. Part of it works without an account (map, murals, routes). If you create an account or use certain features, the app uses:</p>
<ul><li><b>Your account</b>: first name, last name, email address. To log you in and keep your stamp passport and bookings.</li><li><b>Your bookings</b> (workshops, tours): date, number of people, amount. Workshops at the Urban Studio gallery are sold by Urban Studio FWI, which receives your booking.</li><li><b>Payment</b>: handled by <b>Stripe</b>. Your card number goes straight to Stripe: neither the association nor the app ever sees or stores it.</li><li><b>Your location</b>: only if you allow it, to show murals near you. It stays on your phone.</li><li><b>Notifications</b>: only if you allow them.</li><li><b>Volunteer area</b>: name, phone, availability and chosen missions, visible only to the organising team.</li></ul>
<p>We do not sell your data, we do not advertise, and we do not track you across apps.</p>
<h2>Who else sees it</h2>
<p>Only the technical services that run the site and the app (hosting, database, email and notification delivery, Stripe payments), and Urban Studio FWI for the workshops it runs. Each receives only what it needs.</p>
<h2>How long</h2>
<ul><li>App account: as long as you keep it. You can delete it at any time in the app (“Me” section) or by writing to us. Everything is then erased within 30 days.</li><li>Bookings and payments: 10 years, as required by accounting law.</li><li>Volunteers: up to 2 years after your last participation.</li></ul>
<h2>Your rights</h2>
<p>You can at any time access, correct, delete or retrieve your data, or object to its use. Write to <b>{MAIL}</b>: we reply within one month. If you disagree with our answer, you can complain to the CNIL (French data protection authority): cnil.fr.</p>
<h2>Children</h2>
<p>The app is not intended for children under 15 without parental consent. For a child, a parent creates the account and makes the bookings.</p>
<p class="petit gris">Last updated 19 October 2026. If this page changes, the date above changes too.</p>'''
    corps = f'{bloc_tete(p, [(None, T(p, "Confidentialité", "Privacy"))], T(p, "Confidentialité", "Privacy"))}<section class="cadre" style="padding-bottom:clamp(64px,8vw,120px)"><div class="prose">{txt}</div></section>'
    ecrire(p, document(p, T(p, "Confidentialité", "Privacy"), T(p, "Politique de confidentialité du site et de l'appli ARTMADA.", "Privacy policy of the ARTMADA website and app."), corps))

def page_404():
    p = P("fr", "404.html")
    p.racine = "/"; p.base = "/"; p.chemin = ""   # bouton EN -> /en/
    corps = f'''{bloc_tete(p, None, "Mur introuvable", "Cette page n'existe pas (ou plus). Les fresques, elles, sont toujours là. · This page doesn't exist.", "404")}
<section class="cadre" style="padding-bottom:120px"><div class="boutons"><a class="bouton" href="/">Retour à l'accueil</a><a class="bouton bouton-contour" href="/en/">English</a></div></section>'''
    return document(p, "404", "Page introuvable", corps, noindex=True)

# ============================================================ ensemble

def toutes_les_pages(lang):
    accueil(lang)
    boutique(lang)
    legales_plus(lang)
    festival(lang)
    programme(lang)
    visites(lang)
    benevoles(lang)
    partenaires(lang)
    infos(lang)
    legales(lang)
    import pages_donnees as PD
    PD.toutes(lang)
