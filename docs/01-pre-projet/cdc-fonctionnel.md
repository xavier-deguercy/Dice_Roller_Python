# Cahier des charges fonctionnel - Dice Roller Python

## 1. Objet du document

Ce document formalise le besoin fonctionnel du projet Dice Roller Python.
Il sert de reference pour :

- cadrer le MVP ;
- aligner le backlog produit ;
- eviter les ambiguitees fonctionnelles entre code, backlog et documentation.

Le backlog produit reste la source de priorisation et de statut.
Ce document fixe le cadre fonctionnel et les regles metier attendues.

## 2. Contexte

Dice Roller Python est une application permettant de realiser des lancers de des utilises dans Dungeons & Dragons.
La reference de regles retenue est **Dungeons & Dragons 5e - edition 2024**.
Le produit doit proposer un usage simple, lisible et fiable, avec un coeur de logique reutilisable par plusieurs interfaces.

Le projet est mene comme un projet pedagogique incremental.
Chaque increment doit rester petit, demonstrable et documente.

## 3. Public cible

- Joueur ou meneur de jeu souhaitant lancer rapidement des des D&D.
- Utilisateur ayant besoin d'une interface simple, sans manipulation complexe.

## 4. Besoin fonctionnel

L'utilisateur doit pouvoir :

- choisir un type de de supporte ;
- lancer un de unique ;
- lancer plusieurs des du meme type ;
- utiliser les regles specifiques du d20 ;
- consulter un resultat lisible et exploitable immediatement ;
- acceder au produit via une interface graphique minimale, et au besoin en ligne de commande.

## 5. Perimetre fonctionnel du MVP

### 5.1 Fonctions incluses

Le MVP doit couvrir les fonctions suivantes :

- lancer de des supportes : d4, d6, d8, d10, d12, d20, d100 ;
- lancer simple ;
- lancer multiple NdY avec N >= 1 ;
- detection des critiques sur d20 ;
- mode d20 normal ;
- mode d20 avantage ;
- mode d20 desavantage ;
- representation de reference du d100 en `2d10` (dizaines + unites), sans changer le resultat final attendu ;
- options de lancer officielles uniquement si elles sont explicitement nommees, definies et reliees a un contexte de jet ;
- interface Tkinter minimale ;
- acces CLI pour lancer un jet.

### 5.2 Fonctions explicitement hors perimetre

Ne sont pas incluses dans ce document pour le MVP :

- animation avancee du lancer ;
- historique des 10 derniers jets ;
- export txt/csv ;
- packaging en executable ;
- gestion de fiche de personnage ;
- profils multiples ;
- tables de loot ou des custom ;
- base de donnees / API ;
- tout bonus generique non rattache a une regle officielle explicite (ex. faux "inspiration +1d4").

## 6. Exigences fonctionnelles detaillees

### EF-01 - Choix du type de de

Le systeme doit permettre de selectionner un type de de parmi la liste suivante :

- 4
- 6
- 8
- 10
- 12
- 20
- 100

Tout autre type de de doit etre refuse avec un message clair.
Pour le `d100`, la representation de reference suit un lancer de `2d10` :

- un de pour les dizaines ;
- un de pour les unites ;
- le resultat fonctionnel reste interprete comme une valeur finale comprise entre `1` et `100`.

### EF-02 - Lancer simple

Pour un de supporte, le systeme doit retourner un entier compris entre 1 et le nombre de faces demande, bornes incluses.

### EF-03 - Lancer multiple (NdY)

Le systeme doit permettre de lancer N des d'un meme type, avec les regles suivantes :

- N doit etre un entier >= 1 ;
- le resultat doit contenir les valeurs individuelles ;
- le resultat doit contenir le total du lancer ;
- chaque valeur individuelle doit respecter les bornes du de choisi.

### EF-04 - Critiques d20

Le systeme doit detecter les critiques uniquement pour un resultat d20 unique retenu :

- 1 : echec critique ;
- 20 : reussite critique.

Aucun autre de ne doit produire de critique.
Un lancer multi-des standard de type `Nd20` ne doit pas etre traite comme un critique global.

### EF-05 - Modes d20

Le systeme doit prendre en charge trois modes pour le d20 :

- normal ;
- avantage ;
- desavantage.

Regles attendues :

- le mode avantage lance 2d20 et retient le meilleur resultat ;
- le mode desavantage lance 2d20 et retient le moins bon resultat ;
- ces modes sont reserves au d20 ;
- ces modes impliquent un lancer unique retenu et ne se combinent pas avec `N > 1`.

### EF-06 - Options de lancer officielles contextuelles (5e 2024)

Le systeme ne doit pas proposer de bonus generique ambigu de type `+1d4` sans regle explicite.
Toute option de lancer additionnelle doit respecter les principes suivants :

- elle doit correspondre a une regle officielle identifiee ;
- elle doit etre nommee correctement selon la regle 5e 2024 ;
- elle doit etre reliee a un type de jet explicite ;
- elle ne doit pas etre exposee comme un simple "toggle" generique hors contexte.

Ces options ne sont donc pas des bonus universels : elles dependent du contexte du jet et de la regle appliquee.

### EF-07 - Guidance

Si la regle **Guidance** est proposee, elle doit etre modelisee comme une option contextuelle conforme :

- elle ajoute `1d4` ;
- elle s'applique a une **ability check** ciblee ;
- elle ne doit pas etre presentee comme un bonus universel pour tous les jets ;
- le detail du `1d4` doit rester visible dans le resultat.

