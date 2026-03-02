# Product Backlog - Dice Roller Python

## 1. Role du document

Ce product backlog est la reference operationnelle unique du projet pour :

- le perimetre fonctionnel courant ;
- la priorisation ;
- le statut des user stories ;
- l'ordre logique des evolutions.

Les documents amont restent complementaires :

- `docs/00-vision/vision-projet.md` fixe la direction produit ;
- `docs/01-pre-projet/cdc-fonctionnel.md` fixe les regles et exigences fonctionnelles.

En cas d'ecart :

- la vision fixe la direction ;
- le CDC fixe la regle fonctionnelle ;
- le backlog pilote la priorisation et le statut des travaux.

## 2. Cadre produit

- Cadre : projet pedagogique mene en Scrum, avec increments courts et documentation maintenue.
- Reference de regles : **Dungeons & Dragons 5e - edition 2024**.
- Objectif perso : construire un projet portfolio utile, lisible et evolutif.
- Produit vise : un simulateur de lancers de des D&D simple, fiable et reutilisable par plusieurs interfaces.
- Vision long terme : preparer un futur "compagnon D&D" sans sortir prematurement du scope V1.

## 3. Regles de lecture

### Priorite

- `P0` : indispensable, bloque le reste
- `P1` : forte valeur, prochaine iteration
- `P2` : confort, qualite, experience
- `P3` : preparation long terme

### Statut

- `FAIT` : livre et considere fonctionnellement disponible
- `EN COURS` : partiellement en place, mais non stabilise ou incomplet
- `A FAIRE` : non demarre ou non livrable en l'etat

## 4. Regles metier de reference du MVP

Les regles suivantes font foi pour le MVP :

- Des supportes : `d4`, `d6`, `d8`, `d10`, `d12`, `d20`, `d100`
- Un lancer simple retourne une valeur comprise entre `1` et le nombre de faces demande
- Un lancer multiple `NdY` retourne les details individuels et le total, avec `N >= 1`
- Les critiques s'appliquent uniquement a un resultat `d20` unique retenu :
  - `1` = echec critique
  - `20` = reussite critique
- Un `Nd20` standard n'est pas un critique global
- Les modes `avantage` et `desavantage` sont reserves au `d20`
- En `avantage` ou `desavantage`, le systeme lance `2d20` et retient une seule valeur
- En `avantage` ou `desavantage`, `N` doit rester egal a `1`
- Le `d100` est reference comme un lancer de `2d10` :
  - un de pour les dizaines
  - un de pour les unites
  - le resultat final reste interprete entre `1` et `100`
- Aucun bonus generique ambigu de type `+1d4` ne doit etre expose sans regle officielle explicite
- Si une option de lancer additionnelle est proposee, elle doit :
  - etre une regle officielle clairement nommee
  - etre rattachee a un type de jet explicite
  - rester comprehensible dans le resultat
- L'interface ne doit jamais generer elle-meme le hasard ; le core reste la source de verite metier

## 5. Ordre logique d'implementation

1. Socle de lancers stable
2. Interface graphique minimale
3. Regles metier visibles du MVP (multi-des, critiques, modes d20, d100 coherent)
4. Stabilisation technique du socle (API, strategy, separation UI/core, tests)
5. Mise en conformite stricte du MVP avec la 5e 2024
6. Options officielles contextuelles 5e 2024
7. Evolutions de confort et d'experience
8. Preparation du futur compagnon D&D

## 6. Priorites immediates

### Bloc P0 - Assainir le socle et corriger le MVP

Ces items sont prioritaires car ils conditionnent la coherence du produit et debloquent la suite :

1. **TICKET-P0-001 - Validation centrale des des supportes**
2. **TICKET-P0-002 - Realignement backlog / code**
3. **TICKET-P0-003 - Garde-fou central sur la volumetrie des lancers**
4. **US-TECH-001 - Refacto core (API claire + constantes partagees + separation UI)**
5. **US-TECH-002 - Pattern Strategy pour les modes de lancer**
6. **US-UI-002 - Options de lancer d20 (modes de jet)**
7. **US-TECH-003 - Mise en conformite 5e 2024 des options de lancer**

Objectif du bloc P0 :

