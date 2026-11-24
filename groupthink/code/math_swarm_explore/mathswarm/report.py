"""Read a run: its tables, its problems one line each, one problem step by step, and every agent a line a step.
Needs no model."""
from __future__ import annotations

import re
from pathlib import Path

from .looks import said as said_at_a_look
from .metrics import score, summarize
from .paths import EXPERIMENTS
from .tables import markdown, percent, with_interval
from .tracking import Run


def find(run: str) -> Run:
    """A run from its folder, or from `experiment/run`, or from `experiment` alone when it has a run called main
    or only one run. The board experiments are looked for under `archive/` too."""
    parts = run.strip("/").split("/")
    homes = (EXPERIMENTS, EXPERIMENTS / "archive")
    folders = [Path(run), *(home / run for home in homes), *(home.joinpath(*parts[:-1]) / "runs" / parts[-1] for home in homes),
               *(home / run / "runs" / "main" for home in homes)]
    for folder in folders:
        if (folder / "config.json").exists():
            return Run(folder)
    runs = [config for home in homes for config in sorted((home / run / "runs").glob("*/config.json"))]
    if len(runs) == 1:
        return Run(runs[0].parent)
    listed = ", ".join(f"{run}/{r.parent.name}" for r in runs) or "none found"
    raise SystemExit(f"no run at {run!r} (runs: {listed}). `lab ls` lists them all.")


def arms_of(episodes: list[dict]) -> dict[str, list[dict]]:
    """Episodes by arm, each scored afresh from its logged answers, so that a measure added after a run was
    made is there for that run too."""
    by_arm: dict[str, list[dict]] = {}
    for episode in episodes:
        by_arm.setdefault(episode["arm"], []).append({**episode, **score(episode["answers"], episode["truth"])})
    return by_arm


def baseline_of(settings: dict) -> str | None:
    """The arm of a run in which nobody reads anybody, by its settings: what the other arms are held against."""
    arms = [saved for key, saved in settings.items() if key.startswith("arm:")]
    return next((saved["name"] for saved in arms if not saved.get("looks")), None)


def in_words(saved: dict) -> str:
    """What an arm's agents do, in a few plain words, from how it is set: the name of its bar in a figure. An arm
    with a rule of looks this does not know keeps its own name."""
    looks = saved.get("looks")
    if not looks:
        return "alone"
    if not isinstance(looks, dict) or looks.get("rule") != "RandomLooks" or not looks.get("p"):
        return saved["name"]
    every = 1 / looks["p"]
    often = "after every step" if every <= 1 else f"1 step in {every:.0f}" if abs(every - round(every)) < 1e-9 else f"{looks['p']:.0%} of its steps"
    return ("pauses over its own file" if looks.get("at") == "own" else "reads another's file") + "\n" + often


def summary_of(episodes: list[dict], alone: str | None = None) -> dict:
    """Every arm's numbers over all its problems, and benchmark by benchmark. `alone` names the arm in which
    nobody reads anybody (`baseline_of`): each other arm is also held against it, agent for agent."""
    by_arm = arms_of(episodes)
    alone = alone if alone in by_arm and len(by_arm) > 1 else None
    out = {}
    for arm, mine in by_arm.items():
        benchmarks = list(dict.fromkeys(e["benchmark"] for e in mine))
        out[arm] = {"all": summarize(mine, by_arm[alone] if alone not in (None, arm) else ()),
                    "by_benchmark": {b: summarize([e for e in mine if e["benchmark"] == b]) for b in benchmarks},
                    "against": alone if alone != arm else None}
    return out


def of(part: int, whole: int) -> str:
    return f"{part} of {whole}"


