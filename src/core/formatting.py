"""
Helpers de presentation partages entre CLI et GUI.

Ces fonctions consomment le resultat structure du core sans recalculer
de logique metier.
"""

from src.core.dice_roller import RollResult


def _format_d100_details(result: RollResult) -> str:
    """Construit une chaine lisible pour les details 2d10 d'un d100."""
    details = [
        f"{item.tens} + {item.ones} = {item.value}" for item in result.d100_rolls
    ]
    if result.count == 1:
        return details[0]
    return ", ".join(f"[{detail}]" for detail in details)


def _format_effect_label(effect_name: str) -> str:
    """Normalise le libelle d'un effet de regle pour l'affichage."""
    return effect_name.replace("_", " ").title()


def _format_bonus_effect(result: RollResult, effect) -> str:
    """Formate un effet additif applique au lancer."""
    option_label = _format_effect_label(effect.name)
    if effect.note and effect.added_rolls:
        added_rolls = "/".join(str(value) for value in effect.added_rolls)
        detail = f"{effect.note}={added_rolls}"
    else:
        detail = f"+{effect.added_value}"
    return f" | {option_label} ({detail}) -> total {result.final_value}"


def _format_reroll_effect(result: RollResult, effect) -> str:
    """Formate une relance appliquee au lancer."""
    option_label = _format_effect_label(effect.name)
    if effect.note:
        option_label = f"{option_label} ({effect.note})"
    return (
        f" | {option_label}: {effect.rerolled_from} -> "
        f"{effect.rerolled_to} -> total {result.final_value}"
    )


def format_roll_result(result: RollResult) -> str:
    """Transforme un resultat structure en message texte lisible."""
    if result.is_d20_special:
        msg = (
            f"d20 {result.roll_mode} -> {list(result.rolls)} "
            f"(retenu {result.selected})"
        )
    elif result.count == 1 and result.die_faces == 100 and result.d100_rolls:
        detail = _format_d100_details(result)
        msg = f"d100 -> {result.rolls[0]} (2d10: {detail})"
    elif result.count == 1:
        msg = f"d{result.die_faces} -> {result.rolls[0]}"
    elif result.die_faces == 100 and result.d100_rolls:
        detail = _format_d100_details(result)
        msg = (
            f"{result.count}d100 -> {list(result.rolls)} "
            f"(2d10: {detail}) (total {result.base_value})"
        )
    else:
        msg = (
            f"{result.count}d{result.die_faces} -> "
            f"{list(result.rolls)} (total {result.base_value})"
        )

    if result.critical == "success":
        msg = "Reussite critique ! " + msg
    elif result.critical == "failure":
        msg = "Echec critique ! " + msg

    for effect in result.rule_effects:
        if not effect.applied:
            continue

        if effect.effect_type == "bonus":
            msg += _format_bonus_effect(result, effect)
        elif effect.effect_type == "reroll":
            msg += _format_reroll_effect(result, effect)

    return msg
