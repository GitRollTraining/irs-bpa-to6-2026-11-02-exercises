"""Offline readiness: python3 check_setup.py. Add --check-model to send a live probe."""
import argparse
import importlib.metadata
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

KIT = pathlib.Path(__file__).resolve().parent


def git(*args, folder=KIT):
    return subprocess.run(["git", "-C", str(folder), *args], capture_output=True, text=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-model", action="store_true",
                        help="also send a short live request through model.py")
    args = parser.parse_args()
    missing = []
    versions = {"Python": sys.version.split()[0]}
    print(f"Python interpreter: {sys.executable}")
    if sys.version_info < (3, 10):
        missing.append("Python 3.10 or later")
    for name in ("pytest", "jsonschema", "ipykernel"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            missing.append(f"{name}: run setup.py to install requirements into .venv")

    # Notebook !python3 lines use PATH, which can differ from the kernel environment.
    shell_name = "python" if os.name == "nt" else "python3"
    shell = shutil.which(shell_name)
    if shell:
        probe = subprocess.run([shell, "-c", "import sys; print(sys.prefix)"],
                               capture_output=True, text=True)
        if probe.returncode or pathlib.Path(probe.stdout.strip()).resolve() != pathlib.Path(sys.prefix).resolve():
            missing.append(f"{shell_name} on PATH uses a different environment; activate .venv "
                           "and select/restart the practice notebook kernel")
    else:
        missing.append(f"{shell_name} on PATH; activate .venv before running exercise commands")

    try:
        found = re.search(r"(\d+)\.(\d+)", git("--version").stdout)
    except FileNotFoundError:
        found = None
    if not found:
        missing.append("Git: install Git 2.28 or later")
    elif (int(found[1]), int(found[2])) < (2, 28):
        missing.append(f"Git 2.28 or later (this is {found[0]})")
    else:
        versions["Git"] = found[0]
        for key in ("user.name", "user.email"):
            if not git("config", "--get", key).stdout.strip():
                missing.append(f'{key}: from the course root run git config --local {key} "YOUR VALUE", '
                               "then rerun setup.py (exercise repositories need this identity too)")
        for start in sorted(KIT.glob("week-*/day-*/*/start.py")):
            for name in ("lab", "extractor"):
                repo = start.parent / name
                if not (repo / ".git").exists():
                    continue
                for key in ("user.name", "user.email"):
                    if not git("config", "--get", key, folder=repo).stdout.strip():
                        missing.append(f"{repo.relative_to(KIT)} needs {key}; rerun setup.py "
                                       "to copy the course identity without resetting your work")

    if args.check_model:
        # Importing the model and reading its route are deliberately opt-in.
        try:
            from model import ask
            route = json.loads((KIT / "model-route.json").read_text())
            reply = ask("Reply with the single word ready.", "Are you there?")
            versions["model"] = f"{route['model']} answered {reply.strip()[:20]!r}"
        except Exception as failure:
            missing.append(f"model access: {failure}; check model-route.json and sign in to its provider")

    if missing:
        print("Missing:\n" + "\n".join(f"- {item}" for item in missing))
        return 1
    print("Setup OK (" + ("including live model probe" if args.check_model else "offline") + "): "
          + ", ".join(f"{key} {value}" for key, value in versions.items()))
    if not args.check_model:
        print("Day 1 needs no model. Before the four model exercises on Days 2–3, "
              "run check_setup.py --check-model explicitly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
