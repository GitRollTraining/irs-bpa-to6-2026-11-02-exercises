# AGENTS.md

## The project

`form1040.py` reads named values from tax return files written as XML. The returns in `returns/`
and every value in them are made up for the course. `schema/return.xsd` is the course's schema for
them: it says which elements a return must hold and which may be missing.

## How to run the tests

From this folder, with the course environment active:

```sh
python -m pytest -q
```

## Rules

- Use only Python's standard library to read XML: `xml.etree.ElementTree`.
- Put test files in `tests/`. A test that needs another return file writes it in pytest's
  `tmp_path`; do not change the files in `returns/`.
- Never print or log a value of a field that identifies a person, such as an SSN or a name.
