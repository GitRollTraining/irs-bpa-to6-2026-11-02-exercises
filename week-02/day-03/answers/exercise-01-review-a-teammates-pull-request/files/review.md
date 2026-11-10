# Review of add-penalty-cap

## My comments

- Rule 4: the cap at 500 dollars is a new branch of late_payment_penalty, and no test reaches it. Add a test at the boundary: a penalty just under 500, exactly 500, and over 500.
- Rule 3: PenaltyCapPolicy is a class with an enabled flag that nothing sets, for one min(). `min(penalty, PENALTY_CAP)` in late_payment_penalty says the same.

## Codex's comments

KEPT-RUN

## Compared

KEPT-RUN

## The change I request

- Rule 4: add a test of the 500-dollar cap, with a penalty under, at and over the cap, before this merges.
