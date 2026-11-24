#!/bin/bash
# apex_shortlist: agents alone, eight a problem, on the 47 problems of MathArena's Apex Shortlist, with twenty steps
# and files of up to 200 lines, with `9B-bf16` on a rented H100.
# The trial was made on 2026-10-12 with the arm set so in `experiment.py`; an arm has 300 lines since (and 20 steps, as the trial had), so
# its settings are given here by name. It was also made under the harness before `634021f6f24b`: made again, it is
# told other words at a cut-off and before its last step, and it is another run.
# IT BILLS: a machine at $3.29 an hour. On 2026-10-12 the trial cost $6.58 (2.0 hours: 8.20 million tokens in
# 103 minutes, and a quarter of an hour for the machine to come up). This hands the job in and returns: the
# controller's machine looks after it. A job of a name that is there already is refused, so running this twice
# rents nothing twice.
set -euo pipefail
cd "$(dirname "$0")/../.."
uv run lab data
uv run lab cloud run "lab run apex_shortlist --name trial --arms desk --steps 20 --lines 200 --max-tokens 3840 --open 48" --gpu gpu_1x_h100_pcie --max-hours 8 --name apex-shortlist-trial

# When `uv run lab cloud status apex-shortlist-trial` says the job is done:
#   uv run lab cloud pull apex-shortlist-trial
#   uv run lab show apex_shortlist/trial --list       # problem by problem
#   uv run lab show apex_shortlist/trial --more       # agents right after each step, what they did, the cost

# The main run (2026-10-13): the three arms as they stand (20 steps, files of up to 300 lines), eight agents a
# problem, on the set's problems 1 to 25. All 47 were handed in first (job `apex-shortlist-main`, estimated at
# $27 to $36) and stopped by Barrett for the cost while the machine was being set up ($0.80 by the time the machine was gone, nothing played).
# One job and one machine, the arms in order, so that a later arm recalls what its agents share with an
# earlier one; each arm with as many agents at work as its conversations leave room for.
# IT BILLS: estimated at 4.5 to 6 hours of an H100, $15 to $20, before it ran; it took 4.7 hours and $15.58.
ONLY="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25"
uv run lab cloud run \
  "lab run apex_shortlist --name main --arms desk --only $ONLY --open 40" \
  "lab run apex_shortlist --name main --arms desk look_at_others --only $ONLY --open 32" \
  "lab run apex_shortlist --name main --only $ONLY --open 16" \
  --gpu gpu_1x_h100_pcie --max-hours 14 --name apex-shortlist-main-25

# When `uv run lab cloud status apex-shortlist-main-25` says the job is done:
#   uv run lab cloud pull apex-shortlist-main-25
#   uv run lab show apex_shortlist/main --list
#   uv run lab show apex_shortlist/main --more

# The same with thirty-two agents a problem (2026-10-13, `runs/main_32`), handed in when the run of eight had
# been pulled: the same 25 problems, seed and arms, so its first eight agents alone are the run of eight's,
# recalled from the controller's cache (and with contact they are those until each first reads a file).
# How many agents are at work at once is set by how long conversations got in the run of eight (23,456, 27,177
# and 37,110 tokens at their longest on average), kept under what an H100 held in `gpu_50`: 72 alone (64 of
# them new), 64 reading one time in four, 48 reading after every step.
# IT BILLS: estimated at 12 to 15 hours of an H100, $40 to $50, before it ran, from the run of eight's own
# timings (38.8 million tokens to write). `--max-hours 24` stops it at $79 whatever happens.
uv run lab cloud run \
  "lab run apex_shortlist --name main_32 --agents 32 --arms desk --only $ONLY --open 72" \
  "lab run apex_shortlist --name main_32 --agents 32 --arms desk look_at_others --only $ONLY --open 64" \
  "lab run apex_shortlist --name main_32 --agents 32 --only $ONLY --open 48" \
  --gpu gpu_1x_h100_pcie --max-hours 24 --name apex-shortlist-main-32

# When `uv run lab cloud status apex-shortlist-main-32` says the job is done:
#   uv run lab cloud pull apex-shortlist-main-32
#   uv run lab show apex_shortlist/main_32 --list
