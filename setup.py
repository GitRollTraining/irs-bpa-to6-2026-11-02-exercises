"""Set up this repository for the practice exercises, once: python3 setup.py (on Windows: py setup.py)

It makes the Python environment .venv, installs requirements.txt into it, registers the notebook
kernel "practice", marks the state that a reset restores (the tag start), asks for your Git name
and email if Git has none, and then runs check_setup.py. You can run it again at any time.
"""
import os
import pathlib
import subprocess
import sys

KIT = pathlib.Path(__file__).resolve().parent
VENV = KIT / ".venv"
BIN = VENV / ("Scripts" if os.name == "nt" else "bin")
PYTHON = BIN / ("python.exe" if os.name == "nt" else "python")
KERNEL = "practice"


def step(text):
    print("\n== " + text, flush=True)


def run(*args):
    subprocess.run([str(a) for a in args], check=True)


def git(*args):
    return subprocess.run(["git", "-C", str(KIT), *args], capture_output=True, text=True)


if sys.version_info < (3, 10):
    sys.exit("This needs Python 3.10 or later; this is " + sys.version.split()[0] + ".\n"
             "Install Python from https://www.python.org/downloads/ and run this again.")

step("1 of 5: the Python environment .venv")
if not PYTHON.exists():
    run(sys.executable, "-m", "venv", VENV)
print(PYTHON)

step("2 of 5: pytest, jsonschema and ipykernel, from requirements.txt")
run(PYTHON, "-m", "pip", "install", "--quiet", "--disable-pip-version-check", "-r", KIT / "requirements.txt")

step("3 of 5: the notebook kernel \"" + KERNEL + "\"")
# A notebook's shell lines, such as !python3 -m pytest, use the kernel's PATH: .venv comes first.
run(PYTHON, "-m", "ipykernel", "install", "--user", "--name", KERNEL,
    "--display-name", "Python (practice .venv)",
    "--env", "PATH", str(BIN) + os.pathsep + os.environ.get("PATH", ""),
    "--env", "VIRTUAL_ENV", str(VENV))

step("4 of 5: Git")
if git("rev-parse", "--verify", "--quiet", "refs/tags/start").returncode != 0:
    run("git", "-C", KIT, "tag", "start")
    print("Tagged this state start: a reset restores it.")
for key, question in (("user.name", "Your name, for your Git commits: "),
                      ("user.email", "Your email, for your Git commits: ")):
    if git("config", "--global", key).stdout.strip():
        continue
    try:
        answer = input(question).strip()
    except EOFError:
        answer = ""
    if answer:
        run("git", "config", "--global", key, answer)

step("5 of 5: check_setup.py")
code = subprocess.run([str(PYTHON), str(KIT / "check_setup.py")]).returncode
if code == 0:
    print("\nDone. Open this folder in VS Code, open a notebook, and select the kernel \"" + KERNEL + "\".")
else:
    print("\nThe environment is made. Fix what the Missing line names, then run python3 check_setup.py again.\n"
          "On your own computer the model can show as missing: four exercises of days 2 and 3 need it.")
sys.exit(code)
