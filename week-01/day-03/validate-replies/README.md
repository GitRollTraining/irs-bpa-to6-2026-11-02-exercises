# 3.1 Check every reply

Make `check_reply` count bad replies as failures, while good replies and the lab's tests still pass.

Five of the eight replies in `replies/` failed `check_reply` in `extractor.py`. A teammate then changed the schema and `check_reply`, and now only two fail.

## Start

Follow the [Day 3 setup](../README.md). Work by hand, without AI tools. In a new terminal in the course folder, these commands create the workspace only if it is missing, then enter it:

```sh
test -d week-01/day-03/validate-replies/lab/.git || python3 reset.py validate-replies
cd week-01/day-03/validate-replies/lab
```

All paths below are relative to `lab/`. Each reply in `replies/` is named for its note in `notes/`, and `count_failures.py` gives each reply to `check_reply`.

## Count and fix

Open `schema/output.schema.json` and `extractor.py`, the two files that the teammate changed, and count the failures:

```sh
python3 count_failures.py
```

Expect `Failures: 2 of 8 replies.` Fewer failures do not mean better replies. Use section 3.1 of the notebook to explain each change.

| Problem | Change to make |
|---|---|
| The schema lets `next_action` be null, though the lab's notes always state a next action. Reply 0138 passes with null. | In `schema/output.schema.json`, change `"next_action": {"type": ["string", "null"]}` to `"next_action": {"type": "string"}`. |
| `check_reply` guesses a number from an amount written as text. | In `extractor.py`, remove the six lines from `# The model sometimes`. |
| Reply 0130 gives tax year 2203, after this year. The schema passes any integer. | In `extractor.py`, put `import datetime` above `import json`. Put the two lines below just above `return fields`, after the schema check. |

```python
    if fields["tax_year"] > datetime.date.today().year:
        raise ExtractionFailed("the tax year is after this year")
```

<details><summary>Why each change</summary>

| Problem | Why |
|---|---|
| The schema lets `next_action` be null, though the lab's notes always state a next action. Reply 0138 passes with null. | Note 0138 ends "Wait for the call.", but reply 0138 gives null. Every note states its next action, so null there is wrong. Section 3.1, below the table of fields: "Only amount_in_question may be null, because the lab's notes always state the other four fields." |
| `check_reply` guesses a number from an amount written as text. | These lines turn "40,000 of 95,000" in reply 0105 into 4000095000, a wrong amount. A guess can be wrong, so the reply must fail instead. Section 3.1, below the second figure: "a reply that fails is counted as a failure, never repaired by guessing" |
| Reply 0130 gives tax year 2203, after this year. The schema passes any integer. | Reply 0130 gives tax year 2203, but note 0130 names 2023. The schema passes any integer, so only your own check can fail a year that has not begun. After the schema check, `tax_year` is an integer, so `>` can compare it with this year. Section 3.1, in the list above the second figure: "Tax year 2203 passes the schema, not your own check" |

</details>

Save both files, then count the failures again and check:

```sh
python3 count_failures.py
python3 ../check.py
```

Expect `Failures: 6 of 8 replies.` Finish when the check prints `Done:`. If it prints `Not yet:`, address the findings and check again. The check reads your saved files, so no commit is needed.

## Reflect

The comment you removed names "18,400": should `check_reply` turn it into 18400, and why? Which wrong tax year does your own check still pass, and what would stop it?

[Worked answer](../answers/validate-replies/) · [Start over](../../../README.md#start-an-exercise-again)
