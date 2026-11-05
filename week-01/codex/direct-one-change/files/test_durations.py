import pytest

from durations import parse_duration


def test_hours_and_minutes() -> None:
    assert parse_duration("1h30m") == 5400


def test_seconds_only() -> None:
    assert parse_duration("45s") == 45


def test_rejects_an_unknown_unit() -> None:
    with pytest.raises(ValueError):
        parse_duration("3w")


def test_rejects_empty_text() -> None:
    with pytest.raises(ValueError):
        parse_duration("")
