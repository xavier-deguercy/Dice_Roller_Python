# Rapport de revue technique

## 0) Donnees d'entree prises en compte

- Fichiers analyses :
  - [README.md](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/README.md)
  - [docs/03-backlog/product_backlog.md](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/docs/03-backlog/product_backlog.md)
  - [docs/04-sprints/05-sprint/backlog-sprint.md](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/docs/04-sprints/05-sprint/backlog-sprint.md)
  - [pyproject.toml](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/pyproject.toml)
  - [requirements.txt](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/requirements.txt)
  - [src/core/dice_roller.py](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py)
  - [src/v1_console/cli.py](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v1_console/cli.py)
  - [src/v2_gui/app_tk.py](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v2_gui/app_tk.py)
  - [src/main.py](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/main.py)
  - [tests/test_dice_roller.py](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/tests/test_dice_roller.py)
- Verifications executees :
  - `python -m pytest -q -p no:cacheprovider` : 11 tests passent
  - `python -m ruff check src tests` : 1 ecart + warning de configuration
  - `python -m flake8 src tests --jobs=1` : 1 ecart
  - executions CLI simples pour valider le comportement observable
- Hypotheses :
  - [docs/00-vision/vision-projet.md](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/docs/00-vision/vision-projet.md) et [docs/01-pre-projet/cdc-fonctionnel.md](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/docs/01-pre-projet/cdc-fonctionnel.md) sont presents mais vides ; le backlog et le README ont donc servi de source fonctionnelle principale.
  - L'inspiration est supposee autorisee sur tous les jets tant qu'aucune regle metier plus precise n'est fournie ; si elle doit etre reservee au d20, il y a un ecart fonctionnel.
  - Aucune contrainte de volumetrie ou de SLA n'est fournie ; l'analyse performance reste donc limitee au perimetre actuel.

## 1) Resume executif

Le module implemente un moteur de lancer de des D&D mutualise entre un coeur metier, une CLI et une interface Tkinter, avec `DiceRoller.resolve_roll(...)` comme point d'entree metier annonce. La separation core/UI est globalement saine : le coeur ne depend pas de Tkinter et les deux interfaces reutilisent bien le meme moteur. En revanche, l'API publique du core n'est pas encore coherente : `roll()` accepte toujours des combinaisons metier interdites alors que `resolve_roll()` les refuse. Le pattern Strategy est en place, mais partiellement seulement, car la strategie multi-des n'existe pas et la methode centrale garde encore une orchestration conditionnelle importante. Le lanceur principal importe l'interface graphique trop tot, ce qui couple inutilement le mode CLI a la disponibilite de Tkinter. Le formatage du resultat est duplique entre la CLI et la GUI, ce qui cree un risque de derive fonctionnelle. La base de tests actuelle est utile et passe, mais elle reste incomplète et ne couvre pas encore la CLI, le lanceur principal ni plusieurs cas limites metier. Enfin, l'outillage de qualite n'est pas "vert" : `ruff` et `flake8` signalent tous deux un ecart dans `src/main.py`.

Recommandations prioritaires :

- Verrouiller une seule API publique metier pour supprimer les chemins qui permettent des etats illegaux.
- Finaliser reellement la refacto Strategy avec une vraie strategie multi-des et un contrat de resultat explicite.
- Introduire un objet de resultat type pour remplacer les `dict` heterogenes.
- Mutualiser le formatage des messages entre CLI et GUI.
- Mettre l'outillage de qualite et la documentation de developpement en coherence avec l'etat reel du depot.

## 2) Alignement avec le contexte

### Exigences couvertes

