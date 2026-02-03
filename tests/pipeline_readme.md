# Pipeline qualité — Dice Roller (première version)

> Positionnement : je t’écris comme un **dev senior / formateur senior**, avec une logique
> de **montée en compétence progressive**.  
> Objectif : te donner une **vision claire** d’un pipeline qualité réaliste, utile,
> et aligné avec ton projet actuel (core + IHM Tkinter).

---

## 1) À quoi sert un pipeline qualité ?

Un pipeline qualité sert à **attraper les bugs tôt**, **forcer de bonnes pratiques**
et **éviter la dette technique**.

Tu gagnes :
- de la **confiance** dans le code (moins de surprises),
- de la **lisibilité** (code homogène),
- une **évolution plus facile** (moins de régressions).

---

## 2) La logique d’un pipeline “pro” (simple, efficace)

On part d’un principe :
**plus c’est tôt dans le pipeline, plus c’est rapide et moins ça coûte.**

Donc on met en premier :
1) **Lint + format** → rapide, feedback immédiat  
2) **Tests unitaires** → logique métier validée  
3) **Analyse qualité / complexité** → dette technique  
4) **Audit sécurité** → vulnérabilités des dépendances  

---

## 3) Ce que je te recommande (version MVP)

### ✅ Étape 1 — Lint & Format
**But :** éviter les erreurs basiques et homogénéiser le code.

- **Ruff** (lint rapide)
- **Black** (formatage)

Pourquoi ?
- Ruff détecte vite les imports inutiles, noms incohérents, erreurs simples
- Black te garantit un style uniforme sans débat

### ✅ Étape 2 — Tests unitaires
**But :** valider la logique métier (cœur).

Ici, ce sont surtout :
- `roll()` par stratégie
- `roll_d20()`
- `roll_many()`
- cas invalides (stratégie inconnue, dé interdit, n < 1)

### ✅ Étape 3 — Qualité & dette technique
**But :** éviter que ton code devienne “trop compliqué”.

Outils recommandés :
- **Radon** (complexité)
- **Xenon** (seuils de complexité)

### ✅ Étape 4 — Sécurité dépendances
**But :** prévenir les dépendances vulnérables.

Outil :
- **pip-audit**

---

## 4) Pourquoi pas tout d’un coup ?

Parce que tu vas te décourager si tu installes 8 outils d’un coup.

Je te conseille :
1. Ruff + Black
2. Pytest
3. Radon / Xenon
4. pip-audit

Ça te donne un **pipeline progressif**, sans te noyer.

---

## 5) Exemple d’ordre d’exécution (conceptuel)

1. Ruff (lint)
2. Black (format check)
3. Pytest (unit tests)
4. Radon / Xenon (complexité)
5. pip-audit (sécurité)

Tu gagnes :
✅ rapidité  
✅ fiabilité  
✅ discipline  

---

## 6) Ce que tu peux ajouter plus tard (niveau intermédiaire)

- **Mypy** → typage statique
- **Pylint** → règles strictes (optionnel)
- **Coverage** → couverture de tests

---

## 7) Mini‑règles “pro” que je te conseille

- Pas de commit si Ruff ou Pytest échoue.
- Une PR = un objectif clair.
- Quand tu ajoutes une feature → tu ajoutes au moins 1 test.
- Si un fichier dépasse 200 lignes → pense à le découper.

---

Si tu veux, je peux te proposer **la version 2**, avec :
✅ un pipeline GitHub Actions  
✅ la config Ruff/Black/pytest  
✅ une checklist de validation avant merge  
