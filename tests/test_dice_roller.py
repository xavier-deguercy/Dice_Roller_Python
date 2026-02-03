import random

import pytest

from src.core.dice_roller import DiceRoller


def test_roll_normal_strategy_returns_consistent_shape():
    random.seed(0)
    roller = DiceRoller()
    result = roller.roll(6, "normal")

    assert result["strategy"] == "normal"
    assert result["die_faces"] == 6
    assert len(result["rolls"]) == 1
    assert result["final_value"] == result["rolls"][0]
    assert 1 <= result["final_value"] <= 6


def test_roll_advantage_strategy_keeps_max():
    random.seed(1)
    roller = DiceRoller()
    result = roller.roll(20, "avantage")

    assert result["strategy"] == "avantage"
    assert len(result["rolls"]) == 2
    assert result["final_value"] == max(result["rolls"])


def test_roll_disadvantage_strategy_keeps_min():
    random.seed(2)
    roller = DiceRoller()
    result = roller.roll(20, "desavantage")

    assert result["strategy"] == "desavantage"
    assert len(result["rolls"]) == 2
    assert result["final_value"] == min(result["rolls"])


def test_roll_d20_delegates_to_strategy():
    random.seed(3)
    roller = DiceRoller()
    result = roller.roll_d20("normal")

    assert result["strategy"] == "normal"
    assert result["die_faces"] == 20
    assert len(result["rolls"]) == 1


def test_roll_many_returns_total_and_count():
    random.seed(4)
    roller = DiceRoller()
    result = roller.roll_many(8, 3)

    assert result["strategy"] == "many"
    assert result["die_faces"] == 8
    assert result["count"] == 3
    assert len(result["rolls"]) == 3
    assert result["final_value"] == sum(result["rolls"])


def test_roll_rejects_invalid_strategy():
    roller = DiceRoller()
    with pytest.raises(ValueError, match="Stratégie invalide"):
        roller.roll(6, "critique")


def test_roll_rejects_invalid_die():
    roller = DiceRoller()
    with pytest.raises(ValueError, match="Dé non supporté"):
        roller.roll_die(7)


def test_roll_many_rejects_invalid_count():
    roller = DiceRoller()
    with pytest.raises(ValueError, match="n doit être un entier >= 1"):
        roller.roll_many(6, 0)
