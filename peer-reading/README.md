# Peer reading

*Section of the post: "Reading a peer spreads right answers and wrong ones". One section of the
[Agent Management Science results](../README.md); every path and command below is from this folder,
`peer-reading/`.*

> **Waiting for its logs.** This folder was made on 24 November 2026 so that the experiment has a place in the
> repo. Its logs, tables and code are not here yet, and nothing below has been checked against them. If the
> experiment is yours, the text in angle brackets is yours to replace, and the steps are under
> ["Putting your experiment in"](../README.md#putting-your-experiment-in) on the front page. Take this note out
> when the folder is filled.

Copies of one small open model work on 25 competition math problems. One rule changes from run to run: how often
an agent may read the work of a randomly chosen peer. <Which model and settings, which 25 problems, how many
agents in a team and how many turns each.>

## Headline

<The numbers the post quotes, in one small table. Copy this table into your block on the top-level README.>

| share of agent pairs | no reading | reading on some turns | reading every turn |
|---|---|---|---|
| both right | | | |
| gave the same wrong answer | | | |
| both wrong in any way | | | |
| a missing answer | | | |

**What the number means.** <What a pair is and how many pairs are behind each cell. What counts as the same
answer, and who or what decides an answer is right. How many runs each schedule had.>

**What it does not show.** <The caveats a reader needs before quoting it. The post says two of them itself: each
agent is in several pairs, so the pairs are not independent counts, and the pair rates do not say what a vote or
a verifier would have picked.>

## What is in this folder

```
results/      the tables above, as files, and the script that rebuilds them from the logs   (empty for now)
runs/         the raw logs: each agent's transcript and final answer, and who read whom     (empty for now)
<code>        the code that ran the experiment
```

What the post takes from this experiment, and the file each should come from:

| in the post | file |
|---|---|
| Figure 3, "Peer-reading experiment": the share of agent pairs that were both right, and the share that gave the same wrong answer, with and without reading | `results/<file>` |
| Figure 3's caption: the share of pairs with a missing answer, with and without reading | `results/<file>` |
| The paragraph under Figure 3: the share of pairs that were both wrong in any way, and the share of agents that answered correctly | `results/<file>` |
| Problem 5, and Table 1 in the fold-out under it: the eight final answers under each of the three reading schedules | `results/<file>` |
| "Where agents are not people": the share of pairs that gave the same wrong answer before any contact | the same file as Figure 3 |
| The reanalysis of the estimation data of Lorenz and colleagues: how often two people landed on the same wrong number, in private and when they could see each other's estimates | `results/<file>`, with the script that makes it |

The Lorenz data is a published dataset and not ours. If its terms allow a copy, it goes in `data/`. If they
don't, link to it and say here how to fetch it.

**Left out:** <what is not here and why (too large, can be made again, not ours to share), or "nothing">.

## Rebuilding the tables

    <the command that turns runs/ into results/, and what it needs (ideally no keys and no model calls)>

## Running the experiment again

<What it needs: the operating system, the tools, where the model comes from and what it runs on, which keys (read
from the environment), and roughly what a full run costs in money and time.>

    <the commands>
