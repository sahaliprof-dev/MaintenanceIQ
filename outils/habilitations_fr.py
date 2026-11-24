# Page « Les habilitations électriques » : tous les symboles groupés par thème + questionnaire.
# Sources : norme NF C 18-510 (et amendements), NF C 18-550 (véhicules), brochures INRS.

THEMES = [
("Non-électriciens : travaux d’ordre non électrique", "Peintres, maçons, agents d’entretien, mécaniciens qui travaillent dans un local électrique ou près d’une installation, sans toucher à l’électricité.", [
 ("B0", "Exécutant non électricien, basse tension", "Travaux d’ordre non électrique dans un local ou un environnement électrique BT : peinture, nettoyage, maçonnerie, mécanique."),
 ("B0 Chargé de chantier", "Chef d’équipe non électricien, basse tension", "Diriger des travaux d’ordre non électrique en BT et faire respecter les consignes de sécurité à son équipe."),
 ("H0", "Exécutant non électricien, haute tension", "Travaux d’ordre non électrique dans un local ou un environnement HT, hors zone de voisinage."),
 ("H0V", "Non électricien, haute tension, au voisinage", "Mêmes travaux que H0, mais autorisé à pénétrer dans la zone de voisinage HT. Existe en Exécutant et en Chargé de chantier."),
 ("BF-HF", "Travaux en fouilles", "Terrassements et tranchées à proximité de canalisations électriques isolées enterrées. Existe en Exécutant et en Chargé de chantier."),
]),
("Électriciens : travaux hors tension", "Électriciens qui réalisent des travaux sur une installation consignée, seuls ou en équipe.", [
 ("B1", "Exécutant électricien, basse tension", "Travaux d’ordre électrique hors tension en BT, sous la conduite d’un chargé de travaux."),
 ("B1V", "Exécutant électricien BT, au voisinage", "Comme B1, avec en plus le droit de travailler dans la zone de voisinage renforcé de pièces nues sous tension."),
 ("B2", "Chargé de travaux, basse tension", "Diriger et réaliser des travaux d’ordre électrique hors tension en BT, organiser la sécurité de l’équipe."),
 ("B2V", "Chargé de travaux BT, au voisinage", "Comme B2, au voisinage de pièces nues sous tension."),
 ("B2V Essai", "Chargé d’essais, basse tension", "Chargé de travaux qui réalise aussi des essais sur l’ouvrage, avec mise sous tension."),
 ("H1 / H1V", "Exécutant électricien, haute tension", "Travaux d’ordre électrique hors tension en HT ; V pour le voisinage."),
 ("H2 / H2V", "Chargé de travaux, haute tension", "Diriger des travaux d’ordre électrique hors tension en HT ; V pour le voisinage."),
 ("H2V Essai", "Chargé d’essais, haute tension", "Chargé de travaux HT autorisé à réaliser des essais."),
]),
("Consignation", "La consignation met une installation en sécurité avant des travaux : séparation, condamnation, vérification d’absence de tension, mise à la terre si nécessaire.", [
 ("BC", "Chargé de consignation, basse tension", "Consigner et déconsigner une installation BT pour des travaux réalisés par d’autres."),
 ("HC", "Chargé de consignation, haute tension", "Consigner et déconsigner une installation HT."),
]),
("Interventions en basse tension", "Dépannages, raccordements et remplacements sur des installations BT, souvent par un seul intervenant.", [
 ("BR", "Chargé d’intervention générale, basse tension", "Dépannages, raccordements, mesurages, essais et vérifications en BT ; il peut consigner pour son propre compte. C’est le symbole courant du technicien de maintenance."),
 ("BS", "Chargé d’intervention élémentaire, basse tension", "Opérations simples sur des circuits BT de faible puissance : remplacer un fusible, une lampe, une prise ou un interrupteur, raccorder sur un circuit en attente, dans les limites fixées par la norme."),
]),
("Opérations spécifiques", "Opérations ciblées qui ne sont ni des travaux ni des interventions. Le symbole est toujours suivi d’un attribut.", [
 ("BE Manœuvre / HE Manœuvre", "Chargé d’opérations de manœuvre", "Manœuvres d’exploitation : mettre en marche, arrêter, réarmer une protection, sur des organes prévus pour ça."),
 ("BE Mesurage / HE Mesurage", "Chargé de mesurage", "Mesurer des grandeurs électriques (tension, courant, isolement) sans autre opération."),
 ("BE Vérification / HE Vérification", "Chargé de vérification", "Vérifier une installation (contrôles réglementaires, par exemple)."),
 ("BE Essai / HE Essai", "Chargé d’essais", "Réaliser des essais sur une installation ou un équipement."),
 ("BP", "Installations photovoltaïques", "Opérations sur les générateurs photovoltaïques (côté continu), où la tension est présente dès qu’il y a de la lumière."),
]),
("Travaux sous tension et cas spéciaux", "Ces lettres s’ajoutent en troisième position et demandent une formation spécifique.", [
 ("T (B1T, B2T, H1T, H2T…)", "Travaux sous tension", "Travailler sur des pièces nues sous tension, avec des méthodes et un outillage dédiés."),
 ("N", "Nettoyage sous tension", "Nettoyer des installations maintenues sous tension, principalement en haute tension."),
 ("X", "Habilitation spéciale", "Opérations particulières définies par l’employeur, hors des cas courants."),
]),
("Véhicules et engins électriques (norme NF C 18-550)", "Voitures, utilitaires, bus, chariots élévateurs et engins à batterie : les symboles se terminent par la lettre L. La borne de recharge, elle, est une installation fixe et relève des symboles classiques.", [
 ("B0L", "Non électricien sur véhicule", "Opérations d’ordre non électrique sur un véhicule électrique ou hybride (pneus, carrosserie, vidange). Attribut Exécutant ou Chargé de réparation."),
 ("B1L / B1VL", "Exécutant électricien sur véhicule", "Travaux d’ordre électrique hors tension sur le véhicule ; V pour le voisinage."),
 ("B2L / B2VL", "Chargé de travaux sur véhicule", "Diriger des travaux d’ordre électrique sur le véhicule ; V pour le voisinage."),
 ("BCL", "Chargé de consignation sur véhicule", "Consigner le circuit de traction du véhicule avant travaux."),
 ("BEL / BRL", "Essais et interventions sur véhicule", "Essais (BEL) et interventions (BRL), notamment en conception ou en fabrication."),
 ("B1XL / B2XL", "Opérations particulières sur véhicule", "Métiers spécifiques, précisés par un attribut : contrôle technique, opération batterie, dépannage-remorquage, secours."),
]),
]

