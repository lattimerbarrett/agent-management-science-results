<!-- Written by results/make_tables.py from the logs in runs/. Change the script, not this file. -->

## Headline

| share of agent pairs | without peer reading | with peer reading (a peer's file after every step) |
|---|---|---|
| gave the same wrong answer | **11.3%** (79 of 700) | **32.9%** (230 of 700) |
| gave the same right answer | **28.4%** (199 of 700) | **43.7%** (306 of 700) |

## By how often an agent reads

| 25 problems, 8 agents a problem | no peer reading | a peer's file after 1 step in 4 | a peer's file after every step |
|---|---|---|---|
| after one of its steps, an agent reads a peer's file | never | with a chance of 1 in 4 | every time |
| files read, by how many of the agents | none | 467, by 172 | 1,497, by 200 |
| **pairs: both right** | 28.4% (199) | 32.4% (227) | 43.7% (306) |
| **pairs: the same wrong answer** | 11.3% (79) | 25.3% (177) | 32.9% (230) |
| pairs: two different wrong answers | 28.1% (197) | 23.7% (166) | 10.9% (76) |
| pairs: one right, one wrong | 13.4% (94) | 13.4% (94) | 12.6% (88) |
| pairs: one or both with no answer | 18.7% (131) | 5.1% (36) | 0.0% (0) |
| agents that ended right | 37.5% (75) | 40.0% (80) | 50.0% (100) |
| agents that ended on a wrong answer | 51.0% (102) | 57.0% (114) | 50.0% (100) |
| agents that ended with no answer | 11.5% (23) | 3.0% (6) | 0.0% (0) |

A percent of pairs is of a problem's 28 pairs, averaged over the 25 problems, and the count beside it is of all 700 pairs. A percent of agents is of a problem's 8 agents, averaged over the problems, and the count is of all 200 agents.

## Against no peer reading, problem by problem

| the rise in a problem's pairs, in points | a peer's file after 1 step in 4 | a peer's file after every step |
|---|---|---|
| pairs: the same wrong answer | +14.0 (+5.6 to +23.9) | +21.6 (+9.3 to +34.9) |
| pairs: both right | +4.0 (+0.1 to +8.3) | +15.3 (+5.0 to +27.1) |
| problems on which the pairs on the same wrong answer rose, stayed, fell | 13, 10, 2 | 11, 10, 4 |

In brackets, a 95% interval over the 25 problems (the problems drawn again with replacement, 10,000 times).

With a peer's file after every step, the six largest rises in the pairs on the same wrong answer (problems 11, 13, 10, 6, 5, 17) are 17.4 of the 21.6 points.

## Problem by problem

For each problem, three numbers in the order of the columns above: no peer reading, a peer's file after 1 step in 4, a peer's file after every step.

| problem | known answer | agents right, of 8 | pairs on the same wrong answer, of 28 | agents on the most-held wrong answer |
|---|---|---|---|---|
| 1 | `171` | 0, 0, 0 | 4, 10, 11 | 3, 5, 5 |
| 2 | `89` | 0, 3, 6 | 0, 0, 0 | 1, 1, 1 |
| 3 | `63` | 8, 8, 8 | 0, 0, 0 | 0, 0, 0 |
| 4 | `2618` | 8, 8, 8 | 0, 0, 0 | 0, 0, 0 |
| 5 | `8096` | 3, 3, 0 | 1, 3, 16 | 2, 3, 6 |
| 6 | `2077992225` | 0, 0, 0 | 10, 6, 28 | 5, 4, 8 |
| 7 | `1030219` | 2, 4, 7 | 0, 0, 0 | 1, 1, 1 |
| 8 | `n-1` | 2, 0, 3 | 1, 8, 1 | 2, 4, 2 |
| 9 | `2^{20} - 1` | 7, 8, 8 | 0, 0, 0 | 1, 0, 0 |
| 10 | `59` | 0, 0, 0 | 6, 28, 28 | 4, 8, 8 |
| 11 | `325` | 1, 0, 0 | 1, 21, 28 | 2, 7, 8 |
| 12 | `n(n-1)/2` | 6, 5, 4 | 0, 0, 3 | 1, 1, 3 |
| 13 | `2^{21} - 2` | 2, 1, 0 | 3, 21, 28 | 3, 7, 8 |
| 14 | `2n(n-1)` | 0, 0, 0 | 3, 7, 11 | 3, 4, 5 |
| 15 | `505` | 4, 4, 8 | 0, 3, 0 | 1, 3, 0 |
| 16 | `495` | 0, 0, 0 | 3, 4, 13 | 3, 3, 5 |
| 17 | `4` | 0, 0, 0 | 13, 21, 28 | 5, 7, 8 |
| 18 | `24` | 8, 8, 8 | 0, 0, 0 | 0, 0, 0 |
| 19 | `74` | 8, 8, 8 | 0, 0, 0 | 0, 0, 0 |
| 20 | `1520` | 7, 8, 8 | 0, 0, 0 | 0, 0, 0 |
| 21 | `333400` | 0, 0, 5 | 6, 6, 1 | 3, 3, 2 |
| 22 | `12` | 0, 0, 0 | 15, 21, 28 | 6, 7, 8 |
| 23 | `2023` | 0, 0, 4 | 11, 15, 6 | 5, 6, 4 |
| 24 | `281` | 6, 7, 7 | 1, 0, 0 | 2, 1, 1 |
| 25 | `60` | 3, 5, 8 | 1, 3, 0 | 2, 3, 0 |

## The run

| | |
|---|---|
| model | `Qwen/Qwen3.5-9B@c202236235762e1c871ad0ccb60c8ee5ba337b9a` |
| served by | vllm 0.31.0, as `9B-bf16`, on one NVIDIA H100 PCIe |
| started, finished | 2026-10-13 06:12:42, 2026-10-13 10:46:13 |
| problems | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25 of `apex_shortlist` |
| seed | 0 |
| agents a problem | 8 |
| steps an agent has | 20 |
| tokens of thought a step, at most | 1,024 |
| tokens of reply a step, at most | 5,760 |
| lines a file may have | 300 |
| how a reply is drawn | temperature 0.6, top-k 20, top-p 0.95 (a thought: temperature 1.0, presence penalty 1.5) |
| model calls | 2,613, 3,130, 4,228 |
| tokens the model wrote | 4,357,300, 4,592,226, 4,982,091 |
| commit of the code | `23266ab7188a`, with nothing uncommitted |

The three arms have the same settings but for who reads. Where a row has three numbers, they are in the order: no peer reading, a peer's file after 1 step in 4, a peer's file after every step.
