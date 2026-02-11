import random
from abc import ABC, abstractmethod


class RollStrategy(ABC):
    """Contrat de stratégie pour un lancer de dé.

    Pattern Strategy :
    - On définit une interface commune (roll) pour plusieurs variantes d'un même
      comportement.
    - On délègue l'exécution à une implémentation concrète choisie dynamiquement.
    """

    @abstractmethod
    def roll(self, roller: "DiceRoller", nb_faces: int) -> dict:
        """Retourne un dict décrivant le lancer."""


class NormalRollStrategy(RollStrategy):
    """Lancer classique (1 dé).

    Implémentation concrète de la stratégie "normal".
    """

    def roll(self, roller: "DiceRoller", nb_faces: int) -> dict:
        value = roller.roll_die(nb_faces)
        return {
            "strategy": "normal",
            "rolls": [value],
            "final_value": value,
            "die_faces": nb_faces,
        }


class AdvantageRollStrategy(RollStrategy):
    """Lancer avec avantage (2 dés, garder le meilleur).

    Implémentation concrète de la stratégie "avantage".
    """

    def roll(self, roller: "DiceRoller", nb_faces: int) -> dict:
        rolls = [roller.roll_die(nb_faces), roller.roll_die(nb_faces)]
        return {
            "strategy": "avantage",
            "rolls": rolls,
            "final_value": max(rolls),
            "die_faces": nb_faces,
        }


class DisadvantageRollStrategy(RollStrategy):
    """Lancer avec désavantage (2 dés, garder le moins bon).

    Implémentation concrète de la stratégie "desavantage".
    """

    def roll(self, roller: "DiceRoller", nb_faces: int) -> dict:
        rolls = [roller.roll_die(nb_faces), roller.roll_die(nb_faces)]
        return {
            "strategy": "desavantage",
            "rolls": rolls,
            "final_value": min(rolls),
            "die_faces": nb_faces,
        }


# ici on vas definir la classe DiceRoller
class DiceRoller:  # classe pour gérer le lancer de dés
    DES_AUTORISES = [4, 6, 8, 10, 12, 20, 100]  # liste des dés autorisés

    def __init__(self) -> None:
        # Dictionnaire de stratégies :
        # la clé = nom choisi par l'appelant, la valeur = objet stratégie.
        # Exemple : roll(20, "avantage") -> AdvantageRollStrategy.
        self._strategies = {
            "normal": NormalRollStrategy(),
            "avantage": AdvantageRollStrategy(),
            "desavantage": DisadvantageRollStrategy(),
        }

    def roll_die(self, nb_faces: int) -> int:  # méthode pour lancer un dé
        if nb_faces not in self.DES_AUTORISES:
            raise ValueError(f"Dé non supporté : d{nb_faces}")

        return random.randint(1, nb_faces)

    def roll(self, nb_faces: int, strategy: str = "normal") -> dict:
        """Applique une stratégie de lancer sur un type de dé.

        Point d'entrée Strategy :
        - On choisit la stratégie via son nom.
        - On délègue le calcul à l'objet stratégie correspondant.
        """
        if strategy not in self._strategies:
            raise ValueError(f"Stratégie invalide : {strategy}")

        # Délégation : la stratégie fait le travail, DiceRoller reste le contexte.
        return self._strategies[strategy].roll(self, nb_faces)

    def roll_d20(self, mode: str = "normal") -> dict:
        """
        Retourne un dict standardisé pour que l'UI puisse afficher des détails.
        mode: "normal" | "avantage" | "desavantage"
        """
        if mode not in ("normal", "avantage", "desavantage"):
            raise ValueError("mode d20 invalide")

        # On réutilise le pattern Strategy pour d20.
        info = self.roll(20, mode)
        return {
            "strategy": info["strategy"],
            "die_faces": 20,
            "rolls": info["rolls"],
            "final_value": info["final_value"],
        }

    def roll_many(self, nb_faces: int, n: int) -> dict:
        if not isinstance(n, int) or n < 1:
            raise ValueError("n doit être un entier >= 1")

        rolls = [self.roll_die(nb_faces) for _ in range(n)]
        total = sum(rolls)
        return {
            "strategy": "many",
            "die_faces": nb_faces,
            "count": n,
            "rolls": rolls,
            "final_value": total,
        }


def main():  # fonction principale
    print("=== Dice Roller - US-002 (OOP) ===")  # titre de l'application
    roller = DiceRoller()  # création d'une instance de DiceRoller

    print(f"Dés autorisés : {roller.DES_AUTORISES}")  # afficher les dés autorisés
    print(roller.roll(6, "normal"))
    print(roller.roll(20, "avantage"))
    print(roller.roll(10, "desavantage"))
