#!/usr/bin/env python3
"""Fabrique la page HTML des QR codes de l'appli (à imprimer en PDF) :
- page 1 : affiche « Scanne, l'appli ARTMADA s'ouvre » (pour une présentation, un stand, la galerie) ;
- pages suivantes : une plaque par fresque (4 par A4), le QR ouvre directement la fiche de la fresque.

python3 appli/outils/plaques_qr.py SORTIE.html   (puis l'imprimer en PDF, A4, marges 0)
Il faut avoir lancé construire.py avant (il lit dist/appli/donnees.json et les photos réduites).
"""
import base64, html, io, json, sys
from pathlib import Path

import qrcode
import qrcode.image.svg

RACINE = Path(__file__).resolve().parents[2]
APPLI = RACINE / "dist" / "appli"
URL = "https://artmadastreetfestival.com/appli/"


def qr_svg(texte):
    img = qrcode.make(texte, image_factory=qrcode.image.svg.SvgPathImage, border=0,
                      error_correction=qrcode.constants.ERROR_CORRECT_M)
    buf = io.BytesIO(); img.save(buf)
    svg = buf.getvalue().decode()
    return svg[svg.index("<svg"):].replace("<svg ", '<svg class="qr" ', 1)


def data_uri(chemin, mime):
    return f"data:{mime};base64," + base64.b64encode(Path(chemin).read_bytes()).decode()


def main(sortie):
    d = json.loads((APPLI / "donnees.json").read_text("utf-8"))
    e = html.escape
    fonts = RACINE / "assets" / "fonts"
    logo = data_uri(APPLI / "media" / "logo.webp", "image/webp")
    fresques = [f for f in d["fresques"] if f["gps"] and not f["disparue"]]
    fresques.sort(key=lambda f: (f["etape"] or 99, f["slug"]))

    affiche_photo = data_uri(APPLI / "img" / "xan-pointe-simon.webp", "image/webp")
    pages = [f'''<section class="page affiche">
  <div class="photo" style="background-image:url({affiche_photo})"></div>
  <div class="bas">
    <img class="logo" src="{logo}" alt="ARTMADA">
    <h1>L'appli du street art<br>en Martinique</h1>
    <p class="sous">{len(d["fresques"])} fresques · {len(d["parcours"])} parcours à pied · ton passeport de fresques</p>
    <div class="qr-zone">{qr_svg(URL)}<div><b>Scanne avec l'appareil photo</b><span>L'appli s'ouvre tout de suite, sans téléchargement.</span><span class="en">Scan with your camera: the app opens right away.</span><span class="url">artmadastreetfestival.com/appli</span></div></div>
  </div>
</section>''']

    plaques = []
    for f in fresques:
        ph = APPLI / "img" / f"{f['slug']}-v.webp"
        img = f'<img src="{data_uri(ph, "image/webp")}" alt="">' if f["photo"] and ph.exists() else ""
        titre = f'<span class="titre">« {e(f["titre"])} »</span>' if f["titre"] else ""
        plaques.append(f'''<article class="plaque">
  <div class="haut">{img}<div><span class="ed">ARTMADA #{f["edition"]} · {f["annee"]}</span><b class="nom">{e(f["nom"])}</b>{titre}</div></div>
  <div class="milieu">{qr_svg(URL + "#f/" + f["slug"])}<div class="mode"><b>Scanne la fresque</b><span>Son histoire, l'artiste, et ton tampon de passeport.</span><span class="en">Scan for the story of this mural.</span></div></div>
  <div class="pied"><img src="{logo}" alt="ARTMADA"><span>{e(f["lieu"])}</span></div>
</article>''')
    for i in range(0, len(plaques), 4):
        pages.append('<section class="page grille">' + "".join(plaques[i:i + 4]) + "</section>")

    doc = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>QR codes ARTMADA</title><style>
@font-face{{font-family:Anton;src:url({data_uri(fonts / "anton-latin-400-normal.woff2", "font/woff2")})}}
@font-face{{font-family:"DM Sans";src:url({data_uri(fonts / "dm-sans-latin-400-normal.woff2", "font/woff2")});font-weight:400}}
@font-face{{font-family:"DM Sans";src:url({data_uri(fonts / "dm-sans-latin-700-normal.woff2", "font/woff2")});font-weight:700}}
@page{{size:A4;margin:0}}
*{{box-sizing:border-box}} body{{margin:0;font-family:"DM Sans",sans-serif;color:#F6F4EF;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{width:210mm;height:297mm;overflow:hidden;page-break-after:always;background:#232427;position:relative}}
.qr{{background:#fff;padding:3mm;border-radius:3mm;display:block}} .qr path{{fill:#1A1208}}
.affiche .photo{{position:absolute;inset:0 0 auto 0;height:150mm;background-size:cover;background-position:center 40%}}
.affiche .photo::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(35,36,39,0) 55%,#232427 100%)}}
.affiche .bas{{position:absolute;left:16mm;right:16mm;top:128mm;display:flex;flex-direction:column;gap:5mm}}
.affiche .logo{{width:62mm}}
.affiche h1{{font-family:Anton,sans-serif;font-weight:400;text-transform:uppercase;font-size:21mm;line-height:.95;margin:0}}
.affiche .sous{{margin:0;font-size:5mm;color:#B9BCC2;font-weight:700}}
.qr-zone{{display:flex;gap:8mm;align-items:center;margin-top:4mm}}
.qr-zone .qr{{width:62mm;height:62mm}}
.qr-zone div{{display:flex;flex-direction:column;gap:2.5mm;font-size:4.6mm}}
.qr-zone b{{font-size:7mm;color:#EB782F}} .qr-zone .en{{color:#B9BCC2;font-style:italic}} .qr-zone .url{{font-weight:700;color:#FCD40D}}
.grille{{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:0;padding:0}}
.plaque{{border:0.3mm dashed #55585F;padding:9mm 8mm;display:flex;flex-direction:column;gap:6mm;justify-content:space-between}}
.plaque .haut{{display:flex;gap:4mm;align-items:center}}
.plaque .haut img{{width:24mm;height:24mm;border-radius:50%;object-fit:cover;border:1mm solid #EB782F}}
.plaque .haut div{{display:flex;flex-direction:column;gap:1mm;min-width:0}}
.plaque .ed{{font-size:3mm;font-weight:700;letter-spacing:.12em;color:#EB782F}}
.plaque .nom{{font-family:Anton,sans-serif;font-weight:400;font-size:8.5mm;line-height:1;text-transform:uppercase}}
.plaque .titre{{font-size:3.6mm;font-weight:700}}
.plaque .milieu{{display:flex;gap:5mm;align-items:center}}
.plaque .milieu .qr{{width:44mm;height:44mm;flex-shrink:0}}
.plaque .mode{{display:flex;flex-direction:column;gap:1.5mm;font-size:3.4mm}}
.plaque .mode b{{font-size:4.6mm;color:#FCD40D}} .plaque .en{{color:#B9BCC2;font-style:italic}}
.plaque .pied{{display:flex;justify-content:space-between;align-items:center;gap:4mm;font-size:3mm;color:#B9BCC2}}
.plaque .pied img{{width:26mm}}
</style></head><body>{"".join(pages)}</body></html>'''
    Path(sortie).write_text(doc, "utf-8")
    print(f"{len(fresques)} plaques + 1 affiche → {sortie}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "qr-codes-artmada.html")
