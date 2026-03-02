import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _run_main(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "src.main", *args],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        check=False,
    )


def test_main_cli_mode_executes_single_roll_successfully():
    completed = _run_main(
        "--cli",
        "--dice",
        "20",
        "--count",
        "1",
        "--seed",
        "42",
    )

    assert completed.returncode == 0
    assert completed.stdout.strip() == "d20 -> 4"
    assert completed.stderr == ""


def test_main_cli_mode_applies_guidance_on_ability_check():
    completed = _run_main(
        "--cli",
        "--dice",
        "20",
        "--count",
        "1",
        "--roll-kind",
        "ability_check",
        "--guidance",
        "--seed",
        "42",
    )

    assert completed.returncode == 0
    assert completed.stdout.strip() == "d20 -> 4 | Guidance (1d4=1) -> total 5"
    assert completed.stderr == ""


def test_main_cli_mode_applies_bardic_inspiration_bonus():
    completed = _run_main(
        "--cli",
        "--dice",
        "20",
        "--count",
        "1",
        "--roll-kind",
        "attack_roll",
        "--bardic-die",
        "8",
        "--seed",
        "42",
    )

    assert completed.returncode == 0
    assert completed.stdout.strip() == (
        "d20 -> 4 | Bardic Inspiration (1d8=1) -> total 5"
    )
    assert completed.stderr == ""


def test_main_cli_mode_applies_heroic_inspiration_reroll():
    completed = _run_main(
        "--cli",
        "--dice",
        "20",
        "--count",
        "1",
        "--heroic-inspiration",
        "--seed",
        "2",
    )

    assert completed.returncode == 0
    assert completed.stdout.strip() == (
        "d20 -> 3 | Heroic Inspiration (d20): 2 -> 3 -> total 3"
    )
    assert completed.stderr == ""


def test_main_cli_mode_formats_d100_with_2d10_details():
    completed = _run_main(
        "--cli",
        "--dice",
        "100",
        "--count",
        "1",
        "--seed",
        "42",
    )

    assert completed.returncode == 0
    assert "d100 ->" in completed.stdout
    assert "2d10:" in completed.stdout
    assert "=" in completed.stdout
    assert completed.stderr == ""


def test_main_cli_mode_rejects_guidance_outside_ability_check():
    completed = _run_main(
        "--cli",
        "--dice",
        "20",
        "--count",
        "1",
        "--guidance",
        "--seed",
        "42",
    )

    assert completed.returncode == 2
    assert completed.stdout == ""
    assert "Erreur: guidance reserve a ability_check" in completed.stderr


def test_main_rejects_cli_arguments_without_cli_flag():
    completed = _run_main(
        "--dice",
        "20",
    )

    assert completed.returncode == 2
    assert completed.stdout == ""
    assert "Les arguments CLI necessitent l'option --cli." in completed.stderr
