# Appli ARTMADA — version web installable (V1)

En ligne : https://artmadastreetfestival.com/appli/ (mode test : ajouter `?test` à l'adresse pour tamponner sans être devant le mur).

- **Données** : les mêmes que le site (`data/fresques.json`, `data/artistes.json`). Corriger une fresque là → le site ET l'appli changent.
- **Écrans** : accueil (compte à rebours #3, fresque du jour, atelier, visite, aide à l'installation), carte (filtres, recherche, liste, « me localiser »), fiche d'une fresque (y aller à pied, artiste, histoire FR/EN, tamponner), 4 parcours à pied, passeport à tampons (gardé sur le téléphone), Festival #3 (thème An Lot Chimen, infos, chiffres #2), aperçu du mode direct (`#direct`, avec le programme 2026 en exemple), inscription bénévole (`#benevoles`, ouvre un mail prérempli vers contact@).
- **Langues** : français / anglais (bouton FR/EN sur l'accueil et dans le passeport ; `?lang=en` force l'anglais).
- **QR codes** : `python3 appli/outils/plaques_qr.py sortie.html` → affiche + une plaque par fresque (le QR ouvre la fiche), à imprimer en PDF A4.
- **Fabrication** : `build.py` appelle `appli/construire.py`, qui copie `appli/web/` dans `dist/appli/`, écrit `donnees.json` et réduit les photos (960 px + vignettes 160 px).
- **Hors ligne** : `sw.js` garde l'appli et les photos (le fond de carte, lui, demande du réseau).
- **Fond de carte** : OpenStreetMap, passé en sombre par un filtre (`.leaflet-tile-pane` dans app.css). CARTO a été abandonné le 21/10/2026 : il demande désormais une clé payante (« API KEY REQUIRED »).
- **Plus tard** : comptes, espace bénévoles, réservation + paiement Stripe, puis publication App Store / Google Play (même code, emballé avec Capacitor).
