"""Read named Form 1040 values from one return file.

The return files are XML, in the IRS e-file namespace. See schema/return.xsd for which elements a
return must hold and which may be missing.
"""
from pathlib import Path
import xml.etree.ElementTree as ET

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
    form = ET.parse(path).getroot().find("efile:ReturnData/efile:IRS1040", NS)
    return {
        "wages": _amount(form, "WagesAmt"),
        "taxable_interest": _amount(form, "TaxableInterestAmt"),
        "adjusted_gross_income": _amount(form, "AdjustedGrossIncomeAmt"),
    }


def _amount(form: ET.Element, tag: str) -> int | None:
    """Return the whole-dollar amount in one child element of the form, or None when it is missing."""
    text = form.findtext(f"efile:{tag}", namespaces=NS)
    return None if text is None else int(text)


def dependent_relationships(path: str | Path) -> list[str]:
    """Return the relationship code of each dependent on the return's Form 1040, in file order.

    Args:
        path: the return's XML file.

    Returns:
        One DependentRelationshipCd for each DependentDetail, such as ["DAUGHTER"]; an empty list
        when the return names no dependent.
    """
    form = ET.parse(path).getroot().find("efile:ReturnData/efile:IRS1040", NS)
    return [
        code.text
        for code in form.findall("efile:DependentDetail/efile:DependentRelationshipCd", NS)
    ]
