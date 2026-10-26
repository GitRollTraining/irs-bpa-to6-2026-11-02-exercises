# What the case-notes extractor requires before it runs on real notes

The extractor runs on simulated notes in this course. This note pretends it will one day run on real
ones, and works out what that requires with the five moves of the week 1 chapter, section 1.2.

## The protected surface

- Fields: all five fields the extractor returns (`docs/fields.md`) come from a case note, so all
  five are return information.
- The step that crosses a boundary: a note's text leaving this repository for the model the
  extractor calls, through `model.py`.
- The steps that make new copies: a log line written when a reply fails its check, and the tests'
  fixtures.

## What it triggers, as requirements a reviewer can check

Each requirement is one line a reviewer can check from this repository alone. Where they check it
names, in backticks, the file or folder they open.

| What the protected surface triggers | Requirement a reviewer can check | Where they check it |
|---|---|---|
| Only an approved model | The extractor calls only the approved model endpoint named in the configuration | `model-route.json`, `model.py` |
| Logs that hold note text are treated as holding return information | The extractor logs the note identifier and never the note text | `extractor.py`, `logs/` |
| No real note in any fixture | The tests' fixtures are the course's simulated notes and are marked as such | `tests/` |
| Only the note text the extraction needs, and nothing else from the case | TODO | TODO |
| An audit trail of every note processed | TODO | TODO |
| Forbidden: using the extractor's output as a decision on a case | TODO | TODO |

## Open questions, and who answers them

In each row, write the role the chapter names for that question. You answer neither by writing code.

| Question | Who answers it |
|---|---|
| May the extractor be used on real case notes at all? | TODO |
| May simulated or synthetic case notes be used with a generative AI tool for this work? | TODO |
