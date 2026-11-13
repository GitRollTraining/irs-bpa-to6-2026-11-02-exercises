"""Monday's made-up tables (week 3, day 1), and the SQL that builds them in Databricks.

The setup notebook beside this file, day-01-setup.ipynb, runs it once before Monday. The exercises'
checks also read it on a computer with no Databricks, to know what each table holds. The course
made up every row: no number or amount belongs to a real taxpayer.

Tables, in the catalog `course`, schema `returns`:
  return_header   Monday's return table: one row per made-up return of tax year 2025 (40 rows)
  return_summary  built from return_header by one SQL query on Databricks, so it has lineage;
                  its column income_band comes from a Python function the query calls
"""

CATALOG = "course"
SCHEMA = "returns"
RETURNS = 40
MADE_UP = "Made up by the course for week 3; no row is a real taxpayer."

# Each table's columns: (name, SQL type, comment or None for no comment).
COLUMNS = {
    "return_header": [
        ("return_id", "STRING", "The return's identifier in the course data."),
        ("filer_key", "STRING", "The filer's case key. The course wrote it in place of the taxpayer identification number."),
        ("tax_year", "INT", "The tax year the return covers."),
        ("agi_amt", "INT", "Adjusted gross income on the return, in whole dollars. Below 0 when losses are larger than income."),
        ("wages_amt", "INT", "Wages, salaries and tips the filer reported, in whole dollars."),
        ("total_tax_amt", "INT", None),
        ("total_income", "INT", None),
        ("exam_changed_tax", "STRING", "For a return examined in the past: yes when the examination changed the tax, no when it did not. Empty for a return never examined."),
    ],
    "return_summary": [
        ("return_id", "STRING", "The return the summary describes."),
        ("non_wage_income", "INT", "Total income minus wages, in whole dollars."),
        ("adjustments_amt", "INT", "Total income minus adjusted gross income, in whole dollars."),
        ("income_band", "STRING", "A band of total income, from a Python function the query called."),
    ],
}

TABLE_COMMENTS = {
    "return_header": "Monday's return table: one row per made-up return of tax year 2025. " + MADE_UP,
    "return_summary": "Built from return_header by one SQL query on Databricks. " + MADE_UP,
}

# Column tags: (table, column, key, value).
TAGS = [
    ("return_header", "filer_key", "data_class", "case_key"),
    ("return_header", "exam_changed_tax", "role", "label"),
]


def header_rows() -> list[dict]:
    """Make the rows of return_header. The same rows every time: no random numbers.

    Returns:
        One dict per return, with every column of return_header.
    """
    rows = []
    for i in range(1, RETURNS + 1):
        wages = 28000 + 1750 * i
        interest = (i * 37) % 900
        if i % 5 == 0:
            business = -(40000 + 1500 * i)
        elif i % 3 == 0:
            business = (i * 413) % 5000
        else:
            business = 0
        total = wages + interest + business
        agi = total - (2500 if i % 4 == 0 else 0)
        rows.append({
            "return_id": f"R-2025-{i:04d}",
            "filer_key": f"F-{10000 + 7 * i}",
            "tax_year": 2025,
            "agi_amt": agi,
            "wages_amt": wages,
            "total_tax_amt": max(0, agi * 12 // 100),
            "total_income": total,
            "exam_changed_tax": ("yes" if i % 6 == 0 else "no") if i % 3 == 0 else None,
        })
    return rows


def income_band(total_income: int) -> str:
    """Put a total income in its band. The setup notebook registers it as a Python function that
    the SQL query building return_summary calls.

    Args:
        total_income: the return's total income in whole dollars; negative for a loss.

    Returns:
        "loss", "under 50,000", "50,000 to 99,999" or "100,000 and over".
    """
    if total_income is None:
        return None
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
        value: a string, an int or None.

    Returns:
        The literal: 'text', 123 or NULL. A quote inside text is escaped with a backslash, as
        Databricks SQL reads it: two quotes in a row would join two literals into one.
    """
    if value is None:
        return "NULL"
    if isinstance(value, int):
        return str(value)
    return "'" + str(value).replace("\\", "\\\\").replace("'", "\\'") + "'"


def header_statements() -> list[str]:
    """Write the SQL for the schema, return_header with its comments and rows, and its tags.

    Returns:
        The statements, in the order they run.
    """
    full = f"{CATALOG}.{SCHEMA}.return_header"
    columns = ",\n".join(f"  {n} {k}" + (f" COMMENT {sql_value(c)}" if c else "") for n, k, c in COLUMNS["return_header"])
    names = [n for n, _, _ in COLUMNS["return_header"]]
    values = ",\n".join("(" + ", ".join(sql_value(r[n]) for n in names) + ")" for r in header_rows())
    sql = [
        f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA} COMMENT {sql_value('Week 3 tables. ' + MADE_UP)}",
        f"CREATE OR REPLACE TABLE {full} (\n{columns}\n) COMMENT {sql_value(TABLE_COMMENTS['return_header'])}",
        f"INSERT INTO {full} ({', '.join(names)}) VALUES\n{values}",
    ]
    for table, column, key, value in TAGS:
        sql.append(f"ALTER TABLE {CATALOG}.{SCHEMA}.{table} ALTER COLUMN {column} SET TAGS ({sql_value(key)} = {sql_value(value)})")
    return sql


def summary_statements() -> list[str]:
    """Write the SQL that builds return_summary from return_header, and its column comments.

    The query runs on Databricks, so Unity Catalog records which column came from which. It calls
    income_band, a Python function the setup notebook registers first.

    Returns:
        The CREATE statement, then one statement per column comment.
    """
    s = f"{CATALOG}.{SCHEMA}"
    sql = [f"""CREATE OR REPLACE TABLE {s}.return_summary
COMMENT {sql_value(TABLE_COMMENTS['return_summary'])}
AS SELECT
  return_id,
  total_income - wages_amt AS non_wage_income,
  total_income - agi_amt AS adjustments_amt,
  income_band(total_income) AS income_band
FROM {s}.return_header"""]
    for name, _, comment in COLUMNS["return_summary"]:
        sql.append(f"ALTER TABLE {s}.return_summary ALTER COLUMN {name} COMMENT {sql_value(comment)}")
    return sql


def column_facts() -> dict[str, dict]:
    """What a column summary shows for each column, worked out from the rows above.

    Returns:
        For each "table.column": its type, comment, tags, row count, empty count, smallest and largest value.
    """
    rows = {"return_header": header_rows()}
    rows["return_summary"] = [{
        "return_id": r["return_id"],
        "non_wage_income": r["total_income"] - r["wages_amt"],
        "adjustments_amt": r["total_income"] - r["agi_amt"],
        "income_band": income_band(r["total_income"]),
    } for r in rows["return_header"]]
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
