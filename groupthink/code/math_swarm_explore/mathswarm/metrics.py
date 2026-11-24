"""How a swarm did on a problem, from the answer every agent held after each of its steps.

`score` turns one problem's answers into numbers; `summarize` adds problems up. A problem is the unit: under an
arm with looks its agents read each other, so they are one observation, not twelve.

    right           agents who end on the known answer; `unanswered`, agents who end holding none; `wrong`, the
                    rest: agents who end on any other answer
    right_share, wrong_share    `right` and `wrong` as shares of the problem's agents. Their means over problems
                    are the two numbers an approach is tracked by: side by side they say whether a change makes
                    agents right, or only gives an answer, right or wrong, to agents who had none
    correct         a vote over the answers held at the end names the known answer (a tie at the top is split)
    solved          some agent ends on it
    pairs           every pair of the problem's agents, by how the two ended (`PAIRS`): both on the known answer,
                    both on the same wrong answer, on two different wrong answers, one right and one wrong, or
                    one of them with no answer. Shares of the problem's pairs, which add up to 1. Their means
                    over problems, with the two shares above, are what an approach is judged by (Barrett,
                    2026-10-13). `same_wrong` is belief gone to one wrong answer; `wrong_together` in a summary
                    is same_wrong / (same_wrong + different_wrong): of two agents that are both wrong, how
                    often on the same answer
    collapse        in a summary, against the same agents under the arm in which nobody reads anybody: how much
                    `same_wrong` rose (collapse) and how much `both_right` rose (positive collapse), a mean over
                    problems of the difference
    wrong_camp      agents who end on the most common wrong answer: how many agree on a mistake
    endpoint        how the agents' beliefs ended up, as the Flag Game paper sorts them; its "collapse" is at
                    least 85% of the agents on one wrong answer, a line and not the measure above
    distinct_first, distinct_final      how many different answers were held: diversity of opinion
    first_right     agents whose first answer (the first one a run of their file printed) was the known one
    changed         agents who end on another answer than their first; to_right, to_wrong: of those, the ones who
                    went from a wrong answer to the right one, and from the right one to a wrong one
    moves           changes of answer from one step to the next; of those that could have landed on a leading
                    answer of the step before (`open`), how many did (`onto`). A leading answer is one held by
                    more agents than any other, and by at least two. Agents who read nobody land on one only by
                    chance, so the arm in which nobody reads anybody is the measure's baseline

`contact` counts what came of agents reading each other's files, and `twins` holds an arm against the same
agents under another arm: seeds are fixed by the problem, the agent and the step, so until an agent is first
shown something else it is the same agent in both.

The vote, the camps, the endpoints and the leading answer are the measures of the board experiments
(experiments/archive), which are the Flag Game's and those of ../swarm_experiment.
"""
from __future__ import annotations

from collections import Counter

import numpy as np

CONSENSUS, CAMP = 0.85, 0.25   # the Flag Game paper's thresholds for a consensus and for a camp
ENDPOINTS = ("correct consensus", "collapse", "polarized", "fragmented")
MEANS = ("right_share", "wrong_share", "correct", "solved", "distinct_first", "distinct_final")     # averaged over problems, with an interval
COUNTS = ("agents", "right", "wrong", "unanswered", "wrong_camp", "first_right", "first_wrong", "changed", "to_right", "to_wrong",
          "moves", "open", "onto")                                                   # added up over problems
COSTS = ("calls", "invalid", "cut_thoughts", "tokens", "posts")
PAIRS = ("both_right", "same_wrong", "different_wrong", "right_and_wrong", "no_answer")     # how two agents of a problem ended


def share(answers: list[str | None], truth: str) -> float:
    """Share of agents giving `truth`."""
    return sum(a == truth for a in answers) / len(answers) if answers else 0.0


def share_wrong(answers: list[str | None], truth: str) -> float:
    """Share of agents giving an answer that is not `truth`. An agent with no answer is in neither share."""
    return sum(a is not None and a != truth for a in answers) / len(answers) if answers else 0.0


def vote(answers: list[str | None], truth: str) -> float:
    """Chance that a plurality vote names the truth (a tie at the top is broken at random)."""
    counts = Counter(a for a in answers if a is not None)
    if not counts:
        return 0.0
    top = max(counts.values())
    winners = [answer for answer, n in counts.items() if n == top]
    return (truth in winners) / len(winners)


def distinct(answers: list[str | None]) -> int:
    return len({a for a in answers if a is not None})


def largest(answers: list[str | None]) -> float:
    """Share of agents in the biggest camp."""
    counts = Counter(a for a in answers if a is not None)
    return max(counts.values()) / len(answers) if counts else 0.0


