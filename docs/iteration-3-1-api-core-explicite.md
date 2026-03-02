# Iteration 3.1 - API metier du core plus explicite

## 1. Objet

Cette note formalise la cible de conception pour l'iteration **3.1** :

- rendre l'API metier du core plus explicite ;
- supprimer la logique de "bonus booleen generique" ;
- preparer une base stable pour les regles D&D 5e 2024.

Le but n'est pas encore de recrire le code, mais de fixer un contrat metier clair avant implementation.

## 2. Probleme actuel

L'API actuelle du core repose encore sur une signature de type :

- choix d'un de ;
- nombre de des ;
- mode de jet ;
- ancien booleen de type `inspiration`.

Cette forme n'est plus suffisante pour une logique stricte 5e 2024, car elle melange :

- des donnees de lancer ;
- des modes de jet ;
- des regles de jeu ;
- des options contextuelles.

Limites principales :

- un booleen generique ne permet pas de distinguer des regles officielles differentes ;
- le type de jet n'est pas exprime ;
- le contexte metier (ex. ability check) n'est pas formalise ;
- l'API n'est pas prete pour faire evoluer proprement `Guidance`, `Bardic Inspiration` et `Heroic Inspiration`.

## 3. Objectif de l'iteration

L'objectif est de faire evoluer le core vers une API ou un lancer est decrit comme une **requete metier explicite**, et non comme une suite de parametres faiblement relies.

Cette requete doit distinguer au minimum :

- le type de lancer ;
- le mode de lancer ;
- le contexte metier du jet ;
- les options officielles eventuelles.

## 4. Contrat d'entree cible

## 4.1 Principe

Le point d'entree du core doit converger vers une forme de type :

- `roll(request)`

Le `request` represente le lancer complet.
Il doit devenir la source unique de verite de l'entree metier.

## 4.2 Champs metier minimaux du request

Le contrat d'entree cible doit porter les informations suivantes.

### A. Donnees de base du lancer

- `die_faces`
  - type de de demande (`4`, `6`, `8`, `10`, `12`, `20`, `100`)
- `count`
  - nombre de des
- `roll_mode`
  - mode de lancer (`normal`, `avantage`, `desavantage`)

Ces champs couvrent le besoin du simulateur de base.

### B. Type de lancer

- `roll_kind`

Ce champ sert a qualifier la nature metier du jet.
Exemples de valeurs cibles :

- `generic_roll`
- `ability_check`
- `attack_roll`
- `saving_throw`

Pour la V1, seule une partie de ces valeurs peut etre exposee a l'utilisateur.
Mais le contrat doit etre pense pour les supporter.

### C. Options officielles contextuelles

- `official_options`

Ce champ represente les regles officielles appliquees au lancer.
Il ne doit pas etre remplace par des booleens ad hoc.

Exemples d'options cibles :

- `guidance`
- `bardic_inspiration`
- `heroic_inspiration`

Ces options doivent rester :

- explicites ;
- nommees selon la regle ;
- validables selon le contexte du jet.

### D. Metadonnees contextuelles minimales

Selon l'option retenue, il pourra etre necessaire d'avoir :

- une taille de de pour `Bardic Inspiration`
- un indicateur de relance pour `Heroic Inspiration`
- un contexte compatible pour `Guidance`

L'important ici est le principe : les donnees de contexte doivent etre explicites, et non deduites d'un booléen imprécis.

## 5. Regles de responsabilite

Le core doit rester responsable de :

- la validation du `request` ;
- la compatibilite entre `roll_kind` et `official_options` ;
- la validation des combinaisons interdites ;
- la production d'un resultat structure.

L'UI et la CLI ne doivent faire que :

- collecter les choix utilisateur ;
- construire le `request` ;
- afficher le resultat ;
- afficher une erreur claire si le core rejette la requete.

## 6. Regles de validation minimales

Le futur contrat doit pouvoir exprimer et faire respecter ces regles :

- `die_faces` doit faire partie des des supportes
- `count` doit etre un entier >= 1
- `avantage` et `desavantage` ne s'appliquent qu'au `d20`
- `avantage` et `desavantage` ne se combinent pas avec `count > 1`
- `Guidance` ne s'applique pas hors d'un `ability_check`
- `Heroic Inspiration` ne doit pas etre modelisee comme un bonus fixe
- `Bardic Inspiration` doit porter un de explicite, pas une valeur magique implicite

## 7. Contrat de sortie attendu (minimum)

Le sujet principal de cette iteration est l'entree metier, mais son impact direct est le contrat de sortie.

Le resultat du core devra rester unique et stable, avec au minimum :

- les valeurs tirees
- la valeur retenue
- le total final
- le mode applique
- les options officielles appliquees
- les details utiles a l'affichage (`d100`, relance, bonus de regle)

Le point cle :
si l'entree devient plus explicite, la sortie doit rester suffisamment riche pour eviter toute reconstitution metier cote UI.

## 8. Strategie de migration depuis l'API actuelle

La migration recommande est progressive.

### Etape 1 - Geler l'API actuelle comme legacy

L'API actuelle peut continuer a exister temporairement, mais doit etre consideree comme une forme transitoire.

Objectif :

- ne pas casser brutalement l'UI et la CLI ;
- preparer la transition vers un `request` unique.

### Etape 2 - Introduire le nouveau contrat metier

Le core doit introduire un point d'entree base sur un `request` explicite.

Objectif :

- permettre a la nouvelle logique de vivre sans reutiliser les anciens booleens ambigus.

### Etape 3 - Faire migrer les interfaces

La GUI et la CLI doivent ensuite construire ce `request` au lieu d'appeler directement une signature ancienne.

Objectif :

- aligner toutes les interfaces sur le meme contrat.

### Etape 4 - Retirer les anciens raccourcis

Une fois les interfaces alignees :

- supprimer les options legacy ambiguës ;
- retirer l'ancien faux `+1d4` ;
- nettoyer les anciennes validations devenues redondantes.

## 9. Impact sur les US

Cette iteration impacte directement :

- `US-TECH-001`
  - clarifier l'API core
- `US-TECH-002`
  - mieux separer mode de jet et comportement
- `US-TECH-003`
  - supprimer l'ancien faux bonus generique
- `US-015`
  - `Guidance` depend d'un contexte explicite
- `US-016`
  - `Bardic Inspiration` depend d'un parametre explicite de de
- `US-017`
  - `Heroic Inspiration` depend d'une logique de relance explicite

## 10. Criteres de validation de l'iteration

L'iteration 3.1 est consideree comme correctement cadree si :

- le contrat d'entree cible du core est documente ;
- les notions de `roll_kind`, `roll_mode` et `official_options` sont distinguees ;
- le faux modele "booleen generique" est explicitement abandonne ;
- les interfaces sont identifiees comme adaptateurs, non comme porteuses de logique ;
- les futures US officielles (Guidance, Bardic Inspiration, Heroic Inspiration) peuvent s'appuyer sur cette base sans re-ouvrir la conception.

## 11. Recommandation immediate

Avant toute implementation, la suite la plus saine est :

1. valider ce contrat d'entree cible ;
2. en deduire un mini contrat de sortie ;
3. seulement ensuite ajuster le backlog technique et le code.

Sans cette clarification, ajouter les regles 5e 2024 reviendrait a empiler des cas particuliers sur une base trop floue.
