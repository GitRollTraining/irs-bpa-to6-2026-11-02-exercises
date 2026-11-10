# Exercise 1: the answer and its reasons

## The skill, `files/.agents/skills/map-codebase/SKILL.md`

| Part | Why | The line it rests on |
|---|---|---|
| A description that says when to use the skill and that it writes `CODEMAP.md` | Codex reads only the name and the description until it uses a skill, so the description decides when the skill runs. | "ChatGPT and Codex start with each skill’s name and description, then load the full SKILL.md instructions when they decide to use that skill." |
| Steps as orders, each with its input and output: the entry point, then the imports, then the map | A skill's steps are orders that Codex follows in sequence. Mapping starts at the entry point and follows the imports. | "Write imperative steps with explicit inputs and outputs." "So map a package from `__main__.py`, following its imports." |
| Five sections: Flow, Owners, Imports, Checks, Risky spots | These are the parts of a map, not of a summary. | "A **map** says which module owns what, how a request flows, where the code checks data, and where the risky spots are." |
| Imports as `a.py -> b.py` | The comparison with the graph (cell 4) and the check read this form. | none: a choice of this exercise |

## The two commits

- `files/CODEMAP.codex.md`: the kept run's map, committed as it is (cell 3).
- `files/CODEMAP.md`: the corrected map (cell 5). The change: two lines are deleted from `## Checks`, `payment_job/rules.py:23` (nothing owed returns 0.0) and `payment_job/rules.py:25` (the months capped). Both work out the penalty: they are the rule, not a check of data ("Validation is the code that checks data."). `rules.py:21` stays: it raises an error on a negative number of months, a check of the data it gets.

## The graph

`pydeps payment_job --max-bacon 0` finds 7 arrows between the package's modules. One is inside a function: `write_report` in `writer.py` imports `RATE` from `rules.py`. A map made from the first lines of each module misses it. The kept run's map had it, so cell 4 showed no difference.

`--max-bacon 0` gives the same 7 arrows as the default of 2 for this package. It stays in the command because the day teaches it ("So check a map with `--max-bacon 0`.").

## What else the check accepts

- Any wording of the skill that has a description and steps that name `CODEMAP.md`, with no `TODO` left.
- Any correction: the check needs two commits of `CODEMAP.md` that differ, imports that match the graph, and `settings.py` under `## Risky spots`. When every claim holds, a `## Checked` heading with the claims the learner opened makes the second commit differ.
- Module names as `payment_job.reader`, `payment_job/reader.py` or `reader.py`, and an arrow written `->` or `→`.

## Where the notebook's quoted lines come from

The notebook quotes these lines without naming where they come from, so it stands alone for a learner who missed the talk. All are in the Program repository's day file `days/day-02/curated.md`. The exercise is deck slide 15 ("Write a mapping skill and correct its map").

| Quoted line | Section and heading |
|---|---|
| "ChatGPT and Codex start with each skill’s name and description, then load the full SKILL.md instructions when they decide to use that skill." | 1, Package the mapping as a skill |
| "Write imperative steps with explicit inputs and outputs." | 1. Map a codebase before you change it, Package the mapping as a skill |
| "So map a package from `__main__.py`, following its imports." | 1, Find the entry point |
| "A **map** says which module owns what, ..." | The batch job you did not write, the list of moving parts |
| "pydeps finds imports by looking for import-opcodes in python bytecodes" | 1, Check the map against the import graph |
| "exclude nodes that are more than n hops away (default=2, 0 -> infinite)" | 1, Check the map against the import graph |
| "Validation is the code that checks data." | 1, Ask Codex for a map, not a summary |
| "A line there that opens a file runs the first time anything imports the module." | 1, Read the structure Python gives a codebase |
| "The graph shows only who imports whom, not the request flow or where the code checks data." | 1, Check the map against the import graph |
| "recalled 69% of IMPORTS edges" | 1, Check the map against the import graph |

