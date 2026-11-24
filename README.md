# Prover results for "Agent Management Science"

The logs, result tables and code behind the prover experiments in the post. One model, GPT-6.1 Sol at medium
reasoning effort, is organized three ways and set research-level problems from MathArena's ArXivMath: nine from the
September 2026 edition and fourteen from October's.

## Headline

| problems solved | September, 9 problems | October, 14 problems |
|---|---|---|
| **Full system** (explore, then a team of four on each candidate answer) | **8 of 9** · $23.30 a problem | **10 of 14** · $40.52 a problem |
| **One team of four**, given only the problem | **5 of 9** · $7.98 a problem | **8 of 14** · $14.69 a problem |
| **Lone agent**, given only the problem | **3 of 9** on the first run · **4 of 9** by any of up to 8 runs | **1 of 14** on the first run · **4 of 14** by any of up to 4 runs |

On all 47 October problems, one lone agent each solved **34 of 47** ($23.11 in all).

**The three arrangements**

- **Lone agent.** One agent with a Python sandbox, asked to find the answer and prove it.
- **One team of four.** Four agents with the same task, a shared message board and a shared folder.
- **Full system.** Explorer agents branch on their own doubts and propose answers. Each new answer goes to a
  fresh team of four that is told the answer and asked to prove it. The first accepted proof ends the run.

**What "solved" means.** Both of these hold:

1. **The system stopped on a proof.** Its answer is a definite result, and a separate judge (the same model, at
   high effort) read the whole record, reran the code and found the proof sound, with no gap the agents
   themselves had admitted.
2. **The answer is right.** It matches the paper's answer, which nothing inside the system sees.

The judge is a model. No person has checked these proofs.

**How to read a cell.** Each cell is one run, except the lone agent's, which says how many of its runs solved the
problem. Where the full system ran a problem more than once, the table has its latest run. Cost is what the run
spent on the model.

## September, problem by problem

| problem | lone agent, runs solved | one team of four | full system | team handed the answer |
|---|---|---|---|---|
| p1 | 0 of 8 | **solved** · $37.46 | not solved · $89.19 | not solved · $50.04 |
| p9 | 0 of 8 | **solved** · $10.43 | **solved** · $5.33 | **solved** · $2.89 |
| p12 | 0 of 8 | not solved · $11.57 | **solved** · $9.87 | **solved** · $5.80 |
| p25 | 8 of 8 | **solved** · $2.20 | **solved** · $12.28 | **solved** · $0.89 |
| p30 | 7 of 8 | **solved** · $0.89 | **solved** · $2.91 | **solved** · $0.82 |
| p37 | 6 of 8 | **solved** · $2.91 | **solved** · $12.87 | **solved** · $1.83 |
| p41 | 0 of 8 | not solved · $4.85 | **solved** · $50.64 | **solved** · $11.04 |
| p43 | 0 of 8 | not solved · $0.88 | **solved** · $16.05 | **solved** · $2.98 |
| p48 | 1 of 8 | not solved · $0.62 | **solved** · $10.57 | **solved** · $2.02 |
| **9 problems** | **4 of 9** by any run (3 of 9 on the first run; 22 of 72 runs) · $52.15 | **5 of 9** · $71.81 | **8 of 9** · $209.72 | 8 of 9 · $78.32 |

- **These nine are the development set.** The prompts and the stopping rule were built while looking at them.
- **The last column is a diagnostic, not a baseline.** A team of four was told the paper's answer and asked only
  to prove it.
- **Four of the full-system runs (p12, p41, p43, p48) are from 4 to 6 November, before the judge above was the
  stopping rule.** An earlier judge, a model reading the team's report, accepted the proofs of p12, p41 and p48.
  It turned down p43's. The judge above read the saved records of p12, p43 and p48 afterwards and accepted all
  three, and p43 is counted on that reading. Those readings are in `runs/stopbench/`.

## October, problem by problem

| problem | lone agent, runs solved | one team of four | full system |
|---|---|---|---|
| p11 | 0 of 4 | **solved** · $7.06 | not solved · $83.89 |
| p13 | 0 of 4 | **solved** · $32.29 | **solved** · $77.77 |
| p15 | 1 of 4 | **solved** · $21.99 | **solved** · $8.45 |
| p22 | 0 of 4 | **solved** · $7.73 | **solved** · $12.59 |
| p24 | 1 of 4 | **solved** · $1.05 | **solved** · $2.64 |
| p28 | 0 of 4 | not solved · $2.03 | **solved** · $12.43 |
| p29 | 0 of 4 | not solved · $13.54 | not solved · $65.35 |
| p33 | 0 of 4 | not solved · $50.69 | **solved** · $27.13 |
| p38 | 1 of 1 | **solved** · $2.27 | **solved** · $27.14 |
| p39 | 0 of 4 | not solved · $11.62 | not solved · $56.33 |
| p40 | 0 of 4 | **solved** · $19.58 | not solved · $36.90 |
| p41 | 0 of 4 | not solved · $25.88 | **solved** · $138.62 |
| p42 | 1 of 4 | not solved · $0.89 | **solved** · $4.34 |
| p45 | 0 of 4 | **solved** · $9.10 | **solved** · $13.69 |
| **14 problems** | **4 of 14** by any run (1 of 14 on the first run; 4 of 53 runs) · $36.94 | **8 of 14** · $205.73 | **10 of 14** · $567.26 |

