# Site ARTMADA Street Festival — code source

- `data/*.json` : fresques, artistes, programme, presse, archives.
- `pages_contenu.py` : pages fixes (accueil, festival, programme…). `pages_donnees.py` : pages fabriquées à partir des données.
- `build.py` : fabrique le site dans `dist/` (FR à la racine, EN dans `/en/`), avec titres, fiches schema.org, WebP, sitemap.
- Modifier un fichier sur cette branche **source** → GitHub reconstruit et met en ligne tout seul (`.github/workflows/publier.yml`).
- La branche **main** contient le site publié (GitHub Pages, artmadastreetfestival.com). Ne pas la modifier à la main.
