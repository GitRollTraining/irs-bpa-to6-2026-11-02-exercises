"""Tuesday's made-up batches (week 3, day 2), and the SQL that builds them in Databricks.

The setup notebook beside this file, day-02-setup.ipynb, runs it once before Tuesday, after
Monday's setup. The exercises' checks also read it on a computer with no Databricks, to know what
each batch holds. The course made up every row: no number, name or address belongs to a real
taxpayer. Each identification number starts with 000, which is never issued.

The returns are 30 of Wednesday's synthetic returns (day-03-course-data.py beside this file): the
same return_id, tax year, name, filing status and amounts. Tuesday adds the fields Wednesday's
files leave out or replace (the identification number, address, ZIP code, received date, loader
and batch), and puts in the faults.

Tables, in the catalog `course`, schema `returns` (Monday's setup made the schema):
  batch_clean     a batch of 30 returns, tax years 2021 to 2023, with no fault
  batch_dirty     the same batch with a fault of each of the five kinds put in, and one fault
                  that no column summary shows (32 rows)
  batch_governed  a copy of batch_dirty with a column mask on the identification number and a
                  row filter by tax year: the learners' group sees tax year 2023 only, and the
                  number masked; the reviewer group sees every row and the number
"""

import sqlite3

CATALOG = "course"
SCHEMA = "returns"
YEARS = (2021, 2022, 2023)
LEARNER_YEAR = 2023
BATCH_ID = "2026-11-17-a"
MADE_UP = "Made up by the course for week 3; no row is a real taxpayer."
MASKED = "***-**-****"

# The batch's columns: (name, SQL type, comment). The names follow week 3's one list of names.
COLUMNS = [
    ("return_id", "STRING", "The return's identifier in the course data."),
    ("tin", "STRING", "The taxpayer identification number."),
    ("taxpayer_name", "STRING", "The filer's name."),
    ("street_address", "STRING", "The filer's street address."),
    ("zip_code", "STRING", "The filer's five-digit ZIP code."),
    ("filing_status", "STRING", "Filing status code: 1 single, 2 married filing jointly, 3 married filing separately, 4 head of household, 5 qualifying surviving spouse."),
    ("wages_amt", "INT", "Wages, salaries and tips the filer reported, in whole dollars."),
    ("agi_amt", "INT", "Adjusted gross income on the return, in whole dollars."),
    ("total_income", "INT", "Total income on the return, in whole dollars."),
    ("total_tax_amt", "INT", "Total tax on the return, in whole dollars."),
    ("tax_year", "INT", "The tax year the return covers. This batch holds tax years 2021, 2022 and 2023."),
    ("received_date", "DATE", "The date the IRS received the return."),
    ("loaded_by", "STRING", "The user name of the clerk who loaded the batch."),
    ("batch_id", "STRING", "The delivery this row came in."),
]
NAMES = [n for n, _, _ in COLUMNS]

TABLE_COMMENTS = {
    "batch_clean": "A batch of returns, tax years 2021 to 2023, with no fault. " + MADE_UP,
    "batch_dirty": "The same batch with faults put in on purpose, for the data tests. " + MADE_UP,
    "batch_governed": "A copy of batch_dirty with a column mask and a row filter. " + MADE_UP,
}

