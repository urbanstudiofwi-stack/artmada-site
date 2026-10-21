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

def tshirt_3d(p, grand=False, controles=False):
    """Le t-shirt officiel qui tourne sur lui-même (face, puis dos)."""
    cls = "ts-scene ts-grand" if grand else "ts-scene"
    boutons = ""
    if controles:
        boutons = f'''<div class="ts-boutons" role="group" aria-label="{T(p, 'Voir le t-shirt', 'View the T-shirt')}">
  <button type="button" data-ts-vue="tourne" aria-pressed="true">{T(p, 'Il tourne', 'Spin')}</button>
  <button type="button" data-ts-vue="face" aria-pressed="false">{T(p, 'Face', 'Front')}</button>
  <button type="button" data-ts-vue="dos" aria-pressed="false">{T(p, 'Dos', 'Back')}</button>
</div>'''
    return f'''<div class="{cls}" data-ts data-vue="tourne">
  <div class="ts-carte">
    <img class="ts-face" src="{p.a('img/da/tshirt-face.webp')}" alt="{T(p, "T-shirt officiel ARTMADA, face : logo et main tenant une bombe de peinture", "Official ARTMADA T-shirt, front: logo and hand holding a spray can")}" width="785" height="900" loading="lazy" decoding="async">
    <img class="ts-dos" src="{p.a('img/da/tshirt-dos.webp')}" alt="{T(p, "T-shirt officiel ARTMADA, dos : petit logo et tag Lyannaj Karayib", "Official ARTMADA T-shirt, back: small logo and Lyannaj Karayib tag")}" width="784" height="900" loading="lazy" decoding="async">
  </div>
  <span class="ts-ombre" aria-hidden="true"></span>
</div>{boutons}'''

