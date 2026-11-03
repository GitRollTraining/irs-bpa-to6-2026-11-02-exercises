# 4.4 Map the modes of Codex

Say which kind of tool each mode of Codex is, and check that Codex made only the change you asked for.

Before the lab's runs, you map the four modes of Codex in `modes.md`. You give Codex one small request in two of the modes, then read its change in Git.

## Start

Follow the [Day 4 setup](../README.md). This exercise starts Codex in a terminal; use no other AI tool. In a new terminal in the course folder, these commands create the workspace only if it is missing, then enter it:

```sh
test -d week-01/day-04/tool-modes/extractor/.git || python3 reset.py tool-modes
cd week-01/day-04/tool-modes/extractor
```

All paths below are relative to `extractor/`. List the files, and open `modes.md` to read what each mode lets Codex do:

```sh
ls -a
code modes.md
```

Expect `.claude`, Claude Code's settings, and no `.codex`: no file here holds settings or instructions for Codex.

## Try two modes and record

Start Codex in this folder. If it does not start, or asks you to sign in, tell your trainer.

```sh
codex
```

1. When Codex asks if you trust this folder, answer yes.
2. Type `/permissions` and select Read Only. Give this request: `Add this line at the end of README.md: The data-rules check passed before any AI tool ran here.` Note what Codex reads and runs without your yes. If it asks, answer no: a yes adds the line, and the next run adds it again.
3. Type `/permissions` and select Ask for approval. Give the same request. If Codex asks, select `Yes, proceed`.
4. Type `/exit`. Do not commit.

Show what Codex changed:

```sh
git status --short
git diff HEAD
```

Expect `M README.md` and the request's line after `+`. `git diff HEAD` shows the change whether Codex staged it or not.

Fill in `modes.md` by hand. Use section 4.4 of the notebook to explain each answer.

| In `modes.md` | What to write |
|---|---|
| Kind, in each row. Each row says that Codex reads files and runs commands without your yes, in Read Only too. Only an agent does that. | `agent` |
| `Answer:`. The done-when allows only the request's line, at the end of `README.md`. Blank lines do not count. | `yes` if Git shows only that change, else `no`. |

<details><summary>Why each answer</summary>

| In `modes.md` | Why |
|---|---|
| Kind, in each row. Each row says that Codex reads files and runs commands without your yes, in Read Only too. Only an agent does that. | In `modes.md`, each row says that Codex uses tools without your yes: it reads files and runs commands, in Read Only too. Only an agent does that: chat reaches only what you paste into it. Section 4.4, under "Three kinds of tool, and they need different checks.": "Coding agents: conversational AI models with tools". |
| `Answer:`. The done-when allows only the request's line, at the end of `README.md`. Blank lines do not count. | The done-when in `modes.md` allows only that change. Section 4.4, under the same heading: "then its result against the done-when". |

</details>

Save the file, then check:

```sh
python3 ../check.py
```

Finish when the check prints `Done:`. If it prints `Not yet:`, address the findings and check again. The check reads `modes.md` and what Git shows; it does not ask who made the change.

## Reflect

Why does your answer rest on Git, not on Codex's report? Which mode will you use for the lab's runs, and why? Which of your files must no agent read, even in Read Only, and why?

[Worked answer](../answers/tool-modes/) · [Start over](../../../README.md#start-an-exercise-again)