def ends(summary: dict) -> str:
    """One row per arm: how its agents ended. The two tracked numbers come first."""
    header = ["arm", "problems", "avg % of agents right", "avg % on a wrong answer", "agents right", "no answer",
              "on the leading wrong answer", "different answers held", "a vote is right", "problems solved",
              "85% or more on one wrong answer"]
    rows = []
    for arm, entry in summary.items():
        s = entry["all"]
        rows.append([arm, s["problems"], percent(s["right_share"]["mean"], 1), percent(s["wrong_share"]["mean"], 1),
                     of(s["right"], s["agents"]), s["unanswered"], s["wrong_camp"],
                     f"{s['distinct_first']['mean']:.1f} → {s['distinct_final']['mean']:.1f}", with_interval(s["correct"]),
                     of(round(s["solved"]["mean"] * s["problems"]), s["problems"]), s["endpoints"]["collapse"]])
    return markdown(header, rows)


def points(stat: dict | None) -> str:
    """A change in a share as '+21.6 (+9.6 to +34.9)': points of a percent, and its 95% interval over problems."""
    if not stat or stat["mean"] != stat["mean"]:
        return ""
    return f"{100 * stat['mean']:+.1f} ({100 * stat['low']:+.1f} to {100 * stat['high']:+.1f})"


PAIRS = {"both_right": "both right", "same_wrong": "on the same wrong answer", "different_wrong": "on different wrong answers",
         "right_and_wrong": "one right, one wrong", "no_answer": "one has no answer"}          # the kinds of a pair, in words


def pairs(summary: dict) -> str:
    """One row per arm: how the pairs of a problem's agents ended, a mean over problems. The five add up to 100%."""
    rows = [[arm] + [percent(s["pairs"][kind]["mean"], 1) for kind in PAIRS] + [percent(s["wrong_together"], 1)]
            for arm, s in ((arm, entry["all"]) for arm, entry in summary.items()) if s.get("pairs")]
    return markdown(["arm: pairs of agents"] + list(PAIRS.values()) + ["when both are wrong, on the same answer"], rows) if rows else ""


def collapse(summary: dict) -> str:
    """Each arm against the same agents under the arm in which nobody reads anybody: how much more of a problem's
    pairs end on the same wrong answer, and how much more of them both right."""
    rows = [[arm, entry["against"], c["problems"], points(c["same_wrong"]), points(c["both_right"])]
            for arm, entry in summary.items() if (c := entry["all"].get("collapse"))]
    return markdown(["arm", "against", "problems", "collapse: pairs on the same wrong answer, in points",
                     "positive collapse: pairs both right, in points"], rows) if rows else ""


def moved(summary: dict) -> str:
    """How answers moved after an agent's first one."""
    header = ["arm", "first answers right", "first answers wrong", "ended on another answer", "wrong → right",
              "right → wrong", "changes of answer", "of those that could, onto a leading answer"]
    rows = [[arm, s["first_right"], s["first_wrong"], s["changed"], s["to_right"], s["to_wrong"], s["moves"],
             of(s["onto"], s["open"]) if s["open"] else ""] for arm, s in ((arm, entry["all"]) for arm, entry in summary.items())]
    return markdown(header, rows)


def against(summary: dict) -> str:
    """Each arm against the same agents under the arm in which nobody reads anybody."""
    rows = [[arm, entry["against"], t["agents"], t["differ"], t["right_here"], t["right_there"]]
            for arm, entry in summary.items() if (t := entry["all"].get("twins"))]
    return markdown(["arm", "against", "agents", "end on another answer", "right only here", "right only there"], rows) if rows else ""


def contacts(summary: dict) -> str:
    """Agents reading files: counts of looks, pooled over problems. What was read and said, and then what moved."""
    looked = [(arm, c) for arm, c in ((arm, entry["all"].get("contact")) for arm, entry in summary.items()) if c]
    if not looked:
        return ""
    read = markdown(["arm", "files read", "of another agent", "reader said something (only when asked again)",
                     "called a tool of its own in reply", "words that reached the other agent at work"],
                    [[arm, c["read"], c["others"], f"{c['said']} ({c['said_late']})", c["called"], c["heard"]] for arm, c in looked])
    moved = markdown(["arm", "reader held another answer than the file printed", "then ended on the file's (right; without the look too)",
                      "reader held no answer yet", "then ended on the file's (right)", "the other held another answer than the reader's",
                      "then ended on the reader's (right; without the look too)"],
                     [[arm, c["differed"], f"{c['took']} ({c['took_right']}; {c['took_anyway']})", c["had_none"],
                       f"{c['took_first']} ({c['took_first_right']})", c["could_give"], f"{c['gave']} ({c['gave_right']}; {c['gave_anyway']})"]
                      for arm, c in looked if c["others"]])
    return read + ("\n\n" + moved if any(c["others"] for _, c in looked) else "")