def accueil(lang):
    p = P(lang, "index.html")
    une = [f for f in FRESQUES if f.get("une")][:6]
    if len(une) < 6:
        une += [f for f in FRESQUES if f not in une and f.get("photo")][:6 - len(une)]
    affiches = ""
    for f in une:
        affiches += f'''<a class="da-affiche rv" href="{p.u('fresques/' + f['slug'] + '.html')}"><span class="da-scotch" aria-hidden="true"></span>{img_fresque(p, f)}<span class="da-affiche-nom">{e(nom_artistes(f))} · {e(f.get('lieu') or 'Fort-de-France')}</span></a>'''
    noms_part = "".join(f"<span>{e(n)}</span>" for n, _, _ in PARTENAIRES)
    a = p.a
    corps = f'''
<section class="da-hero da-beton" aria-labelledby="titre-accueil">
  <img class="da-splash" src="{a('img/da/splash.webp')}" srcset="{a('img/da/splash-640.webp')} 640w, {a('img/da/splash.webp')} 1000w" sizes="(max-width: 640px) 130vw, 68vw" alt="" width="1000" height="1099" fetchpriority="high" decoding="async">
  <img class="da-grillage" src="{a('img/da/grillage.webp')}" alt="" width="420" height="618" decoding="async">
  <div class="cadre da-hero-in">
    <div class="da-hero-texte">
      <h1 id="titre-accueil" class="da-h1"><img class="da-logo" src="{a('img/da/logo-halo.webp')}" srcset="{a('img/da/logo-halo-800.webp')} 800w, {a('img/da/logo-halo.webp')} 1600w" sizes="(max-width: 900px) 92vw, 820px" alt="ARTMADA" width="1600" height="529" decoding="async"><span class="sr"> Street Festival #3 · Fort-de-France, Martinique</span></h1>
      <img class="da-script" src="{a('img/da/street-festival.webp')}" alt="" width="1000" height="199" decoding="async">
      <div class="da-badges">
        <span class="da-edition">{T(p, 'Édition #3', 'Edition #3')}</span>
        <span class="da-lieu">Fort-de-France · Martinique</span>
      </div>
      <div class="da-cartouche">
        <img src="{a('img/da/spray-cartouche.webp')}" alt="" width="620" height="622" decoding="async">
        <p>{T(p, 'du 25 janv.<br>au 4 févr.', '25 Jan<br>to 4 Feb')}<br><b>2027</b></p>
      </div>
      <div class="boutons da-boutons">
        <a class="bouton bouton-orange" href="{p.u('programme.html')}">{T(p, 'Le programme', 'Programme')}</a>
        <a class="bouton bouton-clair" href="{p.u('fresques/index.html')}">{T(p, 'Voir les murs', 'See the walls')}</a>
      </div>
    </div>
    <div class="da-bombe-boite"><img class="da-bombe" src="{a('img/da/bombe-mains.webp')}" srcset="{a('img/da/bombe-mains-600.webp')} 600w, {a('img/da/bombe-mains.webp')} 1100w" sizes="(max-width: 640px) 50vw, 520px" alt="" width="1100" height="1131" decoding="async"></div>
  </div>
</section>
<div class="da-coulure" aria-hidden="true"><img src="{a('img/da/coulure.webp')}" srcset="{a('img/da/coulure-900.webp')} 900w, {a('img/da/coulure.webp')} 1800w" sizes="100vw" alt="" width="1800" height="539" decoding="async"></div>

<section class="da-beton-sombre da-theme">
  <div class="cadre" style="display:flex;flex-direction:column;gap:22px">
    <span class="surtitre da-jaune">{T(p, "Le thème de l'édition #3", 'The theme of edition #3')}</span>
    <h2 class="da-geant rv">An Lot Chimen</h2>
    <svg class="da-chemin rv" viewBox="0 0 1300 110" aria-hidden="true"><defs><mask id="masque-chemin"><path class="da-trace" d="M10 80 C 220 20, 420 100, 640 50 S 1000 20, 1220 60" fill="none" stroke="#fff" stroke-width="14" pathLength="1"/></mask></defs><path d="M10 80 C 220 20, 420 100, 640 50 S 1000 20, 1220 60" fill="none" stroke="#F6F4EF" stroke-width="6" stroke-dasharray="20 14" stroke-linecap="round" mask="url(#masque-chemin)"/><path class="da-fleche" d="M1196 30 L1252 62 L1194 92" fill="none" stroke="#FCD40D" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <p class="da-citation rv">{T(p, "« À l'heure d'un certain fatalisme social, guerrier, climatique et numérique, un autre chemin est-il possible ? »", "“In a time of social, military, climate and digital fatalism, is another way possible?”")}</p>
    <p class="petit da-doux">{T(p, "Texte de Xän pour le collectif Mada Paint · Un autre chemin · Another way", "Text by Xän for the Mada Paint collective · Un autre chemin · Another way")} · <a href="{p.u('festival.html')}">{T(p, 'Lire le texte du thème', 'Read the theme')}</a></p>
  </div>
</section>

<section class="da-beton da-section" aria-labelledby="titre-prog">
  <div class="cadre">
    <h2 class="da-titre rv" id="titre-prog">{T(p, 'Pendant 11 jours', 'For 11 days')}</h2>
    <div class="da-tuiles">
      <a class="da-tuile da-orange rv" href="{p.u('programme.html')}"><span>{T(p, 'Dans les quartiers', 'In the neighbourhoods')}</span><b>{T(p, 'Fresques en direct', 'Live murals')}</b></a>
      <a class="da-tuile da-jaune-fond rv" href="{p.u('visites.html')}"><span>{T(p, 'Pour tous les âges', 'For all ages')}</span><b>{T(p, 'Ateliers', 'Workshops')}</b></a>
      <a class="da-tuile da-turquoise rv" href="{p.u('programme.html')}"><span>{T(p, 'Avec DJ', 'With DJs')}</span><b>{T(p, 'Soirées', 'Parties')}</b></a>
      <a class="da-tuile da-magenta rv" href="{p.u('programme.html')}"><span>{T(p, 'Pour finir en beauté', 'The grand finale')}</span><b>Block party</b></a>
    </div>
  </div>
</section>

<section class="da-beton da-section" aria-labelledby="titre-aftermovie">
  <div class="cadre">
    <div class="entete-section">
      <h2 class="da-titre rv" id="titre-aftermovie">{T(p, "L'after movie", "The after movie")}</h2>
      <p class="da-doux">{T(p, "ARTMADA #2, du 1er au 11 février 2026 : les fresques, la jam et la block party à Fort-de-France.", "ARTMADA #2, 1–11 February 2026: the murals, the jam and the block party in Fort-de-France.")}</p>
    </div>
    <div class="video da-video rv" data-video="{AFTERMOVIE_EMBED}">
      <button type="button" class="video-lien video-facade" data-titre="{T(p, "After movie d'ARTMADA #2", "ARTMADA #2 after movie")}">
        <img src="{a('img/f/a2-curtis.jpg')}" alt="" width="1600" height="900"><span class="lecture" aria-hidden="true"></span>
        <span class="surtitre">{T(p, "Vidéo : JoBlackProd", "Video: JoBlackProd")}</span><b>{T(p, "Lancer l'after movie · ARTMADA #2", "Play the after movie · ARTMADA #2")}</b>
      </button>
    </div>
    <p class="petit da-doux" style="margin-top:10px">{T(p, "La vidéo se charge depuis YouTube quand tu cliques.", "The video loads from YouTube when you click.")} <a href="{AFTERMOVIE_URL}" rel="noopener">{T(p, "La voir sur YouTube", "Watch on YouTube")}</a> · <a href="{p.u('temps-forts-2026.html')}">{T(p, "Temps forts 2026", "2026 highlights")}</a> · <a href="{p.u('temps-forts-2024.html')}">{T(p, "Temps forts 2024", "2024 highlights")}</a></p>
  </div>
</section>

<section class="da-beton da-section" aria-labelledby="titre-murs">
  <div class="cadre">
    <div class="entete-section">
      <h2 class="da-titre rv" id="titre-murs">{T(p, 'Les murs restent', 'The walls stay')}</h2>
      <p class="da-doux">{T(p, "On peut aller voir les fresques toute l'année, à pied, gratuitement.", "You can see the murals all year round, on foot, for free.")} <a href="{p.u('carte.html')}">{T(p, 'Ouvrir la carte', 'Open the map')}</a></p>
    </div>
    <div class="da-affiches">{affiches}</div>
    <div class="boutons" style="margin-top:44px"><a class="bouton bouton-orange" href="{p.u('fresques/index.html')}">{T(p, 'Toutes les fresques', 'All the murals')}</a><a class="bouton bouton-clair" href="{p.u('carte.html')}">{T(p, 'La carte', 'The map')}</a></div>
  </div>
</section>

<section class="da-beton-sombre da-section">
  <div class="cadre">
    <div class="da-chiffres">
      <div class="rv"><b class="da-orange-texte">40</b><span>{T(p, 'fresques', 'murals')}</span></div>
      <div class="rv"><b class="da-jaune">2 650 m²</b><span>{T(p, 'de murs peints', 'of painted walls')}</span></div>
      <div class="rv"><b class="da-turquoise-texte">95</b><span>{T(p, 'bénévoles', 'volunteers')}</span></div>
    </div>
    <p class="petit da-doux" style="margin-top:18px">{T(p, 'Au total depuis la création du festival (éditions #1 en 2024 et #2 en 2026).', 'In total since the festival began (editions #1 in 2024 and #2 in 2026).')}</p>
  </div>
</section>

{bloc_visites(p)}

<section class="da-beton da-section" aria-labelledby="titre-boutique">
  <div class="cadre da-boutique-teaser">
    <div class="da-ts-boite">
      <img class="da-ts-splash" src="{a('img/da/splash-640.webp')}" alt="" width="640" height="703" loading="lazy" decoding="async">
      {tshirt_3d(p)}
    </div>
    <div class="rv" style="display:flex;flex-direction:column;gap:18px;align-items:flex-start">
      <span class="da-sticker">{T(p, 'Boutique', 'Shop')}</span>
      <h2 class="da-titre" id="titre-boutique">{T(p, 'Porte le festival', 'Wear the festival')}</h2>
      <p class="da-doux" style="font-size:19px;max-width:520px">{T(p, "Le t-shirt officiel à 30 € et la casquette à 20 €. À récupérer à l'Urban Studio, Village de la Poterie, Les Trois-Îlets. Chaque achat aide le festival à peindre de nouveaux murs.", "The official T-shirt (€30) and cap (€20). Pick them up at Urban Studio, Village de la Poterie, Les Trois-Îlets. Every purchase helps the festival paint new walls.")}</p>
      <a class="bouton bouton-orange" href="{p.u('boutique.html')}">{T(p, 'Voir la boutique', 'Visit the shop')}</a>
    </div>
  </div>
</section>

<section class="da-benevoles">
  <img src="{a('img/da/spray-cartouche.webp')}" alt="" width="620" height="622" loading="lazy" decoding="async">
  <div class="cadre" style="position:relative;display:flex;justify-content:space-between;align-items:center;gap:28px;flex-wrap:wrap">
    <h2 class="da-titre rv">{T(p, 'Le festival<br>se fait ensemble', 'We make it<br>together')}</h2>
    <div style="display:flex;flex-direction:column;gap:14px;max-width:420px">
      <p style="font-size:18px">{T(p, "75 bénévoles ont fait vivre ARTMADA #2. Conduire les artistes, accueillir le public, aider sur les murs : même quelques heures comptent.", "75 volunteers brought ARTMADA #2 to life. Driving artists, welcoming visitors, helping on the walls: even a few hours make a difference.")}</p>
      <a class="bouton bouton-nuit" href="{p.u('benevoles.html')}">{T(p, 'Je deviens bénévole', 'Become a volunteer')}</a>
    </div>
  </div>
</section>

<section class="da-beton-sombre da-partenaires" aria-label="{T(p, 'Nos partenaires', 'Our partners')}">
  <p class="cadre surtitre da-jaune">{T(p, "Sans eux, le festival n'aurait pas pu exister", "Without them, the festival could not exist")} · <a href="{p.u('partenaires.html')}">{T(p, 'Devenir partenaire', 'Become a partner')}</a></p>
  <div class="da-defile-boite"><div class="da-defile">{noms_part}{noms_part.replace('<span>', '<span aria-hidden="true">')}</div></div>
</section>
'''
    ecrire(p, document(p, "", T(p, "ARTMADA Street Festival, le festival de street art de Fort-de-France (Martinique). Édition #3 « An Lot Chimen » du 25 janvier au 4 février 2027 : fresques, ateliers, visites, block party.", "ARTMADA Street Festival, the street art festival of Fort-de-France, Martinique. Edition #3 “An Lot Chimen”, 25 January to 4 February 2027: murals, workshops, tours, block party."), corps, actif="index.html", image="img/hd/a2-doudou.jpg",
                       ld=[{"@type": "WebSite", "@id": SITE_URL + "#site", "name": "ARTMADA Street Festival", "url": SITE_URL, "inLanguage": ["fr", "en"], "publisher": {"@id": ORGA["@id"]}},
                           festival_ld(p.lang), aftermovie_ld(p.lang)]))

