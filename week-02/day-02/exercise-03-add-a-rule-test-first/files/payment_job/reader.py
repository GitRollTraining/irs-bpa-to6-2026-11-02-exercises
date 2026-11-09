"""Read the day's file of accounts, and the relief list."""
import csv
from dataclasses import dataclass
from pathlib import Path

RELIEF_FILE = Path(__file__).resolve().parent.parent / "data" / "relief_areas.txt"


@dataclass
class Account:
    """One account of the day's file."""

    account_id: str
    area: str
    months_late: int
    unpaid_tax: float


def read_accounts(path: str) -> list[Account]:
    """Read the accounts file, one account a row.

    Args:
        path: the CSV file, with the columns account_id, area, months_late and unpaid_tax.

    Returns:
        The accounts, in the file's order.

    Raises:
        ValueError: a row has no id or area, or a negative number.
    """
    accounts = []
    with open(path, newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            if not row["account_id"] or not row["area"]:
                raise ValueError(f"A row has no account_id or area: {row}")
            months_late, unpaid_tax = int(row["months_late"]), float(row["unpaid_tax"])
            if months_late < 0 or unpaid_tax < 0:
                raise ValueError(f"Account {row['account_id']} has a negative number")
            accounts.append(Account(row["account_id"], row["area"], months_late, unpaid_tax))
    return accounts


def load_relief_areas(path: Path = RELIEF_FILE) -> set[str]:
    """Read the relief list: the areas whose accounts owe no penalty.

    Args:
        path: the relief file, one area a line.

    Returns:
        The areas on the list.
    """
    return {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}