### EF-08 - Bardic Inspiration

Si la regle **Bardic Inspiration** est proposee, elle doit etre modelisee comme une option contextuelle conforme :

- elle n'est pas un `+1d4` fixe ;
- elle ajoute un **de de barde** ;
- la taille du de doit rester parametree selon la regle ou le niveau retenu ;
- le detail du de ajoute doit rester visible dans le resultat.

### EF-09 - Heroic Inspiration

Si la regle **Heroic Inspiration** est proposee, elle doit etre modelisee comme une option contextuelle conforme :

- elle permet une **relance** ;
- elle n'ajoute pas de bonus fixe ;
- la relance doit etre visible et comprehensible pour l'utilisateur ;
- le produit doit eviter toute ambiguite entre resultat initial, relance et resultat retenu.

### EF-10 - Interface graphique minimale

Le produit doit proposer une interface graphique minimale permettant :

- de choisir un type de de dans une liste ;
- de choisir un nombre de des ;
- de lancer le jet ;
- d'afficher le resultat ;
- d'exposer les options liees au d20 sans dupliquer les regles metier dans l'UI.

### EF-11 - Ligne de commande

Le produit doit proposer un mode CLI permettant d'executer un lancer sans passer par l'interface graphique.

Le mode CLI doit :

- accepter les parametres principaux du jet ;
- afficher un resultat lisible ;
- renvoyer une erreur claire en cas de saisie invalide.

## 7. Regles metier transverses

- Les des autorises sont definis une seule fois dans le produit.
- Les regles de lancer sont centralisees dans le core.
- L'interface ne doit pas produire elle-meme de hasard.
- Les messages retournes a l'utilisateur doivent rester comprensibles.
- Un resultat de lancer doit etre structure et contenir assez d'information pour etre affiche sans recalcul metier cote UI.
- Les options officielles non generiques (Guidance, Bardic Inspiration, Heroic Inspiration) ne peuvent etre proposees que si le type de jet et la condition d'application sont explicites.

## 8. Exigences non fonctionnelles

### ENF-01 - Fiabilite

- Les cas invalides doivent etre geres proprement.
- Le produit ne doit pas planter sur une saisie utilisateur invalide.

### ENF-02 - Maintenabilite

- La logique metier doit rester separee de l'interface.
- Les constantes partagees doivent etre centralisees.
- Les comportements de lancer doivent rester extensibles.

### ENF-03 - Testabilite

- Les regles metier doivent pouvoir etre testees de facon deterministe.
- Les criteres d'acceptation du MVP doivent etre traduits en tests automatises.

### ENF-04 - Tracabilite

- Les evolutions fonctionnelles doivent pouvoir se relier a une user story ou a un item de backlog.
- La documentation produit doit rester synchronisee avec l'etat du code.

## 9. Contraintes

- Reference de regles : D&D 5e 2024.
- Langage cible : Python 3.11+.
- Interface graphique cible : Tkinter.
- Le produit doit rester exploitable localement sans dependance externe complexe.
- Le coeur metier doit etre reutilisable par plusieurs interfaces.
- Le projet doit rester dans un scope compatible avec un MVP et un usage portfolio.

## 10. Mapping avec le backlog produit

- **US-002** : types de des supportes.
- **US-UI-001** : interface graphique minimale.
- **US-003** : lancers multiples.
- **US-004** : critiques d20.
- **US-UI-002** : options de lancer d20 (modes de jet).
- **US-TECH-001** : separation UI/core et centralisation des regles.
- **US-TECH-002** : formalisation des modes de lancer.
- **US-009** : tests du coeur metier.

Des user stories dediees devront etre creees ou mises a jour pour :

- la mise en conformite stricte des options de lancer contextuelles 5e 2024 ;
- Guidance ;
- Bardic Inspiration ;
- Heroic Inspiration.

Les items suivants sont consideres comme evolutions hors MVP mais deja identifies :

- **US-005** : modificateurs de caracteristique sur d20.
- **US-006** : seuil de reussite (DC).
- **US-UI-003a a US-UI-003d** : animation.
- **US-007** / **US-008** : historique et export.
- **US-010 a US-014** : industrialisation et preparation du futur compagnon D&D.

## 11. Criteres d'acceptation globaux du MVP

Le MVP est considere comme fonctionnel si :

- un utilisateur peut lancer un de supporte et obtenir un resultat valide ;
- un utilisateur peut lancer plusieurs des et obtenir detail + total ;
- un utilisateur peut utiliser les modes d20 et voir le resultat retenu ;
- le d100 reste lisible et sans ambiguite, y compris s'il est represente en `2d10` ;
- les critiques sont detectees uniquement dans les cas prevus ;
- les options de lancer additionnelles, si elles sont proposees, respectent strictement la regle 5e 2024 qui leur correspond ;
- l'interface graphique minimale permet un usage simple sans saisie libre du type de de ;
- le mode CLI permet un lancer equivalent sur le plan fonctionnel.

## 12. Points de vigilance documentaires

Les documents amont `vision-projet.md` et `cdc-fonctionnel.md` etaient vides au moment de cette remise a plat.
La reference fonctionnelle historique etait donc diffuse dans :

- le backlog produit ;
- certains backlogs de sprint ;
- le README.

Desormais, tout changement fonctionnel significatif doit rester aligne entre :

- ce CDC ;
- la vision produit ;
- le product backlog, qui reste la reference operationnelle unique.
