#!/usr/bin/env python3
"""Fabrique l'appli ARTMADA (version web installable) dans dist/appli/.

Les données viennent des MÊMES fichiers que le site (data/fresques.json, data/artistes.json) :
on corrige une fresque une fois, le site ET l'appli changent.

Appelé à la fin de build.py. Peut aussi se lancer seul : python3 appli/construire.py
"""
import json, math, shutil
from pathlib import Path
from urllib.parse import quote

ICI = Path(__file__).parent
RACINE = ICI.parent
DATA = RACINE / "data"
ASSETS = RACINE / "assets"

ANNEE = {1: "2024", 2: "2026"}

# Mêmes parcours que la page Carte du site (pages_donnees.py : PARCOURS / ETAPES_PARCOURS).
PARCOURS = [
    ("centre", "Pointe Simon et centre-ville", "Pointe Simon & city centre",
     "Du front de mer à la rue Moreau de Jonnès : le Mur de la Jam, les bulles de Tempo Nok, Sitou, Roxane Shade, Jaddict…",
     "From the seafront to rue Moreau de Jonnès: the Jam Wall, Tempo Nok's bubbles, Sitou, Roxane Shade, Jaddict…",
     list(range(1, 11))),
    ("tom", "Rue Victor Sévère et Terres-Sainville", "Rue Victor Sévère & Terres-Sainville",
     "Le cœur du festival 2026 autour du TOM : Yelow, Curtis Hylton, Doudou Style, Oshea, Mounlan, puis Les Fortes de France de Carole B.",
     "The heart of the 2026 festival around the TOM: Yelow, Curtis Hylton, Doudou Style, Oshea, Mounlan, then Carole B.'s Les Fortes de France.",
     list(range(11, 18))),
    ("est", "Clarac, Sainte-Thérèse et Canal Alaric", "Clarac, Sainte-Thérèse & Canal Alaric",
     "De la cité Clarac au canal : l'ancien cinéma Olympia, Difé Pri d'Oshea, le lettrage de Wuna, Rayza, Al Pacman…",
     "From Cité Clarac to the canal: the old Olympia cinema, Oshea's Difé Pri, Wuna's lettering, Rayza, Al Pacman…",
     list(range(18, 29))),
    ("2024", "Les fresques de 2024", "The 2024 murals",
     "De Pointe Simon à la cité Dillon : Sitou, Les Fortes de France de Carole B., l'ancien Olympia, Difé Pri d'Oshea et Transmission de Magiic.",
     "From Pointe Simon to Cité Dillon: Sitou, Carole B.'s Les Fortes de France, the old Olympia, Oshea's Difé Pri and Magiic's Transmission.",
     [3, 17, 20, 23, 29]),
]

# Missions bénévoles : mêmes que la page Bénévoles du site (pages_contenu.py, benevoles()).
MISSIONS = [
    ("Accueil", "Welcome", "Accueillir le public, orienter, répondre aux questions sur les murs.", "Welcome visitors, give directions, answer questions about the walls."),
    ("Logistique", "Logistics", "Préparer le matériel, aider sur les murs, ranger en fin de journée.", "Prepare equipment, help on the walls, tidy up at the end of the day."),
    ("Chauffeur", "Driver", "Conduire les artistes entre leur logement, les murs et les soirées.", "Drive the artists between their lodging, the walls and the events."),
    ("Photo & vidéo", "Photo & video", "Garder la trace du festival, jour après jour.", "Capture the festival, day after day."),
    ("Soirées", "Events", "Bar, entrée, installation pendant les soirées et la block party.", "Bar, entrance and set-up during the parties and the block party."),
    ("Ateliers", "Workshops", "Encadrer les participants aux côtés des artistes.", "Support participants alongside the artists."),
]


def texte_theme():
    """Texte « An Lot Chimen » de Xän, repris de la page Festival du site (pages_contenu.py)."""
    import re
    src = (RACINE / "pages_contenu.py").read_text("utf-8")
    q = "'" * 3
    blocs = re.findall(r"texte = " + q + r"(.*?)" + q, src, flags=re.S)

    def nettoie(h):
        paras = re.findall(r"<p>(.*?)</p>", h, flags=re.S)
        return [re.sub(r"<[^>]+>", "", x).strip() for x in paras]
    if len(blocs) >= 2:
        return nettoie(blocs[0]), nettoie(blocs[1])
    return [], []


