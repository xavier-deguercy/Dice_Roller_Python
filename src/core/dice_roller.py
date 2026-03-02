"""
Moteur de lancer de des pour l'application Dice Roller.

Idee directrice:
- le core contient la logique metier (tirages, validations, regles d20),
- l'UI se contente de fournir des entrees et d'afficher le resultat.
"""

import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class RuleOptionRequest:
    """Decrit une option de regle officielle appliquee a un lancer."""

    name: str
    die_faces: int | None = None


@dataclass(frozen=True)
class RollRequest:
    """
    Requete metier explicite pour decrire un lancer.

    Ce contrat separe :
    - les donnees du lancer,
    - le mode de jet,
    - le type de jet,
    - les options de regles eventuelles.
    """

    die_faces: int
    count: int = 1
    roll_mode: str = "normal"
    roll_kind: str = "generic_roll"
    official_options: tuple[RuleOptionRequest, ...] = ()


@dataclass(frozen=True)
class D100RollDetail:
    """Details d'un d100 represente comme 2d10 (dizaines + unites)."""

    tens: int
    ones: int
    value: int


@dataclass(frozen=True)
class RuleEffect:
    """Trace structurée d'une option de regle appliquee au lancer."""

    name: str
    effect_type: str
    applied: bool
    added_rolls: tuple[int, ...] = ()
    added_value: int = 0
    rerolled_from: int | None = None
    rerolled_to: int | None = None
    note: str = ""


@dataclass(frozen=True)
class RollStrategyResult:
    """Resultat intermediaire produit par une strategie de lancer."""

    strategy: str
    rolls: tuple[int, ...]
    final_value: int
    die_faces: int
    count: int
    d100_rolls: tuple[D100RollDetail, ...] = ()


@dataclass(frozen=True)
class RollResult:
    """Resultat metier complet et stable renvoye par le core."""

    die_faces: int
    count: int
    roll_mode: str
    roll_kind: str
    official_options: tuple[str, ...]
    rolls: tuple[int, ...]
    selected: int | None
    base_value: int
    bonus_total: int
    final_value: int
    critical: str | None
    is_d20_special: bool
    d100_rolls: tuple[D100RollDetail, ...] = ()
    rule_effects: tuple[RuleEffect, ...] = ()


class RollStrategy(ABC):
    """Contrat minimal pour une strategie de lancer."""

    @abstractmethod
    def roll(self, roller: "DiceRoller", nb_faces: int) -> RollStrategyResult:
        """Retourne un resultat intermediaire de lancer."""


class NormalRollStrategy(RollStrategy):
    """Lancer classique (1 de)."""

    def roll(self, roller: "DiceRoller", nb_faces: int) -> RollStrategyResult:
        value = roller.roll_die(nb_faces)
        return RollStrategyResult(
            strategy="normal",
            rolls=(value,),
            final_value=value,
            die_faces=nb_faces,
            count=1,
        )


class AdvantageRollStrategy(RollStrategy):
    """Lancer avec avantage (2 des, garder le meilleur)."""

    def roll(self, roller: "DiceRoller", nb_faces: int) -> RollStrategyResult:
        rolls = (roller.roll_die(nb_faces), roller.roll_die(nb_faces))
        return RollStrategyResult(
            strategy="avantage",
            rolls=rolls,
            final_value=max(rolls),
            die_faces=nb_faces,
            count=1,
        )


class DisadvantageRollStrategy(RollStrategy):
    """Lancer avec desavantage (2 des, garder le moins bon)."""

    def roll(self, roller: "DiceRoller", nb_faces: int) -> RollStrategyResult:
        rolls = (roller.roll_die(nb_faces), roller.roll_die(nb_faces))
        return RollStrategyResult(
            strategy="desavantage",
            rolls=rolls,
            final_value=min(rolls),
            die_faces=nb_faces,
            count=1,
        )


class RuleOptionHandler(ABC):
    """Contrat pour les regles officielles appliquees apres le lancer de base."""

    name: str

    @abstractmethod
    def validate(
        self, roller: "DiceRoller", request: RollRequest, option: RuleOptionRequest
    ) -> None:
        """Valide qu'une option peut s'appliquer a la requete."""

    @abstractmethod
    def apply(
        self,
        roller: "DiceRoller",
        request: RollRequest,
        result: RollResult,
        option: RuleOptionRequest,
    ) -> tuple[RollResult, RuleEffect]:
        """Applique l'option a un resultat et retourne l'effet produit."""


