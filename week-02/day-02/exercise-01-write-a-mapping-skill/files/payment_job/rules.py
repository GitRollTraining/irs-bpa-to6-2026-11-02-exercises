"""The late-payment penalty rule."""
from payment_job import reader

RATE = 0.01  # 1 percent of the unpaid tax for each whole month late
CAP_MONTHS = 10  # the penalty stops growing after 10 months


def late_payment_penalty(months_late: int, unpaid_tax: float) -> float:
    """Return the late-payment penalty, in dollars.

    Args:
        months_late: whole months since the payment was due.
        unpaid_tax: the tax still unpaid, in dollars.

    Returns:
        1 percent of the unpaid tax for each month late, for at most 10 months; 0 when nothing is owed.

    Raises:
        ValueError: months_late is negative.
    """
    if months_late < 0:
        raise ValueError("months_late cannot be negative")
    if unpaid_tax <= 0:
        return 0.0
    months = min(months_late, CAP_MONTHS)
    return round(unpaid_tax * RATE * months, 2)


def penalty_for(account: reader.Account) -> float:
    """Return the penalty for one account of the day's file.

    Args:
        account: one row of the accounts file.

    Returns:
        The account's late-payment penalty, in dollars.
    """
    return late_payment_penalty(account.months_late, account.unpaid_tax)
