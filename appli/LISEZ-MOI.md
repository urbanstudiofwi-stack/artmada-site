# Appli ARTMADA — version web installable (V1)

En ligne : https://artmadastreetfestival.com/appli/ (mode test : ajouter `?test` à l'adresse pour tamponner sans être devant le mur).

- **Données** : les mêmes que le site (`data/fresques.json`, `data/artistes.json`). Corriger une fresque là → le site ET l'appli changent.
- **Écrans** : accueil (compte à rebours #3, fresque du jour, atelier, visite), carte (filtres, recherche, liste, « me localiser »), fiche d'une fresque (y aller à pied, artiste, histoire FR/EN, tamponner), 4 parcours à pied, passeport à tampons (gardé sur le téléphone).
- **Fabrication** : `build.py` appelle `appli/construire.py`, qui copie `appli/web/` dans `dist/appli/`, écrit `donnees.json` et réduit les photos (960 px + vignettes 160 px).
- **Hors ligne** : `sw.js` garde l'appli, les photos et les fonds de carte déjà vus.
- **Fond de carte** : CARTO « dark matter » (données OpenStreetMap), gratuit avec mention.
- **Plus tard** : comptes, espace bénévoles, réservation + paiement Stripe, puis publication App Store / Google Play (même code, emballé avec Capacitor).