- disposer d'un socle metier propre ;
- fiabiliser le contrat central du core ;
- realigner le pilotage backlog avec l'etat reel du depot ;
- borner proprement les usages excessifs ;
- isoler correctement les modes de jet d20 ;
- supprimer l'ancien faux bonus generique `+1d4` ;
- preparer une base propre pour les options officielles contextuelles.

### Bloc P1 - Ajouter les options officielles contextuelles

Ces US viennent juste apres le nettoyage du socle :

1. **US-009 - Tests unitaires (core)**
2. **US-015 - Guidance (5e 2024)**
3. **US-016 - Bardic Inspiration (5e 2024)**
4. **US-017 - Heroic Inspiration (5e 2024)**

Objectif du bloc P1 :

- fiabiliser les regles deja en place ;
- ajouter les options officielles 5e 2024 sans ambiguity metier.

### Sequence d'execution recommandee

1. `TICKET-P0-001`
2. `TICKET-P0-002`
3. `TICKET-P0-003`
4. `US-TECH-001`
5. `US-TECH-002`
6. `US-UI-002`
7. `US-TECH-003`
8. `US-009`
9. `US-015`
10. `US-016`
11. `US-017`

## 7. Backlog detaille

### 7.1 Socle MVP livre

### US-002 - Lancer differents types de des (d4, d6, d8, d10, d12, d20, d100)

- Priorite : `P0`
- Statut : `FAIT`
- Type : `Core`
- Dependances : aucune
- User story :
  - En tant que joueur de D&D
  - Je veux lancer un de supporte
  - Afin d'obtenir un resultat coherent avec le type de de demande
- Criteres d'acceptation resumes :
  - un de supporte retourne un entier dans la bonne borne
  - un de non supporte est refuse proprement
  - des lancers successifs sur des differents restent coherents
  - le `d100` est documente fonctionnellement comme un lancer de `2d10` (dizaines + unites), sans changer le resultat final attendu

### US-UI-001 - IHM minimale (Tkinter)

- Priorite : `P0`
- Statut : `FAIT`
- Type : `UI`
- Dependances : `US-002`
- User story :
  - En tant que joueur
  - Je veux une interface graphique simple
  - Afin de ne pas dependre uniquement de la ligne de commande
- Criteres d'acceptation resumes :
  - choix du de via une liste
  - bouton "Lancer"
  - resultat affiche en clair
  - l'UI reutilise la logique existante sans `randint` duplique

### US-003 - Lancer plusieurs des (NdY)

- Priorite : `P1`
- Statut : `FAIT`
- Type : `Core + UI`
- Dependances : `US-002`, `US-UI-001`
- User story :
  - En tant que joueur
  - Je veux lancer `N` des d'un meme type
  - Afin de gerer les jets multiples utiles en jeu
- Criteres d'acceptation resumes :
  - `N >= 1`
  - le resultat contient `N` valeurs individuelles
  - le resultat contient le total du lancer
  - chaque valeur respecte les bornes du de choisi

### US-004 - Critiques d20 (1 / 20)

- Priorite : `P1`
- Statut : `FAIT`
- Type : `Core + UI`
- Dependances : `US-002`, `US-UI-001`
- User story :
  - En tant que joueur
  - Je veux que le systeme detecte les critiques sur un d20
  - Afin d'identifier automatiquement les moments cles du jet
- Criteres d'acceptation resumes :
  - `1` sur un d20 unique retenu = echec critique
  - `20` sur un d20 unique retenu = reussite critique
  - aucun autre de ne declenche de critique
  - un `Nd20` standard ne declenche pas de critique global

### US-UI-002 - Options de lancer d20 (modes de jet)

- Priorite : `P0`
- Statut : `EN COURS`
- Type : `Core + UI`
- Dependances : `US-UI-001`, `US-003`, `US-004`
- User story :
  - En tant que joueur
  - Je veux choisir un mode de lancer pour mes jets `d20`
  - Afin d'appliquer un jet normal, avec avantage, ou avec desavantage selon la situation de jeu
- Regle metier :
  - le simulateur propose le mode de lancer
  - il ne decide pas automatiquement si l'avantage ou le desavantage s'applique
