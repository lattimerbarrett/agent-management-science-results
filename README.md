# Agent Management Science: results

The data, logs and code behind the experiments in the post "Agent Management Science". Each experiment in the post
has one folder here, with what you need to check its numbers and to run it again.

## The experiments

The post has three case studies, then a prover. In the post's order:

| in the post | the experiment | folder | what is in it today |
|---|---|---|---|
| Case study "Groupthink: How should agents communicate?" (Figure 2) | peer reading, on MathArena problems | [`groupthink/`](groupthink/) | logs, result tables and code |
| Case study "Contingency Theory: How should agent systems be organized?" (Figure 3) | program reconstruction, on ProgramLab | [`contingency-theory/`](contingency-theory/) | logs and result tables |
| Case study "Superstitious Learning: How should agents learn from experience?" (Figure 4) | harness optimizers, on τ²-Bench | [`superstitious-learning/`](superstitious-learning/) | waiting for its logs |
| "AMS lets us build much better agentic systems" (Figure 5) | the prover, on ArXivMath: explore, then prove | [`prover/`](prover/) | logs, result tables and code |

A case study's folder is named for the case study. A folder that is waiting for its logs has a README that lists
what the post takes from the experiment, an empty `results/` and an empty `runs/`. Its numbers are not in this
repo yet.

## Results at a glance

One short block per experiment whose numbers are in, in the order the post has them. The detail is in each
folder's own README.

### Groupthink: how often agents read a peer's work · [`groupthink/`](groupthink/)

*In the post: the case study "Groupthink: How should agents communicate?" (Figure 2).* Eight Qwen3.5-9B agents
work on each of the first 25 problems of MathArena's Apex Shortlist, under three rules for how often an agent
reads the work of a randomly picked peer: never, after 1 step in 4, and after every step.