# The 30 returns Tuesday shares with Wednesday's day-03-course-data.py, copied from its returns():
# (filer case key, tax_year, name, filing_status, wages_amt, total_income, agi_amt, total_tax_amt).
# return_id is the case key and the tax year, as Wednesday's return_rows() makes it.
SHARED = [
    ("F-30037", 2021, "ALEX SAMPLE", 2, 48000, 49200, 46440, 6502),
    ("F-30037", 2022, "ALEX SAMPLE", 2, 50000, 51330, 49340, 3947),
    ("F-30037", 2023, "ALEX SAMPLE", 2, 57500, 59340, 57360, 8030),
    ("F-30074", 2023, "SAM EXAMPLE", 4, 47000, 48720, 46490, 5579),
    ("F-30111", 2022, "RILEY TESTER", 1, 65490, 66240, 64060, 8968),
    ("F-30111", 2023, "RILEY TESTER", 1, 91590, 92300, 89720, 8972),
    ("F-30148", 2021, "JORDAN PLACEHOLDER", 4, 54330, 55660, 53690, 4295),
    ("F-30148", 2022, "JORDAN PLACEHOLDER", 4, 66070, 67400, 65850, 7902),
    ("F-30148", 2023, "JORDAN PLACEHOLDER", 4, 59410, 59750, 59450, 7134),
    ("F-30185", 2022, "TAYLOR MADEUP", 1, 32000, 32050, 30160, 3619),
    ("F-30185", 2023, "TAYLOR MADEUP", 1, 33810, 35330, 33980, 4078),
    ("F-30222", 2021, "MORGAN SAMPLE", 2, 94000, 94680, 93460, 11215),
    ("F-30222", 2022, "MORGAN SAMPLE", 2, 102540, 104260, 103120, 14437),
    ("F-30222", 2023, "MORGAN SAMPLE", 2, 101090, 102540, 100240, 12029),
    ("F-30259", 2021, "CASEY EXAMPLE", 3, 63200, 64650, 62560, 5005),
    ("F-30259", 2022, "CASEY EXAMPLE", 3, 74400, 75990, 73380, 10273),
    ("F-30259", 2023, "CASEY EXAMPLE", 3, 65430, 67350, 64700, 7764),
    ("F-30296", 2021, "JAMIE TESTER", 1, 58010, 58770, 57550, 4604),
    ("F-30296", 2022, "JAMIE TESTER", 1, 70510, 71730, 71420, 8570),
    ("F-30296", 2023, "JAMIE TESTER", 1, 73170, 73490, 73460, 10284),
    ("F-30333", 2021, "DREW PLACEHOLDER", 4, 70110, 71930, 71490, 10009),
    ("F-30333", 2022, "DREW PLACEHOLDER", 4, 67320, 68240, 66890, 6689),
    ("F-30333", 2023, "DREW PLACEHOLDER", 4, 73850, 74820, 74420, 7442),
    ("F-30370", 2021, "AVERY MADEUP", 4, 110000, 110800, 108650, 15211),
    ("F-30370", 2022, "AVERY MADEUP", 4, 105640, 105970, 105830, 12700),
    ("F-30370", 2023, "AVERY MADEUP", 4, 97640, 99510, 96800, 13552),
    ("F-30407", 2022, "ALEX SAMPLE", 2, 48000, 48110, 45420, 3634),
    ("F-30444", 2021, "SAM EXAMPLE", 1, 40950, 41580, 39260, 5496),
    ("F-30481", 2021, "RILEY TESTER", 3, 44360, 45580, 43630, 4363),
    ("F-30518", 2021, "JORDAN PLACEHOLDER", 3, 50520, 50750, 49400, 5928),
]
REFILED_FROM, REFILED_AS = "F-30111-2022", "F-30629-2022"   # F-30629: a case key no filer has

# What was put into the dirty batch, one line per fault: (kind, what, rows). For the trainer and
# for each answer's decisions file. A row is named by its return_id.
FAULTS = [
    ("completeness", "agi_amt is empty", ["F-30148-2022", "F-30296-2021"]),
    ("validity", "wages_amt is -1", ["F-30185-2023"]),
    ("uniqueness", "the whole row is there twice", ["F-30259-2022"]),
    ("consistency", "wages_amt is larger than total_income", ["F-30333-2021"]),
    ("freshness", "tax_year is 2019, a year the batch does not hold", ["F-30444-2021", "F-30518-2021"]),
    ("no column summary shows it", f"the return {REFILED_FROM} is there again under a new return_id, {REFILED_AS}: "
     "same identification number, same tax year, every value in range", [REFILED_AS]),
]


def clean_rows() -> list[dict]:
    """Make the rows of batch_clean. The same rows every time: no random numbers.

    Returns:
        One dict per return, with every column of the batch. received_date is text, YYYY-MM-DD.
        One filer keeps one identification number, name and address in every year.
    """
    rows = []
    for i, (key, year, name, status, wages, total, agi, tax) in enumerate(SHARED, start=1):
        n = (int(key[2:]) - 30000) // 37   # the filer's place in Wednesday's list, 1 to 16
        rows.append({
            "return_id": f"{key}-{year}",
            "tin": f"000-{10 + n:02d}-{4000 + 37 * n}",
            "taxpayer_name": name.title(),
            "street_address": f"{100 + 7 * n} Example Street",
            "zip_code": f"{20001 + (n % 6) * 1100:05d}",
            "filing_status": str(status),
            "wages_amt": wages,
            "agi_amt": agi,
            "total_income": total,
            "total_tax_amt": tax,
            "tax_year": year,
            "received_date": f"{year + 1}-0{2 + i % 3}-{10 + i % 18:02d}",
            "loaded_by": "intake.clerk07",
            "batch_id": BATCH_ID,
        })
    return rows


def dirty_rows() -> list[dict]:
    """Make the rows of batch_dirty: the clean rows with the faults of FAULTS put in.

    Returns:
        32 rows: the 30 clean ones, five of them changed, then the copied row and the re-filed return.
    """
    rows = [dict(r) for r in clean_rows()]
    by_id = {r["return_id"]: r for r in rows}
    by_id["F-30148-2022"]["agi_amt"] = None
    by_id["F-30296-2021"]["agi_amt"] = None
    by_id["F-30185-2023"]["wages_amt"] = -1
    larger = by_id["F-30333-2021"]
    larger["wages_amt"] = larger["total_income"] + 9000
    by_id["F-30444-2021"]["tax_year"] = 2019
    by_id["F-30518-2021"]["tax_year"] = 2019
    rows.append(dict(by_id["F-30259-2022"]))
    refiled = dict(by_id[REFILED_FROM])
    refiled["return_id"] = REFILED_AS
    rows.append(refiled)
    return rows


