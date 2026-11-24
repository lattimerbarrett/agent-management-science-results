# Superstitious Learning: How should agents learn from experience?

*In the post: the case study of the same name, and its Figure 4, "Harness optimizers". One section of the
[Agent Management Science results](../README.md); every path and command below is from this folder,
`superstitious-learning/`.*

> **Waiting for its logs.** This folder was made on 24 November 2026 so that the case study has a place in the
> repo. Its logs, tables and code are not here yet, and nothing below has been checked against them. If the
> experiment is yours, the text in angle brackets is yours to replace, and the steps are under
> ["Putting your experiment in"](../README.md#putting-your-experiment-in) on the front page. Take this note out
> when the folder is filled.

Three harness optimizers, GEPA, MetaHarness and AdaEvolve, run meta-optimization on τ²-Bench. The candidates that
scored above their parents the first time are then evaluated again, to see how many keep the lead. <Which model
and settings, what a candidate is, and how the candidates to re-evaluate were chosen.>

## Headline

<The numbers the post quotes, in one small table. Copy this table into your block on the top-level README.>

| candidates that first scored above their parent | GEPA | MetaHarness | AdaEvolve | all three |
|---|---|---|---|---|
| re-evaluated | | | | |
| kept an advantage of at least one standard error | | | | |
| within noise of the parent | | | | |
| scored below the parent | | | | |

**What the number means.** <What a candidate and its parent are. How many evaluation runs are behind the first
score and behind the re-evaluation, and how the standard error is worked out. Where "better" ends and "noisy"
begins.>

**What it does not show.** <The caveats a reader needs before quoting it: one benchmark, one model, which
candidates were left out, and so on.>

## What is in this folder

```
results/      the tables above, as files, and the script that rebuilds them from the logs       (empty for now)
runs/         the raw logs: each optimizer's run, and every evaluation of a candidate and its parent   (empty for now)
<code>        the code that ran the optimizers, and the code that re-evaluated their candidates
```

What the post takes from this experiment, and the file each should come from:

| in the post | file |
|---|---|
| "Our experiment": how many candidates were re-evaluated, and how many kept an advantage of at least one standard error over their parents | `results/<file>`, a candidate a row |
| Figure 4, "Harness optimizers": the share of proposed edits that were better, and the share that were noisy | the same file |
| "Meta-Optimization" in the teaser under the TL;DR: the share of noisy edits | the same file |

**Left out:** <what is not here and why (too large, can be made again, not ours to share), or "nothing".>

## Rebuilding the tables

    <the command that turns runs/ into results/, and what it needs (ideally no keys and no model calls)>

## Running the experiment again

<What it needs: the operating system, the tools, which keys (read from the environment), and roughly what a full
run costs in money and time.>

    <the commands>
