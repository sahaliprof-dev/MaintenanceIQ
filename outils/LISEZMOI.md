# Générateur des pages MaintenanceIQ

- `fiches_data.py` : contenu des fiches terrain (une entrée par fiche).
- `gen.py` : génère les pages territoires, fiches, index des fiches, calculateur, glossaire, à propos, `sitemap.xml` et `llms.txt`.

Ajouter une fiche : ajouter une entrée dans `FICHES` (slug, machine, date, h1, title ≤ 50 car., desc ≤ 155 car., intro, signes, causes, faire, secu, faq, related), puis depuis la racine du dépôt :

    python3 outils/gen.py .

La page d'accueil (index.html) n'est pas générée : y ajouter le lien de la nouvelle fiche dans la section « Fiches terrain, outils et territoires ».
