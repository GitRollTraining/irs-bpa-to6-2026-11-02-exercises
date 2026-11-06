# Day 3: Test automation with AI, and CI/CD

Nine exercises, one notebook each. In exercises 1 to 6, Codex writes tests and you check that each test can fail. You also read test results and find why a test fails. In exercises 7 to 9, GitHub runs your tests on every change, a failing check stops the merge, and a scanner looks for security faults.

Open an exercise's `exercise.ipynb`, choose the **.venv** kernel, and run its first code cell to write the practice files. Then follow the steps in a terminal. An exercise is done when its last cell prints `Done:`.

| Exercise | What you will do |
|---|---|
| [1 · Tests that can fail](exercise-01-tests-that-can-fail/exercise.ipynb) | Break the code on purpose, see which of five passing tests fail, and keep only those. |
| [2 · Codex writes unit tests](exercise-02-codex-writes-unit-tests/exercise.ipynb) | Write the expected values yourself, have Codex write the tests, and check that each one can fail. |
| [3 · Find elements as a user would](exercise-03-find-elements-as-a-user/exercise.ipynb) | Install the test browser, and have Codex rewrite a browser test that waits a fixed time and finds a row by its position. |
| [4 · Run headless, read the results](exercise-04-run-headless-read-results/exercise.ipynb) | Run the unit tests, then the browser tests without a window, and read the failure from its result file and its trace. |
| [5 · Test or application?](exercise-05-test-or-application/exercise.ipynb) | After two changes by a teammate, decide which part is at fault each time, and fix only that part. |
| [6 · Find a flaky test's cause](exercise-06-flaky-test-cause/exercise.ipynb) | Find why a test passes alone and fails after another, and fix the cause instead of running it again. |
| [7 · Tests on every pull request](exercise-07-tests-on-every-pull-request/exercise.ipynb) | Have Codex write a GitHub Actions workflow, and see your tests run on GitHub for a pull request. |
| [8 · A failing check blocks the merge](exercise-08-a-failing-check-blocks-the-merge/exercise.ipynb) | Make the check required on `main`, and see GitHub refuse a change whose test fails. |
| [9 · Scan and decide](exercise-09-scan-and-decide/exercise.ipynb) | Scan the code with Bandit, then fix each finding or keep it with a reason. |

Exercises 4 and 5 use the test browser that you install in exercise 3. Exercise 7 makes a public practice repository on GitHub, and exercise 8 continues in it. Before exercise 1, Codex must be installed and signed in (course README, step 1). Solved copies are in [answers/](answers/): each is the same notebook, and its first cell writes the finished files.
