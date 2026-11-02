"""Prepare the course: python3 setup.py (Windows: py setup.py).

Creates .venv, installs requirements, registers the practice kernel, creates the
start tag if absent, and configures missing Git identity in this checkout only.
The final readiness check is offline; --check-model adds an explicit live probe.
"""
import argparse
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


def run(*args, **kwargs):
    return subprocess.run([str(a) for a in args], check=True, **kwargs)


def git(*args):
    return subprocess.run(["git", "-C", str(KIT), *args], capture_output=True, text=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-model", action="store_true", help="also send a live model probe")
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        sys.exit("Install Python 3.10 or later and run setup.py again.")
    try:
        version = git("--version")
    except FileNotFoundError:
        sys.exit("Install Git 2.28 or later and run setup.py again.")
    if version.returncode or git("rev-parse", "--show-toplevel").returncode:
        sys.exit("Run setup.py in a Git checkout of the course, with Git 2.28 or later installed.")

    step("1 of 5: the Python environment .venv")
    if not PYTHON.exists():
        try:
            run(sys.executable, "-m", "venv", VENV)
        except subprocess.CalledProcessError:
            sys.exit("Could not create .venv. Install your Python distribution's venv/ensurepip "
                     "support (on Debian/Ubuntu: python3-venv), then run "
                     f'"{sys.executable}" -m venv "{VENV}" and rerun setup.py.')
    print(PYTHON)

    step("2 of 5: requirements.txt")
    run(PYTHON, "-m", "pip", "install", "--quiet", "--disable-pip-version-check", "-r", KIT / "requirements.txt")

    step("3 of 5: the notebook kernel " + KERNEL)
    env = os.environ.copy()
    env.update(PATH=str(BIN) + os.pathsep + env.get("PATH", ""), VIRTUAL_ENV=str(VENV))
    run(PYTHON, "-m", "ipykernel", "install", "--user", "--name", KERNEL,
        "--display-name", "Python (practice .venv)",
        "--env", "PATH", env["PATH"], "--env", "VIRTUAL_ENV", VENV)

    step("4 of 5: Git (this checkout and its exercises)")
    if git("rev-parse", "--verify", "--quiet", "refs/tags/start").returncode != 0:
        run("git", "-C", KIT, "tag", "start")
        print("Tagged this state start: a reset restores it.")
    for key, question in (("user.name", "Your name, for your Git commits: "),
                          ("user.email", "Your email, for your Git commits: ")):
        if git("config", "--get", key).stdout.strip():
            continue
        try:
            answer = input(question).strip()
        except EOFError:
            answer = ""
        if answer:
            run("git", "-C", KIT, "config", "--local", key, answer)
    # Existing exercises retain files/history and explicit local identity overrides.
    sys.path.insert(0, str(KIT / "lab-states"))
    from build_lab import configure_identity
    for start in KIT.glob("week-*/day-*/*/start.py"):
        for name in ("lab", "extractor"):
            repo = start.parent / name
            if (repo / ".git").exists():
                configure_identity(repo)

    step("5 of 5: readiness" + (" including a live model probe" if args.check_model else " (offline)"))
    check_args = [PYTHON, KIT / "check_setup.py"]
    if args.check_model:
        check_args.append("--check-model")
    check = subprocess.run([str(a) for a in check_args], env=env)
    if check.returncode:
        print("\nNot ready yet. Fix the items above and rerun setup.py.")
        return check.returncode
    print('\nDone. Open this folder in VS Code and select "Python (practice .venv)". '
          'Restart an already running notebook kernel after setup.')
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, subprocess.CalledProcessError) as failure:
        sys.exit(f"Setup failed: {failure}. Fix the reported step and rerun setup.py.")
