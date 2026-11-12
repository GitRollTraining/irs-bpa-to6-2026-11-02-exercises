"""Read named Form 1040 values from one return file.

The return files are XML, in the IRS e-file namespace. See schema/return.xsd for which elements a
return must hold and which may be missing.
"""
import xml.etree.ElementTree as ET
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
    irs1040 = ET.parse(path).getroot().find("efile:ReturnData/efile:IRS1040", NS)
    return {
        "wages": _amount(irs1040, "WagesAmt"),
        "taxable_interest": _amount(irs1040, "TaxableInterestAmt"),
        "adjusted_gross_income": _amount(irs1040, "AdjustedGrossIncomeAmt"),
    }


def _amount(irs1040: ET.Element, tag: str) -> int | None:
    element = irs1040.find(f"efile:{tag}", NS)
    return None if element is None else int(element.text)
