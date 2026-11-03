# 4.2 Push after a rejection

Check where your push goes, then push your commit to the lab's remote without losing your teammate's work.

You committed a coding agent's change, and the agent set where your clone pushes. Then a teammate pushed to the lab's remote. Each `.git` folder beside your clone `extractor` stands in for a repository on a Git host.

## Start

Follow the [Day 4 setup](../README.md). Work by hand, without AI tools. In a new terminal in the course folder, these commands create the workspace only if it is missing, then enter it:

```sh
test -d week-01/day-04/push-after-rejection/extractor/.git || python3 reset.py push-after-rejection
cd week-01/day-04/push-after-rejection/extractor
```

All paths below are relative to `extractor/`. Read `docs/remote.md`, which names the lab's remote, and show your commit:

```sh
git show --stat HEAD
```

Expect your commit, `Fail a reply whose amount is text`, and `1 file changed`. If the output fills the screen, press `q`.

## Push, fetch and merge

**Check the remote.**

```sh
git remote -v
```

Expect a line that ends `shared.git (fetch)` and one that ends `mirror.git (push)`.

**Set the push line.** Use section 4.2 of the notebook to explain the change.

| Problem | Change to make |
|---|---|
| `git push` uses the `(push)` line, which names `mirror.git`, not the lab's remote that `docs/remote.md` names. | Set only the `(push)` line: `git remote set-url --push origin ../shared.git`. |

<details><summary>Why each change</summary>

| Problem | Why |
|---|---|
| `git push` uses the `(push)` line, which names `mirror.git`, not the lab's remote that `docs/remote.md` names. | `docs/remote.md` names `shared.git`, the lab's remote. The `(fetch)` line names it. But `git push` uses the `(push)` line, which names `mirror.git`, not the lab's remote. Section 4.2, list "A remote", on `git remote -v`: "Before the first push, run it: is origin the lab's remote?" |

</details>

```sh
git remote set-url --push origin ../shared.git
git remote -v
```

Expect both lines to name `shared.git`.

**Push.**

```sh
git push
```

Expect `! [rejected]`: your clone does not hold your teammate's commit yet. If you do not see `rejected`, run `python3 ../check.py`.

**Fetch.** Use section 4.2 of the notebook to explain the change.

| Problem | Change to make |
|---|---|
| Git's hint names `git pull`, which also merges what came in before you read it. | Use `git fetch`: it only downloads, so you can read your teammate's commit first. |

<details><summary>Why each change</summary>

| Problem | Why |
|---|---|
| Git's hint names `git pull`, which also merges what came in before you read it. | A pull also tries to merge what came in, before you read it. A fetch only downloads, so you can read it first. Section 4.2, the figure of two copies: "fetch, read what came in, merge, then push." |

</details>

```sh
git fetch
```

Expect `-> origin/main`, your copy of origin's main branch.

**Read what came in.**

```sh
git show --stat origin/main
```

Expect `Author: Teammate` and `2 files changed`. Merge only what you have read.

**Merge.** `--no-edit` keeps Git's own message, so no editor opens.

```sh
git merge --no-edit origin/main
```

Expect `Merge made by`.

**Push again**, then check:

```sh
git push
python3 ../check.py
```

Expect `main -> main`, with no `rejected`. Finish when the check prints `Done:`. If it prints `Not yet:`, address the findings and check again. The check cannot tell whether you read your teammate's commit before the merge.

## Reflect

When should the `(fetch)` and `(push)` lines name two repositories? When would `git pull` do as well as a fetch, a read and a merge? What in your teammate's commit would make you stop before the merge?

[Worked answer](../answers/push-after-rejection/) · [Start over](../../../README.md#start-an-exercise-again)
