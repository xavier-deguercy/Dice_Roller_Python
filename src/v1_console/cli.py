"""
Point d'entree console pour Dice Roller.

Ce module expose un petit CLI autour de `DiceRoller.resolve_roll` afin que les
regles metier soient partagees entre l'interface graphique et la console.
"""

import argparse
import random
import sys
from typing import Sequence

from src.core.dice_roller import DiceRoller, RollRequest, RuleOptionRequest
from src.core.formatting import format_roll_result


def build_parser() -> argparse.ArgumentParser:
    """Construit le parseur CLI pour un lancer unique."""
    parser = argparse.ArgumentParser(
        prog="python -m src.v1_console.cli",
        description="Lance des des DnD depuis la ligne de commande.",
    )
    parser.add_argument(
        "--dice",
        type=int,
        default=20,
        help="Nombre de faces du de (ex: 4, 6, 8, 10, 12, 20, 100).",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Nombre de des a lancer.",
    )
    parser.add_argument(
        "--mode",
        choices=DiceRoller.MODES_D20,
        default="normal",
        help="Mode d20 (normal, avantage, desavantage).",
    )
    parser.add_argument(
        "--roll-kind",
        choices=DiceRoller.ROLL_KINDS,
        default="generic_roll",
        help=(
            "Type metier du jet "
            "(generic_roll, ability_check, attack_roll, saving_throw)."
        ),
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Graine RNG optionnelle pour un resultat reproductible.",
    )
    parser.add_argument(
        "--guidance",
        action="store_true",
        help="Applique Guidance (reserve a ability_check).",
    )
    parser.add_argument(
        "--bardic-die",
        type=int,
        choices=(6, 8, 10, 12),
        default=None,
        help="Applique Bardic Inspiration avec le de indique.",
    )
    parser.add_argument(
        "--heroic-inspiration",
        action="store_true",
        help="Applique Heroic Inspiration comme relance.",
    )
    return parser
def main(argv: Sequence[str] | None = None) -> int:
    """
    Execute une commande de lancer en console.

    Codes de retour:
    - 0: succes
    - 2: erreur de saisie utilisateur
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    rng = random.Random(args.seed) if args.seed is not None else None
    roller = DiceRoller(rng=rng)
    official_options: list[RuleOptionRequest] = []

    if args.guidance:
        official_options.append(RuleOptionRequest(name="guidance"))
    if args.bardic_die is not None:
        official_options.append(
            RuleOptionRequest(name="bardic_inspiration", die_faces=args.bardic_die)
        )
    if args.heroic_inspiration:
        official_options.append(RuleOptionRequest(name="heroic_inspiration"))

    request = RollRequest(
        die_faces=args.dice,
        count=args.count,
        roll_mode=args.mode,
        roll_kind=args.roll_kind,
        official_options=tuple(official_options),
    )

    try:
        details = roller.resolve_roll(request)
    except ValueError as exc:
        print(f"Erreur: {exc}", file=sys.stderr)
        return 2

    print(format_roll_result(details))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
