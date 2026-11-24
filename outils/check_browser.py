"""Ouvre chaque page en largeur téléphone (390 px) : erreurs JavaScript et débordement horizontal.
Usage : python3 outils/check_browser.py http://localhost:8765 <racine>"""
import os, sys
from playwright.sync_api import sync_playwright
BASE, ROOT = sys.argv[1], sys.argv[2]
urls = []
for d, dirs, files in os.walk(ROOT):
    dirs[:] = [x for x in dirs if x not in {".git", "outils", ".github", "node_modules"}]
    if "index.html" in files and 'http-equiv="refresh"' not in open(os.path.join(d, "index.html"), encoding="utf-8").read(1500):
        rel = "/" + os.path.relpath(d, ROOT).replace(os.sep, "/").strip(".") + "/"
        urls.append(rel.replace("//", "/"))
bad = 0
with sync_playwright() as p:
    kw = {"executable_path": os.environ["CHROME"]} if os.environ.get("CHROME") else {}
    b = p.chromium.launch(**kw)
    ctx = b.new_context(viewport={"width": 390, "height": 844})
    ctx.route("**/*", lambda r: r.abort() if not r.request.url.startswith(BASE) else r.continue_())
    for u in sorted(urls):
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(BASE + u, wait_until="load")
        w = pg.evaluate("Math.max(document.documentElement.scrollWidth, document.body.scrollWidth)")
        wide = pg.evaluate("""() => [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect(); return r.right > 392 && getComputedStyle(e).position !== 'fixed' && !e.closest('.tw,pre,table') }).slice(0,3).map(e => e.tagName + '.' + e.className)""")
        if errs or w > 392:
            bad += 1; print("PROBLÈME", u, "| erreurs JS :", errs[:2], "| largeur :", w, wide)
        pg.close()
    b.close()
print(f"{len(urls)} pages ouvertes, {bad} avec problème")
sys.exit(1 if bad else 0)