# ============================================================ BOUTIQUE

URBAN_STUDIO = "Urban Studio, Village de la Poterie, Les Trois-Îlets"

def boutique(lang):
    p = P(lang, "boutique.html")
    a = p.a
    sujet = T(p, "Réservation t-shirt ARTMADA", "ARTMADA T-shirt reservation")
    corps_mail = T(p, "Bonjour, je voudrais réserver le t-shirt officiel ARTMADA (30 €) en taille M. Je viendrai le chercher à l'Urban Studio.",
                   "Hello, I would like to reserve the official ARTMADA T-shirt (€30) in size M. I will pick it up at Urban Studio.")
    from urllib.parse import quote
    mailto = f"mailto:{MAIL}?subject={quote(sujet)}&body={quote(corps_mail)}"
    tailles = "".join(f'<button type="button" class="ts-taille" data-taille="{n}" aria-pressed="{"true" if n == "M" else "false"}">{n}</button>' for n in ["S", "M", "L", "XL", "XXL"])
    corps = f'''
<div class="da-beton">
<div class="da-coulure-haut" aria-hidden="true"><img src="{a('img/da/coulure.webp')}" srcset="{a('img/da/coulure-900.webp')} 900w, {a('img/da/coulure.webp')} 1800w" sizes="100vw" alt="" width="1800" height="539" decoding="async"></div>
<section class="cadre da-boutique-tete">
  <nav class="fil" aria-label="{T(p, 'Fil d’Ariane', 'Breadcrumb')}"><a href="{p.u('index.html')}">{T(p, 'Accueil', 'Home')}</a> / {T(p, 'Boutique', 'Shop')}</nav>
  <h1 class="da-geant">{T(p, 'La boutique', 'The shop')}</h1>
  <p class="da-doux" style="font-size:20px;max-width:640px">{T(p, "Le merch officiel d'ARTMADA Street Festival. Chaque achat aide le festival à peindre de nouveaux murs.", "Official ARTMADA Street Festival merch. Every purchase helps the festival paint new walls.")}</p>
</section>

<section class="cadre da-produit" aria-labelledby="titre-tshirt" data-produit data-mail="{MAIL}" data-sujet="{e(sujet)}" data-corps="{e(corps_mail)}">
  <div class="da-produit-visuel">
    <span class="da-edition da-produit-badge">{T(p, 'Édition officielle', 'Official edition')}</span>
    {tshirt_3d(p, grand=True, controles=True)}
  </div>
  <div class="da-produit-infos">
    <span class="surtitre da-jaune">{T(p, 'T-shirt', 'T-shirt')}</span>
    <h2 class="da-titre" id="titre-tshirt">{T(p, 'T-shirt officiel ARTMADA', 'Official ARTMADA T-shirt')}</h2>
    <p class="da-doux" style="font-size:17px">{T(p, "T-shirt blanc. Au recto, le logo ARTMADA et la main qui tient la bombe. Au dos, le tag « Lyannaj Karayib ».", "White T-shirt. On the front, the ARTMADA logo and the hand holding the spray can. On the back, the “Lyannaj Karayib” tag.")}</p>
    <p class="da-prix">30 €</p>
    <div style="display:flex;flex-direction:column;gap:10px">
      <p style="font-weight:700">{T(p, 'Taille', 'Size')} : <span data-taille-choisie>M</span> <span class="da-doux" style="font-weight:400">· {T(p, 'toutes les tailles du S au XXL sont disponibles', 'all sizes from S to XXL are available')}</span></p>
      <div class="ts-tailles" role="group" aria-label="{T(p, 'Choisir la taille', 'Choose a size')}">{tailles}</div>
    </div>
    <a class="bouton bouton-orange da-reserver" href="{e(mailto)}" data-reserver>{T(p, 'Je le réserve', 'Reserve it')}</a>
    <p class="da-lieu-retrait"><svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path d="M10 1.5c-3.3 0-6 2.6-6 5.9 0 4.4 6 11.1 6 11.1s6-6.7 6-11.1c0-3.3-2.7-5.9-6-5.9z" fill="none" stroke="#FCD40D" stroke-width="2"/><circle cx="10" cy="7.5" r="2.2" fill="#FCD40D"/></svg><span>{T(p, f"À récupérer à l'{URBAN_STUDIO}.", f"Pick it up at {URBAN_STUDIO}.")}</span></p>
  </div>
</section>

<section class="cadre da-section" aria-labelledby="titre-tout">
  <h2 class="da-titre rv" id="titre-tout" style="margin-bottom:28px">{T(p, 'Toute la boutique', 'Everything')}</h2>
  <div class="da-cartes">
    <a class="da-carte rv" href="#titre-tshirt">
      <span class="da-carte-photo"><img src="{a('img/da/tshirt-face.webp')}" alt="{T(p, 'T-shirt officiel ARTMADA', 'Official ARTMADA T-shirt')}" width="785" height="900" loading="lazy" decoding="async"></span>
      <span class="da-carte-bas"><b>{T(p, 'T-shirt officiel', 'Official T-shirt')}</b><span class="da-jaune">30 €</span></span>
    </a>
    <div class="da-carte rv">
      <span class="da-carte-photo da-carte-attente"><img src="{a('img/da/spray-cartouche.webp')}" alt="" width="620" height="622" loading="lazy" decoding="async"><span>{T(p, 'Casquette', 'Cap')}<small>{T(p, 'photo à venir', 'photo coming soon')}</small></span></span>
      <span class="da-carte-bas"><b>{T(p, 'Casquette ARTMADA', 'ARTMADA cap')}</b><span class="da-jaune">20 €</span></span>
    </div>
  </div>
  <p class="da-doux" style="margin-top:28px">{T(p, f"Pour la casquette ou une autre question : écris-nous à", f"For the cap or any other question, email us at")} <a href="mailto:{MAIL}">{MAIL}</a>.</p>
</section>
</div>
'''
    produits = [
        {"@type": "Product", "name": t(lang, "T-shirt officiel ARTMADA Street Festival", "Official ARTMADA Street Festival T-shirt"),
         "image": [SITE_URL + "assets/img/da/tshirt-face.webp", SITE_URL + "assets/img/da/tshirt-dos.webp"],
         "description": t(lang, "T-shirt blanc, logo ARTMADA et main tenant une bombe au recto, tag Lyannaj Karayib au dos. Tailles S à XXL.", "White T-shirt, ARTMADA logo and hand holding a spray can on the front, Lyannaj Karayib tag on the back. Sizes S to XXL."),
         "brand": {"@type": "Brand", "name": "ARTMADA Street Festival"},
         "offers": {"@type": "Offer", "price": "30", "priceCurrency": "EUR", "availability": "https://schema.org/InStoreOnly", "url": SITE_URL + ("" if lang == "fr" else "en/") + "boutique.html"}},
        {"@type": "Product", "name": t(lang, "Casquette ARTMADA Street Festival", "ARTMADA Street Festival cap"),
         "brand": {"@type": "Brand", "name": "ARTMADA Street Festival"},
         "offers": {"@type": "Offer", "price": "20", "priceCurrency": "EUR", "availability": "https://schema.org/InStoreOnly", "url": SITE_URL + ("" if lang == "fr" else "en/") + "boutique.html"}},
    ]
    ecrire(p, document(p, T(p, "Boutique : t-shirt et casquette", "Shop: T-shirt and cap"),
                       T(p, "Le t-shirt officiel ARTMADA Street Festival (30 €, du S au XXL) et la casquette (20 €), à récupérer à l'Urban Studio aux Trois-Îlets, Martinique.", "The official ARTMADA Street Festival T-shirt (€30, S to XXL) and cap (€20), to pick up at Urban Studio in Les Trois-Îlets, Martinique."),
                       corps, actif="boutique.html", image="img/da/tshirt-face.webp",
                       ld=produits + [fil_ld(p, [(None, T(p, "Boutique", "Shop"))])]))

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
        <a class="bouton bouton-orange bouton-petit" href="{BIZOUK}" rel="noopener">{T(p, 'Réserver', 'Book')}</a>
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
      <a class="bouton bouton-orange" href="{BIZOUK}" rel="noopener">{T(p, 'Réserver sur Bizouk', 'Book on Bizouk')}</a>
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
      <a class="bouton bouton-orange" style="align-self:flex-start" href="mailto:{MAIL}?subject={T(p, 'Partenariat%20ARTMADA%20%233', 'ARTMADA%20%233%20partnership')}">{T(p, 'Nous écrire', 'Get in touch')}</a>
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
<ul><li>Numéro RNA : W9M1010969</li><li>SIREN : 897 410 858 · SIRET du siège : 897 410 858 00012</li><li>Siège : Résidence Aigue Marine, bâtiment 2, appartement 29, rue de la Dorsale, 97200 Fort-de-France, Martinique</li><li>Contact : {MAIL}</li><li>Directrice de la publication : Jennifer Monlouis Bonnaire, présidente de l'association</li></ul>
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
<ul><li>RNA number: W9M1010969</li><li>SIREN: 897 410 858 · SIRET: 897 410 858 00012</li><li>Registered office: Résidence Aigue Marine, bâtiment 2, appartement 29, rue de la Dorsale, 97200 Fort-de-France, Martinique</li><li>Contact: {MAIL}</li><li>Publication director: Jennifer Monlouis Bonnaire, president of the association</li></ul>
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
<ul><li>Pas de compte, pas de formulaire, pas de cookie, pas de publicité, pas de mesure d'audience.</li><li>Les polices d'écriture et les images sont chargées depuis le site lui-même.</li><li>Sur la page « Carte », le fond de carte vient d'OpenStreetMap et l'outil de carte de cdnjs (Cloudflare) : ces services reçoivent ton adresse IP pour afficher la carte. Les liens « Y aller à pied » t'emmènent sur Google Maps, et le parcours guidé sur Creapolis ; ces services ont leurs propres règles.</li><li>L'hébergeur (GitHub) enregistre l'adresse IP des visiteurs dans ses journaux techniques, pour la sécurité du service. L'association n'y a pas accès.</li><li>Les liens vers Instagram, YouTube ou Bizouk t'emmènent sur ces services, qui ont leurs propres règles.</li><li>L'after movie de la page d'accueil est hébergé sur YouTube (mode « confidentialité renforcée ») : rien n'est chargé depuis YouTube tant que tu ne cliques pas sur la vidéo.</li></ul>
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
<ul><li>No account, no form, no cookies, no advertising, no audience tracking.</li><li>Fonts and images are served from the site itself.</li><li>On the “Map” page, map tiles come from OpenStreetMap and the map library from cdnjs (Cloudflare): these services receive your IP address to display the map. “Walk there” links take you to Google Maps, and the guided tour to Creapolis; these services have their own rules.</li><li>The host (GitHub) records visitors' IP addresses in its technical logs for security. The association has no access to them.</li><li>Links to Instagram, YouTube or Bizouk take you to those services, which have their own rules.</li><li>The after movie on the home page is hosted on YouTube (privacy-enhanced mode): nothing loads from YouTube until you click the video.</li></ul>
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
    festival(lang)
    programme(lang)
    visites(lang)
    benevoles(lang)
    partenaires(lang)
    infos(lang)
    legales(lang)
    import pages_donnees as PD
    PD.toutes(lang)
