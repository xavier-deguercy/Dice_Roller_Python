import random

import pytest

from src.core.dice_roller import (
    D100RollDetail,
    DiceRoller,
    RollRequest,
    RollResult,
    RollStrategyResult,
    RuleOptionRequest,
)


class FakeRng:
    def __init__(self, values):
        self._values = list(values)

    def randint(self, _a, _b):
        return self._values.pop(0)


def test_roll_normal_strategy_returns_consistent_shape():
    random.seed(0)
    roller = DiceRoller()
    result = roller.roll(6, "normal")

    assert isinstance(result, RollStrategyResult)
    assert result.strategy == "normal"
    assert result.die_faces == 6
    assert result.count == 1
    assert len(result.rolls) == 1
    assert result.final_value == result.rolls[0]
    assert 1 <= result.final_value <= 6


def test_roll_advantage_strategy_keeps_max():
    random.seed(1)
    roller = DiceRoller()
    result = roller.roll(20, "avantage")

    assert isinstance(result, RollStrategyResult)
    assert result.strategy == "avantage"
    assert len(result.rolls) == 2
    assert result.final_value == max(result.rolls)


def test_roll_disadvantage_strategy_keeps_min():
    random.seed(2)
    roller = DiceRoller()
    result = roller.roll(20, "desavantage")

    assert isinstance(result, RollStrategyResult)
    assert result.strategy == "desavantage"
    assert len(result.rolls) == 2
    assert result.final_value == min(result.rolls)


def test_roll_d20_delegates_to_strategy():
    random.seed(3)
    roller = DiceRoller()
    result = roller.roll_d20("normal")

    assert isinstance(result, RollStrategyResult)
    assert result.strategy == "normal"
    assert result.die_faces == 20
    assert len(result.rolls) == 1


def test_roll_many_returns_total_and_count():
    random.seed(4)
    roller = DiceRoller()
    result = roller.roll_many(8, 3)

    assert isinstance(result, RollStrategyResult)
    assert result.strategy == "many"
    assert result.die_faces == 8
    assert result.count == 3
    assert len(result.rolls) == 3
    assert result.final_value == sum(result.rolls)
    assert result.d100_rolls == ()


def test_roll_many_d100_returns_detailed_components():
    roller = DiceRoller(rng=FakeRng([7, 3, 0, 0]))
    result = roller.roll_many(100, 2)

    assert result.rolls == (73, 100)
    assert result.final_value == 173
    assert result.d100_rolls == (
        D100RollDetail(tens=70, ones=3, value=73),
        D100RollDetail(tens=0, ones=0, value=100),
    )


def test_roll_rejects_invalid_strategy():
    roller = DiceRoller()
    with pytest.raises(ValueError, match="Strategie invalide"):
        roller.roll(6, "critique")


def test_roll_rejects_invalid_die():
    roller = DiceRoller()
    with pytest.raises(ValueError, match="De non supporte"):
        roller.roll_die(7)


def test_roll_many_rejects_invalid_count():
    roller = DiceRoller()
    with pytest.raises(ValueError, match="count doit etre un entier >= 1"):
        roller.roll_many(6, 0)


def test_resolve_roll_request_d20_advantage_with_critical():
    roller = DiceRoller(rng=FakeRng([5, 20]))
    request = RollRequest(die_faces=20, count=1, roll_mode="avantage")
    result = roller.resolve_roll(request)

    assert isinstance(result, RollResult)
    assert result.is_d20_special is True
    assert result.rolls == (5, 20)
    assert result.selected == 20
    assert result.base_value == 20
    assert result.bonus_total == 0
    assert result.critical == "success"
    assert result.roll_kind == "generic_roll"
    assert result.official_options == ()
    assert result.final_value == 20


def test_resolve_roll_request_nd20_normal_does_not_trigger_critical():
    roller = DiceRoller(rng=FakeRng([10, 10]))
    request = RollRequest(die_faces=20, count=2)
    result = roller.resolve_roll(request)

    assert result.is_d20_special is False
    assert result.base_value == 20
    assert result.critical is None


