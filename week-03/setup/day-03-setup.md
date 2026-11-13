# Set up Wednesday in Databricks (week 3, day 3)

For the trainer. Wednesday's four exercises run in the class's Databricks workspace. Do these steps before class, in order, after Monday's setup (`day-01-setup.md`). The course made up the return files: no file is a real taxpayer. Wednesday's setup makes the volume `course.returns.raw` with 52 return files, and one schema for each learner, `course.learner_NN`, where the learner makes tables.

## Before Wednesday

1. **Get the files.** In your Git folder of the course, pull, so that `week-03/day-03` and `week-03/setup/day-03-setup.ipynb` are there.
2. **Start the compute.** The class's notebook compute must run Databricks Runtime 14.3 or above, or be serverless: the XML reader needs it. Write down its name: learners select it in each exercise.
3. **Fill in the learners.** Open `week-03/setup/day-03-setup.ipynb` and attach it to the compute. In cell 1, set `CLASS_GROUP` to the group that holds the learners. In `LEARNERS`, give each learner a two-digit number and their Databricks user name, and put your own user name at `"00"`. Do this in the workspace only. Do not commit it: the course repository holds no learner's name or email. You need `CREATE VOLUME` and `CREATE SCHEMA` on the catalog `course`, and `MANAGE` (or ownership) on it to grant rights.
4. **Run cells 1 to 4.** Cell 3 should print these things:
   - 52 files and 52 rows
   - dependents 77, W-2s 62, tax-change cases 11
   - F-30037: 4 returns; F-30074: 1
   - adjusted gross income 0: `return-F-30111-2021.xml`
   - `IRSW2 is array | DependentDetail is array`
5. **Tell each learner their number.** Each learner types `course.learner_NN` in cell 1 of each exercise notebook.
6. **Check the reader path.** Week 2's reader is in your Git folder at `week-02/day-03/answers/exercise-04-a-repeated-element/files/form1040.py`. Exercise 1's test 3 imports it from there.

## In class

- Demo before exercise 1: read the folder with `_metadata.file_name` named, explode the dependents with `return_id`, and count rows against the files. Leave the W-2s to the learners.
- Demo before exercise 2: add `tax_to_agi` and fill its record row. Show its null on `F-30111-2021`. Leave the W-2 ratio to the learners.
- Demo before exercise 3: build the window with the frame ending at -1 on `agi_amt`, and check the filer F-30037's 2023 value by hand. Exercise 3 uses `wages_amt` and adds `LAG`.
- Demo before exercise 4: split at random, find one filer in two sets, then split by year and run the five tests (exercise 4's cell 5). Use your own schema, `course.learner_00`.
- Short on time: exercise 4 becomes on-your-own work. Thursday needs `train`, `valid` and `test`, so name it at the close.
- Thursday runs `week-03/day-03/wednesday-tables.ipynb` in each learner's Git folder as a one-off job. The jobs file must name that path in the learner's own Git folder, so that the notebook finds the exercise notebooks and week 2's reader beside it.

## After class

Nothing to reset. Each learner's notebooks write with `overwrite`, so a second run replaces their tables. To write the files again, run cells 1 and 2.

## Not yet checked in Databricks

The course team ran the exercises on a computer without Databricks, against a stand-in in plain Python that reads the same 52 files. Each exercise's `decisions.md` says how, under "Where it ran". Check each item at your run-through, and tell the course team what differs:

1. Cell 2 writes files to `/Volumes/course/returns/raw/` with Python's `open`, and cell 3's numbers match step 4 above. Our proposed answer: volumes allow file access by path ("This makes them ideal for machine learning frameworks and open source Python modules that require POSIX-style access.", https://docs.databricks.com/aws/en/volumes/volume-files).
2. The XML reader reads the default namespace of the files and names the columns `ReturnHeader`, `ReturnData` and `CourseLabel`, with `IRSW2` and `DependentDetail` as arrays (exercise 1, cells 2 to 4).
3. Exercise 1, run as a learner from start: cell 3 fails with "cannot be resolved" on `file_name`, and passes once cell 2 names `_metadata.file_name`. Cell 6's test 3 imports `form1040` by the path it appends.
4. Exercises 2 to 4, run as a learner from start: each check prints `Not yet` first and `Done:` with the answer's cells. Exercise 2's cell 4 stops on the join that comes first (63 rows against 52).
5. Exercise 3's check reads 48,000 and 0.15 for `F-30037-2023`, and exercise 4's cell 6 prints train 21 returns with 3 tax-change cases, valid 15 with 3, test 16 with 5.
6. `wednesday-tables.ipynb` runs the four exercise notebooks with `%run ./<folder>/exercise` and lists eight tables. Our proposed answer: "You can organize notebooks into directories, such as `%run ./dir/notebook`." (https://docs.databricks.com/aws/en/notebooks/notebook-workflows)
