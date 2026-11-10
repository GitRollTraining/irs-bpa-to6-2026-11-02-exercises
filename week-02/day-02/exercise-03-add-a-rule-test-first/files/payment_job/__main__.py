"""Run the nightly job: python -m payment_job data/accounts.csv report.txt"""
import sys

from payment_job import reader, rules, writer


def main(argv: list[str]) -> int:
    """Read the day's accounts, work out each penalty and write the report.

    Args:
        argv: the path of the accounts file, then the path of the report.

    Returns:
        0 when the report is written.
    """
    accounts = reader.read_accounts(argv[0])
    lines = [(account, rules.penalty_for(account)) for account in accounts]
    writer.write_report(argv[1], lines)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