- Criteres d'acceptation resumes :
  - `normal`, `avantage`, `desavantage` sont disponibles pour le `d20`
  - `avantage` et `desavantage` ne s'appliquent qu'au `d20`
  - `avantage` lance `2d20` et retient le meilleur resultat
  - `desavantage` lance `2d20` et retient le moins bon resultat
  - `N > 1` n'est pas combine avec `avantage` ou `desavantage`
- Note :
  - cette US ne couvre plus aucun faux bonus generique de type "inspiration +1d4"

### 7.2 Stabilisation technique (priorite immediate)

### TICKET-P0-001 - Validation centrale des des supportes

- Priorite : `P0`
- Statut : `A FAIRE`
- Type : `Core`
- Dependances : aucune
- Objectif :
  - garantir que le contrat central du core rejette toujours les des non supportes
  - supprimer tout chemin visible qui contourne cette regle metier
- Definition de done cible :
  - `resolve_roll` valide explicitement les faces supportees
  - aucun chemin public ne permet un lancer hors liste autorisee
  - un test automatise dedie couvre ce cas

### TICKET-P0-002 - Realignement backlog / code

- Priorite : `P0`
- Statut : `A FAIRE`
- Type : `Produit + Documentation`
- Dependances : aucune
- Objectif :
  - remettre le backlog en coherence avec l'etat reel du depot
  - distinguer clairement ce qui est code, stabilise, documente et encore a finaliser
- Definition de done cible :
  - les statuts de `US-TECH-003`, `US-015`, `US-016`, `US-017` sont revises
  - aucun item majeur deja visible dans le code ne reste `A FAIRE` sans justification
  - la priorisation immediate reste exploitable pour le prochain sprint

### TICKET-P0-003 - Garde-fou central sur la volumetrie des lancers

- Priorite : `P0`
- Statut : `A FAIRE`
- Type : `Core + CLI`
- Dependances : `TICKET-P0-001`
- Objectif :
  - definir puis appliquer une borne unique sur `count`
  - aligner les limites du core, de la CLI et de l'IHM
- Definition de done cible :
  - une limite de volumetrie explicite est retenue
  - le core applique cette limite de facon centralisee
  - un depassement produit une erreur claire et testee
  - la regle est documentee dans le backlog

### US-TECH-001 - Refacto core (API claire + constantes partagees + separation UI)

- Priorite : `P0`
- Statut : `EN COURS`
- Type : `Tech`
- Dependances : `US-002`, `US-UI-001`
- Objectif :
  - finaliser une API metier claire et non ambigue
  - centraliser les constantes partagees
  - garantir une separation stricte entre UI et logique metier
- Definition de done cible :
  - un seul contrat metier clair pour declencher un lancer
  - les des autorises et modes sont definis une seule fois
  - l'UI n'embarque aucune logique metier ni RNG
  - le core reste independant de Tkinter

### US-TECH-002 - Pattern Strategy pour les modes de lancer

- Priorite : `P0`
- Statut : `EN COURS`
- Type : `Tech`
- Dependances : `US-TECH-001`
- Objectif :
  - encapsuler les modes de lancer dans des strategies dediees
  - rendre le coeur plus extensible avant les prochaines US
- Definition de done cible :
  - `normal`, `multi`, `d20 avantage`, `d20 desavantage` passent par des strategies explicites
  - le contexte choisit la strategie sans logique metier dans l'UI
  - le resultat retourne une structure stable (`rolls`, `final_value`, `meta`, etc.)

### US-009 - Tests unitaires (core)

- Priorite : `P1`
- Statut : `EN COURS`
- Type : `Tech`
- Dependances : `US-TECH-001`
- Objectif :
  - couvrir les criteres d'acceptation essentiels du MVP
  - fiabiliser le coeur avant les prochaines evolutions fonctionnelles
- Definition de done cible :
  - validation des faces supportees
  - validation de `N >= 1`
  - couverture d20 normal / avantage / desavantage
  - critiques sur d20 uniquement
  - comportement du `d100` coherent avec sa representation de reference
  - tests alignes avec les regles du backlog

### 7.3 Mise en conformite 5e 2024 (priorite produit)

