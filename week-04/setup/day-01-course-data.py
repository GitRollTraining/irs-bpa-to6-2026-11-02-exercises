"""Week 4's course data: the made-up returns a baseline model learns from, and the SQL that writes them.

The setup notebook beside this file, day-01-setup.ipynb, runs it once before Monday. The week's
exercises can also read it on a computer with no Databricks, to know what each table holds. The
course made up every return, name and amount: no row belongs to a real taxpayer.

Tables, in the catalog `course`, schema `returns` (the schema week 3's setup made):
  model_returns   one row per return as filed: the header (case key, made-up name) and the Form
                  1040 body amounts, with the examination label (1,000 rows)
  model_features  one row per return: the amounts, the features built from them, and the columns
                  that are not features (keys, the made-up channel, the label) (1,000 rows)
  model_train     model_features for tax years 2020 and 2021 (500 rows)
  model_valid     model_features for tax year 2022 (250 rows); case 123 is here
  model_test      model_features for tax year 2023 (250 rows)

Six things are planted, each named in day-01-setup.md: case 123, a return the models score high; a
made-up group column, made_up_channel; a feature that tracks it, other_income_amt; missing amounts
in deduction_amt; name_length, built from a header field; and tax_added_by_exam, written after
selection. Nothing here is random at run time: random.Random(SEED) gives the same rows every run.
"""
import math
import random

CATALOG = "course"
SCHEMA = "returns"
SEED = 2
YEARS = [2020, 2021, 2022, 2023]
SETS = {"model_train": [2020, 2021], "model_valid": [2022], "model_test": [2023]}
FILERS = 250           # each filer files one return a year, 2020 to 2023: 1,000 returns
EXAMINED_PER_YEAR = 200  # of each year's 250 returns, 200 were examined and carry a label
YES_PER_YEAR = 40        # of each year's 200 examined returns, 40 had their tax changed
CASE_123_FILER = "F-40409"  # its 2022 return is case 123, in model_valid
NOISE = 0.5  # how far chance moves a return's risk before the 40 riskiest are labelled yes
MADE_UP = "Made up by the course for week 4; no row is a real taxpayer."
FIRST = ["ALEX", "SAM", "RILEY", "JORDAN", "TAYLOR", "MORGAN", "CASEY", "JAMIE", "DREW", "AVERY",
         "KIM", "ROBIN", "LEE", "SKYLER", "QUINN", "BLAIR", "FRANCES", "EMERSON"]
LAST = ["SAMPLE", "EXAMPLE", "TESTER", "PLACEHOLDER", "MADEUP", "DUMMY", "FICTIONAL", "STANDIN"]
STANDARD_DEDUCTION = {1: 12950, 2: 25900, 3: 12950, 4: 19400}  # by filing status, one set for every year

# The features the measurement in day-01-setup.md trains on, in this order: every amount of the
# filed return, the two ratios, and deduction_missing, the flag Monday's exercise 3 adds (1 when
# deduction_amt is empty). The other columns of model_features are keys, the group, the label, a
# feature built from a header field (name_length) and one written after selection (tax_added_by_exam).
FEATURES = ["filing_status", "wages_amt", "taxable_interest_amt", "other_income_amt", "total_income",
            "agi_amt", "deduction_amt", "deduction_missing", "total_tax_amt", "withholding_amt",
            "tax_to_agi", "deduction_to_agi"]

