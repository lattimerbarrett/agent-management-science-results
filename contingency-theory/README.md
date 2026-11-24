# Contingency Theory: How should agent systems be organized?

*In the post: the case study of the same name, and its Figure 3, "Program reconstruction". One section of the
[Agent Management Science results](../README.md); every path and command below is from this folder,
`contingency-theory/`.*

The logs and result tables behind the case study. Ten agents, all one model, rebuild a program from its executable
and its documentation, in Python with the standard library only, and hidden tests score what they build. They do
this on 18 ProgramLab tasks, organized two ways: as one group of ten, and as two groups of five. The model is
GPT-6 Luna in the Codex harness at medium reasoning effort, and a run lasts 30 minutes.

## Headline

| 18 ProgramLab tasks | one group of ten | two groups of five |
|---|---|---|
| mean score | **0.405** | **0.367** |
| tasks on which it scored higher | **14 of 18** | **4 of 18** |
| its largest lead on a task | **13.1 points** (ttdl) | **6.5 points** (gitleaks) |

Neither arrangement led on every task.

**The two arrangements**

- **One group of ten.** All ten agents share one `main` branch and one channel to post in.
- **Two groups of five.** Each group has its own `main` and its own private channel, and cannot see the other
  group's `main`. All ten agents can also read and post in a public channel. The same five agents are in each
  group on every task.

In both, each agent works in its own sandbox, on its own git repository, and pushes to its group's `main`.

**What the number means.** A score is the fraction of a task's hidden tests passed by the code on a group's `main`
when time ran out, from 0 to 1. With two groups, the agents were told that the run's score is the higher of the
two groups' scores. The logs hold one score for a run, and not one for each group. A lead is the difference of two
scores in points: 0.496 against 0.365 is 13.1 points.

**How to read a cell.** Each score is one run. Every task was run once under each arrangement, 36 runs in all.

**What it does not show.**

- **One run a cell.** Nothing here measures how much a score moves from one run to the next, so a lead on a single
  task may be within that.
- **One model, one harness, one time limit.**
- **The two arrangements are not scored alike.** By the scoring rule the agents were given, two groups of five are
  scored on the better of their two programs, and one group of ten on its one program.
- **Why an arrangement led on a task.** The logs carry no measure of how a task's work divides. The post leaves
  that as the question to test.

## Task by task

| task in Figure 3 | task | one group of ten | two groups of five | difference, points |
|---|---|---|---|---|
| 1 | `vladimirmarkelov__ttdl.f0e6ecb` | 0.496 | 0.365 | +13.1 |
| 2 | `checkmarx__2ms.e2fafb4` | 0.483 | 0.378 | +10.5 |
| 3 | `boeing__config-file-validator.151f141` | 0.659 | 0.558 | +10.1 |
| 4 | `rtk-ai__rtk.39583cf` | 0.347 | 0.259 | +8.8 |
| 5 | `chaqchase__lla.5b6574f` | 0.397 | 0.310 | +8.7 |
| 6 | `tavianator__bfs.605e1f1` | 0.590 | 0.508 | +8.2 |
| 7 | `medialab__xan.792f400` | 0.397 | 0.352 | +4.5 |
| 8 | `twpayne__chezmoi.6458368` | 0.205 | 0.161 | +4.4 |
| 9 | `tdewolff__minify.98dea98` | 0.343 | 0.306 | +3.7 |
| 10 | `zizmorcore__zizmor.b50d8f6` | 0.269 | 0.235 | +3.4 |
| 11 | `ouch-org__ouch.d6e8063` | 0.429 | 0.409 | +2.0 |
| 12 | `temisu__ancient.91107f2` | 0.198 | 0.181 | +1.7 |
| 13 | `mitsuhiko__minijinja.571e28a` | 0.511 | 0.498 | +1.3 |
| 14 | `go-task__task.e92109f` | 0.455 | 0.443 | +1.2 |
| 15 | `tamasfe__taplo.20a9145` | 0.349 | 0.355 | -0.6 |
| 16 | `josephburnett__jd.e37eef0` | 0.522 | 0.541 | -1.9 |
| 17 | `tomwright__dasel.abc1e1d` | 0.263 | 0.306 | -4.3 |
| 18 | `gitleaks__gitleaks.83d9cd6` | 0.375 | 0.440 | -6.5 |
| | **mean of 18** | **0.405** | **0.367** | **+3.8** |

- **The first column is the task's number in Figure 3.** The figure orders the tasks from the largest lead of one
  group of ten to the largest lead of two groups of five. Its "Structure 1" is the one group of ten, and its
  "Structure 2" the two groups of five.
- **A task is named for the program's repository and commit**: `tamasfe__taplo.20a9145` is `tamasfe/taplo` at
  commit `20a9145`.

## The runs

| | one group of ten | two groups of five |
|---|---|---|
| runs | 18 | 18 |
| runs whose transcripts are here | 16 | 16 |
| agents in a run | 10 | 10 |
| minutes from a run's first record to its last: median (shortest to longest) | 30.6 (30.0 to 33.0) | 30.2 (30.1 to 45.7) |
| posts by agents in a group's channel | 3,828 | 3,762 |
| posts by agents in the public channel | no such channel | 218 |
| pushes to a group's `main` | 3,085 | 3,774 |

