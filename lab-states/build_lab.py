"""Build the lab repository at one of its saved states, for an exercise's start.py:

    from build_lab import build
    build(destination_folder, "run1")

Each state is the one before it plus the files in its folder here, committed as the course team:

  base        the simulated notes, the field list and the route to the model
  configured  + the coding agent's configuration, then the data-rules check, passed
  run1        + the output schema and its tests, with no model call
  run2        + the extractor, its system prompt, and its tests on recorded replies

The destination is emptied in place rather than deleted, so a terminal open inside it keeps working.
"""
import pathlib
import shutil
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
KIT = HERE.parent
TEAM = ["-c", "user.name=Course team", "-c", "user.email=course@example.invalid"]
STATES = ["base", "configured", "run1", "run2"]
COMMITS = {
    "base": [(["README.md", "docs/fields.md", "notes", "model.py", "model-route.json", ".gitignore"],
              "Add the simulated notes, the field list and the route to the model")],
    "configured": [([".claude/settings.json"], "Add the coding agent's configuration for the lab repository"),
                   (["docs/data-rules-check.md"], "Record the data-rules check, passed, before any AI tool")],
    "run1": [(["schema", "tests/test_schema.py"], "Run 1: add the output schema and its tests, with no model call")],
    "run2": [(["extractor.py", "prompts", "tests/test_extractor.py", "tests/recorded"],
              "Run 2: add the extractor, its system prompt and its tests on recorded replies")],
}


def build(dest, state):
    dest = pathlib.Path(dest)
    dest.mkdir(exist_ok=True)
    for child in dest.iterdir():
        shutil.rmtree(child) if child.is_dir() else child.unlink()

    def git(*args):
        subprocess.run(["git", *TEAM, *args], cwd=dest, check=True, capture_output=True)

    git("init", "-q", "-b", "main")
    for name in STATES[:STATES.index(state) + 1]:
        shutil.copytree(HERE / name, dest, dirs_exist_ok=True)
        if name == "base":
            shutil.copytree(KIT / "notes", dest / "notes", dirs_exist_ok=True)
            for supplied in ("model.py", "model-route.json"):
                shutil.copy(KIT / supplied, dest / supplied)
        for paths, message in COMMITS[name]:
            git("add", *paths)
            git("commit", "-q", "-m", message)
