import xml.etree.ElementTree as ET
from pathlib import Path

from form1040 import dependent_relationships, read_form_1040

SAMPLE = Path("returns/sample-return.xml")
EFILE = "{http://www.irs.gov/efile}"


def test_reads_the_three_values_of_the_sample_return() -> None:
    assert read_form_1040(SAMPLE) == {
        "wages": 52340,
        "taxable_interest": 120,
        "adjusted_gross_income": 52460,
    }


def test_a_missing_taxable_interest_gives_none(tmp_path: Path) -> None:
    tree = ET.parse(SAMPLE)
    form = tree.getroot().find(f"{EFILE}ReturnData/{EFILE}IRS1040")
    form.remove(form.find(f"{EFILE}TaxableInterestAmt"))
    no_interest = tmp_path / "no-interest.xml"
    tree.write(no_interest, xml_declaration=True, encoding="UTF-8")

    values = read_form_1040(no_interest)

    assert values["taxable_interest"] is None
    assert values["wages"] == 52340
    assert values["adjusted_gross_income"] == 52460


def test_a_repeated_dependent_detail_comes_back_as_a_list() -> None:
    assert dependent_relationships(Path("returns/two-dependents.xml")) == ["DAUGHTER", "SON"]
