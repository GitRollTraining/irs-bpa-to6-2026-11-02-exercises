"""Tests of the late-payment penalty rule, in payment_job/rules.py."""
from payment_job.rules import late_payment_penalty


def test_one_month_late() -> None:
    assert late_payment_penalty(1, 1000) == 10
