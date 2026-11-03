# The run of 2026-11-03

On 2026-11-03, the course team did this exercise in a terminal, as its README says, on the route the course uses. `send_five.py` sent each note five times, with `prompt.txt` and no schema. `replies/` holds the ten replies, as `model.py` gave them. `record.md` is the record for these replies. The check accepts it.

- Route: `codex`, in `model-route.json`. `model.py` runs `codex exec`.
- Version of `codex`: 0.165.0-alpha.1.2.
- Model: `gpt-6-luna`, at the reasoning level `low`, both in `model-route.json`.
- Calls: 10, about 5 seconds each.
- Date: 2026-11-03.
- Place: a computer of the course team, not the workspace where you work.

In these replies, no `next_action` of note 0147 adds a date or a number, and every `amount_in_question` of note 0104 is null, so both rows are `none`. Other fields still differ between the five replies to one note: `tax_year` is a number in some and text in others, and `form` is `1040` in some and `Form 1040` in others.

To see this run in `lab`, run the reset first. Then, from `lab`, run `sh ../../answers/same-note-five-times/run-2026-11-03/commands.sh`. It calls no model. It puts the ten replies and this record in `lab`, and the check prints `Done:`.
