# CODEMAP: payment_job

Entry point: `payment_job/__main__.py` (`python -m payment_job data/accounts.csv report.txt`).

## Flow

```
__main__.main(argv)
   │
   ├─▶ reader.read_accounts(argv[0])      CSV rows ──▶ list of Account
   │
   ├─▶ rules.penalty_for(account)         once per account
   │        └─▶ rules.late_payment_penalty(months_late, unpaid_tax)
   │
   └─▶ writer.write_report(argv[1], lines)   title + one line per account
            ├─▶ settings.SETTINGS["report_title"]   (read at import)
            └─▶ rules.RATE                          (imported inside the function)
```

Returns 0 when the report is written. `reader.load_relief_areas` is not part of the run (see Risky spots).

## Owners

- `payment_job/__init__.py`: package docstring only.
- `payment_job/__main__.py`: command-line entry; wires reader, rules and writer.
- `payment_job/reader.py`: the `Account` dataclass, reading the accounts CSV, loading the relief list.
- `payment_job/rules.py`: the penalty rule (`RATE` 1% a month, `CAP_MONTHS` 10) and the per-account wrapper.
- `payment_job/settings.py`: loads `data/job_settings.json` into `SETTINGS`.
- `payment_job/writer.py`: formats and writes the report file.

## Imports

- `__main__.py -> reader.py`
- `__main__.py -> rules.py`
- `__main__.py -> writer.py`
- `rules.py -> reader.py`
- `writer.py -> settings.py`
- `writer.py -> reader.py`
- `writer.py -> rules.py` (inside `write_report`, `writer.py:15`, not at the top)

## Checks

- `payment_job/reader.py:34`: row must have `account_id` and `area`, else `ValueError`.
- `payment_job/reader.py:36`: `int()` / `float()` conversion of `months_late` and `unpaid_tax` (raises `ValueError` on bad text; a missing column raises `KeyError`).
- `payment_job/reader.py:37`: `months_late` and `unpaid_tax` must not be negative, else `ValueError`.
- `payment_job/rules.py:21`: `months_late` must not be negative, else `ValueError` (repeats the reader check).
- `payment_job/rules.py:23`: `unpaid_tax <= 0` returns 0.0 (no error).
- `payment_job/rules.py:25`: months capped at `CAP_MONTHS`.
- `payment_job/__main__.py:16`: none. `argv[0]` / `argv[1]` are not checked (`IndexError` if missing).

## Risky spots

Runs at import:
- `payment_job/settings.py:5`: reads and parses `data/job_settings.json` the moment `settings` is imported. Any import of `writer` triggers it; a missing or bad file fails at import.
- `payment_job/reader.py:6`: `RELIEF_FILE` path built at import (no file read).

Side effects:
- `payment_job/writer.py:19`: writes (overwrites) the report file at the given path. `.gitignore` ignores `report.txt`.
- `payment_job/__main__.py:23`: `sys.exit` on run as a script.

Fragile structure:
- `payment_job/writer.py:15`: import inside the function; hides the `writer -> rules` dependency.
- `payment_job/reader.py:43`: `load_relief_areas` is never called by any module. `data/relief_areas.txt` has no effect on penalties.
- Paths to `data/` are built from `__file__` in `reader.py:6` and `settings.py:5` (two places).

No tests:
- No test files exist in the repo. `.gitignore` lists `.coverage`, but nothing produces it.
- Untested: all six modules, especially `rules.late_payment_penalty` (cap, zero, negative) and `reader.read_accounts` (bad rows).

## Read next

1. `payment_job/rules.py`: the business rule, any edit lands here.
2. `payment_job/reader.py`: validation and the unused relief loader.
3. `payment_job/writer.py`: the import-time settings read and the hidden `rules` import.
4. `data/relief_areas.txt` and `data/accounts.csv`: the data the job and the unused loader point at.
