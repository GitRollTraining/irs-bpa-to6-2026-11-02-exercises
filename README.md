# Practice environment: Full Stack Data and AI

- **Program:** `irs-bpa-to6`
- **Written from:** `programs/irs-bpa-to6/design/local-setup.md` and the provisional activity
  forms in `programs/irs-bpa-to6/profile.md` § 5a (curriculum repository), as of 2026-10-20. The
  forms are "signed by nobody" (the profile's own words); week 1's labs are a live build, "walked
  through", so every exercise here starts from a state the kit supplies, never from the lab.

## The case every exercise shares

The case-notes extractor, the week's lab repository: a small Python function that reads one
simulated case note and returns its fields as JSON that a later program can rely on. It returns
exactly five fields, each with its rule in `~/practice/lab-states/base/docs/fields.md`:

| Field | What it holds |
|---|---|
| `tax_year` | the tax year the note names, such as `2023` |
| `form` | the form number only, such as `"1040"` |
| `issue` | what looked wrong, in a short phrase of the note's own words |
| `amount_in_question` | the amount the note names as in question, in whole dollars; `null` when the note names none |
| `next_action` | what happens next, as the note says it |

Each exercise starts from its own copy of the extractor, at the point in the week it needs, so
an exercise never depends on how your own lab went.

## Where you work

- **VS Code, connected to your workspace in our hosted environment:** open the hosted environment's
  connection page in your browser and sign in with the account issued to you. VS Code opens in the
  browser, already connected to your workspace.
- **The terminal:** in VS Code, menu Terminal > New Terminal. Every command in an exercise is typed
  here.
- **The model the extractor calls:** reached only through the practice kit's `model.py`, which sends
  one note with a system prompt and prints the model's reply:
  `python3 ~/practice/model.py SYSTEM_PROMPT_FILE NOTE_FILE`. The workspace provides the model and
  its key; you need no account of your own.
- **The coding agents:** both Codex and Claude Code, two of the course's approved coding tools,
  each started from the terminal inside the folder an exercise names: Codex by typing `codex`, and
  Claude Code by typing `claude`. An exercise that uses one names it and what you type into it; every other exercise uses
  no AI tool. The first time you start one in a folder, it may ask whether you trust the files in
  that folder: answer yes, which lets the folder's own settings for the agent apply, where it has
  any.

## Set up once, before the first exercise

1. Open the connection page and sign in. You should see: VS Code, with a folder named `practice` in
   the Explorer on the left.
2. Open a terminal (Terminal > New Terminal) and type `cd ~/practice`. You should see: the prompt
   now ends in `practice`.
3. Tell Git your name and email, which it writes into every commit you make:
   `git config --global user.name "Your Name"`, then
   `git config --global user.email "you@example.com"`, with your own name and your work email
   address. Git only writes them into your commits; nothing is sent to that address. You should
   see: nothing; Git prints no reply when it saves a setting.
4. Check: type `python3 check_setup.py`. It asks the model one short question, so it takes a few
   seconds. It shows `Setup OK` and the versions of Python, pytest, jsonschema and Git, and the
   model's one-word answer. If it shows `Missing:` and a name, tell your trainer before the first
   exercise.

## The practice kit

The `practice` folder is the practice kit, placed in your workspace before day 1. Every note,
description and reply in it is made up; none is about a real person, business or return.

- **One folder per exercise,** with that exercise's starting files: the table below, by day.
- **`notes/`:** the 41 simulated case notes the week's exercises share, one per file: `0101.txt` to
  `0140.txt`, and `0147.txt`, the note the chapter uses as its example. "Synthetic filer" stands
  where a name would be.
- **`model.py` and `model-route.json`:** the route to the model the extractor calls. Do not edit
  them; the course team sets the route.
- **`answers/`, in each day's folder:** each exercise's answer, in a folder named like the exercise's.
- **`lab-states/`:** the week's lab repository's files at each of its saved states, which an
  exercise's reset uses to build its starting repository. You change nothing in it; an exercise
  names a file in it when you need one, such as the extractor's output schema.

| Day | Starting state | For | How you open it |
|---|---|---|---|
| 1 | `week-01/day-01/find-note-leaks/` | Find and close the three places a note leaks from the extractor | `cd ~/practice/week-01/day-01/find-note-leaks` |
| 1 | `week-01/day-01/data-rules-check/` | Write the extractor's data requirements, then pass the data-rules check | `python3 ~/practice/reset.py data-rules-check`, then `cd ~/practice/week-01/day-01/data-rules-check/lab` |
| 1 | `week-01/day-01/agent-boundary/` | Probe the lab's agent boundary, then propose the regulated one | `python3 ~/practice/reset.py agent-boundary`, then `cd ~/practice/week-01/day-01/agent-boundary/lab` |

A folder whose starting state is a Git repository of its own is built by the reset command the
first time, so its exercise starts with that command.

Answers: `~/practice/week-NN/day-NN/answers/<folder>/` holds each exercise's answer, which passes the exercise's
done check. Exercises are not graded, so you may open it; try the exercise first.

## Start again

`python3 ~/practice/reset.py <folder>`, such as `python3 ~/practice/reset.py validate-replies`,
puts that exercise's folder back as it was supplied, and builds its Git repository again where it
has one. It replaces your changes in that folder; it does not repair them, and it touches no other
folder, the answers included. A terminal open inside the folder keeps working.

## Not known yet

| Question | Who answers | Our proposed answer, and the page it came from |
|---|---|---|
| The connection page's address | the hosting team, at kickoff | issued at kickoff (`programs/irs-bpa-to6/design/local-setup.md`, Web browser: "address issued at kickoff") |
| Which of the three routes into the workspace IRS security approves | IRS security, through the hosting team | VS Code in the browser, which "needs only the hosted environment's HTTPS address" (`programs/irs-bpa-to6/design/local-setup.md`, VS Code) |
| Whether the hosting team places the practice kit at `~/practice` in each workspace | the hosting team | yes, cloned into each workspace before day 1 |
| Python 3.10 or later, pytest, jsonschema and Git 2.28 or later installed in the workspace image | the hosting team | yes; `check_setup.py` names any that is missing |
| The route `model.py` takes to the model the extractor calls in the workspace: its address, its key, and which model | the hosting team | the model access the workspace provides ("the model access the labs use", `programs/irs-bpa-to6/design/local-setup.md`), set once in `model-route.json`; the kit was run with Claude Code's print mode and a small Claude model behind the same file |
| Whether the workspace installs both coding agents, and where each keeps its settings file | the hosting team, with the trainers | yes: both Codex and Claude Code, as the program owner ruled on 2026-10-20 ("Any coding agents is fine. (both Codex and Claude Code)"); `programs/irs-bpa-to6/design/local-setup.md` names Codex ("In the hosted environment Codex runs on an API key we configure"). Five exercises use Claude Code and the exercise that maps a tool's modes uses Codex; each names, for its trainer, the steps that differ in the other tool |
| Whether each coding agent starts already signed in, so that a learner never sees a sign-in | the hosting team | yes, on a key the course team configures, as the page says of Codex: "In the hosted environment Codex runs on an API key we configure" (`programs/irs-bpa-to6/design/local-setup.md`) |
| How a learner reaches the trainer when a step says "tell your trainer" | the trainers | in the session itself, in the room or in its chat, while the exercise runs |
| Where a learner opens the week's chapter, which each exercise names by section as the talk it follows | the trainers, with the team that builds the Program's learning materials | the chapter's material on the course's Google Classroom page, which links its NotebookLM notebook (`sops/material/classroom-delivery.md`, curriculum repository) |
