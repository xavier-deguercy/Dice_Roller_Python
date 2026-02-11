"""
Point d'entree principal de l'application.

Comportement par defaut:
- lance l'interface Tkinter.

Option:
- `--cli` execute un lancer unique en mode console.
"""

import argparse # https://docs.python.org/3/library/argparse.html
from typing import Sequence

from src.v1_console.cli import main as cli_main
from src.v2_gui.app_tk import DiceRollerApp


def build_parser() -> argparse.ArgumentParser:
    """Construit le parseur pour choisir le mode d'execution."""
    parser = argparse.ArgumentParser(
        prog="python -m src.main",
        description="Lance Dice Roller en mode GUI ou CLI.",
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Execute le mode console a la place de l'interface Tkinter.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """
    Redirige vers le mode GUI ou CLI.

    Exemples:
    - `python -m src.main` demarre l'interface.
    - `python -m src.main --cli --dice 20 --count 1` lance un jet en CLI.
    """
    parser = build_parser()
    args, remaining = parser.parse_known_args(argv)

    if args.cli:
        return cli_main(remaining)

    if remaining:
        parser.error("Les arguments CLI necessitent l'option --cli.")

    app = DiceRollerApp()
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