def by_benchmark(summary: dict) -> str:
    """Agents right, one row per arm and one column per benchmark."""
    benchmarks = list(dict.fromkeys(b for entry in summary.values() for b in entry["by_benchmark"]))
    rows = [[arm] + [of(entry["by_benchmark"][b]["right"], entry["by_benchmark"][b]["agents"]) if b in entry["by_benchmark"] else ""
                     for b in benchmarks] for arm, entry in summary.items()]
    return markdown(["arm: agents right"] + benchmarks, rows)


def work(summary: dict) -> str:
    """How agents ended, and what they did with their tools. Counts of agents and of tool calls, pooled over
    problems. `right` and `held an answer` are agents at the end, submitted or not; a problem is solved when
    some agent ended right. An edit is `near` when its `old` was not in the file word for word and the lines
    nearest to it were replaced; `failed` when nothing was changed."""
    header = ["arm", "agents", "right", "problems solved", "held an answer", "submitted (wrong)", "steps used (median)",
              "files written", "edits (near, failed)", "Python runs", "of those, stopped with an error",
              "replies cut off", "replies with no call"]
    rows = [[arm, w["agents"], w["right"], w["solved"], w["answered"], f"{w['submitted']} ({w['submitted_wrong']})", f"{w['steps']:g}",
             w["writes"], f"{w['edits']} ({w['edits_near']}, {w['edits_failed']})", w["runs"], w["runs"] - w["runs_clean"],
             w["cut_off"], w["no_call"] + w["unknown_tool"]]
            for arm, w in ((arm, entry["all"].get("work")) for arm, entry in summary.items()) if w]
    return markdown(header, rows) if rows else ""


def by_step(summary: dict) -> str:
    """How many agents held the right answer after each step, and how many took the step (the others had
    stopped)."""
    desks = [(arm, w) for arm, w in ((arm, entry["all"].get("work")) for arm, entry in summary.items()) if w]
    rows = [row for arm, w in desks for row in ([f"{arm}: right after it"] + w["right_by_step"], [f"{arm}: agents who took it"] + w["working_by_step"])]
    return markdown(["step"] + [str(step) for step in range(1, max((len(row) for row in rows), default=1))], rows) if rows else ""


def cost(summary: dict) -> str:
    rows = [[arm, s["calls"], f"{s['tokens']:,}", percent(s["cut_thoughts"] / s["calls"] if s["calls"] else None),
             percent(s["invalid"] / s["posts"] if s["posts"] else None)] for arm, s in ((arm, entry["all"]) for arm, entry in summary.items())]
    return markdown(["arm", "calls", "tokens written", "thoughts cut", "steps after which no answer was held"], rows)


def tables(summary: dict, more: bool = True) -> str:
    """A run's tables: how each arm's agents ended, how its pairs of agents ended, how much of that is collapse,
    how answers moved, each arm against the same agents left alone, and what came of the looks. With `more`:
    after each step, what agents did with their tools, and the cost."""
    parts = [ends(summary), pairs(summary), collapse(summary), moved(summary), against(summary), contacts(summary)]
    if len({b for entry in summary.values() for b in entry["by_benchmark"]}) > 1:
        parts.append(by_benchmark(summary))
    return "\n\n".join(part for part in parts + [by_step(summary), work(summary), cost(summary)] * more if part)


