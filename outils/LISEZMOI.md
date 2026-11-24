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

Ajouts du 23/11/2026 (gérés par `gen.py`, ne pas retirer) :
- Code Google AdSense (`ADSENSE`) dans le `<head>` de chaque page générée. Les pages écrites à la main (index.html, en/index.html, cgv, confidentialite, mentions-legales, 404, merci) l'ont aussi : à garder si on les modifie.
- Bloc « Partager cette fiche » (WhatsApp, LinkedIn, Facebook, e-mail, copier le lien) en bas des fiches, méthodes et guides.
- Flux RSS : `/feed.xml` (FR) et `/en/feed.xml` (EN).
- IndexNow : `.github/workflows/indexnow.yml` prévient Bing et les autres moteurs à chaque mise en ligne ; la clé est le fichier `<clé>.txt` à la racine (ne pas supprimer).
- Outils gratuits : `calcs_fr.py` (calculateurs `/calculateurs/…` et modèles à imprimer `/modeles/…`). Schémas et repères chiffrés des fiches : `schemas_fr.py`. Images d'aperçu : `/og/` (générées).

## Contrôle qualité (anti-bug)
- `python3 outils/gen.py <racine>` lance automatiquement `outils/check.py` et s'arrête en cas d'erreur : ne jamais publier si « ÉCHEC du contrôle qualité » s'affiche.
- Tests navigateur (largeur téléphone) : `python3 outils/check_browser.py http://localhost:8765 .` et `python3 outils/check_interactif.py http://localhost:8765` (serveur local `python3 -m http.server 8765`).
- GitHub Action « Contrôle qualité du site » : refait les trois contrôles à chaque mise en ligne et chaque lundi.
- Habilitations : données dans `outils/symboles_fr.py` (une entrée = une page + son quiz). Anciennes adresses regroupées redirigées via REDIRECTS.
