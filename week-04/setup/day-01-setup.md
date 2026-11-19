# Set up week 4 in Databricks (week 4, day 1)

For the trainer. Every exercise of week 4, Monday to Friday, reads the same five tables in the catalog `course`, schema `returns`. Make them once, before Monday, with the setup notebook `day-01-setup.ipynb` beside this file. The course made up every row: no name, number or amount belongs to a real taxpayer. Learners only read these tables, so nothing needs resetting during the week.

## Before Monday

1. **Get the files.** In your Git folder of the course, pull, so that `week-04/setup` is there.
2. **Check week 3's setup.** The catalog `course` and the schema `course.returns` must exist, with `USE CATALOG`, `USE SCHEMA` and `SELECT` on them for `training-students`: week 3's Monday setup (`week-03/setup/day-01-setup.md`) made them. You need `CREATE TABLE` on `course.returns`, which `training-admins` holds.
3. **Run the setup notebook.** Open `week-04/setup/day-01-setup.ipynb`, attach it to the class's notebook compute (**Serverless** in the class workspace), and run cells 1 to 4. Cell 3 should print these things:
   - `model_features`: 1000 rows, yes 160, no 640, empty 200
   - `model_train`: 500 rows, yes 80, no 320, empty 100
   - `model_valid`: 250 rows, yes 40, no 160, empty 50
   - `model_test`: 250 rows, yes 40, no 160, empty 50
   - `deduction_amt` empty: 63
   - case 123 in `model_valid`: `F-40409-2022`, label yes
   - channels: A 648, B 352
4. **Hand the tables to the trainers' group,** so any trainer can run the notebook again, as week 3's setup did for its schema. In the SQL editor:

   ```sql
   ALTER TABLE course.returns.model_returns OWNER TO `training-admins`;
   ALTER TABLE course.returns.model_features OWNER TO `training-admins`;
   ALTER TABLE course.returns.model_train OWNER TO `training-admins`;
   ALTER TABLE course.returns.model_valid OWNER TO `training-admins`;
   ALTER TABLE course.returns.model_test OWNER TO `training-admins`;
   ```

5. **Check each learner's schema.** Exercise 3 on Monday writes two tables in the learner's own schema, `course.learner_NN`, which each learner made in week 3 (`week-03/setup/day-03-setup.md`): `features_flagged` and `model_feature_record`. A learner who has no schema yet makes it as week 3's exercise 1 did; tell each learner their number again.

## The tables

