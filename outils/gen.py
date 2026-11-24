import json, os, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fiches_data import FICHES, FICHES_BY_SLUG
import contenu_fr_plus
from contenu_fr_plus import METHODES
from schemas_fr import SCHEMAS, CAS
from calcs_fr import CALCS, MODELES
from habilitations_fr import THEMES, LECTURE, QUIZ
from symboles_fr import SYMBOLES, QZ, REDIRECTS
from PIL import Image, ImageDraw, ImageFont
_F = "/usr/share/fonts/opentype/inter/"
def make_og(name, kicker, title):
    """Image d'aperçu 1200x630 propre à chaque article (WhatsApp, LinkedIn, Facebook, Google)."""
    out = os.path.join(ROOT, "og", name + ".png")
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), "#21403A"); d = ImageDraw.Draw(im)
    fk = ImageFont.truetype(_F + "Inter-SemiBold.otf", 28)
    d.text((70, 64), kicker.upper(), font=fk, fill="#79D49B")
    size = 68
    while True:
        ft = ImageFont.truetype(_F + "Inter-ExtraBold.otf", size)
        words, lines, cur = title.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if d.textlength(t, font=ft) <= W - 140: cur = t
            else: lines.append(cur); cur = w
        lines.append(cur)
        if len(lines) * size * 1.18 <= 330 or size <= 44: break
        size -= 4
    y = 140
    for l in lines:
        d.text((70, y), l, font=ft, fill="#F0F3E9"); y += int(size * 1.18)
    for i, c in enumerate(["#3FA66A", "#E2B32C", "#E5832F", "#D9473B"]):
        d.rounded_rectangle((70 + i * 70, 520, 126 + i * 70, 538), radius=9, fill=c)
    d.text((W - 70, 516), "maintenanceiq.fr", font=fk, fill="#F0F3E9", anchor="ra")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, optimize=True)
    return "/og/" + name + ".png"
from contenu_en import GUIDES_EN, METHODS_EN
FICHES_BY_SLUG.update({f["slug"]: f for f in FICHES})
ROOT = sys.argv[1]
SITE = "https://www.maintenanceiq.fr"
WA = "https://wa.me/33698711848"
NEWSLETTER = "https://f91f7b52.sibforms.com/serve/MUIFAE3mTHOHHnIqAx6XriVNf0kF2q94i1T1sqUD_fUxcWgm9xXpYHQdRz3DVkORU_Trk67I03HwSelgxsTai8I6QkUo0lNF5dvb2g8qNoxJ0LvPhV72kSb2pihQ2ooRTTA8CjpW8GoL322ZxPbguX6AelR780rlV9cmqvEyWNshj5CgfdPo_Gem0q8SmJ332ewyCTsXBWsARAnFAQ=="  # formulaire Brevo (liste « Votre première liste »)
NL_CARD = ('<div class="card nl"><strong>Recevez 1 fiche de dépannage par semaine</strong><br>Une panne réelle expliquée simplement, gratuitement, dans votre boîte mail. Désinscription en 1 clic.<br>'
           f'<a class="btn" href="{NEWSLETTER}" target="_blank" rel="noopener">Je m’inscris gratuitement</a></div>')
TODAY = "2026-11-22"
# Ne pas supprimer : code Google AdSense (compte ca-pub-6829528595387726)
ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6829528595387726" crossorigin="anonymous"></script>\n'

FOOT = ('<footer><div class="wrap">© 2026 MaintenanceIQ — SAHALI, Bourg-en-Bresse.\n'
        '<nav><a href="/">Diagnostic gratuit</a><a href="/fiches/">Fiches terrain</a><a href="/methodes/">Méthodes</a><a href="/calculateurs/">Outils gratuits</a><a href="/habilitation-electrique/">Habilitation électrique</a><a href="/glossaire/">Glossaire</a><a href="/a-propos/">À propos</a>'
        '<a href="/mentions-legales/">Mentions légales</a><a href="/cgv/">Conditions de vente</a>'
        '<a href="/confidentialite/">Confidentialité</a><a href="mailto:sahali.prof@gmail.com">Contact</a></nav>'
        '<nav><a href="/mayotte/">Mayotte</a><a href="/la-reunion/">La Réunion</a><a href="/guadeloupe/">Guadeloupe</a>'
        '<a href="/martinique/">Martinique</a><a href="/guyane/">Guyane</a><a href="/en/" hreflang="en">English</a></nav></div></footer>')
FOOT_EN = ('<footer><div class="wrap">© 2026 MaintenanceIQ — SAHALI, France.\n'
        '<nav><a href="/en/">Home</a><a href="/en/guides/">Troubleshooting guides</a><a href="/en/methods/">Maintenance methods</a>'
        '<a href="/en/about/">About</a><a href="/mentions-legales/">Legal notice (FR)</a><a href="/cgv/">Terms of sale (FR)</a>'
        '<a href="/confidentialite/">Privacy (FR)</a><a href="mailto:sahali.prof@gmail.com">Contact</a><a href="/" hreflang="fr">Français</a></nav></div></footer>')

ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": "MaintenanceIQ", "url": SITE + "/"}

def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}

