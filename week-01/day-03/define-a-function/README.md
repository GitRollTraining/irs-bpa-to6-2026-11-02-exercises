# 3.2 Define one function

Offer the model only a harmless function, describe it, and test it where a call is right and where none is.

A teammate wrote the functions that the model can ask for when a caseworker asks about a case note. Fix the list before anyone uses it.

## Start

Follow the [Day 3 setup](../README.md). `ask.py` calls the model; use no other AI tool. In a new terminal in the course folder, these commands create the workspace only if it is missing, then enter it:

```sh
test -d week-01/day-03/define-a-function/lab/.git || python3 reset.py define-a-function
cd week-01/day-03/define-a-function/lab
```

All paths below are relative to `lab/`. The model sees the function list in `functions.json`, not the code in `tools.py` that runs each call.

## Fix and send

Open the list:

```sh
code functions.json
```

Use section 3.2 of the notebook to explain each change. Copy each `\"` as it is: JSON needs a `\` before a quote inside a text.

| Problem | Change to make |
|---|---|
| `add_follow_up` writes an action into the case file; that call belongs to a person. | Remove its definition, from its `{` to its `},`. |
| The `description` of `lookup_form` is `TODO`. | In place of `TODO`: `Gives the title of a tax form, such as \"U.S. Individual Income Tax Return\" for 1040. Call it only when a question asks what a form is, and the note does not say it. It reads a table of titles. It writes nothing.` |
| The `description` of `form_number` is `TODO`. | In place of `TODO`: `The number of the form as the note writes it, without the word Form, such as \"5329\", \"1120-S\" or \"W-2\".` |

<details><summary>Why each change</summary>

| Problem | Why |
|---|---|
| `add_follow_up` writes an action into the case file; that call belongs to a person. | In `tools.py`, it writes the next action into the case file. IRS policy keeps such actions under a person's oversight. Section 3.2, the table of functions, row "Record an action on a case": "No: that call belongs to a person". |
| The `description` of `lookup_form` is `TODO`. | The model cannot see `tools.py`. So this text says what the function does, when to call it, and that it writes nothing. Notes 0106 and 0147 name a form. Only the question about 0106 asks what a form is. Section 3.2, list "Describe each function": "Could an intern use it from that alone?" |
| The `description` of `form_number` is `TODO`. | `tools.py` finds the title of `5329`, but nothing for `Form 5329`. So the description says what to send. Section 3.2, the same list: "Its purpose, and each parameter". |

</details>

Save `functions.json`, then send the two questions:

```sh
python3 ask.py
```

Expect a call to `lookup_form` with `{"form_number": "5329"}` for note 0106, and no call for note 0147. If it prints `Not sent:`, fix what it names and run it again. Then check:

```sh
python3 ../check.py
```

Finish when the check prints `Done:`. If it prints `Not yet:`, address the findings, run `python3 ask.py` again, and check again. The check reads your saved list and its two replies, so no commit is needed.

## Reflect

When could `add_follow_up` go back on the list, and why? If a teammate adds `read_note(note_id)`, which reads any note, who should choose `note_id`, and why? Which third question would you add to test the list, and why?

[Worked answer](../answers/define-a-function/) · [Start over](../../../README.md#start-an-exercise-again)
