"""The made-up tables of week 3, day 1, and the SQL that builds them in Databricks.

The setup notebook beside this file runs it once per workspace. The exercises' checks also read it
on a computer with no Databricks, to know what each table holds. The course made up every row:
no name, number or amount belongs to a real taxpayer.

Tables, all in the schema case_selection of the course catalog:
  returns              one row per made-up return of tax year 2025 (40 rows)
  third_party_reports  one row per return: the wages and interest that payers reported (40 rows)
  exam_outcomes        one row per past examination, with how its return was selected (24 rows)
  income_bands         one row per return: an income band that Python computed in the setup notebook
  case_features        built by SQL from the tables above, so Unity Catalog records its lineage
"""

SCHEMA = "case_selection"
RETURNS = 40
EXAMS = 24
MADE_UP = "Made up by the course for week 3; no row is a real taxpayer."

# Each table's columns: (name, SQL type, comment or None for no comment).
COLUMNS = {
    "returns": [
        ("return_id", "STRING", "The return's identifier in the course data."),
        ("tax_year", "INT", "The tax year the return covers."),
        ("taxpayer_name", "STRING", "The taxpayer's name as filed. Identifies a person."),
        ("taxpayer_tin", "STRING", "The taxpayer identification number, in the form of an SSN. Identifies a person."),
        ("filing_status", "STRING", "The filing status on the return."),
        ("wages", "INT", "Wages, salaries and tips the taxpayer reported, in whole dollars."),
        ("taxable_interest", "INT", "Taxable interest the taxpayer reported, in whole dollars. Empty when the line was left blank."),
        ("business_income", "INT", "Business income or loss the taxpayer reported, in whole dollars. A loss is negative."),
        ("total_income", "INT", None),
    ],
    "third_party_reports": [
        ("return_id", "STRING", "The return the reports were matched to."),
        ("wages_reported", "INT", "Total wages that employers reported for the taxpayer on Forms W-2, in whole dollars."),
        ("interest_reported", "INT", None),
        ("payer_count", "INT", None),
    ],
    "exam_outcomes": [
        ("exam_id", "STRING", "The examination's identifier in the course data."),
        ("tax_year", "INT", "The tax year of the examined return."),
        ("selection_method", "STRING", "How the return was selected for examination: random sample or score."),
        ("tax_changed", "BOOLEAN", "True when the examination changed the tax."),
        ("change_amount", "INT", "The change to the tax in whole dollars; 0 when the tax did not change."),
    ],
    "income_bands": [
        ("return_id", "STRING", "The return the band belongs to."),
        ("income_band", "STRING", "A band of total income, computed in Python in the setup notebook."),
    ],
    "case_features": [
        ("return_id", "STRING", "The return the features describe."),
        ("income_gap", "INT", "Wages on the return minus wages employers reported, in whole dollars."),
        ("interest_gap", "INT", "Taxable interest on the return minus interest payers reported, in whole dollars."),
        ("income_band", "STRING", "A band of total income, from income_bands."),
    ],
}

TABLE_COMMENTS = {
    "returns": "One row per made-up return of tax year 2025. " + MADE_UP,
    "third_party_reports": "One row per return: what employers and banks reported to the IRS for the taxpayer. " + MADE_UP,
    "exam_outcomes": "One row per past examination, and how its return was selected. " + MADE_UP,
    "income_bands": "One band of total income per return, written by the setup notebook from Python. " + MADE_UP,
    "case_features": "Features for the case-selection model, built by SQL from the course tables. " + MADE_UP,
}

# Column tags: (table, column, key, value). The tag marks a field that identifies a person.
TAGS = [
    ("returns", "taxpayer_name", "data_class", "pii"),
    ("returns", "taxpayer_tin", "data_class", "pii"),
]

FILING = ["single", "married filing jointly", "head of household", "married filing separately"]


def return_rows() -> list[dict]:
    """Make the rows of returns and third_party_reports. The same rows every time: no random numbers.

    Returns:
        One dict per return, with every column of returns and the three of third_party_reports.
    """
    rows = []
    for i in range(1, RETURNS + 1):
        wages = 28000 + 1750 * i
        interest = None if i % 8 == 0 else (i * 37) % 900
        if i % 5 == 0:
            business = -(40000 + 1500 * i)
        elif i % 3 == 0:
            business = (i * 413) % 5000
        else:
            business = 0
        rows.append({
            "return_id": f"R-2025-{i:04d}",
            "tax_year": 2025,
            "taxpayer_name": f"Made-up Taxpayer {i:02d}",
            "taxpayer_tin": f"000-00-{i:04d}",
            "filing_status": FILING[i % 4],
            "wages": wages,
            "taxable_interest": interest,
            "business_income": business,
            "total_income": wages + (interest or 0) + business,
            "wages_reported": wages + (4000 if i % 6 == 0 else 2500 if i % 7 == 0 else 0),
            "interest_reported": (i * 37) % 900,
            "payer_count": 1 + i % 3,
        })
    return rows


def exam_rows() -> list[dict]:
    """Make the rows of exam_outcomes: past examinations, a quarter of them from a random sample.

    Returns:
        One dict per examination.
    """
    rows = []
    for i in range(1, EXAMS + 1):
        changed = i % 3 != 0
        rows.append({
            "exam_id": f"E-{i:04d}",
            "tax_year": 2021 + i % 3,
            "selection_method": "random sample" if i % 4 == 0 else "score",
            "tax_changed": changed,
            "change_amount": 300 + 175 * i if changed else 0,
        })
    return rows


