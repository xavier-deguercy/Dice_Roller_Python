# 004-sprint
# US-003 — Lancer plusieurs dés (avantage desavantage au D20)

## Description
**En tant que** joueur de D&D  
**Je veux** pouvoir lancer plusieurs dés du même type si d20   
**Afin de** gérer les jets de dégâts, sorts et caractéristiques.

--- a revoir car faux 

## Critères d’acceptation

### CA-1 — Lancer N dés
**Given** je choisis un type de dé autorisé  
 

**When** je demande un lancer de `N` dés (`N ≥ 1`)  

**Then** le programme retourne :
- `N` résultats individuels
- le total du lancer

---

### CA-2 — Validation de N
**Given** je saisis une valeur `N` invalide  
(0, négatif, non numérique)  

**When** je valide  

**Then** le programme :
- affiche un message d’erreur clair
- ne plante pas

---

### CA-3 — Cohérence des bornes
**Then** chaque résultat individuel est compris entre :
- `1` et `Y`  
(`Y` étant le nombre de faces du dé)

---

## Hors périmètre
- Avantage / désavantage (2d20 garder le meilleur ou le pire)
- Modificateurs (+X / -X)
- Critiques (traitées dans **US-004**)

---








# US-004 — Critiques d20

## Description
**En tant que** joueur de D&D  
**Je veux** que le programme détecte un échec critique (1) et une réussite critique (20) sur un d20  
**Afin de** reconnaître automatiquement les moments clés du jeu.

---

## Critères d’acceptation

### CA-1 — Échec critique (d20)
**Given** je lance un d20 (1d20)  

**When** le résultat est `1`  

**Then** le programme indique :
- **Échec critique**

---

### CA-2 — Réussite critique (d20)
**Given** je lance un d20 (1d20)  

**When** le résultat est `20`  

**Then** le programme indique :
- **Réussite critique**

---

### CA-3 — Pas de critique hors d20
**Given** je lance un autre dé  
(d6, d10, d100, etc.)  

**Then** le programme :
- n’indique aucune critique

---

## Hors périmètre
- Avantage / désavantage (US dédiée)
- Seuil de réussite (ex. `15+`)
- Relances
