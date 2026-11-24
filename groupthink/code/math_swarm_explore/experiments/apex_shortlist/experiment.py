"""How far do agents get on MathArena's Apex Shortlist, a set of hard problems that somebody else picked: alone,
reading each other's files now and then, and reading one after every step?

`hard_set` makes a set of hard problems out of AIME by what this lab's own agents got wrong. The Apex Shortlist
is a set that was picked elsewhere and for other models: 47 problems with a final answer from competitions of
2025, on which the strongest models of the time were right about half the time (MathArena; data/README.md).
The trial asked whether the GPU's model gets anywhere on it alone: a set on which nobody is ever right says as
little about agreement and correctness as one on which everybody is. It does (27.9% of a problem's agents
right, and on 8 problems most of the eight on one wrong answer), so the swarms are played on it.

    lab run apex_shortlist --dry-run --problems 2
    lab show apex_shortlist/trial --list                   # problem by problem: how many of the eight are right

Three arms (Barrett, 2026-10-13: "baseline, random talking, and random full talking ... don't do the controls,
just the baseline"), eight agents a problem, and then thirty-two (`--agents 32`): the baseline, the swarm that
reads one time in four (`random_looks`' own) and the swarm that reads after every step (`every_step`'s own).
As an arm stands that is 20 steps and a file of up to 300 lines in a reply of up to 5,760 tokens, and a reader
is shown the whole of a file. **Neither control is here**: what the swarms add over the baseline is contact
and the extra turns together. The trial was made before, alone, with 20 steps, 200 lines and 3,840 tokens,
which `reproduce.sh` gives it by name (`--arms desk --steps 20 --lines 200 --max-tokens 3840`).
"""
from mathswarm import Arm, RandomLooks

# All 47, the only split there is. MathArena's file calls it `train`; here it is `test`, as its AIME sets are.
BENCHMARKS = ["apex_shortlist"]
SPLIT = "test"
PROBLEMS = None

DESK = Arm("desk", agents=8)

ARMS = [
    DESK,
    DESK.but("look_at_others", looks=RandomLooks()),                 # after a step, one time in four
    DESK.but("always_look_at_others", looks=RandomLooks(p=1.0)),     # after every step
]