NOTES = ("avg % of agents right, avg % on a wrong answer: the percent of a problem's agents that end on the known answer, "
         "and on any other answer, averaged over problems (the rest end with none): the two numbers an approach is "
         "tracked by. agents right, no answer: agents at the end, whether or not they submitted. on the leading wrong answer: "
         "agents who end on a problem's most common wrong answer, added up over problems. different answers held: "
         "among a problem's agents, their first answers → their last (a mean over problems). a vote is right: a "
         "vote over the answers held at the end names the known one, with a 95% interval over problems. 85% or more on "
         "one wrong answer: problems that end so. pairs of agents: every pair of a problem's agents, by how the two "
         "ended, as a percent of the problem's pairs averaged over problems; the five kinds add up to 100%. when both "
         "are wrong, on the same answer: pairs on the same wrong answer as a share of the pairs in which both are wrong. "
         "collapse: how much more of a problem's pairs end on the same wrong answer than among the same agents with "
         "nobody reading anybody, in points of a percent, with a 95% interval over problems; positive collapse: the "
         "same for pairs that are both right. A first answer is the first one a "
         "run of an agent's file printed. A leading answer is one held by more agents than any other, and by at "
         "least two, the step before. A look is one agent reading a file and saying what it makes of it; what the "
         "file printed is what Python printed when it last ran; without the look too: the same agent ends on that "
         "answer in the arm in which nobody reads anybody.")
DESK_NOTES = ("problems solved: some agent ended right. An edit is near when one line of its `old` was miscopied and it "
              "was carried out all the same, failed when nothing was changed. thoughts cut: closed at the budget.")


def shared_only(episodes: list[dict]) -> list[dict]:
    """The episodes on problems that every arm in the run has played: arms compared on the same problems."""
    played: dict[str, set] = {}
    for e in episodes:
        played.setdefault(e["arm"], set()).add((e["benchmark"], e["problem"]))
    common = set.intersection(*played.values()) if played else set()
    return [e for e in episodes if (e["benchmark"], e["problem"]) in common]


def settings_line(key: str, saved: dict, desk: dict | None) -> str:
    """An arm's settings in a line. Arms after the first are told apart from it."""
    if desk is not None:
        return f"{key}: as {desk['name']}, but {differs(saved, desk)}"
    wrote, thought = saved["sampling"], saved.get("thought_sampling") or saved["sampling"]
    steps = saved["steps"] if "steps" in saved else saved["rounds"] + 1           # a run made before `rounds` became `steps`
    return (f"{key}: {saved['agents']} agents, each in a Python file for {steps} steps, model {saved['model']}, "
            f"thinking {saved['thinking']} (temperature {thought['temperature']:g}, presence penalty {thought['presence_penalty']:g}), "
            f"writing {saved['max_tokens']} (temperature {wrote['temperature']:g}, presence penalty {wrote['presence_penalty']:g}), "
            f"looks {rule(saved.get('looks'))}")


def rule(saved: dict | None) -> str:
    """A rule of a run's settings as it is written in an experiment: RandomLooks(p=0.25, first=2, at=others)."""
    if not isinstance(saved, dict) or "rule" not in saved:
        return str(saved) if saved else "none"
    return f"{saved['rule']}({', '.join(f'{key}={value}' for key, value in saved.items() if key != 'rule')})"