The last four rows are over the runs whose transcripts are here.

- **Four runs have only their score here**: both runs of `gitleaks__gitleaks` and both of `checkmarx__2ms`. Why
  is under [runs/](#runs) below.
- **The runs were made on 11 and 12 November 2026.**
- **In one run an agent worked past the limit.** In the two-group run of `boeing__config-file-validator`, nine
  agents stop after 30 minutes and one, `pale_lantern48`, goes on for 15 more. That is the 45.7 above.
- **Six of the 18 tasks are ProgramLab's hard ones and twelve its medium ones.** The logs do not say which.
- **The logs do not record the model or its reasoning effort.** Those are as stated by the archive the logs came
  in. One transcript prints its sandbox's environment, which gives the Codex version, 0.163.0.

## What is in this folder

```
results/      the tables above, as files, and the script that rebuilds them from the logs
runs/         the logs: the score of all 36 runs, and the transcripts of 32 of them (253 MB)
```

The code that ran the experiment is not here yet. See "Running the experiment again".

### results/

| file | what it holds |
|---|---|
| `tables.md` | the three tables above |
| `scores.csv` | a task a row: its score under each arrangement, the difference in points (one group of ten less two groups of five), and its number in Figure 3 |
| `runs.csv` | a run a row: its folder, its score, the minutes from its first record to its last, and its counts of transcript records, posts and pushes. All but the score are empty for the four runs whose transcripts are not here |
| `make_tables.py` | rebuilds all of the above from `runs/` |

Where each number in the post comes from:

| in the post | file |
|---|---|
| Figure 3, "Program reconstruction": the difference between the two arrangements on each of the 18 tasks | `results/scores.csv`: `difference_points`, in the order of `figure_task` |
| "Neither arrangement led on every task", in "Our experiment" and in Figure 3's caption | `results/scores.csv`: 14 differences above zero and 4 below |
| "Swarm Structure" in the teaser under the TL;DR, "up to +13%" | `results/scores.csv`: the largest lead, 13.1 points, on ttdl (0.496 against 0.365) |

### runs/

```
runs/<task>/1x10/     the run with one group of ten
runs/<task>/2x5/      the run with two groups of five
```

In a run's folder:

- `score.json`: the run's score.
- `posts.jsonl`: every post on the platform, in order, a post a line. A post is either something an agent posted
  (`"kind": "post"`) or the notice the platform posts for each push to a `main`
  (`"kind": "push (posted by the platform)"`), which names the commits.
- `agents/<agent>.jsonl`: one agent's transcript in time order, a record a line. Records with
  `"source": "codex"` are what the agent was told, its messages, its tool calls and their outputs. Records with
  `"source": "platform"` are the platform's notices to it of new posts.

**What the agents were told is at the top of every transcript.** The first record (its `role` is `developer`)
holds the rules, the scoring rule, how the platform works and how to work together. The third (`user`) holds the
task. Both are the same for every agent of an arrangement, apart from the names.

**The ten agents have the same names in every run.** With two groups, `group_0` is `brisk_harbor75`,
`early_island22`, `jolly_ember22`, `pale_kettle84` and `rapid_thistle87`, and `group_1` is `gentle_otter27`,
`pale_lantern48`, `sandy_walnut42`, `urban_comet97` and `zesty_lantern63`.

The logs' words for things differ from the post's:

| the post says | the logs say |
|---|---|
| one group of ten | `1x10` |
| two groups of five | `2x5` |
| all ten agents together | the swarm |
| a group's shared branch | `main`, on the remote `team` |

**Where the logs came from.** They are the archive `programlab_luna_2x5_1x10_traj.tar.gz` of
[xli04/ams-results](https://github.com/xli04/ams-results), unpacked. No file here is changed from the archive's.
The archive's own table of scores has the same numbers as `results/scores.csv`.

**Four runs have only their score here**: both runs of `gitleaks__gitleaks` and both of `checkmarx__2ms`. Those
two programs search files for leaked keys. So the transcripts and posts of their runs are full of strings shaped
like keys: test input that the agents wrote, and the examples in the two programs' own documentation. They are not
credentials, but GitHub's check for leaked keys cannot tell, and refuses a push that holds them. The transcripts
and posts of those four runs are in the archive.

**Written by agents.** The transcripts hold commands and code that agents wrote. Read them, and run them only
inside a sandbox.

**Not here:**

- **The transcripts and posts of the four runs above.** They are in the archive.
- **The tasks themselves**: the reference executables, their documentation and the hidden tests. They belong to
  [ProgramLab](https://programlab.blog/).
- **The agents' repositories.** A post points at a commit by its hash, and the commits are not here. What an agent
  wrote is in its transcript, in its tool calls.
- **A score for each of the two groups** in a two-group run, and which six tasks are the hard ones.

## Rebuilding the tables

    python3 results/make_tables.py

It needs Python 3.9 or later and nothing else: no packages, no keys and no model calls. It takes about a second.

## Running the experiment again

Not from this folder yet. The code that ran these runs is not here: the platform that carries the agents' posts
and pushes, the sandboxes, and the scoring against ProgramLab's hidden tests. What each agent was told, word for
word, is at the top of its transcript.
