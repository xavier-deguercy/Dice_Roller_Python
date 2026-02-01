# 004-sprint
# 🎲 User Story — US-002 : Lancer différents types de dés

## US-002 — Lancer un dé de type D&D

**En tant que** joueur de Donjons & Dragons  
**Je veux** pouvoir lancer des dés de différents types *(d4, d6, d8, d10, d12, d20, d100)*  
**Afin de** réaliser tous les jets nécessaires au jeu *(attaques, dégâts, compétences, sauvegardes)*.

---

## ✅ Critères d’acceptation

### CA-1 : Dé supporté
**Given** le programme est lancé  
**When** je demande un lancer de dé avec un nombre de faces parmi **4, 6, 8, 10, 12, 20, 100**  
**Then** le programme retourne un entier compris entre **1** et **le nombre de faces demandé** *(bornes incluses)*.

### CA-2 : Dé non supporté
**Given** le programme est lancé  
**When** je demande un lancer de dé avec un nombre de faces non supporté *(ex. 7, 15, 30)*  
**Then** le programme affiche un message indiquant que ce type de dé n’est pas pris en charge.

### CA-3 : Indépendance du type de dé
**Given** je lance successivement différents types de dés  
**When** je lance un **d4**, puis un **d20**, puis un **d100**  
**Then** chaque lancer est indépendant et retourne un résultat cohérent avec le type de dé demandé.

---

## 🧩 Hors périmètre (pour cette US)

- Lancer plusieurs dés en une fois *(ex. 3d6)*  
- Ajouter des modificateurs *(+X / -X)*  
- Gestion des échecs / réussites critiques *(d20)*  

➡️ Ces éléments feront l’objet d’autres user stories.

---

## 📌 Notes techniques (pour le développeur)

- Le nombre de faces doit être passé en paramètre à une fonction *(ex. `roll_die(nb_faces)`)*.
- Une liste de dés autorisés doit être définie *(ex. `[4, 6, 8, 10, 12, 20, 100]`)*.
- La fonction doit lever ou gérer proprement les cas non valides.

---

## 🧠 Compétences mises en évidence

- Passage d’un code “en dur” à une fonction paramétrable
- Gestion de conditions *(if / else)*
- Validation des entrées
- Application concrète d’une user story Scrum
