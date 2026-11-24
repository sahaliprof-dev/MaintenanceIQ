"""Teste les parties interactives : questionnaires, QCM (chaque thème), calculateurs. Usage : python3 outils/check_interactif.py http://localhost:8765"""
import os, re, sys, glob
from playwright.sync_api import sync_playwright
BASE = sys.argv[1]; bad = []
with sync_playwright() as p:
    kw = {"executable_path": os.environ["CHROME"]} if os.environ.get("CHROME") else {}
    b = p.chromium.launch(**kw); ctx = b.new_context(viewport={"width": 390, "height": 844})
    ctx.route("**/*", lambda r: r.abort() if not r.request.url.startswith(BASE) else r.continue_())
    pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("dialog", lambda d: d.accept())
    # questionnaires des pages habilitation
    for f in sorted(glob.glob("habilitation-electrique/**/index.html", recursive=True)):
        if 'class="card quiz"' not in open(f).read(): continue
        u = "/" + f[:-len("index.html")]; pg.goto(BASE + u); errs.clear()
        n = pg.locator(".quiz").count()
        for k in range(n): pg.click(f'.qopt[data-q="{k}"][data-ok="1"]')
        sc = pg.inner_text("#score")
        if errs or f"{n} / {n}" not in sc or pg.locator(".qex[hidden]").count(): bad.append(f"{u} quiz : {sc} {errs[:1]}")
    # QCM : chaque thème
    pg.goto(BASE + "/qcm-habilitation-electrique/")
    themes = pg.eval_on_selector_all("#qt option", "o => o.map(x => x.value)")
    for t in themes:
        pg.goto(BASE + "/qcm-habilitation-electrique/"); errs.clear()
        pg.select_option("#qt", t); pg.select_option("#qn", "999"); pg.click("#qgo")
        n = pg.locator("#qbox .quiz").count()
        for k in range(n): pg.click(f'#qbox .qopt[data-k="{k}"][data-j="0"]')
        pg.click("#qend"); res = pg.inner_text("#qcm-res")
        m = re.search(r"(\d+) / (\d+)", res)
        if errs or not m or int(m.group(2)) != n or n == 0 or pg.locator(".corr li").count() != n: bad.append(f"QCM {t} : {n} questions, résultat {m.group(0) if m else None} {errs[:1]}")
    # calculateurs : un résultat s'affiche sans message d'erreur
    for f in sorted(glob.glob("calculateurs/*/index.html")) + ["calculateur-cout-panne/index.html", "en/downtime-cost-calculator/index.html"]:
        u = "/" + f[:-len("index.html")]; pg.goto(BASE + u); errs.clear(); pg.wait_for_timeout(150)
        out = pg.evaluate("(document.getElementById('out')||document.getElementById('tot')||{}).innerText||''")
        if errs or not out.strip() or "Vérifiez" in out or "NaN" in out or "Infinity" in out: bad.append(f"{u} calculateur : « {out[:80]} » {errs[:1]}")
    b.close()
for x in bad: print("PROBLÈME", x)
print(f"{len(bad)} problème(s) sur les parties interactives"); sys.exit(1 if bad else 0)
