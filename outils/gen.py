import json, os, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fiches_data import FICHES, FICHES_BY_SLUG
ROOT = sys.argv[1]
SITE = "https://www.maintenanceiq.fr"
WA = "https://wa.me/33698711848"
TODAY = "2026-11-20"

FOOT = ('<footer><div class="wrap">© 2026 MaintenanceIQ — SAHALI, Bourg-en-Bresse.\n'
        '<nav><a href="/">Diagnostic gratuit</a><a href="/fiches/">Fiches terrain</a><a href="/calculateur-cout-panne/">Coût d’une panne</a><a href="/glossaire/">Glossaire</a><a href="/a-propos/">À propos</a>'
        '<a href="/mentions-legales/">Mentions légales</a><a href="/cgv/">Conditions de vente</a>'
        '<a href="/confidentialite/">Confidentialité</a><a href="mailto:sahali.prof@gmail.com">Contact</a></nav>'
        '<nav><a href="/mayotte/">Mayotte</a><a href="/la-reunion/">La Réunion</a><a href="/guadeloupe/">Guadeloupe</a>'
        '<a href="/martinique/">Martinique</a><a href="/guyane/">Guyane</a></nav></div></footer>')

ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": "MaintenanceIQ", "url": SITE + "/"}

def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}

def page(path, title, desc, body, ld, og_type="website"):
    url = SITE + path
    ldjson = json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False)
    html = f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><script>(function(l){{if(l.hostname!=="localhost"&&(l.protocol==="http:"||l.hostname==="maintenanceiq.fr"))l.replace("https://www.maintenanceiq.fr"+l.pathname+l.search+l.hash)}})(location)</script><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}"><meta property="og:locale" content="fr_FR"><meta property="og:site_name" content="MaintenanceIQ">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.png"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon.png" type="image/png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/fonts.css"><link rel="stylesheet" href="/assets/pages.css">
