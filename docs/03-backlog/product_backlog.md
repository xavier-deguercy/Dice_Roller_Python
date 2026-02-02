# 🎲 Product Backlog — Dice Roller Python

> **Cadre** : projet pédagogique en **Scrum** (incréments courts, commits fréquents, docs à jour).  
> **Objectif perso** : projet “side” pour accompagner ma reconversion (portfolio + montée en compétences Python / OOP).  
> **MVP actuel** : Dice Roller D&D (core + IHM Tkinter) avec multi-dés, critiques d20, avantage/désavantage d20, inspiration (+1d4).  
> **Vision long terme (hors MVP)** : préparer un futur “Compagnon D&D” (fiche perso, persistance, entités, etc.).

---

## 🧾 Légende

### Priorité
- **P0** : indispensable / bloque le reste
- **P1** : forte valeur, prochaine itération
- **P2** : confort / qualité
- **P3** : préparation long terme

### Statut
- ✅ **FAIT**
- 🟡 **EN COURS**
- ⬜ **À FAIRE**

---

## 📌 Règles de dépendances (ordre logique)

1) **Core stable** (US-002)  
2) **IHM minimale** (US-UI-001)  
3) **Multi-dés** (US-003) + **règles d20** (US-004 + US-UI-002)  
4) **Stabilisation technique** : refacto core + Strategy + tests (US-TECH-001/002 + US-009)  
5) **Modificateurs d20 (carac)** (US-005) → **DC / seuil** (US-006)  
6) **Animation “BG3-like”** (US-UI-003a → 003b → 003c → 003d)  
7) Qualité de vie (historique, export, exe), puis préparation “fiche perso”.

---

## ✅ Backlog (détaillé)

|-------------------------------------------------------------------------------------|
|-----# US-002 — Lancer différents types de dés (d4, d6, d8, d10, d12, d20, d100)-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P0  
- **Statut** : ✅ FAIT  
- **Type** : Core  
- **Dépendances** : aucune  
- **Livrable** : logique de jet + validation des dés autorisés

---

|-------------------------------------------------------------------------------------|
|-----# US-UI-001 — IHM minimale (Tkinter)-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P0  
- **Statut** : ✅ FAIT  
- **Type** : UI  
- **Dépendances** : US-002  
- **Livrable** : `src/v2_gui/app_tk.py` (choix du dé + bouton Lancer + résultat)

---

|-------------------------------------------------------------------------------------|
|-----# US-003 — Lancer plusieurs dés (NdY)-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P1  
- **Statut** : ✅ FAIT  
- **Type** : Core + UI  
- **Dépendances** : US-002, US-UI-001  
- **Notes** : multi-dés pour tous les dés autorisés (ex. 3d6, 2d8, 4d10, etc.)

---

|-------------------------------------------------------------------------------------|
|-----# US-004 — Critiques d20 (1 / 20)-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P1  
- **Statut** : ✅ FAIT  
- **Type** : Core + UI  
- **Dépendances** : US-002, US-UI-001  
- **Notes** : critiques uniquement sur d20 (affichage après le jet)

---

|-------------------------------------------------------------------------------------|
|-----# US-UI-002 — Options d20 + bonus (Avantage/Désavantage + Inspiration +1d4)-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P1  
- **Statut** : ✅ FAIT  
- **Type** : UI (et core pour d20 adv/disadv)  
- **Dépendances** : US-UI-001, US-003, US-004  
- **Notes** :
  - **Avantage / Désavantage** : uniquement d20
  - **Inspiration bardique** : bonus **+1d4**

---

## 🧱 Stabilisation technique (Sprint 5)

|-------------------------------------------------------------------------------------|
|-----# US-TECH-001 — Refacto core (API claire + constantes partagées + séparation UI)-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P0  
- **Statut** : ⬜ À FAIRE  
- **Type** : Tech  
- **Dépendances** : US-002, US-UI-001  
- **But** :
  - 0 duplication de logique entre UI et core
  - constantes centralisées (dés autorisés / modes)
  - core indépendant de Tkinter
- **AC (résumé)** :
  - les dés autorisés sont définis **une seule fois**
  - l’UI ne contient pas de RNG ni de règles métier
  - l’exécution UI fonctionne après refacto

---

|-------------------------------------------------------------------------------------|
|-----# US-TECH-002 — Pattern Strategy pour les modes de lancer-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P1  
- **Statut** : ⬜ À FAIRE  
- **Type** : Tech  
- **Dépendances** : US-TECH-001  
- **But** : séparer les comportements (normal / multi / d20 avantage / d20 désavantage) en stratégies interchangeables
- **AC (résumé)** :
  - `DiceRoller.roll(request)` délègue à une stratégie (pas de gros if/else métier dans l’UI)
  - résultat structuré (rolls + valeur finale + meta)

---

|-------------------------------------------------------------------------------------|
|-----# US-009 — Tests unitaires (core)-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P1  
- **Statut** : ⬜ À FAIRE  
- **Type** : Tech  
- **Dépendances** : US-TECH-001 (core stabilisé)  
- **AC (résumé)** :
  - validation faces
  - d20 normal/avantage/désavantage
  - NdY (N >= 1)
  - critiques d20 uniquement

---

## 🧠 Préparer la future fiche de perso (sans basculer dans un gros scope)

