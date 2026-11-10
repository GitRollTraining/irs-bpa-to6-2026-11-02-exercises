"""The late-payment penalty rule."""
from payment_job import reader

RATE = 0.01  # 1 percent of the unpaid tax for each whole month late
CAP_MONTHS = 10  # the penalty stops growing after 10 months
PENALTY_CAP = 500.0  # no account owes more than 500 dollars of penalty


class PenaltyCapPolicy:
    """Decide the most penalty one account can owe."""

    def __init__(self, cap: float = PENALTY_CAP, enabled: bool = True) -> None:
        """Keep the cap, and whether it applies.

        Args:
            cap: the most penalty one account can owe, in dollars.
            enabled: False turns the cap off.
        """
        self.cap = cap
        self.enabled = enabled

    def apply(self, penalty: float) -> float:
        """Return the penalty, cut to the cap when the cap applies."""
        if not self.enabled:
            return penalty
        return min(penalty, self.cap)


def late_payment_penalty(months_late: int, unpaid_tax: float) -> float:
    """Return the late-payment penalty, in dollars.

    Args:
        months_late: whole months since the payment was due.
        unpaid_tax: the tax still unpaid, in dollars.

    Returns:
        1 percent of the unpaid tax for each month late, for at most 10 months, and at most
        500 dollars; 0 when nothing is owed.

    Raises:
        ValueError: months_late is negative.
    """
    if months_late < 0:
        raise ValueError("months_late cannot be negative")
    if unpaid_tax <= 0:
        return 0.0
    months = min(months_late, CAP_MONTHS)
    return PenaltyCapPolicy().apply(round(unpaid_tax * RATE * months, 2))


def penalty_for(account: reader.Account) -> float:
    """Return the penalty for one account of the day's file.

    Args:
        account: one row of the accounts file.

    Returns:
        The account's late-payment penalty, in dollars; 0 when its area is on the relief list.
    """
    if account.area in reader.load_relief_areas():
        return 0.0
    return late_payment_penalty(account.months_late, account.unpaid_tax)