<script type="application/ld+json">{ldjson}</script>
</head><body>
<header class="top"><div class="wrap"><a href="/">MaintenanceIQ</a><a class="back" href="/#demande-pilote">Pilote gratuit</a></div></header>
<main><div class="wrap">
{body}
</div></main>
{FOOT}
</body></html>
'''
    d = os.path.join(ROOT, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(html)

def wa(text):
    return WA + "?text=" + urllib.parse.quote(text)

OFFER = '''<h2>Comment commencer</h2>
<ul>
<li><strong>Diagnostic gratuit</strong> sur <a href="/#diagnostic">la page d’accueil</a> : choisissez la machine, cochez ce que vous constatez, obtenez un niveau d’urgence et quoi vérifier. Sans compte, sans capteur.</li>
<li><strong>Pilote gratuit de 30 jours</strong> sur 5 machines, suivies avec vous à distance par téléphone ou WhatsApp. Aucun paiement demandé.</li>
<li><strong>Abonnements sans engagement</strong> : Essentiel 45 € par mois (10 machines), Pro 70 € par mois (30 machines), Entreprise 120 € par mois (60 machines). <a href="/#pilote">Voir les offres</a>.</li>
<li><strong>Guide « Diagnostiquer avant la panne »</strong> : 37 pages, 29 €, téléchargement immédiat. <a href="/ebook/extrait-diagnostiquer-avant-la-panne.pdf">Lire le chapitre 1 gratuitement</a> · <a href="/#pilote">Acheter le guide</a>.</li>
</ul>'''

# ---------- Territoires ----------
T = [
 ("mayotte", "Mayotte", "à Mayotte", "Mayotte",
  "Chaleur et humidité toute l’année, air salin sur une île où la plupart des sites sont proches de la mer, et des pièces de rechange qui arrivent par bateau au port de Longoni ou par avion : à Mayotte, une machine à l’arrêt peut le rester longtemps.",
  ["Les tensions sur l’eau potable font travailler dur les pompes, surpresseurs et groupes de forage : une cavitation ou un roulement fatigué doit être repéré tôt.",
   "Les coupures de courant rendent les groupes électrogènes indispensables : un filtre ou une batterie négligés se paient au pire moment.",
   "La saison des pluies et l’humidité attaquent les armoires électriques, les bornes et les fixations.",
   "La saison cyclonique (le cyclone Chido a frappé l’île en décembre 2024) rappelle l’intérêt de connaître l’état de ses machines avant un événement."]),
 ("la-reunion", "La Réunion", "à La Réunion", "La Réunion",
  "Climat tropical, saison cyclonique, embruns sur le littoral et pièces importées par le port de la Pointe des Galets : à La Réunion, chaque panne imprévue coûte du temps et de la production.",
  ["Pendant la campagne sucrière, les équipements des sucreries et distilleries tournent sans relâche : un arrêt en pleine campagne pèse lourd.",
   "Les sites du littoral subissent l’air salin : corrosion des bornes, des fixations et des carters.",
   "La chaleur humide encrasse les radiateurs et les condenseurs des groupes froids, ce qui fait chauffer les machines.",
   "Les épisodes cycloniques et les fortes pluies coupent parfois routes et électricité : groupes électrogènes et pompes de relevage doivent être prêts."]),
 ("guadeloupe", "Guadeloupe", "en Guadeloupe", "Guadeloupe",
  "Air salin, saison cyclonique, épisodes de brume de sable venue du Sahara et pièces qui arrivent par bateau : en Guadeloupe, la maintenance doit anticiper plus qu’ailleurs.",
  ["La brume de sable encrasse vite les filtres à air des compresseurs, des groupes électrogènes et des moteurs : leur contrôle doit être plus fréquent pendant ces épisodes.",
   "Les distilleries et l’agroalimentaire dépendent de pompes, de convoyeurs et de groupes froids en bon état pendant la saison de production.",
   "L’air marin corrode les parties métalliques et les connexions électriques exposées.",
   "Pendant la saison cyclonique, il vaut mieux connaître l’état des groupes électrogènes et des pompes avant l’alerte."]),
 ("martinique", "Martinique", "en Martinique", "Martinique",
  "Chaleur, humidité, air salin, saison cyclonique et brume de sable : en Martinique, les machines des petits sites industriels s’usent plus vite et les pièces mettent du temps à arriver par bateau.",
  ["Pendant la récolte de la canne, les distilleries de rhum tournent au maximum : une pompe ou un convoyeur qui lâche arrête toute la chaîne.",
   "La brume de sable encrasse les filtres à air : compresseurs et groupes électrogènes en souffrent.",
   "L’air marin attaque bornes, fixations et carters, surtout sur les sites côtiers.",
   "Les épisodes cycloniques imposent d’avoir des groupes électrogènes et des pompes prêts à démarrer."]),
 ("guyane", "Guyane", "en Guyane", "Guyane",
  "Climat équatorial très humide, fortes pluies, grandes distances entre les sites et pièces importées par le port de Dégrad-des-Cannes : en Guyane, une panne loin de tout peut immobiliser un site pendant des jours.",
  ["L’humidité permanente favorise la condensation dans les armoires électriques et les moteurs : défauts d’isolement et disjonctions à surveiller.",
   "Sur les chantiers, carrières et scieries, la poussière et la boue usent les roulements, les courroies et les filtres.",
   "Les sites isolés dépendent de groupes électrogènes : leur entretien régulier évite des arrêts longs.",
   "La chaleur fait travailler les groupes froids et les ventilateurs : condenseurs et grilles encrassés font vite monter la température."]),
]
for slug, name, prep, area, intro, points in T:
    title = f"Maintenance industrielle {prep} — MaintenanceIQ"
    desc = f"Diagnostic de panne gratuit sur téléphone, sans capteur, pour les petits sites industriels {prep}. Pilote gratuit 30 jours, abonnements dès 45 €/mois."
    others = " · ".join(f'<a href="/{s}/">{n}</a>' for s, n, *_ in T if s != slug)
    msg = f"Bonjour MaintenanceIQ,\n\nJe souhaite demander le pilote gratuit de 30 jours.\nEntreprise : (à préciser)\nTerritoire : {name}\nNombre de machines : (à préciser)\n\nMerci."
    body = f'''<h1>Maintenance industrielle {prep}</h1>
