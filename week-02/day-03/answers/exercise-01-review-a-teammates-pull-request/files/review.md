# Review of add-penalty-cap

## My comments

- Rule 4: the cap at 500 dollars is a new branch of late_payment_penalty, and no test reaches it. Add a test at the boundary: a penalty just under 500, exactly 500, and over 500.
- Rule 3: PenaltyCapPolicy is a class with an enabled flag that nothing sets, for one min(). `min(penalty, PENALTY_CAP)` in late_payment_penalty says the same.

## Codex's comments

- Rule 4 (Tests): the cap has no test. No test input makes a penalty above 500, so a wrong cap value would pass all 9 tests.
- Rule 3 (Complexity): PenaltyCapPolicy has an enabled switch and a cap argument that its one caller never uses; min(penalty, PENALTY_CAP) does the same.
- Rule 1 (Design): the rest of rules.py is plain functions and constants; a class is not how this file is built.
- Rule 2 (Functionality): no account in data/accounts.csv can reach 500, so running the job cannot show the cap working; the cap binds only above 5,000 dollars of unpaid tax.
- Rule 5 (Size): passes, 24 added lines, one change.

## Compared

- Both of us: the missing test of the cap (rule 4) and the class nothing needs (rule 3).
- Only Codex: that the class does not fit how the file is built (rule 1), that the sample data never reaches the cap (rule 2), and that the size passes (rule 5).
- Only me: the boundary values for the test, under, at and over 500.

## The change I request

- Rule 4: add a test of the 500-dollar cap, with a penalty under, at and over the cap, before this merges.
