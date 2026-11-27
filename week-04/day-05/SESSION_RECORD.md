# Save the Codex work that produced your Databricks submission

Follow this procedure when the trainer assigns the Codex route or enables conversation
assessment. The trainer controls Ownership and Trait settings in the assessment Engine;
choosing a tool does not let a learner opt into or out of assessment. For the browser-only
route without Codex, the trainer disables those checkpoints. Use this procedure instead of
the standing guide's local-code commit step.
Your notebook and handoff are authored in Databricks. The Workstation only records the genuine
Codex conversation and pulls unchanged platform exports. Use the public fork created in START_HERE.md. Never commit credentials or unrelated personal conversations.

For this optional route, complete steps 1–2 before starting work and steps 3–5 after each
practice or final submission. Step 6 is only for the completed task. Entire is the recorder
that preserves your original conversation; its checkpoint is a saved record, not a task score.

## 1. Install the tested recorder in your Workstation

This course walkthrough uses Entire **0.13.4**. Version 0.8.1 could not read the current Codex
session format in our check. Run these commands in a Workstation terminal (Linux) in your
fork's `week-04/day-05/` folder, where every command on this page runs; they install the official release in the ignored tools directory:

```sh
mkdir -p .tools/entire
case "$(uname -m)" in
  x86_64) ENTIRE_ARCH=amd64 ;;
  aarch64|arm64) ENTIRE_ARCH=arm64 ;;
  *) echo 'Ask the facilitator for the build for this machine'; exit 1 ;;
esac
curl -fL "https://github.com/entireio/cli/releases/download/v0.13.4/entire_linux_${ENTIRE_ARCH}.tar.gz" -o .tools/entire/release.tar.gz
curl -fL https://github.com/entireio/cli/releases/download/v0.13.4/checksums.txt -o .tools/entire/checksums.txt
python3 - "$ENTIRE_ARCH" <<'PY'
import hashlib, pathlib, sys
p = pathlib.Path('.tools/entire')
name = f'entire_linux_{sys.argv[1]}.tar.gz'
expected = next(line.split()[0] for line in (p/'checksums.txt').read_text().splitlines() if line.split()[-1] == name)
assert hashlib.sha256((p/'release.tar.gz').read_bytes()).hexdigest() == expected, 'Download checksum mismatch'
PY
tar -xzf .tools/entire/release.tar.gz -C .tools/entire
.tools/entire/entire version
```

Continue only if the checksum passed and the version is 0.13.4. A download or version error is
an environment issue; send the facilitator the failing command, without tokens.

## 2. Enable recording before starting Codex

```sh
.tools/entire/entire enable --agent codex --local --checkpoint-backend branch --absolute-git-hook-path --telemetry=false
python3 - <<'PY'
import json, pathlib
p = pathlib.Path('.entire/settings.local.json')
settings = json.loads(p.read_text())
settings['redaction'] = {'pii': {'enabled': True, 'email': True, 'phone': True}}
p.write_text(json.dumps(settings, indent=2) + '\n')
PY
.tools/entire/entire status
```

The recorder must be enabled. Do not commit `.entire/settings.local.json`, credentials or local
receipts. Never put tokens, passwords or sign-in codes into Codex. The recorder's automatic
redaction is an additional check, not a reason to include secrets.

Start **Codex CLI in your fork's `week-04/day-05/` folder** (`codex`). Complete the ungraded native round trip
in OPTIONAL_TOOLS.md. For the actual Challenge, start or resume Codex here again. Keep your own
instructions, observations and decisions in that real conversation.

## 3. Finish the native submission, then save its conversation

After `databricks_platform.py submit` reports `verified: true`, note its native commit SHA.
Exit Codex. In the same Workstation terminal:

```sh
git pull --ff-only origin main
python3 list_codex_sessions.py
```

The list shows the timestamp and original session ID for this folder. Select the session(s) you
actually used. Do not select someone else's session or invent a transcript. If the list is empty,
stop and report it; a notebook export is not a conversation record.

Create a new empty commit to hold the capture link. It does not change the exported notebook:

```sh
git commit --allow-empty -m "Record Codex work for native Databricks submission"
.tools/entire/entire session attach YOUR-SESSION-ID --agent codex
```

Read the confirmation: it must name your session and this new unpublished commit. Confirm to
attach. For additional sessions used on this submission, run `session attach` with each ID.
This supported command reads original Codex records; it does not reconstruct your conversation.
Do not amend the native submission or force-push.

## 4. Check the captured record and push it

```sh
.tools/entire/entire checkpoint list
.tools/entire/entire checkpoint explain YOUR-CHECKPOINT-ID --full --no-pager
git push origin main
git push origin entire/checkpoints/v1
```

Use the checkpoint ID printed by attach/list. Inspect that it contains your instructions,
Codex's replies and the native operation context. Do not proceed if the recorder reports zero
turns, cannot find the transcript, or the push fails. If you discover a credential in the record,
do not push; ask the facilitator to help remove it safely.

## 5. Confirm the remote record

```sh
git fetch origin entire/checkpoints/v1
git rev-parse entire/checkpoints/v1
git rev-parse FETCH_HEAD
git rev-parse HEAD
```

The first two hashes must match: the checkpoint branch reached GitHub. Open your public
fork in GitHub and select `entire/checkpoints/v1` to confirm the checkpoint files are there.
The last hash is your final submission commit, which includes the capture link. Your native
run receipt still names the successful Databricks run.

**For the connection walkthrough, stop here. Do not turn in the practice result.** Return to
CHALLENGE.md and start the actual task. Repeat these finish steps after completing it.

## 6. Turn in the completed Challenge only

Check [the task’s submission checklist](CHALLENGE.md#what-to-submit-and-how-it-is-checked)
for the notebook, report and output evidence; this page adds the conversation-saving steps
only when the trainer requires them.

In Classroom, attach your fork's **base URL** with **Add or create → Link**, add branch `main` and the final
commit SHA in a private comment, and select **Turn in**. Keep your fork public so the assessment service can read the repository and checkpoint branch without an invitation.
Ownership and Trait evidence comes from your Codex work, not from Genie logs.