LECTURE = [
("1er caractère : la tension", "B pour la basse et la très basse tension, H pour la haute tension."),
("2e caractère : le type d’opération", "0 non électricien · 1 exécutant électricien · 2 chargé de travaux · C consignation · R intervention générale · S intervention élémentaire · E opération spécifique · P photovoltaïque · F fouilles."),
("3e caractère, si besoin : la nature", "V voisinage · T sous tension · N nettoyage sous tension · X spécial. L en dernier pour les véhicules (NF C 18-550)."),
("L’attribut écrit en toutes lettres", "Essai, Vérification, Mesurage, Manœuvre, Chargé de chantier… Il précise ce que le titulaire a le droit de faire."),
]

QUIZ = [
("Que signifie la lettre B au début d’un symbole ?", ["Bâtiment", "Basse tension (et très basse tension)", "Brevet d’électricien"], 1, "B désigne le domaine basse et très basse tension ; H désigne la haute tension."),
("Un peintre doit repeindre un local électrique BT. Quelle habilitation ?", ["B0", "B1", "BS"], 0, "Il réalise des travaux d’ordre non électrique : B0 suffit, il ne touche pas à l’installation."),
("Que veut dire la lettre V dans B1V ?", ["Vérification", "Voisinage", "Véhicule"], 1, "V autorise à travailler au voisinage de pièces nues sous tension."),
("Quel symbole pour un technicien de maintenance qui dépanne des machines en BT ?", ["B0", "BR", "BE Mesurage"], 1, "BR, chargé d’intervention générale : dépannage, raccordement, mesurage, essais, et consignation pour son propre compte."),
("Qui consigne une installation BT pour qu’une autre équipe y travaille ?", ["Le chargé de consignation BC", "L’exécutant B1", "Le non-électricien B0"], 0, "La consignation pour le compte d’autrui revient au chargé de consignation BC (HC en haute tension)."),
("Remplacer un fusible ou une lampe sur un circuit simple : quel symbole minimum ?", ["BS", "B2V", "HC"], 0, "BS couvre les interventions élémentaires sur des circuits BT de faible puissance."),
("Réarmer un disjoncteur et remettre une machine en marche relève de :", ["BE Manœuvre", "BP", "BF-HF"], 0, "Les manœuvres d’exploitation relèvent du symbole BE Manœuvre."),
("Une entreprise creuse une tranchée près d’un câble enterré. Quel symbole ?", ["B1V", "BF-HF", "BC"], 1, "BF-HF couvre les travaux en fouilles à proximité de canalisations isolées enterrées."),
("Que signifie la lettre T en troisième position ?", ["Travaux sous tension", "Tableau électrique", "Technicien"], 0, "T désigne les travaux sous tension, qui demandent une formation spécifique."),
("Un mécanicien répare l’électronique de puissance d’une voiture électrique. Quelle norme ?", ["NF C 18-510", "NF C 18-550", "NF C 15-100"], 1, "Les véhicules et engins à énergie électrique embarquée relèvent de la NF C 18-550 ; les symboles se terminent par L."),
("Qui délivre l’habilitation électrique ?", ["L’organisme de formation", "L’employeur", "L’inspection du travail"], 1, "L’organisme forme et donne un avis ; c’est l’employeur qui délivre le titre d’habilitation à son salarié."),
("Tous les combien recommande-t-on un recyclage ?", ["Tous les ans", "Tous les 3 ans", "Tous les 10 ans"], 1, "La norme recommande un recyclage tous les 3 ans au maximum, et plus tôt en cas de changement de poste ou d’incident."),
]
