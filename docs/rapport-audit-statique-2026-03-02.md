# AUDIT STATIQUE LOGICIEL — VERSION CABINET D’AUDIT

Date du rapport : 2026-03-02

---

# 1. POSITIONNEMENT

Ce rapport est produit dans une posture de **cabinet d’audit logiciel indépendant**.

Principes appliqués pour ce livrable :

- Analyse strictement statique
- Aucun lancement de l’application
- Aucune validation runtime
- Aucune hypothèse métier non déductible des documents fournis
- Constatations limitées aux éléments lisibles dans le dépôt

---

# 2. PÉRIMÈTRE DE L’AUDIT

## 2.1 Éléments analysés

- Fichiers source :
  - [src/core/dice_roller.py](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py)
  - [src/core/formatting.py](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/formatting.py)
  - [src/v1_console/cli.py](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v1_console/cli.py)
  - [src/v2_gui/app_tk.py](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v2_gui/app_tk.py)
  - [src/main.py](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/main.py)
- Arborescence :
  - `src/`
  - `tests/`
  - `docs/`
  - `.github/workflows/`
- Documents contextuels :
  - [docs/00-vision/vision-projet.md](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/docs/00-vision/vision-projet.md)
  - [docs/01-pre-projet/cdc-fonctionnel.md](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/docs/01-pre-projet/cdc-fonctionnel.md)
  - [docs/03-backlog/product_backlog.md](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/docs/03-backlog/product_backlog.md)
  - [README.md](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/README.md)
- Autres éléments :
  - [pyproject.toml](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/pyproject.toml)
  - [requirements.txt](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/requirements.txt)
  - [.github/workflows/ci.yml](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/.github/workflows/ci.yml)
  - [tests/test_dice_roller.py](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/tests/test_dice_roller.py)
  - [tests/test_main_integration.py](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/tests/test_main_integration.py)

## 2.2 Limites du périmètre

- Éléments non fournis :
  - Aucun rapport de couverture
  - Aucun résultat CI historisé
  - Aucun schéma d’architecture
  - Aucun ADR technique
  - Aucun packaging/distribution final
- Impact sur le niveau de confiance :
  - L’analyse de robustesse réelle, de comportement GUI, de portabilité Tkinter et de conformité fonctionnelle effective reste partielle sans exécution ni artefacts d’observabilité.

## 2.3 Niveau de confiance de l’audit

- ☐ Élevé
- ☒ Modéré
- ☐ Limité

Justification :

Le code source principal, les tests, la documentation produit et un workflow CI minimal sont présents. En revanche, l’audit reste purement statique et ne permet ni de confirmer les comportements effectifs ni de mesurer les propriétés non observables à la lecture seule.

---

# 3. SYNTHÈSE EXÉCUTIVE

## 3.1 Objet de l’audit

Évaluer, par lecture statique, la qualité structurelle, la cohérence documentaire, les risques techniques visibles et le niveau de maturité du projet `Dice Roller Python`, présenté comme un simulateur de lancers de dés D&D 5e 2024.

## 3.2 Résumé global

Le dépôt présente une base propre pour un MVP Python : séparation explicite entre cœur métier, CLI et GUI, structuration par dataclasses, présence de patterns identifiables (Strategy, handlers de règles, formatter partagé), documentation produit existante et CI minimale.  
La conception montre une intention claire d’industrialisation légère, cohérente avec un projet pédagogique de portfolio.

Deux écarts structurants réduisent toutefois la confiance :

- le contrat fonctionnel documenté “dés supportés uniquement” n’est pas appliqué uniformément dans le cœur métier ;
- la documentation de backlog n’est plus alignée avec l’état visible du code sur plusieurs US marquées `A FAIRE` alors que des implémentations existent déjà.

Le projet est donc techniquement au-dessus du prototype brut, mais pas encore stabilisé au niveau de la traçabilité et de la robustesse métier.

## 3.3 Principaux risques identifiés

