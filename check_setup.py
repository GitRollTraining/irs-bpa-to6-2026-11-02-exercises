"""Check that this workspace can run the practice exercises: python3 check_setup.py"""
import importlib.metadata
import json
import pathlib
import re
import subprocess
import sys

KIT = pathlib.Path(__file__).resolve().parent
missing = []
if sys.version_info < (3, 10):
    missing.append(f"Python 3.10 or later (this is {sys.version.split()[0]})")
versions = {"Python": sys.version.split()[0]}
for name in ("pytest", "jsonschema"):
    try:
        versions[name] = importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        missing.append(name)


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout.strip()


try:
    found = re.search(r"(\d+)\.(\d+)", git("--version"))
except FileNotFoundError:
    found = None
if not found:
    missing.append("Git")
elif (int(found[1]), int(found[2])) < (2, 28):
    missing.append(f"Git 2.28 or later (this is {found[0]})")
else:
    versions["Git"] = found[0]
    for key in ("user.name", "user.email"):
        if not git("config", "--global", key):
            missing.append(f"your Git {key.split('.')[1]} (git config --global {key} ...)")

# The model the extractor calls, asked one short question through the kit's one route to it.
sys.path.insert(0, str(KIT))
from model import ask  # noqa: E402

route = json.loads((KIT / "model-route.json").read_text())
try:
    reply = ask("Reply with the single word ready.", "Are you there?")
    versions["model"] = f"{route['model']} answered \"{reply.strip()[:20]}\""
except Exception as failure:  # any failure of the route is reported, not raised
    missing.append(f"the model the extractor calls ({failure})")

if missing:
    print("Missing: " + ", ".join(missing))
    sys.exit(1)
print("Setup OK: " + ", ".join(f"{k} {v}" for k, v in versions.items()))
