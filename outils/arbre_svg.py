"""Génère un arbre de diagnostic SVG vertical (lisible sur téléphone) à partir d'une fiche."""
import html, textwrap

COUL = ["#3FA66A", "#D4A72C", "#E07B39", "#C9453B"]  # ordre de vérification : 1 vert ... 4 rouge (du plus simple au plus lourd)

def _lines(t, n):
    return textwrap.wrap(t, n, break_long_words=False) or [""]

def arbre(f, W=360):
    e = html.escape
    y = 0; out = []
    # en-tête
    out.append(f'<rect x="0" y="0" width="{W}" height="34" rx="6" fill="#21403A"/>'
               f'<text x="14" y="22" font-size="13" font-weight="700" fill="#FFFFFF">Arbre de diagnostic · {e(f["machine"])}</text>')
    y = 46
    # symptôme
    sl = _lines(f["signes"][0], 46)
    h = 26 + 17 * len(sl)
    out.append(f'<rect x="0" y="{y}" width="{W}" height="{h}" rx="6" fill="#EDF0EA" stroke="#21403A" stroke-width="1.2"/>'
               f'<text x="14" y="{y+18}" font-size="10.5" font-weight="700" fill="#5B726C" letter-spacing="1">SYMPTÔME</text>')
    for i, l in enumerate(sl):
        out.append(f'<text x="14" y="{y+36+17*i}" font-size="13.5" font-weight="600" fill="#14201D">{e(l)}</text>')
    y += h
    # flèche
    out.append(f'<path d="M{W//2} {y+2} v14" stroke="#21403A" stroke-width="2"/><path d="M{W//2-6} {y+10} l6 8 l6 -8" fill="#21403A"/>')
    y += 24
    out.append(f'<text x="0" y="{y+10}" font-size="11" font-weight="700" fill="#5B726C" letter-spacing="1">À VÉRIFIER DANS CET ORDRE</text>')
    y += 20
    for k, (cause, verif) in enumerate(f["causes"][:4]):
        cl = _lines(cause, 40); vl = _lines(verif, 46)
        h = 16 + 17 * len(cl) + 15 * len(vl) + 6
        c = COUL[k]
        out.append(f'<rect x="0" y="{y}" width="{W}" height="{h}" rx="6" fill="#FFFFFF" stroke="#CFD6D0"/>'
                   f'<rect x="0" y="{y}" width="6" height="{h}" rx="3" fill="{c}"/>'
                   f'<circle cx="26" cy="{y+20}" r="12" fill="{c}"/><text x="26" y="{y+25}" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">{k+1}</text>')
        ty = y + 24
        for l in cl:
            out.append(f'<text x="46" y="{ty}" font-size="13" font-weight="700" fill="#14201D">{e(l)}</text>'); ty += 17
        for l in vl:
            out.append(f'<text x="46" y="{ty}" font-size="12" fill="#4A5A55">{e(l)}</text>'); ty += 15
        y += h + 8
    # pied
    out.append(f'<rect x="0" y="{y+2}" width="{W}" height="30" rx="6" fill="#FBE9E7"/>'
               f'<text x="14" y="{y+22}" font-size="12" font-weight="700" fill="#7A1F14">Machine arrêtée et consignée avant toute intervention</text>')
    y += 34
    label = f"Arbre de diagnostic : {f['signes'][0]} Causes à vérifier dans l’ordre : " + " ; ".join(c for c, _ in f["causes"][:4])
    return (f'<svg viewBox="0 0 {W} {y}" role="img" aria-label="{e(label)}" font-family="Arial, Helvetica, sans-serif" '
            f'style="width:100%;max-width:520px;height:auto;display:block;margin:0 auto">' + "".join(out) + "</svg>")
