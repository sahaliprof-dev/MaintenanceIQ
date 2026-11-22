# Générateur du site MaintenanceIQ (FR + EN)

Fichiers :
- `fiches_data.py` : fiches terrain FR d'origine (machines industrielles).
- `contenu_fr_plus.py` : niveaux (Simple / Intermédiaire / Avancé) et domaines des fiches, nouvelles fiches FR (bâtiment, avancé) et méthodes de maintenance FR (`METHODES`).
- `contenu_en.py` : pages anglaises — `GUIDES_EN` (fiches traduites, clé `fr` = slug français) et `METHODS_EN` (méthodes traduites, clé `fr`).
- `gen.py` : génère pages territoires, fiches, /fiches/, /methodes/, calculateur, glossaire, à propos, toutes les pages /en/, `sitemap.xml` et `llms.txt`, avec hreflang FR/EN automatiques quand une traduction existe.

Commande, depuis la racine du dépôt :

    python3 outils/gen.py .

Ajouter une fiche FR : une entrée dans `FICHES` (dans `contenu_fr_plus.py`) avec slug, machine, domaine ("Machines industrielles" ou "Bâtiment et installations"), niveau, date, h1, title (≤ 50 car.), desc (≤ 155 car.), intro, signes, causes, faire, secu, faq, related (slugs existants).
Traduire une page : ajouter une entrée dans `GUIDES_EN` ou `METHODS_EN` avec la clé `fr` = slug français ; les liens hreflang se créent tout seuls.
La page d'accueil FR (index.html) n'est pas générée : y ajouter les liens des nouvelles fiches dans la section « Résoudre une panne, organiser la maintenance ».