def overview(run: Run, shared: bool = False, benchmark: str | None = None, arm: str | None = None, more: bool = False) -> str:
    c = run.config
    lines = [f"{c['experiment']} / {c['run']}: {c['status']}, started {c['started']}, finished {c['finished'] or '-'}",
             f"command: {c['command']}",
             f"git: {c['git']['commit'][:10] or 'no commit'}{' + uncommitted changes' if c['git']['uncommitted_changes'] else ''}"]
    settings = c["settings"]
    lines.append("problems: " + ", ".join(f"{k}={settings[k]}" for k in ("benchmarks", "split", "problems", "seed") if k in settings)
                 + (" (DRY RUN: scripted stand-ins, not a model)" if settings.get("dry_run") else ""))
    episodes = run.read("episodes")
    if episodes and not all(e.get("work") for e in episodes):
        saved = run.path("summary.md")                      # a board experiment: its tables as they were written then
        lines += ["", "This run was made by the board machinery, which is no longer in the code (experiments/archive/README.md).",
                  "Its tables as they were saved:", "", saved.read_text().strip() if saved.exists() else "(no summary.md was saved)"]
        return "\n".join(lines)
    desk = None                                             # the first arm: the others are told apart from it
    for key, saved in settings.items():
        if key.startswith("arm:"):
            lines.append(settings_line(key, saved, desk))
            desk = desk or saved
    shown = [e for e in episodes if benchmark in (None, e["benchmark"]) and arm in (None, e["arm"])]
    shown = shared_only(shown) if shared else shown
    if benchmark or arm:
        lines.append("\nOnly " + ", ".join(part for part in (benchmark, arm and f"arm {arm}") if part) + ":")
    if shown:
        if shared:
            lines.append(f"\nOn the {len({(e['benchmark'], e['problem']) for e in shown})} problems every arm has played:")
        lines += ["", tables(summary_of(shown, baseline_of(settings)), more), "", NOTES + (" " + DESK_NOTES if more else "")]
    lines.append(f"\n{len(episodes)} (arm, problem) pairs logged. Next: --more, --list, --trace, or --problem ID --arm ARM.")
    return "\n".join(lines)


def differs(arm: dict, base: dict) -> str:
    """What sets an arm's settings apart from another's, in a few words."""
    parts = []
    for key, value in arm.items():
        other = base.get(key)
        if key == "name" or value == other:
            continue
        if key == "system":
            parts.append(f"told {len(value):,} characters instead of {len(other or ''):,}")
        elif key in ("contact", "own_words"):
            continue                                        # the version of the rules of a look: said with `looks`; words
                                                            # of its own: said with `system`
        elif key == "looks":
            parts.append(f"looks {rule(value)}")
        elif isinstance(value, dict) and isinstance(other, dict):
            parts += [f"{key} {inner} {inside}" for inner, inside in value.items() if inside != other.get(inner)]
        else:
            parts.append(f"{key} {'as sampling' if key == 'thought_sampling' and value is None else value}")
    return ", ".join(parts) or "nothing"


WHERE = {
    "wrong": lambda e: e["correct"] < 0.5, "right": lambda e: e["correct"] >= 0.5,
    "collapse": lambda e: e["endpoint"] == "collapse", "unsolved": lambda e: not e["solved"],
    "split": lambda e: e["distinct_final"] > 1,              # the agents end on more than one answer
}


def listing(run: Run, arm: str | None = None, where: str | None = None, benchmark: str | None = None) -> str:
    rows = []
    for e in (scored for mine in arms_of(run.read("episodes")).values() for scored in mine):
        if (arm and e["arm"] != arm) or (benchmark and e["benchmark"] != benchmark) or (where and not WHERE[where](e)):
            continue
        last = e["answers"][-1]
        held = sorted(((last.count(a), a) for a in {a for a in last if a is not None}), reverse=True)
        rows.append([e["arm"], e["benchmark"], e["problem"], e["truth"], of(e["right"], e["agents"]),
                     ", ".join(f"{a} ×{n}" for n, a in held[:4]) + (" …" if len(held) > 4 else "") or "(none)",
                     "✓" if e["correct"] >= 0.5 else "✗", e["endpoint"], f"{e['distinct_first']} → {e['distinct_final']}"])
    return markdown(["arm", "benchmark", "problem", "known answer", "agents right", "answers held at the end", "a vote", "ended",
                     "different answers"], rows)


def verdict(post: dict) -> str:
    """In a few words, what Python made of an agent's file."""
    check = post.get("check")
    if not check:
        return ""
    words = check["output"] if check["status"] == "ok" or "error" not in check else check["error"].strip().split("\n")[-1]
    return f"   [Python {check['status']}" + (f": {' '.join(words.split())[:90]}" if words else "") + "]"


