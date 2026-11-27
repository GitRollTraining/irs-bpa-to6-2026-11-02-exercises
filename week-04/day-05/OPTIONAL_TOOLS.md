# Optional: use your existing Codex workflow

The default is [Databricks in your browser](START_HERE.md). This alternative is opt-in;
it uses the same task, fork and submission files. No changes to this folder's files are needed.
Your notebook implementation and outputs still originate in Databricks. This route does require
tooling in your course Workstation (Python 3.11+, Git, uv, Codex and Databricks CLI).
Clone your own public fork there and run the commands from its `week-04/day-05/` folder
(`cd week-04/day-05`); every path on this page is relative to that folder.
Use the workspace base URL from the Classroom environment card. Replace
`YOUR-WORKSPACE-HOST` below with that host (no account IDs or query string).

Tool choice and assessment settings are separate. The trainer decides whether Ownership and
Trait checkpoints are enabled in the assessment Engine; learners do not opt into or out of
assessment by choosing a tool. When the trainer assigns this route or enables conversation
assessment, follow [SESSION_RECORD.md](SESSION_RECORD.md) before work and preserve the genuine
conversation. Those checkpoints require attributable evidence: agent replies and tool activity
are context, not a replacement for your judgment. Never reconstruct a chat. For the browser-only
route without Codex, the trainer disables those checkpoints in the Engine.

## What the conversation shows

Ownership concerns how you direct and check this task's work. Trait checkpoints concern
broader working behaviours visible in that same conversation. Keep your actual observations
and reasons: what you checked, which result you compared it with, and why you chose the next
step. An agent's claim alone does not establish that you checked it. These explanations clarify
the existing assessment; they do not add another deliverable or change its criteria.

