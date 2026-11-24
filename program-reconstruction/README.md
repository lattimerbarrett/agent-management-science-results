# Program reconstruction

*Section of the post: "A team boundary keeps work from traveling". One section of the
[Agent Management Science results](../README.md); every path and command below is from this folder,
`program-reconstruction/`.*

> **Waiting for its logs.** This folder was made on 24 November 2026 so that the experiment has a place in the
> repo. Its logs, tables and code are not here yet, and nothing below has been checked against them. If the
> experiment is yours, the text in angle brackets is yours to replace, and the steps are under
> ["Putting your experiment in"](../README.md#putting-your-experiment-in) on the front page. Take this note out
> when the folder is filled.

Coding agents rebuild programs from their binaries and documentation, and hidden tests score what they build. The
model and the tasks stay fixed. What changes is how the agents are organized. <Which benchmark and which tasks,
which model and settings, the time limit, and how many runs each arrangement had.>

## Headline

<The numbers the post quotes, in one small table. Copy this table into your block on the top-level README.>

| hidden tests passed, 20 tasks | mean pass rate | against one team of five |
|---|---|---|
| the best of five separate attempts | | |
| one team of five | | |
| two groups of five with a channel in common | | |
| one group of ten | | |

**What the number means.** <What the pass rate is a share of. How the best of five separate attempts is picked,
before scoring or after. How many runs are behind each cell.>

**What it does not show.** <The caveats a reader needs before quoting it. The post says one of them itself: each
group was graded on its own branch, so both needed a working fix whether or not the other had one.>

## What is in this folder

```
results/      the tables above, as files, and the script that rebuilds them from the logs   (empty for now)
runs/         the raw logs: a folder for each comparison below, then a folder for each run   (empty for now)
<code>        the code that ran the experiment
```

The post draws on five comparisons. Each needs its logs in `runs/` and its numbers in a file under `results/`:

| comparison | in the post | file |
|---|---|---|
| A team of five against the best of five separate attempts, on 20 tasks | The section's first paragraph: on how many of the 20 tasks the team passed more tests | `results/<file>`, a task a row |
| Ten agents as one group, and as two groups of five with a channel in common, each against a single team of five | The second paragraph: the two score gains, the share of posts the two groups kept inside their own group, and the bugs both groups ran into (how many were fixed twice, how many were handled in the common channel) | `results/<file>` |
| Two structures on each of the 20 tasks | Figure 4, "Program reconstruction", and "Swarm Structure" in the teaser under the TL;DR | `results/<file>`, a task a row |
| Ten agents that organize themselves (Flat) against one agent directing three teams of three (Leader), on four tasks | The fold-out "A second comparison: flat teams against led teams" | `results/<file>` |
| A team of five with and without its message channel, on two models | "Where agents are not people": the change in the mean pass rate for each model, and the note committed to the shared repository | `results/<file>` |

If one of these was run on other tasks, another model or another harness than the rest, say so beside it. The
SQL warehouse fold-out in the same section of the post is a separate pilot and is not part of this folder.

**Left out:** <what is not here and why (too large, can be made again, not ours to share), or "nothing". The
benchmark's own programs and hidden tests are the likely case: if its terms don't allow copies, link to it.>

## Rebuilding the tables

    <the command that turns runs/ into results/, and what it needs (ideally no keys and no model calls)>

## Running the experiment again

<What it needs: the operating system, the tools, which keys (read from the environment), and roughly what a full
run costs in money and time.>

    <the commands>
