"""Write the day's report."""
from pathlib import Path

from payment_job import settings
from payment_job.reader import Account


def write_report(path: str, lines: list[tuple[Account, float]]) -> None:
    """Write one line for each account and its penalty, under the report's title.

    Args:
        path: the report file to write.
        lines: each account with its penalty, in dollars.
    """
    from payment_job.rules import RATE

    rows = [f"{settings.SETTINGS['report_title']}, at {RATE:.0%} a month"]
    rows += [f"{account.account_id}  {account.area}  {penalty:10.2f}" for account, penalty in lines]
    Path(path).write_text("\n".join(rows) + "\n", encoding="utf-8")