def km_entre(a, b):
    la1, lo1 = a; la2, lo2 = b
    r = 6371.0
    p1, p2 = math.radians(la1), math.radians(la2)
    dp, dl = p2 - p1, math.radians(lo2 - lo1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def gps(f):
    if not f.get("gps"):
        return None
    la, lo = f["gps"].replace(" ", "").split(",")
    return [round(float(la), 6), round(float(lo), 6)]


def images(fresques, sortie):
    """Photo 960 px + vignette carrée 160 px pour chaque fresque (WebP, légères pour le téléphone)."""
    from PIL import Image, ImageOps
    (sortie / "img").mkdir(parents=True, exist_ok=True)
    for f in fresques:
        if not f.get("photo"):
            continue
        src = ASSETS / f["photo"]
        if not src.exists():
            print("  ! photo absente :", src)
            f["photo"] = ""
            continue
        im = Image.open(src).convert("RGB")
        grand = im.copy(); grand.thumbnail((960, 960))
        grand.save(sortie / "img" / f"{f['slug']}.webp", "WEBP", quality=74, method=6)
        petit = ImageOps.fit(im, (160, 160), centering=(0.5, 0.45))
        petit.save(sortie / "img" / f"{f['slug']}-v.webp", "WEBP", quality=70, method=6)


def construire(dist):
    dist = Path(dist)
    sortie = dist / "appli"
    if sortie.exists():
        shutil.rmtree(sortie)
    shutil.copytree(ICI / "web", sortie)

    artistes = json.loads((DATA / "artistes.json").read_text("utf-8"))
    fresques = json.loads((DATA / "fresques.json").read_text("utf-8"))
    A = {a["slug"]: a for a in artistes}

    images(fresques, sortie)

    def noms(f):
        n = [A[s]["nom"] if s in A else s for s in f.get("artistes", [])] + f.get("avec", [])
        return " & ".join(n)

    sortie_f = []
    for f in fresques:
        g = gps(f)
        dest = f"{g[0]},{g[1]}" if g else quote(f"{f.get('lieu','')}, {f.get('ville', 'Fort-de-France')}, Martinique")
        sortie_f.append({
            "slug": f["slug"],
            "nom": f.get("signature") or noms(f),
            "artistes": [s for s in f.get("artistes", []) if s in A] if not f.get("collectif") else [],
            "collectif": bool(f.get("collectif")),
            "edition": f["edition"],
            "annee": ANNEE.get(f["edition"], ""),
            "titre": f.get("titre", ""),
            "lieu": f.get("lieu", ""),
            "secteur": f.get("secteur", ""),
            "ville": f.get("ville", "Fort-de-France"),
            "gps": g,
            "photo": bool(f.get("photo")),
            "credit": f.get("credit_photo") or ("Shaman" if f["edition"] == 2 else ""),
            "texte": f.get("description", ""),
            "texte_en": f.get("description_en", ""),
            "surface": f.get("surface") or "",
            "disparue": bool(f.get("disparue")),
            "etape": f.get("etape"),
            "y_aller": "https://www.google.com/maps/dir/?api=1&travelmode=walking&destination=" + dest,
        })

    par_etape = {f["etape"]: f for f in sortie_f if f.get("etape") and f["gps"]}
    sortie_p = []
    for cle, titre, titre_en, texte, texte_en, nums in PARCOURS:
        etapes = [par_etape[n] for n in nums if n in par_etape]
        if len(etapes) < 2:
            continue
        km = sum(km_entre(a["gps"], b["gps"]) for a, b in zip(etapes, etapes[1:]))
        pts = [f"{f['gps'][0]},{f['gps'][1]}" for f in etapes]
        url = ("https://www.google.com/maps/dir/?api=1&travelmode=walking&origin=" + pts[0]
               + "&destination=" + pts[-1])
        if len(pts) > 2:
            url += "&waypoints=" + quote("|".join(pts[1:-1]), safe=",")
        sortie_p.append({
            "cle": cle, "titre": titre, "titre_en": titre_en, "texte": texte, "texte_en": texte_en,
            "etapes": [f["slug"] for f in etapes],
            "km": round(km, 1),
            "minutes": max(5, round(km / 4 * 60 / 5) * 5),
            "url": url,
            "editions": sorted({f["edition"] for f in etapes}),
        })

    sortie_a = {a["slug"]: {"nom": a["nom"], "origine": a.get("origine", ""), "origine_en": a.get("origine_en", ""),
                            "bio": a.get("bio", ""), "bio_en": a.get("bio_en", ""),
                            "instagram": a.get("instagram", ""), "collectif": a.get("collectif", "")}
                for a in artistes}

    donnees = {
        "festival": {"edition": 3, "theme": "An Lot Chimen", "theme_fr": "Un autre chemin",
                     "debut": "2027-01-25", "fin": "2027-02-04", "ville": "Fort-de-France"},
        "atelier": {"titre": "Atelier street art", "titre_en": "Street art workshop",
                    "quand": "Tous les samedis, 10h → 12h", "quand_en": "Every Saturday, 10am → 12pm",
                    "ou": "Urban Studio, Village de la Poterie, Trois-Îlets", "prix": "49,90 €", "prix_en": "€49.90",
                    "places": 8, "lien": "https://www.bizouk.com/events/details/atelier-graffiti-a-lurban-studio-avec-do/131478"},
        "fresques": sortie_f, "artistes": sortie_a, "parcours": sortie_p,
        "programme_exemple": json.loads((DATA / "programme.json").read_text("utf-8")),
        "missions": [{"titre": a, "titre_en": b, "texte": c, "texte_en": d} for a, b, c, d in MISSIONS],
        "contact": "contact@artmadastreetfestival.com",
    }
    fr, en = texte_theme()
    donnees["festival"].update({"texte": fr, "texte_en": en,
                                "quartiers": "Langellier, Mongérald, Tocade et le centre-ville de Fort-de-France",
                                "quartiers_en": "Langellier, Mongérald, Tocade and Fort-de-France city centre"})
    (sortie / "donnees.json").write_text(json.dumps(donnees, ensure_ascii=False, separators=(",", ":")), "utf-8")

    # Logo, icônes, polices, texture : copiés depuis les fichiers du site (une seule source).
    (sortie / "media").mkdir(exist_ok=True)
    for nom in ("icon-192.png", "icon-512.png", "apple-touch-icon.png"):
        shutil.copy(ASSETS / nom, sortie / "media" / nom)
    from PIL import Image
    logo = Image.open(ASSETS / "img" / "logo-blanc.png"); logo.thumbnail((560, 560))
    logo.save(sortie / "media" / "logo.webp", "WEBP", quality=90, method=6)
    shutil.copy(ASSETS / "img" / "da" / "beton.webp", sortie / "media" / "beton.webp")
    shutil.copytree(ASSETS / "fonts", sortie / "fonts")

    # Liste des fichiers à garder hors ligne (pour se promener sans réseau).
    fichiers = sorted(str(p.relative_to(sortie)).replace("\\", "/") for p in sortie.rglob("*")
                      if p.is_file() and p.name != "sw.js")
    import hashlib
    empreinte = hashlib.md5()
    for nom in fichiers:
        empreinte.update(nom.encode()); empreinte.update((sortie / nom).read_bytes())
    version = empreinte.hexdigest()[:10]
    sw = (sortie / "sw.js").read_text("utf-8")
    sw = sw.replace("__VERSION__", version).replace("__FICHIERS__", json.dumps(fichiers))
    (sortie / "sw.js").write_text(sw, "utf-8")
    print(f"Appli : {len(sortie_f)} fresques, {len(sortie_p)} parcours, {len(fichiers)} fichiers → {sortie}")


if __name__ == "__main__":
    construire(RACINE / "dist")
