# The data-rules check: ten uses proposed for the extractor's pilot

Everything in this file is made up for the course: the office, its people, its notes and its
approvals. Read it as if they were your own office's.

Your office is about to pilot the case-notes extractor on the real case notes of one office, the
pilot office. The pilot team is Dana, Kim, Lee and Pat, developers employed by the IRS, and Sam, a
developer on the staff of the contractor that supports the office's work under its IRS contract.
Before any AI tool touches the pilot's work, the team lead asks you to answer for the ten uses the
team has proposed.

## The approvals on file

An accountable agency official gave both. Nothing else is approved, and the contract file holds no
approval of AI tools.

- **The office's coding agent:** for code work by the office's developers and the contractor's
  staff, in the office's development environment, in repositories that hold no return information.
  Each session's log is kept with the system's audit trail.
- **The extractor's pilot:** the extractor, run by the pilot team on the pilot office's case notes,
  calling only the model endpoint its configuration names, one note per call. Every call is written
  to the system's audit trail, and a caseworker reads the fields before anything is done on a case.

## The ten uses

1. Dana runs the extractor on note 2231, a case note of the pilot office, to check the pilot's first
   morning. It sends that note alone to the model endpoint its configuration names.
2. Lee wants the coding agent to write a loader for the pilot's work list, a file that would sit in
   the extractor's repository: one line per case the pilot office works this month, each line a
   case number, a tax year and a form number, and nothing else.
3. Pat wants a better system prompt, and would paste the pilot office's desk guide for working these
   cases, an internal document that names no taxpayer, into a public chat tool, once the office's
   name and every case number in it are taken out.
4. Dana wants the coding agent to add a writer for the pilot's audit trail to the extractor, whose
   repository holds its code and its documentation and no return information.
5. Kim wants the coding agent to read 500 synthetic case notes while it improves how the extractor
   handles long notes. The data team made them by fitting a text generator to the pilot office's
   real notes of last year.
6. Lee wants a one-page summary of the IRS's policy on AI, Internal Revenue Manual 10.24.1, for the
   team, and would paste its text, as published on irs.gov, into a public chat tool.
7. Sam wants to start the coding agent in the extractor's repository, the one in use 4, to write the
   tests of the audit-trail writer.
8. Yesterday, to ask why the extractor failed on note 2231, Dana pasted the note's fields into the
   coding agent's chat. Lee wants to attach that session's log to the pull request as evidence, as
   the course does with the lab's.
9. Kim wants to ask the AI assistant built into the data team's analytics workspace, where the pilot
   office's notes are kept, which of the notes name no amount.
10. Pat wants the coding agent to build the pilot's weekly report from one table: for each form, the
    number of notes the extractor processed and the number that failed, across the whole office. No
    count is under 200, and the table holds no case number, name, note text or date.

## Your answers

In Permitted?, write Yes, No, or Not mine to decide. In Who decides, for Not mine to decide, write
the role whose decision it is, in the chapter's words; otherwise leave the dash. In Why, write the
rule and the fact of the use it turns on, ending with the section of the week 1 chapter the rule is
in, such as (section 1.3); for a Yes, also what it requires of the work.