class GuidanceRuleOptionHandler(RuleOptionHandler):
    """Applique Guidance a une ability check."""

    name = "guidance"

    def validate(
        self, roller: "DiceRoller", request: RollRequest, option: RuleOptionRequest
    ) -> None:
        if request.roll_kind != "ability_check":
            raise ValueError("guidance reserve a ability_check")
        if option.die_faces is not None:
            raise ValueError("guidance utilise un d4 fixe")

    def apply(
        self,
        roller: "DiceRoller",
        request: RollRequest,
        result: RollResult,
        option: RuleOptionRequest,
    ) -> tuple[RollResult, RuleEffect]:
        bonus = roller.roll_die(4)
        effect = RuleEffect(
            name=self.name,
            effect_type="bonus",
            applied=True,
            added_rolls=(bonus,),
            added_value=bonus,
            note="1d4",
        )
        updated_result = replace(
            result,
            bonus_total=result.bonus_total + bonus,
            final_value=result.final_value + bonus,
        )
        return updated_result, effect


class BardicInspirationRuleOptionHandler(RuleOptionHandler):
    """Applique Bardic Inspiration avec un de explicite."""

    name = "bardic_inspiration"
    _VALID_DICE = (6, 8, 10, 12)
    _VALID_ROLL_KINDS = ("ability_check", "attack_roll", "saving_throw")

    def validate(
        self, roller: "DiceRoller", request: RollRequest, option: RuleOptionRequest
    ) -> None:
        if request.roll_kind not in self._VALID_ROLL_KINDS:
            raise ValueError(
                "bardic_inspiration reserve a ability_check/attack_roll/saving_throw"
            )
        if option.die_faces not in self._VALID_DICE:
            raise ValueError("bardic_inspiration requiert un de de barde valide")

    def apply(
        self,
        roller: "DiceRoller",
        request: RollRequest,
        result: RollResult,
        option: RuleOptionRequest,
    ) -> tuple[RollResult, RuleEffect]:
        bonus = roller.roll_die(option.die_faces)
        effect = RuleEffect(
            name=self.name,
            effect_type="bonus",
            applied=True,
            added_rolls=(bonus,),
            added_value=bonus,
            note=f"1d{option.die_faces}",
        )
        updated_result = replace(
            result,
            bonus_total=result.bonus_total + bonus,
            final_value=result.final_value + bonus,
        )
        return updated_result, effect


class HeroicInspirationRuleOptionHandler(RuleOptionHandler):
    """Applique Heroic Inspiration comme une relance explicite."""

    name = "heroic_inspiration"

    def validate(
        self, roller: "DiceRoller", request: RollRequest, option: RuleOptionRequest
    ) -> None:
        if request.count != 1:
            raise ValueError("heroic_inspiration requiert count=1")
        if request.roll_mode != "normal":
            raise ValueError("heroic_inspiration requiert roll_mode=normal")
        if option.die_faces is not None:
            raise ValueError("heroic_inspiration n'utilise pas de de additionnel")

    def apply(
        self,
        roller: "DiceRoller",
        request: RollRequest,
        result: RollResult,
        option: RuleOptionRequest,
    ) -> tuple[RollResult, RuleEffect]:
        rerolled_from = (
            result.selected if result.selected is not None else result.base_value
        )
        rerolled_to, d100_detail = roller._roll_value_with_metadata(request.die_faces)
        rerolled_details = (d100_detail,) if d100_detail is not None else ()
        updated_result = replace(
            result,
            rolls=(rerolled_to,),
            selected=rerolled_to,
            base_value=rerolled_to,
            final_value=rerolled_to + result.bonus_total,
            critical=roller._compute_critical(
                request.die_faces,
                request.count,
                result.is_d20_special,
                rerolled_to,
            ),
            d100_rolls=rerolled_details,
        )
        effect = RuleEffect(
            name=self.name,
            effect_type="reroll",
            applied=True,
            rerolled_from=rerolled_from,
            rerolled_to=rerolled_to,
            note=f"d{request.die_faces}",
        )
        return updated_result, effect


