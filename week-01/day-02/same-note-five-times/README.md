# 2.1 Send each note five times

Send two notes to the model five times each, and record which replies give a value that the note does not state.

The extractor sends each note to its model once and keeps the reply. One reply cannot show how much the replies to the same note vary.

## Start

Follow the [Day 2 setup](../README.md). `send_five.py` calls the model; use no other AI tool. In a new terminal in the course folder, these commands create the workspace only if it is missing, then enter it:

```sh
test -d week-01/day-02/same-note-five-times/lab/.git || python3 reset.py same-note-five-times
cd week-01/day-02/same-note-five-times/lab
```

All paths below are relative to `lab/`. `prompt.txt` is the system prompt that goes with each note, and `record.md` holds the two rows you fill in.

## Send and record

```sh
python3 send_five.py 0147 0104
```

Expect `Note 0104: reply 1 2 3 4 5 saved.` The script saves the replies in `replies/` and writes `field-by-field.txt`, which shows each note beside the five values of each field. A second run sends nothing.

Open `field-by-field.txt` and `record.md`. For each row of `record.md`, find its note and field in `field-by-field.txt`. In the row, write the numbers of the replies that the table names, such as `2, 4`, or `none` if no reply fits. Use section 2.1 of the notebook to explain each answer.

| Row of `record.md` | What to write |
|---|---|
| 0147, `next_action`: the note says "Follow up in 30 days" and gives no date. | The numbers of the replies whose value has a date, or another number that the note does not have. |
| 0104, `amount_in_question`: the note says "No amount yet", so null is the right value. | The numbers of the replies whose value is not null. A value in quotes, such as `"None stated"`, is text, not null. |

<details><summary>Why each answer</summary>

| Row of `record.md` | Why |
|---|---|
| 0147, `next_action`: the note says "Follow up in 30 days" and gives no date. | Note 0147 says only "Follow up in 30 days". It gives no date. So a reply with a date adds a fact that is not in the note: the model wrote a likely date. Section 2.1, under "A fluent answer is not a known answer.": "It writes the likeliest text, not a lookup." |
| 0104, `amount_in_question`: the note says "No amount yet", so null is the right value. | Note 0104 says "No amount yet", so the right value is null. A reply with text, such as `"None stated"`, puts words in a field that must stay empty. Section 2.1, under the same heading: "text where null belongs" |

</details>

Save `record.md`, then check:

```sh
python3 ../check.py
```

Finish when the check prints `Done:`. If it prints `Not yet:`, address the findings and check again. The check reads your own replies, so your numbers can differ from another learner's.

## Reflect

Why does note 0147 get its amount back, while note 0104 can get text in place of null? Why did some fields change across the five replies to one note? What if you had sent note 0104 only once?

[Worked answer](../answers/same-note-five-times/) · [Start over](../../../README.md#start-an-exercise-again)
