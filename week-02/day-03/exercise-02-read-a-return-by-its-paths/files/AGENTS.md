# AGENTS.md

## The project

`returns/sample-return.xml` is a tax return written as XML. The course made it up: no real taxpayer
and no real return. `paths.csv` lists three fields of its Form 1040, one row each, with a path to
each field and a label.

## Paths

- Write each path in ElementTree's path syntax, from the root element, `Return`, one step per
  element, such as `efile:ReturnHeader/efile:TaxYr`. Do not use `//`.
- The prefix `efile:` stands for the namespace `http://www.irs.gov/efile`, and `course:` for
  `urn:course:instructor`.

## Rules

- Never print or log a value of a field that identifies a person, such as an SSN or a name.
- Do not change `returns/sample-return.xml`.
- Leave the `label` column for the person you work with.
