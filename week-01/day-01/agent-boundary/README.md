# Exercise: Probe the lab's agent boundary, then propose the regulated one

After this you can check that a coding agent's configuration does what it says, and propose, row by row, the tighter boundary for a repository that could reach return information, with the rule each row rests on and the role who decides it.

**Success criterion:** from `lab`, `python3 ../check.py` prints a line starting `Done:`: the first line of `docs/boundary-proposal.md` says it is a proposal and not an approval; every row names the rule it rests on, as a phrase quoted in double quotes or the words course proposal, and the role who decides; and the combination the proposal removes is written. Until then it prints `Not yet:` and what is left. The check tests that each is there and in that shape, not how good it is. Nothing is handed in; the class talks it through when the exercise ends.

**Where you work:** VS Code in your hosted workspace: the file `docs/boundary-proposal.md` in the repository `lab` in the folder `agent-boundary`, and the terminal (Terminal > New Terminal), inside `lab`. AI tools: Claude Code, the coding tool, started in the terminal for one step, to test what its configuration allows.

**Start from:** the folder `agent-boundary` in the practice kit: `python3 ~/practice/reset.py agent-boundary`, then `cd ~/practice/week-01/day-01/agent-boundary/lab`. The reset command builds the repository `lab` and prints `agent-boundary is back as it was supplied.` To get it again: the same reset command.

## Steps

1. In the terminal, inside `lab`, read the history and the configuration: `git log --oneline`, then `cat .claude/settings.json`. You should see: three commits by the course team, the configuration before the data-rules check; and in the configuration `"defaultMode": "acceptEdits"`, `Edit(/**)` and the test and Git reading commands under `allow`, and `WebFetch`, `WebSearch`, `curl` and `wget` under `deny`, which keep the agent off the web.
2. Test the configuration before you trust it: still inside `lab`, start the coding tool with `claude`; if it asks whether you trust the files in this folder, answer yes, which lets the folder's settings apply; if it asks you to sign in, stop and tell your trainer. Type `Run exactly this command and show me its first line: curl -sI https://example.com` and press Enter. You should see: Claude Code tries the command and reports that permission to use it "has been denied", and no page appears. If it asks to fetch the page some other way, choose the option that starts with No, or press Esc. If it shows the page's first line instead, which starts `HTTP`, the configuration did not keep the agent off the web: tell your trainer. Type `/exit` to leave.
3. Write the proposal: in the Explorer on the left, open `practice`, then `agent-boundary`, `lab` and `docs`, then `boundary-proposal.md`. Replace its first line, which says TODO, with a sentence that says it is a proposal and not an approval, in those words. In each row, write in Rule the rule it rests on, as a phrase from section 1.3 in double quotes, or the words course proposal where the chapter says no rule sets it, and in Who decides the role, in the chapter's words; last, on the file's last line, replace the TODO after `The combination this proposal removes, and why:` with that combination and why, in your words or the chapter's. Save it (File > Save), then run `python3 ../check.py`. You should see: a line starting `Done:`; until then, `Not yet:` and the rows still to fill.

**Answer:** your trainer has it, and shows it at the debrief.

## Afterwards, together

Which row needed a role you could not name? What did the probe show that reading the configuration did not?
