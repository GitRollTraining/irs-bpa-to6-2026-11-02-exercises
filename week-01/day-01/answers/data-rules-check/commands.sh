# The answer to "Write the extractor's data requirements, then pass the data-rules check".
# Run it from ~/practice/week-01/day-01/data-rules-check/lab, after
# python3 ~/practice/reset.py data-rules-check
# The two files filled in: the files as supplied, with every empty and TODO cell written.
cp ~/practice/week-01/day-01/answers/data-rules-check/data-rules-check.md ~/practice/week-01/day-01/answers/data-rules-check/requirements.md docs/
git add docs/data-rules-check.md docs/requirements.md
git commit -m "Record the data-rules check, passed, and the extractor's requirements, before any AI tool"
git log --oneline   # your commit above the course team's, and no commit an AI tool made before it
python3 ../check.py
