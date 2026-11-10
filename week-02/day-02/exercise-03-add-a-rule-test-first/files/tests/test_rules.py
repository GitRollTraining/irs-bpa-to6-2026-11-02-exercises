"""Tests of the late-payment penalty rule, in payment_job/rules.py."""
import pytest

from payment_job.reader import Account
from payment_job.rules import late_payment_penalty, penalty_for


@pytest.mark.parametrize(
    "months_late, unpaid_tax, expected",
    [
        pytest.param(0, 1000, 0, id="on-time"),
        pytest.param(1, 1000, 10, id="first-month-late"),
        pytest.param(5, 1000, 50, id="inside-1-to-10"),
        pytest.param(10, 1000, 100, id="last-month-before-cap"),
        pytest.param(11, 1000, 100, id="first-capped-month"),
        pytest.param(5, 0, 0, id="nothing-owed"),
    ],
)
def test_late_payment_penalty(months_late: int, unpaid_tax: float, expected: float) -> None:
    assert late_payment_penalty(months_late, unpaid_tax) == expected


def test_negative_months_is_an_error() -> None:
    with pytest.raises(ValueError):
        late_payment_penalty(-1, 1000)


def test_penalty_for_one_account() -> None:
    account = Account(account_id="A1", area="north", months_late=4, unpaid_tax=2000)
    assert penalty_for(account) == 80