<p class="muted">Diagnostic de panne sur téléphone pour les petits sites industriels · mis à jour le 20 novembre 2026</p>
<p>{intro}</p>
<p>MaintenanceIQ aide les petits sites industriels {prep} qui n’ont ni capteurs ni logiciel de maintenance à repérer les signes d’une panne avant l’arrêt : vibration, bruit, chauffe, fuite, baisse de débit ou de pression.</p>
<h2>Ce qui use les machines {prep}</h2>
<ul>{"".join(f"<li>{p}</li>" for p in points)}</ul>
<h2>Les machines que vous pouvez diagnostiquer</h2>
<p>Groupe électrogène, pompe, moteur électrique, compresseur d’air, groupe froid, ventilateur, convoyeur, broyeur ou mélangeur, réducteur. Pour chacune, l’outil donne un niveau d’urgence (bon état, surveillance, alerte, critique), le délai conseillé, quoi vérifier en premier et les pièces à prévoir.</p>
{OFFER}
<div class="card"><strong>Demander le pilote gratuit {prep}</strong><br>Sans engagement, aucun paiement demandé.<br>
<a class="btn" href="{wa(msg)}" target="_blank" rel="noopener">Envoyer ma demande sur WhatsApp</a><br>
<span class="muted">Ou par e-mail : <a href="mailto:sahali.prof@gmail.com">sahali.prof@gmail.com</a> · WhatsApp 06 98 71 18 48</span></div>
<h2>À lire aussi</h2>
<ul>{"".join(f'<li><a href="/fiches/{x}/">{FICHES_BY_SLUG[x]["h1"]}</a></li>' for x in ["groupe-electrogene-ne-demarre-pas","cavitation-pompe","chambre-froide-temperature-remonte","armoire-electrique-connexion-qui-chauffe","moteur-qui-disjoncte"])}</ul>
<p><a href="/calculateur-cout-panne/">Calculer le coût d’une panne sur votre site</a> · <a href="/fiches/">Toutes les fiches terrain</a></p>
<p class="muted">Autres territoires : {others}</p>'''
    ld = [ORG,
          {"@type": "Service", "name": f"Diagnostic et suivi de maintenance industrielle {prep}",
           "serviceType": "Maintenance conditionnelle sans capteurs", "provider": {"@id": SITE + "/#org"},
           "areaServed": {"@type": "AdministrativeArea", "name": area}, "url": SITE + f"/{slug}/",
           "offers": [{"@type": "Offer", "name": "Pilote gratuit 30 jours (5 machines)", "price": "0", "priceCurrency": "EUR"},
                      {"@type": "Offer", "name": "Essentiel (10 machines)", "price": "45", "priceCurrency": "EUR"}]},
          crumbs([("Accueil", "/"), (name, f"/{slug}/")])]
    page(f"/{slug}/", title, desc, body, ld)

# ---------- Fiche cavitation ----------
fiche_body = '''<p class="muted"><a href="/fiches/">Fiches terrain</a> · publiée le 16 novembre 2026 · par SAHALI, MaintenanceIQ</p>
<h1>La pompe qui « mange du gravier » : reconnaître la cavitation</h1>
<p>Une pompe centrifuge qui fait un bruit de gravier est le plus souvent en cavitation : de petites bulles de vapeur se forment à l’aspiration puis éclatent sur la roue. Elle use la roue en silence pendant des semaines, puis le débit s’effondre. Forage, surpresseur, eau de process, lavage : toutes les pompes centrifuges sont concernées. Sur une île où la roue de rechange arrive par bateau, mieux vaut la repérer tôt.</p>
<h2>Les signes</h2>
<ul>
<li>Un bruit de crépitement, comme du gravier qui passe dans la pompe.</li>
<li>Une vibration qui augmente, souvent irrégulière.</li>
<li>Un débit ou une pression au refoulement qui baisse ou fluctue.</li>
<li>Le moteur tourne mais la pompe « pousse » moins qu’avant.</li>
</ul>
<h2>Comment vérifier</h2>
<ul>
<li>Le niveau d’eau à l’aspiration (bâche, cuve, forage) est-il trop bas ?</li>
<li>La crépine ou le filtre d’aspiration est-il encrassé ?</li>
<li>La vanne d’aspiration est-elle bien ouverte en grand ?</li>
<li>Y a-t-il une prise d’air : joint, raccord ou presse-étoupe côté aspiration ?</li>
<li>Si un manomètre est monté à l’aspiration, la dépression est-elle plus forte que d’habitude ?</li>
</ul>
<h2>Que faire</h2>
<ul>
<li>Machine arrêtée et consignée : nettoyer la crépine ou le filtre, ouvrir complètement la vanne d’aspiration, resserrer ou changer le joint qui prend l’air.</li>
<li>Rétablir un niveau d’eau suffisant avant de redémarrer, ou protéger la pompe contre la marche à sec.</li>
<li>Si le bruit continue, faire contrôler la pompe par un technicien : la roue est peut-être déjà creusée. Commander la pièce avant la casse coûte moins cher qu’un arrêt.</li>
<li>Noter la date, le bruit et la pression dans le carnet de la machine pour suivre l’évolution.</li>
</ul>
<p>Toujours respecter les consignes de sécurité du site : ne jamais intervenir sur une pompe en marche.</p>
<div class="card"><strong>Un doute sur une pompe ?</strong><br>Faites le <a href="/#diagnostic">diagnostic gratuit</a> en 2 minutes, ou demandez l’avis de MaintenanceIQ.<br>
<a class="btn" href="https://wa.me/33698711848" target="_blank" rel="noopener">Écrire sur WhatsApp</a></div>
<p>Pour aller plus loin : <a href="/ebook/extrait-diagnostiquer-avant-la-panne.pdf">lisez gratuitement le chapitre 1</a> du guide « Diagnostiquer avant la panne » (37 pages, 29 €).</p>
<p class="muted">Territoires : <a href="/mayotte/">Mayotte</a> · <a href="/la-reunion/">La Réunion</a> · <a href="/guadeloupe/">Guadeloupe</a> · <a href="/martinique/">Martinique</a> · <a href="/guyane/">Guyane</a></p>'''
page("/fiches/cavitation-pompe/", "Pompe qui fait un bruit de gravier : la cavitation — MaintenanceIQ",
     "Bruit de gravier, vibration, baisse de débit : comment reconnaître la cavitation d’une pompe centrifuge, quoi vérifier et que faire avant la casse.",
     fiche_body,
     [ORG, {"@type": "Article", "headline": "La pompe qui « mange du gravier » : reconnaître la cavitation",
            "datePublished": "2026-11-16", "dateModified": TODAY, "inLanguage": "fr",
            "author": {"@type": "Person", "name": "SAHALI", "url": SITE + "/a-propos/"},
            "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": SITE + "/fiches/cavitation-pompe/"},
      crumbs([("Accueil", "/"), ("Fiches terrain", "/fiches/"), ("Cavitation d’une pompe", "/fiches/cavitation-pompe/")])],
     og_type="article")

page("/fiches/", "Fiches terrain de maintenance industrielle — MaintenanceIQ",
     "Fiches pratiques pour repérer une panne avant l’arrêt : signes, vérifications et actions, pour les petits sites industriels d’outre-mer.",
     '''<h1>Fiches terrain</h1>