### US-TECH-003 - Mise en conformite 5e 2024 des options de lancer

- Priorite : `P0`
- Statut : `A FAIRE`
- Type : `Tech`
- Dependances : `US-TECH-001`, `US-TECH-002`
- Objectif :
  - supprimer l'ancien bonus generique `+1d4` non conforme
  - introduire une base propre pour les options officielles contextuelles
- Definition de done cible :
  - aucun faux libelle "inspiration +1d4" ne subsiste dans le produit
  - les options officielles sont nommees selon la 5e 2024
  - le systeme distingue clairement les modes de jet generiques et les options contextuelles
  - une notion de type de jet explicite existe pour eviter les bonus hors contexte

### US-015 - Guidance (5e 2024)

- Priorite : `P1`
- Statut : `A FAIRE`
- Type : `Core + UI`
- Dependances : `US-TECH-003`
- User story :
  - En tant que joueur
  - Je veux appliquer Guidance a un jet compatible
  - Afin d'ajouter la regle officielle correspondante sans approximation
- Criteres d'acceptation resumes :
  - Guidance ajoute `1d4`
  - Guidance ne s'applique qu'a une **ability check** ciblee
  - Guidance n'est pas exposee comme un bonus universel pour tous les jets
  - le detail du `1d4` apparait clairement dans le resultat

### US-016 - Bardic Inspiration (5e 2024)

- Priorite : `P1`
- Statut : `A FAIRE`
- Type : `Core + UI`
- Dependances : `US-TECH-003`
- User story :
  - En tant que joueur
  - Je veux appliquer une Bardic Inspiration a un jet compatible
  - Afin d'utiliser la regle officielle correspondante sans la simplifier a tort
- Criteres d'acceptation resumes :
  - Bardic Inspiration n'est pas modelisee comme un `+1d4`
  - elle ajoute un **de de barde**
  - la taille du de reste explicite et parametrable selon la regle retenue
  - le detail du de ajoute apparait clairement dans le resultat

### US-017 - Heroic Inspiration (5e 2024)

- Priorite : `P1`
- Statut : `A FAIRE`
- Type : `Core + UI`
- Dependances : `US-TECH-003`
- User story :
  - En tant que joueur
  - Je veux utiliser Heroic Inspiration sur un jet compatible
  - Afin de beneficier de la relance prevue par la regle 5e 2024
- Criteres d'acceptation resumes :
  - Heroic Inspiration permet une **relance**
  - elle n'ajoute aucun bonus fixe
  - le resultat initial, la relance et le resultat retenu restent lisibles
  - la presentation evite toute ambiguite pour l'utilisateur

### 7.4 Evolutions V2 - assistance aux jets et logique de jeu

### US-005 - Modificateur de caracteristique sur d20

- Priorite : `P2`
- Statut : `A FAIRE`
- Type : `Core + UI`
- Dependances : `US-TECH-002`, `US-009`
- Objectif :
  - appliquer un modificateur de caracteristique a un jet `d20`
- Criteres d'acceptation resumes :
  - visible seulement si le de choisi est `d20`
  - choix parmi `FOR`, `DEX`, `CON`, `INT`, `SAG`, `CHA`
  - calcul du modificateur (ex. `16 -> +3`)
  - affichage : jet brut + mod + total
- Hors perimetre :
  - competences
  - maitrise / expertise
  - buffs temporaires complexes

### US-006 - Seuil de reussite (DC) pour les jets d20

- Priorite : `P2`
- Statut : `A FAIRE`
- Type : `Core + UI`
- Dependances : `US-005`
- Objectif :
  - comparer un jet `d20` a un seuil de reussite
- Criteres d'acceptation resumes :
  - saisie d'un DC entier
  - verdict : reussite / echec
  - champ masque ou desactive si le de n'est pas `d20`

### 7.5 Experience utilisateur et qualite de vie

### US-UI-003a - Animation V1 (slot machine + verrouillage UI)

- Priorite : `P2`
- Statut : `A FAIRE`
- Type : `UI`
- Dependances : `US-UI-001`, `US-TECH-001`
- Objectif :
  - montrer visuellement un de qui "roule" sans introduire de second RNG
