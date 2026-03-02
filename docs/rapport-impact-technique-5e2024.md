# Rapport d'impact technique - Dice Roller Python (D&D 5e 2024)

## 1. Objet du rapport

Ce rapport synthétise l'impact technique des décisions produit récemment actées :

- positionnement du produit comme **simulateur de lancers de dés** ;
- référence de règles : **Dungeons & Dragons 5e - édition 2024** ;
- V1 orientée **minimaliste et pratique** ;
- suppression de l'ancien faux bonus générique `+1d4` ;
- introduction future d'options officielles contextuelles (`Guidance`, `Bardic Inspiration`, `Heroic Inspiration`).

Il sert à :

- expliciter les conséquences techniques avant modification du code ;
- sécuriser l'ordre de réalisation ;
- préparer la transition entre la documentation produit et la mise en œuvre.

## 2. Décisions produit déjà validées

### 2.1 Ce que le produit est en V1

Le produit est un **simulateur de lancers de dés D&D**.

Le cœur de la V1 est :

- lancer des dés standards (`d4`, `d6`, `d8`, `d10`, `d12`, `d20`, `d100`) ;
- lancer un ou plusieurs dés ;
- gérer les cas visibles du `d20` (critiques, modes de jet) ;
- proposer une interface simple (Tkinter + CLI).

### 2.2 Ce que le produit n'est pas encore

La V1 n'est pas :

- un moteur complet de résolution d'actions de jeu ;
- un assistant de personnage ;
- un produit orienté immersion visuelle ;
- un système de stockage des lancers ou des profils.

### 2.3 Cadre de règles

La logique métier doit maintenant rester compatible avec la **5e 2024**.

Conséquences immédiates :

- `Guidance` = `1d4` sur une **ability check** ciblée ;
- `Bardic Inspiration` = **dé de barde**, pas `+1d4` ;
- `Heroic Inspiration` = **relance**, pas bonus additif fixe.

## 3. Impacts techniques majeurs

### 3.1 L'API métier du core doit devenir plus explicite

Le moteur ne peut plus se limiter à une logique du type :

- choix d'un dé ;
- nombre de dés ;
- bonus booléen générique.

Avec les nouvelles règles, il faut distinguer :

- le type de lancer ;
- le mode de lancer ;
- le contexte métier du jet ;
- les options officielles éventuelles.

Impact :

- le contrat d'entrée du core doit être plus structuré ;
- un simple booléen de type `inspiration=True` n'est plus acceptable ;
- les futures options doivent s'appuyer sur une représentation métier stable.

### 3.2 Il faut séparer deux concepts aujourd'hui faciles à confondre

Le système doit distinguer clairement :

- les **modes de jet** : `normal`, `avantage`, `desavantage`
- les **options de règles officielles** : `Guidance`, `Bardic Inspiration`, `Heroic Inspiration`

Impact :

- `US-UI-002` doit rester centrée sur les modes de jet `d20` ;
- les règles officielles doivent être modélisées comme une autre couche ;
- le code doit éviter de centraliser toutes les variantes dans un seul bloc conditionnel.

### 3.3 Le modèle de résultat doit devenir plus riche

Pour rester lisible et extensible, le résultat d'un lancer doit pouvoir décrire :

- les dés réellement tirés ;
- la valeur retenue ;
- un éventuel détail `d100` ;
- un bonus officiel appliqué ;
- une relance ;
- les métadonnées utiles à l'affichage.

Impact :

- le format de sortie du core doit devenir plus stable ;
- le risque de dette augmente si tout reste en `dict` implicites ;
- CLI et UI doivent dépendre d'un contrat unique.

### 3.4 Le `d100` en `2d10` ajoute une contrainte de modélisation

Fonctionnellement, le résultat final reste un nombre entre `1` et `100`.
Mais la règle de représentation change :

- un dé pour les dizaines ;
- un dé pour les unités.

Impact :

- le core doit pouvoir exposer cette décomposition ;
- l'affichage doit pouvoir la restituer clairement ;
- les tests doivent couvrir cette représentation de référence.

### 3.5 Les options officielles imposent une notion de contexte de jet

Certaines règles ne s'appliquent pas à tous les jets.
Exemple :

- `Guidance` ne doit pas être disponible hors **ability check** ;
- `Heroic Inspiration` n'est pas un simple bonus additif ;
- `Bardic Inspiration` suppose une logique de dé additionnel, pas un entier fixe.

Impact :

- il faut introduire une notion de **type de jet** ;
- sans ce contexte, l'outil retomberait dans une logique de "toggle flou", contraire au cadre retenu.

### 3.6 La séparation UI / core devient encore plus importante

La contrainte d'architecture est saine et doit être maintenue :

- un seul RNG dans le core ;
- aucune logique métier dans l'UI ;
- GUI et CLI limitées à l'entrée / sortie.

Impact :

- les validations fonctionnelles doivent rester dans le cœur ;
- l'UI ne doit ni recalculer, ni interpréter les règles ;
- l'UI doit dépendre d'un contrat clair fourni par le core.