def page(path, title, desc, body, ld, og_type="website", lang="fr", alt=None):
    url = SITE + path
    if len(title) > 60 and title.endswith(" — MaintenanceIQ"):
        title = title[: -len(" — MaintenanceIQ")]
    if alt:
        fr_u, en_u = (url, SITE + alt) if lang == "fr" else (SITE + alt, url)
        hl = f'<link rel="alternate" hreflang="fr" href="{fr_u}"><link rel="alternate" hreflang="en" href="{en_u}"><link rel="alternate" hreflang="x-default" href="{fr_u}">\n'
    else:
        hl = ""
    if lang == "en":
        head_link = '<a class="back" href="/en/#offers">Free 30-day pilot</a>'
        foot = FOOT_EN
        loc = "en_GB"
        switch = f'<a class="back" href="{alt}" hreflang="fr" style="margin-left:14px">FR</a>' if alt else '<a class="back" href="/" hreflang="fr" style="margin-left:14px">FR</a>'
    else:
        head_link = '<a class="back" href="/#demande-pilote">Pilote gratuit</a>'
        foot = FOOT
        loc = "fr_FR"
        switch = f'<a class="back" href="{alt}" hreflang="en" style="margin-left:14px">EN</a>' if alt else '<a class="back" href="/en/" hreflang="en" style="margin-left:14px">EN</a>'
    if lang == "fr" and (og_type == "article" or path in ("/fiches/", "/methodes/", "/glossaire/", "/calculateur-cout-panne/", "/calculateurs/", "/habilitation-electrique/", "/qcm-habilitation-electrique/") or path.startswith("/habilitation-electrique/") or path.startswith("/calculateurs/") or path.startswith("/modeles/")):
        body += NL_CARD
    if og_type == "article":
        q = urllib.parse.quote(url, safe="")
        qt = urllib.parse.quote(title + " " + url)
        lab = ("Share this guide", "Copy link", "Link copied") if lang == "en" else ("Partager cette fiche", "Copier le lien", "Lien copié")
        body += (f'<div class="card share"><strong>{lab[0]}</strong><br>'
                 f'<a href="https://wa.me/?text={qt}" target="_blank" rel="noopener">WhatsApp</a> · '
                 f'<a href="https://www.linkedin.com/sharing/share-offsite/?url={q}" target="_blank" rel="noopener">LinkedIn</a> · '
                 f'<a href="https://www.facebook.com/sharer/sharer.php?u={q}" target="_blank" rel="noopener">Facebook</a> · '
                 f'<a href="mailto:?subject={urllib.parse.quote(title)}&amp;body={q}">E-mail</a> · '
                 f'<a href="#" onclick="navigator.clipboard&&navigator.clipboard.writeText(\'{url}\');this.textContent=\'{lab[2]}\';return false">{lab[1]}</a></div>')
    og_img = "/og-image.png"
    if og_type == "article":
        kick = ("MaintenanceIQ · Troubleshooting guide" if "/guides/" in path else "MaintenanceIQ · Maintenance method") if lang == "en" else ("MaintenanceIQ · Fiche terrain" if path.startswith("/fiches/") else "MaintenanceIQ · Habilitation électrique" if path.startswith("/habilitation-electrique/") else "MaintenanceIQ · Méthode de maintenance")
        h = title[: -len(" — MaintenanceIQ")] if title.endswith(" — MaintenanceIQ") else title
        og_img = make_og(path.strip("/").replace("/", "-"), kick, h)
        for node in ld:
            if isinstance(node, dict) and node.get("image") == SITE + "/og-image.png": node["image"] = SITE + og_img
    ldjson = json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False)
    html = f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><script>(function(l){{if(l.hostname!=="localhost"&&(l.protocol==="http:"||l.hostname==="maintenanceiq.fr"))l.replace("https://www.maintenanceiq.fr"+l.pathname+l.search+l.hash)}})(location)</script><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
{hl}<meta property="og:type" content="{og_type}"><meta property="og:locale" content="{loc}"><meta property="og:site_name" content="MaintenanceIQ">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{og_img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon.png" type="image/png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/fonts.css"><link rel="stylesheet" href="/assets/pages.css">
<script type="application/ld+json">{ldjson}</script>
<link rel="alternate" type="application/rss+xml" title="MaintenanceIQ" href="{'/en/feed.xml' if lang=='en' else '/feed.xml'}">
{ADSENSE}</head><body>
<header class="top"><div class="wrap"><a href="{'/en/' if lang=='en' else '/'}">MaintenanceIQ</a><span>{head_link}{switch}</span></div></header>
<main><div class="wrap">
{body}
</div></main>
{foot}
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
    desc = f"Diagnostic de panne sur téléphone, sans capteur, pour les petits sites industriels {prep}. Pilote gratuit 30 jours, abonnements dès 45 €/mois."
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
     '''<h1>À propos de MaintenanceIQ</h1><p><img src="/avatar-sahali.svg" width="140" height="140" alt="Avatar illustré de SAHALI, technicien de maintenance" style="display:block;border-radius:50%"></p>
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
      crumbs([("Accueil", "/"), ("À propos", "/a-propos/")])], alt="/en/about/")

# ---------- Fiches terrain (données) ----------
EN_OF = {g["fr"]: g["slug"] for g in GUIDES_EN}
EN_M_OF = {m["fr"]: m["slug"] for m in METHODS_EN}
NIV_CLASS = {"Simple": "n1", "Intermédiaire": "n2", "Avancé": "n3", "Intermediate": "n2", "Advanced": "n3"}
MONTHS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
def fr_date(d):
    y, m, j = d.split("-"); return f"{int(j)} {MONTHS[int(m)-1]} {y}"
EXTRAIT = "/ebook/extrait-diagnostiquer-avant-la-panne.pdf"

def cas_block(slug):
    c = CAS.get(slug)
    if not c: return ""
    figs = "".join(f'<figure class="schema"><img src="{src}" alt="{alt}" width="800" height="1059" loading="lazy" style="width:100%;height:auto;border-radius:4px"><figcaption>{cap}</figcaption></figure>' for src, alt, cap in c["photos"])
    return (f'<div class="card cas"><h2 style="margin-top:0">{c["titre"]}</h2><p class="muted">Témoignage de <a href="/a-propos/">SAHALI</a>, auteur de MaintenanceIQ, photos prises par l’auteur.</p>'
            + "".join(f"<p>{t}</p>" for t in c["texte"]) + figs + f'<p><strong>Ce qu’il faut en retenir.</strong> {c["lecon"]}</p></div>\n')

def schema_block(slug):
    sc = SCHEMAS.get(slug)
    if not sc: return ""
    rep = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in sc["reperes"])
    return (f'<h2>En un coup d’œil</h2><figure class="schema">{sc["svg"]}<figcaption>{sc["legende"]}</figcaption></figure>'
            f'<h2>Les repères chiffrés</h2><div class="tw"><table><thead><tr><th>Repère</th><th>Valeur indicative</th></tr></thead><tbody>{rep}</tbody></table></div>'
            '<p class="muted">Valeurs courantes données à titre indicatif : la notice du constructeur et les consignes de votre site passent avant.</p>\n')

for f in FICHES:
    rel = "".join(f'<li><a href="/fiches/{r}/">{FICHES_BY_SLUG[r]["h1"]}</a></li>' for r in f["related"])
    causes = "".join(f"<tr><td>{c}</td><td>{v}</td></tr>" for c, v in f["causes"])
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in f["faq"])
    body = f'''<p class="muted"><a href="/">Accueil</a> › <a href="/fiches/">Fiches terrain</a> › {f["machine"]}</p>
<h1>{f["h1"]}</h1>
<p class="muted"><span class="niv {NIV_CLASS[f["niveau"]]}">Niveau : {f["niveau"]}</span> {f["domaine"]} · {f["machine"]} · publiée le {fr_date(f["date"])} · par <a href="/a-propos/">SAHALI</a>, MaintenanceIQ</p>
<p>{f["intro"]}</p>
<h2>Les signes qui doivent alerter</h2>
<ul>{"".join(f"<li>{x}</li>" for x in f["signes"])}</ul>
<h2>Causes probables et comment les vérifier</h2>
<div class="tw"><table><thead><tr><th>Cause probable</th><th>Comment vérifier</th></tr></thead><tbody>{causes}</tbody></table></div>
{schema_block(f["slug"])}{cas_block(f["slug"])}<h2>Que faire</h2>
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
    page(f"/fiches/{f['slug']}/", f'{f["title"]} — MaintenanceIQ', f["desc"], body, ld, og_type="article", alt=(f"/en/guides/{EN_OF[f['slug']]}/" if f["slug"] in EN_OF else None))

# ---------- Index des fiches, groupé par machine ----------
idx = ""
for dom in ["Machines industrielles", "Bâtiment et installations"]:
    groups = {}
    for f in FICHES:
        if f["domaine"] == dom: groups.setdefault(f["machine"], []).append(f)
    idx += f'<h2>{dom}</h2>' + "".join(f'<h3>{m}</h3><ul>' + "".join(f'<li><a href="/fiches/{x["slug"]}/"><strong>{x["h1"]}</strong></a> <span class="niv {NIV_CLASS[x["niveau"]]}">{x["niveau"]}</span><br><span class="muted">{x["desc"]}</span></li>' for x in L) + "</ul>" for m, L in groups.items())
page("/fiches/", "Fiches terrain de maintenance industrielle — MaintenanceIQ",
     "Fiches de dépannage, du simple à l’avancé : pompes, moteurs, roulements, groupes électrogènes, froid, climatisation, électricité du bâtiment.",
     f'''<p class="muted"><a href="/">Accueil</a> › Fiches terrain</p>
<h1>Fiches terrain</h1>
<p>Une fiche par problème réel, du plus simple au plus complexe : les signes qui doivent alerter, les causes probables et comment les vérifier, puis quoi faire avant la casse. {len(FICHES)} fiches pour les machines industrielles et les installations du bâtiment, avec un niveau de difficulté : <span class="niv n1">Simple</span> <span class="niv n2">Intermédiaire</span> <span class="niv n3">Avancé</span>. Pour organiser la maintenance, voir les <a href="/methodes/">méthodes</a>.</p>
<p>Vous ne savez pas par où commencer ? Faites le <a href="/#diagnostic">diagnostic gratuit</a> ou <a href="/calculateur-cout-panne/">calculez ce que vous coûte une panne</a>.</p>
{idx}
<div class="card">Pour aller plus loin : <a href="{EXTRAIT}">lisez gratuitement le chapitre 1</a> du guide « Diagnostiquer avant la panne » (37 pages, 29 €).</div>''',
     [ORG, {"@type": "CollectionPage", "name": "Fiches terrain MaintenanceIQ", "url": SITE + "/fiches/",
            "hasPart": [{"@type": "TechArticle", "headline": x["h1"], "url": SITE + f"/fiches/{x['slug']}/"} for x in FICHES]},
      crumbs([("Accueil", "/"), ("Fiches terrain", "/fiches/")])], alt="/en/guides/")

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
      crumbs([("Accueil", "/"), ("Coût d’une panne", "/calculateur-cout-panne/")])], alt="/en/downtime-cost-calculator/")

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
     "Cavitation, balourd, garniture mécanique, pied boiteux, intervalle P-F, maintenance conditionnelle : les mots de la maintenance expliqués simplement.",
     f'''<p class="muted"><a href="/">Accueil</a> › Glossaire</p>
<h1>Glossaire de la maintenance industrielle</h1>
<p>Les mots essentiels pour comprendre et suivre l’état de vos machines, expliqués simplement. Issus du guide « Diagnostiquer avant la panne ».</p>
{gl}
<div class="card">Mettez ces notions en pratique avec le <a href="/#diagnostic">diagnostic gratuit</a> et les <a href="/fiches/">fiches terrain</a>.</div>''',
     [ORG, {"@type": "DefinedTermSet", "name": "Glossaire de la maintenance industrielle", "url": SITE + "/glossaire/", "inLanguage": "fr",
            "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d, s in GLOSS]},
      crumbs([("Accueil", "/"), ("Glossaire", "/glossaire/")])])


# ---------- Méthodes de maintenance (FR) ----------
M_BY = {m["slug"]: m for m in METHODES}
for m in METHODES:
    secs = "".join(f"<h2>{h}</h2>{c}" for h, c in m["sections"])
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in m["faq"])
    fl = "".join(f'<li><a href="/fiches/{x}/">{FICHES_BY_SLUG[x]["h1"]}</a></li>' for x in m["fiches"])
    others = "".join(f'<li><a href="/methodes/{o["slug"]}/">{o["h1"]}</a></li>' for o in METHODES if o["slug"] != m["slug"])[:2000]
    body = f'''<p class="muted"><a href="/">Accueil</a> › <a href="/methodes/">Méthodes</a></p>
<h1>{m["h1"]}</h1>
<p class="muted"><span class="niv {NIV_CLASS[m["niveau"]]}">Niveau : {m["niveau"]}</span> Méthode de maintenance · par <a href="/a-propos/">SAHALI</a>, MaintenanceIQ</p>
<p>{m["intro"]}</p>
{secs}
<h2>Questions fréquentes</h2>
{faq_html}
<div class="card"><strong>Passer à la pratique</strong><br>Faites le <a href="/#diagnostic">diagnostic gratuit</a>, <a href="/calculateur-cout-panne/">calculez le coût d’une panne</a>, ou demandez le <a href="/#demande-pilote">pilote gratuit de 30 jours</a> : nous mettons la méthode en place avec vous, à distance.</div>
<h2>Fiches terrain liées</h2><ul>{fl}</ul>
<h2>Autres méthodes</h2><ul>{others}</ul>'''
    url = SITE + f"/methodes/{m['slug']}/"
    ld = [ORG, {"@type": "Article", "headline": m["h1"], "description": m["desc"], "dateModified": TODAY, "datePublished": "2026-11-22",
                "inLanguage": "fr", "author": {"@type": "Person", "name": "SAHALI", "url": SITE + "/a-propos/"},
                "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": url, "image": SITE + "/og-image.png"},
          {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in m["faq"]]},
          crumbs([("Accueil", "/"), ("Méthodes", "/methodes/"), (m["h1"], f"/methodes/{m['slug']}/")])]
    page(f"/methodes/{m['slug']}/", f'{m["title"]} — MaintenanceIQ', m["desc"], body, ld, og_type="article",
         alt=(f"/en/methods/{EN_M_OF[m['slug']]}/" if m["slug"] in EN_M_OF else None))

page("/methodes/", "Méthodes de maintenance : guide complet — MaintenanceIQ",
     "Types de maintenance, courbe P-F, criticité, MTBF et MTTR, AMDEC, causes racines, plan préventif, TPM, pièces de rechange : les méthodes expliquées.",
     f'''<p class="muted"><a href="/">Accueil</a> › Méthodes</p>
<h1>Méthodes de maintenance</h1>
<p>Les fiches terrain résolvent un problème ; les méthodes organisent la maintenance pour qu’il ne revienne pas. Du plus simple au plus avancé, avec des exemples chiffrés.</p>
<ul>{"".join(f'<li><a href="/methodes/{m["slug"]}/"><strong>{m["h1"]}</strong></a> <span class="niv {NIV_CLASS[m["niveau"]]}">{m["niveau"]}</span><br><span class="muted">{m["desc"]}</span></li>' for m in METHODES)}</ul>
<div class="card"><strong>Nouveau :</strong> <a href="/habilitation-electrique/">tous les symboles d’habilitation électrique, par thème, avec un quiz</a>.</div>
<div class="card">Voir aussi : les <a href="/fiches/">fiches terrain</a>, le <a href="/calculateur-cout-panne/">calculateur du coût d’une panne</a> et le <a href="/glossaire/">glossaire</a>.</div>''',
     [ORG, {"@type": "CollectionPage", "name": "Méthodes de maintenance", "url": SITE + "/methodes/",
            "hasPart": [{"@type": "Article", "headline": m["h1"], "url": SITE + f"/methodes/{m['slug']}/"} for m in METHODES]},
      crumbs([("Accueil", "/"), ("Méthodes", "/methodes/")])], alt="/en/methods/")

