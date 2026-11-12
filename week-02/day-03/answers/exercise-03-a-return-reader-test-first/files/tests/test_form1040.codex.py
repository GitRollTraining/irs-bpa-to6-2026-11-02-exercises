from pathlib import Path

from form1040 import read_form_1040

SAMPLE = Path(__file__).parent.parent / "returns" / "sample-return.xml"


def write_sample_without(tmp_path, element_line, count=1):
    """Write a copy of the sample return with the first `count` copies of `element_line` removed."""
    text = SAMPLE.read_text(encoding="utf-8")
    assert element_line in text, "the fixture edit must change the copy"
    copy = tmp_path / "return.xml"
    copy.write_text(text.replace(element_line, "", count), encoding="utf-8")
    return copy


def test_reads_the_three_values_of_the_sample_return():
    assert read_form_1040(SAMPLE) == {
        "wages": 52340,
        "taxable_interest": 120,
        "adjusted_gross_income": 52460,
    }


def test_missing_taxable_interest_is_none_and_the_others_are_unchanged(tmp_path):
    copy = write_sample_without(tmp_path, "<TaxableInterestAmt>120</TaxableInterestAmt>")

    assert read_form_1040(copy) == {
        "wages": 52340,
        "taxable_interest": None,
        "adjusted_gross_income": 52460,
    }


def test_wages_missing_from_the_1040_are_not_taken_from_the_w2(tmp_path):
    # The first WagesAmt in the sample is the IRS1040's; the second is the IRSW2's.
    copy = write_sample_without(tmp_path, "<WagesAmt>52340</WagesAmt>")

    assert read_form_1040(copy)["wages"] is None
