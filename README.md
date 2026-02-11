# Dice Roller Python (D&D)

Application Python pour lancer des des de type Dungeons & Dragons, avec:
- un moteur metier (`src/core`)
- une interface Tkinter (`src/v2_gui`)
- un mode console (`src/v1_console`)

Le projet est pilote en mode Scrum. Le backlog produit est dans `docs/03-backlog/product_backlog.md`.

## Etat actuel

Fonctionnalites disponibles:
- des supportes: d4, d6, d8, d10, d12, d20, d100
- lancers multiples `NdY`
- mode d20: `normal`, `avantage`, `desavantage`
- critiques d20 (1 et 20)
- inspiration bardique (+1d4)

## Architecture rapide

- `src/core/dice_roller.py`
  - coeur metier, sans dependance UI
  - point d'entree principal: `DiceRoller.resolve_roll(...)`
- `src/v2_gui/app_tk.py`
  - interface Tkinter
  - lit les entrees utilisateur et affiche le resultat
- `src/v1_console/cli.py`
  - interface ligne de commande
  - reutilise le meme coeur metier
- `src/main.py`
  - lanceur principal (GUI par defaut, CLI avec `--cli`)

## Prerequis

- Python 3.11+ recommande
- Tkinter disponible (inclus par defaut sur la plupart des installations Python)

## Lancer l'application

Depuis la racine du depot.

Mode GUI (recommande):

```bash
python -m src.main
```

Mode GUI direct:

```bash
python -m src.v2_gui.app_tk
```

Mode CLI via le lanceur principal:

```bash
python -m src.main --cli --dice 20 --count 1 --mode normal
```

Mode CLI direct:

```bash
python -m src.v1_console.cli --dice 20 --count 1 --mode avantage --inspiration
```

## Exemples CLI

Jet simple:

```bash
python -m src.v1_console.cli --dice 6
```

Jet multiple:

```bash
python -m src.v1_console.cli --dice 8 --count 3
```

Jet d20 avec avantage + inspiration:

```bash
python -m src.v1_console.cli --dice 20 --mode avantage --inspiration
```

Jet reproductible (debug/test):

```bash
python -m src.v1_console.cli --dice 20 --mode normal --seed 42
```

## Tests et qualite

Lancer les tests:

```bash
python -m pytest -q
```

Lancer les verifications statiques principales:

```bash
python -m ruff check src tests
python -m flake8 src tests --jobs=1
```

## Documentation projet

- Vision: `docs/00-vision/vision-projet.md`
- Cahier des charges: `docs/01-pre-projet/cdc-fonctionnel.md`
- Backlog produit: `docs/03-backlog/product_backlog.md`
- Sprints: `docs/04-sprints/`

## Notes

- Les fichiers `*_legacy.py` sont des anciennes versions conservees temporairement.
- Les rapports d'analyse statique sont generes dans `reports/` (ignore par Git).
