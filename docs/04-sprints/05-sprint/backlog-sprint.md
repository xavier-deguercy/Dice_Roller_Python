# 005-sprint — Sprint Backlog (Sprint 5)
## Thème : Refacto “propre” + Pattern Strategy + socle de tests

> Objectif : remettre le **core** d’équerre, appliquer **Strategy** pour les différents modes de lancer,
> et sécuriser le tout avec des **tests**.
> Sprint majoritairement **tech** : on fiabilise l’existant pour préparer US-005/006 et l’animation.

---

## 🧾 Légende
- **Priorité**
  - **P0** : indispensable / bloque le reste
  - **P1** : forte valeur, prochaine itération
  - **P2** : confort / qualité
  - **P3** : préparation long terme
- **Statut**
  - ✅ **FAIT**
  - 🟡 **EN COURS**
  - ⬜ **À FAIRE**

---

## 🎯 Objectif du Sprint
1) **Séparer clairement** logique métier (core) et interface Tkinter (UI).  
2) Mettre en place un **Strategy minimal viable** pour encapsuler les modes de lancer.  
3) Avoir un **socle de tests** qui couvre les critères d’acceptation essentiels.

---

## 📦 In-Scope (ce sprint)
- Refacto core (API claire, constantes partagées, méthode multi-dés propre)
- Strategy pattern (normal / avantage / désavantage / multi)
- Pytest : couverture des critères d’acceptation du MVP

## 🚫 Out-of-Scope (ce sprint)
- Nouvelles features visibles (ex: animation “BG3-like”, historique UI, export)
- Modificateurs de caractéristiques (US-005) / DC (US-006) — seulement préparation technique si besoin

---

## 🧩 Items concernés (référence Product Backlog)
- US-TECH-001 / US-TECH-002 : **à livrer** (refacto + Strategy)
- US-009 : **à livrer** (tests)
- US-002 / US-003 / US-004 / US-UI-001 / US-UI-002 : déjà “FAIT” fonctionnellement, mais **à sécuriser**

---

## Backlog (tâches ordonnées)

### T0 — Analyse rapide de l’existant (cadrage refacto)
- **Priorité** : P0
- **Statut** : ⬜ À FAIRE
- **But** : lister ce qui est “mélangé” (core/UI), les incohérences d’API, et ce qui doit être stabilisé
- **Livrable** :
  - une note courte (markdown) : “problèmes → décisions → plan de refacto”
  - un mini schéma (Mermaid) “avant → après”

✅ **DoD**
- Liste des décisions actées (API core, constantes, stratégie, tests)

---

### T1 — Remettre le core d’équerre (bloquant)
- **Priorité** : P0
- **Statut** : ⬜ À FAIRE

Sous-tâches :
1) Corriger/fiabiliser `roll_many` (vraie méthode, indentation OK, logique stable)
2) Clarifier l’API core (choix unique) :
   - soit `DiceRoller(faces)` → méthodes simples
   - soit `DiceRoller.roll(request)` avec un objet de requête (**recommandé si Strategy**)
3) Ajouter `constants.py` (dés autorisés + modes) et **l’importer partout** (core + UI)
4) S’assurer que l’UI n’a **aucune logique métier dupliquée** (pas de RNG dans l’UI, pas de constantes en double)
5) Le core n’importe **jamais** Tkinter (dépendance à sens unique : UI → core)

✅ **DoD**
- `python -m src.v2_gui.app_tk` démarre sans exception liée au core
- Les constantes (dés autorisés / modes) sont définies **une seule fois** dans `constants.py`
- Core “clean” (pas de dépendance UI)

---

### T2 — Implémenter Strategy (minimum viable)
- **Priorité** : P1
- **Statut** : ⬜ À FAIRE
- **But** : encapsuler chaque façon de lancer (normal, avantage, désavantage, multi) dans une stratégie dédiée

Stratégies attendues (MVP) :
- `NormalRollStrategy`
- `D20AdvantageStrategy`
- `D20DisadvantageStrategy`
- `MultiRollStrategy` (NdY)

Règles :
- Le **contexte** (`DiceRoller`) choisit/délègue à la stratégie (mapping sur “mode”)
- L’UI ne fait que fournir les options (faces, n, mode…) et afficher le résultat

✅ **DoD**
- `DiceRoller.roll(.)` délègue à une stratégie (plus de “if/else” métier dans l’UI)
- Résultat structuré (ex: `rolls`, `final_value`, `die_faces`, `mode`, `meta`)

---

### T3 — Tests = critères d’acceptation (socle MVP)
- **Priorité** : P1
- **Statut** : ⬜ À FAIRE
- **But** : transformer les critères d’acceptation en tests Pytest

Tests minimum attendus :
- Dés supportés → résultat dans `[1..faces]`
- Dé non supporté → erreur claire (exception maîtrisée ou message standardisé)
- Indépendance des lancers → appels multiples donnent des résultats cohérents
- Multi-dés → `N` résultats + total
- Critiques d20 → tag/flag sur 1 et 20 uniquement (et jamais sur d6/d10/etc.)

✅ **DoD**
- `pytest` passe (suite minimale)
- CA MVP couverts au moins par 1 test (US-002, US-003, US-004)

---

### T4 — Mise à jour doc & exécution (propreté repo)
- **Priorité** : P2
- **Statut** : ⬜ À FAIRE

Sous-tâches :
- Mettre à jour le README : commandes de run, structure, “où est le core / où est l’UI”
- Ajouter/mettre à jour une note “architecture” (optionnel mais recommandé)
- Vérifier `.gitignore` (cache, build, etc.) si nécessaire

✅ **DoD**
- Un nouveau lecteur peut :
  - installer les dépendances
  - lancer l’UI
  - lancer les tests
  - comprendre où ajouter une nouvelle stratégie

---

## ✅ Definition of Done (Sprint)
- UI fonctionnelle (Tkinter) sur le core refactoré
- Strategy en place (au moins normal + multi + d20 adv/disadv)
- Tests Pytest : MVP couvert et passing
- Zéro duplication des constantes core/UI

---

## 📌 Risques / points d’attention
- Ne pas “casser” l’UI pendant la refacto : avancer par petites PR/commits
- Garder **un seul RNG** côté core (important pour préparer l’animation plus tard)
- Ne pas dériver vers la fiche perso (juste préparer le terrain)