def wrong_camp(answers: list[str | None], truth: str) -> int:
    """How many agents hold the most common wrong answer."""
    counts = Counter(a for a in answers if a is not None and a != truth)
    return max(counts.values(), default=0)


def pairs(answers: list[str | None], truth: str) -> dict[str, float]:
    """Every pair of a problem's agents, by how the two ended, as shares of its n(n - 1)/2 pairs: both on the
    known answer, both on the same wrong answer, on two different wrong answers, one right and one wrong, or at
    least one of them with no answer. The five add up to 1 (they are not numbers with one agent: no pair).

    A share of pairs does not depend on how many agents there are: for agents who each end on an answer with
    the same chances, whatever the others do, `same_wrong` of eight and of thirty-two have the same mean, where
    the share on the most common answer is higher for eight. And same_wrong = (both wrong) × (of those, on the
    same answer): how many are wrong and how bunched they are, in one number that only rises when agents do
    end on a wrong answer together."""
    n, counts = len(answers), Counter(a for a in answers if a is not None)
    if n < 2:
        return dict.fromkeys(PAIRS, float("nan"))
    right = counts.get(truth, 0)
    wrong = sum(counts.values()) - right
    same = sum(v * (v - 1) // 2 for answer, v in counts.items() if answer != truth)
    kinds = {"both_right": right * (right - 1) // 2, "same_wrong": same, "different_wrong": wrong * (wrong - 1) // 2 - same,
             "right_and_wrong": right * wrong}
    total = n * (n - 1) // 2
    return {**{kind: count / total for kind, count in kinds.items()}, "no_answer": (total - sum(kinds.values())) / total}


def leaders(answers: list[str | None]) -> set[str]:
    """The answers held by more agents than any other, when at least two agents hold them (several if they
    tie). Empty when every answer is held once: then nothing leads."""
    counts = Counter(a for a in answers if a is not None)
    top = max(counts.values(), default=0)
    return {answer for answer, n in counts.items() if n == top} if top >= 2 else set()


def firsts(answers: list[list[str | None]]) -> list[str | None]:
    """Each agent's first answer: the first one it held (None if it never held one)."""
    return [next((a for a in mine if a is not None), None) for mine in zip(*answers)]


def movement(answers: list[list[str | None]]) -> tuple[int, int, int]:
    """(moves, open, onto): how often an agent that held an answer held another one a step later; how many of
    those changes left an answer that was not leading while some answer led; and how many of these landed on
    a leading answer. An agent's first answer is not a change."""
    moves = open_ = onto = 0
    for before, after in zip(answers, answers[1:]):
        ahead = leaders(before)
        for a, b in zip(before, after):
            if a is not None and a != b:
                moves += 1
                if ahead and a not in ahead:
                    open_ += 1
                    onto += b in ahead
    return moves, open_, onto


def endpoint(answers: list[str | None], truth: str) -> str:
    """Classify where the agents ended up, the way the Flag Game paper does."""
    counts = Counter(a for a in answers if a is not None)
    if not counts:
        return "fragmented"
    leader, n = counts.most_common(1)[0]
    if n / len(answers) >= CONSENSUS:
        return "correct consensus" if leader == truth else "collapse"
    camps = sum(v / len(answers) >= CAMP for v in counts.values())
    return "polarized" if camps >= 2 else "fragmented"


def score(answers: list[list[str | None]], truth: str) -> dict:
    """One problem's numbers. `answers[r][i]` is the answer agent i held after its step r + 1 (None: none yet)."""
    first, last = firsts(answers), answers[-1]
    moves, open_, onto = movement(answers)
    return {
        "agents": len(last), "right": sum(a == truth for a in last), "unanswered": sum(a is None for a in last),
        "wrong": sum(a is not None and a != truth for a in last),
        "right_share": share(last, truth), "wrong_share": share_wrong(last, truth),
        "pairs": pairs(last, truth),
        "correct": vote(last, truth), "solved": float(truth in last), "wrong_camp": wrong_camp(last, truth),
        "distinct_first": distinct(first), "distinct_final": distinct(last), "endpoint": endpoint(last, truth),
        "first_right": sum(a == truth for a in first), "first_wrong": sum(a is not None and a != truth for a in first),
        "changed": sum(a is not None and a != b for a, b in zip(first, last)),
        "to_right": sum(a is not None and a != truth and b == truth for a, b in zip(first, last)),
        "to_wrong": sum(a == truth and b != truth for a, b in zip(first, last)),
        "moves": moves, "open": open_, "onto": onto,
        "by_round": [{"right": share(a, truth), "vote": vote(a, truth), "distinct": distinct(a), "largest": largest(a)}
                     for a in answers],
    }


def interval(values, n_boot: int = 2000, seed: int = 0) -> tuple[float, float, float]:
    """Mean with a 95% bootstrap interval over problems."""
    values = np.asarray(values, dtype=float)
    values = values[~np.isnan(values)]              # a measure that is undefined on a problem leaves it out
    if len(values) == 0:
        return float("nan"), float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    means = values[rng.integers(len(values), size=(n_boot, len(values)))].mean(axis=1)
    return float(values.mean()), float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def summarize(episodes: list[dict], alone: list[dict] = ()) -> dict:
    """Add a set of scored problems up: counts of agents, means over problems as {"mean", "low", "high"}, how
    many problems ended each way, how its pairs of agents ended, the averages after each step, what it cost, what
    agents did at their desks and what came of their reading each other. `alone` is the same problems under the
    arm in which nobody reads anybody, when there is one to hold this arm against (`collapse`, `twins`,
    `contact`)."""
    out: dict = {"problems": len(episodes)}
    for name in COUNTS:
        out[name] = int(sum(e[name] for e in episodes))
    for name in MEANS:
        mean, low, high = interval([e[name] for e in episodes])
        out[name] = {"mean": mean, "low": low, "high": high}
    out["pairs"] = {}
    for kind in PAIRS:
        mean, low, high = interval([pairs_of(e)[kind] for e in episodes])
        out["pairs"][kind] = {"mean": mean, "low": low, "high": high}
    both_wrong = out["pairs"]["same_wrong"]["mean"] + out["pairs"]["different_wrong"]["mean"]
    out["wrong_together"] = out["pairs"]["same_wrong"]["mean"] / both_wrong if both_wrong > 0 else float("nan")
    out["collapse"] = collapse(episodes, alone) if alone else {}
    out["endpoints"] = {name: sum(e["endpoint"] == name for e in episodes) for name in ENDPOINTS}
    rounds = min((len(e["by_round"]) for e in episodes), default=0)
    out["by_round"] = [{key: float(np.mean([e["by_round"][r][key] for e in episodes]))
                        for key in ("right", "vote", "distinct", "largest")} for r in range(rounds)]
    for name in COSTS:
        out[name] = int(sum(e.get(name, 0) for e in episodes))
    out["work"] = work(episodes)
    out["contact"] = contact(episodes, alone)
    out["twins"] = twins(episodes, alone) if alone else {}
    return out


def pairs_of(episode: dict) -> dict[str, float]:
    """A problem's pairs: as it was scored, or from its answers if it was logged before pairs were counted."""
    return episode["pairs"] if "pairs" in episode else pairs(episode["answers"][-1], episode["truth"])


def collapse(here: list[dict], there: list[dict]) -> dict:
    """An arm against the same agents under the arm in which nobody reads anybody, on the problems both have
    played with as many agents: how much the share of pairs on the same wrong answer rose (`same_wrong`: the
    collapse), and the share of pairs that are both right (`both_right`: the positive collapse). Each is a mean
    over problems of the difference, as {"mean", "low", "high"}. What is alone already is the model's own
    leaning, with no contact; this is what was added to it."""
    other = {(e["benchmark"], e["problem"]): e for e in there}
    return collapse_over([(e, twin) for e in here if (twin := other.get((e["benchmark"], e["problem"]))) is not None
                          and len(twin["answers"][-1]) == len(e["answers"][-1])])


def collapse_over(held: list[tuple[dict, dict]]) -> dict:
    """`collapse` over problems that are already held together: each as (under the arm, the same agents alone)."""
    kinds = [(pairs_of(mine), pairs_of(theirs)) for mine, theirs in held]
    out: dict = {"problems": len(kinds)}
    for kind in ("same_wrong", "both_right"):
        mean, low, high = interval([mine[kind] - theirs[kind] for mine, theirs in kinds])
        out[kind] = {"mean": mean, "low": low, "high": high}
    return out if kinds else {}


def work(episodes: list[dict]) -> dict:
    """What agents did with their tools: counts of agents and of tool calls, pooled over problems. Empty for a
    run that was not made at desks (the board experiments of experiments/archive)."""
    desks = [(e, w) for e in episodes for w in e.get("work", [])]
    if not desks:
        return {}
    out = {key: int(sum(w.get(key, 0) for _, w in desks))
           for key in ("writes", "edits", "edits_near", "edits_failed", "runs", "runs_clean", "no_call", "unknown_tool", "cut_off")}
    steps = range(max(len(e["answers"]) for e, _ in desks))
    return {**out, "agents": len(desks), "steps": float(np.median([w["steps"] for _, w in desks])),
            "answered": sum(e["answers"][-1][w["agent"]] is not None for e, w in desks),
            "submitted": sum(w["submitted"] is not None for _, w in desks),
            "submitted_wrong": sum(w["submitted"] is not None and e["answers"][-1][w["agent"]] != e["truth"] for e, w in desks),
            "right": sum(e["answers"][-1][w["agent"]] == e["truth"] for e, w in desks),
            "solved": sum(e["truth"] in e["answers"][-1] for e in episodes if e.get("work")),
            "right_by_step": [sum(e["answers"][min(s, len(e["answers"]) - 1)][w["agent"]] == e["truth"] for e, w in desks) for s in steps],
            "working_by_step": [sum(w["steps"] > s for _, w in desks) for s in steps]}


def contact(episodes: list[dict], alone: list[dict] = ()) -> dict:
    """What came of agents reading files, pooled over problems: counts of looks. A look is `due` when the reader
    was picked and still at work; it is `read` unless there was no file yet. The reader `said` something of the
    file (`said_late`: only when it was asked a second time), or it is one of `no_words`; `called`: it called one
    of its own tools in reply, which was not carried out.

    Of the looks at another agent's file, by what that file printed when Python ran it:
      `differed`    the reader held an answer and the file printed another; `took`: the reader then ended on the
                    file's (`took_right` when it is the known one)
      `had_none`    the reader held no answer yet and the file printed one; `took_first`: the reader ended on it
                    (`took_first_right`). Kept apart: an agent's first answer is not a change of mind
      `heard`       the reader's words reached the other agent while it was at work. `could_give`: the reader
                    held an answer and the other, when it heard, did not hold it; `gave`: the other ended on
                    the reader's answer (`gave_right`)

    `alone` is the same problems played by the same agents with nobody reading anybody: `took_anyway` and
    `gave_anyway` count the agents who end on that answer there too, and so did not need the look for it."""
    names = ("due", "read", "said", "said_late", "own", "others", "differed", "took", "took_right", "took_anyway", "had_none",
             "took_first", "took_first_right", "heard", "could_give", "gave", "gave_right", "gave_anyway", "no_words", "called")
    out = dict.fromkeys(names, 0)
    left_alone = {(e["benchmark"], e["problem"]): e["answers"][-1] for e in alone}
    for e in (e for e in episodes if e.get("looks")):
        answers, last, truth = e["answers"], e["answers"][-1], e["truth"]
        twin = left_alone.get((e["benchmark"], e["problem"]))
        twin = twin if twin is not None and len(twin) == len(last) else [object()] * len(last)      # nobody to hold it against
        for look in e["looks"]:
            out["due"] += 1
            if look["seen"] is None:
                continue
            out["read"] += 1
            out["said"] += bool(look["words"])
            out["said_late"] += bool(look["words"]) and look.get("asks", 1) > 1
            out["no_words"] += not look["words"]
            out["called"] += look["called"]
            if look["of"] == look["reader"]:
                out["own"] += 1
                continue
            out["others"] += 1
            reader, of, own = look["reader"], look["of"], look["own"]
            printed = look["printed"] if "printed" in look else look["theirs"]
            if printed is not None and own is None:
                out["had_none"] += 1
                out["took_first"] += last[reader] == printed
                out["took_first_right"] += last[reader] == printed == truth
            elif printed is not None and printed != own:
                out["differed"] += 1
                took = last[reader] == printed
                out["took"] += took
                out["took_right"] += took and printed == truth
                out["took_anyway"] += took and twin[reader] == printed
            if look["heard"] is not None:
                out["heard"] += 1
                if own is not None and answers[look["heard"] - 1][of] != own:
                    out["could_give"] += 1
                    gave = last[of] == own
                    out["gave"] += gave
                    out["gave_right"] += gave and own == truth
                    out["gave_anyway"] += gave and twin[of] == own
    return out if out["due"] else {}


def twins(here: list[dict], there: list[dict]) -> dict:
    """An arm against the same agents under another arm, on the problems both have played: how many agents end
    on another answer `here` than `there`, and of those, how many are right only here and only there."""
    other = {(e["benchmark"], e["problem"]): e for e in there}
    out = {"agents": 0, "differ": 0, "right_here": 0, "right_there": 0}
    for e in here:
        if (twin := other.get((e["benchmark"], e["problem"]))) is None or len(twin["answers"][-1]) != len(e["answers"][-1]):
            continue
        for mine, theirs in zip(e["answers"][-1], twin["answers"][-1]):
            out["agents"] += 1
            out["differ"] += mine != theirs
            out["right_here"] += mine == e["truth"] and theirs != e["truth"]
            out["right_there"] += theirs == e["truth"] and mine != e["truth"]
    return out
