# Findings

- Exercise 3 is the copy containing the invoked planning-with-files skill.
- AGENTS.md requires pytest after changes; do not start the Flask server.
- templates/list.html already receives each case score. Add the label beside the case link for scores >= 50.
- Preserve case data and scoring rules.

- Verified scores 49, 50, and 51: label absent at 49, present at 50 and 51.
- Verified every actual case row matches its selection score.
- Case data unchanged; git diff --check passed.