def problem(run: Run, problem_id: str, arm: str | None = None, benchmark: str | None = None, thoughts: bool = False,
            prompts: bool = False, agent: int | None = None) -> str:
    """One problem, step by step: what every agent held after each step, and what it did in it."""
    def mine(row: dict) -> bool:
        return row["problem"] == problem_id and (not arm or row["arm"] == arm) and (not benchmark or row["benchmark"] == benchmark)

    episodes = [{**e, **score(e["answers"], e["truth"])} for e in run.read("episodes") if mine(e)]
    if not episodes:
        raise SystemExit(f"no problem {problem_id!r} matching that in {run.folder} (see --list)")
    if len(episodes) > 1:
        options = sorted({f"--benchmark {e['benchmark']} --arm {e['arm']}" for e in episodes})
        raise SystemExit("several match; narrow it down:\n  " + "\n  ".join(options))
    e = episodes[0]
    posts = [p for p in run.read("posts") if mine(p) and p["arm"] == e["arm"]]
    calls = [c for c in run.read("transcripts") if mine(c) and c["arm"] == e["arm"]]
    out = [f"{e['arm']} on {e['benchmark']} {e['problem']} ({e['split']}): {e['agents']} agents, up to {len(e['answers'])} steps. "
           f"Known answer: {e['truth']}."]
    if calls:
        statement = calls[0]["prompt"].split("Problem:\n", 1)[1]
        out.append(statement if len(statement) <= 1500 else f"{statement[:1100]}\n[... {len(statement) - 1400} characters ...]\n{statement[-300:]}")
    elif thoughts or prompts:
        out.append("(no transcripts.jsonl for this run on this machine: thoughts and prompts are not tracked by git)")
    for round_, standing in enumerate(e["by_round"]):
        out.append(f"\n--- step {round_ + 1}: {percent(standing['right'])} of agents right, {standing['distinct']} different answers ---")
        for post in (p for p in posts if p["round"] == round_ and agent in (None, p["agent"] + 1)):
            said = [c for c in calls if c["round"] == round_ and c["agent"] == post["agent"]]
            call = next((c for c in said if "look" not in c), None)
            if prompts and call:
                out.append(f"\n[what Agent {post['agent'] + 1} was shown]\n{call['prompt']}")
            if thoughts and call and call.get("thought"):
                out.append(f"\n[Agent {post['agent'] + 1} thought, {call['thought_tokens']} tokens"
                           f"{', cut at its budget' if call['finished_thinking'] is False else ''}]\n{call['thought']}\n")
            out.append(f"  Agent {post['agent'] + 1:<3} {(post['answer'] or '(none)'):<14} {'✓' if post['right'] else '✗'}  [{post['did']}] {post['note']}{verdict(post)}")
            if call and (thoughts or prompts):              # each call and what it said
                for name, told in call["did"]:
                    out.append(f"      {name or '(no tool call)'} →\n        " + told.replace("\n", "\n        "))
            for look in (c for c in said if "look" in c):   # and then it read a file
                whose = "its own file" if look["look"]["of"] == post["agent"] else f"Agent {look['look']['of'] + 1}'s file"
                out.append(f"      then read {whose} and said: {quoted(said_at_a_look(look['reply'])[0], 600) or '(nothing)'}")
                if prompts:
                    out.append(f"\n[what Agent {post['agent'] + 1} was shown]\n{look['prompt']}")
    out.append(f"\n{of(e['right'], e['agents'])} agents right at the end; a vote over their answers: {percent(e['correct'])}; ended: {e['endpoint']}.")
    return "\n".join(out)


