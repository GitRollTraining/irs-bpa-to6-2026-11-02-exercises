# Exercise 1 notes

Type each answer after its colon, on the same line. The steps of README.md say what goes where.

## Step 1. databricks -v

version: Databricks CLI v0.278.0
version_exit: 0

## Step 2. databrick -v

miss_message: bash: databrick: command not found
miss_exit: 127

## Step 3. databricks auth login, then databricks auth profiles

profile: course
login_exit: 0
profile_valid: YES

## Step 4. databricks catalogs list

predicted_catalogs: course, because the trainer gave our group USE CATALOG on it on Monday; maybe system
listed_catalogs: course, system
catalogs_exit: 0
catalogs_match: It matches: I see course because of the grant, and only catalogs I may use.

## Step 5. databricks tables list, two schemas

returns_tables: batch_clean, batch_dirty, batch_governed, return_header, return_summary
returns_exit: 0
my_schema: course.learner_07
my_tables: dependents, feature_record, features, return_table, test, train, valid, w2s
my_tables_exit: 0

## Step 6. databricks tables get course.returns.return_header

get_exit: 0
column_1: total_income
column_1_type: INT
column_1_comment: none
column_1_monday: INT; comment and tags none; the draft said "always positive" and I gave it change
column_2: wages_amt
column_2_type: INT
column_2_comment: Wages, salaries and tips the filer reported, in whole dollars.
column_2_monday: INT; comment "Wages, salaries and tips the filer reported, in whole dollars."; no tags
difference: No difference in type or comment; my Monday draft for total_income was never saved, so the catalog still has no comment.