<p>Une fiche par défaut fréquent : les signes qui doivent alerter, comment vérifier sans capteur, et quoi faire avant la casse. Une nouvelle fiche paraît régulièrement.</p>
<ul>
<li><a href="/fiches/cavitation-pompe/"><strong>La pompe qui « mange du gravier » : reconnaître la cavitation</strong></a> — 16 novembre 2026</li>
</ul>
<p>Pour aller plus loin : le guide <a href="/#pilote">« Diagnostiquer avant la panne »</a> (37 pages, 6 fiches à imprimer, 29 €).</p>''',
     [ORG, {"@type": "CollectionPage", "name": "Fiches terrain MaintenanceIQ", "url": SITE + "/fiches/"},
      crumbs([("Accueil", "/"), ("Fiches terrain", "/fiches/")])])

# ---------- À propos ----------
page("/a-propos/", "À propos de MaintenanceIQ — SAHALI",
     "MaintenanceIQ, créé par SAHALI, formé à la maintenance industrielle : un diagnostic simple, sur téléphone, pour les petits sites industriels d’outre-mer.",
     '''<h1>À propos de MaintenanceIQ</h1>
<p>MaintenanceIQ est une marque de <strong>SAHALI</strong>, entrepreneur individuel (nom commercial Atelier Calibre, SIREN 132 761 131) basé à Bourg-en-Bresse. Elle s’adresse aux petits sites industriels de Mayotte, de La Réunion, de la Guadeloupe, de la Martinique et de la Guyane.</p>
<h2>Qui est derrière MaintenanceIQ</h2>
<p>SAHALI a appris la maintenance là où les pannes coûtent : sur les lignes de production. Il a d’abord été conducteur de machines de filmage et de conditionnement dans l’agroalimentaire, puis opérateur et monteur dans l’industrie du poids lourd, avant d’assembler des châssis de camions frigorifiques en atelier.</p>
<ul>
<li>Formation d’agent de maintenance industrielle (2024-2025).</li>
<li>Habilitation électrique BR.</li>
<li>Réglage, conduite et maintenance de premier niveau de machines industrielles.</li>
<li>Plus de six ans en production industrielle : agroalimentaire, conditionnement, assemblage de véhicules.</li>
</ul>
<p>C’est cette expérience de terrain qui a donné la méthode de MaintenanceIQ : partir de ce que l’opérateur voit, entend et sent, signaler tôt les dysfonctionnements et choisir le moment de l’intervention.</p>
<h2>Pourquoi l’outre-mer</h2>
<p>Dans ces territoires, une panne coûte plus cher qu’ailleurs : chaleur, humidité et air salin usent les machines plus vite, et les pièces de rechange arrivent par bateau ou par avion. Les petits sites ont rarement des capteurs ou un logiciel de maintenance. MaintenanceIQ propose une méthode simple, en français, depuis un téléphone, pour repérer les signes d’une panne assez tôt et intervenir au moment choisi.</p>
<h2>La méthode</h2>
<ul>
<li>Des règles publiques et simples : le niveau d’urgence retenu est le plus grave des signes constatés (voir <a href="/#methode">comment le niveau est choisi</a>).</li>
<li>Une vibration mesurée est lue selon les zones de la norme ISO 10816, d’après la puissance de la machine.</li>
<li>Un suivi à distance par WhatsApp ou e-mail pour les abonnés, avec l’historique de chaque machine.</li>
</ul>
<h2>Ce que MaintenanceIQ ne fait pas</h2>
<p>L’outil ne voit pas la machine, ne prédit pas de date de panne, ne se connecte pas à vos équipements et ne remplace ni un technicien ni un contrôle obligatoire.</p>
<h2>Contact</h2>
<p>E-mail : <a href="mailto:sahali.prof@gmail.com">sahali.prof@gmail.com</a> · WhatsApp : <a href="https://wa.me/33698711848">06 98 71 18 48</a></p>''',
     [{**ORG, "email": "sahali.prof@gmail.com", "telephone": "+33698711848", "founder": {"@type": "Person", "@id": SITE + "/a-propos/#sahali", "name": "SAHALI", "url": SITE + "/a-propos/",
         "jobTitle": "Agent de maintenance industrielle",
         "hasCredential": [{"@type": "EducationalOccupationalCredential", "name": "Formation d’agent de maintenance industrielle"},
                           {"@type": "EducationalOccupationalCredential", "name": "Habilitation électrique BR"}],
         "knowsAbout": ["maintenance industrielle de premier niveau", "conduite de machines de conditionnement", "agroalimentaire", "assemblage de véhicules frigorifiques"]},
       "areaServed": ["Mayotte", "La Réunion", "Guadeloupe", "Martinique", "Guyane"]},
      {"@type": "AboutPage", "url": SITE + "/a-propos/", "about": {"@id": SITE + "/#org"}},
      crumbs([("Accueil", "/"), ("À propos", "/a-propos/")])])

# ---------- Fiches terrain (données) ----------
MONTHS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
def fr_date(d):
    y, m, j = d.split("-"); return f"{int(j)} {MONTHS[int(m)-1]} {y}"
EXTRAIT = "/ebook/extrait-diagnostiquer-avant-la-panne.pdf"

for f in FICHES:
    rel = "".join(f'<li><a href="/fiches/{r}/">{FICHES_BY_SLUG[r]["h1"]}</a></li>' for r in f["related"])
    causes = "".join(f"<tr><td>{c}</td><td>{v}</td></tr>" for c, v in f["causes"])
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in f["faq"])
    body = f'''<p class="muted"><a href="/">Accueil</a> › <a href="/fiches/">Fiches terrain</a> › {f["machine"]}</p>
