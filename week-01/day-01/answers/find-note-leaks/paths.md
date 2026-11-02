# Answer: the three disclosure paths

All notes are fictional. The fixture represents a protected note in this scenario.

| Path | Why it matters | Fix |
|---|---|---|
| The failure log in `extractor.py` writes the whole note. | Ignoring `logs/` in Git does not remove the copy on disk. | Log only the note identifier. |
| The fallback sends notes to `inference.example.net`. | A retry can disclose data to an unapproved provider. | Retry through the approved `ask` route; remove the fallback. |
| `tests/fixtures/two_amounts.txt` represents a note with its name and TIN removed. | Remaining details can still identify someone. | Use simulated course note `notes/0122.txt`, which preserves the two-amount test case. |

Section 1.1 explains the rules. Replacing the fixture in a new commit leaves its previous contents in Git history; discuss the response required if protected data has already been pushed.
