"""Wednesday's course data (week 3, day 3): the synthetic return files the trainer's setup writes.

The course made up every return, name and amount: no file belongs to a real taxpayer. Each file is
one return, in the layout of week 2's sample returns (the IRS e-file namespace), with three changes:

- the filer's taxpayer identification number is already replaced by a case key, `CaseKey`, by the
  rule Tuesday's field record applies, so no learner reads a lookup of numbers and keys;
- the dependents' and employees' identification numbers are left out;
- a `CourseLabel` element, which the course added, holds the examination label `ExamChangedTax`
  (yes or no; left out for a return never examined) and `TaxAddedByExam`, the tax an examination
  added, which is written after selection.

The setup notebook, day-03-setup.ipynb beside this file, runs this file and writes each return to
/Volumes/course/returns/raw/. The same returns in table form, by the week's column names, come from
return_rows(). Nothing here is random at run time: the same files every run.
"""
import random

YEARS = [2020, 2021, 2022, 2023]
HISTORY_FILER = "F-30037"   # four returns, 2020 to 2023: named in exercise 3
SINGLE_FILER = "F-30074"    # one return, 2023 only: named in exercise 3
ZERO_AGI = ("F-30111", 2021)  # adjusted gross income 0: exercise 2's null ratio
FIRST = ["ALEX", "SAM", "RILEY", "JORDAN", "TAYLOR", "MORGAN", "CASEY", "JAMIE", "DREW", "AVERY"]
LAST = ["SAMPLE", "EXAMPLE", "TESTER", "PLACEHOLDER", "MADEUP"]
RELATIONSHIPS = ["SON", "DAUGHTER", "PARENT", "NEPHEW", "NIECE"]


def _filers() -> list[str]:
    """The 16 filers' case keys, in a fixed order."""
    return [f"F-{30000 + 37 * i}" for i in range(1, 17)]


def returns() -> list[dict]:
    """Every synthetic return as a dictionary, in file order.

    Returns:
        One dictionary per return: filer_key, tax_year, name, filing_status, wages_amt,
        taxable_interest_amt, total_income, agi_amt, total_tax_amt, dependents (a list of
        relationship codes), w2s (a list of W-2 wage amounts), exam_changed_tax ("yes", "no" or
        None) and tax_added_by_exam (whole dollars, or None).
    """
    rng = random.Random(3)
    out = []
    for n, key in enumerate(_filers()):
        if key == HISTORY_FILER:
            years = YEARS
        elif key == SINGLE_FILER:
            years = [2023]
        else:
            start = rng.choice([2020, 2020, 2021, 2022])
            years = [y for y in YEARS if y >= start]
        base = rng.randrange(30, 120) * 1000
        status = rng.randint(1, 4)
        name = f"{FIRST[n % len(FIRST)]} {LAST[n % len(LAST)]}"
        for k, year in enumerate(years):
            wages = round(base * (1 + rng.uniform(-0.08, 0.10)) ** k, -1)
            if key == HISTORY_FILER:
                wages = {2020: 46000, 2021: 48000, 2022: 50000, 2023: 57500}[year]
            interest = rng.randrange(0, 2000, 10)
            adjust = rng.randrange(0, 3000, 10)
            if (key, year) == ZERO_AGI:
                wages, interest, adjust = 0, 0, 0
            wages = int(wages)
            total = wages + interest
            agi = max(0, total - adjust)
            tax = round(agi * rng.choice([0.08, 0.10, 0.12, 0.14]))
            if wages == 0:
                w2s = []
            elif rng.random() < 0.3:
                first = int(round(wages * rng.uniform(0.3, 0.6), -1))
                w2s = [first, wages - first]
            else:
                w2s = [wages]
            if w2s and rng.random() < 0.2:   # some wages no W-2 confirms
                w2s = [int(round(w * 0.8, -1)) for w in w2s]
            dependents = [rng.choice(RELATIONSHIPS) for _ in range(rng.choice([0, 0, 1, 2, 3]))]
            if (key, year) == ZERO_AGI:
                dependents = []
            roll = rng.random()
            label = None if roll < 0.55 else ("yes" if roll > 0.82 else "no")
            added = None if label is None else (rng.randrange(500, 6000, 10) if label == "yes" else 0)
            out.append({
                "filer_key": key, "tax_year": year, "name": name, "filing_status": status,
                "wages_amt": wages, "taxable_interest_amt": interest, "total_income": total,
                "agi_amt": agi, "total_tax_amt": tax, "dependents": dependents, "w2s": w2s,
                "exam_changed_tax": label, "tax_added_by_exam": added,
            })
    return out


def file_name(record: dict) -> str:
    """The file a return is written to, such as return-F-30037-2023.xml."""
    return f"return-{record['filer_key']}-{record['tax_year']}.xml"


