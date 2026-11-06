# Day 3: Forms, tools and a score

Three exercises, one notebook each. Each one practises one idea from the Day 3 slides.

- **Exercises 1 and 3** use a food delivery app: when an order goes wrong, you message the app, and its AI turns your message into four fields of JSON. The AI's replies are sample data inside each notebook, so you need no model, key or sign-in. You run cells and change one value at a time.
- **Exercise 2** is an advanced topic, and optional. It uses synthetic IRS case notes and calls a real model when you run it in Databricks. You write a tool definition and change a few lines of Python. Outside Databricks, a scripted stand-in plays the model, so the notebook still runs.

Open an exercise's `exercise.ipynb` and run the cells from the top: click a cell and press Shift+Enter. In VS Code, choose the **.venv** kernel first. In Databricks, open the notebook from your Git folder and attach it to a compute resource. An exercise is done when its last cell prints `Done:`.

| Exercise | What you will do | Slides | Time |
|---|---|---|---|
| [1 · Check every reply against a schema](exercise-01-validate-replies/exercise.ipynb) | Run a checker on six sample replies, then tighten two loose rules so that every bad reply is rejected. | 4, 5, 7 | 10 min |
| [2 · Tool calling: the model asks, your code decides (advanced topic, optional)](exercise-02-tool-calling/exercise.ipynb) | Watch a model mail a tax notice that no person approved, then change your code: replace the tool, supply the case number yourself, and stop the model guessing a tax year. | 13 to 17 | 40 min |
| [3 · Score a prompt](exercise-03-score-a-prompt/exercise.ipynb) | Read two score tables, find the prompt line that causes the errors, and keep the better prompt. | 23, 24, 25, 28 | 15 min |

Solved copies are in [answers/](answers/): each is the same notebook with the answers filled in.