- 🔴 **Violation observable du contrat fonctionnel sur la validation des dés** : `resolve_roll()` ne valide pas explicitement `die_faces`, et le chemin `roll_many()` accepte statiquement des faces non prévues ([src/core/dice_roller.py#L488](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L488), [src/core/dice_roller.py#L509](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L509)).
- 🔴 **Traçabilité produit dégradée** : le backlog annonce `US-TECH-003`, `US-015`, `US-016`, `US-017` comme `A FAIRE`, alors que le code contient déjà des handlers, des options CLI et des contrôles UI correspondants ([docs/03-backlog/product_backlog.md#L266](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/docs/03-backlog/product_backlog.md#L266), [src/core/dice_roller.py#L168](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L168), [src/v1_console/cli.py#L56](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v1_console/cli.py#L56), [src/v2_gui/app_tk.py#L163](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v2_gui/app_tk.py#L163)).
- 🟠 **Durcissement incomplet de l’architecture** : certaines règles restent dupliquées entre core et UI, et la GUI masque les exceptions techniques par un `except Exception` générique ([src/core/dice_roller.py#L208](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L208), [src/v2_gui/app_tk.py#L32](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v2_gui/app_tk.py#L32), [src/v2_gui/app_tk.py#L329](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v2_gui/app_tk.py#L329)).

## 3.4 Évaluation synthétique

| Critère | Score (/10) | Commentaire synthétique |
|---------------|------------|--------------------------|
| Maintenabilité | 7 | Structure claire et patterns visibles, mais duplication de règles UI/core et backlog désaligné. |
| Robustesse | 5 | Validations partielles ; un trou de validation métier sur `die_faces` est visible. |
| Sécurité | 7 | Faible surface d’attaque, peu d’I/O ; la principale faiblesse visible reste la validation d’entrée incomplète. |
| Scalabilité | 5 | Suffisant pour un MVP local ; modèle O(n) acceptable, mais absence de borne centrale sur `count` et stockage systématique des tirages. |

## 3.5 Niveau de maturité estimé

- ☐ Prototype
- ☒ MVP
- ☐ Pré-production
- ☐ Production-ready

Justification :

Le projet dispose d’un socle modulaire, d’une documentation produit, de tests et d’une CI minimale, ce qui dépasse un simple prototype. En revanche, des écarts de contrat métier et de gouvernance documentaire empêchent de le qualifier de pré-production.

## 3.6 Risque global projet

- ☐ Faible
- ☒ Modéré
- ☐ Élevé
- ☐ Critique

Justification :

Le risque n’est pas celui d’une architecture chaotique, mais celui d’une dérive de cohérence : ce que le produit prétend garantir n’est pas encore totalement sécurisé dans le core, et la documentation de pilotage ne reflète plus fidèlement l’implémentation visible.

---

# 4. ANALYSE DÉTAILLÉE

---

# 4.1 Analyse fonctionnelle déductible

## Faits observables

- Le produit est documenté comme un simulateur de lancers de dés D&D 5e 2024, centré sur un MVP local CLI + Tkinter ([docs/00-vision/vision-projet.md#L11](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/docs/00-vision/vision-projet.md#L11), [docs/01-pre-projet/cdc-fonctionnel.md#L17](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/docs/01-pre-projet/cdc-fonctionnel.md#L17)).
- Le cœur métier expose un point d’entrée structuré `DiceRoller.resolve_roll(RollRequest)` ([src/core/dice_roller.py#L509](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L509)).
- Les notions métier visibles sont :
  - type de dé
  - nombre de dés
  - mode de jet
  - type de jet
  - options officielles
- Les résultats sont structurés via `RollResult`, `RuleEffect` et `D100RollDetail` ([src/core/dice_roller.py#L41](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L41), [src/core/dice_roller.py#L50](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L50), [src/core/dice_roller.py#L76](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L76)).
- Le `d100` est explicitement modélisé en `2d10` dans le code ([src/core/dice_roller.py#L388](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L388)).
- La GUI et la CLI délèguent toutes deux au core et utilisent un formatter partagé ([src/v1_console/cli.py#L13](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v1_console/cli.py#L13), [src/v2_gui/app_tk.py#L13](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v2_gui/app_tk.py#L13), [src/core/formatting.py#L48](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/formatting.py#L48)).

## Hypothèses strictement déductibles

- Le projet cherche à faire converger code, backlog et documentation, mais cette convergence n’est pas terminée.
- Les règles “officielles” sont traitées comme options contextuelles et non comme bonus génériques.
- L’intention de design est clairement orientée “source de vérité dans le core”.

## Zones d’incertitude

- L’exacte conformité fonctionnelle n’est pas vérifiable sans exécution.
- Le comportement effectif de l’interface Tkinter (états des widgets, lisibilité réelle, ergonomie) n’est pas mesurable statiquement.
- La compatibilité multi-plateforme de Tkinter n’est pas vérifiable ici.
- La valeur réelle de la couverture de tests n’est pas mesurable sans exécution.

---

# 4.2 Analyse architecturale

## Organisation modulaire

- L’organisation est simple et cohérente :
  - `src/core` : logique métier et présentation textuelle partagée
  - `src/v1_console` : adaptation CLI
  - `src/v2_gui` : adaptation Tkinter
  - `src/main.py` : point d’entrée / routage de mode
- Le routage GUI/CLI est proprement découplé avec import GUI différé ([src/main.py#L42](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/main.py#L42), [src/main.py#L48](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/main.py#L48)).

## Cohésion / Couplage

- La cohésion du core est bonne : validation, résolution de base, application d’options et structure de résultat sont regroupées de façon logique.
- Le couplage UI/core reste raisonnable.
- Deux zones de couplage évitable subsistent :
  - duplication de la liste des dés de barde entre core et GUI ([src/core/dice_roller.py#L208](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L208), [src/v2_gui/app_tk.py#L32](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v2_gui/app_tk.py#L32))
  - duplication implicite des types de jet supportés entre `DiceRoller.ROLL_KINDS` et `ROLL_KIND_LABELS` ([src/core/dice_roller.py#L312](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L312), [src/v2_gui/app_tk.py#L26](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v2_gui/app_tk.py#L26))

## Respect des principes SOLID

### S — Single Responsibility

- Globalement respecté.
- `DiceRoller` concentre la logique métier.
- `formatting.py` centralise le rendu texte.
- `app_tk.py` reste toutefois une classe volumineuse mêlant construction UI, orchestration d’état et adaptation d’entrée.

### O — Open/Closed

- Partiellement respecté.
- L’ajout de règles officielles via `RuleOptionHandler` est extensible par dictionnaire de handlers ([src/core/dice_roller.py#L320](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L320)).
- L’ajout de nouveaux types de jet ou de nouvelles contraintes UI nécessitera encore des modifications directes dans plusieurs endroits.

### L — Liskov Substitution

- Aucun écart visible.
- Les sous-classes de `RollStrategy` et `RuleOptionHandler` respectent le contrat abstrait observé.

### I — Interface Segregation

- Correct.
- Les interfaces abstraites sont minimales et focalisées.

### D — Dependency Inversion

- Partiel.
- Le core accepte une injection de RNG ([src/core/dice_roller.py#L314](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L314)).
- En revanche, la GUI instancie directement `DiceRoller` et n’est pas injectée depuis un composition root ([src/v2_gui/app_tk.py#L41](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v2_gui/app_tk.py#L41)).

## Patterns identifiables

- Strategy :
  - `NormalRollStrategy`
  - `AdvantageRollStrategy`
  - `DisadvantageRollStrategy`
- Command/DTO-like request-response :
  - `RollRequest`
  - `RuleOptionRequest`
  - `RollResult`
- Handler polymorphe pour règles officielles :
  - `RuleOptionHandler` + implémentations
- Formatter partagé :
  - séparation partielle entre calcul et rendu

## Dépendances critiques

- `random` standard library comme source d’aléa métier
- `tkinter` comme dépendance GUI
- `argparse` pour le CLI
- `pytest` indiqué dans [requirements.txt](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/requirements.txt)
- `ruff` requis par CI mais non déclaré dans `requirements.txt` ([.github/workflows/ci.yml#L20](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/.github/workflows/ci.yml#L20), [requirements.txt](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/requirements.txt))

---

# 4.3 Analyse qualité du code

## Lisibilité

- Le code est lisible, docstringé et globalement bien structuré.
- Les dataclasses améliorent la compréhension des flux.
- Un léger défaut de qualité documentaire est visible avec une chaîne encodée incorrectement dans une docstring (`"Trace structurÃ©e"`) ([src/core/dice_roller.py#L52](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L52)).

## Nommage

- Le nommage métier est cohérent :
  - `roll_mode`
  - `roll_kind`
  - `official_options`
  - `rule_effects`
- La distinction entre `base_value`, `bonus_total` et `final_value` est claire.

## Complexité estimée

- Complexité faible à modérée.
- `resolve_roll()` reste le point le plus dense, mais demeure lisible grâce à la séparation validation / base roll / application des règles ([src/core/dice_roller.py#L509](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L509)).
- `app_tk.py` est plus dense, surtout autour de la gestion de l’état UI.

## Profondeur d’imbrication

- Faible dans le core.
- Modérée dans la GUI, sans excès critique.

## Duplication

- Duplication métier partielle visible :
  - dés de barde autorisés en core et en GUI
  - types de jet explicités dans le core et remappés en GUI
- Le formatter partagé a correctement supprimé la duplication CLI/GUI sur le rendu texte.

## Gestion des erreurs

- Le core lève des `ValueError` explicites sur plusieurs cas invalides.
- Le CLI convertit ces erreurs en message utilisateur sur `stderr` ([src/v1_console/cli.py#L106](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v1_console/cli.py#L106)).
- La GUI masque toute exception non prévue avec un `except Exception` générique, sans log ni distinction entre bug interne et erreur utilisateur ([src/v2_gui/app_tk.py#L327](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v2_gui/app_tk.py#L327)).

## Programmation défensive

- Positive :
  - validation de `count`
  - validation de `roll_mode`
  - validation de `roll_kind`
  - normalisation des options officielles
- Lacune majeure :
  - absence de validation centralisée et systématique de `die_faces` dans `resolve_roll()` et `roll_many()` ([src/core/dice_roller.py#L470](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L470), [src/core/dice_roller.py#L488](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L488), [src/core/dice_roller.py#L523](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L523)).

---

# 4.4 Analyse performance (statique)

## Algorithmes identifiés

- Lancer simple : O(1)
- Avantage / désavantage : O(1)
- Lancer multiple `NdY` : O(n)
- Application d’options officielles : O(k), `k` = nombre d’options

## Complexité asymptotique estimée

- `roll_many()` est en O(n) temps et O(n) mémoire, car toutes les valeurs sont stockées ([src/core/dice_roller.py#L488](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L488)).
- `resolve_roll()` est O(n + k) dans le cas général.

## Risques N² / N³

- Aucun risque N² / N³ visible dans le code analysé.

## Structures de données

- `tuple` pour les résultats structurés : bon choix pour l’immutabilité des retours.
- `list` transitoires dans `roll_many()` : pertinent avant conversion.
- `dict` pour registres de stratégies et handlers : approprié.

## Risques mémoire visibles

- Le cœur conserve tous les tirages individuels, ce qui est normal pour un affichage détaillé.
- Il n’existe pas de borne centralisée sur `count` dans le core ni dans le CLI ; seule l’UI borne son `Spinbox` à 50 ([src/v2_gui/app_tk.py#L99](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v2_gui/app_tk.py#L99)).
- En conséquence, un appel CLI ou direct peut demander un `count` très élevé, avec coût temps/mémoire non borné par contrat technique.

---

# 4.5 Analyse sécurité

Référentiel : OWASP Top 10 / CWE / Secure Coding

## Validation des entrées

- Validation présente sur :
  - `count`
  - `roll_mode`
  - `roll_kind`
  - noms d’options officielles
- Validation absente ou incomplète sur :
  - `die_faces` dans le chemin principal `resolve_roll()` / `roll_many()`

## Risques d’injection

- Aucun vecteur d’injection classique visible :
  - pas de SQL
  - pas de shell dans le code applicatif
  - pas de templates dynamiques
  - pas d’entrées réseau

## Gestion des secrets

- Aucun secret visible dans les fichiers analysés.

## Logging sensible

- Aucun mécanisme de logging structuré visible.
- Donc pas de fuite de secret observable, mais aussi faible observabilité en cas de défaut.

## Surface d’attaque visible

- Très réduite :
  - paramètres CLI
  - saisie GUI locale
- Le principal risque de “sécurité” ici est un défaut de validation conduisant à des états inattendus, pas une compromission classique.

Pour chaque point critique :

- Constat :
  - Le core n’applique pas uniformément la restriction documentaire sur les dés autorisés ([docs/01-pre-projet/cdc-fonctionnel.md#L76](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/docs/01-pre-projet/cdc-fonctionnel.md#L76), [src/core/dice_roller.py#L488](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L488)).
- Impact :
  - États métier invalides, résultats non conformes au contrat produit, affaiblissement de toute validation amont.
- Probabilité estimée :
  - Modérée à élevée, car le chemin est directement visible et public.
- Gravité :
  - Majeure.

---

# 4.6 Testabilité & industrialisation

## Injection de dépendances

- Bonne base côté core via injection de RNG ([src/core/dice_roller.py#L314](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L314)).
- Moins bon côté GUI, qui instancie son `DiceRoller` elle-même ([src/v2_gui/app_tk.py#L41](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v2_gui/app_tk.py#L41)).

## Isolation possible

- Le core est bien isolable.
- Le formatter est testable séparément.
- Le point d’entrée `src.main` est testable par subprocess, ce que la présence de `tests/test_main_integration.py` suggère.

## Couplage au framework

- Le core n’est pas couplé à Tkinter.
- La GUI est naturellement couplée à Tkinter, mais reste globalement une couche d’adaptation.

## Mockabilité

- Bonne dans le core.
- Moyenne dans la GUI sans injection du moteur ni couche contrôleur dédiée.

## Observabilité

- Faible :
  - pas de logging
  - pas de journalisation des erreurs GUI
  - pas de mécanisme de trace technique hors exceptions propagées au CLI

## Pré-requis CI/CD

- Présence d’un workflow GitHub Actions minimal ([.github/workflows/ci.yml](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/.github/workflows/ci.yml)).
- CI limitée à :
  - installation des dépendances
  - lint `ruff`
  - `pytest`
- Pas de :
  - matrice de versions Python
  - couverture
  - type-checking
  - packaging check
- `ruff` n’est pas versionné dans `requirements.txt`, ce qui réduit la reproductibilité locale stricte ([requirements.txt](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/requirements.txt), [.github/workflows/ci.yml#L23](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/.github/workflows/ci.yml#L23)).

---

# 5. DETTE TECHNIQUE STRUCTURÉE

---

## 🔴 Critique

| Constat | Risque | Effort estimé | Priorité |
|---------|--------|--------------|----------|
| `resolve_roll()` ne valide pas explicitement `die_faces`, et `roll_many()` accepte des faces hors liste autorisée | Non-conformité directe au CDC/backlog, résultats métier invalides, perte de confiance dans le contrat central | S | Immédiate |
| Backlog produit désaligné avec l’état visible du code (`US-TECH-003`, `US-015/016/017` marquées `A FAIRE` alors que le code les matérialise déjà) | Pilotage erroné, décisions de priorisation faussées, traçabilité dégradée | S | Immédiate |

---

## 🟠 Majeure

| Constat | Risque | Effort estimé | Priorité |
|---------|--------|--------------|----------|
| Borne technique absente sur `count` dans le core et le CLI | Coût temps/mémoire non borné via API/CLI, divergence avec l’UI | S | Haute |
| Duplication des règles de disponibilité (dés de barde, types de jet) entre core et GUI | Dérive de comportement lors d’une évolution | M | Haute |
| `except Exception` générique dans la GUI sans log | Débogage difficile, erreurs techniques masquées, observabilité faible | S | Haute |
| `roll_many` n’est pas encapsulé dans une stratégie dédiée alors que le backlog technique le cible explicitement | Architecture partiellement inachevée par rapport au référentiel projet | M | Moyenne |

---

## 🟢 Mineure

| Constat | Risque | Effort estimé | Priorité |
|---------|--------|--------------|----------|
| `ruff` utilisé en CI mais non déclaré dans les dépendances du projet | Environnement local moins reproductible | S | Moyenne |
| Fonction `main()` de démonstration conservée dans le module core | Bruit structurel, confusion sur les points d’entrée | S | Basse |
| Anomalie d’encodage dans une docstring | Dégradation mineure de lisibilité / crédibilité | S | Basse |

---

# 6. PLAN DE REMÉDIATION

---

## Phase 1 — Stabilisation immédiate

Actions prioritaires liées aux risques critiques.

- Introduire une validation centrale de `die_faces` dans `resolve_roll()` avant toute résolution.
- Faire en sorte que tous les chemins internes (`roll_many`, `_roll_value_with_metadata` ou un validateur dédié) passent par le même contrôle.
- Mettre à jour le backlog pour refléter l’état réel du code :
  - soit reclasser `US-TECH-003`, `US-015`, `US-016`, `US-017`
  - soit redéfinir leur DoD comme “stabilisation” si elles sont jugées incomplètes.
- Ajouter un test unitaire explicitement dédié au rejet d’un dé non supporté via `resolve_roll(RollRequest(...))`.

## Phase 2 — Refactorisation structurante

Améliorations architecturales et découplage.

- Centraliser les constantes métier exposées à l’UI :
  - dés de barde autorisés
  - types de jet exposables
- Réduire le couplage de `app_tk.py` :
  - isoler les règles d’activation/désactivation UI dans une petite couche de présentation dédiée
  - injecter le `DiceRoller` au lieu de l’instancier en dur si l’objectif est une testabilité GUI plus mature
- Compléter réellement l’abstraction Strategy si le backlog continue de l’exiger pour les lancers multiples.
- Supprimer ou déplacer la fonction de démonstration `main()` du module core.

## Phase 3 — Industrialisation

- Stratégie de tests :
  - compléter les tests unitaires sur validation de contrat
  - ajouter des tests ciblés du formatter (sans subprocess)
  - isoler si possible des tests de logique GUI non visuelle
- CI/CD :
  - versionner aussi les outils de dev (`ruff`) dans un groupe de dépendances clair
  - ajouter une métrique de couverture
  - envisager une matrice Python si le projet vise plus qu’un seul runtime
- Monitoring :
  - non prioritaire pour ce type de MVP local
- Observabilité :
  - introduire un logging minimal, au moins pour les exceptions GUI inattendues
- Optimisation performance :
  - définir une borne centrale de `count` ou un garde-fou de volumétrie
  - documenter cette borne dans le CDC et le backlog

---

# 7. LIMITES DE L’AUDIT

- Éléments non analysables en statique :
  - comportement effectif des tirages
  - rendu réel de l’interface Tkinter
  - stabilité runtime multi-OS
  - qualité effective des messages affichés en usage réel
- Hypothèses non vérifiables :
  - conformité exacte des options officielles à la règle attendue en exécution
  - qualité réelle de l’expérience utilisateur
- Risques non mesurables sans exécution :
  - performance réelle sur volumes élevés
  - comportement en environnement Tkinter absent
  - régressions non détectées par les tests existants

---

# 8. RÉFÉRENTIELS UTILISÉS

- SOLID
- Clean Code
- Clean Architecture
- OWASP Top 10
- CWE
- Bonnes pratiques Python observables dans le code
- Complexité algorithmique standard

---

# 9. MÉTHODOLOGIE D’ÉVALUATION DES SCORES

Les scores sont attribués selon :

- Respect visible des principes d’architecture
- Cohésion et couplage observables
- Complexité statiquement estimable
- Présence de programmation défensive
- Gestion lisible des erreurs
- Exposition potentielle aux états invalides
- Cohérence entre code, documentation et backlog
- Niveau d’industrialisation visible (tests, outillage, CI)

Notation qualitative convertie en score /10.

---

# FIN DU RAPPORT
