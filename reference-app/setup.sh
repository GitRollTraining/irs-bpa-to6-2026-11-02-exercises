#!/bin/sh
# Week 2's setup: bash reference-app/setup.sh, from the course folder, after git pull.
# Makes reference-app/.venv with venv, installs the app's packages (Flask, pytest, the notebooks'
# kernel) into it, then runs check_setup.py in it: Python, the packages, the app's page and tests,
# the notebooks' kernel, and Codex. Running it again keeps the environment and installs only what changed.
set -e
cd "$(dirname "$0")"

# Under pyenv, python3 fails when the course folder's .python-version names a Python that pyenv
# lacks; the system Python then makes the environment.
PYTHON="python3"
if ! python3 -c "" 2>/dev/null; then
    PYTHON="env PYENV_VERSION=system python3"
fi
if ! $PYTHON -c "import sys; sys.exit(sys.version_info < (3, 10))"; then
    echo "Missing: Python 3.10 or later. This terminal's python3 is $($PYTHON --version 2>&1). Tell your trainer."
    exit 1
fi

echo "Making the environment: python3 -m venv .venv"
$PYTHON -m venv .venv
echo "Installing the app's packages: pip install -r requirements.txt"
.venv/bin/python -m pip install --quiet --disable-pip-version-check -r requirements.txt

# The environment is on for this script only: a script cannot turn it on in the learner's terminal.
. .venv/bin/activate
echo "Checking the setup: python reference-app/check_setup.py"
python check_setup.py
echo "Next, in this terminal and in each new one: source reference-app/.venv/bin/activate"
