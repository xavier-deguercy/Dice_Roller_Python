# 004-sprint

# Sprint Backlog — Sprint 3 (US-UI-001 : IHM minimale)

## Objectif
Mettre à disposition une **IHM Tkinter minimale** pour lancer les dés D&D supportés.

---

## User Story incluse

### US-UI-001 — IHM minimale Dice Roller (Tkinter)
**En tant que** joueur de D&D  
**Je veux** une interface graphique simple pour lancer les dés  
**Afin de** ne pas dépendre uniquement de la ligne de commande.

#### Critères d’acceptation
- L’IHM propose un choix parmi : **4, 6, 8, 10, 12, 20, 100**.
- Le bouton “Lancer” affiche un résultat cohérent (1..N).
- L’IHM réutilise la logique existante (pas de “randint” en double dans l’UI).
- En cas de problème, un message clair est affiché (ex : exception import / bug).
- Le lancement est documenté (commande + fichier d’entrée).

---

## Livrables attendus
- Un script UI (ex : `src/v2-gui/app_tk.py`)
- Une documentation de lancement (README ou note dans docs)
- Un commit + push

---

## Dépendances
- US-002 livrée (OK)
- Avoir un point d’appel stable côté logique (ex : `DiceRoller.roll_die()` ou `roll_die()`)

---

## Notes
Ce sprint est volontairement **minimal** : on vise un incrément visible, pas une IHM “BG3-like”.