# ---------- English ----------
NIV_EN = {"Simple": "Simple", "Intermediate": "Intermediate", "Advanced": "Advanced"}
FR_OF = {g["slug"]: g["fr"] for g in GUIDES_EN}
G_BY = {g["slug"]: g for g in GUIDES_EN}
OFFER_EN = '''<h2>How MaintenanceIQ can help</h2>
<ul>
<li><strong>Free 30-day pilot</strong>: we follow 5 of your machines with you, remotely, by WhatsApp or e-mail. No payment required.</li>
<li><strong>Monthly plans, no commitment</strong>: Essential €45/month (10 machines), Pro €70/month (30 machines), Enterprise €120/month (60 machines). Available worldwide.</li>
<li><strong>Field guide</strong> “Diagnostiquer avant la panne” (37 pages, in French, €29).</li>
</ul>'''
for g in GUIDES_EN:
    rel = "".join(f'<li><a href="/en/guides/{r}/">{G_BY[r]["h1"]}</a></li>' for r in g["related"] if r in G_BY)
    causes = "".join(f"<tr><td>{c}</td><td>{v}</td></tr>" for c, v in g["causes"])
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in g["faq"])
    body = f'''<p class="muted"><a href="/en/">Home</a> › <a href="/en/guides/">Troubleshooting guides</a> › {g["machine"]}</p>
<h1>{g["h1"]}</h1>
<p class="muted"><span class="niv {NIV_CLASS[g["niveau"]]}">Level: {g["niveau"]}</span> {g["domaine"]} · {g["machine"]} · by <a href="/en/about/">SAHALI</a>, MaintenanceIQ</p>
<p>{g["intro"]}</p>
<h2>Warning signs</h2>
<ul>{"".join(f"<li>{x}</li>" for x in g["signes"])}</ul>
<h2>Likely causes and how to check</h2>
<div class="tw"><table><thead><tr><th>Likely cause</th><th>How to check</th></tr></thead><tbody>{causes}</tbody></table></div>
<h2>What to do</h2>
<ol>{"".join(f"<li>{x}</li>" for x in g["faire"])}</ol>
<div class="card"><strong>Safety first.</strong> {g["secu"]} Your site’s rules and the manufacturer’s instructions always come first.</div>
<h2>Frequently asked questions</h2>
{faq_html}
<div class="card"><strong>Not sure about this machine?</strong><br>Ask for the <a href="/en/#offers">free 30-day pilot</a>: we follow 5 machines with you, remotely, wherever you are.<br>
<a class="btn" href="https://wa.me/33698711848" target="_blank" rel="noopener">Ask MaintenanceIQ on WhatsApp</a></div>
<h2>Related guides</h2><ul>{rel}</ul>'''
    url = SITE + f"/en/guides/{g['slug']}/"
    ld = [ORG, {"@type": "TechArticle", "headline": g["h1"], "description": g["desc"], "dateModified": TODAY, "datePublished": "2026-11-22",
                "inLanguage": "en", "about": g["machine"], "author": {"@type": "Person", "name": "SAHALI", "url": SITE + "/en/about/"},
                "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": url, "image": SITE + "/og-image.png"},
          {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g["faq"]]},
          crumbs([("Home", "/en/"), ("Troubleshooting guides", "/en/guides/"), (g["machine"], f"/en/guides/{g['slug']}/")])]
    page(f"/en/guides/{g['slug']}/", f'{g["title"]} — MaintenanceIQ', g["desc"], body, ld, og_type="article", lang="en", alt=f"/fiches/{g['fr']}/")

MBY_EN = {m["slug"]: m for m in METHODS_EN}
for m in METHODS_EN:
    secs = "".join(f"<h2>{h}</h2>{c}" for h, c in m["sections"])
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in m["faq"])
    fl = "".join(f'<li><a href="/en/guides/{x}/">{G_BY[x]["h1"]}</a></li>' for x in m["fiches"] if x in G_BY)
    others = "".join(f'<li><a href="/en/methods/{o["slug"]}/">{o["h1"]}</a></li>' for o in METHODS_EN if o["slug"] != m["slug"])
    body = f'''<p class="muted"><a href="/en/">Home</a> › <a href="/en/methods/">Maintenance methods</a></p>
<h1>{m["h1"]}</h1>
<p class="muted"><span class="niv {NIV_CLASS[m["niveau"]]}">Level: {m["niveau"]}</span> Maintenance method · by <a href="/en/about/">SAHALI</a>, MaintenanceIQ</p>
<p>{m["intro"]}</p>
{secs}
<h2>Frequently asked questions</h2>
{faq_html}
<div class="card"><strong>Put it into practice</strong><br>Use the <a href="/en/downtime-cost-calculator/">downtime cost calculator</a> or ask for the <a href="/en/#offers">free 30-day pilot</a>: we set the method up with you, remotely.</div>
<h2>Related troubleshooting guides</h2><ul>{fl}</ul>
<h2>Other methods</h2><ul>{others}</ul>'''
    url = SITE + f"/en/methods/{m['slug']}/"
    ld = [ORG, {"@type": "Article", "headline": m["h1"], "description": m["desc"], "dateModified": TODAY, "datePublished": "2026-11-22",
                "inLanguage": "en", "author": {"@type": "Person", "name": "SAHALI", "url": SITE + "/en/about/"},
                "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": url, "image": SITE + "/og-image.png"},
          {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in m["faq"]]},
          crumbs([("Home", "/en/"), ("Maintenance methods", "/en/methods/"), (m["h1"], f"/en/methods/{m['slug']}/")])]
    page(f"/en/methods/{m['slug']}/", f'{m["title"]} — MaintenanceIQ', m["desc"], body, ld, og_type="article", lang="en", alt=f"/methodes/{m['fr']}/")

page("/en/guides/", "Machine troubleshooting guides — MaintenanceIQ",
     "Practical troubleshooting guides for pumps, motors, bearings, generators, compressors, HVAC and more: warning signs, causes, checks and fixes.",
     f'''<p class="muted"><a href="/en/">Home</a> › Troubleshooting guides</p>
<h1>Troubleshooting guides</h1>
<p>One guide per real-world problem, from simple to complex: warning signs, likely causes and how to check them, then what to do before failure. Levels: <span class="niv n1">Simple</span> <span class="niv n2">Intermediate</span> <span class="niv n3">Advanced</span>. New guides are added every week; more are available <a href="/fiches/" hreflang="fr">in French</a>.</p>
<ul>{"".join(f'<li><a href="/en/guides/{g["slug"]}/"><strong>{g["h1"]}</strong></a> <span class="niv {NIV_CLASS[g["niveau"]]}">{g["niveau"]}</span><br><span class="muted">{g["desc"]}</span></li>' for g in GUIDES_EN)}</ul>''',
     [ORG, {"@type": "CollectionPage", "name": "MaintenanceIQ troubleshooting guides", "url": SITE + "/en/guides/", "inLanguage": "en"},
      crumbs([("Home", "/en/"), ("Troubleshooting guides", "/en/guides/")])], lang="en", alt="/fiches/")

page("/en/methods/", "Maintenance methods explained — MaintenanceIQ",
     "Types of maintenance, P-F curve, machine criticality, MTBF and MTTR, root cause analysis: maintenance methods explained with worked examples.",
     f'''<p class="muted"><a href="/en/">Home</a> › Maintenance methods</p>
<h1>Maintenance methods</h1>
<p>Troubleshooting guides fix a problem; methods organise maintenance so it does not come back. From basic to advanced, with worked examples. More methods are available <a href="/methodes/" hreflang="fr">in French</a>.</p>
<ul>{"".join(f'<li><a href="/en/methods/{m["slug"]}/"><strong>{m["h1"]}</strong></a> <span class="niv {NIV_CLASS[m["niveau"]]}">{m["niveau"]}</span><br><span class="muted">{m["desc"]}</span></li>' for m in METHODS_EN)}</ul>''',
     [ORG, {"@type": "CollectionPage", "name": "Maintenance methods", "url": SITE + "/en/methods/", "inLanguage": "en"},
      crumbs([("Home", "/en/"), ("Maintenance methods", "/en/methods/")])], lang="en", alt="/methodes/")

page("/en/about/", "About MaintenanceIQ — SAHALI",
     "MaintenanceIQ was created by SAHALI, trained in industrial maintenance, to help small sites and buildings diagnose failures early, by phone, worldwide.",
     '''<p class="muted"><a href="/en/">Home</a> › About</p>
<h1>About MaintenanceIQ</h1><p><img src="/avatar-sahali.svg" width="140" height="140" alt="Illustrated avatar of SAHALI, maintenance technician" style="display:block;border-radius:50%"></p>
<p>MaintenanceIQ is a brand of <strong>SAHALI</strong>, sole trader (trade name Atelier Calibre) based in France. It helps small industrial sites and buildings that have neither sensors nor maintenance software to spot failures early and act at the right time.</p>
<h2>Who is behind MaintenanceIQ</h2>
<p>SAHALI learned maintenance where failures cost money: on production lines. He worked as a machine operator on packaging lines in the food industry, then as an operator and fitter in the heavy-vehicle industry, before assembling refrigerated truck chassis.</p>
<ul><li>Industrial maintenance technician training (2024–2025).</li><li>Electrical clearance (French BR level).</li><li>First-level setting, operation and maintenance of industrial machines.</li><li>More than six years in industrial production.</li></ul>
<h2>The method</h2>
<p>Simple, public rules: start from what the operator sees, hears and feels, measure consistently, compare with the machine’s own baseline, and decide with a traffic-light code. Vibration readings are read against the ISO 10816 zones.</p>
<h2>What MaintenanceIQ does not do</h2>
<p>It does not see your machine, does not predict a failure date, does not connect to your equipment and does not replace an on-site technician or mandatory inspections.</p>
<h2>Contact</h2>
<p>E-mail: <a href="mailto:sahali.prof@gmail.com">sahali.prof@gmail.com</a> · WhatsApp: <a href="https://wa.me/33698711848">+33 6 98 71 18 48</a></p>''',
     [ORG, {"@type": "AboutPage", "url": SITE + "/en/about/", "about": {"@id": SITE + "/#org"}, "inLanguage": "en"},
      crumbs([("Home", "/en/"), ("About", "/en/about/")])], lang="en", alt="/a-propos/")