| Table | Rows | What it holds | Days that read it |
|---|---|---|---|
| `course.returns.model_returns` | 1,000 | One row per return as filed, tax years 2020 to 2023: the header (case key, a made-up name and city) and the Form 1040 body amounts, with the label | Monday (where a feature's source field is) |
| `course.returns.model_features` | 1,000 | One row per return: the body amounts, the features built from them, and the columns that are not features | Monday (the feature record), Tuesday (the leakage check) |
| `course.returns.model_train` | 500 | `model_features` for tax years 2020 and 2021: the training set | Monday (the baseline), Tuesday (training), Friday |
| `course.returns.model_valid` | 250 | `model_features` for tax year 2022: the validation set, which holds case 123 | Tuesday (scoring), Wednesday, Thursday, Friday |
| `course.returns.model_test` | 250 | `model_features` for tax year 2023: the test set, kept for the last check | Friday, if a learner reports a final score |

The three sets split by tax year, as week 3's exercise 4 did (`train` 2020 and 2021, `valid` 2022, `test` 2023), so no return of a later year trains a model scored on an earlier one. Each filer files one return each year, so a filer is in every set, a year apart.

## The columns

`model_returns` has the first 18 columns below. `model_features` and the three sets have every column below except `filer_name` and `city_nm`. Every amount is in whole dollars.

| Column | What it holds | Days that use it |
|---|---|---|
| `case_id` | The case number, 1 to 1,000. "Case #123" is the row where `case_id = 123` | Wednesday (the ten returns), Thursday (case 123) |
| `return_id` | The return: the filer's case key and the tax year, such as `F-40409-2022`, as week 3 wrote it | every day, as the key |
| `filer_key` | The filer's case key, written in place of the taxpayer identification number, as in week 3 | Monday (a key, not a feature) |
| `tax_year` | The tax year, 2020 to 2023; it decides the set | Monday (a key, not a feature) |
| `filer_name` | Header: a made-up name, such as `ALEX SAMPLE`. `model_returns` only | Monday (the source of `name_length`) |
| `city_nm` | Header: a made-up city, `ANYTOWN`. `model_returns` only | Monday (a header field) |
| `made_up_channel` | A filing channel the course invented, `A` or `B`. It describes no real person or group. Kept out of the features | Thursday (selection rate by group), Friday |
| `filing_status` | Filing status code: 1 single, 2 married filing jointly, 3 married filing separately, 4 head of household | Monday to Friday (a feature) |
| `wages_amt` | Wages, salaries and tips | Monday to Friday (a feature) |
| `taxable_interest_amt` | Taxable interest | Monday to Friday (a feature) |
| `other_income_amt` | Additional income from Schedule 1, such as business income. The planted feature that tracks `made_up_channel` | Monday to Friday (a feature); Thursday (the planted feature) |
| `total_income` | Wages plus taxable interest plus other income | Monday to Friday (a feature) |
| `agi_amt` | Adjusted gross income | Monday to Friday (a feature) |
| `deduction_amt` | The standard or itemized deduction. Empty in 63 returns, where the line was left blank | Monday (the missing-amount flag); Tuesday to Friday (a feature) |
| `total_tax_amt` | Total tax | Monday to Friday (a feature) |
| `withholding_amt` | Federal income tax withheld | Monday to Friday (a feature) |
| `exam_changed_tax` | The label: `yes` when a past examination changed the tax, `no` when it did not, empty for a return never examined | Monday (the outcome counts), Tuesday (the label's values; training), Wednesday (the confusion matrix) |
| `tax_added_by_exam` | The tax an examination added: 0 when it changed nothing, empty for a return never examined. Written after selection, so it gives the label away | Tuesday (the planted leak) |
| `tax_to_agi` | Total tax divided by adjusted gross income, to 4 places, as week 3 built it | Monday to Friday (a feature) |
| `deduction_to_agi` | Deduction divided by adjusted gross income, to 4 places. Empty where `deduction_amt` is empty | Monday to Friday (a feature) |
| `name_length` | The number of characters in `filer_name`, a header field. A defensible feature list strikes it | Monday (the feature to strike) |

Nothing in a table names the answer: the column comments in Databricks say what a column holds, not whether it is a feature, a leak or a proxy. The three days that need the answer read it here.

## What the course planted, and why

- **Case 123** (`F-40409-2022`, in `model_valid`): examined, label yes, tax added 3,250. Filing status 2, wages 54,400, taxable interest 120, other income 28,500, total income 83,020, adjusted gross income 81,820, deduction 42,000 (51% of its income), total tax 5,177, withholding 6,500, channel A. Its two largest pushes are its other income and its deduction (see the measurement below); in the made-up world those two raise the chance that an examination changes the tax. It is the one channel A return with other income above 5,000.
- **A group and the feature that tracks it.** `made_up_channel` is A for 648 returns and B for 352, one value per filer. `other_income_amt` names no group, but its median is 0 in channel A and 16,140 in channel B, and 344 of channel B's 352 returns have more than 5,000 of it, against 1 of channel A's 648 (case 123). The label depends on the amounts only, never on the channel; the channel reaches the score through other income.
- **Missing amounts:** `deduction_amt` is empty in 63 returns. The measurement reads an empty amount as 0 and adds `deduction_missing`, 1 where it was empty: the flag Monday's exercise 3 asks learners to add. `deduction_to_agi` is empty in the same rows.
- **A header field:** `name_length` is built from `filer_name`. It says nothing about the return's tax.
- **A leak:** `tax_added_by_exam` is above 0 for every yes and 0 for every no, so it matches the label exactly. Tuesday's check marks it known after selection.

**The label rule.** Only an examined return has a label. The baseline counts outcomes over the examined returns of `model_train` (400: 80 yes, 320 no), the models train on those 400, and accuracy, the confusion matrix, precision and recall count the 200 examined returns of `model_valid`. A never-examined return is neither right nor wrong. A model still scores it, so the selection rate by group counts all 250 returns of `model_valid`. The course chose the examined returns at random, 200 of each year's 250; a real file's examined returns were themselves picked by past selection, which Tuesday's talk on a label's origin can name.

## Why 1,000 returns: the measurement

The aim: three candidates whose accuracies differ and stay in the same order however the data falls, on numbers small enough to work by hand. The candidates, as the week's given cells should fit them:

- the baseline: always predict the most common outcome in `model_train`, which is `no`;
- logistic regression with one stated setting, the amounts scaled to one range first: `make_pipeline(StandardScaler(), LogisticRegression())`. Unscaled, the dollar amounts kept `LogisticRegression()` from converging on these rows;
- a decision tree at scikit-learn's defaults, with `random_state=0` so every run grows the same tree: `DecisionTreeClassifier(random_state=0)`.

They train on the 12 features `FEATURES` names in `day-01-course-data.py`: every amount above, the two ratios and `deduction_missing`, an empty amount read as 0. Nothing else: no key, no `made_up_channel`, no `name_length`, no `tax_added_by_exam`.

Each year has 200 examined returns, 40 of them yes. So the baseline's accuracy is a fraction a learner can work out: 320 of 400 on `model_train` and 160 of 200 on `model_valid`, both 0.80. With fewer returns the gaps fell inside chance: at 52 returns, week 3's size, `valid` held 3 tax-change cases, and one return moves accuracy by 1 in 15. At 200 examined validation returns, one return moves it by 0.005.

Run on 2026-11-19 UTC, from the course folder, with scikit-learn 1.5.2, pandas 3.1.1 and Python 3.12.6:

```
uv run --no-project --python 3.12 --with scikit-learn==1.5.2 --with pandas==3.1.1 python week-04/setup/day-01-model-check.py
```

```
1. Course data (seed 2), model_valid's 200 examined returns: baseline 0.800, logistic regression 0.955, decision tree 0.910
2. Tree under random_state 0 to 9: 0.890 to 0.910
3. Order baseline < tree < logistic kept in 981 of 1000 resamples of model_valid
4. Order kept in 17 of 19 other generator seeds; means: baseline 0.800, logistic 0.928, tree 0.898
5. Case 123 (F-40409-2022, label yes): logistic 0.964 (rank 10 of 200), tree 1; largest logistic pushes from the training mean, on the log-odds scale: other_income_amt +3.81, deduction_amt +2.65, tax_to_agi +1.24
6. Logistic at 0.5, all 250 of model_valid: channel A 22 of 162 selected (13.6%), channel B 20 of 88 selected (22.7%)
7. other_income_amt median: channel A 0, channel B 16,140; above 5,000: A 0%, B 98%
8. Wednesday's ten, logistic at 0.5: 4 TN 0.06, 11 TN 0.00, 37 TN 0.47, 50 FN 0.07, 123 TP 0.96, 205 TP 1.00, 224 TP 0.98, 463 FP 0.65, 471 FN 0.18, 905 FP 0.94; cells {'TN': 3, 'TP': 3, 'FN': 2, 'FP': 2}
```

How to read it. Line 1: the three accuracies, 0.800, 0.910 and 0.955. Line 2: the tree grown with ten other `random_state` values stays between the baseline and logistic regression. Line 3: drawing the 200 validation returns again with replacement, 1,000 times, keeps the order in 981. Line 4: making the whole data set again under 19 other seeds keeps the order in 17; in the other two (seeds 4 and 14) the tree comes level with logistic regression, and both still beat the baseline. The course's tables use seed 2, `SEED` in `day-01-course-data.py`. In line 6, TP is a true positive (selected, tax changed), FP a false positive, FN a false negative, TN a true negative.

**Case 123's pushes.** For logistic regression a feature's push is its weight times how far case 123's scaled value sits from the training mean, which is what a linear model's SHAP value is under its usual assumption. This measurement did not run the SHAP library; Thursday's writer does.

**Wednesday's ten.** `WEDNESDAY_TEN` in `day-01-course-data.py`: the examined returns of `model_valid` with `case_id` 4, 11, 37, 50, 123, 205, 224, 463, 471 and 905. Scored by the logistic regression above at 0.5 they fall 3 true positives, 2 false positives, 2 false negatives and 3 true negatives, so precision and recall on the ten are both 3 of 5. Case 37 scores 0.47, near the threshold. A tree's scores differ: the ten hold only under the logistic regression above.

## Checked in Databricks, and not yet checked

Nothing in this setup has run in Databricks yet. Checked on 2026-11-19 UTC on a computer with no Databricks: `day-01-course-data.py` gives the same 15 statements every run, and the setup notebook's cells 1, 2 and 4 run against a stand-in for `spark` that only counts the statements (18).

Not yet checked: check each at your run-through, and tell the course team what differs:

1. Cells 1 to 4 run in the class workspace on Serverless, and cell 3 prints each number of step 3. New since week 3: each table's rows go in one `INSERT` of up to 1,000 rows, about 130,000 characters, and two columns are `DOUBLE`.
2. A learner in `training-students` reads each of the five tables with no new grant, through week 3's `SELECT` on the schema.
3. The class compute's scikit-learn gives the three accuracies of line 1. The measurement used scikit-learn 1.5.2; another version may move them.
4. The `ALTER TABLE ... OWNER TO` lines of step 4.
5. Monday's three exercises (`week-04/day-01/`), each from its start to `Done:`, run as the course's test learner, a member of `training-students`: cell 1 of exercise 1 lists the 18 columns of `course.returns.model_returns`; exercise 2's counting cell shows `NULL` for the 100 empty labels; exercise 3's cells 3 and 4 write `features_flagged` and `model_feature_record` in the learner's own schema, and `.show()` prints the counts each step names. Each ran only against `week-04/day-01/answers/stand_in.py`, which reads the same SQL with DuckDB.