<h1>{f["h1"]}</h1>
<p class="muted">Fiche terrain · {f["machine"]} · publiée le {fr_date(f["date"])} · par <a href="/a-propos/">SAHALI</a>, MaintenanceIQ</p>
<p>{f["intro"]}</p>
<h2>Les signes qui doivent alerter</h2>
<ul>{"".join(f"<li>{x}</li>" for x in f["signes"])}</ul>
<h2>Causes probables et comment les vérifier</h2>
<div class="tw"><table><thead><tr><th>Cause probable</th><th>Comment vérifier</th></tr></thead><tbody>{causes}</tbody></table></div>
<h2>Que faire</h2>
<ol>{"".join(f"<li>{x}</li>" for x in f["faire"])}</ol>
<div class="card"><strong>Sécurité d’abord.</strong> {f["secu"]} Les consignes de votre site et du constructeur passent toujours avant cette fiche.</div>
<h2>Questions fréquentes</h2>
{faq_html}
<div class="card"><strong>Un doute sur cette machine ?</strong><br>Faites le <a href="/#diagnostic">diagnostic gratuit</a> en 2 minutes sur téléphone, ou demandez le <a href="/#demande-pilote">pilote gratuit de 30 jours</a> : nous suivons 5 machines avec vous, à distance.<br>
<a class="btn" href="https://wa.me/33698711848" target="_blank" rel="noopener">Demander l’avis de MaintenanceIQ sur WhatsApp</a></div>
<p>Pour aller plus loin : <a href="{EXTRAIT}">lisez gratuitement le chapitre 1</a> du guide « Diagnostiquer avant la panne » (37 pages, 29 €), qui détaille le diagnostic machine par machine.</p>
<h2>Fiches liées</h2>
<ul>{rel}</ul>
<p class="muted">Territoires : <a href="/mayotte/">Mayotte</a> · <a href="/la-reunion/">La Réunion</a> · <a href="/guadeloupe/">Guadeloupe</a> · <a href="/martinique/">Martinique</a> · <a href="/guyane/">Guyane</a></p>'''
    url = SITE + f"/fiches/{f['slug']}/"
    ld = [ORG,
          {"@type": "TechArticle", "headline": f["h1"], "description": f["desc"], "datePublished": f["date"], "dateModified": TODAY,
           "inLanguage": "fr", "about": f["machine"], "author": {"@type": "Person", "name": "SAHALI", "url": SITE + "/a-propos/"},
           "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": url, "image": SITE + "/og-image.png"},
          {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in f["faq"]]},
          crumbs([("Accueil", "/"), ("Fiches terrain", "/fiches/"), (f["machine"], f"/fiches/{f['slug']}/")])]
    page(f"/fiches/{f['slug']}/", f'{f["title"]} — MaintenanceIQ', f["desc"], body, ld, og_type="article")

# ---------- Index des fiches, groupé par machine ----------
groups = {}
for f in FICHES: groups.setdefault(f["machine"], []).append(f)
idx = "".join(f'<h2>{m}</h2><ul>' + "".join(f'<li><a href="/fiches/{x["slug"]}/"><strong>{x["h1"]}</strong></a><br><span class="muted">{x["desc"]}</span></li>' for x in L) + "</ul>" for m, L in groups.items())
page("/fiches/", "Fiches terrain de maintenance industrielle — MaintenanceIQ",
     "Pompes, moteurs, roulements, groupes électrogènes, compresseurs, froid, armoires électriques : des fiches pour repérer une panne avant l’arrêt, sans capteur.",
     f'''<p class="muted"><a href="/">Accueil</a> › Fiches terrain</p>
