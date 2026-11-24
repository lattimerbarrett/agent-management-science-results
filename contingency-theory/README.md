# Contingency Theory: How should agent systems be organized?

*In the post: the case study of the same name, and its Figure 3, "Program reconstruction". One section of the
[Agent Management Science results](../README.md); every path and command below is from this folder,
`contingency-theory/`.*

> **Waiting for its logs.** This folder was made on 24 November 2026 so that the case study has a place in the
> repo. Its logs, tables and code are not here yet, and nothing below has been checked against them. If the
> experiment is yours, the text in angle brackets is yours to replace, and the steps are under
> ["Putting your experiment in"](../README.md#putting-your-experiment-in) on the front page. Take this note out
> when the folder is filled.

Ten GPT-6 Luna agents in the Codex harness work on 18 ProgramLab tasks, each of which is to rebuild a program.
The agents are organized two ways: as one group of ten, and as two groups of five. <The model's settings, the
time or budget limit, what the two groups of five share, how a task is scored, and how many runs each
arrangement had.>

## Headline

<The numbers the post quotes, in one small table. Copy this table into your block on the top-level README.>

| 18 ProgramLab tasks | one group of ten | two groups of five |
|---|---|---|
| mean score | | |
| tasks on which it scored higher | | |
| its largest lead on a task | | |

**What the number means.** <What a task's score is a share of, and how many runs are behind each one. Which
arrangement is the figure's Structure 1 and which is its Structure 2.>

**What it does not show.** <The caveats a reader needs before quoting it: one model, one harness, how many runs a
cell, and so on.>

## What is in this folder

```
results/      the tables above, as files, and the script that rebuilds them from the logs   (empty for now)
runs/         the raw logs: a folder for each arrangement, then a folder for each task       (empty for now)
<code>        the code that ran the experiment
```

What the post takes from this experiment, and the file each should come from:

| in the post | file |
|---|---|
| Figure 3, "Program reconstruction": the difference between the two arrangements on each of the 18 tasks | `results/<file>`, a task a row, with each arrangement's score |
| "Neither arrangement led on every task", in "Our experiment" and in Figure 3's caption | the same file |
| "Swarm Structure" in the teaser under the TL;DR: the largest gain from the better structure | the same file |

**Left out:** <what is not here and why (too large, can be made again, not ours to share), or "nothing". The
benchmark's own programs and tests are the likely case: if its terms don't allow copies, link to it.>

## Rebuilding the tables

    <the command that turns runs/ into results/, and what it needs (ideally no keys and no model calls)>

## Running the experiment again

<What it needs: the operating system, the tools, which keys (read from the environment), and roughly what a full
run costs in money and time.>

    <the commands>
