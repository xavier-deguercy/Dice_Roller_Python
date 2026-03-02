# Vision produit - Dice Roller Python

## 1. Contexte

Dice Roller Python est un projet personnel et pedagogique mene en mode Scrum.
Le produit sert deux objectifs complementaires :

- proposer un outil simple pour lancer des des de type Dungeons & Dragons ;
- servir de support de montee en competences Python, structuration logicielle et documentation produit.

Le projet est aujourd'hui centre sur un MVP de "dice roller" autonome.
La reference de regles retenue est desormais **Dungeons & Dragons 5e - edition 2024**.
La vision long terme est de preparer un futur "compagnon D&D" plus large, sans ouvrir ce scope trop tot.

## 2. Probleme a resoudre

Un joueur de jeu de role a besoin de realiser rapidement des jets fiables, lisibles et adaptes a plusieurs situations de jeu :

- jets simples ;
- jets multiples ;
- jets d20 avec regles specifiques ;
- bonus ponctuels.

Le besoin principal n'est pas la simulation visuelle complexe, mais un outil clair, rapide a utiliser et coherent avec les usages D&D.

## 3. Vision du produit

Fournir un lanceur de des D&D simple, fiable et evolutif, avec un coeur metier reutilisable par plusieurs interfaces, afin de livrer vite un outil utile aujourd'hui et de poser une base propre pour des evolutions futures.

Le produit est d'abord un **simulateur de lancers de des**.
Il peut proposer des options de lancer conformes aux regles officielles 5e 2024 quand elles sont clairement modelisees, mais il ne doit pas devenir trop tot un assistant complet de resolution des actions de jeu.

## 4. Utilisateurs cibles

### Utilisateur principal

- Joueur de D&D qui veut lancer des des sans passer uniquement par la ligne de commande.

### Utilisateur secondaire

- Developpeur apprenant / recruteur / lecteur du portfolio qui doit pouvoir comprendre rapidement le produit, son architecture et son evolution.

## 5. Proposition de valeur

Le produit doit apporter :

- un lancement rapide des des standards D&D ;
- une interface simple a prendre en main ;
- des regles de lancer explicites et predictibles ;
- une base technique propre permettant de faire evoluer l'application sans reintroduire de logique dupliquee.

## 6. Perimetre MVP

Le MVP actuel couvre :

- les des supportes : d4, d6, d8, d10, d12, d20, d100 ;
- le lancer simple ;
- le lancer multiple de type NdY ;
- les regles critiques sur d20 (1 et 20) ;
- les modes d20 : normal, avantage, desavantage ;
- des options de lancer uniquement si elles restent compatibles avec une logique stricte D&D 5e 2024 ;
- une interface graphique minimale en Tkinter ;
- un acces en ligne de commande.

Le MVP reste centre sur le **lancer de des**.
Les mecanismes d'aide a la resolution de situations de jeu (attaque, test complet, gestion de personnage) ne font pas partie du coeur de la V1.

## 7. Principes directeurs

Le produit doit respecter les principes suivants :

- un seul coeur metier pour definir les regles de lancer ;
- aucune logique metier dupliquee dans l'interface ;
- un seul RNG cote core pour garantir une source de verite unique ;
- une separation claire entre logique metier, presentation et futur outillage ;
- une documentation suffisamment claire pour qu'un nouveau lecteur comprenne le produit et ses limites.

## 8. Hors perimetre du MVP

Ne font pas partie du MVP actuel :

- animation avancee du type "BG3-like" ;
- historique des jets ;
- export des jets ;
- generation d'un executable Windows ;
- gestion de personnages, profils, persistance, base de donnees ;
- aide a la resolution complete des actions de jeu (jets d'attaque, gestion automatique des tests, logique de combat) ;
- systemes D&D avances (competences, maitrise, expertise, buffs complexes).

Ces sujets restent des evolutions possibles, mais ne doivent pas destabiliser le socle actuel.

## 9. Vision d'evolution

L'evolution du produit suit trois etapes logiques :

1. Stabiliser le socle actuel :
   core propre, API claire, strategy, tests, documentation.
2. Etendre l'experience de lancer :
   modificateurs d20, seuil de reussite (DC), animation, historique, export.
3. Preparer un futur compagnon D&D :
   modele joueur, profils, entites et eventuelle persistance.

## 10. Critere de succes

Le produit est considere comme sur de bons rails si :

- un utilisateur peut lancer un de ou plusieurs des sans ambiguite ;
- les options de lancer disponibles sont comprises et correctement appliquees dans le respect des regles 5e 2024 retenues ;
- l'interface reste simple et ne contient pas de logique metier cachee ;
- les evolutions futures peuvent s'ajouter sans refonte lourde du coeur ;
- la documentation produit et technique reste alignee avec l'etat reel du depot.

## 11. Orientation UX V1

L'experience cible de la V1 est volontairement **minimaliste et pratique**.

Cela implique :

- une interface simple et lisible ;
- un acces rapide aux lancers les plus utiles ;
- un affichage clair du resultat et de ses details ;
- aucune priorite donnee a l'immersion visuelle par rapport a la clarte et a la fiabilite.

Les elements immersifs ou de confort plus "jeu" (animation, polish visuel, memoire des lancers) sont reportes aux versions ulterieures.

## 12. Gouvernance documentaire

La repartition des roles documentaires est la suivante :

- ce document fixe la direction produit ;
- le CDC fixe le cadre fonctionnel ;
- le product backlog est la reference operationnelle unique pour le perimetre, la priorisation et les statuts.

Les documents de sprint servent a decrire l'execution d'une iteration, mais ne doivent plus porter seuls la verite fonctionnelle du produit.