<h1>Fiches terrain</h1>
<p>Une fiche par défaut fréquent : les signes qui doivent alerter, les causes probables et comment les vérifier sans capteur, puis quoi faire avant la casse. {len(FICHES)} fiches, classées par machine, écrites pour les petits sites industriels d’outre-mer où chaque panne coûte cher.</p>
<p>Vous ne savez pas par où commencer ? Faites le <a href="/#diagnostic">diagnostic gratuit</a> ou <a href="/calculateur-cout-panne/">calculez ce que vous coûte une panne</a>.</p>
{idx}
<div class="card">Pour aller plus loin : <a href="{EXTRAIT}">lisez gratuitement le chapitre 1</a> du guide « Diagnostiquer avant la panne » (37 pages, 29 €).</div>''',
     [ORG, {"@type": "CollectionPage", "name": "Fiches terrain MaintenanceIQ", "url": SITE + "/fiches/",
            "hasPart": [{"@type": "TechArticle", "headline": x["h1"], "url": SITE + f"/fiches/{x['slug']}/"} for x in FICHES]},
      crumbs([("Accueil", "/"), ("Fiches terrain", "/fiches/")])])

# ---------- Calculateur du coût d'une panne ----------
calc = f'''<p class="muted"><a href="/">Accueil</a> › Coût d’une panne</p>
<h1>Calculez le vrai coût d’une panne</h1>
<p>Une direction ne finance pas « de la maintenance » : elle finance des pertes évitées. Entrez vos propres chiffres pour estimer ce que coûte une panne non anticipée sur votre site. Le calcul se fait sur votre téléphone : rien n’est envoyé.</p>
<form id="calc" class="card" onsubmit="return false" style="display:grid;gap:12px">
<label>Heures d’arrêt de production<br><input id="h" type="number" inputmode="decimal" min="0" step="any" value="72"></label>
<label>Marge perdue par heure d’arrêt (€)<br><input id="m" type="number" inputmode="decimal" min="0" step="any" value="125"></label>
<label>Heures de main-d’œuvre (attente et réparation)<br><input id="mo" type="number" inputmode="decimal" min="0" step="any" value="20"></label>
<label>Coût horaire de la main-d’œuvre (€)<br><input id="t" type="number" inputmode="decimal" min="0" step="any" value="35"></label>
<label>Pièces au prix d’urgence et transport express (€)<br><input id="p" type="number" inputmode="decimal" min="0" step="any" value="1800"></label>
<label>Coûts induits : produits perdus, pénalités, heures supplémentaires, location (€)<br><input id="c" type="number" inputmode="decimal" min="0" step="any" value="1200"></label>
<p style="margin:0;font-size:20px">Coût estimé de la panne : <strong id="tot">–</strong></p>
<p class="muted" id="det" style="margin:0"></p>
</form>
<p>Valeurs de départ : hypothèses d’illustration. Remplacez-les par les vôtres.</p>
<h2>La formule</h2>
<p><strong>Coût d’une panne</strong> = production perdue (heures d’arrêt × marge perdue par heure) + main-d’œuvre (attente, réparation, heures supplémentaires) + pièces (prix d’urgence, transport express) + coûts induits (produits perdus, pénalités de retard, clients perdus, location de matériel de secours).</p>
<h2>Pourquoi c’est plus cher en outre-mer</h2>
<p>À Mayotte, à La Réunion, aux Antilles ou en Guyane, la pièce qui manque arrive souvent par avion ou par bateau. Chaque jour d’attente ajoute des heures d’arrêt. La même défaillance repérée quelques semaines plus tôt (bruit, chauffe, vibration) permet de commander la pièce par voie normale et de la changer pendant un arrêt déjà prévu.</p>
<h2>Exemple</h2>
<p>Dans l’exemple du guide « Diagnostiquer avant la panne », la panne non anticipée d’une pompe de reprise dans une petite unité d’embouteillage (3 jours d’arrêt, pièces par avion) est estimée à 12 700 €, contre 285 € pour la même défaillance repérée six semaines plus tôt. Ces chiffres sont des hypothèses d’illustration, pas un résultat client.</p>
<div class="card"><strong>Réduire ce coût</strong><br>Commencez par le <a href="/#diagnostic">diagnostic gratuit</a>, lisez les <a href="/fiches/">fiches terrain</a>, ou demandez le <a href="/#demande-pilote">pilote gratuit de 30 jours</a>.<br>
<a class="btn" href="https://wa.me/33698711848" target="_blank" rel="noopener">Parler de vos machines sur WhatsApp</a></div>
<script>(function(){{var $=function(i){{return document.getElementById(i)}};var f=new Intl.NumberFormat("fr-FR",{{style:"currency",currency:"EUR",maximumFractionDigits:0}});
function v(i){{var x=parseFloat($(i).value);return isFinite(x)&&x>0?x:0}}
function r(){{var prod=v("h")*v("m"),mo=v("mo")*v("t"),p=v("p"),c=v("c");$("tot").textContent=f.format(prod+mo+p+c);
$("det").textContent="Production perdue "+f.format(prod)+" · main-d’œuvre "+f.format(mo)+" · pièces "+f.format(p)+" · coûts induits "+f.format(c)}}
$("calc").addEventListener("input",r);r()}})()</script>'''
page("/calculateur-cout-panne/", "Calculateur du coût d’une panne machine — MaintenanceIQ",
     "Calculez gratuitement le coût réel d’une panne : production perdue, main-d’œuvre, pièces en urgence, coûts induits. Pour les sites industriels d’outre-mer.",
     calc,
     [ORG, {"@type": "WebApplication", "name": "Calculateur du coût d’une panne", "url": SITE + "/calculateur-cout-panne/",
            "applicationCategory": "BusinessApplication", "operatingSystem": "Tous navigateurs", "inLanguage": "fr",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "provider": {"@id": SITE + "/#org"}},
      crumbs([("Accueil", "/"), ("Coût d’une panne", "/calculateur-cout-panne/")])])

# ---------- Glossaire ----------
GLOSS = [
 ("Balourd", "Répartition inégale de la masse d’un rotor (pale encrassée, pièce usée), qui le fait vibrer à chaque tour.", "ventilateur-qui-vibre"),
 ("Cavitation", "Formation puis implosion de bulles de vapeur dans une pompe quand la pression à l’aspiration est trop faible. Bruit de graviers, érosion de la roue.", "cavitation-pompe"),
 ("Consignation", "Ensemble des opérations qui mettent une machine en sécurité avant intervention : séparation des énergies, condamnation, vérification d’absence de tension.", None),
 ("Criticité", "Importance d’une machine pour l’activité, la sécurité et le coût d’une panne.", None),
 ("Émissivité", "Capacité d’une surface à émettre du rayonnement infrarouge. Les surfaces brillantes ont une faible émissivité et faussent les mesures sans contact.", None),
 ("État de référence", "Ensemble des mesures prises sur une machine en bon état, qui sert de base de comparaison.", None),
 ("Garniture mécanique", "Dispositif d’étanchéité entre l’arbre tournant et le corps d’une pompe.", "pompe-garniture-mecanique-fuit"),
 ("GMAO", "Gestion de maintenance assistée par ordinateur : logiciel de suivi des machines et des interventions.", None),
 ("Intervalle P-F", "Temps entre le moment où un défaut devient détectable (P) et la panne (F).", None),
 ("Maintenance conditionnelle", "Maintenance déclenchée par l’état mesuré de la machine, et non par une date fixe ou par la panne.", None),
 ("Pied boiteux", "Pied de machine qui ne repose pas à plat : en serrant le boulon, on déforme le bâti et on fausse l’alignement.", "courroie-qui-siffle-ou-patine"),
 ("Résistance d’isolement", "Résistance entre le bobinage d’un moteur et sa carcasse, mesurée en MΩ. Elle baisse avec l’humidité et le vieillissement.", "moteur-qui-disjoncte"),
 ("Vitesse vibratoire efficace", "Mesure de vibration en mm/s utilisée par les normes (série ISO 10816, devenue ISO 20816) pour évaluer l’état général d’une machine.", "ventilateur-qui-vibre"),
]
gl = "".join(f'<h2 id="{urllib.parse.quote(t.lower().replace(" ","-"))}">{t}</h2><p>{d}' + (f' <a href="/fiches/{s}/">Voir la fiche terrain</a>.' if s else "") + "</p>" for t, d, s in GLOSS)
page("/glossaire/", "Glossaire de la maintenance industrielle — MaintenanceIQ",
     "Cavitation, balourd, garniture mécanique, pied boiteux, intervalle P-F, maintenance conditionnelle : les mots de la maintenance industrielle expliqués simplement.",
     f'''<p class="muted"><a href="/">Accueil</a> › Glossaire</p>
