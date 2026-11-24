"""Where every approach stands, read off the runs: `lab standings`, `lab ls`, and two tables in CURRENT.md.

A run keeps how each of its arms was set (config.json) and what every agent ended on (episodes.jsonl). From the
runs under experiments/ that were made with a model, at desks, and have finished, this draws up:

  approaches   a row for each way of setting agents, under each version of the harness and of the looks it
               has been run with, its runs added up: the two numbers it is tracked by (the percent of a
               problem's agents that end right, and on a wrong answer, averaged over problems), how many agents
               end right, how the same agents do under the baseline in the same runs, how the pairs of a
               problem's agents end (both right, on the same wrong answer, on different wrong answers), and
               the collapse: how much more of them end on the same wrong answer than under the baseline
  runs         a row for each run: when it finished, the versions it was made under, what it played

`lab standings --write` puts both into CURRENT.md between two marks, `lab run` does so when a run ends, and a
test fails when the file and the run folders disagree: a number there is one that a run gives.

Two arms are the same approach when an experiment could not tell them apart by how they are set: steps, model,
room to think and to write, how replies are drawn, drafts, looks, and words of their own if they were given
any. An arm's name does not make it another approach. The version of the harness or of the looks it was run
under makes another row of the same approach, and so does the number of agents on a problem when they read
each other: a swarm of eight is not a swarm of forty.

The model is part of how agents are set, so the same approach on another model is a row of its own, named for
the approach and the model ("**baseline** on `9B-bf16`": the released weights on a GPU, where `9B` is the Mac's
4-bit build). Its agents are held against the baseline on the same model, never against another model's.

The problems a run is about (its benchmarks and its split) make another row too, named for them: a share of
agents right is a mean over problems, and the fifteen train problems and another set are not one mean. A row
with no problems named is on `USUAL`, the train split every run before `hard_set` was about.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

from . import current, harness, looks, metrics, report
from .paths import EXPERIMENTS
from .swarm import Arm
from .tables import markdown, percent
from .tracking import Run

BEGIN = "<!-- lab standings: begin (written by `uv run lab standings --write`, and by `lab run` when a run ends) -->"
END = "<!-- lab standings: end -->"
USUAL = (("aime_2024",), "train")       # the problems a row is on when it names none: benchmarks, and their split
NAMED = {"baseline": "alone at a desk, nobody reads anybody", "control": "pauses over its own file",
         "swarm": "reads other agents' files", "control, every step": "pauses over its own file after every step",
         "swarm, every step": "reads another agent's file after every step"}
NOTES = ("An approach is a way of setting agents; `current` is the harness and the looks as the code has them now "
         "(the table of versions below says what each earlier one was). avg % of agents right, avg % on a wrong answer: "
         "the percent of a problem's agents that end on the known answer, and on any other answer, averaged over "
         "problems (the rest end with none): the two numbers an approach is tracked by. agents right: at the end, "
         "added up over the runs. the same agents under the baseline: in the same runs, the same agents on the same problems under the "
         "arm that is set as the baseline is now (in a run made when agents were set otherwise: under its own arm that is set "
         "as this one but for nobody reading anybody), and how many are right under only one of the two. pairs both right, "
         "on the same wrong answer, on different wrong answers: every pair of a problem's agents, by how the two ended, "
         "as a percent of the problem's pairs averaged over problems (the pairs left are one right and one wrong, or "
         "one with no answer: `lab show` has all five). collapse: how many points more of a problem's pairs end on the "
         "same wrong answer than among the same agents under the baseline, and in brackets the same for pairs that are "
         "both right (the positive collapse). These with the two tracked numbers are what an approach is judged by "
         "(Barrett, 2026-10-13).")
RUNS = ("A run `x/y` is the folder `experiments/x/runs/y`, with its settings (`config.json`), its tables (`summary.md`) "
        "and every step of every agent; `uv run lab show x/y` reads it. Not here: runs that have not finished and dry "
        "runs (`uv run lab ls` lists those too), and the board experiments under `experiments/archive/`.")


@dataclass
class Made:
    """A run, as its folder has it."""
    experiment: str
    name: str
    config: dict
    episodes: dict[str, list[dict]]             # by arm, each scored afresh from its logged answers

    @property
    def settings(self) -> dict:
        return self.config["settings"]

    @property
    def arms(self) -> list[dict]:
        return [saved for key, saved in self.settings.items() if key.startswith("arm:")]

    @property
    def kept(self) -> bool:
        """A run the tables count: made with a model, by agents at desks, and finished."""
        played = [e for episodes in self.episodes.values() for e in episodes]
        return (self.config["status"] == "done" and not self.settings.get("dry_run") and bool(played)
                and all(e.get("work") for e in played))

    @property
    def when(self) -> str:
        """When it finished. A run that was stopped and kept as it stood has no such time: then, when it began."""
        return self.config.get("finished") or self.config.get("started") or ""

    @property
    def under(self) -> str:
        """The versions of the code it was made under, as a table says them."""
        return under(next((a.get("harness") for a in self.arms), None), next((a["contact"] for a in self.arms if a.get("contact")), None))


def made(home: Path | None = None) -> list[Made]:
    """Every run under experiments/. The archive's are a folder deeper and are not found: they were not made at
    desks, and their tables are as they were saved."""
    out = []
    for config in sorted((home or EXPERIMENTS).glob("*/runs/*/config.json")):
        run = Run(config.parent)
        out.append(Made(config.parent.parent.parent.name, config.parent.name, run.config, report.arms_of(run.read("episodes"))))
    return out


def way(saved: dict, first: dict) -> dict:
    """How an arm was set, in the settings an arm has now. The runs of `desk_work` were made when an arm had the
    board's settings as well: their `rounds` were the steps after the first, and a run with no word of drafts
    kept them. Whether an arm was given words of its own is in its settings since `own_words` was; before
    that, it was if it was told something else than the first arm of its run, which is how an experiment is
    laid out (the template's first arm is the baseline). Its own words are then part of how it is set; the
    harness's are not, they belong to the harness's version."""
    wrote = saved["sampling"]
    own = saved["own_words"] if "own_words" in saved else saved["system"] != first["system"]
    return {"steps": saved["steps"] if "steps" in saved else saved["rounds"] + 1, "model": saved["model"],
            "thinking": saved["thinking"], "max_tokens": saved["max_tokens"], "max_total_tokens": saved["max_total_tokens"],
            "lines": saved.get("lines", 80),                 # what a file was to stay within before it was a setting
            "sampling": wrote, "thought_sampling": saved.get("thought_sampling") or wrote, "drafts": saved.get("drafts", True),
            "looks": saved.get("looks"), "words": hashlib.sha256(saved["system"].encode()).hexdigest()[:12] if own else None}


def named() -> dict[str, dict]:
    """The approaches CURRENT.md names, as the code sets them now."""
    desk = Arm("desk")
    arms = {"baseline": desk, "control": desk.but("control", looks=looks.RandomLooks(at="own")),
            "swarm": desk.but("swarm", looks=looks.RandomLooks()),
            "control, every step": desk.but("control", looks=looks.RandomLooks(p=1.0, at="own")),
            "swarm, every step": desk.but("swarm", looks=looks.RandomLooks(p=1.0))}
    saved = {name: json.loads(json.dumps(arm.describe(), default=str)) for name, arm in arms.items()}
    return {name: way(settings, settings) for name, settings in saved.items()}


def plain(set_as: dict) -> dict:
    """A way of setting agents as it would be on the model an arm has when none is named: what makes it the
    baseline, the control or the swarm does not depend on the model that plays it."""
    return {**set_as, "model": Arm("desk").model}


# A harness that gains a setting tells an agent who is not given it what the harness before told it, and does
# for it what that one did. A pair here says so of two versions, the earlier first: a run under the earlier one
# stands as a run under the later. CURRENT.md's table of versions says how each pair was checked. (They are kept
# here and not in harness.py, whose version would change with them.)
AS_BEFORE = (("79b1ed093d6e", "484eb06312d1"),)       # `Arm.lines`: with 80 lines, word for word the harness as it was
ANEW = ("634021f6f24b",)      # versions that say or do other things than the one before, so that no run before one stands
                              # as current. This one: a file that is too long is not run, a cut-off reply is told that the
                              # step is used up, and an agent is told before its last step that it is its last


def as_now(harness_version: str | None) -> str | None:
    """The version a run's harness stands as: the latest one that says and does the same for it."""
    later = dict(AS_BEFORE)
    while harness_version in later:
        harness_version = later[harness_version]
    return harness_version


def under(harness_version: str | None, contact: str | None) -> str:
    """The versions something was made under: `current`, or the earlier ones by name."""
    earlier = []
    if as_now(harness_version) != harness.VERSION:
        earlier.append(f"harness `{harness_version}`" if harness_version else "a harness whose version was not kept")
    if contact not in (None, looks.VERSION):
        earlier.append(f"looks `{contact}`")
    return "earlier: " + ", ".join(earlier) if earlier else "current"


@dataclass
class Row:
    """One approach under one version, on one set of problems: its runs, added up."""
    way: dict
    harness: str | None
    contact: str | None
    on: tuple = USUAL                                                   # the problems its runs are about: benchmarks, split
    runs: list[tuple[str, str, str]] = field(default_factory=list)      # experiment, run, the arm's name there
    played: dict = field(default_factory=dict)      # (benchmark, problem, seed) -> its episode, and the same agents' under the baseline
    finished: str = ""                              # of its latest run

    @property
    def current(self) -> bool:
        return under(self.harness, self.contact) == "current"

    @property
    def episodes(self) -> list[dict]:
        return [episode for episode, _ in self.played.values()]

    @property
    def right(self) -> int:
        return sum(e["right"] for e in self.episodes)

    @property
    def agents(self) -> int:
        return sum(e["agents"] for e in self.episodes)

    def against(self) -> dict | None:
        """The same agents under the baseline, where a run of this approach had it beside it: how many of them
        were right there, and how many are right under only one of the two."""
        pairs = [(e, twin) for e, twin in self.played.values() if twin is not None and twin["agents"] == e["agents"]]
        if not pairs:
            return None
        out = {"agents": 0, "right": 0, "here": 0, "there": 0}
        for e, twin in pairs:
            for mine, theirs in zip(e["answers"][-1], twin["answers"][-1]):
                out["agents"] += 1
                out["right"] += theirs == e["truth"]
                out["here"] += mine == e["truth"] and theirs != e["truth"]
                out["there"] += theirs == e["truth"] and mine != e["truth"]
        return out

    def gain(self) -> int:
        against = self.against()
        return against["here"] - against["there"] if against else 0

    def pairs(self) -> dict[str, float]:
        """How the pairs of a problem's agents ended, each kind a mean over the problems that have a pair."""
        each = [pairs for pairs in map(metrics.pairs_of, self.episodes) if pairs["both_right"] == pairs["both_right"]]
        return {kind: sum(pairs[kind] for pairs in each) / len(each) for kind in metrics.PAIRS} if each else {}

    def collapse(self) -> dict | None:
        """Against the same agents under the baseline, where a run had it beside it (`metrics.collapse`): problem
        for problem and seed for seed, as the runs held them together."""
        return metrics.collapse_over([(e, twin) for e, twin in self.played.values()
                                      if twin is not None and twin["agents"] == e["agents"] > 1]) or None


def rows(runs: list[Made]) -> list[Row]:
    """Every approach under every version it has been run with, the named ones first and each one's current
    version first; among the others, those that gain most on the baseline first.

    An agent that plays one problem under one seed in two runs of a row is counted once: an agent alone is the
    same agent in both (its replies come from the cache), so the run with more agents holds the other's."""
    names = named()
    found: dict[tuple, Row] = {}
    for run in (r for r in runs if r.kept):
        ways = {saved["name"]: way(saved, run.arms[0]) for saved in run.arms}
        on = (tuple(run.settings.get("benchmarks") or USUAL[0]), run.settings.get("split") or USUAL[1])
        for saved in run.arms:
            name, set_as = saved["name"], ways[saved["name"]]
            if name not in run.episodes:
                continue
            alone = next((other for other, theirs in ways.items() if plain(theirs) == names["baseline"]       # the baseline on this
                          and theirs["model"] == set_as["model"] and other in run.episodes), None)           # arm's own model
            if alone is None:                # a run made when agents were set otherwise than now: held against its own arm
                alone = next((other for other, theirs in ways.items()                # set as this one but for nobody reading anybody
                              if other in run.episodes and theirs == {**set_as, "looks": None}), None)
            size = saved["agents"] if set_as["looks"] else None
            made_under = as_now(saved.get("harness"))
            key = (json.dumps(set_as, sort_keys=True), made_under, saved.get("contact"), size, on)
            row = found.setdefault(key, Row(set_as, made_under, saved.get("contact"), on))
            row.runs.append((run.experiment, run.name, name))
            row.finished = max(row.finished, run.when)
            twins = {(e["benchmark"], e["problem"]): e for e in run.episodes[alone]} if alone not in (None, name) else {}
            for e in run.episodes[name]:
                played = (e["benchmark"], e["problem"], run.settings.get("seed", 0))
                if played not in row.played or e["agents"] > row.played[played][0]["agents"]:
                    row.played[played] = (e, twins.get((e["benchmark"], e["problem"])))
    order, usual = list(names.values()), Arm("desk").model
    out = sorted(found.values(), key=lambda row: row.finished, reverse=True)
    return sorted(out, key=lambda row: (row.way["model"] != usual, str(row.way["model"]),      # a model's rows stand together,
                                        row.on != USUAL, str(row.on),                          # and of those a set of problems' rows
                                        order.index(plain(row.way)) if plain(row.way) in order else len(order), not row.current,
                                        -row.gain() if plain(row.way) not in order else 0))


def name_of(row: Row) -> str | None:
    return next((name for name, set_as in named().items() if set_as == plain(row.way)), None)


def apart(mine: dict, base: dict) -> str:
    """What sets one way of setting agents apart from the baseline, in a few words."""
    parts = []
    for key, value in mine.items():
        other = base[key]
        if value == other:
            continue
        if key == "words":
            parts.append("told words of its own")
        elif key == "looks":
            parts.append(f"looks {report.rule(value)}" if value else "nobody reads anybody")
        elif key == "drafts":
            parts.append("a reply that was cut off kept in the conversation" if value else "a reply that was cut off left out")
        elif isinstance(value, dict) and isinstance(other, dict):
            parts += [f"{key} {inner} {inside:g}" for inner, inside in value.items() if inside != other.get(inner)]
        else:
            parts.append(f"{key} {value:,}" if isinstance(value, int) and not isinstance(value, bool) else f"{key} {value}")
    return ", ".join(parts) or "nothing"


def count(n: int, what: str) -> str:
    return f"{n:,} {what}{'' if n == 1 else 's'}"


def tracked(episodes: list[dict]) -> tuple[float, float]:
    """The two numbers an approach is tracked by: the share of a problem's agents that end on the known answer,
    and the share that end on any other answer (the rest end with none), each a mean over problems. A problem
    counts once each time it was played, however many agents played it. Counted from `right`, `agents` and
    `unanswered`, which every version of the measures gives: `lab run` loads this file when a run ends, beside
    the measures as they were when that run began."""
    right = [e["right"] / e["agents"] for e in episodes]
    wrong = [(e["agents"] - e["right"] - e["unanswered"]) / e["agents"] for e in episodes]
    return sum(right) / len(right), sum(wrong) / len(wrong)


def cells(row: Row) -> list:
    name, episodes, against, pairs, collapse = name_of(row), row.episodes, row.against(), row.pairs(), row.collapse()
    right, wrong = tracked(episodes)
    by: dict[tuple[str, str], list[str]] = {}
    for experiment, run, arm in row.runs:
        by.setdefault((experiment, arm), []).append(run)
    problems, seeds, sizes = {key[:2] for key in row.played}, {key[2] for key in row.played}, {e["agents"] for e in episodes}
    each = next(iter(sizes))
    played = (f"{count(len(problems), 'problem')} × {count(each, 'agent')}" + (f" × {len(seeds)} seeds" if len(seeds) > 1 else "")
              if len(sizes) == 1 and len(problems) * len(seeds) == len(episodes) else f"{count(row.agents, 'agent')} on {count(len(problems), 'problem')}")
    on = "" if row.way["model"] == Arm("desk").model else f" on `{row.way['model']}`"
    if row.on != USUAL:                                    # another set of problems than the usual one is named too
        on += f", the {row.on[1]} problems of {' and '.join(f'`{benchmark}`' for benchmark in row.on[0])}"
    return [f"**{name}**{on}: {NAMED[name]}" if name else f"as the baseline{on}, but " + apart(plain(row.way), named()["baseline"]),
            under(row.harness, row.contact),
            "; ".join(f"{experiment}/{', '.join(runs)} (`{arm}`)" for (experiment, arm), runs in by.items()),
            played, percent(right, 1), percent(wrong, 1), f"{row.right} of {row.agents}",
            f"{against['right']} of {against['agents']} ({against['here']} right only here, {against['there']} only there)" if against else "",
            *(percent(pairs.get(kind), 1) for kind in ("both_right", "same_wrong", "different_wrong")),
            f"{100 * collapse['same_wrong']['mean']:+.1f} ({100 * collapse['both_right']['mean']:+.1f})" if collapse else ""]


def approaches(runs: list[Made], everything: bool = False) -> str:
    """The table of approaches. Unless `everything`, the named approaches under every version they have been run
    with, and any other approach that has been run under the current one: what was tried and left behind under
    an earlier version is counted in a line, not listed."""
    found = rows(runs)
    if not found:
        return "No run made with a model has finished yet."
    shown, since = [row for row in found if everything or name_of(row) or row.current], ""
    if not shown:                            # agents were set anew and nothing has run since: every row is a record
        shown, since = found, ("\n\nNo run has been made yet with agents set as they are now: every row above is of agents set "
                               "otherwise, under an earlier version, and says what set them apart.")
    table = markdown(["approach", "made under", "runs (and the arm's name there)", "played", "avg % of agents right",
                      "avg % on a wrong answer", "agents right", "the same agents under the baseline", "pairs both right",
                      "pairs on the same wrong answer", "pairs on different wrong answers", "collapse (positive)"],
                     [cells(row) for row in shown])
    left = len(found) - len(shown)
    return table + since + (f"\n\n{count(left, 'other way')} of setting agents {'was' if left == 1 else 'were'} run only under earlier "
                            "versions and left behind: `uv run lab standings --all` lists them." if left else "")


def right_by_arm(run: Made) -> str:
    return ", ".join(f"{arm} {sum(e['right'] for e in episodes)} of {sum(e['agents'] for e in episodes)}"
                     for arm, episodes in run.episodes.items() if all(e.get("work") for e in episodes))


def finished_runs(runs: list[Made]) -> str:
    """A row for each run the approaches are added up from, the latest first."""
    table = []
    for run in sorted((r for r in runs if r.kept), key=lambda r: r.when, reverse=True):
        played = [e for episodes in run.episodes.values() for e in episodes]
        problems, benchmarks = {(e["benchmark"], e["problem"]) for e in played}, list(dict.fromkeys(e["benchmark"] for e in played))
        table.append([f"{run.experiment}/{run.name}", run.when[:10], run.under,
                      f"{count(len(problems), 'problem')} of {', '.join(benchmarks)} {run.settings.get('split', '')}".strip(),
                      run.settings.get("seed", 0), right_by_arm(run)])
    return markdown(["run", "finished", "made under", "played", "seed", "agents right, by arm"], table) if table else ""


def tables(everything: bool = False, home: Path | None = None) -> str:
    """Both tables, as CURRENT.md has them."""
    runs = made(home)
    listed = finished_runs(runs)
    return "\n\n".join([approaches(runs, everything), NOTES, listed, RUNS]) if listed else approaches(runs, everything)


def listing(home: Path | None = None) -> str:
    """Every experiment and every run, finished or not, dry or not (`lab ls`)."""
    home, runs, table = home or EXPERIMENTS, made(home), []
    for path in sorted(home.glob("*/experiment.py")):
        mine = [run for run in runs if run.experiment == path.parent.name]
        if not mine:
            table.append([path.parent.name, "", "not run", "", "", ""])
        for run in mine:
            dry = run.settings.get("dry_run")
            table.append([run.experiment, run.name + (" (dry run)" if dry else ""), run.config["status"],
                          max((len(episodes) for episodes in run.episodes.values()), default=""), right_by_arm(run),
                          "" if dry else run.under])
    out = markdown(["experiment", "run", "status", "problems", "agents right, by arm", "made under"], table)
    archived = sorted(p.parent.name for p in (home / "archive").glob("*/README.md"))
    if archived:
        out += f"\n\nIn experiments/archive (the board experiments, made by code that is no longer here): {', '.join(archived)}."
    return out


def written() -> str | None:
    """The tables as CURRENT.md has them; None if the file or its marks are missing."""
    return current.between(BEGIN, END)


def write(strict: bool = True) -> str:
    """Put the tables into CURRENT.md, between their marks. At the end of a run a file with no place for them is
    said and not an error (`strict=False`): the run is whole without it."""
    if current.put(BEGIN, END, tables()):
        return f"wrote the standings into {current.FILE.name}"
    if strict:
        raise SystemExit(f"{current.FILE.name} has no place for the standings: they go between the lines\n{BEGIN}\n{END}")
    return f"{current.FILE.name} has no place for the standings (`uv run lab standings` prints them)"
