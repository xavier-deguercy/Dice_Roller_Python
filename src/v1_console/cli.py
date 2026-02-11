"""
Point d'entree console pour Dice Roller.

Ce module expose un petit CLI autour de `DiceRoller.resolve_roll` afin que les
regles metier soient partagees entre l'interface graphique et la console.
"""

import argparse
import random
import sys
from typing import Sequence

from src.core.dice_roller import DiceRoller


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
        "--inspiration",
        action="store_true",
        help="Ajoute un bonus d'inspiration +1d4.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Graine RNG optionnelle pour un resultat reproductible.",
    )
    return parser


def format_roll_result(details: dict) -> str:
    """Transforme le resultat structure en message texte lisible."""
    if details["is_d20_special"]:
        msg = (
            f"d20 {details['mode']} -> {details['rolls']} "
            f"(retenu {details['selected']})"
        )
    elif details["count"] == 1:
        msg = f"d{details['die_faces']} -> {details['rolls'][0]}"
    else:
        msg = (
            f"{details['count']}d{details['die_faces']} -> "
            f"{details['rolls']} (total {details['base_value']})"
        )

    if details["critical"] == "success":
        msg = "Reussite critique ! " + msg
    elif details["critical"] == "failure":
        msg = "Echec critique ! " + msg

    if details["bonus"] > 0:
        msg += (
            f" | Inspiration +{details['bonus']} -> "
            f"Total {details['final_value']}"
        )

    return msg


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

    try:
        details = roller.resolve_roll(
            nb_faces=args.dice,
            n=args.count,
            mode=args.mode,
            inspiration=args.inspiration,
        )
    except ValueError as exc:
        print(f"Erreur: {exc}", file=sys.stderr)
        return 2

    print(format_roll_result(details))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