class DiceRoller:
    """
    Moteur de lancer de des, sans dependance UI.

    API principale:
    - `roll_die`: lancer un de simple,
    - `roll`: helper bas niveau via une strategie,
    - `roll_many`: lancer N des identiques,
    - `roll_d20`: cas d20 via strategies,
    - `resolve_roll`: point d'entree metier via `RollRequest`.
    """

    DES_AUTORISES = [4, 6, 8, 10, 12, 20, 100]
    MODES_D20 = ("normal", "avantage", "desavantage")
    ROLL_KINDS = ("generic_roll", "ability_check", "attack_roll", "saving_throw")

    def __init__(self, rng=None) -> None:
        # Injection de RNG pour des tests deterministes.
        # En usage normal, on utilise le module random standard.
        self._rng = rng if rng is not None else random
        self._strategies = {
            "normal": NormalRollStrategy(),
            "avantage": AdvantageRollStrategy(),
            "desavantage": DisadvantageRollStrategy(),
        }
        self._rule_option_handlers = {
            "guidance": GuidanceRuleOptionHandler(),
            "bardic_inspiration": BardicInspirationRuleOptionHandler(),
            "heroic_inspiration": HeroicInspirationRuleOptionHandler(),
        }

    def _validate_count(self, count: int) -> None:
        """Valide le nombre de des pour les lancers NdY."""
        if not isinstance(count, int) or count < 1:
            raise ValueError("count doit etre un entier >= 1")

    def _validate_d20_mode(self, roll_mode: str) -> None:
        """Valide le mode de jet d20."""
        if roll_mode not in self.MODES_D20:
            raise ValueError("mode de jet invalide")

    def _validate_roll_kind(self, roll_kind: str) -> None:
        """Valide le type metier du jet."""
        if roll_kind not in self.ROLL_KINDS:
            raise ValueError("type de lancer invalide")

    def _normalize_official_options(
        self,
        official_options: (
            tuple[RuleOptionRequest, ...]
            | list[RuleOptionRequest]
            | tuple[str, ...]
            | list[str]
            | RuleOptionRequest
            | str
            | None
        ),
    ) -> tuple[RuleOptionRequest, ...]:
        """Normalise les options officielles vers des objets explicites."""
        if official_options is None:
            return ()
        if isinstance(official_options, RuleOptionRequest):
            return (official_options,)
        if isinstance(official_options, str):
            return (RuleOptionRequest(name=official_options),)

        normalized_options = []
        for option in official_options:
            if isinstance(option, RuleOptionRequest):
                normalized_options.append(option)
            elif isinstance(option, str):
                normalized_options.append(RuleOptionRequest(name=option))
            else:
                raise ValueError("official_options contient un type invalide")
        return tuple(normalized_options)

    def _validate_official_option_names(
        self, official_options: tuple[RuleOptionRequest, ...]
    ) -> None:
        """Valide que les noms d'options sont connus."""
        invalid_options = [
            option.name
            for option in official_options
            if option.name not in self._rule_option_handlers
        ]
        if invalid_options:
            raise ValueError(
                "option officielle invalide : " + ", ".join(sorted(invalid_options))
            )

    def _roll_percentile(self) -> tuple[int, D100RollDetail]:
        """Genere un d100 comme 2d10 (dizaines + unites)."""
        tens_digit = self._rng.randint(0, 9)
        ones_digit = self._rng.randint(0, 9)
        tens = tens_digit * 10
        value = tens + ones_digit
        if value == 0:
            value = 100
        return value, D100RollDetail(tens=tens, ones=ones_digit, value=value)

    def _roll_value_with_metadata(
        self, nb_faces: int
    ) -> tuple[int, D100RollDetail | None]:
        """Retourne la valeur d'un de et, si besoin, ses metadonnees d'affichage."""
        if nb_faces == 100:
            value, detail = self._roll_percentile()
            return value, detail
        return self._rng.randint(1, nb_faces), None

    def _compute_critical(
        self, die_faces: int, count: int, is_d20_special: bool, base_value: int
    ) -> str | None:
        """Calcule l'etat critique pour un resultat d20 retenu."""
        is_single_d20 = die_faces == 20 and (count == 1 or is_d20_special)
        if not is_single_d20:
            return None
        if base_value == 20:
            return "success"
        if base_value == 1:
            return "failure"
        return None

    def _resolve_base_roll(self, request: RollRequest) -> RollResult:
        """Construit le resultat de base avant application des regles officielles."""
        if request.die_faces != 20 and request.roll_mode != "normal":
            raise ValueError("avantage/desavantage reserve au d20")
        if (
            request.die_faces == 20
            and request.roll_mode in ("avantage", "desavantage")
            and request.count != 1
        ):
            raise ValueError("count doit etre 1 en mode avantage/desavantage")

        is_d20_special = (
            request.die_faces == 20
            and request.roll_mode in ("avantage", "desavantage")
        )

        if is_d20_special:
            details = self.roll_d20(request.roll_mode)
            rolls = details.rolls
            base_value = details.final_value
            selected = details.final_value
            d100_rolls = ()
        else:
            details = self.roll_many(request.die_faces, request.count)
            rolls = details.rolls
            base_value = details.final_value
            selected = rolls[0] if request.count == 1 else None
            d100_rolls = details.d100_rolls

        return RollResult(
            die_faces=request.die_faces,
            count=request.count,
            roll_mode=request.roll_mode,
            roll_kind=request.roll_kind,
            official_options=tuple(option.name for option in request.official_options),
            rolls=rolls,
            selected=selected,
            base_value=base_value,
            bonus_total=0,
            final_value=base_value,
            critical=self._compute_critical(
                request.die_faces,
                request.count,
                is_d20_special,
                base_value,
            ),
            is_d20_special=is_d20_special,
            d100_rolls=d100_rolls,
        )

    def roll_die(self, nb_faces: int) -> int:
        """Lance un de simple dX."""
        if nb_faces not in self.DES_AUTORISES:
            raise ValueError(f"De non supporte : d{nb_faces}")
        value, _detail = self._roll_value_with_metadata(nb_faces)
        return value

    def roll(self, nb_faces: int, strategy: str = "normal") -> RollStrategyResult:
        """Helper bas niveau qui delegue a une strategie nommee."""
        if strategy not in self._strategies:
            raise ValueError(f"Strategie invalide : {strategy}")
        return self._strategies[strategy].roll(self, nb_faces)

    def roll_d20(self, roll_mode: str = "normal") -> RollStrategyResult:
        """Lance un d20 selon un mode (normal/avantage/desavantage)."""
        self._validate_d20_mode(roll_mode)
        return self.roll(20, roll_mode)

    def roll_many(self, nb_faces: int, count: int) -> RollStrategyResult:
        """Lance N des de meme type et calcule le total."""
        self._validate_count(count)
        rolls: list[int] = []
        d100_rolls: list[D100RollDetail] = []

        for _ in range(count):
            value, detail = self._roll_value_with_metadata(nb_faces)
            rolls.append(value)
            if detail is not None:
                d100_rolls.append(detail)

        return RollStrategyResult(
            strategy="many",
            die_faces=nb_faces,
            count=count,
            rolls=tuple(rolls),
            final_value=sum(rolls),
            d100_rolls=tuple(d100_rolls),
        )

    def resolve_roll(self, request: RollRequest) -> RollResult:
        """
        Point d'entree metier complet pour l'UI et la CLI.

        Gere dans le core:
        - le type de lancer,
        - le mode d20 (normal/avantage/desavantage),
        - les critiques d20,
        - les options officielles via une abstraction dediee,
        - un resultat structure pour le formatage UI.
        """
        if not isinstance(request, RollRequest):
            raise TypeError("resolve_roll attend un RollRequest")

        normalized_options = self._normalize_official_options(request.official_options)
        normalized_request = replace(request, official_options=normalized_options)

        # 1) Validation des entrees metier.
        self._validate_count(normalized_request.count)
        self._validate_d20_mode(normalized_request.roll_mode)
        self._validate_roll_kind(normalized_request.roll_kind)
        self._validate_official_option_names(normalized_options)

        # 2) Resolution du jet principal.
        result = self._resolve_base_roll(normalized_request)

        # 3) Application separee des options de regles.
        for option in normalized_options:
            handler = self._rule_option_handlers[option.name]
            handler.validate(self, normalized_request, option)
            result, effect = handler.apply(self, normalized_request, result, option)
            result = replace(result, rule_effects=result.rule_effects + (effect,))

        return result


def main():
    print("=== Dice Roller - core ===")
    roller = DiceRoller()
    print(f"Des autorises : {roller.DES_AUTORISES}")
    print(roller.resolve_roll(RollRequest(die_faces=6)))
    print(roller.resolve_roll(RollRequest(die_faces=20, roll_mode="avantage")))


if __name__ == "__main__":
    main()