def outcome(said: str) -> str:
    """What a tool told an agent, in a few words: enough to see where a step went."""
    head = said.split("\n", 1)[0]
    if "It ran with no errors" in said:
        for line in reversed(said.split("\n")):
            checks = (", typed in" if "text you typed in" in line else ", unchecked" if re.search(r"Nothing in th(e|is) file checks it", line) else
                      f", {m.group(1)} held" if (m := re.search(r"The file's (\d+ asserts|assert) held", line)) else "")
            if (m := re.match(r"Your answer was (.+) and now stands at (.+?)\. Be sure", line)):
                return f"ran: answer {m.group(1)} → {m.group(2)}{checks}"
            if (m := re.match(r"Your answer still stands at (.+?)\.(?: |$)", line)):
                return f"ran: answer {m.group(1)} again{checks}"
            if (m := re.match(r"Your answer now stands at (.+?)\.(?: |$)", line)):
                return f"ran: answer {m.group(1)}{checks}"
            if line.startswith("`ANSWER:"):
                return "ran: an ANSWER line that is not an answer"
        return "ran: no answer printed"
    if "It stopped with an error" in said:
        error = said.split("It stopped with an error:\n", 1)[1].split("\nBefore that it printed", 1)[0].split("\nIt had printed nothing", 1)[0]
        return "error: " + " ".join(error.strip().split("\n")[-1].split())[:100]
    if "It was stopped" in said:
        return "stopped: " + said.split("It was stopped: ", 1)[1].split(". Make what", 1)[0][:100]
    return " ".join(head.split())[:100]


def trace(run: Run, arm: str | None = None, problem_id: str | None = None, agent: int | None = None, files: bool = False) -> str:
    """What every agent did, a line a step: how long it thought and wrote, the tools it called and what came of
    each, and the answer it held afterwards. A file it read, and what it wrote of it, is a line of its own
    (`read`), and so is what another agent wrote about its file (`heard`). With `files`, the file that printed
    the answer each agent holds (its last file, if it holds none). It is for following an agent to where it
    went wrong: in its reasoning, in its use of the tools, or in what it took from another."""
    episodes = [e for e in run.read("episodes") if e.get("work") and arm in (None, e["arm"]) and problem_id in (None, e["problem"])]
    if not episodes:
        raise SystemExit(f"no agents at desks matching that in {run.folder} (see --list)")
    calls, read, posts, said = {}, {}, {}, {}
    for call in run.read("transcripts"):
        if "look" in call:                                  # the replies of one look: one, or two if it was asked again
            read.setdefault((call["arm"], call["benchmark"], call["problem"], call["agent"], call["round"]), []).append(call)
        else:
            calls[call["arm"], call["benchmark"], call["problem"], call["agent"], call["round"]] = call
    for post in run.read("posts"):
        posts.setdefault((post["arm"], post["benchmark"], post["problem"], post["agent"]), []).append(post)
    for look in run.read("looks"):
        said[look["arm"], look["benchmark"], look["problem"], look["reader"], look["step"]] = look.get("said") or ""
    out = [] if calls else ["(no transcripts.jsonl for this run on this machine: tokens and what the tools said are not tracked by git)"]
    for e in episodes:
        out.append(f"\n{e['arm']} on {e['benchmark']} {e['problem']}: known answer {e['truth']}")
        looks = e.get("looks", [])
        for work in e["work"]:
            seat = work["agent"]
            if agent not in (None, seat + 1):
                continue
            held = e["answers"][-1][seat]
            how = f"submitted in step {work['submitted']}" if work["submitted"] else f"out of steps after {work['steps']}"
            out.append(f"\n  agent {seat + 1}: holds {held or 'no answer'} {'✓' if held == e['truth'] else '✗'}, {how}; "
                       f"{work['runs']} runs ({work['runs_clean']} with no errors), {work['lines']} lines")
            mine, proof = posts.get((e["arm"], e["benchmark"], e["problem"], seat), []), None
            for post in mine:
                key = (e["arm"], e["benchmark"], e["problem"], seat, post["round"])
                call = calls.get(key)
                did = [(name or "no tool call", outcome(told)) for name, told in call["did"]] if call else \
                    [(name, "") for name in post["did"].split(", ")]
                if any(told.startswith("ran: answer") for _, told in did):
                    proof = post["python"]                  # the file as it last printed the answer the agent holds
                spent = spent_on(call)
                holds = f"   (holds {post['answer']} {'✓' if post['right'] else '✗'})" if post["answer"] else ""
                out.append(f"    step {post['round'] + 1:>2}  {spent}{did[0][0]:<10} {did[0][1]}{holds if len(did) == 1 else ''}")
                out += [f"{'':>{13 + len(spent)}}{name:<10} {told}{holds if at == len(did) - 2 else ''}" for at, (name, told) in enumerate(did[1:])]
                step = post["round"] + 1
                for look in (look for look in looks if look["reader"] == seat and look["step"] == step and look["seen"] is not None):
                    whose = "its own file" if look["of"] == seat else f"agent {look['of'] + 1}'s file after its step {look['seen']}"
                    theirs = "" if look["of"] == seat else f" (it held {look['theirs'] or 'no answer'}{' ✓' if look['theirs'] == e['truth'] else ''})"
                    words = said.get((e["arm"], e["benchmark"], e["problem"], seat, step), "")
                    asked = read.get(key, [])
                    late = ", asked twice" if look.get("asks", 1) > 1 else ""
                    for unanswered in asked[:-1]:
                        out.append(f"    read     {spent_on(unanswered)}{whose}{theirs}: said nothing (called {', '.join(said_at_a_look(unanswered['reply'])[1]) or 'nothing'})")
                    out.append(f"    read     {spent_on(asked[-1] if asked else None)}{whose}{theirs}{late}" + (f': "{quoted(words)}"' if words else ": said nothing"))
                for look in (look for look in looks if look["of"] == seat and look["reader"] != seat and look["heard"] == step):
                    words = said.get((e["arm"], e["benchmark"], e["problem"], look["reader"], look["step"]), "")
                    out.append(f"    heard    from agent {look['reader'] + 1}, who read its file after step {look['seen']}" + (f': "{quoted(words)}"' if words else ""))
            last = next((post["python"] for post in reversed(mine) if post.get("python")), None)
            if files and (proof or last):
                out.append(("    the file that printed its answer:\n" if proof else "    its file:\n") + numbered_file(proof or last))
    if calls:
        out.append("\nthought N*: the thought was cut at its budget. wrote: tokens of the reply after the thought.")
    return "\n".join(out)


