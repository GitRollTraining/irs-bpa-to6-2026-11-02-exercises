# Exercise 3: Codex checks your three sets, and you approve each command

**Goal:** After this exercise, you can judge each Databricks command Codex proposes before it runs, and check its answer in Catalog Explorer.

**Scenario:** On Wednesday you split your returns into `train`, `valid` and `test`. Before a model trains on them, you check two things. Does each set hold the label `exam_changed_tax`, the answer the model learns? Is the column `tax_added_by_exam` gone? Codex asks the workspace for you through the Databricks CLI. You approve or decline each command it proposes.

**AI tool:** Codex, in the Workstation's terminal, with the settings it starts with when you type only `codex`. It asks you before it runs a `databricks` command.

**Where you work:** the Workstation's terminal, in this folder: `week-03/day-04/exercise-03-codex-checks-the-sets/` in your course folder. You start Codex there. You write in `notes.md`: open it from the Explorer panel on the left. Type each answer on one line, after its colon. You read columns in Catalog Explorer, as on Monday.

**Done when:** `python3 check.py`, in this folder, prints `Done:`.

**Optional part, after step 6:** ask Codex to save Wednesday's notebook as a job from `../exercise-02-run-wednesday-as-a-job/job.json` (`databricks jobs create`), then to run it (`databricks jobs run-now`). These commands change the workspace. Judge each one before you approve it.

**What you have:**

- Your profile `course`, and your schema `course.learner_NN` with Wednesday's tables. `NN` is your learner number.
- Codex on your Workstation, as in weeks 1 and 2.
- `notes.md` and `check.py`, in this folder.
- A transcript the course wrote, `week-03/setup/day-04-codex-transcript.md` in your course folder: six commands Codex proposed in one run. Step 3 says when you use it.

**Start from:** the trainer just asked Codex the same kind of question about Monday's table, and declined one command. Open a terminal in your course folder, then go into this folder:

Terminal:

```text
cd week-03/day-04/exercise-03-codex-checks-the-sets
```

To start again, delete what you typed after each colon.

### Step 1. Explain first

Why: you judge Codex's answer better when you know the answer you need. `tax_added_by_exam` is the tax an examination added. A model picks returns before any examination. On Wednesday you marked it no in your known-on-selection-day record, and the split dropped it.

After `why_absent:`, write one sentence: why must `tax_added_by_exam` be absent from `train`, `valid` and `test`?

### Step 2. Start Codex and give it the task

Why: when you name the profile, the schema and the question, you can tell whether each command is the one you asked for.

Terminal:

```text
codex
```

If Codex asks whether to trust this folder, answer yes: the course gave you this folder. Then type your request. It must say four things:

- Use the Databricks CLI with the profile `course`.
- The schema is your `course.learner_NN`.
- The two questions of the scenario, with the table names `features`, `train`, `valid` and `test`.
- Use only commands that read.

Write your schema after `schema:`. Copy your request after `request:`.

<details><summary>Stuck? One way to say it</summary>

Codex:

```text
Use the Databricks CLI with the profile course. In my schema course.learner_NN, check two things: does each of train, valid and test have the column exam_changed_tax, and is the column tax_added_by_exam absent from features, train, valid and test? Use only commands that read. Show me each command before you run it.
```

</details>

### Step 3. Judge each command before it runs

Why: a `databricks` command goes to the workspace across the network, so Codex stops and shows it to you first. That is your one moment to refuse a wrong command. Ask the four questions:

| Question | Look at | Decline when |
|---|---|---|
| Is it the profile you meant? | `-p` or `--profile` | it has no profile: the CLI then picks one for you |
| Does it read or change something? | the command: `list` and `get` read, and `create`, `delete`, `update` and `cancel-run` (stop a run) change | it changes something: you asked only to read |
| Is the target the one you named? | the schema, table or job id in the command | you did not name it |
| Does it carry an option that turns off a safeguard? | the options, such as `--force`, which makes a command skip the checks it makes first | it carries one |

Approve a command only when all four answers are good. Otherwise decline it. In the choices Codex shows, take the one that does not run the command, and type why. For each `databricks` command, fill one block in `notes.md`:

1. After `cmd_1:`, copy the whole command.
2. After `reads_or_changes_1:`, write `reads` or `changes`.
3. After `profile_1:` and `target_1:`, write `yes` when the answer is good.
4. After `safeguard_removed_1:`, write `yes` when the command carries such an option.
5. After `decision_1:`, write `approve` or `decline`. After `reason_1:`, write why.

Number the next blocks 2, 3 and on. Codex may run other commands in this folder without asking, such as `ls`. They need no block.

If Codex runs a `databricks` command without asking, stop it with Ctrl+C. Then tell the trainer. Use the transcript when your run proposes no `databricks` command, or Codex does not start. Judge its six commands the same way, in six blocks. Write `transcript` after `source:`, and `course.learner_07` after `schema:`.

### Step 4. Write Codex's answer

Copy Codex's last answer after `codex_answer:`. In step 5 you check each part of it.

### Step 5. Read the columns yourself in Catalog Explorer

Why: Codex's answer rests only on the commands that ran.

In the workspace's left bar, select **Catalog**. Open `course`, then your own schema (also when you judged the transcript). Open each of `features`, `train`, `valid` and `test`, then the **Columns** tab. Write `yes` when the table has the column, and `no` when it does not:

- `label_train:`, `label_valid:`, `label_test:` for `exam_changed_tax`
- `tax_added_features:`, `tax_added_train:`, `tax_added_valid:`, `tax_added_test:` for `tax_added_by_exam`

After `agree:`, write `yes` when each part of Codex's answer matches your lines, and `no` when one does not. After `compared:`, write one sentence: which part differs, or which approved commands the answer rests on.

### Step 6. Check

Leave Codex, or open a second terminal in this folder.

Terminal:

```text
python3 check.py
```

It prints `Done:` when no line is empty and each decision follows your four answers. Otherwise it prints `Not yet:` and each thing still to do.

### Afterwards, together

1. Codex's answer can sound sure about a table it never read. Which of your approved commands does each part of its answer rest on?
2. A command without `-p` still works on some Workstations. Why would you still decline it?
3. You declined a command that only read a table, and approved one that read another. What made the difference?

The answer, after you try: [`answers/exercise-03-codex-checks-the-sets`](../answers/exercise-03-codex-checks-the-sets/).