| Use | Information | Tool | Permitted? | Who decides | Why |
|---|---|---|---|---|---|
| 1 | Note 2231, a case note of the pilot office | The pilot's model endpoint, through the extractor | Yes | - | Every use of AI must be approved by an accountable official, and the pilot's approval covers this one: its team, the pilot office's note, the endpoint its configuration names, one note per call. It requires the call written to the system's audit trail, and a caseworker reading the fields before anything is done on the case, never the fields as a decision (section 1.3, section 1.2) |
| 2 | The pilot's work list | The office's coding agent | Not mine to decide | The accountable agency official | A case number with its tax year and form, for cases the office is working, can be associated with a taxpayer and says whose return is being examined, which the statute counts as return information; the coding agent is approved only for repositories that hold none, so this is work it is not approved for, and approving a use is the accountable official's (section 1.1, section 1.2) |
| 3 | The pilot office's desk guide, its name and case numbers taken out | A public chat tool | No | - | Only approved tools may be used. The guide is still a non-public record of how the office works its cases, and public tools retain and reuse what is entered, which can disclose IRS internal strategies, plans or intentions; taking out names does not make it public (section 1.1, section 1.3) |
| 4 | The extractor's code and documentation | The office's coding agent, started by Dana | Yes | - | The coding agent is approved for this work, by the office's developers, in a repository that holds no return information. It requires the session log kept with the system's audit trail, and the agent's change read by a person and taken through the approved development life cycle before it is used (section 1.3) |
| 5 | 500 synthetic notes made from the pilot office's real notes | The office's coding agent | Not mine to decide | The privacy contact the IRS policy names | Made by fitting a generator to real notes, they may still be associated with a taxpayer, which is not a call a developer makes alone; questions about using data in generative AI, synthetic data included, go to the privacy contact (section 1.1, section 1.2) |
| 6 | The published text of Internal Revenue Manual 10.24.1 | A public chat tool | No | - | Only Treasury- or IRS-approved AI tools may be used for work, even on public text, and the policy warns that seemingly innocuous work matters carry risk in public tools: the question itself says what the team is working on (section 1.3, section 1.1) |
| 7 | The extractor's code and documentation | The office's coding agent, started by Sam | Not mine to decide | IRS Cybersecurity, consulted, and the Contracting Officer, who approves | Sam works for the contractor, and contractors must not employ AI technologies to support the IRS contract without consultation with IRS Cybersecurity and approval from the Contracting Officer; the contract file holds no such approval, and the accountable official's approval of the coding agent does not stand in for it (section 1.3) |
| 8 | The coding agent's session log from yesterday | Attached to the pull request | No | - | The log now holds note 2231's fields, which are return information, and a log that holds note text is treated as holding return information; the statute opens return information only to those whose duties require it, not to everyone who reads a pull request. The approval keeps session logs with the system's audit trail (section 1.2, section 1.3) |
| 9 | The pilot office's notes, in the analytics workspace | The workspace's built-in AI assistant | No | - | The assistant is not among the approved tools, and the policy prohibits putting taxpayer information into any otherwise-unauthorized AI system (section 1.1, section 1.3) |
| 10 | The pilot's weekly counts per form | The office's coding agent | Yes | - | Counts per form across the whole office, none under 200, with no case number, name, note text or date, cannot be associated with a particular taxpayer, so the statute does not count them as return information, and the repository stays within the coding agent's approval. It requires the session log kept with the system's audit trail (section 1.1, section 1.3) |

## Other answers the check accepts

Two careful readers can answer these five uses two ways from the chapter. The check accepts each
answer below as well as the one in the table, and the debrief compares them.

| Use | Permitted? | Who decides | Its reason |
|---|---|---|---|
| 2 | No | - | The approval on file keeps return information out of the coding agent's repositories, so the use is outside it (section 1.3) |
| 2 | Not mine to decide | The privacy contact | Whether a list of case numbers may go into a generative AI tool is a question about using data in one (section 1.2) |
| 5 | No | - | Accepted when Why gives the reason it rests on: the notes come from real notes and may still be associated with a taxpayer (section 1.1) |
| 7 | No | - | Accepted when Why or Who decides names the contractor rule's roles: no AI tool on the IRS contract without consultation with IRS Cybersecurity and approval from the Contracting Officer (section 1.3) |
| 9 | Not mine to decide | The accountable agency official | Approving a new use of an AI tool is the accountable official's (section 1.3) |
| 9 | Not mine to decide | The privacy contact | Whether the pilot office's notes may go into another generative AI tool is a question about using data in one (section 1.2) |
| 10 | Not mine to decide | The privacy contact | Deciding that data can no longer be associated with a taxpayer is not a call a developer makes alone (section 1.1, section 1.2) |
