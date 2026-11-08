# Versions

## En développement (après v261104, non publié)

- Arsenal : les équipements de cavalerie (chanfreins, bardes, fers) vont jusqu’à 80 000 par objet (au lieu de 50 000), comme dans le jeu.
- Sans Python (Chrome, Edge) : le fichier choisi la première fois est retenu ; chaque modification y est ensuite enregistrée automatiquement, sans créer de nouveau fichier, même après avoir fermé la page (bouton « Reprendre rol-data.json » si le navigateur redemande l’autorisation).
- Sans Python (Firefox, Safari) : explication affichée — ces navigateurs ne peuvent pas écrire dans un fichier, chaque enregistrement télécharge une copie.
- Windows : le lanceur trouve aussi Python lorsqu’il n’est pas dans le PATH (dossiers d’installation habituels, lanceur py, Anaconda) et ignore le raccourci du Microsoft Store.
- Mac : le lanceur trouve aussi Python lorsqu’il n’est pas dans le PATH (installateur python.org, Homebrew, MacPorts, Anaconda, pyenv) et n’ouvre plus la fenêtre d’installation d’Apple quand les outils de développement manquent.
- Bilan et Plan : saboteurs, expérience des hérauts et production d’unités par jour sont trois secrets séparés, chacun avec sa barre, son coût restant et sa place dans l’ordre des achats (avant, une seule barre « Saboteurs » mélangeait les trois).
- Plan : nouveau revenu « Top like du forum » (5 000 000 écus, nombre de fois par mois), compté dans le revenu mensuel et dans le journal des gains.

## v261104 — Première version publique (4 novembre 2026)

- Accueil : résumé du profil (points, armée, bilan, revenus, nourriture, mana, combats), évolution des points, prochains achats et points d’attention.
- Calculette des points de classement (formules de Kingadri), avec profils et historique daté, relevés passés et point de départ du royaume.
- Siège, équipement des sorciers, arsenal (emplacements, capacité, protections) et secrets (loups-garous, Léviathan, Citadelle féerique, tacticien, saboteurs, colosse).
- Production et consommation de nourriture, avec un objectif d’achat et les techniques les moins chères pour nourrir l’armée.
- Bilan des investissements et plan d’achats (revenus, événements, journal des gains, ordre des achats par glisser-déposer).
- Outils : somme des pillages, calculateur de prix et de mana.
- Combats : fiches ennemis importées des rapports (avec l’armée magique vue dans chaque rapport : sorciers, dragons, démons, loups, Colosse, et l’équipement des sorciers qui en découle), simulation des combats et « Où investir ? ».
- Enregistrement automatique avec Python (Windows, Mac, Linux), ou page seule avec ouverture et enregistrement manuels du fichier.