Here, **native** means authored and run in Databricks; **MCP** is the connection the tools use
to reach the platforms; a **receipt** is the tool's record of an operation; and **connection
smoke** or **round trip** means the ungraded practice that runs, submits and checks a result.
The **handoff** is SUBMISSION.md. See [the task's submission checklist](CHALLENGE.md#what-to-submit-and-how-it-is-checked)
for the required files.

## One-time connection setup

The following installs platform tooling, not a solution. Run from your fork's `week-04/day-05/`:

```sh
mkdir -p .tools
git clone https://github.com/databricks-solutions/ai-dev-kit.git .tools/ai-dev-kit
git -C .tools/ai-dev-kit checkout --detach 07f8e1ccf3dfc09a794eaf86fd15a5848f9d63d4
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python -r requirements.txt ./.tools/ai-dev-kit/databricks-tools-core ./.tools/ai-dev-kit/databricks-mcp-server
```

If `.tools/ai-dev-kit` already exists, check its revision rather than cloning over it. The wrapper
requires this exact revision and clean tracked server files. Tooling, environment and local
receipts are ignored by Git. Run the local checks with:

```sh
.venv/bin/python -m unittest discover -s . -v
```

Sign in to the course Databricks workspace with the named profile (the CLI opens the browser):

```sh
databricks auth login --host 'YOUR-WORKSPACE-BASE-URL' --profile TO6
```

Use your own learner account, not an operator account. Do not set token or host environment
variables to override this profile. Set your own fork's base URL in the following command:

```sh
.venv/bin/python databricks_platform.py init --repository https://github.com/YOUR-USERNAME/YOUR-FORK
```

If you already signed in to this course workspace under another profile, add `--profile YOUR-EXISTING-PROFILE`
to `init`. Use that existing authenticated profile; copying its host into a new profile does not
copy its OAuth login. Never copy tokens. Later commands automatically reuse the saved profile.

`init` reads your authenticated Databricks username and writes `.platform/config.json`. Read the
printed configuration before proceeding:

| Setting | Assigned value |
|---|---|
| Profile | `TO6` by default, or the existing signed-in profile you selected |
| Notebook | `/Users/<your Databricks username>/to6-challenge4/notebook` |
| Input schema | `training.to6_challenge4_inputs` |
| Input tables | `closed_returns` and `new_returns` in that schema |
| MLflow experiment | `/Users/<your Databricks username>/week-04-challenge`, as the notebook's setup cell names it |
| Output schema | `training.to6_c4_` followed by the first 12 hex characters of SHA-256 of your exact Databricks username; `init` calculates it |
| Submission | Your fork's URL, branch `main`, folder `week-04/day-05/` |

The administrator must already have created your output schema and granted input read access.
Do not change the derived schema/path to another learner's values. Unity Catalog grants and
workspace permissions enforce isolation; this tool is **not** a SQL or Python sandbox. Both SQL
and notebook code run with your actual Databricks permissions. Use fully qualified table names.

### Authorize your own GitHub connection

The managed GitHub MCP service is named `system.ai.github`. Its endpoint in this workspace is:

`https://YOUR-WORKSPACE-HOST/ai-gateway/mcp-services/system.ai.github`

1. Open [Authorize GitHub for Databricks](https://YOUR-WORKSPACE-HOST/mcp-service-login?name=system.ai.github)
   while signed in to your training Databricks account.
2. Complete the GitHub authorization using **your own GitHub account**, the owner of the
   fork you created in START_HERE.md. Permit the connection to access your public fork.
3. Return to the Workstation. Never paste authorization tokens into a prompt. This connection
   belongs to you; an operator's connected account cannot submit your work. Run:

```sh
.venv/bin/python databricks_platform.py check
```

The check verifies the connected GitHub user owns your fork, then reads your Databricks identity, both input table descriptions/columns, your output schema and
this folder's README on your fork's `main`. It does not write to external platforms. A successful check proves
these reads only. The walkthrough below tests compute/write/export; MLflow logging and
session-record transfer have their own checks.

## Ungraded native round trip

When the trainer assigns this route or enables conversation assessment, first complete [SESSION_RECORD.md](SESSION_RECORD.md), steps 1–2.
Use its Databricks-specific finish steps after every submission. Remote GitHub commits do not
trigger your Workstation's Git hooks. When capture is required by the trainer, keep the genuine Codex conversation, including tool context;
screenshots and reconstructed chat are not substitutes.

Start Codex in this repository. Give it the following platform operating contract:

> Use `.venv/bin/python databricks_platform.py execute` with JSON on stdin containing inline `code`.
> Author and update the notebook through that native operation, never a local solution file or
> `file_path`. Run only on Databricks. Read `.platform/config.json` for my exact paths/schema.
> Use `sql` for independent readback and `submit` for native exports. Ask before writes whose
> target I have not authorized. Never edit a downloaded/exported notebook locally.

For the connection smoke only, send this inline Python through `execute`, replacing
`YOUR_OUTPUT_SCHEMA` with the exact configuration value. No local `.py` file is created:

```python
import json
schema = "YOUR_OUTPUT_SCHEMA"
practice = schema + ".connection_smoke"
spark.createDataFrame([(1, "connected")], ["check_id", "message"]).write.mode("overwrite").saveAsTable(practice)
rows = [r.asDict() for r in spark.table(practice).collect()]
assert rows == [{"check_id": 1, "message": "connected"}]
dbutils.notebook.exit(json.dumps({"files": {
    "SUBMISSION.md": "Ungraded connection smoke. Native output: " + practice + "\n",
    "outputs/connection-smoke.json": json.dumps(rows)
}}))
```

The operation accepts exactly `{"code":"...inline notebook source..."}` on stdin. Codex can
serialize that JSON and pass it directly without writing a solution file. Open the returned
run URL and your native notebook in the Databricks browser. Confirm the run succeeded.

Independently read the saved practice table with `sql`, passing JSON on stdin:

```json
{"query":"SELECT * FROM YOUR_OUTPUT_SCHEMA.connection_smoke"}
```

Replace `YOUR_OUTPUT_SCHEMA` first. Also open the two supplied inputs and their column
descriptions in Catalog Explorer, and open your MLflow experiment from the **Experiments** page.
The administrator owns missing permissions or metadata.

Now run:

```sh
.venv/bin/python databricks_platform.py submit
.venv/bin/python databricks_platform.py read notebook.py
.venv/bin/python databricks_platform.py read SUBMISSION.md
```

`submit` obtains the native source and the successful run's notebook output. It creates a GitHub
commit on your fork's `main`, writing the files into `week-04/day-05/`, then reads every submitted file at that exact commit and checks its
bytes or Git blob hash. Open that commit in GitHub. A `verified: false` receipt means a commit
may already exist but its readback failed: inspect it before retrying. When capture is required by the trainer, complete SESSION_RECORD.md steps 3–5 and confirm the remote checkpoint too. Only then begin
the actual task.

## Work and submission contract

Use the same native notebook for your own implementation. Log your MLflow runs from that native
notebook and read them back there to write `outputs/runs.csv`. The wrapper retains run IDs
in ignored local receipts; include the required evidence in the native handoff/output files so
reviewers receive it. A successful run must end with `dbutils.notebook.exit` containing JSON of
this shape, constructed **in Databricks**:

```json
{"files":{"SUBMISSION.md":"Your handoff text","outputs/your-output.json":"Your small synthetic output export"}}
```

The wrapper permits only `SUBMISSION.md` and paths under `outputs/`. It adds `notebook.py` from the
native SOURCE export and `outputs/native-run.json` with the execution reference. Do not supply
a notebook file or reserved run receipt yourself. Large/truncated notebook output is rejected;
keep these synthetic exports small. Failed latest execution, changed native source, unsuccessful
run status or mismatched GitHub readback cannot produce a verified submission receipt.

`sql` accepts a query and returns the actual managed SQL result. If it returns a pending
`statement_id`, call `.venv/bin/python databricks_platform.py sql --statement-id ID` to read its
status; repeat while pending, without resubmitting the original query. It is not an access-control
filter. Use it for inspecting your inputs and saved outputs; never modify the shared inputs.
The approved output boundary is your derived schema, enforced by platform grants.

The task defines the actual deliverables and quality requirements. Record your final run references,
source/output identifiers and limitations in the native handoff. After `submit`, identify its
commit in the Classroom submission alongside your fork's **base** URL. Do not edit the
handoff locally merely to add its own commit hash (a file cannot name its containing future hash).
When the trainer assigns this route or enables conversation assessment, follow SESSION_RECORD.md to preserve your genuine Codex session. This starter does
not promise that automated grading is ready.

The practice table and `outputs/connection-smoke.json` may remain as ungraded connection evidence.
Submission updates the files named by the successful native run; it does not erase older exports.
List the files belonging to your final task delivery in SUBMISSION.md so a reviewer can
distinguish them from practice runs and older exports.
