"""Check week 2's setup: python reference-app/check_setup.py, with the week's environment active.

It checks Python 3.10 or later, that this terminal runs a virtual environment (reference-app/.venv,
made by bash reference-app/setup.sh), that Flask and pytest are in it, that the app's case list page
opens and its tests pass, and that the Codex CLI answers and is signed in. Nothing is sent to a model.
Continue when it prints Setup OK.
"""
import importlib.metadata
import os
import pathlib
import shutil
import subprocess
import sys

APP = pathlib.Path(__file__).resolve().parent
ACTIVATE = "source reference-app/.venv/bin/activate (from the course folder)"
SETUP = "bash reference-app/setup.sh (from the course folder)"
CODEX_INSTALL = "curl -fsSL https://chatgpt.com/codex/install.sh | sh"


def check_python(missing, found):
    """Python 3.10 or later, run from a virtual environment this terminal has active."""
    found.append(f"Python {sys.version.split()[0]}")
    if sys.version_info < (3, 10):
        missing.append("Python 3.10 or later: tell your trainer which Python python3 --version shows")
    active = os.environ.get("VIRTUAL_ENV")
    if not active or sys.prefix == sys.base_prefix:
        missing.append(f"the environment is not active in this terminal: run {ACTIVATE}, "
                       "then python reference-app/check_setup.py")
        return False
    if pathlib.Path(active).resolve() != pathlib.Path(sys.prefix).resolve():
        missing.append(f"this check ran with another Python than the active environment: run {ACTIVATE}, "
                       "then python reference-app/check_setup.py")
        return False
    found.append(f"environment {sys.prefix}")
    return True


def check_packages(missing, found):
    """Flask and pytest import in this environment."""
    ready = True
    for name in ("flask", "pytest"):
        try:
            __import__(name)
            found.append(f"{name} {importlib.metadata.version(name)}")
        except ImportError:
            missing.append(f"{name}: run {SETUP}, then {ACTIVATE}")
            ready = False
    return ready


def check_app(missing, found):
    """The case list page opens, and the app's tests pass, as python -m pytest runs them."""
    page = subprocess.run([sys.executable, "-c", "from app import app; "
                           "print(app.test_client().get('/').status_code)"],
                          cwd=APP, capture_output=True, text=True, timeout=120)
    if page.stdout.strip() != "200":
        said = (page.stderr.strip() or page.stdout.strip() or "no output").splitlines()[-1]
        missing.append(f"the app's case list page did not open ({said}): tell your trainer")
    else:
        found.append("the case list page opens")
    tests = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
                           cwd=APP, capture_output=True, text=True, timeout=300)
    summary = (tests.stdout.strip() or tests.stderr.strip() or "no output").splitlines()[-1]
    if tests.returncode:
        missing.append(f"the app's tests did not pass ({summary}): tell your trainer")
    else:
        found.append(f"tests: {summary}")


def check_codex(missing, found):
    """The Codex CLI answers, and is signed in. Nothing is sent to a model."""
    codex = shutil.which("codex")
    if not codex:
        missing.append(f"Codex CLI: install it with {CODEX_INSTALL}, open a new terminal, then sign in "
                       "with codex login (in the hosted workspace, codex login --device-auth)")
        return
    try:
        version = subprocess.run([codex, "--version"], capture_output=True, text=True, timeout=60)
        status = subprocess.run([codex, "login", "status"], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as failure:
        missing.append(f"Codex CLI did not answer ({failure}): install it again with {CODEX_INSTALL}")
        return
    said = (version.stdout.strip() or version.stderr.strip()).splitlines()
    if version.returncode or not said:
        missing.append(f"Codex CLI did not give its version: install it again with {CODEX_INSTALL}")
    elif status.returncode:
        missing.append("Codex CLI is not signed in: run codex login, or in the hosted workspace "
                       "codex login --device-auth")
    else:
        found.append(f"{said[0]}, signed in")


def main():
    missing, found = [], []
    if check_python(missing, found) and check_packages(missing, found):
        check_app(missing, found)
    check_codex(missing, found)
    if missing:
        if found:
            print("OK: " + "; ".join(found))
        print("Missing:\n" + "\n".join(f"- {item}" for item in missing))
        print("Fix each item, then run python reference-app/check_setup.py again.")
        return 1
    print("Setup OK: " + "; ".join(found))
    return 0


if __name__ == "__main__":
    sys.exit(main())
