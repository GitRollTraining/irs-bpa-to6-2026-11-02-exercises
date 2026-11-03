# Answer: the replies that state what the note does not

This answer is for the ten replies in `replies/`, which the model gave on 2026-10-20 in the run that section 2.1 names. The "all ten" replies to note 0104 that section 2.1 counts are the five here and five from a second run that day, which was not kept. `commands.sh` puts these replies and `record.md` in `lab/`, and the check prints `Done:`.

| Row | Answer | Reason |
|---|---|---|
| 0147, `next_action` | 2, 5 | Replies 2 and 5 add a date, 2026-11-19, but the note says only "Follow up in 30 days". The model writes the likeliest text, not a fact it looked up (section 2.1). |
| 0104, `amount_in_question` | 1, 2, 3, 4, 5 | Each reply gives text, such as "None stated", but the note names no amount, so only null is right. A reply stays fluent where the note is silent (section 2.1). |

The check judges each row on your own replies. In `next_action` of note 0147, a value with a date or a number that the note does not have must be in the row, and one made only of the note's words and numbers, in its order, must not; any other value may be either, so 1, 3 and 4 may also be in that row here. In `amount_in_question` of note 0104, every value that is not null must be in the row, and null must not. A reply with no JSON, or without the field, may be either. `run-2026-10-30/` holds a later run with other replies and the record the check accepts for them. Passing shows that your rows match your replies; it does not show that the other fields are right.
