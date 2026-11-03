# Answer: one failure, its cause and the change

Paths start at `extractor/`. The first run and `run/` hold the replies that `gpt-6-luna` gave through `model.py`, on the route through Codex, on 2026-11-03; `commands.sh` copies `run/` as the run of the changed prompt, so it calls no model.

| Part | Answer | Reason |
|---|---|---|
| The failure | `Note: 0147` and `Field: form` | All 20 values of `form` in the first score are wrong: each reply adds "Form" to the number, and each label gives the number only, as `docs/fields.md` asks. So any note shows the failure, and the field names the instruction to change (section 3.3). The one other wrong value, the amount of note 0105, comes from a note that names two amounts; both runs give it. |
| The cause | `Cause: 11, 17` | Lines 11 and 17 of `prompts/system.txt` are the two example replies. Both write `"form": "Form 1040"`, and no line says how to write `form`, so the model copies the examples: examples teach the shape of a reply (section 2.2). |
| The change | In both example replies of `prompts/system.txt`, `"form": "1040"` in place of `"form": "Form 1040"`. This puts back the course's prompt. | With "1040" in the examples, the model writes the form number only, as the labels do. Change the prompt, then score the whole set again (section 2.2). |
| The second score | `form` at 1.00/1.00, after 0.00/0.00 in the first run. The check prints both. | Run on the same notes, labels and scorer, the two scores compare (sections 2.2 and 3.3). |
| What stays | The notes, the labels, the scorer, the schema, the extractor and the first run. | A changed label or reply changes the score, not the prompt; the set is scored the same way every time (section 3.3). |

The check also accepts any of the 20 notes, with `form` in capitals or not; any cause that names line 11 or 17, such as `8 to 17`, or the word `missing`, since no line says how to write `form`; and any other change to the prompt, beyond spaces and line breaks, whose run has a reply for each note and gets more `form` values right than the first run. When a run with the changed examples still gets no `form` value right, the check asks for one more line below line 4, "Give form as the form number only."; with both changes, it asks the learner to show the run's `score.txt` to the trainer. Passing shows one run better on `form`, not a prompt right on every run: note 0137 names two tax years, so a run can give 2022 where the label says 2023, a difference that comes from the run, not from the change.
