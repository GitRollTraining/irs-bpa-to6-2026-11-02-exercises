---
name: map-codebase
description: Map a Python codebase before an edit. Use when asked to map, onboard to or explain the structure of a codebase. Writes CODEMAP.md; changes no code.
---

# Map a codebase

Input: the Python package in this folder. Output: `CODEMAP.md` in this folder. Do not change any other file.

1. Find the entry point: the package's `__main__.py`, or the file with `if __name__ == "__main__":`.
2. Read the first lines of each module for its imports.
3. Write `CODEMAP.md` with these five sections:
   - `## Flow`: how one run goes through the modules, from the entry point.
   - `## Owners`: each module, and what it owns, in one line.
   - `## Imports`: one line for each import between the package's modules, as `a.py -> b.py`.
   - `## Checks`: each place that checks data, as file and line.
   - `## Risky spots`: code that runs at import, side effects such as file writes, and code without tests.
4. End with the files to read next.