### 3.7 Il existe un impact de migration sur l'existant

Le produit porte encore des traces d'une ancienne logique incorrecte autour de `+1d4`.

Impact :

- les documents ont été corrigés ;
- le code devra être nettoyé ;
- certains libellés, certaines options UI et certains tests devront être mis à jour ;
- cette correction doit être traitée comme une **mise en conformité**, pas comme un simple renommage.

## 4. Risques techniques identifiés

### 4.1 Risque principal : accumulation de cas spéciaux

Si les nouvelles règles sont ajoutées sans refonte de l'API métier :

- la logique va se disperser ;
- les `if/else` vont s'empiler ;
- les comportements deviendront plus difficiles à tester.

### 4.2 Risque de divergence entre interfaces

Si le contrat de résultat n'est pas clarifié :

- CLI et GUI risquent de formatter des cas différemment ;
- les nouvelles options contextuelles seront plus difficiles à garder cohérentes.

### 4.3 Risque de non-conformité règle / implémentation

Si les options officielles sont ajoutées sans notion de contexte :

- `Guidance` pourrait être proposée à tort sur tous les jets ;
- `Heroic Inspiration` pourrait être mal modélisée ;
- la documentation 5e 2024 et le produit repartiraient en divergence.

### 4.4 Risque de régression

Le nettoyage du faux `+1d4` peut casser :

- l'UI actuelle ;
- des messages existants ;
- des tests existants ;
- les habitudes d'utilisation actuelles.

Il faut donc considérer cette étape comme un changement métier contrôlé.

## 5. Garde-fous recommandés

- Conserver **un seul RNG** dans le core.
- Garder **Tkinter** pour la V1.
- Garder une **séparation stricte UI / core**.
- Introduire un **contrat d'entrée métier explicite** avant d'ajouter de nouvelles règles.
- Introduire un **contrat de sortie unique** avant de multiplier les cas spéciaux.
- Ne pas ajouter `Guidance`, `Bardic Inspiration` ou `Heroic Inspiration` tant que l'ancien `+1d4` n'est pas supprimé.
- Faire évoluer les tests en parallèle des changements métier.

## 6. Séquence technique recommandée

### Etape 1 - Stabiliser le socle

Traiter d'abord :

- `US-TECH-001`
- `US-TECH-002`
- `US-UI-002`

Objectif :

- clarifier le contrat du core ;
- isoler proprement les modes de jet `d20` ;
- garder les interfaces simples.

### Etape 2 - Corriger la conformité 5e 2024

Traiter ensuite :

- `US-TECH-003`

Objectif :

- retirer le faux `+1d4` ;
- introduire une base de modélisation propre pour les options contextuelles ;
- préparer le terrain pour les règles officielles.

### Etape 3 - Sécuriser

Traiter ensuite :

- `US-009`

Objectif :

- figer les règles du MVP par des tests ;
- éviter les régressions avant d'ajouter les nouvelles options officielles.

### Etape 4 - Ajouter les options officielles

Traiter ensuite :

- `US-015` (`Guidance`)
- `US-016` (`Bardic Inspiration`)
- `US-017` (`Heroic Inspiration`)

Objectif :

- ajouter les nouvelles règles sans casser le socle ;
- garder une modélisation claire et testable.

## 7. Suite recommandée

### 7.1 Suite documentaire immédiate

La base documentaire est désormais cohérente.
La prochaine suite utile côté documentation est :

1. relire et valider le statut exact de `US-TECH-001`, `US-TECH-002`, `US-UI-002`, `US-009` ;
2. découper un **sprint backlog court** centré sur `US-TECH-001` à `US-TECH-003` ;
3. définir les critères d'acceptation détaillés (Given / When / Then) pour `US-015`, `US-016`, `US-017`.

### 7.2 Suite technique immédiate

Avant d'ajouter de nouvelles règles, il faut :

1. nettoyer le faux `+1d4` dans le produit existant ;
2. clarifier le contrat d'entrée du core ;
3. préparer une structure de résultat plus stable ;
4. seulement ensuite ajouter les options officielles.

### 7.3 Recommandation pragmatique

La meilleure suite n'est pas de coder immédiatement `Guidance`.
La meilleure suite est :

1. finir d'assainir le moteur ;
2. retirer la mauvaise règle ;
3. sécuriser par tests ;
4. puis ajouter les règles officielles une par une.

## 8. Conclusion

Les décisions produit prises sont cohérentes, mais elles augmentent le niveau d'exigence du moteur.

La conséquence n'est pas d'ajouter beaucoup plus de fonctionnalités d'un coup.
La conséquence est de devoir mieux modéliser :

- ce qu'est un lancer ;
- ce qu'est un mode de jet ;
- ce qu'est une option de règle ;
- ce qu'est un résultat exploitable par plusieurs interfaces.

Si cette base est bien posée maintenant, la suite restera propre, testable et cohérente avec une logique de développement "indus / senior".
