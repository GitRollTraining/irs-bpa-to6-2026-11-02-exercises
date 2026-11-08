#!/bin/sh
# Week 2's Python environment: bash reference-app/setup.sh, from the course folder.
# Makes reference-app/.venv with venv and installs the app's packages (Flask, pytest) into it.
# Running it again keeps the environment and installs only what changed.
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
echo "Done. Next, in this terminal:"
echo "  source reference-app/.venv/bin/activate"
echo "  python reference-app/check_setup.py"
