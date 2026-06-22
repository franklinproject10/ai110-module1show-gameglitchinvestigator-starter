import sys
from pathlib import Path

# Ensure project root is on sys.path so logic_utils can be imported
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from logic_utils import check_guess, parse_guess


def test_check_guess_too_high():
    outcome, message = check_guess(80, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_check_guess_too_low():
    outcome, message = check_guess(20, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_check_guess_correct():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_parse_guess_valid():
    ok, val, err = parse_guess("42")
    assert ok is True
    assert val == 42
    assert err is None


def test_parse_guess_empty():
    ok, val, err = parse_guess("")
    assert ok is False
    assert val is None
    assert isinstance(err, str)
