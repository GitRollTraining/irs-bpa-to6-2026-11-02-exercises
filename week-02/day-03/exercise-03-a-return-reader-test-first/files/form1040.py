"""Read named Form 1040 values from one return file.

The return files are XML, in the IRS e-file namespace. See schema/return.xsd for which elements a
return must hold and which may be missing.
"""
from pathlib import Path

NS = {"efile": "http://www.irs.gov/efile"}


def read_form_1040(path: str | Path) -> dict[str, int | None]:
    """Return three Form 1040 values of one return file, as whole dollars.

    Args:
        path: the return's XML file.

    Returns:
        A dictionary with the keys "wages" (WagesAmt), "taxable_interest" (TaxableInterestAmt) and
        "adjusted_gross_income" (AdjustedGrossIncomeAmt), each read from the return's IRS1040.
        A value the return leaves out is None.
    """
    raise NotImplementedError("read_form_1040 is not written yet")
