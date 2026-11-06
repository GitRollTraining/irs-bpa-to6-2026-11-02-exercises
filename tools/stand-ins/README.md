# Stand-ins

`codex`, `claude` and `code` stand in for the real commands while `check_setup.py` runs every cell of the
notebooks. With them first on that run's `PATH`, no text goes to a model, no coding agent starts and no
editor tab opens: `codex` answers the `codex exec` calls of `model.py` with made-up replies, as `claude`
does for the route through Claude Code. Do not put this folder on your own `PATH`: the exercises need the
real commands.