# Each table's columns: (name, SQL type, comment).
RETURN_COLUMNS = [
    ("case_id", "INT", "The case number: case 123 is the row where case_id = 123."),
    ("return_id", "STRING", "The return: the filer's case key and the tax year, such as F-40409-2022."),
    ("filer_key", "STRING", "The filer's case key. The course wrote it in place of the taxpayer identification number."),
    ("tax_year", "INT", "The tax year the return covers."),
    ("filer_name", "STRING", "Header: the filer's name, made up by the course."),
    ("city_nm", "STRING", "Header: the filer's city, made up by the course."),
    ("made_up_channel", "STRING", "A made-up filing channel, A or B, invented by the course for the bias check. It describes no real person or group."),
    ("filing_status", "INT", "Filing status code: 1 single, 2 married filing jointly, 3 married filing separately, 4 head of household."),
    ("wages_amt", "INT", "Wages, salaries and tips, in whole dollars."),
    ("taxable_interest_amt", "INT", "Taxable interest, in whole dollars."),
    ("other_income_amt", "INT", "Additional income from Schedule 1, such as business income, in whole dollars."),
    ("total_income", "INT", "Wages plus taxable interest plus other income, in whole dollars."),
    ("agi_amt", "INT", "Adjusted gross income, in whole dollars."),
    ("deduction_amt", "INT", "The standard or itemized deduction, in whole dollars. Empty where the line was left blank."),
    ("total_tax_amt", "INT", "Total tax, in whole dollars."),
    ("withholding_amt", "INT", "Federal income tax withheld, in whole dollars."),
    ("exam_changed_tax", "STRING", "For a return examined in the past: yes when the examination changed the tax, no when it did not. Empty for a return never examined."),
    ("tax_added_by_exam", "INT", "The tax an examination added, in whole dollars: 0 when it changed nothing. Empty for a return never examined."),
]
FEATURE_COLUMNS = [c for c in RETURN_COLUMNS if c[0] not in ("filer_name", "city_nm")] + [
    ("tax_to_agi", "DOUBLE", "Total tax divided by adjusted gross income, to 4 places."),
    ("deduction_to_agi", "DOUBLE", "Deduction divided by adjusted gross income, to 4 places. Empty where deduction_amt is empty."),
    ("name_length", "INT", "The number of characters in the filer's name."),
]
TABLE_COMMENTS = {
    "model_returns": "Week 4: one row per return as filed, 2020 to 2023. " + MADE_UP,
    "model_features": "Week 4: one row per return, the amounts and the features built from them. " + MADE_UP,
    "model_train": "Week 4: the training set, tax years 2020 and 2021. " + MADE_UP,
    "model_valid": "Week 4: the validation set, tax year 2022; case 123 is here. " + MADE_UP,
    "model_test": "Week 4: the test set, tax year 2023. " + MADE_UP,
}


def _risk(r: dict) -> float:
    """What makes an examination change the tax, in this made-up world: a large deduction for the
    income, and a large share of income from outside wages."""
    return 7.0 * (r["_deduction"] / max(r["agi_amt"], 1) - 0.30) + 5.0 * (r["other_income_amt"] / max(r["total_income"], 1))


def returns(seed: int = SEED) -> list[dict]:
    """Every made-up return as a dictionary, ordered by case_id.

    Args:
        seed: the generator's seed. The course's tables use SEED; another seed is only for the
            stability measurement in day-01-setup.md.

    Returns:
        One dictionary per return, with every column of model_returns.
    """
    rng = random.Random(seed)
    rows = []
    for n in range(FILERS):
        key = f"F-{40000 + 7 * n + 3}"
        channel = "B" if rng.random() < 0.4 else "A"
        status = rng.choices([1, 2, 3, 4], weights=[45, 35, 5, 15])[0]
        base = rng.lognormvariate(math.log(52000), 0.45)
        name = f"{FIRST[rng.randrange(len(FIRST))]} {LAST[rng.randrange(len(LAST))]}"
        for k, year in enumerate(YEARS):
            wages = int(round(base * 1.03 ** k * rng.uniform(0.95, 1.05), -1))
            interest = rng.randrange(0, 1500, 10)
            if channel == "B":
                other = int(round(rng.lognormvariate(math.log(16000), 0.6), -1))
            else:
                other = 0 if rng.random() < 0.6 else rng.randrange(200, 4000, 10)
            total = wages + interest + other
            agi = total - rng.randrange(0, 3000, 10)
            itemized = int(round(agi * rng.uniform(0.12, 0.50), -1)) if rng.random() < 0.35 else 0
            deduction = max(STANDARD_DEDUCTION[status], itemized)
            withholding = int(round(wages * rng.uniform(0.06, 0.16), -1))
            if (key, year) == (CASE_123_FILER, 2022):  # case 123: two pushes an examiner can read
                wages, interest, other = 54400, 120, 28500
                total = wages + interest + other
                agi, deduction, withholding = total - 1200, 42000, 6500
            tax = round(max(0, agi - deduction) * 0.13)
            rows.append({
                "return_id": f"{key}-{year}", "filer_key": key, "tax_year": year, "filer_name": name,
                "city_nm": "ANYTOWN", "made_up_channel": channel, "filing_status": status,
                "wages_amt": wages, "taxable_interest_amt": interest, "other_income_amt": other,
                "total_income": total, "agi_amt": agi, "_deduction": deduction,
                "deduction_amt": None if rng.random() < 0.05 else deduction,
                "total_tax_amt": tax, "withholding_amt": withholding, "_noise": rng.gauss(0, NOISE),
            })
    case_123 = next(r for r in rows if r["return_id"] == f"{CASE_123_FILER}-2022")
    case_123["deduction_amt"] = case_123["_deduction"]
    for year in YEARS:  # the label: 200 examined a year, the 40 riskiest of them changed
        year_rows = [r for r in rows if r["tax_year"] == year]
        others = [r for r in year_rows if r is not case_123]
        examined = rng.sample(others, EXAMINED_PER_YEAR - (case_123 in year_rows))
        examined += [case_123] if case_123 in year_rows else []
        # case 123 is planted: its examination changed the tax, so it ranks first
        ranked = sorted(examined, key=lambda r: math.inf if r is case_123 else _risk(r) + r["_noise"], reverse=True)
        for i, r in enumerate(ranked):
            r["exam_changed_tax"] = "yes" if i < YES_PER_YEAR else "no"
            r["tax_added_by_exam"] = rng.randrange(500, 8000, 10) if i < YES_PER_YEAR else 0
        for r in year_rows:
            r.setdefault("exam_changed_tax", None)
            r.setdefault("tax_added_by_exam", None)
    ids = list(range(1, len(rows) + 1))
    rng.shuffle(ids)
    for r, case_id in zip(rows, ids):
        r["case_id"] = case_id
    holder = next(r for r in rows if r["case_id"] == 123)  # give case_id 123 to case 123
    holder["case_id"], case_123["case_id"] = case_123["case_id"], 123
    for r in rows:
        del r["_deduction"], r["_noise"]
    return sorted(rows, key=lambda r: r["case_id"])


