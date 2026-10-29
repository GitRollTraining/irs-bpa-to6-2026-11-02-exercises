# The extractor's five fields

The extractor returns one JSON object per note, with exactly these five fields and no other.

| Field | Type | Rule |
|---|---|---|
| `tax_year` | integer | the tax year the note names, such as `2023` |
| `form` | string | the form number only, such as `"1040"`, without the word "Form" |
| `issue` | string | what looked wrong, in a short phrase of the note's own words |
| `amount_in_question` | integer or null | the amount the note names as in question, in whole dollars with no comma; `null` when the note names no amount. Always present |
| `next_action` | string | what happens next, as the note says it |

For note 0147 (`notes/0147.txt`) the result is:

```json
{"tax_year": 2023, "form": "1040", "issue": "Schedule C gross receipts below information returns",
 "amount_in_question": 18400, "next_action": "Follow up on records request in 30 days"}
```

A note that names no amount has no amount, and the extractor must say so rather than supply one.
