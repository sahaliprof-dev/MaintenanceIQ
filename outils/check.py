"""Contrôle qualité du site MaintenanceIQ. Usage : python3 outils/check.py <racine_du_site>
Vérifie : liens internes cassés, images manquantes, JSON-LD invalide, titres/descriptions/canonical/h1,
titres en double, sitemap (pages existantes, pas de noindex), ads.txt, présence AdSense.
Sort avec le code 1 s'il trouve une erreur bloquante."""
import html.parser, json, os, re, sys, urllib.parse

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
SITE = "https://www.maintenanceiq.fr"
SKIP_DIRS = {".git", "outils", "node_modules", ".github"}
errors, warnings = [], []

class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.title = None; self._t = False; self.h1 = 0; self.meta = {}; self.canon = None; self.ld = []; self._ld = False; self._buf = ""; self.ids = set()
    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a: self.ids.add(a["id"])
        if tag == "a" and a.get("href"): self.links.append(("href", a["href"]))
        if tag in ("img", "script", "iframe", "source") and a.get("src"): self.links.append(("src", a["src"]))
        if tag == "link" and a.get("href") and a.get("rel") in ("stylesheet", "icon", "manifest", "apple-touch-icon"): self.links.append(("href", a["href"]))
        if tag == "link" and a.get("rel") == "canonical": self.canon = a.get("href")
        if tag == "meta" and a.get("name"): self.meta[a["name"]] = a.get("content", "")
        if tag == "meta" and a.get("property") == "og:image": self.links.append(("og", a.get("content", "")))
        if tag == "title": self._t = True; self.title = ""
        if tag == "h1": self.h1 += 1
        if tag == "script" and a.get("type") == "application/ld+json": self._ld = True; self._buf = ""
    def handle_endtag(self, tag):
        if tag == "title": self._t = False
        if tag == "script" and self._ld: self._ld = False; self.ld.append(self._buf)
    def handle_data(self, d):
        if self._t: self.title += d
        if self._ld: self._buf += d

def target_exists(path):
    path = urllib.parse.unquote(path.split("#")[0].split("?")[0])
    if not path or path == "/": return os.path.exists(os.path.join(ROOT, "index.html"))
    f = os.path.join(ROOT, path.lstrip("/"))
    if path.endswith("/"): return os.path.exists(os.path.join(f, "index.html"))
    return os.path.exists(f) or os.path.exists(os.path.join(f, "index.html"))

pages = {}
for d, dirs, files in os.walk(ROOT):
    dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
    for fn in files:
        if fn.endswith(".html"):
            full = os.path.join(d, fn)
            rel = "/" + os.path.relpath(full, ROOT).replace(os.sep, "/")
            url = rel[:-len("index.html")] if rel.endswith("index.html") else rel
            p = P(); src = open(full, encoding="utf-8").read(); p.feed(src)
            pages[url] = (p, src)

titles = {}
for url, (p, src) in pages.items():
    noindex = "noindex" in p.meta.get("robots", "")
    is_redirect = 'http-equiv="refresh"' in src
    for kind, l in p.links:
        if l.startswith(SITE): l = l[len(SITE):] or "/"
        if l.startswith("#"):
            if len(l) > 1 and l[1:] not in p.ids: errors.append(f"{url} : ancre introuvable {l}")
            continue
        if not l.startswith("/") or l.startswith("//"): continue
        if not target_exists(l): errors.append(f"{url} : lien interne cassé {l}")
        elif "#" in l:
            base, anc = l.split("#", 1)
            tp = pages.get(base.split("?")[0])
            if tp and anc and anc not in tp[0].ids: errors.append(f"{url} : ancre introuvable {l}")
    for b in p.ld:
        try: json.loads(b)
        except Exception as e: errors.append(f"{url} : JSON-LD invalide ({e})")
    if is_redirect or noindex: continue
    if url.startswith("/merci") or url.startswith("/ebook/"): continue
    if not p.title: errors.append(f"{url} : pas de <title>")
    else:
        titles.setdefault(p.title.strip(), []).append(url)
        if len(p.title) > 70: warnings.append(f"{url} : titre long ({len(p.title)} car.)")
    if not p.meta.get("description"): errors.append(f"{url} : pas de meta description")
    if not p.canon: warnings.append(f"{url} : pas de canonical")
    elif p.canon != SITE + url: errors.append(f"{url} : canonical incorrect {p.canon}")
    if p.h1 != 1: errors.append(f"{url} : {p.h1} balises h1")
    if "ca-pub-6829528595387726" not in src: errors.append(f"{url} : code AdSense absent")
for t, us in titles.items():
    if len(us) > 1: errors.append(f"titre en double « {t[:60]} » : {', '.join(us)}")

sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
if len(locs) != len(set(locs)): errors.append("sitemap : URL en double")
for loc in locs:
    path = loc[len(SITE):]
    if not target_exists(path): errors.append(f"sitemap : page inexistante {path}")
    elif path in pages:
        p, src = pages[path]
        if "noindex" in p.meta.get("robots", "") or 'http-equiv="refresh"' in src: errors.append(f"sitemap : page noindex ou redirection {path}")
for url, (p, src) in pages.items():
    if url.endswith("/") and SITE + url not in locs and "noindex" not in p.meta.get("robots", "") and 'http-equiv="refresh"' not in src and not url.startswith(("/merci", "/ebook/", "/404")):
        warnings.append(f"{url} : absente du sitemap")
if "pub-6829528595387726" not in open(os.path.join(ROOT, "ads.txt")).read(): errors.append("ads.txt incorrect")

print(f"{len(pages)} pages HTML contrôlées — {len(errors)} erreur(s), {len(warnings)} avertissement(s)")
for e in errors: print("ERREUR  ", e)
for w in warnings: print("AVERTIS.", w)
sys.exit(1 if errors else 0)
