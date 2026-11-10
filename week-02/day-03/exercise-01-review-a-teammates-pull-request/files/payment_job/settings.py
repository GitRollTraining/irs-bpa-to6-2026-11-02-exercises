"""The job's settings, from data/job_settings.json."""
import json
from pathlib import Path

SETTINGS = json.loads((Path(__file__).resolve().parent.parent / "data" / "job_settings.json").read_text(encoding="utf-8"))
