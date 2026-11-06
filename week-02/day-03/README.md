# Day 3: Test automation with AI, and CI/CD

Six exercises, one notebook each. Codex writes tests, and you check that each test can fail. You run unit tests and browser tests without a window, read their results, decide whether a failing test or the application is at fault, and fix a flaky test at its cause.

Open an exercise's `exercise.ipynb`, choose the **.venv** kernel, and run its first code cell to write the practice files. Then follow the steps in a terminal. An exercise is done when its last cell prints `Done:`.

| Exercise | What you will do |
|---|---|
| [1 · Tests that can fail](exercise-01-tests-that-can-fail/exercise.ipynb) | Break the code on purpose, see which of five passing tests fail, and keep only those. |
| [2 · Codex writes unit tests](exercise-02-codex-writes-unit-tests/exercise.ipynb) | Write the expected values yourself, have Codex write the tests, and check that each one can fail. |
| [3 · Find elements as a user would](exercise-03-find-elements-as-a-user/exercise.ipynb) | Install the test browser, and have Codex rewrite a browser test that waits a fixed time and finds a row by its position. |
| [4 · Run headless, read the results](exercise-04-run-headless-read-results/exercise.ipynb) | Run the unit tests, then the browser tests without a window, and read the failure from its result file and its trace. |
| [5 · Test or application?](exercise-05-test-or-application/exercise.ipynb) | After two changes by a teammate, decide which part is at fault each time, and fix only that part. |
| [6 · Find a flaky test's cause](exercise-06-flaky-test-cause/exercise.ipynb) | Find why a test passes alone and fails after another, and fix the cause instead of running it again. |

Exercises 4 and 5 use the test browser that you install in exercise 3. Before exercise 1, Codex must be installed and signed in (course README, step 1). Solved copies are in [answers/](answers/): each is the same notebook, and its first cell writes the finished files.
