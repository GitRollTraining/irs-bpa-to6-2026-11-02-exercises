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
| 1 | Note 2231, a case note of the pilot office | The pilot's model endpoint, through the extractor |  | - |  |
| 2 | The pilot's work list | The office's coding agent |  | - |  |
| 3 | The pilot office's desk guide, its name and case numbers taken out | A public chat tool |  | - |  |
| 4 | The extractor's code and documentation | The office's coding agent, started by Dana |  | - |  |
| 5 | 500 synthetic notes made from the pilot office's real notes | The office's coding agent |  | - |  |
| 6 | The published text of Internal Revenue Manual 10.24.1 | A public chat tool |  | - |  |
| 7 | The extractor's code and documentation | The office's coding agent, started by Sam |  | - |  |
| 8 | The coding agent's session log from yesterday | Attached to the pull request |  | - |  |
| 9 | The pilot office's notes, in the analytics workspace | The workspace's built-in AI assistant |  | - |  |
| 10 | The pilot's weekly counts per form | The office's coding agent |  | - |  |
