# Groupthink: How should agents communicate?

*In the post: the case study of the same name, and its Figure 2, "Peer-reading experiment". One section of the
[Agent Management Science results](../README.md); every path and command below is from this folder,
`groupthink/`.*

> **Waiting for its logs.** This folder was made on 24 November 2026 so that the case study has a place in the
> repo. Its logs, tables and code are not here yet, and nothing below has been checked against them. If the
> experiment is yours, the text in angle brackets is yours to replace, and the steps are under
> ["Putting your experiment in"](../README.md#putting-your-experiment-in) on the front page. Take this note out
> when the folder is filled.

Teams of eight agents, each the Qwen3.5-9B model, work on the first 25 problems of MathArena's Apex Shortlist. One
rule changes from run to run: how often an agent can read the work of a randomly selected peer. <The model's
settings, how many turns an agent has, which reading frequencies were run, and how many runs each had.>

## Headline

<The numbers the post quotes, in one small table. Copy this table into your block on the top-level README.>

| share of agent pairs | without peer reading | with peer reading |
|---|---|---|
| gave the same wrong answer | | |
| gave the same right answer | | |

**What the number means.** <What a pair is and how many pairs are behind each cell. What counts as the same
answer, and who or what decides an answer is right. Which reading frequency "with peer reading" stands for.>

**What it does not show.** <The caveats a reader needs before quoting it: one model, one set of problems, how
many runs a cell, and that an agent is in several pairs, so the pairs are not independent counts.>

## What is in this folder

```
results/      the tables above, as files, and the script that rebuilds them from the logs   (empty for now)
runs/         the raw logs: each agent's transcript and final answer, and who read whom     (empty for now)
<code>        the code that ran the experiment
```

What the post takes from this experiment, and the file each should come from:

| in the post | file |
|---|---|
| Figure 2, "Peer-reading experiment", and the last sentence of "Our experiment": the share of agent pairs that gave the same wrong answer, without and with peer reading | `results/<file>` |
| "More frequent peer reading increased convergence on both correct and incorrect answers": the share of pairs that agreed on a right answer, and on a wrong one, at each reading frequency | `results/<file>` |

**Left out:** <what is not here and why (too large, can be made again, not ours to share), or "nothing">.

## Rebuilding the tables

    <the command that turns runs/ into results/, and what it needs (ideally no keys and no model calls)>

## Running the experiment again

<What it needs: the operating system, the tools, where the model comes from and what it runs on, which keys (read
from the environment), and roughly what a full run costs in money and time.>

    <the commands>
