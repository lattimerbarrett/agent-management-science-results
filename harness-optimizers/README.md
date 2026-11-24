# Harness optimizers

*Section of the post: "Autoresearch needs somewhere to start". One section of the
[Agent Management Science results](../README.md); every path and command below is from this folder,
`harness-optimizers/`.*

> **Waiting for its logs.** This folder was made on 24 November 2026 so that the experiment has a place in the
> repo. Its logs, tables and code are not here yet, and nothing below has been checked against them. If the
> experiment is yours, the text in angle brackets is yours to replace, and the steps are under
> ["Putting your experiment in"](../README.md#putting-your-experiment-in) on the front page. Take this note out
> when the folder is filled.

Four harness optimizers each propose a long series of edits to an agent's harness. Every edit is classified by
which strategies it changes and by what it did to the score. <Which four optimizers, on which task, with which
model and settings.>

## Headline

<The numbers the post quotes, in one small table. Copy this table into your block on the top-level README.>

| | <optimizer 1> | <optimizer 2> | <optimizer 3> | <optimizer 4> | all four |
|---|---|---|---|---|---|
| edits proposed | | | | | |
| edits that change several strategies at once | | | | | |
| edits that scored better | | | | | |
| edits within noise | | | | | |
| edits that scored worse | | | | | |

**What the number means.** <What counts as a strategy, and who or what decided which strategies an edit changes.
What makes an edit "better" and not "within noise": how many evaluation runs are behind a score, and how wide the
noise is.>

**What it does not show.** <The caveats a reader needs before quoting it. The post says one of them itself:
bundled edits are the conditions for a false lesson, and nothing here shows that an optimizer learned one.>

## What is in this folder

```
results/      the tables above, as files, and the script that rebuilds them from the logs   (empty for now)
runs/         the raw logs: each optimizer's edits, with the score of each                  (empty for now)
<code>        the code that ran the optimizers, and the code that classified their edits
```

What the post takes from this experiment, and the file each should come from:

| in the post | file |
|---|---|
| The sentence that counts the four optimizers' edits and gives the share classified as changing several strategies at once | `results/<file>` |
| Figure 2, "Harness optimizers": the share of proposed edits that were better, and the share that were within noise | `results/<file>` |
| "Meta-Optimization" in the teaser under the TL;DR: the same shares, with the share that were worse | the same file as Figure 2 |

**Left out:** <what is not here and why (too large, can be made again, not ours to share), or "nothing">.

## Rebuilding the tables

    <the command that turns runs/ into results/, and what it needs (ideally no keys and no model calls). If a
    model classified the edits, keep its labels in results/ so that the tables rebuild without calling it again.>

## Running the experiment again

<What it needs: the operating system, the tools, which keys (read from the environment), and roughly what a full
run costs in money and time.>

    <the commands>
