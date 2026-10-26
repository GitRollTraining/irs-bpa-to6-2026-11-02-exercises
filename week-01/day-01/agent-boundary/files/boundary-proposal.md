TODO: replace this line with one line saying what this document is, and what it is not.

# The case-notes extractor's coding agent, in a repository that could reach real notes

The lab default is what this repository's `.claude/settings.json` and the course's hosted
environment give the agent today. The regulated column is the course's proposal from the week 1
chapter, section 1.3. For each row, write in Rule the rule it rests on, as a phrase quoted from
section 1.3 in double quotes, or the words course proposal where the chapter says no rule sets it;
and in Who decides, the role that says yes or no to it.

| Setting | Lab default | Regulated repository | Rule | Who decides |
|---|---|---|---|---|
| Which tool | Any of the approved coding tools | Only a tool approved for that system and that work, with the approval recorded | TODO | TODO |
| Where it runs | The lab sandbox | An isolated environment with no route to production data the task does not need | TODO | TODO |
| Network | Package installs from the lockfile | None beyond what the task needs, and never alongside reachable protected data | TODO | TODO |
| What it may change | Files in the lab repository | A branch. It opens a pull request; it never merges | TODO | TODO |
| Approvals | Every command that is not a read, a test run or an edit in the repository | Every command that is not a read or a test run | TODO | TODO |
| Record | The session log, kept as evidence | The session log, plus the audit trail the system itself must keep | TODO | TODO |

The combination this proposal removes, and why: TODO
