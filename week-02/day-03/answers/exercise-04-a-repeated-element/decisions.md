# Exercise 4: decisions

For the trainer. The exercise is deck slide 52, "Extra: an element that repeats". Each section gives one thing the learner does, the reason, the notebook line it rests on, and what else the check accepts. The check is `check.py` in the exercise folder. It finds the tests that are new since the start, runs them, and reads the function on three returns.

## 1. Read the two relationship codes in two-dependents.xml

- **The answer.** The first `DependentDetail` holds `DAUGHTER`. The second holds `SON`. The learner reads only the `DependentRelationshipCd` of each.
- **Reason.** The expected values come from the file, before the function exists. The names and SSNs beside the codes stay unread, because they count as protected data even though the course made them up.
- **The notebook line.** "Read only the `DependentRelationshipCd` of each: `DAUGHTER` in the first, `SON` in the second. The names and SSNs beside it count as protected data, even though the course made them up."
- **What else the check accepts.** The check does not read the learner's notes. It tests the function on this file, and the answer must be `["DAUGHTER", "SON"]`.

## 2. Write the test first and watch it fail

- **The answer.** Two changes in `tests/test_form1040.py`. The import line becomes `from form1040 import dependent_relationships, read_form_1040`. A new test at the end, `test_a_repeated_dependent_comes_back_as_a_list`, calls `dependent_relationships` on `returns/two-dependents.xml` and expects `["DAUGHTER", "SON"]`. `files/tests/test_form1040.py` holds both.
- **Reason.** The return has two dependents, so the test expects two codes, in the order the file holds them. The learner reads the codes in the file, not from the function. A test that fails first shows that it calls the function. Step 2 gives the import line and the test whole, then a reason for each part. This follows the SOP's test 6: the step gives the answer and its reason, and the learner does the move.
- **The notebook line.** The table's row for `["DAUGHTER", "SON"]`: "You read the expected values from the sample return yourself, before the code exists." Below the table: "If you didn't watch the test fail, you don't know if it tests the right thing."
- **What else the check accepts.** Any new test, with any name, that fails when `dependent_relationships` is not written. The check compares the test names with the start's names to find the new ones. A new test that passes on the unwritten function fails the check, with a message that says it was never red.

## 3. Make it pass

- **The answer.** `dependent_relationships` in `form1040.py`. It finds `efile:ReturnData/efile:IRS1040` from the root. It runs `findall("efile:DependentDetail", NS)` and gives the `DependentRelationshipCd` text of each. `files/form1040.py` holds it. Codex may write it, or the learner may.
- **Reason.** A repeated element comes back as a list. A return with no dependent gives an empty list, so a loop over it does nothing and the code needs no special case.
- **The notebook line.** "a repeated element comes back as a list. No dependent gives an empty list"
- **What else the check accepts.** Any function that gives `["DAUGHTER", "SON"]` for `two-dependents.xml`, `["DAUGHTER"]` for the sample return, and `[]` for a copy of the sample without its dependent. All tests must pass.

## 4. Commit the function and its test

- **The answer.** `files = "form1040.py tests/test_form1040.py"` in cell 3. The commit message in the cell is "Read each dependent's relationship, test first".
- **Reason.** The commit holds the function and its test, which are the two files that changed.
- **The notebook line.** "The commit holds the function and its test."
- **What else the check accepts.** Any commit that changes `form1040.py` or `tests/` since the start. It fails when those two paths have changes that are not in a commit.

## Where each quote comes from

The curated file is the day's own file, `days/day-03/curated.md`. Both quotes below sit under the heading "Write a return reader test first", in its part "Write the test before the reader". The deck is the day's `deck.json`. Slide numbers count its `slides` from 1.

| Quote in the notebook | Curated file: heading and line | Deck slide |
|---|---|---|
| "You read the expected values from the sample return yourself, before the code exists." | Write the test before the reader, line 618 | not on a slide (deck slides 43 and 45 say it in other words) |
| "If you didn't watch the test fail, you don't know if it tests the right thing." | Write the test before the reader, line 614 | deck slide 43 |

## Quotes with no source in the day's files

None.

## Findings of the linter inside quotes

None.
