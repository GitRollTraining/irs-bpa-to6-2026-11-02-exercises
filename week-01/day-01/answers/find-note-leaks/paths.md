# The paths in the agent's change

The agent's change lets the text of a note leave the extractor in three places. Each line gives one
place and the rule that it breaks.

- `extractor.py:75`: the log line for a failure writes the whole note to `logs/extractor.log`. A log line that prints the whole note is one of the two paths that an agent creates (section 1.1). The ignore rule for `logs/` keeps the file out of Git, but the file stays on the disk. So the ignore rule closes nothing.
- `extractor.py:25`, `extractor.py:59` to `extractor.py:63`, and `extractor.py:77`: the second provider. For each failed reply, the code sends the system prompt and the note to `inference.example.net`. This is a non-Treasury AI tool, and the policy does not let a note go to it (section 1.1). The retry can stay, but its destination cannot.
- `tests/fixtures/two_amounts.txt`: a note from a closed case, with its name and TIN removed. Without the name, the note still does not pass the test of the law (section 1.1). The test asks that no one can link the data to a particular taxpayer, directly or indirectly. A real note in a fixture is the other path that an agent creates (section 1.1). Course note 0122 has two amounts, so the edge case does not need a copied note.

The agent's commit still holds the copy, also after a later commit replaces the file. The debrief
discusses this.