<h1>Glossaire de la maintenance industrielle</h1>
<p>Les mots essentiels pour comprendre et suivre l’état de vos machines, expliqués simplement. Issus du guide « Diagnostiquer avant la panne ».</p>
{gl}
<div class="card">Mettez ces notions en pratique avec le <a href="/#diagnostic">diagnostic gratuit</a> et les <a href="/fiches/">fiches terrain</a>.</div>''',
     [ORG, {"@type": "DefinedTermSet", "name": "Glossaire de la maintenance industrielle", "url": SITE + "/glossaire/", "inLanguage": "fr",
            "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d, s in GLOSS]},
      crumbs([("Accueil", "/"), ("Glossaire", "/glossaire/")])])

# ---------- sitemap et llms.txt ----------
urls = [("/", TODAY)] + [(f"/{s}/", TODAY) for s in ["mayotte","la-reunion","guadeloupe","martinique","guyane"]] + \
       [("/fiches/", TODAY)] + [(f"/fiches/{f['slug']}/", f["date"] if f["date"] > "2026-11-20" else TODAY) for f in FICHES] + \
       [("/calculateur-cout-panne/", TODAY), ("/glossaire/", TODAY), ("/a-propos/", TODAY),
        ("/cgv/", "2026-11-20"), ("/mentions-legales/", "2026-11-20"), ("/confidentialite/", "2026-11-14")]
open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n")
llms = open(os.path.join(ROOT, "llms.txt")).read()
llms = llms.split("## Fiches terrain")[0].rstrip() + "\n\n## Outils\n- [Calculateur du coût d'une panne](https://www.maintenanceiq.fr/calculateur-cout-panne/)\n- [Glossaire de la maintenance industrielle](https://www.maintenanceiq.fr/glossaire/)\n\n## Fiches terrain\n" + \
       "".join(f"- [{f['title']}]({SITE}/fiches/{f['slug']}/): {f['desc']}\n" for f in FICHES)
open(os.path.join(ROOT, "llms.txt"), "w").write(llms)

print("ok")