- **US-002** : des supportes (`d4`, `d6`, `d8`, `d10`, `d12`, `d20`, `d100`) via [src/core/dice_roller.py#L80](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L80).
- **US-003** : lancers multiples via [src/core/dice_roller.py#L126](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L126).
- **US-004** : critiques d20 via [src/core/dice_roller.py#L179](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L179).
- **US-UI-001** : interface Tkinter minimale via [src/v2_gui/app_tk.py](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v2_gui/app_tk.py).
- **US-UI-002** : avantage/desavantage d20 et bonus d'inspiration sont exposes dans l'UI et geres par le core.

### Exigences partiellement couvertes

- **US-TECH-001** :
  - la separation UI/core est globalement correcte ;
  - les constantes ne sont pas dupliquees au sens metier ;
  - mais le backlog Sprint 5 demande explicitement un `constants.py`, absent du depot.
- **US-TECH-002** :
  - des strategies existent pour `normal`, `avantage`, `desavantage` ;
  - `MultiRollStrategy` n'existe pas, alors que le sprint la demande explicitement.
- **US-009** :
  - un socle de tests core existe ;
  - la couverture reste incomplete sur les criteres d'acceptation et ne couvre pas la CLI ni le lanceur principal.

### Ecarts vs backlog / specs

- Le backlog produit et le backlog Sprint 5 marquent **US-TECH-001**, **US-TECH-002** et **US-009** comme "a faire", alors que le code en implemente deja une partie. La documentation de pilotage n'est donc plus parfaitement alignee avec l'etat reel du code.
- Le backlog Sprint 5 demande explicitement :
  - un fichier `constants.py` ;
  - une `MultiRollStrategy` ;
  - un socle de tests couvrant les AC essentiels.
  Ces objectifs ne sont pas encore pleinement atteints dans la forme demandee.

### Risques projet

- Dette de conception avant **US-005** / **US-006** : l'API actuelle et les retours en `dict` vont se complexifier rapidement.
- Risque de regression silencieuse : logique de rendu dupliquee, erreurs GUI masquees, couverture de tests encore trop concentree sur le core.
- Risque de traçabilite : vision et cahier des charges vides, donc faible lisibilite des contraintes non fonctionnelles.

## 3) Analyse technique detaillee

### 3.1 Correctness & fiabilite

- `resolve_roll()` valide correctement :
  - `n >= 1`
  - `mode` valide
  - interdiction de `avantage/desavantage` hors d20
  - obligation de `n == 1` en mode d20 special
- Point faible principal : `roll()` reste public et accepte encore `roller.roll(10, "desavantage")`, ce qui contourne les regles metier de `resolve_roll()`.
- La fonction de demonstration du module illustre meme ce cas invalide :
  - [src/core/dice_roller.py#L212](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/core/dice_roller.py#L212)
- Cote CLI :
  - les `ValueError` sont converties en message utilisateur + code retour `2`, ce qui est propre.
- Cote GUI :
  - `except Exception` capture tout sans log ;
  - cela evite un crash visible, mais masque les erreurs de programmation.
- Cas ambigu :
  - l'inspiration est appliquee a tous les jets par le core ;
  - l'UI laisse aussi cette option visible hors d20 ;
  - si la regle metier vise uniquement le d20, l'implementation actuelle n'est pas conforme.

### 3.2 Design & lisibilite

- Points positifs :
  - bonne separation entre coeur metier, CLI et GUI ;
  - injection du RNG dans le core, bon choix pour la testabilite ;
  - code globalement lisible et nommage correct.
- Limites de design :
  - l'API metier est fragmentee entre `roll()`, `roll_d20()`, `roll_many()` et `resolve_roll()`;
  - ces methodes exposent des structures de resultat differentes ;
  - cela augmente le couplage implicite entre appelants et implementation.
- Le pattern Strategy est incomplet :
  - presence de strategies pour `normal`, `avantage`, `desavantage` ;
  - absence de strategie pour le multi-des ;
  - orchestration conditionnelle encore centralisee dans `resolve_roll()`.
- La logique de formatage est dupliquee presque a l'identique entre :
  - [src/v1_console/cli.py#L54](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v1_console/cli.py#L54)
  - [src/v2_gui/app_tk.py#L191](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/v2_gui/app_tk.py#L191)
- Les retours en `dict` reposent sur une convention informelle plutot que sur un contrat de type explicite.

### 3.3 Performance & scalabilite

- `roll_many()` est en **O(n)** en temps et **O(n)** en memoire, ce qui est normal puisqu'il conserve tous les tirages.
- Aucune operation couteuse ni I/O externe n'apparait dans le perimetre actuel.
- Le principal point d'attention n'est pas un hotspot, mais l'absence de borne cote core/CLI sur `n` :
  - l'UI borne le champ a `50`,
  - mais le core et la CLI acceptent n'importe quel entier >= 1.
- Le choix d'un seul RNG cote core est pertinent et aligne avec le backlog Sprint 5 ("un seul RNG").

### 3.4 Qualite Python & dette technique

- Compatibilite Python :
  - la cible **Python 3.11** est coherente avec l'usage de `Sequence[str] | None`.
- Dette principale :
  - retours en `dict` non types ;
  - `rng` non type ;
  - absence de `TypedDict`, `dataclass` ou contrat formel de resultat ;
  - cela reduit l'aide IDE et la surete de refacto.
- Outillage :
  - `ruff` remonte un import non trie dans [src/main.py#L11](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/main.py#L11)
  - `flake8` remonte aussi un probleme sur le commentaire inline de cette meme ligne
  - `ruff` signale egalement que `select` est configure au mauvais endroit dans [pyproject.toml#L5](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/pyproject.toml#L5)
- Documentation de dev :
  - le README documente `ruff` et `flake8`,
  - mais [requirements.txt#L1](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/requirements.txt#L1) ne contient que `pytest`,
  - l'installation d'un environnement de developpement n'est donc pas totalement reproductible.

### 3.5 Securite & conformite

- Surface d'attaque faible dans le perimetre actuel :
  - pas de reseau ;
  - pas d'acces fichier sensible ;
  - pas de secrets ;
  - uniquement des entrees numeriques.
- Aucun risque d'injection evident dans l'etat actuel.
- Le principal sujet de "conformite" ici est la conformite :
  - au backlog ;
  - aux conventions d'outillage ;
  - aux regles metier explicites ou implicites.

### 3.6 Testabilite

- Point fort :
  - l'injection du RNG dans `DiceRoller` permet des tests deterministes simples.
- Limite actuelle :
  - plusieurs tests utilisent encore `random.seed()` global ;
  - cela introduit un couplage plus fragile que l'usage systematique d'un RNG injecte.
- La GUI est moins testable car elle :
  - instancie elle-meme `DiceRoller` ;
  - melange orchestration UI et formatage.
- Aucun test ne couvre :
  - la CLI ;
  - le lanceur principal ;
  - l'alignement du rendu entre CLI et GUI ;
  - la dependance implicite a Tkinter.

## 4) Propositions d'amelioration (sans code reecrit)

| Intitule | Constat | Pourquoi c'est un probleme | Proposition | Justification Python | Impact attendu | Effort | Risque | Dependances / prerequis |
|---|---|---|---|---|---|---|---|---|
| Verrouiller une API publique unique du core | `roll()` permet encore des etats metier interdits et coexiste avec plusieurs points d'entree | Un appelant peut contourner les invariants sans le vouloir ; la maintenance devient plus fragile | Definir un seul point d'entree public metier et rendre les helpers de bas niveau internes ou strictement valides | Une API etroite reduit les etats illegaux et facilite test, typage et evolution | Robustesse, coherence metier, reduction des regressions | M | moyen | Arbitrer le perimetre exact de l'inspiration et du contrat metier |
| Finaliser le pattern Strategy | Le multi-des ne passe pas par une strategie et `resolve_roll()` reste centralement conditionnel | L'ajout de nouvelles US fera grossir le nombre de branches et le couplage | Ajouter une strategie dediee au multi-des et faire porter a chaque strategie la responsabilite du resultat metier | La polymorphie remplace utilement la croissance de `if/else` metier en Python | Extensibilite, lisibilite, dette technique reduite | M | moyen | Stabiliser l'API cible du core |
| Structurer les payloads de sortie | Tous les retours sont des `dict` heterogenes et implicites | Risque d'erreur sur les cles, faible aide IDE, refacto fragile | Introduire un objet de requete et un objet de resultat explicites (`dataclass` ou `TypedDict`) | `dataclass` et `typing` sont des bonnes pratiques pour formaliser un contrat d'echange | Maintenabilite, qualite de refacto, meilleure testabilite | M | faible | Peut etre mene en meme temps que la refacto API |
| Decoupler le mode CLI de Tkinter dans le lanceur | [src/main.py#L15](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/src/main.py#L15) importe la GUI au chargement | Le mode CLI depend inutilement d'une brique graphique | Deplacer l'import GUI dans la branche non-CLI | En Python, les imports ont des effets de bord ; les retarder evite des dependances inutiles | Portabilite, robustesse en environnement headless | S | faible | Aucun |
| Mutualiser le formatage du resultat | La construction du message est dupliquee entre CLI et GUI | Toute evolution doit etre reporte a deux endroits, avec risque de divergence | Extraire un formatter/presenter partage | Le principe DRY est pertinent ici car la logique est quasi identique | Coherence UX, maintenance simplifiee | S | faible | Plus simple avec un resultat structure |
| Rendre les erreurs GUI observables | `except Exception` masque tout sans journalisation | Les erreurs techniques deviennent difficiles a diagnostiquer | Limiter les exceptions capturees pour l'utilisateur et journaliser les inattendues | Separer erreur utilisateur et erreur technique est une pratique saine pour une app desktop | Debug plus simple, fiabilite percue accrue | S | faible | Definir une politique minimale de logging |
| Mettre l'outillage et les tests au meme niveau que le code | `pytest` passe mais `ruff` / `flake8` echouent ; les tests restent tres centres sur le core | Le depot donne une impression de stabilite superieure a la realite | Corriger les ecarts lint, migrer la config Ruff, ajouter tests CLI/lanceur, formaliser les dependances de dev | Un pipeline fiable suppose des checks reels, verts et reproductibles | Reduction des regressions, confiance de livraison | M | faible | Clarifier le standard d'outillage retenu |

### Quick wins

- Decoupler l'import Tkinter dans le lanceur principal.
- Mutualiser le formatter de resultat.
- Journaliser les exceptions inattendues cote GUI.
- Remettre `ruff` / `flake8` au vert.

### Refactor structurant

- Unifier l'API publique metier.
- Completer effectivement le pattern Strategy.
- Introduire des objets types de requete / resultat.

## 5) Plan de qualite (sans ecrire les tests)

### Tests unitaires essentiels

- `test_public_roll_rejects_non_d20_advantage`
  - verifier qu'aucune API publique n'autorise avantage/desavantage hors d20
- `test_resolve_roll_rejects_special_d20_mode_when_count_gt_1`
  - couvrir explicitement la regle `n == 1`
- `test_resolve_roll_inspiration_scope`
  - figer le comportement attendu de l'inspiration sur d20 vs non-d20
- `test_roll_result_contract_shape`
  - valider la forme exacte du resultat (champs presents et invariants)
- `test_formatter_outputs_same_message_for_same_result`
  - garantir un rendu identique entre CLI et GUI si un formatter partage est introduit
- `test_gui_unexpected_exception_is_logged`
  - verifier que les erreurs techniques ne sont pas seulement masquees

### Tests d'integration / contract tests

- Tester `python -m src.v1_console.cli` :
  - cas valide
  - cas invalide
  - code retour attendu
- Tester `python -m src.main --cli ...`
  - meme contrat de sortie que la CLI directe
- Tester le lanceur en contexte "sans GUI disponible"
  - verifier que le mode CLI ne casse pas si Tkinter est absent, une fois le couplage corrige

### Checks outillage

- `python -m pytest -q -p no:cacheprovider`
- `python -m ruff check src tests`
- `python -m flake8 src tests --jobs=1` si `flake8` est conserve
- `mypy` si le contrat de donnees est formalise
- couverture cible en CI (par exemple 85 % sur le core)
- execution CI sur Python 3.11, cible actuellement declaree

## 6) Questions bloquantes

Aucune question bloquante.

## Documents a demander si absents (sans bloquer)

- Une version renseignee de [docs/00-vision/vision-projet.md](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/docs/00-vision/vision-projet.md) et de [docs/01-pre-projet/cdc-fonctionnel.md](C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/docs/01-pre-projet/cdc-fonctionnel.md), actuellement vides.
- Un cahier des charges technique explicite ou une ADR sur l'API cible du core.
- Les regles metier precises sur :
  - le perimetre de l'inspiration
  - les bornes attendues de `n`
- Les contraintes de volumetrie / SLA, meme minimales.
- Une convention outillage claire :
  - `ruff` seul ou `ruff + flake8`
  - `mypy` oui/non
  - seuil de couverture
  - gestion des dependances de developpement