- Criteres d'acceptation resumes :
  - l'animation demarre au clic
  - les controles sont desactives pendant l'animation
  - aucun RNG cache dans l'animation
  - duree parametree entre environ `0.8s` et `1.5s`

### US-UI-003b - Animation d20 lisible + feedback critique

- Priorite : `P2`
- Statut : `A FAIRE`
- Type : `UI`
- Dependances : `US-UI-003a`, `US-004`
- Objectif :
  - rendre le resultat final d20 plus lisible et plus expressif
- Criteres d'acceptation resumes :
  - affichage final clair
  - indication visuelle de critique sur `1` ou `20`

### US-UI-003c - Animation d100 coherente (2d10)

- Priorite : `P2`
- Statut : `A FAIRE`
- Type : `UI + Core`
- Dependances : `US-UI-003a`, `US-002`
- Objectif :
  - proposer une animation d100 comprehensible et coherente avec sa representation de reference
- Criteres d'acceptation resumes :
  - animation de deux d10 (dizaines + unites)
  - resultat final correct entre `1` et `100`
  - affichage lisible du detail final

### US-UI-003d - Polish animation (skip, vitesse, micro-effets)

- Priorite : `P3`
- Statut : `A FAIRE`
- Type : `UI`
- Dependances : `US-UI-003a`, idealement `US-UI-003b`
- Objectif :
  - apporter des options de confort sur l'animation
- Criteres d'acceptation resumes :
  - option de desactivation
  - reglage de vitesse

### US-007 - Historique des jets dans l'IHM

- Priorite : `P2`
- Statut : `A FAIRE`
- Type : `UI`
- Dependances : `US-UI-001`
- Criteres d'acceptation resumes :
  - liste des 10 derniers jets
  - bouton "Effacer"
  - entrees lisibles (de, details, total)

### US-008 - Export / log des jets

- Priorite : `P2`
- Statut : `A FAIRE`
- Type : `Core + UI`
- Dependances : `US-007`
- Criteres d'acceptation resumes :
  - export manuel
  - format simple : timestamp, de, details, total

### US-010 - Generer un executable Windows (.exe)

- Priorite : `P3`
- Statut : `A FAIRE`
- Type : `Tech`
- Dependances : `US-UI-001`
- Criteres d'acceptation resumes :
  - build PyInstaller documente
  - `.gitignore` couvre `dist/`, `build/`, `*.spec`
  - executable GUI lancable sans console

### 7.6 Preparation du futur compagnon D&D (hors V1)

### US-011 - Modele Player minimal (JSON)

- Priorite : `P3`
- Statut : `A FAIRE`
- Type : `Core`
- Dependances : optionnellement `US-005`
- Objectif :
  - stocker un joueur minimal pour eviter la ressaisie

### US-012 - Gestion de profils

- Priorite : `P3`
- Statut : `A FAIRE`
- Type : `Core + UI`
- Dependances : `US-011`
- Objectif :
  - gerer plusieurs profils de joueur

### US-013 - Mode "tables" (des custom / loot)

- Priorite : `P3`
- Statut : `A FAIRE`
- Type : `Core + Data`
- Dependances : `US-008`, potentiellement `US-011`
- Objectif :
  - lancer un "de" qui mappe vers une table de resultat

### US-014 - Modele Entity (PJ / PNJ / Monstre)

- Priorite : `P3`
- Statut : `A FAIRE`
- Type : `Core`
- Dependances : optionnellement `US-011`
- Objectif :
  - preparer un modele commun d'entite pour une future persistence ou API

## 8. Hors perimetre officiel de la V1

Les sujets suivants restent hors scope tant que le socle n'est pas stabilise :

- simulation 3D
- resolution complete des actions de jeu
- fiche de personnage complete
- logique de combat complete
- persistance riche
- API distante
- refonte graphique ambitieuse non liee a la valeur produit immediate

## 9. Point d'attention de gouvernance

Le backlog doit rester maintenu en meme temps que :

- la vision produit ;
- le CDC fonctionnel ;
- le code quand une US change de statut.

Objectif : eviter qu'une US soit marquee `FAIT` dans un document et `A FAIRE` dans un autre, ou qu'une regle metier reste implicite.