def income_band(total_income: int) -> str:
    """Put a total income in its band. The setup notebook runs this in Python, outside any SQL query.

    Args:
        total_income: the return's total income in whole dollars; negative for a loss.

    Returns:
        "loss", "under 50,000", "50,000 to 99,999" or "100,000 and over".
    """
    if total_income < 0:
        return "loss"
    if total_income < 50000:
        return "under 50,000"
    if total_income < 100000:
        return "50,000 to 99,999"
    return "100,000 and over"


def sql_value(value: object) -> str:
    """Write one Python value as a SQL literal.

    Args:
        value: a string, an int, a bool or None.

    Returns:
        The literal: 'text', 123, true or NULL. A quote inside text is escaped with a backslash, as
        Databricks SQL reads it: two quotes in a row would join two literals into one.
    """
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return "'" + str(value).replace("\\", "\\\\").replace("'", "\\'") + "'"


def create_table(catalog: str, table: str, rows: list[dict]) -> list[str]:
    """Write the SQL that makes one table with its comments, then fills it.

    Args:
        catalog: the course catalog's name.
        table: a key of COLUMNS.
        rows: the rows to insert, each a dict with every column of the table.

    Returns:
        A CREATE OR REPLACE TABLE statement and an INSERT statement.
    """
    full = f"{catalog}.{SCHEMA}.{table}"
    columns = []
    for name, kind, comment in COLUMNS[table]:
        columns.append(f"  {name} {kind}" + (f" COMMENT {sql_value(comment)}" if comment else ""))
    create = (f"CREATE OR REPLACE TABLE {full} (\n" + ",\n".join(columns) + "\n)"
              f" COMMENT {sql_value(TABLE_COMMENTS[table])}")
    names = [name for name, _, _ in COLUMNS[table]]
    values = ",\n".join("(" + ", ".join(sql_value(row[n]) for n in names) + ")" for row in rows)
    return [create, f"INSERT INTO {full} ({', '.join(names)}) VALUES\n{values}"]


def base_statements(catalog: str) -> list[str]:
    """Write the SQL for the schema, the three base tables, their rows and their tags.

    Args:
        catalog: the course catalog's name.

    Returns:
        The statements, in the order they run.
    """
    sql = [f"CREATE SCHEMA IF NOT EXISTS {catalog}.{SCHEMA} COMMENT {sql_value('Tables for the case-selection exercises of week 3. ' + MADE_UP)}"]
    sql += create_table(catalog, "returns", return_rows())
    sql += create_table(catalog, "third_party_reports", return_rows())
    sql += create_table(catalog, "exam_outcomes", exam_rows())
    for table, column, key, value in TAGS:
        sql.append(f"ALTER TABLE {catalog}.{SCHEMA}.{table} ALTER COLUMN {column} SET TAGS ({sql_value(key)} = {sql_value(value)})")
    return sql


def features_statements(catalog: str) -> list[str]:
    """Write the SQL that builds case_features from the other tables, and its column comments.

    The query runs on Databricks, so Unity Catalog records which column came from which.

    Args:
        catalog: the course catalog's name.

    Returns:
        The CREATE statement, then one statement per column comment.
    """
    s = f"{catalog}.{SCHEMA}"
    sql = [f"""CREATE OR REPLACE TABLE {s}.case_features
COMMENT {sql_value(TABLE_COMMENTS['case_features'])}
AS SELECT
  r.return_id,
  r.wages - t.wages_reported AS income_gap,
  r.taxable_interest - t.interest_reported AS interest_gap,
  b.income_band
FROM {s}.returns AS r
JOIN {s}.third_party_reports AS t ON t.return_id = r.return_id
JOIN {s}.income_bands AS b ON b.return_id = r.return_id"""]
    for name, _, comment in COLUMNS["case_features"]:
        sql.append(f"ALTER TABLE {s}.case_features ALTER COLUMN {name} COMMENT {sql_value(comment)}")
    return sql


def column_facts() -> dict[str, dict]:
    """What a column summary shows for each column, worked out from the rows above.

    Returns:
        For each "table.column": its type, comment, tags, empty count, smallest and largest value.
    """
    rows = {"returns": return_rows(), "third_party_reports": return_rows(), "exam_outcomes": exam_rows()}
    rows["income_bands"] = [{"return_id": r["return_id"], "income_band": income_band(r["total_income"])}
                            for r in rows["returns"]]
    rows["case_features"] = [{
        "return_id": r["return_id"],
        "income_gap": r["wages"] - r["wages_reported"],
        "interest_gap": None if r["taxable_interest"] is None else r["taxable_interest"] - r["interest_reported"],
        "income_band": income_band(r["total_income"]),
    } for r in rows["returns"]]
    tags = {f"{t}.{c}": f"{k}={v}" for t, c, k, v in TAGS}
    facts = {}
    for table, columns in COLUMNS.items():
        for name, kind, comment in columns:
            values = [row[name] for row in rows[table]]
            present = [v for v in values if v is not None]
            facts[f"{table}.{name}"] = {
                "type": kind, "comment": comment, "tags": tags.get(f"{table}.{name}"),
                "rows": len(values), "empty": len(values) - len(present),
                "min": min(present) if present else None, "max": max(present) if present else None,
            }
    return facts