calc_en = '''<p class="muted"><a href="/en/">Home</a> › Downtime cost calculator</p>
<h1>Calculate the real cost of a breakdown</h1>
<p>Management does not fund “maintenance”: it funds avoided losses. Enter your own figures to estimate what an unplanned breakdown costs your site. The calculation runs on your device: nothing is sent.</p>
<form id="calc" class="card" onsubmit="return false" style="display:grid;gap:12px">
<label>Hours of lost production<br><input id="h" type="number" inputmode="decimal" min="0" step="any" value="72"></label>
<label>Margin lost per hour of downtime<br><input id="m" type="number" inputmode="decimal" min="0" step="any" value="125"></label>
<label>Labour hours (waiting and repair)<br><input id="mo" type="number" inputmode="decimal" min="0" step="any" value="20"></label>
<label>Hourly labour cost<br><input id="t" type="number" inputmode="decimal" min="0" step="any" value="35"></label>
<label>Emergency parts and express shipping<br><input id="p" type="number" inputmode="decimal" min="0" step="any" value="1800"></label>
<label>Knock-on costs: lost product, penalties, overtime, rentals<br><input id="c" type="number" inputmode="decimal" min="0" step="any" value="1200"></label>
<p style="margin:0;font-size:20px">Estimated cost of the breakdown: <strong id="tot">–</strong></p>
<p class="muted" id="det" style="margin:0"></p>
</form>
<p>Starting values are illustrative assumptions in your own currency. Replace them with yours.</p>
<h2>The formula</h2>
<p><strong>Breakdown cost</strong> = lost production (downtime hours × margin lost per hour) + labour (waiting, repair, overtime) + parts (emergency prices, express transport) + knock-on costs (lost product, late penalties, lost customers, backup equipment rental).</p>
<h2>Why remote sites pay more</h2>
<p>On islands, in remote regions or far from suppliers, the missing part often arrives by air or sea. Every day of waiting adds downtime. The same defect spotted a few weeks earlier (noise, heat, vibration) lets you order the part normally and replace it during a planned stop.</p>
<div class="card"><strong>Reduce this cost</strong><br>Read the <a href="/en/guides/">troubleshooting guides</a> or ask for the <a href="/en/#offers">free 30-day pilot</a>.<br>
<a class="btn" href="https://wa.me/33698711848" target="_blank" rel="noopener">Talk about your machines on WhatsApp</a></div>
<script>(function(){var $=function(i){return document.getElementById(i)};var f=new Intl.NumberFormat("en-GB",{maximumFractionDigits:0});
function v(i){var x=parseFloat($(i).value);return isFinite(x)&&x>0?x:0}
function r(){var prod=v("h")*v("m"),mo=v("mo")*v("t"),p=v("p"),c=v("c");$("tot").textContent=f.format(prod+mo+p+c);
$("det").textContent="Lost production "+f.format(prod)+" · labour "+f.format(mo)+" · parts "+f.format(p)+" · knock-on costs "+f.format(c)}
$("calc").addEventListener("input",r);r()})()</script>'''
page("/en/downtime-cost-calculator/", "Downtime cost calculator — MaintenanceIQ",
     "Free calculator for the real cost of a machine breakdown: lost production, labour, emergency parts and knock-on costs. Works in any currency.",
     calc_en,
     [ORG, {"@type": "WebApplication", "name": "Downtime cost calculator", "url": SITE + "/en/downtime-cost-calculator/",
            "applicationCategory": "BusinessApplication", "operatingSystem": "Any browser", "inLanguage": "en",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "provider": {"@id": SITE + "/#org"}},
      crumbs([("Home", "/en/"), ("Downtime cost calculator", "/en/downtime-cost-calculator/")])], lang="en", alt="/calculateur-cout-panne/")

pilot_msg = urllib.parse.quote("Hello MaintenanceIQ,\n\nI would like the free 30-day pilot.\nCompany:\nCountry:\nNumber of machines:\n\nThank you.")
home_en = f'''<h1>Fix machine problems before they stop your business</h1>
<p style="font-size:19px">Practical maintenance for small industrial sites and buildings, worldwide: from a whistling bearing to a vibration spectrum, from the AC that no longer cools to your preventive maintenance plan. No sensors, no software to install: everything works from a phone.</p>
<p><a class="btn" href="/en/guides/">Troubleshooting guides</a> <a class="btn" href="#offers" style="background:none;color:var(--ink);border:2px solid var(--ink)">Free 30-day pilot</a></p>
<h2>Solve a problem now</h2>
<ul>{"".join(f'<li><a href="/en/guides/{g["slug"]}/">{g["h1"]}</a> <span class="niv {NIV_CLASS[g["niveau"]]}">{g["niveau"]}</span></li>' for g in GUIDES_EN)}</ul>
<p><a href="/en/guides/">All troubleshooting guides</a></p>
<h2>Organise your maintenance</h2>
<ul>{"".join(f'<li><a href="/en/methods/{m["slug"]}/">{m["h1"]}</a></li>' for m in METHODS_EN)}</ul>
<p><a href="/en/downtime-cost-calculator/">Downtime cost calculator</a> · <a href="/en/methods/">All methods</a></p>
<h2 id="offers">Offers</h2>
<p>All plans are monthly, with no commitment, cancel by e-mail. Follow-up is remote, by WhatsApp or e-mail, from any country. Prices in euros; your bank converts automatically.</p>
<div class="tw"><table><thead><tr><th>Plan</th><th>Machines</th><th>Price</th><th></th></tr></thead><tbody>
<tr><td><strong>Pilot</strong></td><td>5</td><td>Free for 30 days</td><td><a href="https://wa.me/33698711848?text={pilot_msg}" target="_blank" rel="noopener">Request</a></td></tr>
<tr><td><strong>Essential</strong></td><td>up to 10</td><td>€45 / month</td><td><a href="https://buy.stripe.com/7sY00kcgFfJLcLdenhgfu00" target="_blank" rel="noopener">Subscribe</a></td></tr>
<tr><td><strong>Pro</strong></td><td>up to 30</td><td>€70 / month</td><td><a href="https://buy.stripe.com/7sYbJ2eoN1SVdPhgvpgfu01" target="_blank" rel="noopener">Subscribe</a></td></tr>
<tr><td><strong>Enterprise</strong></td><td>up to 60</td><td>€120 / month</td><td><a href="https://buy.stripe.com/5kQ9AU5Sh9ln4eHfrlgfu03" target="_blank" rel="noopener">Subscribe</a></td></tr>
</tbody></table></div>
<p>After subscribing, send the list of your machines to <a href="mailto:sahali.prof@gmail.com">sahali.prof@gmail.com</a>: follow-up starts within 2 working days. You send your readings and observations; we keep each machine’s history and send you a monthly summary. Terms of sale and legal notice are in French.</p>
<div class="card"><strong>Free 30-day pilot</strong><br>5 machines followed with you, remotely. No payment required.<br>
<a class="btn" href="https://wa.me/33698711848?text={pilot_msg}" target="_blank" rel="noopener">Request the pilot on WhatsApp</a><br>
<span class="muted">Or by e-mail: <a href="mailto:sahali.prof@gmail.com">sahali.prof@gmail.com</a> · WhatsApp +33 6 98 71 18 48</span></div>
<h2>What MaintenanceIQ does not do</h2>
<p>It does not see your machine, does not predict a failure date, does not connect to your equipment and does not replace an on-site technician or mandatory inspections.</p>'''
page("/en/", "MaintenanceIQ — machine troubleshooting and maintenance",
     "Practical troubleshooting guides and maintenance methods for industrial sites and buildings, from simple to complex, plus a free 30-day remote pilot.",
     home_en,
     [ORG, {"@type": "WebSite", "@id": SITE + "/en/#site", "url": SITE + "/en/", "name": "MaintenanceIQ", "inLanguage": "en", "publisher": {"@id": SITE + "/#org"}},
      {"@type": "Service", "name": "Remote condition-based maintenance follow-up", "provider": {"@id": SITE + "/#org"}, "areaServed": "Worldwide",
       "hasOfferCatalog": {"@type": "OfferCatalog", "name": "MaintenanceIQ plans", "itemListElement": [
        {"@type": "Offer", "name": "Pilot (5 machines, 30 days)", "price": "0", "priceCurrency": "EUR"},
        {"@type": "Offer", "name": "Essential", "price": "45", "priceCurrency": "EUR"},
        {"@type": "Offer", "name": "Pro", "price": "70", "priceCurrency": "EUR"},
        {"@type": "Offer", "name": "Enterprise", "price": "120", "priceCurrency": "EUR"}]}}],
     lang="en", alt="/")

# ---------- Flux RSS (FR et EN) ----------
from email.utils import format_datetime
import datetime, html as _h
def rss(path, title, desc, lang, items):
    def d(x): return format_datetime(datetime.datetime.fromisoformat(x).replace(tzinfo=datetime.timezone.utc))
    items = sorted(items, key=lambda i: i[3], reverse=True)
    x = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
         f'<title>{_h.escape(title)}</title><link>{SITE}{"/en/" if lang=="en" else "/"}</link><description>{_h.escape(desc)}</description><language>{lang}</language>'
         + "".join(f'<item><title>{_h.escape(t)}</title><link>{SITE}{u}</link><guid>{SITE}{u}</guid><description>{_h.escape(ds)}</description><pubDate>{d(dt)}</pubDate></item>' for t, u, ds, dt in items)
         + "</channel></rss>\n")
    os.makedirs(os.path.join(ROOT, os.path.dirname(path.strip("/"))) or ROOT, exist_ok=True)
    open(os.path.join(ROOT, path.strip("/")), "w").write(x)
