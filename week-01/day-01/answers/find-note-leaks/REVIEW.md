# Review of agent-draft, "Make the extractor robust to bad model replies"

Read the change as if `notes/` held real notes. List every place it lets a case note's text, or a
value taken from a note, leave the extractor other than in the one call to the model that
`model.py` reaches. One line each, starting `- `: the file and line, where the text goes, and the
rule in the week 1 chapter it breaks.

- `extractor.py:92`, the failure's log line, writes the model's whole reply, which holds the note's fields, to `logs/extractor.log`: logs that hold note text are "treated as holding return information", and the requirement is that it "logs the note identifier and never the note text" (section 1.2). Ignoring `logs/` keeps the file out of Git, not off the disk.
- `extractor.py:55`, through the same log line: the failure's message is built from the validator's messages, which repeat the value they reject (`'18,400' is not of type 'integer', 'null'`). An amount tied to note 0147 is return information, which covers "the amounts on a return" (section 1.2). Taking the reply out of the log line does not close this one.
- `extractor.py:26` and `extractor.py:76`, the second provider: on any failed reply, the system prompt and the note go to `inference.example.net`, which is "anywhere other than the model the extractor is approved to call" (section 1.1). The retry is fine; where it goes is not.
- `extractor.py:61` to `extractor.py:73`, the context notes: every call sends up to three other notes with the one being read. They go to the approved model and are still more than the extraction needs: "minimize the collection, use, retention, and disclosure of data in AI to what is specifically relevant and necessary" (section 1.1). `tests/test_extractor.py:42` was loosened from `startswith` to `in` so that the context passes it.
- `tests/fixtures/two_amounts.txt`: a note from a closed case with its name and TIN taken out, so "any fixture not written for the course" (section 1.1); without a name it has still not passed the law's test, "cannot be associated with, or otherwise identify, directly or indirectly, a particular taxpayer" (section 1.1). Course note 0122 names two amounts, so the edge case needs no copied note.
