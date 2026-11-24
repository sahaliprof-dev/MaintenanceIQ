# Schémas (SVG en ligne) et repères chiffrés ajoutés aux fiches terrain.
# Clé = slug de la fiche. Valeurs indicatives : la notice du constructeur passe toujours avant.

T = 'font-family="Instrument Sans, Arial, sans-serif"'

SCHEMAS = {
"cavitation-pompe": {
"svg": f'''<svg viewBox="0 0 640 300" role="img" aria-label="Schéma d’une installation de pompage : les trois points à vérifier côté aspiration et la vanne de réglage côté refoulement" {T}>
<rect x="20" y="150" width="150" height="120" rx="4" fill="#EDF0EA" stroke="#21403A" stroke-width="2"/>
<rect x="22" y="200" width="146" height="68" fill="#BFD9EA"/>
<line x1="22" y1="200" x2="168" y2="200" stroke="#2F6F9F" stroke-width="2" stroke-dasharray="6 4"/>
<text x="112" y="175" font-size="14" fill="#14201D">Cuve</text>
<path d="M95 245 V120 H330" fill="none" stroke="#21403A" stroke-width="10"/>
<rect x="80" y="240" width="30" height="22" fill="#21403A"/>
<circle cx="230" cy="120" r="13" fill="#F0F3E9" stroke="#21403A" stroke-width="3"/><line x1="230" y1="107" x2="230" y2="133" stroke="#21403A" stroke-width="3"/>
<circle cx="365" cy="120" r="38" fill="#21403A"/><text x="365" y="125" font-size="14" fill="#F0F3E9" text-anchor="middle">Pompe</text>
<path d="M365 82 V40 H600" fill="none" stroke="#21403A" stroke-width="10"/>
<circle cx="500" cy="40" r="13" fill="#F0F3E9" stroke="#3FA66A" stroke-width="3"/><line x1="487" y1="40" x2="513" y2="40" stroke="#3FA66A" stroke-width="3"/>
<g font-size="13" fill="#14201D">
<circle cx="125" cy="252" r="11" fill="#D9473B"/><text x="125" y="257" fill="#fff" text-anchor="middle" font-weight="700">1</text><text x="140" y="290">Crépine bouchée</text>
<circle cx="230" cy="88" r="11" fill="#D9473B"/><text x="230" y="93" fill="#fff" text-anchor="middle" font-weight="700">2</text><text x="190" y="54">Vanne d’aspiration :</text><text x="190" y="70">toujours ouverte en grand</text>
<circle cx="45" cy="200" r="11" fill="#D9473B"/><text x="45" y="205" fill="#fff" text-anchor="middle" font-weight="700">3</text><text x="180" y="215">Niveau trop bas</text>
<text x="440" y="78" fill="#2E7D52" font-weight="700">Réglez le débit ici,</text><text x="440" y="94" fill="#2E7D52" font-weight="700">au refoulement</text>
<text x="400" y="200" fill="#4A5A55">Aspiration : le côté</text><text x="400" y="216" fill="#4A5A55">où naît la cavitation</text>
</g></svg>''',
"legende": "Les trois causes à contrôler côté aspiration (en rouge) et le seul bon endroit pour régler le débit (en vert).",
"reperes": [
 ["Hauteur d’aspiration en eau froide", "10,3 m en théorie, environ 6 à 7 m en pratique : au-delà, la cavitation est presque assurée."],
 ["Marge de NPSH", "NPSH disponible supérieur au NPSH requis de la pompe d’au moins 0,5 à 1 m (courbe du constructeur)."],
 ["Vitesse de l’eau à l’aspiration", "Viser environ 1 à 1,5 m/s ; une conduite trop fine fait monter la vitesse et les pertes."],
 ["Température du liquide", "L’eau à 60 °C bout déjà à environ 0,2 bar absolu, à 80 °C vers 0,47 bar : plus elle est chaude, plus la marge fond."],
]},

"roulement-qui-siffle-ou-gronde": {
"svg": f'''<svg viewBox="0 0 640 210" role="img" aria-label="Seuils de vibration de la norme ISO 10816-3 pour une machine moyenne sur fondation rigide" {T}>
<text x="20" y="26" font-size="15" font-weight="700" fill="#14201D">Vitesse vibratoire efficace (mm/s), machine de 15 à 300 kW sur fondation rigide</text>
<rect x="20" y="60" width="140" height="50" fill="#3FA66A"/><rect x="160" y="60" width="140" height="50" fill="#9CCB6E"/>
<rect x="300" y="60" width="160" height="50" fill="#E2B32C"/><rect x="460" y="60" width="160" height="50" fill="#D9473B"/>
<g font-size="15" font-weight="700" text-anchor="middle"><text x="90" y="91" fill="#14201D">A · neuf</text><text x="230" y="91" fill="#14201D">B · correct</text><text x="380" y="91" fill="#14201D">C · à surveiller</text><text x="540" y="91" fill="#fff">D · dangereux</text></g>
<g font-size="14" fill="#14201D" text-anchor="middle"><line x1="160" y1="56" x2="160" y2="120" stroke="#14201D"/><text x="160" y="138">1,4</text>
<line x1="300" y1="56" x2="300" y2="120" stroke="#14201D"/><text x="300" y="138">2,8</text>
<line x1="460" y1="56" x2="460" y2="120" stroke="#14201D"/><text x="460" y="138">4,5</text></g>
<text x="20" y="180" font-size="13" fill="#4A5A55">En zone C : planifier l’intervention. En zone D : arrêter dès que possible, le roulement peut lâcher.</text>
<text x="20" y="198" font-size="13" fill="#4A5A55">Comparez toujours avec la mesure précédente au même point : c’est la hausse qui alerte.</text>
</svg>''',
"legende": "Seuils de la norme ISO 10816-3 (groupe 2, fondation rigide). Un vibromètre de poche suffit pour suivre la tendance.",
"reperes": [
 ["Température d’un palier", "Jusqu’à environ 70 à 80 °C, c’est courant. Au-delà de 90 °C, ou 20 °C de plus que d’habitude : à investiguer."],
 ["Quantité de graisse", "Remplir environ 30 à 50 % du volume libre du palier : trop de graisse fait chauffer autant que pas assez."],
 ["Vibrations", "1,4 / 2,8 / 4,5 mm/s : limites des zones A/B, B/C et C/D pour une machine moyenne sur fondation rigide."],
 ["Bruit", "Un sifflement aigu évoque un manque de lubrification, un grondement régulier une piste ou une bille abîmée."],
]},

"moteur-electrique-qui-chauffe": {
"svg": f'''<svg viewBox="0 0 640 230" role="img" aria-label="Règle des 10 degrés : chaque dépassement de 10 °C divise par deux la durée de vie de l’isolation du moteur" {T}>
<text x="20" y="26" font-size="15" font-weight="700" fill="#14201D">Durée de vie de l’isolation selon le dépassement de température</text>
<g font-size="14" fill="#14201D">
<rect x="150" y="45" width="440" height="30" fill="#3FA66A"/><text x="20" y="66">À la limite</text><text x="578" y="66" text-anchor="end" fill="#fff" font-weight="700">100 %</text>
<rect x="150" y="85" width="220" height="30" fill="#E2B32C"/><text x="20" y="106">+10 °C</text><text x="380" y="106">50 %</text>
<rect x="150" y="125" width="110" height="30" fill="#E5832F"/><text x="20" y="146">+20 °C</text><text x="270" y="146">25 %</text>
<rect x="150" y="165" width="55" height="30" fill="#D9473B"/><text x="20" y="186">+30 °C</text><text x="215" y="186">12 %</text>
</g>
<text x="20" y="220" font-size="13" fill="#4A5A55">Un moteur qui tourne 10 °C trop chaud vit environ deux fois moins longtemps.</text>
</svg>''',
"legende": "La règle des 10 °C : une surchauffe permanente use l’isolation des bobinages bien avant la panne visible.",
"reperes": [
 ["Température ambiante prévue", "La plupart des moteurs sont calculés pour 40 °C ambiants au maximum : un local plus chaud impose un déclassement."],
 ["Température de la carcasse", "60 à 80 °C au toucher-thermomètre peut être normal ; comparez avec un moteur identique ou une mesure précédente."],
 ["Tension d’alimentation", "Rester dans ±5 % de la tension de la plaque en fonctionnement normal."],
 ["Déséquilibre entre phases", "Au-delà de 1 % de déséquilibre de tension, le courant se déséquilibre plusieurs fois plus et le moteur chauffe : à faire mesurer."],
]},

"courroie-qui-siffle-ou-patine": {
"svg": f'''<svg viewBox="0 0 640 230" role="img" aria-label="Contrôle de la tension d’une courroie : mesure de la flèche au milieu de l’entraxe" {T}>
<circle cx="110" cy="110" r="60" fill="#EDF0EA" stroke="#21403A" stroke-width="3"/><circle cx="110" cy="110" r="8" fill="#21403A"/>
<circle cx="520" cy="110" r="40" fill="#EDF0EA" stroke="#21403A" stroke-width="3"/><circle cx="520" cy="110" r="6" fill="#21403A"/>
<path d="M110 50 L520 70" stroke="#21403A" stroke-width="6" fill="none"/><path d="M110 170 Q315 175 520 150" stroke="#21403A" stroke-width="6" fill="none"/>
<path d="M110 50 Q315 85 520 70" stroke="#E5832F" stroke-width="3" stroke-dasharray="7 5" fill="none"/>
<line x1="315" y1="20" x2="315" y2="55" stroke="#D9473B" stroke-width="3"/><path d="M308 48 L315 62 L322 48 Z" fill="#D9473B"/>
<g font-size="14" fill="#14201D"><text x="330" y="32">Appuyer au milieu</text><text x="190" y="128" fill="#B35F14">Flèche ≈ 16 mm par mètre d’entraxe</text>
<line x1="110" y1="205" x2="520" y2="205" stroke="#4A5A55"/><text x="315" y="222" text-anchor="middle" fill="#4A5A55">Entraxe (distance entre les axes)</text></g>
</svg>''',
"legende": "Machine arrêtée et consignée : la flèche mesurée au milieu de l’entraxe donne une première idée de la tension.",
"reperes": [
 ["Flèche de contrôle", "Environ 16 mm par mètre d’entraxe sous la force d’essai donnée par le fabricant de la courroie."],
 ["Alignement des poulies", "Désalignement inférieur à environ 0,5° pour des courroies trapézoïdales ; vérifier à la règle ou au fil tendu."],
 ["Rodage", "Une courroie neuve s’allonge : recontrôler la tension après 24 à 48 h de marche."],
 ["Jeu de courroies", "Sur une transmission à plusieurs courroies, on change tout le jeu, jamais une seule."],
]},

"armoire-electrique-connexion-qui-chauffe": {
"svg": f'''<svg viewBox="0 0 640 200" role="img" aria-label="Écarts de température entre phases mesurés par thermographie et décision associée" {T}>
<text x="20" y="26" font-size="15" font-weight="700" fill="#14201D">Écart de température entre deux phases identiques (thermographie)</text>
<rect x="20" y="50" width="190" height="56" fill="#E2B32C"/><rect x="210" y="50" width="220" height="56" fill="#E5832F"/><rect x="430" y="50" width="190" height="56" fill="#D9473B"/>
<g font-size="15" font-weight="700" text-anchor="middle"><text x="115" y="75" fill="#14201D">1 à 3 °C</text><text x="320" y="75" fill="#14201D">4 à 15 °C</text><text x="525" y="75" fill="#fff">plus de 15 °C</text></g>
<g font-size="13" text-anchor="middle"><text x="115" y="96" fill="#14201D">surveiller</text><text x="320" y="96" fill="#14201D">réparer dès que possible</text><text x="525" y="96" fill="#fff">réparer immédiatement</text></g>
<text x="20" y="150" font-size="13" fill="#4A5A55">Mesure à faire armoire fermée ou par une personne habilitée, sous charge normale.</text>
<text x="20" y="170" font-size="13" fill="#4A5A55">Une connexion chaude se resserre au couple du constructeur, hors tension et après consignation.</text>
</svg>''',
"legende": "Grille d’interprétation courante (inspirée de la norme américaine NETA) pour comparer des connexions identiques.",
"reperes": [
 ["Écart entre phases", "1 à 3 °C : surveiller. 4 à 15 °C : réparer dès que possible. Plus de 15 °C : réparer immédiatement."],
 ["Charge pendant la mesure", "Mesurer avec au moins 40 % de la charge habituelle, sinon l’échauffement ne se voit pas."],
 ["Resserrage", "Toujours au couple indiqué par le constructeur, avec une clé dynamométrique : trop serré abîme autant que pas assez."],
 ["Qui intervient", "Ouverture d’armoire et travaux réservés aux personnes habilitées, après consignation."],
]},
}