rss("/feed.xml", "MaintenanceIQ — fiches terrain et méthodes", "Dépannage et méthodes de maintenance, du simple au complexe.", "fr",
    [(f["h1"], f"/fiches/{f['slug']}/", f["desc"], f["date"]) for f in FICHES] + [(m["h1"], f"/methodes/{m['slug']}/", m["desc"], m.get("date", "2026-11-22")) for m in METHODES])
rss("/en/feed.xml", "MaintenanceIQ — troubleshooting guides and methods", "Practical maintenance troubleshooting and methods.", "en",
    [(g["h1"], f"/en/guides/{g['slug']}/", g["desc"], g.get("date", FICHES_BY_SLUG.get(g["fr"], {}).get("date", "2026-11-22"))) for g in GUIDES_EN] + [(m["h1"], f"/en/methods/{m['slug']}/", m["desc"], m.get("date", "2026-11-22")) for m in METHODS_EN])

# ---------- Calculateurs et modèles à imprimer ----------
import html as _html
def field_html(fd):
    if isinstance(fd[2], list):
        opts = "".join(f'<option value="{a}">{b}</option>' for a, b in fd[2])
        return f'<label>{fd[1]}<br><select id="{fd[0]}" style="width:100%;margin-top:4px;padding:10px;font:500 17px var(--body);border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--ink)">{opts}</select></label>'
    return f'<label>{fd[1]}<br><input id="{fd[0]}" type="number" inputmode="decimal" step="{fd[3]}" value="{fd[2]}"></label>'
for c in CALCS:
    ids = [fd[0] for fd in c["fields"]]
    js = ('<script>(function(){var ids=' + json.dumps(ids) + ';var f=function(n,d){return new Intl.NumberFormat("fr-FR",{maximumFractionDigits:d,minimumFractionDigits:0}).format(n)};'
          'function run(){var v={};ids.forEach(function(i){var x=parseFloat(String(document.getElementById(i).value).replace(",","."));v[i]=isNaN(x)?0:x});'
          'var out;try{out=(function(v,f){' + c["js"] + '})(v,f)}catch(e){out="Vérifiez les valeurs saisies."}document.getElementById("out").innerHTML=out}'
          'ids.forEach(function(i){var el=document.getElementById(i);el.addEventListener("input",run);el.addEventListener("change",run)});run()})()</script>')
    others = "".join(f'<li><a href="/calculateurs/{o["slug"]}/">{o["h1"]}</a></li>' for o in CALCS if o["slug"] != c["slug"])
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in c["faq"])
    body = f"""<p class="muted"><a href="/">Accueil</a> › <a href="/calculateurs/">Outils gratuits</a></p>
<h1>{c["h1"]}</h1>
<p>{c["intro"]}</p>
<form class="card" onsubmit="return false" style="display:grid;gap:12px">{"".join(field_html(fd) for fd in c["fields"])}</form>
<div class="card" id="out" aria-live="polite"></div>
<h2>La formule</h2><p class="formule">{c["formule"]}</p>
<h2>Exemple chiffré</h2><p>{c["exemple"]}</p>
<h2>Questions fréquentes</h2>{faq_html}
<p class="muted">Résultat indicatif, calculé sur votre téléphone : rien n’est envoyé. La notice du constructeur et les règles de votre site passent avant.</p>
<h2>Autres outils gratuits</h2><ul>{others}<li><a href="/calculateur-cout-panne/">Calculer le coût d’une panne</a></li></ul>{js}"""
    url = SITE + f"/calculateurs/{c['slug']}/"
    ld = [ORG, {"@type": "WebApplication", "name": c["title"], "url": url, "applicationCategory": "UtilitiesApplication", "operatingSystem": "Tous", "inLanguage": "fr",
                "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "publisher": {"@id": SITE + "/#org"}},
          {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c["faq"]]},
          crumbs([("Accueil", "/"), ("Outils gratuits", "/calculateurs/"), (c["title"], f"/calculateurs/{c['slug']}/")])]
    page(f"/calculateurs/{c['slug']}/", f'{c["title"]} — MaintenanceIQ', c["desc"], body, ld)

for m in MODELES:
    head = "".join(f"<th>{h}</th>" for h in m["head"])
    rows = "".join("<tr>" + "".join(f"<td>{x}</td>" for x in r) + "".join("<td>&nbsp;</td>" for _ in range(len(m["head"]) - len(r))) + "</tr>" for r in m["rows"])
    body = f"""<p class="muted noprint"><a href="/">Accueil</a> › <a href="/calculateurs/">Outils gratuits</a></p>
<h1>{m["h1"]}</h1>
<p class="noprint">{m["intro"]}</p>
<p class="noprint"><button class="btn" onclick="window.print()" style="border:0;cursor:pointer;font-size:17px">Imprimer ou enregistrer en PDF</button></p>
<p class="printonly">Machine : ............................................ Semaine / date : ....................... Nom : ...........................</p>
<div class="tw"><table class="modele"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>
<p class="muted">Modèle gratuit MaintenanceIQ · maintenanceiq.fr · Sécurité : aucune intervention sans consignation.</p>"""
    url = SITE + f"/modeles/{m['slug']}/"
    ld = [ORG, {"@type": "DigitalDocument", "name": m["title"], "url": url, "inLanguage": "fr", "isAccessibleForFree": True, "publisher": {"@id": SITE + "/#org"}},
          crumbs([("Accueil", "/"), ("Outils gratuits", "/calculateurs/"), (m["title"], f"/modeles/{m['slug']}/")])]
    page(f"/modeles/{m['slug']}/", f'{m["title"]} — MaintenanceIQ', m["desc"], body, ld)

hub = ('<p class="muted"><a href="/">Accueil</a> › Outils gratuits</p><h1>Outils gratuits pour la maintenance</h1>'
       '<p>Des calculateurs qui font une seule chose, avec leur formule et un exemple chiffré, et des modèles à imprimer. Gratuits, sans inscription : tout se calcule sur votre téléphone.</p>'
       '<h2>Calculateurs</h2><ul><li><a href="/calculateur-cout-panne/"><strong>Calculer le coût d’une panne</strong></a><br><span class="muted">Production perdue, main-d’œuvre, pièces en urgence : ce que coûte vraiment un arrêt.</span></li>'
       + "".join(f'<li><a href="/calculateurs/{c["slug"]}/"><strong>{c["h1"]}</strong></a><br><span class="muted">{c["desc"]}</span></li>' for c in CALCS) + '</ul>'
       '<h2>Fiche de révision</h2><ul><li><a href="/qcm-habilitation-electrique/"><strong>QCM habilitation électrique : examen blanc corrigé</strong></a><br><span class="muted">Questions tirées au hasard, score, correction à imprimer.</span></li><li><a href="/habilitation-electrique/"><strong>Habilitation électrique : tous les symboles + quiz</strong></a><br><span class="muted">B0, BR, BS, BC, B1V, B2V, H0V, BP, BF-HF, véhicules en L, rangés par thème.</span></li></ul>'
       '<h2>Modèles à imprimer</h2><ul>' + "".join(f'<li><a href="/modeles/{m["slug"]}/"><strong>{m["h1"]}</strong></a><br><span class="muted">{m["desc"]}</span></li>' for m in MODELES) + '</ul>'
       '<div class="card">Un outil vous manque ? Écrivez-nous sur <a href="https://wa.me/33698711848">WhatsApp</a> : les demandes les plus fréquentes sont ajoutées en priorité.</div>')
page("/calculateurs/", "Outils gratuits de maintenance : calculateurs et modèles — MaintenanceIQ",
     "Calculateurs gratuits de maintenance (intensité moteur, chute de tension, MTBF, graissage, AMDEC, courroie, pression) et modèles à imprimer.", hub,
     [ORG, {"@type": "CollectionPage", "name": "Outils gratuits de maintenance", "url": SITE + "/calculateurs/", "inLanguage": "fr"}, crumbs([("Accueil", "/"), ("Outils gratuits", "/calculateurs/")])])


# ---------- Habilitations électriques ----------
def quiz_html(Q):
    qz = ""
    for k, (q, opts, ok, ex) in enumerate(Q):
        bt = "".join(f'<button type="button" class="qopt" data-q="{k}" data-i="{j}" data-ok="{1 if j==ok else 0}">{o}</button>' for j, o in enumerate(opts))
        qz += f'<div class="card quiz" id="q{k}"><p><strong>{k+1}. {q}</strong></p><div class="qopts">{bt}</div><p class="qex" hidden><span class="qv"></span> {ex}</p></div>'
    corr = "".join(f"<li><strong>{q}</strong><br>Réponse : {opts[ok]}. {ex}</li>" for q, opts, ok, ex in Q)
    js = ('<script>(function(){var done={},score=0,n=' + str(len(Q)) + ';document.querySelectorAll(".qopt").forEach(function(b){b.addEventListener("click",function(){var q=b.dataset.q;if(done[q])return;done[q]=1;'
          'var box=document.getElementById("q"+q);box.querySelectorAll(".qopt").forEach(function(o){o.disabled=true;if(o.dataset.ok==="1")o.classList.add("bon")});'
          'if(b.dataset.ok==="1"){score++;box.querySelector(".qv").textContent="Bonne réponse."}else{b.classList.add("faux");box.querySelector(".qv").textContent="Pas tout à fait."}'
          'box.querySelector(".qex").hidden=false;var c=Object.keys(done).length;document.getElementById("score").textContent="Score : "+score+" / "+c+(c===n?(score===n?" — sans faute !":" — questionnaire terminé. Relisez la correction ci-dessous."):"")})})})()</script>')
    return (f'<p>Touchez une réponse : la bonne s’affiche avec l’explication.</p><p class="card" id="score" aria-live="polite">Score : 0 / 0</p>{qz}'
            f'<details class="card"><summary><strong>Voir toute la correction ({len(Q)} questions)</strong></summary><ol>{corr}</ol></details>{js}')

def SHORT(x):
    return {"travaux-sous-tension": "Travaux sous tension (T, N)"}.get(x["slug"], x["sym"])