def spent_on(call: dict | None) -> str:
    """How long a call thought and wrote, for a line of the trace."""
    return (f"thought {call['thought_tokens']:>4}{'*' if call['finished_thinking'] is False else ' '} "
            f"wrote {call['tokens'] - call['thought_tokens']:>4}  ") if call else ""


def quoted(words: str, limit: int = 220) -> str:
    words = " ".join(words.split())
    return words if len(words) <= limit else words[:limit - 1].rstrip() + "…"


def numbered_file(code: str) -> str:
    return "\n".join(f"      {n:>3}  {line}" for n, line in enumerate(code.split("\n"), 1))


def compare(runs: list[Run]) -> str:
    """Arms from several runs, each on the problems that every one of those runs played."""
    loaded = [(run, run.read("episodes")) for run in runs]
    shared = set.intersection(*({(e["benchmark"], e["problem"]) for e in episodes} for _, episodes in loaded))
    if not shared:
        raise SystemExit("these runs have no problem in common")
    merged = {}
    for run, episodes in loaded:
        for arm, mine in arms_of([e for e in episodes if (e["benchmark"], e["problem"]) in shared]).items():
            merged[f"{run.config['experiment']}/{run.config['run']}: {arm}"] = {"all": summarize(mine), "by_benchmark": {}, "against": None}
    return "\n\n".join([ends(merged), pairs(merged), moved(merged)]) + f"\n\nOn the {len(shared)} problems all of these runs played. " + NOTES
