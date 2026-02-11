"""
Moteur de lancer de des pour l'application Dice Roller.

Idee directrice:
- le core contient la logique metier (tirages, validations, regles d20),
- l'UI se contente de fournir des entrees et d'afficher le resultat.
"""

import random
from abc import ABC, abstractmethod


class RollStrategy(ABC):
    """
    Contrat minimal pour une strategie de lancer.

    Chaque strategie retourne un dictionnaire avec:
    - `strategy`: nom de la strategie appliquee,
    - `rolls`: valeurs individuelles obtenues,
    - `final_value`: valeur retenue pour la regle metier,
    - `die_faces`: type de de concerne.
    """

    @abstractmethod
    def roll(self, roller: "DiceRoller", nb_faces: int) -> dict:
        """Retourne un dict de resultat de lancer."""


class NormalRollStrategy(RollStrategy):
    """Lancer classique (1 de)."""

    def roll(self, roller: "DiceRoller", nb_faces: int) -> dict:
        value = roller.roll_die(nb_faces)
        return {
            "strategy": "normal",
            "rolls": [value],
            "final_value": value,
            "die_faces": nb_faces,
        }


class AdvantageRollStrategy(RollStrategy):
    """Lancer avec avantage (2 des, garder le meilleur)."""

    def roll(self, roller: "DiceRoller", nb_faces: int) -> dict:
        rolls = [roller.roll_die(nb_faces), roller.roll_die(nb_faces)]
        return {
            "strategy": "avantage",
            "rolls": rolls,
            "final_value": max(rolls),
            "die_faces": nb_faces,
        }


class DisadvantageRollStrategy(RollStrategy):
    """Lancer avec desavantage (2 des, garder le moins bon)."""

    def roll(self, roller: "DiceRoller", nb_faces: int) -> dict:
        rolls = [roller.roll_die(nb_faces), roller.roll_die(nb_faces)]
        return {
            "strategy": "desavantage",
            "rolls": rolls,
            "final_value": min(rolls),
            "die_faces": nb_faces,
        }


class DiceRoller:
    """
    Moteur de lancer de des, sans dependance UI.

    API principale:
    - `roll_die`: lancer un de simple,
    - `roll`: lancer via une strategie,
    - `roll_many`: lancer N des identiques,
    - `roll_d20`: cas d20 via strategies,
    - `resolve_roll`: point d'entree metier complet pour l'UI.
    """

    DES_AUTORISES = [4, 6, 8, 10, 12, 20, 100]
    MODES_D20 = ("normal", "avantage", "desavantage")

    def __init__(self, rng=None) -> None:
        # Injection de RNG pour des tests deterministes.
        # En usage normal, on utilise le module random standard.
        self._rng = rng if rng is not None else random
        self._strategies = {
            "normal": NormalRollStrategy(),
            "avantage": AdvantageRollStrategy(),
            "desavantage": DisadvantageRollStrategy(),
        }

    def _validate_count(self, n: int) -> None:
        """Valide le nombre de des pour les lancers NdY."""
        if not isinstance(n, int) or n < 1:
            raise ValueError("n doit etre un entier >= 1")

    def _validate_d20_mode(self, mode: str) -> None:
        """Valide le mode de jet d20."""
        if mode not in self.MODES_D20:
            raise ValueError("mode d20 invalide")

    def roll_die(self, nb_faces: int) -> int:
        """Lance un de simple dX."""
        if nb_faces not in self.DES_AUTORISES:
            raise ValueError(f"De non supporte : d{nb_faces}")
        return self._rng.randint(1, nb_faces)

    def roll(self, nb_faces: int, strategy: str = "normal") -> dict:
        """Lance un de en deleguant a une strategie nommee."""
        if strategy not in self._strategies:
            raise ValueError(f"Strategie invalide : {strategy}")
        return self._strategies[strategy].roll(self, nb_faces)

    def roll_d20(self, mode: str = "normal") -> dict:
        """Lance un d20 selon un mode (normal/avantage/desavantage)."""
        self._validate_d20_mode(mode)
        info = self.roll(20, mode)
        return {
            "strategy": info["strategy"],
            "die_faces": 20,
            "rolls": info["rolls"],
            "final_value": info["final_value"],
        }

    def roll_many(self, nb_faces: int, n: int) -> dict:
        """Lance N des de meme type et calcule le total."""
        self._validate_count(n)
        rolls = [self.roll_die(nb_faces) for _ in range(n)]
        total = sum(rolls)
        return {
            "strategy": "many",
            "die_faces": nb_faces,
            "count": n,
            "rolls": rolls,
            "final_value": total,
        }

    def resolve_roll(
        self,
        nb_faces: int,
        n: int = 1,
        mode: str = "normal",
        inspiration: bool = False,
    ) -> dict:
        """
        Point d'entree metier complet pour l'UI.

        Gere dans le core:
        - mode d20 (normal/avantage/desavantage),
        - critiques d20,
        - inspiration (+1d4),
        - resultat structure pour formatage UI.
        """
        # 1) Validation des entrees metier.
        self._validate_count(n)
        self._validate_d20_mode(mode)

        if nb_faces != 20 and mode != "normal":
            raise ValueError("avantage/desavantage reserve au d20")
        if nb_faces == 20 and mode in ("avantage", "desavantage") and n != 1:
            raise ValueError("n doit etre 1 en mode avantage/desavantage")

        # 2) Resolution du jet principal.
        is_d20_special = nb_faces == 20 and mode in ("avantage", "desavantage")

        if is_d20_special:
            details = self.roll_d20(mode)
            rolls = details["rolls"]
            base_value = details["final_value"]
            selected = details["final_value"]
        else:
            details = self.roll_many(nb_faces, n)
            rolls = details["rolls"]
            base_value = details["final_value"]
            # "selected" n'a un sens que pour un seul de ou un d20 special.
            selected = rolls[0] if n == 1 else None

        # 3) Detection critique (uniquement sur un resultat d20 unique retenu).
        critical = None
        is_single_d20 = nb_faces == 20 and (n == 1 or is_d20_special)
        if is_single_d20:
            if base_value == 20:
                critical = "success"
            elif base_value == 1:
                critical = "failure"

        # 4) Bonus optionnel d'inspiration.
        bonus = self.roll_die(4) if inspiration else 0

        # 5) Payload unique pour l'UI (formatage et affichage).
        return {
            "die_faces": nb_faces,
            "count": n,
            "mode": mode,
            "rolls": rolls,
            "selected": selected,
            "base_value": base_value,
            "bonus": bonus,
            "final_value": base_value + bonus,
            "critical": critical,
            "is_d20_special": is_d20_special,
        }


def main():
    print("=== Dice Roller - US-002 (OOP) ===")
    roller = DiceRoller()
    print(f"Des autorises : {roller.DES_AUTORISES}")
    print(roller.roll(6, "normal"))
    print(roller.roll(20, "avantage"))
    print(roller.roll(10, "desavantage"))


if __name__ == "__main__":
    main()