| share of agent pairs | without peer reading | with peer reading (a peer's file after every step) |
|---|---|---|
| gave the same wrong answer | **11.3%** (79 of 700) | **32.9%** (230 of 700) |
| gave the same right answer | **28.4%** (199 of 700) | **43.7%** (306 of 700) |

A pair is two of the eight agents on one problem. With a peer's file after 1 step in 4, the two rows are 25.3% and
32.4%. It is one run with one seed, and no control was run for the extra turns that reading takes. The table for
each reading rule, the 25 problems one by one, the logs of every model call and the code are in
[`groupthink/`](groupthink/).

### Contingency Theory: one group of ten, or two groups of five · [`contingency-theory/`](contingency-theory/)

*In the post: the case study "Contingency Theory: How should agent systems be organized?" (Figure 3).* Ten GPT-6
Luna agents in the Codex harness rebuild a program on each of 18 ProgramLab tasks, organized two ways.

| 18 ProgramLab tasks | one group of ten | two groups of five |
|---|---|---|
| mean score | **0.405** | **0.367** |
| tasks on which it scored higher | **14 of 18** | **4 of 18** |
| its largest lead on a task | **13.1 points** (ttdl) | **6.5 points** (gitleaks) |

A score is the fraction of a task's hidden tests passed, and each is one run. The task-by-task table, the score of
all 36 runs and the transcripts of 32 of them are in [`contingency-theory/`](contingency-theory/).

### Prover: explore, then prove · [`prover/`](prover/)

*Section of the post: "AMS lets us build much better agentic systems".* One model, GPT-6.1 Sol at medium reasoning
effort, is organized three ways and set research-level problems from MathArena's ArXivMath.

| problems solved | September, 9 problems | October, 14 problems |
|---|---|---|
| **Full system** (explore, then a team of four on each candidate answer) | **8 of 9** · median $12.28 a problem | **10 of 14** · median $27.13 a problem |
| **One team of four**, given only the problem | **5 of 9** · median $2.91 a problem | **8 of 14** · median $10.36 a problem |
| **Lone agent**, given only the problem | **3 of 9** on the first run · **4 of 9** by any of up to 8 runs · median $0.56 a run | **1 of 14** on the first run · **4 of 14** by any of up to 4 runs · median $0.47 a run |

"Solved" means the system stopped on a proof that a separate judge, a model, accepted, and its answer matches the
paper's. No person has checked the proofs. The problem-by-problem tables, the logs of every run and the code are
in [`prover/`](prover/).

## How the repo is laid out

```
README.md                 this page: every experiment, and the headline results of those whose numbers are in
_template/                a README to start a new section from
groupthink/               a section (a case study)
contingency-theory/       a section (a case study)
superstitious-learning/   a section (a case study), waiting for its logs
prover/                   a section
```

**A section is one folder, and it stands alone.** It has its own README, its own result tables, its own logs, and
its own code with its own list of what to install. Nothing is shared between sections. So a change in one section
can't break another, and a reader can take one folder and leave the rest.

Inside a section:

| | what goes there |
|---|---|
| `README.md` | The headline numbers first. Then what was run, what the numbers mean, what is in the folder and how to run it again. |
| `results/` | The numbers behind each figure and sentence in the post, as small files (CSV, JSON, Markdown), with the script that rebuilds them from the logs. |
| `runs/` or `data/` | The raw logs or data, as the code wrote them. |
| the code | Only what the experiment needs to run, with its own dependency file (`pyproject.toml`, `requirements.txt`, ...) inside the folder. |

`prover/` is laid out this way, if you want an example to copy from.

## Putting your experiment in

**If your experiment is in the table at the top of this page, its folder is already made.** Then:

1. **Put the raw logs in `runs/`**, as your code wrote them, and the code in the folder beside them, with its own
   dependency file.
2. **Put the numbers in `results/`**, as small files, with the script that rebuilds them from the logs. Your
   folder's README lists each figure and sentence of the post that needs a file.
3. **Fill in your folder's README.** The headline numbers go first: the ones the post quotes. Replace everything
   in angle brackets, and take out the "Waiting for its logs" note at the top.
4. **On this page, change your row in the table at the top and add a block to "Results at a glance"**: a heading
   that links to your folder, the section of the post it belongs to, and one small table or a few sentences. Keep
   everything else in your own README.
5. **Change only your own folder, and your own row and block on this page.** If something in another section
   looks wrong, tell whoever owns it.

**If it has no folder yet** (an experiment that joins the post later), make one first: a folder at the top level,
named for the case study or the experiment in lowercase words joined by hyphens, with a copy of
`_template/README.md` in it. Add a row for it to the table at the top, then carry on from step 1.

### Before you commit

- **No keys, tokens or passwords**, in code or in logs. Code reads its keys from the environment. Logs are where
  one slips in, so search yours before the first commit. This lists the files to look at:

      grep -rlE '(^|[^A-Za-z0-9_-])(sk-|hf_|ghp_|xox[abp]-)[A-Za-z0-9_-]{20,}' your-section/

- **Only what you may share.** If a dataset's terms don't allow copies of it, link to it and leave it out. Read
  through the logs for anything private.
- **No file over 50 MB.** GitHub refuses a file over 100 MB. Leave out caches, model weights and anything that
  can be made again, and say in your README what you left out (`prover/runs/OMITTED.tsv` is the prover's list).
- **No environments or caches**: `.venv/`, `node_modules/`, `__pycache__/`. The `.gitignore` here covers the common
  ones. Put a `.gitignore` in your own folder for anything else.
- **Every number in your README should be in a file under `results/`**, so a reader can trace it to the logs.

### Working on one section without downloading the others

The prover's logs are about 2 GB. To get only your own folder (here `groupthink`):

    git clone --filter=blob:none --sparse https://github.com/lattimerbarrett/agent-management-science-results.git
    cd agent-management-science-results
    git sparse-checkout set groupthink _template

The files at the top level, this page among them, always come along. A folder that isn't in the repo yet works too:
make it, add your files, then commit and push as usual.
