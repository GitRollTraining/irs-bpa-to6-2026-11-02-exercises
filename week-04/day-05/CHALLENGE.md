# A second examination group asks for its own list

The Harbor examination group is a made-up group of examiners. It has never used a model. Its
manager has seen another group's list and writes to you:

> Each year more returns reach us than our examiners can open. We can open about **4 returns for
> every 100** that reach us. We want a list of this year's new returns, in the order our examiners
> should open them, learned from our own past results. Two things worry us. An examination that
> closes with **no change** costs an examiner about six hours and asks the taxpayer to answer our
> letters for nothing. A return that would have **changed** and that nobody opens leaves the tax as
> filed, and our yearly report counts it as missed. Our director asks about both. We do not know
> which should weigh more for us: tell us which you weigh more, and why, and set our list by it.
> We need to be able to defend the list: why a return is on it, and whether it falls more on one
> of our two (made-up) groups of returns, A and B.
>
> A side question. Our examiners write a short summary on each case's cover sheet. Could a
> language model write it, or should someone train a model for it? We keep no past summaries
> marked good or bad.
>
> A second task. Taxpayers whose examination closes with a change often write to ask about paying
> over time. About 40 such letters reach us each week, and we want each one sent to the team that
> answers it: one of three teams. Our mail room keeps 6,000 past letters of this kind, each marked
> with the team that answered it. A letter sent to the wrong team waits until that team sends it
> on.

Everything here is made up by the course: the group, its returns, its amounts and its results.
Groups A and B are synthetic and stand for no real or protected class. A score is a relative
risk indicator, never a finding: the list says which returns an examiner opens first and says
nothing about any taxpayer. Whether a return is selected for examination is always a person's
decision, never the model's.

## Work in Databricks

Create, run and check your work in Databricks; do not develop a solution locally and import it.
Use the walkthrough in [START_HERE.md](START_HERE.md). Genie Code is optional; the trainer may
assign the [optional Codex route](OPTIONAL_TOOLS.md). The training team supplies compute,
read-only input tables with their descriptions, and your own MLflow experiment folder. Missing
access is an environment issue for the trainer.

## What the group sends

Two read-only tables in `training.to6_challenge4_inputs`. One row is one return.

- `closed_returns`: the group's past returns, tax years 2020 to 2023, each with the group's
  recorded result where an examination had closed when the extract was made.
- `new_returns`: this year's new returns, tax year 2024. None has been examined; they have no result.

| Column | What it holds | Where it comes from, and when it is written |
|---|---|---|
| `return_id` | the return | the group's extract |
| `tax_year` | the return's tax year | the filed Form 1040 |
| `filer_zip` | a made-up code for the area of the filer's address | the return's header (name and address), when filed |
| `wages_amt` | wages | the Form 1040 body, when filed |
| `wages_prior_year_amt` | wages on the filer's previous year's return | the previous year's Form 1040 body |
| `agi_amt` | adjusted gross income | the Form 1040 body, when filed |
| `deduction_amt` | the standard or itemized deduction | the Form 1040 body, when filed |
| `total_tax_amt` | total tax | the Form 1040 body, when filed |
| `withholding_amt` | federal income tax withheld; empty where the extract holds no amount | the Form 1040 body, when filed |
| `prior_year_amended` | 1 when the filer amended the previous year's return, else 0 | the group's filing records, before this year's return is filed |
| `posted_adjustment_amt` | the amount the group's case system posted to the taxpayer's account for this return; 0 when nothing was posted | the group's case system, on the day a case on the return closes |
| `synthetic_group` | A or B: made up by the course for the group's question about groups | added by the course |
| `exam_result` (`closed_returns` only) | the group's recorded result: `change` or `no change`; empty where the examination had not closed | the group's case records, when the examination closes |

The same descriptions are on the tables in Catalog Explorer.

## The group's rules

These are the group's, not engineering choices. How you meet them is yours.