def test_resolve_roll_request_d100_exposes_detailed_components():
    roller = DiceRoller(rng=FakeRng([8, 4]))
    request = RollRequest(die_faces=100)
    result = roller.resolve_roll(request)

    assert result.rolls == (84,)
    assert result.selected == 84
    assert result.base_value == 84
    assert result.d100_rolls == (D100RollDetail(tens=80, ones=4, value=84),)


def test_resolve_roll_request_rejects_advantage_for_non_d20():
    roller = DiceRoller()
    request = RollRequest(die_faces=8, roll_mode="avantage")
    with pytest.raises(ValueError, match="reserve au d20"):
        roller.resolve_roll(request)


def test_resolve_roll_rejects_non_request_input():
    roller = DiceRoller()
    with pytest.raises(TypeError, match="RollRequest"):
        roller.resolve_roll({"die_faces": 20})


def test_resolve_roll_request_rejects_invalid_roll_kind():
    roller = DiceRoller()
    request = RollRequest(die_faces=20, roll_kind="loot_table")
    with pytest.raises(ValueError, match="type de lancer invalide"):
        roller.resolve_roll(request)


def test_resolve_roll_request_guidance_applies_bonus_on_ability_check():
    roller = DiceRoller(rng=FakeRng([10, 3]))
    request = RollRequest(
        die_faces=20,
        roll_kind="ability_check",
        official_options=(RuleOptionRequest(name="guidance"),),
    )
    result = roller.resolve_roll(request)

    assert result.base_value == 10
    assert result.bonus_total == 3
    assert result.final_value == 13
    assert len(result.rule_effects) == 1
    assert result.rule_effects[0].name == "guidance"
    assert result.rule_effects[0].added_value == 3


def test_resolve_roll_request_rejects_guidance_outside_ability_check():
    roller = DiceRoller()
    request = RollRequest(
        die_faces=20,
        official_options=(RuleOptionRequest(name="guidance"),),
    )
    with pytest.raises(ValueError, match="guidance reserve a ability_check"):
        roller.resolve_roll(request)


def test_resolve_roll_request_bardic_inspiration_applies_bonus():
    roller = DiceRoller(rng=FakeRng([12, 6]))
    request = RollRequest(
        die_faces=20,
        roll_kind="attack_roll",
        official_options=(RuleOptionRequest(name="bardic_inspiration", die_faces=8),),
    )
    result = roller.resolve_roll(request)

    assert result.base_value == 12
    assert result.bonus_total == 6
    assert result.final_value == 18
    assert result.rule_effects[0].name == "bardic_inspiration"
    assert result.rule_effects[0].added_value == 6


def test_resolve_roll_request_rejects_invalid_bardic_die():
    roller = DiceRoller()
    request = RollRequest(
        die_faces=20,
        roll_kind="attack_roll",
        official_options=(RuleOptionRequest(name="bardic_inspiration", die_faces=4),),
    )
    with pytest.raises(ValueError, match="de de barde valide"):
        roller.resolve_roll(request)


def test_resolve_roll_request_heroic_inspiration_rerolls_and_updates_critical():
    roller = DiceRoller(rng=FakeRng([1, 20]))
    request = RollRequest(
        die_faces=20,
        official_options=(RuleOptionRequest(name="heroic_inspiration"),),
    )
    result = roller.resolve_roll(request)

    assert result.rolls == (20,)
    assert result.selected == 20
    assert result.base_value == 20
    assert result.final_value == 20
    assert result.critical == "success"
    assert result.rule_effects[0].rerolled_from == 1
    assert result.rule_effects[0].rerolled_to == 20


def test_resolve_roll_request_rejects_heroic_inspiration_on_multi_roll():
    roller = DiceRoller()
    request = RollRequest(
        die_faces=6,
        count=2,
        official_options=(RuleOptionRequest(name="heroic_inspiration"),),
    )
    with pytest.raises(ValueError, match="count=1"):
        roller.resolve_roll(request)