def xml_text(record: dict) -> str:
    """One return as XML text, in the layout of week 2's sample returns."""
    deps = "".join(
        "      <DependentDetail>\n"
        f"        <DependentFirstNm>{FIRST[(i + 3) % len(FIRST)]}</DependentFirstNm>\n"
        f"        <DependentRelationshipCd>{code}</DependentRelationshipCd>\n"
        "      </DependentDetail>\n" for i, code in enumerate(record["dependents"]))
    w2s = "".join(
        f'    <IRSW2 documentId="IRSW2-{i + 1:04d}">\n'
        f"      <EmployerEIN>{900000000 + 11 * (i + 1) + record['tax_year']}</EmployerEIN>\n"
        f"      <WagesAmt>{amount}</WagesAmt>\n"
        "    </IRSW2>\n" for i, amount in enumerate(record["w2s"]))
    label = ""
    if record["exam_changed_tax"] is not None:
        label = ("  <!-- Added by the course: the examination label, and the tax an examination added. -->\n"
                 "  <CourseLabel>\n"
                 f"    <ExamChangedTax>{record['exam_changed_tax']}</ExamChangedTax>\n"
                 f"    <TaxAddedByExam>{record['tax_added_by_exam']}</TaxAddedByExam>\n"
                 "  </CourseLabel>\n")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<!-- Made up for the course: no real taxpayer and no real return. The case key is written in\n"
        "     place of the taxpayer identification number. -->\n"
        f'<Return xmlns="http://www.irs.gov/efile" returnVersion="{record["tax_year"]}v5.0">\n'
        "  <ReturnHeader>\n"
        f"    <TaxYr>{record['tax_year']}</TaxYr>\n"
        "    <ReturnTypeCd>1040</ReturnTypeCd>\n"
        "    <Filer>\n"
        f"      <CaseKey>{record['filer_key']}</CaseKey>\n"
        f"      <NameLine1Txt>{record['name']}</NameLine1Txt>\n"
        "      <USAddress>\n"
        "        <AddressLine1Txt>100 EXAMPLE ST</AddressLine1Txt>\n"
        "        <CityNm>ANYTOWN</CityNm>\n"
        "        <StateAbbreviationCd>MD</StateAbbreviationCd>\n"
        "      </USAddress>\n"
        "    </Filer>\n"
        "  </ReturnHeader>\n"
        f'  <ReturnData documentCnt="{1 + len(record["w2s"])}">\n'
        '    <IRS1040 documentId="IRS1040-0001">\n'
        f"      <IndividualReturnFilingStatusCd>{record['filing_status']}</IndividualReturnFilingStatusCd>\n"
        f"{deps}"
        f"      <WagesAmt>{record['wages_amt']}</WagesAmt>\n"
        f"      <TaxableInterestAmt>{record['taxable_interest_amt']}</TaxableInterestAmt>\n"
        f"      <TotalIncomeAmt>{record['total_income']}</TotalIncomeAmt>\n"
        f"      <AdjustedGrossIncomeAmt>{record['agi_amt']}</AdjustedGrossIncomeAmt>\n"
        f"      <TotalTaxAmt>{record['total_tax_amt']}</TotalTaxAmt>\n"
        "    </IRS1040>\n"
        f"{w2s}"
        "  </ReturnData>\n"
        f"{label}"
        "</Return>\n")


def return_rows() -> list[dict]:
    """The same returns in table form, by the week's column names (week-tables.md)."""
    return [{
        "return_id": f"{r['filer_key']}-{r['tax_year']}", "filer_key": r["filer_key"],
        "tax_year": r["tax_year"], "filing_status": r["filing_status"], "wages_amt": r["wages_amt"],
        "total_income": r["total_income"], "agi_amt": r["agi_amt"], "total_tax_amt": r["total_tax_amt"],
        "exam_changed_tax": r["exam_changed_tax"], "tax_added_by_exam": r["tax_added_by_exam"],
    } for r in returns()]


def setup_facts() -> dict:
    """What the setup notebook's read-back cell should print."""
    rs = returns()
    return {
        "files": len(rs),
        "years": sorted({r["tax_year"] for r in rs}),
        "dependents": sum(len(r["dependents"]) for r in rs),
        "w2s": sum(len(r["w2s"]) for r in rs),
        "tax_change_cases": sum(r["exam_changed_tax"] == "yes" for r in rs),
        "history_filer_returns": sum(r["filer_key"] == HISTORY_FILER for r in rs),
        "single_filer_returns": sum(r["filer_key"] == SINGLE_FILER for r in rs),
    }


def volume_statements(class_group: str) -> list[str]:
    """The volume that holds the files, and the class's right to read it."""
    return [
        "CREATE VOLUME IF NOT EXISTS course.returns.raw COMMENT 'Synthetic return XML files for week 3, Wednesday. Made up by the course.'",
        f"GRANT READ VOLUME ON VOLUME course.returns.raw TO `{class_group}`",
    ]


def learner_statements(number: str, principal: str) -> list[str]:
    """One learner's schema, course.learner_NN, and the rights to make tables in it."""
    schema = f"course.learner_{number}"
    return [
        f"CREATE SCHEMA IF NOT EXISTS {schema} COMMENT 'Week 3 tables of one learner.'",
        f"GRANT USE SCHEMA, CREATE TABLE ON SCHEMA {schema} TO `{principal}`",
    ]