- **The fourteen were picked by the lone agent.** They are the 13 October problems that one lone agent did not
  solve, plus p38. So its "1 of 14 on the first run" is how the list was made, not a measurement.
- **Each of the two team arrangements solved problems the other did not.** The full system solved p28, p33, p41
  and p42, which the single team missed. The single team solved p11 and p40, which the full system missed.
- **Stops on a wrong answer** (the judge accepted a proof of an answer that is not the paper's) are the rows of
  `results/runs.csv` with `stop` true and `solved` false. All 13 are lone-agent runs. The 10 in October each
  answered with the question restated as a calculation left to be carried out. The 3 in September are p43
  twice, on 3 where the answer is 2, and p37 once, on a restated question.

## Budgets

| | September | October |
|---|---|---|
| lone agent, a run | $50 | $5 |
| one team of four | $50 | $50 |
| full system, the whole search | $100 to $120 | $100 to $170 |
| full system, each proof team | $12 to $20 | $20 to $40 |
| team handed the answer | $40 to $50 | not run |

## What is in this repo

```
results/      the tables above, as files, and the script that rebuilds them from the logs
runs/         the logs: 190 lone-agent, team and told-team runs, and 24 full-system runs (2 GB)
*.py          the code that ran them
explorer/     the server that runs the systems, and its two pages
```

### results/

| file | what it holds |
|---|---|
| `tables.md` | the three tables above |
| `runs.csv` | every lone-agent, team and told-team run, a run a row: its folder, cost, answer, the judge's verdict, right or not, solved or not |
| `full_system.csv` | the full system, a problem a row: its folder, cost, minutes, explorers, proof teams, the proof it stopped on |
| `full_system_teams.csv` | every proof team the full system started, a team a row: the answer it was told, right or not, what came of it |
| `runs.json` | which run folders belong to which month and arrangement |
| `archive_grades.json` | each answer a full-system team was told, graded against the paper's answer (`by`: the grader model, or by hand) |
| `make_tables.py` | rebuilds all of the above from `runs/`: `python results/make_tables.py` (no keys, no model calls) |

### runs/

The folders keep the names the code gave them, so the code can replay them. The code's words for things differ
from the post's:

| the post says | the code and the folders say |
|---|---|
| the full system | the prover archive: `runs/archive/<time>-p<N>/` |
| an explorer | a node: `nodes/n0`, `nodes/n1`, ... inside an archive |
| a proof team inside the full system | an experiment: `e1`, `e2`, ... inside an archive |
| a team of four | a swarm: `runs/basin/swarm/<time>-p<N>/` |
| given only the problem | not told, untold |
| a lone agent | solo; its folder is a swarm's, with one agent |
| a reminder to keep working | a nudge |
| the judge | the verifier |
| counterfactual verbalized sampling | CFVS, or EVS (`evs.py`, `evs.md`) |

An October problem's number has 1000 added in folder names: `p1041` is October's p41.

| folder | what it holds |
|---|---|
| `runs/basin/swarm/<time>-p<N>/` | one lone-agent run, team run or told-team run |
| `runs/basin/untold/<sweep>/` | a batch of lone-agent or team runs: which runs it started (`sweep.json`) and its table as written at the time (`summary.md`) |
| `runs/archive/<time>-p<N>/` | one full-system run |
| `runs/stopbench/results/verify/` | the judge's later reading of the 4 November full-system proof teams, and of the told teams |
| `runs/OMITTED.tsv` | the files that were left out, with their sizes |

September's p41 is two folders: `20261104-221825-p41`, and `20261106-112838-p41-rerun-e6e7`, which carries on from
the first one's saved state and holds the proof.

**In a lone-agent or team folder:**

- `settings.json`: problem, number of agents, budget, model, limits.
- `system.txt`, `prompt.txt`: the system prompt and the first message as sent.
- `slack.jsonl`: the message board, a message a line. For a lone agent, what it wrote each time it stopped.
- `agents/<name>/conversation.json`: that agent's whole transcript, and the files it wrote.
- `workspace/`: the team's shared files, proofs and checking scripts among them.
- `events.jsonl`: everything that happened, in order. `summary.json`: why the run ended and what it cost.
- `reading.json`: the outcome, written when the run ended: the answer, the judge's verdict, the grade, `solved`.
- `verify/`: the judge's own transcript.

**In a full-system folder:**

- `settings.json`, `prompts.json`: its settings and every prompt as used.
- `state.json`: what it spent, how it ended, every explorer (`nodes`) and every proof team (`experiments`), each
  with the answer it was told, the report on it and the judge's verdict (`verify`).
- `nodes/<id>/`: an explorer's transcript, the options it wrote (`cfvs.jsonl`) and its files.
- `e<i>/`: a proof team's folder, laid out as a team run's is.
- `calls.jsonl`: every judging call, with its prompt and reply.

**Left out, to keep the repo small:** files an agent wrote that are over 1 MB (over 5 MB for text), which are
caches and solver dumps; the sandbox's home folders; `slack.db`, whose content is in `slack.jsonl`; and links
between folders. Every transcript, message board and verdict is here. Files under `workspace/`, `agents/` and
`nodes/` were written by agents: read them, and run them only inside the sandbox.

### The code

It is the research code, cut down to what these three arrangements use. A few small helpers that lived in
unrelated modules were moved into `replies.py`, `evs.py`, `swarm_untold.py` and `streamed.py`, and the server
lost a page that these runs did not use. Two things read differently: the nine September statements come straight
from the dataset (before, from a saved copy of it), and the model's name and effort are written in
`swarm_play.py` (before, read from an earlier run's settings). The prompts, first messages and tool definitions
that the cut-down code builds were compared with the original's on all 23 problems, and they are the same.

| file | what it does |
|---|---|
| `swarm_untold.py` | runs and reads the two baselines: lone agents (`--solo`) and one team of four |
| `archive_sweep.py` | runs the full system on a list of problems |
| `explorer/serve.py` | the server that runs everything, with a page for teams (`swarm.html`) and one for the full system (`archive.html`) |
| `explorer/prover_archive.py` | the full system: explorers, the judge of new answers, proof teams, the stopping rule |
| `explorer/swarm_play.py` | a team or a lone agent: prompts, the message board, reminders, compaction |
| `verifier.py` | the judge: is the answer a definite result, and is the proof sound |
| `evs.py`, `evs.md` | counterfactual verbalized sampling: the question that gives an explorer its options |
| `grading.py` | the outside grade of an answer against the paper's |
| `benchmark.py` | the problems, from `MathArena/arxivmath-0926` and `MathArena/arxivmath-1026` |
| `sandbox.py`, `scratchpad.py`, `slack.py`, `toolkit.py`, `tools*.yaml` | the agents' tools: a Python sandbox and the message board |
| `llm.py`, `replies.py`, `explorer/streamed.py` | calls to the model |

## Looking at a run

Open its folder (the `folder` column of `results/runs.csv` and `results/full_system.csv`), or replay it in the
browser:

    uv sync
    ./setup_sandbox.sh
    OPENAI_API_KEY=... uv run python explorer/serve.py

then open http://127.0.0.1:8765/archive.html or http://127.0.0.1:8765/swarm.html. The sidebar lists every saved
run. The viewer is the server that runs experiments, so it wants the sandbox built and a key set even to look.
Nothing is spent until you start a run.

## Running the experiments

Needs macOS (the sandbox uses `sandbox-exec`), [uv](https://docs.astral.sh/uv/) and an OpenAI key.
`./setup_sandbox.sh` builds the Python that agents' code runs in, about 2 GB. Start the server as above and leave
it running. Then, in another terminal:

    # lone agents: the nine September problems, 8 runs each at $50; then all 47 October problems, one run each at $5
    uv run python swarm_untold.py start --solo --name my-lone
    uv run python swarm_untold.py start --solo --edition 10 --copies 1 --budget 5 --name my-lone-october

    # one team of four, $50 a team: the nine, then the October list
    uv run python swarm_untold.py start --name my-teams
    uv run python swarm_untold.py start --october --name my-teams-october

    # the full system: the nine, then the October list
    uv run python archive_sweep.py start --problems 1 9 12 25 30 37 41 43 48 --budget 100 --exp-budget 18 --name my-full
    uv run python archive_sweep.py start --october --budget 100 --exp-budget 20 --name my-full-october

Give each batch a new `--name`: a name that is already in `runs/` carries that batch on. Each command waits for
its runs, reads them as they end and prints its table. These spend real money, up to the budgets shown. A team
handed the answer is started from the swarm page.