def feature_rows(seed: int = SEED) -> list[dict]:
    """The rows of model_features: each return's amounts, and the features built from them."""
    out = []
    for r in returns(seed):
        row = {name: r[name] for name, _, _ in FEATURE_COLUMNS if name in r}
        agi = r["agi_amt"]
        row["tax_to_agi"] = round(r["total_tax_amt"] / agi, 4) if agi else None
        row["deduction_to_agi"] = round(r["deduction_amt"] / agi, 4) if agi and r["deduction_amt"] is not None else None
        row["name_length"] = len(r["filer_name"])
        out.append(row)
    return out


def set_rows(name: str, seed: int = SEED) -> list[dict]:
    """The rows of one set, model_train, model_valid or model_test, by tax year."""
    return [r for r in feature_rows(seed) if r["tax_year"] in SETS[name]]


def sql_value(value: object) -> str:
    """Write one Python value as a SQL literal: 'text', 123, 0.25 or NULL."""
    if value is None:
        return "NULL"
    if isinstance(value, (int, float)):
        return repr(value)
    return "'" + str(value).replace("\\", "\\\\").replace("'", "\\'") + "'"


def table_statements() -> list[str]:
    """The SQL that makes the five tables, with their comments and rows, in the order it runs."""
    s = f"{CATALOG}.{SCHEMA}"
    tables = [("model_returns", RETURN_COLUMNS, returns())]
    tables += [("model_features", FEATURE_COLUMNS, feature_rows())]
    tables += [(name, FEATURE_COLUMNS, set_rows(name)) for name in SETS]
    sql = []
    for table, columns, rows in tables:
        names = [n for n, _, _ in columns]
        body = ",\n".join(f"  {n} {k} COMMENT {sql_value(c)}" for n, k, c in columns)
        values = ",\n".join("(" + ", ".join(sql_value(r[n]) for n in names) + ")" for r in rows)
        sql.append(f"CREATE OR REPLACE TABLE {s}.{table} (\n{body}\n) COMMENT {sql_value(TABLE_COMMENTS[table])}")
        sql.append(f"INSERT INTO {s}.{table} ({', '.join(names)}) VALUES\n{values}")
    for table in ["model_returns", "model_features", *SETS]:
        sql.append(f"ALTER TABLE {s}.{table} ALTER COLUMN exam_changed_tax SET TAGS ('role' = 'label')")
    return sql


def setup_facts() -> dict:
    """What the setup notebook's read-back cell should print."""
    facts = {}
    for name in ["model_features", *SETS]:
        rows = feature_rows() if name == "model_features" else set_rows(name)
        facts[name] = {
            "rows": len(rows),
            "yes": sum(r["exam_changed_tax"] == "yes" for r in rows),
            "no": sum(r["exam_changed_tax"] == "no" for r in rows),
            "empty": sum(r["exam_changed_tax"] is None for r in rows),
        }
    feats = feature_rows()
    facts["deduction_amt empty"] = sum(r["deduction_amt"] is None for r in feats)
    facts["case 123"] = next(r for r in feats if r["case_id"] == 123)["return_id"]
    facts["channels"] = {g: sum(r["made_up_channel"] == g for r in feats) for g in ("A", "B")}
    return facts


# Wednesday's ten held-out returns, by case_id: examined returns of model_valid, case 123 among them.
# Scored by the logistic regression of day-01-setup.md at 0.5 they fall 3 true positives (123, 205,
# 224), 2 false positives (463, 905), 2 false negatives (50, 471) and 3 true negatives (4, 11, 37).
WEDNESDAY_TEN = [4, 11, 37, 50, 123, 205, 224, 463, 471, 905]

if __name__ == "__main__":
    for name, value in setup_facts().items():
        print(name, value)