def learner_view(rows: list[dict]) -> list[dict]:
    """What a member of the learners' group gets back from batch_governed.

    Args:
        rows: the rows of batch_governed, as the reviewer group sees them.

    Returns:
        The rows of tax year 2025 only, each with its identification number masked.
    """
    return [dict(r, tin=MASKED) for r in rows if r["tax_year"] == LEARNER_YEAR]


def sql_value(value: object) -> str:
    """Write one Python value as a SQL literal: 'text', 123 or NULL (a quote in text gets a backslash)."""
    if value is None:
        return "NULL"
    if isinstance(value, int):
        return str(value)
    return "'" + str(value).replace("\\", "\\\\").replace("'", "\\'") + "'"


def row_values(row: dict) -> str:
    """Write one row as a SQL tuple, received_date as a DATE."""
    parts = []
    for name, kind, _ in COLUMNS:
        value = row[name]
        parts.append(f"DATE {sql_value(value)}" if kind == "DATE" and value is not None else sql_value(value))
    return "(" + ", ".join(parts) + ")"


def batch_statements() -> list[str]:
    """Write the SQL that makes batch_clean and batch_dirty with their comments and rows.

    Returns:
        The statements, in the order they run.
    """
    columns = ",\n".join(f"  {n} {k} COMMENT {sql_value(c)}" for n, k, c in COLUMNS)
    sql = []
    for table, rows in (("batch_clean", clean_rows()), ("batch_dirty", dirty_rows())):
        full = f"{CATALOG}.{SCHEMA}.{table}"
        sql.append(f"CREATE OR REPLACE TABLE {full} (\n{columns}\n) COMMENT {sql_value(TABLE_COMMENTS[table])}")
        sql.append(f"INSERT INTO {full} ({', '.join(NAMES)}) VALUES\n" + ",\n".join(row_values(r) for r in rows))
    return sql


def governed_statements(reviewer_group: str) -> dict[str, list[str]]:
    """Write the SQL for batch_governed: the copy, then the filter and the mask.

    Args:
        reviewer_group: the account group that sees every row and the full number (the trainer's).

    Returns:
        "copy": make the table; "controls": make the two functions and bind them to the table.
    """
    s = f"{CATALOG}.{SCHEMA}"
    group = sql_value(reviewer_group)
    return {
        "copy": [
            f"CREATE OR REPLACE TABLE {s}.batch_governed COMMENT {sql_value(TABLE_COMMENTS['batch_governed'])} "
            f"AS SELECT * FROM {s}.batch_dirty",
        ],
        "controls": [
            f"CREATE OR REPLACE FUNCTION {s}.learner_year_filter(tax_year INT) "
            f"RETURN IF(is_account_group_member({group}), true, tax_year = {LEARNER_YEAR})",
            f"CREATE OR REPLACE FUNCTION {s}.tin_mask(tin STRING) "
            f"RETURN CASE WHEN is_account_group_member({group}) THEN tin ELSE {sql_value(MASKED)} END",
            f"ALTER TABLE {s}.batch_governed SET ROW FILTER {s}.learner_year_filter ON (tax_year)",
            f"ALTER TABLE {s}.batch_governed ALTER COLUMN tin SET MASK {s}.tin_mask",
        ],
    }


def local_db(governed: str = "learner") -> sqlite3.Connection:
    """Load the three batches into an in-memory SQLite database, for the checks on a computer with
    no Databricks. Table names drop `course.returns.`; the checks strip it from each query.

    Args:
        governed: "learner" gives batch_governed as the learners' group sees it; "plain" gives it
            with no filter and no mask, as a workspace without them would.

    Returns:
        The open connection.
    """
    db = sqlite3.connect(":memory:")
    types = {"STRING": "TEXT", "INT": "INTEGER", "DATE": "TEXT"}
    columns = ", ".join(f"{n} {types[k]}" for n, k, _ in COLUMNS)
    dirty = dirty_rows()
    tables = {
        "batch_clean": clean_rows(),
        "batch_dirty": dirty,
        "batch_governed": learner_view(dirty) if governed == "learner" else dirty,
    }
    for table, rows in tables.items():
        db.execute(f"CREATE TABLE {table} ({columns})")
        db.executemany(f"INSERT INTO {table} VALUES ({', '.join('?' for _ in NAMES)})",
                       [[r[n] for n in NAMES] for r in rows])
    return db


def local_sql(query: str) -> str:
    """Make a Databricks query run on local_db(): drop the catalog and schema from table names."""
    return query.replace(f"{CATALOG}.{SCHEMA}.", "")