1. **Learn only from what is known when a new return is scored**, before anyone selects it.
2. **No feature identifies the filer or where the filer lives** (the course's need-to-know rule).
3. **`synthetic_group` is for the question about groups only**; it is never a feature.
4. **A result is only a closed examination's result.** An empty `exam_result` is neither outcome.
5. **Learn from tax years 2020 to 2022, judge on 2023, list from 2024.** The 2023 returns never
   train a model or any step fitted to the data.
6. **Two candidates of different model types**, each recorded as its own MLflow run, compared
   from what the runs recorded.
7. **The list is read from the group's capacity: 4 returns for every 100 scored.** Count the
   hundreds on the returns the list is read from: when you judge a candidate on 2023, the 2023
   returns that have a closed result; when you give the group its list, the 2024 returns. For
   example, on 500 scored returns the threshold is the score of the 20th return. The list never holds more
   returns than the capacity: when returns share the score at the cut, you break the tie, and you
   write down how the group chooses between them.
8. **Nothing you write makes a finding about a taxpayer.** The explanation says what moved a score.

## What the group asks of you

Work toward these connected outcomes. Choose the implementation yourself.

1. **Know the group's result.** Say what the label records. Count its values before training,
   and set the accuracy every candidate must beat.
2. **Choose what the model may learn from.** Defend each feature you keep by its source field, its
   reason and its timing; name the columns you leave out, in one line. Handle empty amounts so that a
   missing amount and a true zero stay different.
3. **Train and record two candidates.** Record each as its own run; compare them from the runs,
   beside the accuracy they must beat. The notebook's given cell writes `outputs/runs.csv` from
   the runs.
4. **Set the group's list.** On the 2023 returns, count each candidate's correct and wrong predictions of
   both kinds, with precision and recall. Write which error costs more **for this group**, and why.
   Choose the candidate and the threshold by that sentence, read within the group's capacity
   (rule 7). Then score the 2024
   returns with the chosen candidate and give the group its list.
5. **Make the list defensible.** Explain the return at the top of the 2024 list in two
   sentences an examiner can read; the notebook's given cell shows what moved its score. Compare how much of
   group A's and group B's 2023 returns the list takes, with the counts, as a result that needs a
   reason. The group also proposes `prior_year_amended` as a new feature: check whether it could
   stand in for group A or B, and say whether you would add it.
6. **Choose the technique for two tasks.** Trained model or prompting for the cover-sheet summary:
   decide from the labelled data the group has, the cost, and the harm a wrong summary would do,
   and say who checks the output. Then the second task: trained model or prompting for sending
   each letter about paying over time to the team that answers it, decided the same way, by the
   labelled data the group has, the cost, and the harm a letter sent to the wrong team would do,
   and say who checks the output.

**The decisions are yours.** Which error costs more for this group, which candidate and threshold
follow from it, and which columns the model may learn from are judgments the group asks of you,
not of a tool. An AI tool may help you build and check the work; the reasons you give must be your own.

## What to submit and how it is checked

Your public fork's `main` branch must contain, in its `week-04/day-05/` folder:

- `notebook.py`: readable notebook source with your implementation and its checks.
- `SUBMISSION.md`: your report to the group, under its headings.
- `outputs/runs.csv`: your two candidates' runs as read back from MLflow, written by the
  notebook's given cell. It keeps only the run ID, the run name, the parameters recorded (the
  settings, split and measure) and the metrics: never your user name or a notebook path.
- `outputs/new_returns_list.csv`: the 500 new returns with `return_id`, the chosen candidate's
  score and whether the return is on the list.

Write two kinds of reason in full in `SUBMISSION.md`: for the threshold, which error costs this
group more and how that set the threshold; and for each technique choice, its reasons. Every
learner writes them. The trainer reads them, and may ask a learner whose written reasons look thin
or copied to explain one choice aloud for 2 to 3 minutes, during block 3 or the close. This is
part of the Challenge's check that the learner owns the work, not a separate grade. The written
parts are judged on their numbers and reasons, not their length.

Any other small export that supports your report may go under `outputs/`. Keep every export small
and made of these made-up returns only. Screenshots may supplement the files but cannot replace
code or saved outputs. Leave the navigation README in place.

Author the submission and exports inside Databricks. For the browser route, commit and push
through the Git folder of your fork; for the trainer-assigned [optional route](OPTIONAL_TOOLS.md),
use its submission procedure. Verify that the exact GitHub commit contains the notebook, report
and exports in `week-04/day-05/`, and that your fork is public.

In Classroom, submit your fork's base URL (`https://github.com/{owner}/{repo}`), `main` and
the final submitted commit SHA. The assignment gives the deadline.
