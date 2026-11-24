# <Experiment name>

*Section of the post: "<the section's heading>". One section of the
[Agent Management Science results](../README.md); every path and command below is from this folder,
`<your-section>/`.*

<Two or three sentences: what was compared, on which tasks, with which model and settings.>

## Headline

<The numbers the post quotes, in one small table. Copy this table into your block on the top-level README.>

| | <arrangement A> | <arrangement B> |
|---|---|---|
| <what was measured> | | |

**What the number means.** <What counts as a success, who or what decides it, and how many runs are behind each
cell.>

**What it does not show.** <The caveats a reader needs before quoting it: one run a cell, one model, a
development set, and so on.>

## What is in this folder

```
results/      the tables above, as files, and the script that rebuilds them from the logs
runs/         the raw logs
<code>        the code that ran the experiment
```

Where each number in the post comes from:

| in the post | file |
|---|---|
| <Figure N, or the sentence> | `results/<file>` |

**Left out:** <what is not here and why (too large, can be made again, not ours to share), or "nothing">.

## Rebuilding the tables

    <the command that turns runs/ into results/, and what it needs (ideally no keys and no model calls)>

## Running the experiment again

<What it needs: the operating system, the tools, which keys (read from the environment), and roughly what a full
run costs in money and time.>

    <the commands>
