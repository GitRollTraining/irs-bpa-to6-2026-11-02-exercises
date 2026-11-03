# 4.3 Read every diff view

Read a coding agent's change in four forms of `git diff`, and commit only what its directing prompt asks for.

A coding agent made one more run in the lab and staged part of its change. Review the change before you commit it.

## Start

Follow the [Day 4 setup](../README.md). Work by hand, without AI tools. In a new terminal in the course folder, these commands create the workspace only if it is missing, then enter it:

```sh
test -d week-01/day-04/diff-views/lab/.git || python3 reset.py diff-views
cd week-01/day-04/diff-views/lab
```

All paths below are relative to `lab/`. Read `docs/directing-prompt.md`: your directing prompt and the agent's report. Compare the files they name with what Git shows.

## Read and stage

Use section 4.3 of the notebook to explain each answer.

| What the form shows | Form, and the change to make |
|---|---|
| Only the changes not staged yet | `--name-status` |
| Every change since the last commit, staged or not: also `prompts/system.txt`, which the directing prompt does not allow | `HEAD --name-status`, then unstage `prompts/system.txt` |
| What your commit will hold: it needs `extractor.py`, which the agent did not stage | Stage `extractor.py`, then `--staged --name-status` |
| What your commit changed | `HEAD^ HEAD --name-status` |

<details><summary>Why each answer</summary>

| What the form shows | Why, in section 4.3 |
|---|---|
| Only the changes not staged yet | This form compares the files on disk with the staging area. So it misses what the agent staged. The list "The trap: the plain form": "Shows only changes still unstaged". |
| Every change since the last commit, staged or not: also `prompts/system.txt`, which the directing prompt does not allow | This form compares the files on disk with the last commit, staged or not. It shows `prompts/system.txt`, which the agent staged but did not report. The directing prompt does not allow that file, so you unstage it. Under "Start wide, then point --exit-code at HEAD for the tests.": "a file outside what the directing prompt allowed is a finding". |
| What your commit will hold: it needs `extractor.py`, which the agent did not stage | This form compares the staging area with the last commit: what your commit will hold. The directing prompt asks for both changes, but the agent did not stage `extractor.py`. So you stage it. The list "The trap: the plain form": "Run git diff --staged before every commit". |
| What your commit changed | `HEAD` is now your commit, and `HEAD^` the one before. So this form shows what your commit changed. The list "A diff shows lines": "HEAD: the commit you are on". "HEAD^: the one before". |

</details>

Read the change in the forms of rows 1 and 2:

```sh
git diff --name-status
git diff HEAD --name-status
```

Expect only `extractor.py`, then all three files. `--name-status` lists only the files; `M` marks a changed file.

Unstage `prompts/system.txt`, stage `extractor.py`, and read what your commit will hold:

```sh
git restore --staged prompts/system.txt
git add extractor.py
git diff --staged --name-status
```

Expect `extractor.py` and `tests/test_extractor.py`. `git restore --staged` keeps the change on disk.

Commit, read your commit, then check:

```sh
git commit -m "Fail a reply whose amount is negative"
git diff HEAD^ HEAD --name-status
python3 ../check.py
```

Expect `2 files changed, 9 insertions(+)`, then the same two files. Finish when the check prints `Done:`. If it prints `Not yet:`, address the findings, commit, and check again. The check reads your commits and runs the tests; it does not see which forms you ran.

## Reflect

Would `git diff --exit-code -- tests/` catch this run's test change, and why? When would the change to `prompts/system.txt` go into a commit, and why?

[Worked answer](../answers/diff-views/) · [Start over](../../../README.md#start-an-exercise-again)