def H1(x):
    return {"travaux-sous-tension": "Habilitation travaux sous tension : B1T, B2T, H1T, H2T et nettoyage N"}.get(x["slug"], "Habilitation électrique " + x["sym"])
def _redirects():
    for old, new in REDIRECTS.items():
        d = os.path.join(ROOT, "habilitation-electrique", old); os.makedirs(d, exist_ok=True)
        u = f"{SITE}/habilitation-electrique/{new}/"
        open(os.path.join(d, "index.html"), "w").write(f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><meta name="robots" content="noindex"><link rel="canonical" href="{u}"><meta http-equiv="refresh" content="0; url={u}"><title>Page déplacée</title></head><body><p>Cette page a déménagé : <a href="{u}">{u}</a></p></body></html>')
_redirects()

def _hab():
    import html as H
    SLUG_OF = {"B0":"b0","B0 Chargé de chantier":"b0","H0":"h0","H0V":"h0v","BF-HF":"bf-hf","B1":"b1","B1V":"b1v","B2":"b2","B2V":"b2v","B2V Essai":"b2v-essai",
               "H1 / H1V":"h1v","H2 / H2V":"h2v","H2V Essai":"h2v","BC":"bc","HC":"hc","BR":"br","BS":"bs","BE Manœuvre / HE Manœuvre":"be-manoeuvre",
               "BE Mesurage / HE Mesurage":"be-mesurage","BE Vérification / HE Vérification":"be-verification","BE Essai / HE Essai":"be-essai","BP":"bp",
               "T (B1T, B2T, H1T, H2T…)":"travaux-sous-tension","N":"travaux-sous-tension",
               "B0L":"b0l","B1L / B1VL":"b1vl","B2L / B2VL":"b2vl","BCL":"bcl","BEL / BRL":"brl","B1XL / B2XL":"b1xl-b2xl"}
    for k, v in SLUG_OF.items():
        assert v in {x["slug"] for x in SYMBOLES}, (k, v)
    lk = lambda s: f'<a href="/habilitation-electrique/{SLUG_OF[s]}/">{s}</a>' if s in SLUG_OF else s
    lect = "".join(f"<li><strong>{a}</strong> — {b}</li>" for a, b in LECTURE)
    toc = "".join(f'<li><a href="#t{i}">{t[0]}</a></li>' for i, t in enumerate(THEMES))
    secs = ""
    for i, (titre, intro, rows) in enumerate(THEMES):
        tr = "".join(f"<tr><td><strong>{lk(s)}</strong></td><td>{n}</td><td>{d}</td></tr>" for s, n, d in rows)
        secs += f'<h2 id="t{i}">{titre}</h2><p>{intro}</p><div class="tw"><table><thead><tr><th>Symbole</th><th>Qui</th><th>Ce qu’il autorise</th></tr></thead><tbody>{tr}</tbody></table></div>'
    faq = [(q, opts[ok] + ". " + ex) for q, opts, ok, ex in QUIZ]
    _gs = []
    for x in SYMBOLES:
        if x["groupe"] not in _gs: _gs.append(x["groupe"])
    PAR_GROUPE = "<ul>" + "".join("<li><strong>" + g + " :</strong> " + " · ".join(f'<a href="/habilitation-electrique/{x["slug"]}/">{SHORT(x)}</a>' for x in SYMBOLES if x["groupe"] == g) + "</li>" for g in _gs) + "</ul>"
    body = f"""<p class="muted"><a href="/">Accueil</a> › <a href="/methodes/">Méthodes</a> › Habilitations électriques</p>
<h1>Habilitation électrique : tous les symboles expliqués, par thème</h1>
<p>B0, H0V, B1V, B2V, BR, BS, BC, BE Manœuvre, BP, BF-HF, B1L… Chaque symbole dit précisément ce qu’une personne a le droit de faire sur ou près d’une installation électrique. Voici la liste complète, rangée par thème, puis un questionnaire de 12 questions avec les réponses pour vérifier que tout est clair.</p>
<div class="card"><strong>Rappel essentiel.</strong> L’habilitation n’est pas un diplôme : c’est l’<strong>employeur</strong> qui la délivre par écrit, après une formation adaptée et un avis favorable. Elle ne vaut que pour les opérations inscrites sur le titre, et se recycle en général tous les 3 ans.</div>
<h2>Comment lire un symbole</h2><ul>{lect}</ul>
<p>Exemple : <strong>B2V Essai</strong> = basse tension (B), chargé de travaux (2), au voisinage (V), autorisé à faire des essais (attribut).</p>
<div class="card"><strong>Examen blanc :</strong> <a href="/qcm-habilitation-electrique/">QCM habilitation électrique gratuit, questions tirées au hasard, score et correction PDF</a>.</div>
<h2>Une page par symbole</h2>{PAR_GROUPE}
<h2>Sommaire par thème</h2><ul>{toc}<li><a href="#quiz">Questionnaire avec réponses</a></li></ul>
{secs}
<h2>Quel symbole pour quel métier ?</h2><div class="tw"><table><thead><tr><th>Métier</th><th>Symbole le plus courant</th></tr></thead><tbody>
<tr><td>Peintre, agent d’entretien, maçon en local électrique</td><td>B0 (H0 / H0V en haute tension)</td></tr>
<tr><td>Technicien ou agent de maintenance industrielle</td><td>BR, souvent avec B1V / B2V et BC</td></tr>
<tr><td>Électricien de chantier</td><td>B1V (exécutant) ou B2V (chef d’équipe)</td></tr>
<tr><td>Opérateur de production qui réarme et redémarre</td><td>BE Manœuvre</td></tr>
<tr><td>Installateur photovoltaïque</td><td>BP, avec B1V / B2V côté réseau</td></tr>
<tr><td>Terrassier près de réseaux enterrés</td><td>BF-HF</td></tr>
<tr><td>Mécanicien automobile sur véhicule électrique ou hybride</td><td>B0L, puis B1VL / B2VL / BCL selon les tâches</td></tr>
</tbody></table></div>
<h2 id="quiz">Questionnaire : testez-vous (12 questions)</h2>
{quiz_html(QUIZ)}
<p class="muted">Page d’information. Seuls la norme NF C 18-510 (et NF C 18-550 pour les véhicules), votre formation et le titre délivré par votre employeur font foi. Sources : INRS (brochure ED 6127 et dossier Risques électriques).</p>
<h2>Pour aller plus loin</h2><ul><li><a href="/methodes/">Les méthodes de maintenance</a></li><li><a href="/fiches/armoire-electrique-connexion-qui-chauffe/">Armoire électrique : connexion qui chauffe</a></li><li><a href="/calculateurs/intensite-moteur-triphase/">Calculer l’intensité d’un moteur triphasé</a></li><li><a href="/glossaire/">Glossaire</a></li></ul>"""
    url = SITE + "/habilitation-electrique/"
    ld = [ORG, {"@type": "TechArticle", "headline": "Habilitation électrique : tous les symboles expliqués, par thème", "url": url, "inLanguage": "fr",
                "author": {"@type": "Person", "name": "Abourare Sahali"}, "publisher": {"@id": SITE + "/#org"}, "datePublished": "2026-11-24", "dateModified": "2026-11-24", "image": SITE + "/og-image.png"},
          {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
          crumbs([("Accueil", "/"), ("Méthodes", "/methodes/"), ("Habilitations électriques", "/habilitation-electrique/")])]

    BY = {x["slug"]: x for x in SYMBOLES}
    for x in SYMBOLES:
        u = f"/habilitation-electrique/{x['slug']}/"
        short = SHORT(x)
        li = lambda L: "".join(f"<li>{i}</li>" for i in L)
        vois = "".join(f'<li><a href="/habilitation-electrique/{v}/">Habilitation {SHORT(BY[v])}</a> — {BY[v]["nom"]}</li>' for v in x["voisins"])
        meme = " · ".join(f'<a href="/habilitation-electrique/{y["slug"]}/">{SHORT(y)}</a>' for y in SYMBOLES if y["groupe"] == x["groupe"] and y["slug"] != x["slug"])
        faqh = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in x["faq"])
        sb = f"""<p class="muted"><a href="/">Accueil</a> › <a href="/habilitation-electrique/">Habilitations électriques</a> › {short}</p>
<h1>{H1(x)}</h1>
<p class="muted">{x["nom"]}</p>
<p>{x["resume"]}</p>
<h2>Pour qui ?</h2><ul>{li(x["qui"])}</ul>
<h2>Ce que {short} autorise</h2><ul>{li(x["oui"])}</ul>
<h2>Ce que {short} n’autorise pas</h2><ul>{li(x["non"])}</ul>
<h2>Exemple sur le terrain</h2><div class="card cas">{x["exemple"]}</div>
<h2>Formation et recyclage</h2><div class="tw"><table><tbody><tr><td>Formation initiale</td><td>{x["form"][0]}</td></tr><tr><td>Recyclage recommandé</td><td>{x["form"][1]}</td></tr><tr><td>Qui délivre le titre</td><td>L’employeur, après la formation et l’avis du formateur</td></tr></tbody></table></div>
<p class="muted">Durées couramment pratiquées par les organismes ; la norme ne donne que des valeurs recommandées.</p>
<h2 id="quiz">Questionnaire {short} : testez-vous ({len(QZ[x["slug"]])} questions)</h2>
{quiz_html(QZ[x["slug"]])}
<h2>Questions fréquentes</h2>{faqh}
<div class="card"><strong>Examen blanc :</strong> <a href="/qcm-habilitation-electrique/">le QCM complet, tous symboles mélangés, avec score et correction PDF</a>. Les autres symboles : <a href="/habilitation-electrique/">la liste complète par thème</a> et <a href="/habilitation-electrique/#quiz">le questionnaire général de 12 questions</a>.</div>
<h2>Symboles proches</h2><ul>{vois}</ul>
{('<p><strong>Même thème (' + x["groupe"] + ') :</strong> ' + meme + '</p>') if meme else ''}
<p class="muted">Page d’information. Seuls la norme NF C 18-510 (NF C 18-550 pour les véhicules), votre formation et le titre délivré par votre employeur font foi.</p>"""
        sld = [ORG, {"@type": "TechArticle", "headline": H1(x), "description": x["resume"], "url": SITE + u, "inLanguage": "fr",
                    "author": {"@type": "Person", "name": "Abourare Sahali"}, "publisher": {"@id": SITE + "/#org"}, "datePublished": "2026-11-24", "dateModified": "2026-11-24", "image": SITE + "/og-image.png"},
              {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in x["faq"]]},
              crumbs([("Accueil", "/"), ("Habilitations électriques", "/habilitation-electrique/"), (short, u)])]
        _t = "Habilitation travaux sous tension (T, N) : rôle, quiz" if x["slug"] == "travaux-sous-tension" else f"Habilitation {SHORT(x)} : rôle, formation et quiz"
        page(u, f"{_t} — MaintenanceIQ", x["resume"] + " Avec un questionnaire corrigé.", sb, sld, og_type="article")
    page("/habilitation-electrique/", "Habilitation électrique : tous les symboles par thème + quiz — MaintenanceIQ",
         "Tous les symboles d’habilitation électrique NF C 18-510 et NF C 18-550 rangés par thème, avec un questionnaire de 12 questions et les réponses.", body, ld, og_type="article")
