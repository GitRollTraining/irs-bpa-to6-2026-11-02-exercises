#!/usr/bin/env python3
"""List original Codex session IDs for this repository; never rewrite transcripts."""
import json
import os
from pathlib import Path

root = Path(__file__).resolve().parent
home = Path(os.environ.get('CODEX_HOME', Path.home() / '.codex'))
rows = []
for path in (home / 'sessions').rglob('*.jsonl'):
    with path.open() as stream:
        try:
            event = json.loads(stream.readline())
        except (ValueError, OSError):
            continue
    meta = event.get('payload', {})
    if event.get('type') == 'session_meta' and Path(meta.get('cwd', '/')).resolve() == root:
        rows.append((meta.get('timestamp', ''), meta.get('id', '')))
for timestamp, session in sorted(set(rows)):
    print(timestamp, session)
if not rows:
    raise SystemExit('No original Codex session found for this folder. Start Codex here before continuing.')
