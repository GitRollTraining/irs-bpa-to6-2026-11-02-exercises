# AGENTS.md

`durations.py` parses short durations such as `1h30m` into seconds; `test_durations.py` holds its tests.

- Run the tests before you say a change is done: `python3 -m pytest -q`.
- Keep a type hint on every argument and return value, and a docstring on every function.
- Change only `durations.py` and `test_durations.py` unless the task names another file.
