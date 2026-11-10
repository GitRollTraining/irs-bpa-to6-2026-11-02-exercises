# Exercise 3: decisions

For the trainer. The exercise is deck slide 51, "A return reader, test first". Each section gives one thing the learner does, the reason, the notebook line it rests on, and what else the check accepts. The check is `check.py` in the exercise folder. It runs the learner's tests three times on copies of `lab`, then reads the learner's commit.

## 1. Install the test-driven-development skill

- **The answer.** The `npx` command of step 2, run in `lab`. It puts the skill into `lab/.agents/skills/test-driven-development`, where Codex finds it.
- **Reason.** The skill makes Codex write a test, see it fail, and only then write the code. It is the install command of Tuesday's exercise 3, so the learner knows it.
- **The notebook line.** "It is the install command of Tuesday's exercise 3. It copies the skill's folder from GitHub into `.agents/skills/test-driven-development` in `lab`, where Codex finds it."
- **What else the check accepts.** Any way to put `SKILL.md` at that path. The install needs internet access and Node.js. A learner without `npx` tells the trainer, as the step says.

## 2. Read the three expected values in the return

- **The answer.** `WagesAmt` is 52340, `TaxableInterestAmt` is 120, and `AdjustedGrossIncomeAmt` is 52460. All three are inside `IRS1040`.
- **Reason.** The learner reads the expected values from the return before the code exists. A test that copies the reader's own output proves nothing.
- **The notebook line.** "Mistake: copying actual, computed values & pasting them into the expected values of the test."
- **What else the check accepts.** The check does not read the learner's notes. It tests the reader on the sample return. The reader must give these three numbers.

## 3. Ask Codex to write the tests first, then the reader

- **The answer.** One request, in the learner's own words. It starts with `$test-driven-development`. It names `read_form_1040` in `form1040.py` and the tests in `tests/test_form1040.py`. It gives the three values, asks for one test on a return without `TaxableInterestAmt`, and says not to commit. The folded request in the notebook is one way to say it.
- **Reason.** Each part of the request has a reason in the step's table. The missing-element test is the main one. The schema lets a return leave the element out. ElementTree gives None for an element it does not find, so a reader that reads `.text` of None crashes.
- **The notebook line.** "The schema lets a return leave the element out. ElementTree gives None for an element it does not find, and a reader that reads `.text` of None crashes."
- **What else the check accepts.** The check does not read the request. It tests the result, and it accepts any wording.

## 4. The tests

- **The answer.** Two tests. One reads the sample return and expects the three values. One reads a copy of the sample without `TaxableInterestAmt`, written in `tmp_path`, and expects `taxable_interest` to be None, with the other two values unchanged. `files/tests/test_form1040.py` holds them.
- **Reason.** The first test shows the reader gives the right values. The second shows what the reader does with a missing element. Red, then green, shows that the tests call the reader.
- **The notebook line.** "If you didn't watch the test fail, you don't know if it tests the right thing."
- **What else the check accepts.** Any tests that pass on three conditions. They pass on the learner's reader. They fail on a reader that is not written yet. At least one of them fails on a reader that crashes when `TaxableInterestAmt` is missing. The check does not read test names or the way a test builds its copy. Extra tests do no harm. In the kept run, the agent added a third test of its own. It reads a return whose Form 1040 has no `WagesAmt`. `files/tests/test_form1040.codex.py` holds all three tests.

## 5. The reader

- **The answer.** `read_form_1040` in `form1040.py`. It finds `efile:ReturnData/efile:IRS1040` from the root. It reads each of the three elements in that form and gives whole dollars. It gives None for an element the return leaves out. `files/form1040.py` holds it.
- **Reason.** A path from the root reaches the Form 1040's `WagesAmt` and not the W-2's. The docstring in the starting file is the contract: three keys, whole dollars, None for a missing value.
- **The notebook line.** "The docstring is the reader's contract: the three keys, whole dollars, and None for a value the return leaves out."
- **What else the check accepts.** Any code that gives 52340, 120 and 52460 for the sample return. It must give None for the interest of a copy without `TaxableInterestAmt`, with the other two values unchanged.

## 6. Commit the reader and its tests

- **The answer.** `files = "form1040.py tests/test_form1040.py"` in cell 2. The commit message in the cell is "Read three Form 1040 values, test first".
- **Reason.** The commit holds the reader and its tests. The skill's files and `skills-lock.json` stay out, because the install made them and not the change.
- **The notebook line.** "The commit holds the reader and its tests. The skill's files and `skills-lock.json` stay out: the install made them, not the change."
- **What else the check accepts.** Any commit that changes `form1040.py` or `tests/` since the start. It fails when those two paths have changes that are not in a commit. The skill's files may stay uncommitted.

## Where each quote comes from

The curated file is the day's own file, `days/day-03/curated.md`. All headings below sit under the heading "Write a return reader test first". The deck is the day's `deck.json`. Slide numbers count its `slides` from 1.

| Quote in the notebook | Curated file: heading and line | Deck slide |
|---|---|---|
| "Mistake: copying actual, computed values & pasting them into the expected values of the test." | Write the test before the reader, line 619 | not on a slide (deck slide 43 says it in other words) |
| "If you didn't watch the test fail, you don't know if it tests the right thing." | Write the test before the reader, line 614 | deck slide 43 |
| "Which elements need a missing-element test? Exactly those the schema marks `minOccurs="0"`." | Write the test before the reader, line 675 | not on a slide (deck slide 46 says it in other words) |

## Quotes with no source in the day's files

None.

## Findings of the linter inside quotes

None.