|-------------------------------------------------------------------------------------|
|-----# US-005 — Modificateur de caractéristique sur d20 (pré-fiche de perso)-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P1  
- **Statut** : ⬜ À FAIRE  
- **Type** : Core + UI  
- **Dépendances** : US-UI-002 + (idéalement) US-TECH-002 + US-009  
- **But** : appliquer un modificateur lié à une caractéristique (FOR/DEX/CON/INT/SAG/CHA) **uniquement sur d20**
- **AC (résumé)** :
  - visible seulement si dé = d20
  - choix de la caractéristique
  - calcul du mod (ex: 16 → +3)
  - affichage : jet brut + mod + total
- **Hors périmètre** : compétences, maîtrise/expertise, buffs temporaires

---

|-------------------------------------------------------------------------------------|
|-----# US-006 — Seuil de réussite (DC) pour les jets d20-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P1  
- **Statut** : ⬜ À FAIRE  
- **Type** : UI + Core  
- **Dépendances** : US-005  
- **AC (résumé)** :
  - saisie d’un DC (entier)
  - verdict : réussite / échec
  - masqué/désactivé si dé ≠ d20

---

## 🎥 Animation “BG3-like” (découpée en sous-US)

> Objectif : “voir un dé qui roule” **sans 3D** (Tkinter Canvas + animation `after()`), et **un seul RNG**
> (le core fournit le résultat final, l’animation le révèle).

|-------------------------------------------------------------------------------------|
|-----# US-UI-003a — Animation V1 (slot machine + shake) + verrouillage UI-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P2  
- **Statut** : ⬜ À FAIRE  
- **Type** : UI  
- **Dépendances** : US-UI-001 + US-TECH-001 (un seul RNG côté core)
- **AC (résumé)** :
  - animation démarre au clic
  - bouton/options désactivés pendant l’animation
  - pas de RNG caché dans l’animation
  - durée ~ 0.8–1.5s (paramétrable)

---

|-------------------------------------------------------------------------------------|
|-----# US-UI-003b — Animation d20 “face visible” + feedback critique-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P2  
- **Statut** : ⬜ À FAIRE  
- **Type** : UI  
- **Dépendances** : US-UI-003a + US-004  
- **AC (résumé)** :
  - affichage final lisible + tag critique (1/20)
  - (optionnel) micro feedback visuel

---

|-------------------------------------------------------------------------------------|
|-----# US-UI-003c — Animation d100 cohérente (2d10 : dizaines + unités)-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P2  
- **Statut** : ⬜ À FAIRE  
- **Type** : UI + Core (si besoin d’exposer dizaines/unités)  
- **Dépendances** : US-UI-003a  
- **AC (résumé)** :
  - animation de deux d10
  - résultat final 1..100 correct
  - affichage lisible : “d100 → 70 + 3 = 73”

---

|-------------------------------------------------------------------------------------|
|-----# US-UI-003d — Polish animation (skip, vitesse, micro-effets)-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P3  
- **Statut** : ⬜ À FAIRE  
- **Type** : UI  
- **Dépendances** : US-UI-003a (+ idéalement 003b)  
- **AC (résumé)** :
  - option “désactiver l’animation”
  - réglage de vitesse

---

## 🧰 Qualité de vie / projet “propre”

|-------------------------------------------------------------------------------------|
|-----# US-007 — Historique des jets dans l’IHM-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P2  
- **Statut** : ⬜ À FAIRE  
- **Type** : UI  
- **Dépendances** : US-UI-001  
- **AC (résumé)** :
  - liste des 10 derniers jets
  - bouton “Effacer”
  - entrée lisible (dé, détails, total)

---

|-------------------------------------------------------------------------------------|
|-----# US-008 — Export / log des jets (txt ou csv)-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P2  
- **Statut** : ⬜ À FAIRE  
- **Type** : Core + UI  
- **Dépendances** : US-007  
- **AC (résumé)** :
  - export manuel
  - format simple (timestamp, dé, détails, total)

---

|-------------------------------------------------------------------------------------|
|-----# US-010 — Générer un exécutable Windows (.exe)-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P3  
- **Statut** : ⬜ À FAIRE  
- **Type** : Tech  
- **Dépendances** : US-UI-001 (IHM stable)  
- **AC (résumé)** :
  - build PyInstaller documenté
  - `.gitignore` : dist/, build/, *.spec
  - exe lancé sans console (Tkinter)

---

## 🧩 Préparation “Compagnon D&D” (hors MVP)

|-------------------------------------------------------------------------------------|
|-----# US-011 — Modèle Player minimal (JSON)-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P3  
- **Statut** : ⬜ À FAIRE  
- **Type** : Core  
- **Dépendances** : (optionnel) US-005  
- **But** : stocker un joueur (nom + caractéristiques) pour éviter de ressaisir les scores

---

|-------------------------------------------------------------------------------------|
|-----# US-012 — Gestion de profils (plusieurs joueurs)-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P3  
- **Statut** : ⬜ À FAIRE  
- **Type** : Core + UI  
- **Dépendances** : US-011  

---

|-------------------------------------------------------------------------------------|
|-----# US-013 — Mode “tables” (dés custom / tables de loot)-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P3  
- **Statut** : ⬜ À FAIRE  
- **Type** : Core + Data  
- **Dépendances** : US-008 + US-011 (si lié à un joueur)  
- **But** : lancer un “dé” qui mappe vers une table

---

|-------------------------------------------------------------------------------------|
|-----# US-014 — Modèle Entity (PJ / PNJ / Monstre) — préparation DB/API-----|
|-------------------------------------------------------------------------------------|

- **Priorité** : P3  
- **Statut** : ⬜ À FAIRE  
- **Type** : Core (modèle)  
- **Dépendances** : US-011 (optionnel)  
- **But** : poser une classe mère “Entity” commune (stats, PV, vitesse, etc.) et des variantes (Player / NPC / Monster)
