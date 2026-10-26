# Exercise repository template

The starting point of a Program's exercise repository: the public repository a Cohort's learners
clone as `~/practice`, holding only their exercises' starting states, filed by week and live day.
This template holds no exercise. Exercises are written by the curriculum's exercise SOP,
`sops/material/exercises.md`, in the Program repository, and built into an exercise repository
by one command.

## The repositories, and how they connect

```
gitroll-dev/curriculum (internal)
  sops/material/exercises.md ............ how an exercise is written and filed
  scripts/week/build_exercise_repository.py ... the build below
          |
          | the SOP writes each exercise in
          v
gitroll-dev/program-<program-id>-<topic> (internal, trainers are collaborators)
  practice/<exercise>/ ................... starting state, authored and tested here
  practice/answers/<exercise>/ ........... its answer; never leaves this repository
  domains/<domain>/days/day-NN/extract.md  the day's exercise blocks
          |
          | build_exercise_repository.py (copies no answers/)
          v
GitRollTraining/<program-id>-exercises (PUBLIC; made from this template)
  week-NN/day-NN/<exercise>/ ............. starting state, learner README, notebook
          |
          | "Use this template", once per Cohort, then tag start
          v
GitRollTraining/<program-id>-<start-date>-<cohort-id>-exercises (PUBLIC)
  what a Cohort's learners clone as ~/practice
```

| Repository | Visible to | Holds | Changed by |
|---|---|---|---|
| `gitroll-dev/exercise-repository-template` | organization | this README, `.github/check_repository.py`, its workflow, `.gitignore` | pull request here |
| `gitroll-dev/program-<program-id>-<topic>` | organization and the Program's trainers | each exercise's starting state and answer, and its block in the week's `activities.md` | the exercise SOP, by pull request there |
| `GitRollTraining/<program-id>-exercises` | anyone | every built day; a template for the Cohort copies | the build, by pull request here; never by hand |
| `GitRollTraining/<program-id>-<start-date>-<cohort-id>-exercises` | anyone | one Cohort's copy, its first commit tagged `start` | made once per Cohort |

Task Order 6 today: `gitroll-dev/program-irs-bpa-to6-data-ai` builds
`GitRollTraining/irs-bpa-to6-exercises`, copied as
`GitRollTraining/irs-bpa-to6-2026-11-02-cohort-1-exercises`. Task Order 4 has no exercise
repository: its week 1 exercises are not written yet, and the program owner ruled none today
(2026-10-26).

## What a built exercise repository holds

```
README.md                    the practice environment: setup, the day table, start again
check_setup.py  reset.py     the kit's shared files, at the root, so ~/practice/reset.py,
model.py  model-route.json   ~/practice/model.py and ~/practice/notes/ keep their paths
notes/  lab-states/
week-01/day-01/README.md     the day's exercises, one line each
week-01/day-01/<exercise>/   its starting files, README.md (what the learner reads) and,
                             when its kit has no start.py, <exercise>.ipynb
.github/                     from this template
```

A week is the Domain's place in the Program's `domainIds` (`programs/<program-id>/program.json` in
the curriculum); a day is the day whose `extract.md` holds the exercise's block. Days are
numbered inside each week, as the Program repository numbers them.

## Make a Program's exercise repository (once per Program)

1. `gh repo create GitRollTraining/<program-id>-exercises --public --template
   gitroll-dev/exercise-repository-template`, then clone it.
2. From a curriculum checkout:
   `python3 scripts/week/build_exercise_repository.py <program-repository> <exercise-repository>`.
   It needs a clean checkout of the Program repository at the commit to publish. Name
   `week-NN/day-NN` folders after the two paths to build only those days.
3. In the exercise repository: `python3 .github/check_repository.py` prints `OK`.
4. Verify the moved exercises from a fresh clone tagged `start`: each one's `python3 reset.py
   <exercise>` restores it, its done check on the start does not print `Done:`, and with its
   answer from the Program repository's `practice/answers/` it does.
5. Commit on a branch, open a pull request, merge when its `check` is green.
6. Settings, General: tick "Template repository", so each Cohort's copy is made from it.

An exercise changes in the Program repository, never here. After it merges there, build again
(step 2) and open a pull request here.

## Make a Cohort's copy (once per Cohort, before its first live day)

1. `gh repo create GitRollTraining/<program-id>-<YYYY-MM-DD>-<cohort-id>-exercises --public
   --template GitRollTraining/<program-id>-exercises`, the date being the Cohort's first day and
   the Cohort id the one in the Program repository's `delivery/config.json`.
2. Clone it, then `git tag start` and `git push origin start`. `reset.py` restores a folder from
   the commit tagged `start`; without the tag a learner's reset fails.
3. Give the hosting team its address: each workspace clones it as `~/practice` before day 1.
4. Each day's Classroom post links that day's folder,
   `https://github.com/GitRollTraining/<repository>/tree/main/week-NN/day-NN`.

## Answers

Never in an exercise repository: the Program's and every Cohort's are public. Each exercise's
answer stays in the Program repository's `practice/answers/`, which the Program's trainers open,
and passes the exercise's done check there. A learner's Answer line reads "your trainer has it,
and shows it at the debrief." Two checks hold this:

- the build stops when a built file names an answers folder, or has the same bytes as an answer
  file that is not also a starting file (17 of Task Order 6's 58 answer files equal a starting
  file, such as an unchanged `check.py`, and reveal nothing);
- `.github/check_repository.py`, run on every push, fails on any path named `answers`.

A done check can still show what it checks for: `data-rules-check/check.py` holds the six answers
its table must give.

## Checked on 2026-10-26, Task Order 6 week 1

Built from `gitroll-dev/program-irs-bpa-to6-data-ai` at commit `6056cb47`: 15 exercises (days 1
to 5: 3, 3, 3, 4, 2), 6 of them with a notebook. In a clone tagged `start`, all 15 reset, all 15
starts print `Not yet:` (or failing tests), 13 answers print `Done:` (or `6 passed`), and the tree
was clean after each reset. Not run: the answers of `score-the-prompt` and `direct-run-one`,
which call a model or a coding agent.

## Open, for whoever owns this next

| What | Why it is open |
|---|---|
| A notebook for each exercise whose kit has `start.py` (9 of 15) | `scripts/week/build_notebook.py` stops on such a kit; those exercises have a README only |
| A fix during a Cohort | the Cohort's `start` tag marks the first commit; a fix pushed later is not what `reset.py` restores until the tag moves |
| The verification in step 4 as one command | it ran from a script with one recipe per Task Order 6 exercise, not from anything an exercise records |
| Task Order 4 | its kit is a Pega application archive per live day, not files; the layout may need a form of its own |
| The answers' own commands | `score-the-prompt`'s answer finds its files by a relative path that holds in the Program repository's flat `practice/` only |

## The SOPs this follows

- `sops/material/exercises.md` (curriculum): what an exercise is, the tests it passes, and § Where a
  day's exercises live.
- `templates/practice-environment.md` (curriculum): the practice environment every Program writes
  as `practice/README.md`, which becomes this repository's README.
- `sops/material/classroom-delivery.md` (curriculum): the day posts that link each day's folder.
