# Four uses of AI tools

The course made up these files. Read `exports/case-2231.txt` as a real case note. Each path starts at the folder
`~/practice/week-01/day-01/data-rules-check/lab`.

The course's approved tool is the model that the extractor calls. Its approval covers only the simulated
notes in `notes/`. No other use has an approval.

- Permitted?: Yes, No, or Not mine to decide.
- Who decides: write a role only for Not mine to decide.
- Why: the fact in the file, and the section of the rule, such as (section 1.1).

| Use | File | Tool | Permitted? | Who decides | Why |
|---|---|---|---|---|---|
| 1 | `notes/0147.txt` | The course's approved tool | Yes | - | The note names a synthetic filer, so it is a simulated note. The approval covers it (section 1.2) |
| 2 | `exports/case-2231.txt` | A public chat tool | No | - | Without its name, the note still gives year, form, amount, date. So it can still point at one taxpayer (section 1.1) |
| 3 | `exports/case-2231.txt` | The course's approved tool | Not mine to decide | The accountable official | It is a real note, and the approval covers only simulated notes. Use approval goes to the accountable official (section 1.2) |
| 4 | `model.py` | A public chat tool | No | - | It holds no taxpayer data. But the policy covers "any information, including seemingly innocuous work-related matters", in public AI tools (section 1.1) |