_hab()

# ---------- QCM / examen blanc habilitation électrique ----------
def _qcm():
    SYM_NAME = {x["slug"]: SHORT(x) for x in SYMBOLES}
    bank = [{"t": "general", "q": q, "o": o, "a": a, "e": e} for q, o, a, e in QUIZ]
    seen = {b["q"] for b in bank}
    for sl, L in QZ.items():
        for q, o, a, e in L:
            if q not in seen:
                seen.add(q); bank.append({"t": sl, "q": q, "o": o, "a": a, "e": e})
    opts = '<option value="all">Tous les symboles (' + str(len(bank)) + ' questions)</option>' + "".join(f'<option value="{sl}">{SYM_NAME[sl]} ({sum(1 for b in bank if b["t"] == sl)} questions)</option>' for sl in QZ)
    app = r'''<div id="qcm-setup" class="card" style="display:grid;gap:12px">
<label>Thème<br><select id="qt" style="width:100%;margin-top:4px;padding:10px;font:500 17px var(--body);border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--ink)">OPTS</select></label>
<label>Nombre de questions<br><select id="qn" style="width:100%;margin-top:4px;padding:10px;font:500 17px var(--body);border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--ink)"><option value="10">10 questions (5 min)</option><option value="20" selected>20 questions (10 min)</option><option value="40">40 questions (20 min)</option><option value="999">Toutes les questions du thème</option></select></label>
<button class="btn" id="qgo" type="button" style="border:0;cursor:pointer;font-size:17px">Commencer l’examen blanc</button>
<p class="muted" style="margin:0">Gratuit, sans inscription. Les questions sont tirées au hasard : chaque essai est différent.</p></div>
<div id="qcm-run" hidden><p class="card" id="qbar" aria-live="polite"></p><div id="qbox"></div>
<p><button class="btn" id="qend" type="button" style="border:0;cursor:pointer;font-size:17px">Terminer et voir la correction</button></p></div>
<div id="qcm-res" hidden></div>
<script>(function(){var B=BANK,S=SYMS,cur=[],ans={},t0=0,tm=null;
function $(i){return document.getElementById(i)}
function shuf(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var x=a[i];a[i]=a[j];a[j]=x}return a}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function bar(){var n=Object.keys(ans).length,s=Math.floor((Date.now()-t0)/1000);$("qbar").textContent="Répondu : "+n+" / "+cur.length+" · Temps : "+Math.floor(s/60)+" min "+("0"+s%60).slice(-2)+" s"}
$("qgo").onclick=function(){var t=$("qt").value,n=+$("qn").value;var pool=t==="all"?B:B.filter(function(x){return x.t===t});cur=shuf(pool).slice(0,n).map(function(x){var ix=shuf(x.o.map(function(_,i){return i}));return {t:x.t,q:x.q,e:x.e,o:ix.map(function(i){return x.o[i]}),a:ix.indexOf(x.a)}});ans={};
var h="";cur.forEach(function(x,k){h+='<div class="card quiz" id="r'+k+'"><p><strong>'+(k+1)+". "+esc(x.q)+'</strong></p><div class="qopts">'+x.o.map(function(o,j){return '<button type="button" class="qopt" data-k="'+k+'" data-j="'+j+'">'+esc(o)+"</button>"}).join("")+"</div></div>"});
$("qbox").innerHTML=h;$("qcm-setup").hidden=true;$("qcm-run").hidden=false;$("qcm-res").hidden=true;t0=Date.now();clearInterval(tm);tm=setInterval(bar,1000);bar();
document.querySelectorAll("#qbox .qopt").forEach(function(b){b.onclick=function(){var k=b.dataset.k;ans[k]=+b.dataset.j;document.querySelectorAll('#r'+k+' .qopt').forEach(function(o){o.classList.remove("sel")});b.classList.add("sel");bar()}});window.scrollTo(0,$("qcm-run").offsetTop-20)};
$("qend").onclick=function(){var n=cur.length,miss=n-Object.keys(ans).length;if(miss>0&&!confirm(miss+" question(s) sans réponse. Corriger quand même ?"))return;clearInterval(tm);
var ok=0,c="";cur.forEach(function(x,k){var g=ans[k]===x.a;if(g)ok++;c+='<li class="'+(g?"cok":"cko")+'"><strong>'+esc(x.q)+"</strong><br>"+(ans[k]===undefined?"Sans réponse":"Votre réponse : "+esc(x.o[ans[k]]))+(g?" ✔":" ✘")+"<br>Bonne réponse : <strong>"+esc(x.o[x.a])+"</strong>. "+esc(x.e)+(S[x.t]?' <a href="/habilitation-electrique/'+x.t+'/">Revoir '+esc(S[x.t])+"</a>":"")+"</li>"});
var p=Math.round(ok*100/n),s=Math.floor((Date.now()-t0)/1000),m=p>=80?"Objectif atteint : vous maîtrisez bien le sujet.":p>=60?"Pas mal, mais révisez les erreurs avant votre formation ou votre recyclage.":"À retravailler : relisez les pages des symboles concernés, puis refaites un essai.";
var txt="J’ai eu "+ok+"/"+n+" au QCM habilitation électrique de MaintenanceIQ. Et vous ?",u=encodeURIComponent(location.origin+location.pathname),e=encodeURIComponent(txt+" "+location.origin+location.pathname);
$("qcm-res").innerHTML='<div class="card"><p style="font-size:28px;margin:0"><strong>'+ok+" / "+n+"</strong> ("+p+" %)</p><p>"+m+'</p><p class="muted">Temps : '+Math.floor(s/60)+" min "+("0"+s%60).slice(-2)+' s · Objectif conseillé : 80 %</p>'+
'<p class="noprint"><button class="btn" type="button" onclick="window.print()" style="border:0;cursor:pointer;font-size:17px">Imprimer ou enregistrer le corrigé en PDF</button></p>'+
'<p class="noprint"><strong>Défiez vos collègues :</strong> <a href="https://wa.me/?text='+e+'" target="_blank" rel="noopener">WhatsApp</a> · <a href="https://www.linkedin.com/sharing/share-offsite/?url='+u+'" target="_blank" rel="noopener">LinkedIn</a> · <a href="https://www.facebook.com/sharer/sharer.php?u='+u+'" target="_blank" rel="noopener">Facebook</a></p>'+
'<p class="noprint"><button class="btn" type="button" id="qagain" style="border:0;cursor:pointer;font-size:17px;background:var(--ink)">Refaire un examen</button></p></div><h2>Correction détaillée</h2><ol class="corr">'+c+"</ol>";
$("qcm-run").hidden=true;$("qcm-res").hidden=false;$("qagain").onclick=function(){$("qcm-res").hidden=true;$("qcm-setup").hidden=false;window.scrollTo(0,0)};
try{var h=JSON.parse(localStorage.getItem("miq_qcm")||"[]");h.push({d:Date.now(),s:ok,n:n});localStorage.setItem("miq_qcm",JSON.stringify(h.slice(-20)))}catch(_){}
window.scrollTo(0,$("qcm-res").offsetTop-20)};
try{var h=JSON.parse(localStorage.getItem("miq_qcm")||"[]");if(h.length){var l=h[h.length-1];$("qcm-setup").insertAdjacentHTML("beforeend",'<p class="muted" style="margin:0">Votre dernier score sur cet appareil : '+l.s+" / "+l.n+" ("+h.length+" essai"+(h.length>1?"s":"")+").</p>")}}catch(_){}
})()</script>'''
    app = app.replace("OPTS", opts).replace("BANK", json.dumps(bank, ensure_ascii=False)).replace("SYMS", json.dumps(SYM_NAME, ensure_ascii=False))
    liens = " · ".join(f'<a href="/habilitation-electrique/{x["slug"]}/">{SHORT(x)}</a>' for x in SYMBOLES)
    body = f"""<p class="muted noprint"><a href="/">Accueil</a> › <a href="/habilitation-electrique/">Habilitations électriques</a> › QCM</p>
<h1>QCM habilitation électrique gratuit : examen blanc corrigé</h1>
<p class="noprint">{len(bank)} questions corrigées sur tous les symboles de la NF C 18-510 et de la NF C 18-550 : B0, H0V, BS, BE Manœuvre, BR, BC, B1V, B2V, BP, BF-HF, haute tension et véhicules électriques. Choisissez un symbole ou mélangez tout, répondez, puis obtenez votre score et la correction détaillée, à imprimer ou enregistrer en PDF.</p>
{app}
<div class="noprint"><h2>Réviser symbole par symbole</h2><p>{liens}</p>
<h2>Questions fréquentes</h2>
<h3>Ce QCM délivre-t-il une habilitation ?</h3><p>Non. C’est un entraînement gratuit. L’habilitation est délivrée par l’employeur après une formation par un organisme.</p>
<h3>Quel score viser ?</h3><p>Visez au moins 80 % avant une formation ou un recyclage, et relisez chaque erreur dans la correction.</p>
<h3>Mes réponses sont-elles envoyées quelque part ?</h3><p>Non. Le QCM fonctionne sur votre téléphone ; seul votre dernier score est gardé sur cet appareil.</p>
<div class="card">Formateur, organisme ou entreprise ? <a href="/qcm-habilitation-electrique/integrer/">Intégrez ce QCM gratuitement sur votre site</a>.</div></div>"""
    url = SITE + "/qcm-habilitation-electrique/"
    faq = [("Ce QCM délivre-t-il une habilitation ?", "Non. C’est un entraînement gratuit. L’habilitation est délivrée par l’employeur après une formation par un organisme."),
           ("Quel score viser ?", "Visez au moins 80 % avant une formation ou un recyclage, et relisez chaque erreur dans la correction."),
           ("Mes réponses sont-elles envoyées quelque part ?", "Non. Le QCM fonctionne sur votre téléphone ; seul votre dernier score est gardé sur cet appareil.")]
    ld = [ORG, {"@type": "WebApplication", "name": "QCM habilitation électrique gratuit", "url": url, "applicationCategory": "EducationalApplication", "operatingSystem": "Tous", "inLanguage": "fr",
                "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "publisher": {"@id": SITE + "/#org"}},
          {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
          crumbs([("Accueil", "/"), ("Habilitations électriques", "/habilitation-electrique/"), ("QCM", "/qcm-habilitation-electrique/")])]
    page("/qcm-habilitation-electrique/", "QCM habilitation électrique gratuit : examen blanc corrigé — MaintenanceIQ",
         f"Examen blanc gratuit d’habilitation électrique : {len(bank)} questions corrigées (B0, BS, BR, BC, B1V, B2V, H0V, BP, véhicules), score, correction PDF.", body, ld)
    # version intégrable (iframe) : page minimale, non indexée, lien retour
    css = open(os.path.join(ROOT, "assets/pages.css")).read() if False else ""
    emb = f"""<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>QCM habilitation électrique — MaintenanceIQ</title><link rel="canonical" href="{url}"><link rel="stylesheet" href="/assets/fonts.css"><link rel="stylesheet" href="/assets/pages.css">
<style>body{{margin:0;padding:12px;background:var(--bg,#fff)}}</style></head><body><main class="wrap">
<p><strong>QCM habilitation électrique</strong> · {len(bank)} questions corrigées</p>{app}
<p class="muted" style="text-align:center">QCM gratuit proposé par <a href="{url}" target="_blank" rel="noopener">MaintenanceIQ, QCM habilitation électrique</a></p></main></body></html>"""
    os.makedirs(os.path.join(ROOT, "embed/qcm-habilitation-electrique"), exist_ok=True)
    open(os.path.join(ROOT, "embed/qcm-habilitation-electrique/index.html"), "w").write(emb)
    code = _h.escape(f'<iframe src="{SITE}/embed/qcm-habilitation-electrique/" width="100%" height="900" style="border:0;max-width:760px" title="QCM habilitation électrique" loading="lazy"></iframe>\n<p><a href="{url}">QCM habilitation électrique gratuit</a> par MaintenanceIQ</p>')
    ib = f"""<p class="muted"><a href="/">Accueil</a> › <a href="/qcm-habilitation-electrique/">QCM habilitation électrique</a> › Intégrer</p>
<h1>Intégrez le QCM habilitation électrique sur votre site, gratuitement</h1>
<p>Organisme de formation, entreprise, lycée professionnel, CFA : proposez à vos stagiaires un examen blanc de {len(bank)} questions corrigées, directement sur votre site ou votre intranet. Gratuit, sans compte, sans publicité dans le module, mis à jour automatiquement.</p>
<h2>Le code à copier</h2><p>Collez ce code dans votre page (bloc HTML) :</p>
<pre style="white-space:pre-wrap;word-break:break-all;background:var(--bg);border:1px solid var(--line);padding:12px;border-radius:6px;font-size:14px">{code}</pre>
<h2>Aperçu</h2><iframe src="/embed/qcm-habilitation-electrique/" width="100%" height="700" style="border:1px solid var(--line);border-radius:8px" title="Aperçu du QCM" loading="lazy"></iframe>
<h2>Conditions</h2><ul><li>Usage gratuit, y compris en formation payante.</li><li>Merci de garder le lien « par MaintenanceIQ » sous le module.</li><li>Une question à corriger ou à ajouter ? Écrivez-nous sur <a href="https://wa.me/33698711848">WhatsApp</a>.</li></ul>"""
    page("/qcm-habilitation-electrique/integrer/", "Intégrer le QCM habilitation électrique sur votre site — MaintenanceIQ",
         "Code gratuit pour intégrer un examen blanc d’habilitation électrique corrigé sur le site d’un organisme de formation ou d’une entreprise.", ib,
         [ORG, crumbs([("Accueil", "/"), ("QCM habilitation électrique", "/qcm-habilitation-electrique/"), ("Intégrer", "/qcm-habilitation-electrique/integrer/")])])
    return len(bank)
NB_QCM = _qcm()

# ---------- sitemap et llms.txt ----------
urls = [("/", TODAY)] + [(f"/{t}/", TODAY) for t in ["mayotte","la-reunion","guadeloupe","martinique","guyane"]] + \
       [("/fiches/", TODAY)] + [(f"/fiches/{f['slug']}/", TODAY) for f in FICHES] + \
       [("/methodes/", TODAY)] + [(f"/methodes/{m['slug']}/", TODAY) for m in METHODES] + \
       [("/calculateur-cout-panne/", TODAY), ("/glossaire/", TODAY), ("/a-propos/", TODAY), ("/calculateurs/", TODAY), ("/habilitation-electrique/", TODAY), ("/qcm-habilitation-electrique/", TODAY), ("/qcm-habilitation-electrique/integrer/", TODAY)] + [(f"/habilitation-electrique/{x['slug']}/", TODAY) for x in SYMBOLES] + \
       [(f"/calculateurs/{c['slug']}/", TODAY) for c in CALCS] + [(f"/modeles/{m['slug']}/", TODAY) for m in MODELES] + \
       [("/en/", TODAY), ("/en/guides/", TODAY), ("/en/methods/", TODAY), ("/en/about/", TODAY), ("/en/downtime-cost-calculator/", TODAY)] + \
       [(f"/en/guides/{g['slug']}/", TODAY) for g in GUIDES_EN] + [(f"/en/methods/{m['slug']}/", TODAY) for m in METHODS_EN] + \
       [("/cgv/", "2026-11-20"), ("/mentions-legales/", "2026-11-20"), ("/confidentialite/", "2026-11-14")]
open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n")
L = ["# MaintenanceIQ", "",
 "> Practical maintenance for industrial sites and buildings, worldwide, in French and English: troubleshooting guides from simple to complex, maintenance methods, a downtime cost calculator, and a remote condition-based follow-up service (free 30-day pilot). Brand of SAHALI (sole trader, trade name Atelier Calibre, France).", "",
 "Offres / Plans : pilote gratuit 30 jours (5 machines) ; Essentiel 45 €/mois (10 machines) ; Pro 70 €/mois (30 machines) ; Entreprise 120 €/mois (60 machines), sans engagement, suivi à distance par WhatsApp ou e-mail dans tous les pays. Guide PDF « Diagnostiquer avant la panne » (37 pages, en français, 29 €) ; extrait gratuit : https://www.maintenanceiq.fr/ebook/extrait-diagnostiquer-avant-la-panne.pdf",
 "Ce que MaintenanceIQ ne fait pas : pas de capteurs, pas de connexion aux machines, pas de prédiction de date de panne, ne remplace pas un technicien sur place.",
 "Contact : sahali.prof@gmail.com · WhatsApp +33 6 98 71 18 48", "",
 "## Pages principales (FR)",
 "- [Accueil, diagnostic gratuit et offres](https://www.maintenanceiq.fr/)", "- [Fiches terrain](https://www.maintenanceiq.fr/fiches/)", "- [Méthodes de maintenance](https://www.maintenanceiq.fr/methodes/)",
 "- [Calculateur du coût d'une panne](https://www.maintenanceiq.fr/calculateur-cout-panne/)", "- [Glossaire](https://www.maintenanceiq.fr/glossaire/)", "- [À propos](https://www.maintenanceiq.fr/a-propos/)", "",
 "## English", "- [Home and plans](https://www.maintenanceiq.fr/en/)", "- [Troubleshooting guides](https://www.maintenanceiq.fr/en/guides/)", "- [Maintenance methods](https://www.maintenanceiq.fr/en/methods/)", "- [Downtime cost calculator](https://www.maintenanceiq.fr/en/downtime-cost-calculator/)", "- [About](https://www.maintenanceiq.fr/en/about/)", ""]
L += ["## Habilitations électriques (FR)", f"- [Tous les symboles d'habilitation électrique par thème, avec quiz]({SITE}/habilitation-electrique/)", f"- [QCM habilitation électrique gratuit, examen blanc corrigé]({SITE}/qcm-habilitation-electrique/)"] + [f"- [{H1(x)}]({SITE}/habilitation-electrique/{x['slug']}/): {x['resume']}" for x in SYMBOLES] + [""]
L += ["## Outils gratuits (FR)"] + [f"- [{c['title']}]({SITE}/calculateurs/{c['slug']}/): {c['desc']}" for c in CALCS] + [f"- [{m['title']}]({SITE}/modeles/{m['slug']}/): {m['desc']}" for m in MODELES] + [""]
L += ["## Fiches terrain (FR)"] + [f"- [{f['title']}]({SITE}/fiches/{f['slug']}/): {f['desc']}" for f in FICHES] + [""]
L += ["## Méthodes (FR)"] + [f"- [{m['title']}]({SITE}/methodes/{m['slug']}/): {m['desc']}" for m in METHODES] + [""]
L += ["## Guides (EN)"] + [f"- [{g['title']}]({SITE}/en/guides/{g['slug']}/): {g['desc']}" for g in GUIDES_EN] + [f"- [{m['title']}]({SITE}/en/methods/{m['slug']}/): {m['desc']}" for m in METHODS_EN] + [""]
L += ["## Territoires d'outre-mer (FR)"] + [f"- [{n}]({SITE}/{t}/)" for t, n in [("mayotte","Mayotte"),("la-reunion","La Réunion"),("guadeloupe","Guadeloupe"),("martinique","Martinique"),("guyane","Guyane")]]
open(os.path.join(ROOT, "llms.txt"), "w").write("\n".join(L) + "\n")
# garde-fou : contrôle qualité automatique après chaque génération
import subprocess
_r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "check.py"), ROOT])
if _r.returncode:
    sys.exit("ÉCHEC du contrôle qualité : corriger avant de publier.")
print("ok")
