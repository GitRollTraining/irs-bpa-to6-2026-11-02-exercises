# Exercise 2: decisions

For the trainer. The exercise is deck slide 34, "Read a return by its paths". Each section gives one thing the learner does, the reason, the notebook line it rests on, and what else the check accepts. The check is `check.py` in the exercise folder. It reads `lab/paths.csv` and follows each path in `lab/returns/sample-return.xml` with ElementTree.

## 1. The path to the wages on Form 1040

- **The answer.** `efile:ReturnData/efile:IRS1040/efile:WagesAmt`. Codex writes it into the `path` column of `paths.csv`. The learner checks it against the file. `files/paths.csv` holds the kept answer.
- **Reason.** The path starts at the root and names one element for each step. The sample holds two `WagesAmt` elements, one in the Form 1040 and one in the W-2. A path through `IRS1040` reaches the right one.
- **The notebook line.** "The sample has two elements named `WagesAmt`: one in the Form 1040 and one in the W-2."
- **What else the check accepts.** Any path that reaches the same element as the kept path, without `//`. For example, the same path with a leading `./`. A path that reaches the W-2's `WagesAmt` fails, with a message that says it reaches a different field.

## 2. The path to the dependent's SSN

- **The answer.** `efile:ReturnData/efile:IRS1040/efile:DependentDetail/efile:DependentSSN`.
- **Reason.** Every element of the return is in a namespace, so every step has a prefix. This path shows the field's place: a dependent, inside the Form 1040.
- **The notebook line.** "Every element of the return is in a namespace, so the path has a prefix on every step."
- **What else the check accepts.** Any path without `//` that reaches the first `DependentDetail`'s `DependentSSN`. The sample holds one dependent.

## 3. The path to the review label

- **The answer.** `efile:ReturnData/efile:IRS1040/course:ReviewLabel`.
- **Reason.** The course added this element in its own namespace. So its step takes the prefix `course:`, and the other steps take `efile:`. `AGENTS.md` in `lab` gives both prefixes to Codex.
- **The notebook line.** "Did the course add the field for the trainer, in its own namespace, `course:`? No real return holds it." Step 2 also says the request uses "the prefixes `efile:` and `course:` that `AGENTS.md` gives".
- **What else the check accepts.** Any path without `//` that reaches the same element. A path with the wrong prefix finds nothing, and the check says so.

## 4. The three labels

- **The answer.** Wages: `made-up test value`. The dependent's SSN: `protected data`. The review label: `instructor-only label`.
- **Reason.** The learner asks three questions in order and stops at the first yes. First: did the course add the field for the trainer? Then the label is `instructor-only label`. Second: does the field identify a person? Then the label is `protected data`, even when the course invented the value. Otherwise the label is `made-up test value`. The sorting is about the field, not about this file's values. Step 3 gives the three questions, then a table with each row's label and its reason. The learner types the label after the row's last comma. This follows the SOP's test 6: the step gives the answer and its reason, and the learner does the move.
- **The notebook line.** Above step 3's table: "you never print, log or paste a protected field into a coding agent." The table's SSN row: "the same field on a real return is taxpayer data."
- **What else the check accepts.** Capitals and spaces around the label do not matter. The check accepts no other label. A wrong label gets a message that gives the reason for the right one.

## 5. A broken copy of the return

- **The answer.** `broken.xml`, a copy of the sample with one closing tag deleted. The kept answer deletes `</WagesAmt>`. `files/broken.xml` holds it.
- **Reason.** The learner sees what the parser says when an element opens and never closes. A deleted tag in the Form 1040 gives a mismatch, and the parser names the first closing tag that does not match.
- **The notebook line.** "Open `lab/broken.xml` in the editor. Inside `IRS1040`, delete one closing tag, for example `</WagesAmt>`, and save."
- **What else the check accepts.** Any change that makes the file not well-formed. The tag need not be `</WagesAmt>`. The check parses the learner's own copy.

## 6. The parser's line in parse-error.txt

- **The answer.** `mismatched tag: line 35, column 6`. The learner copies the line that cell 3 prints. `files/parse-error.txt` holds it.
- **Reason.** The line number is where the parser noticed the fault. It is at or after the line the learner changed. So the learner reads upward from it.
- **The notebook line.** "Make a new file, `lab/parse-error.txt`, and copy the line that cell 3 prints into it."
- **What else the check accepts.** Any text that holds the words `line` and the number the parser reports for the learner's own copy. A deletion in another place gives another number, and the check reads that number.

## Where each quote comes from

The curated file is the day's own file, `days/day-03/curated.md`. All headings below sit under the heading "Read a return's XML by its paths". The deck is the day's `deck.json`. Slide numbers count its `slides` from 1.

| Quote in the notebook | Curated file: heading and line | Deck slide |
|---|---|---|
| "A path names each element on the way down, one step per element." | Write a path from the root to a value, line 393 | not on a slide |
| "Every element of the return is in a namespace, so the path has a prefix on every step." | Write a path from the root to a value, line 421 | not on a slide |
| "Selects all subelements, on all levels beneath the current element." | Write a path from the root to a value, line 425 | deck slide 27 |
| "The sample has two elements named `WagesAmt`: one in the Form 1040 and one in the W-2." | Write a path from the root to a value, line 426 | not on a slide (deck slide 27 says it in other words) |
| "you never print, log or paste a protected field into a coding agent." | Sort each field before you use it, line 443 | not on a slide (deck slide 29 says it in other words) |
| "the same field on a real return is taxpayer data." | Sort each field before you use it, line 439 | deck slide 29 |
| "A path with `//` finds both, and nothing in it says which form you mean." | Write a path from the root to a value, line 427 | not on a slide |
| "The sorting is about the field, not this file's values." | Sort each field before you use it, line 442 | not on a slide |
| "Read upward from the reported line to the element that was never closed." | Read the parser's error on a broken document, line 473 | not on a slide (deck slide 30 says it in other words) |

## Quotes with no source in the day's files

None.

## Findings of the linter inside quotes

None.
