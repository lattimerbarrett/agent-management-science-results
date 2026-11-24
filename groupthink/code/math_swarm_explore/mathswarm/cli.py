"""`lab`: everything this repo does, from the command line.

    lab current                                 what the baseline and the swarm are now, from the code (CURRENT.md)
    lab standings                               every approach's numbers, added up over its runs (CURRENT.md; --all, --write)
    lab doctor                                  is this machine ready? (model, Python's sandbox, data, lock, memory; a Mac's
                                                battery, a GPU machine's GPU and vLLM)
    lab cloud run "lab run every_step ..."      the same run on a rented GPU, which is given back when it ends (lab cloud --help)
    lab data                                    build the paper's benchmarks into data/benchmarks/
    lab new passing_notes "Does ... help?"      start an experiment from the template
    lab run random_looks --dry-run              scripted stand-ins instead of a model: seconds, checks the plumbing
    lab run random_looks --name pilot --problems 2 --arms desk look_at_others
    lab show random_looks/pilot                 a run's tables (--more: what agents did with their tools, and the cost)
    lab show random_looks/pilot --list --where split
    lab show random_looks/pilot --trace         every agent, a line a step (--problem, --agent, --files)
    lab show random_looks/pilot --problem 2024-I-9 --arm look_at_others --thoughts
    lab plot random_looks/pilot                 its figures: agents right and answers held after each step, and how
                                                the pairs of a problem's agents ended
    lab compare desk_work/main random_looks/main
    lab ls                                      every experiment and run, finished or not
    lab python 'print(2 + 2)'                   what an agent is told when it runs that as its file (or a file of it)

A run is resumable: the same command carries on from what is logged, `--problems` can be raised later, and an
arm can be added to a run with `--arms`. A different swarm (agents, steps, model, thinking) needs its own
`--name`.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import replace
from pathlib import Path

from . import experiment, report
from .paths import BENCHMARKS, CACHE, ROOT

SPEED = CACHE / "speed.json"                    # tokens a second, per model, as the last real run on this machine measured it
GUESS = {"9B": 150.0, "4B": 300.0}              # on the Mac, before anything has been measured. A GPU has no guess: it
                                                # is some tens of times faster, by how much depends on the GPU
USED = 0.35                                     # of the most they may write, agents have written a third: they stop
                                                # when they submit, and most thoughts are short (desk_work)


def chunks(items: list, size: int) -> list[list]:
    return [items[i:i + size] for i in range(0, len(items), size)]


def thinking_budget(text: str) -> int | None:
    """`1024`, or `none` (no limit)."""
    return None if text.strip().lower() in ("none", "natural") else int(text)


# ---------------------------------------------------------------- run

def fill_new_fields(folder: Path):
    """An arm setting added to the code after a run was made is written into that run's saved arms at its
    default, which is what the run in fact used. Without this, every new setting would refuse to resume every
    older run. A saved setting is never changed, so an arm that does differ is still refused. A run made
    before agents' arms had the settings they have now (it has settings there no longer are) is left as it
    is: it is a record, and is refused."""
    from .swarm import Arm
    config = folder / "config.json"
    if not config.exists():
        return
    saved = json.loads(config.read_text())
    versions = ("harness", "contact", "workshop")           # of the code a run was made under: never filled in for it
    defaults = {k: v for k, v in json.loads(json.dumps(Arm("default").describe(), default=str)).items()
                if k not in ("name", "system", *versions)}
    changed = False
    for key, arm in saved["settings"].items():
        if key.startswith("arm:") and set(arm) <= set(defaults) | {"name", "system", *versions}:
            for field, value in defaults.items():
                if field not in arm:
                    arm[field], changed = value, True
    if changed:
        config.write_text(json.dumps(saved, indent=2) + "\n")


def estimate(arms, problems: int) -> str:
    """A rough upper bound on the model work ahead, before anything is recalled from the cache: agents are
    charged for what such agents have used of their steps, not for all of them, and a look for one more reply."""
    speeds = json.loads(SPEED.read_text()) if SPEED.exists() else {}

    def turns(arm) -> float:
        return arm.steps * (1 + (arm.looks.p if arm.looks is not None else 0))

    def speed(arm) -> float | None:
        return speeds.get(arm.model_of(0)) or GUESS.get(arm.model_of(0))

    def tokens(arm) -> float:
        each = (8000 if arm.thinking is None else arm.thinking) + arm.max_tokens      # a thought and a reply, in tokens
        return arm.agents * turns(arm) * each * USED

    calls = sum(arm.agents * turns(arm) for arm in arms)
    if not all(speed(arm) for arm in arms):          # a model that has not run on this machine: no time is made up for it
        return (f"up to {problems * calls:,.0f} model calls, very roughly {problems * sum(map(tokens, arms)):,.0f} tokens to "
                "write if none are recalled (no run here has timed this model yet)")
    return (f"up to {problems * calls:,.0f} model calls, very roughly "
            f"{problems * sum(tokens(arm) / speed(arm) for arm in arms) / 60:.0f} minutes if none are recalled")


def side_by_side(arms, batch: int | None, desks: int | None) -> tuple[int, int]:
    """How many problems are played side by side, and how many agents work at once where nobody reads anybody,
    when the command line does not say. On the Mac it is one problem and twelve agents, which is what its
    memory keeps in flight. On a GPU it is what the server writes side by side (../swarm_engine: `capacity`):
    as many whole problems as that holds, since under an arm with looks every agent of a problem is open at
    once."""
    from swarm_engine import backend_of
    room = None
    if all(backend_of(arm.model_of(0)) == "vllm" for arm in arms):
        from swarm_engine.vllm_server import capacity
        room = capacity(arms[0].model_of(0))
    if room is None:
        return batch or 1, desks or 12
    return batch or max(1, room // max(arm.agents for arm in arms)), desks or room


def at_least_one(text: str) -> int:
    """A count, as an option gives one: 1 or more."""
    try:
        value = int(text)
    except ValueError:
        value = 0
    if value < 1:
        raise argparse.ArgumentTypeError(f"a number of 1 or more, not {text!r}")
    return value


def packed_room(arms, most: int | None = None):
    """The room of the server that a run's pieces are packed into (packing.py), or None where a run is played a
    group of problems at a time: on the Mac, where the arms do not all run one model on a GPU, and where the
    server's plan is not known (the model's files are not on this machine). `most` is the most agents at work
    at once, if the command line says: then that is the whole of the rule, and tokens are not counted."""
    from swarm_engine import backend_of
    models = {arm.model_of(seat) for arm in arms for seat in range(arm.agents)}
    if len(models) != 1 or backend_of(next(iter(models))) != "vllm":
        return None
    from swarm_engine.vllm_server import room

    from .packing import FULL, PIECES, Room
    planned = room(next(iter(models)))
    if not planned or PIECES * max(arm.agents for arm in arms) < planned["max_num_seqs"]:
        return None                                         # so few agents a problem that the pieces played at once would not
    side = planned["max_num_seqs"]                          # fill the server: groups hold more of them
    return Room(None, side, most) if most else Room(FULL * planned["room_tokens"], side)


def play_packed(run, pieces: list, room, backend_here, python, seed: int, desks: int | None = None) -> int:
    """Play a run's pieces, as many at once as the server has room for (packing.py), and write each down as it
    ends. `backend_here()` is the backend of the thread that asks: every piece is played on a thread of its
    own. `desks` is how many agents of a piece work at once where nobody reads anybody. What is logged says
    which arm an agent is of, since agents of several arms stop in the same minute."""
    from .llm import WORKERS
    from .packing import AFewAtATime, pack, play_open

    lock, began, started = threading.Lock(), {}, time.time()
    seen = {"replies": 0, "stopped": 0, "said": time.time(), "played": 0}
    files = AFewAtATime(python, WORKERS) if python is not None else None

    def play_one(piece, stopped):
        def progress(episode, seat, has_stopped):
            with lock:
                seen["replies"] += 1
                seen["stopped"] += has_stopped
                if has_stopped:
                    run.say(f"  {piece.arm.name}: {episode.told(seat)}")
                elif time.time() - seen["said"] >= 60:
                    seen["said"] = time.time()
                    run.say(f"  ... {seen['replies']} replies taken, {seen['stopped']} agents have stopped, {room.open} are at work")
            if has_stopped:
                stopped(seat)
        return play_open(piece, backend_here(), files, seed, progress, desks)

    def begun(piece):
        began[id(piece)] = time.time()
        with lock:
            run.say(f"{piece} ({piece.agents} agents; {room.open} at work in all)")

    def ended(piece, episode):
        episode.close()                                     # here, on the main thread: marking answers needs it (play_open)
        for row in episode.post_rows():
            run.write("posts", row)
        for row in episode.look_rows():
            run.write("looks", row)
        for row in episode.call_rows():
            run.write("transcripts", row)
        run.write("episodes", episode.row())                # last: its presence is what marks the pair as done
        seen["played"] += 1
        rate, left = (time.time() - started) / seen["played"], len(pieces) - seen["played"]
        with lock:
            run.say(f"  {piece}: played in {(time.time() - began.pop(id(piece))) / 60:.1f} min. {left} of {len(pieces)} left, "
                    f"about {left * rate / 60:.0f} min to go")

    return pack(pieces, play_one, room, begun, ended)


def problems_of(args) -> list:
    """The problems a `lab run` command plays, in the order it plays them: the experiment's, or what the command
    line says in their place, and of those only the ones `--only` names. `lab cloud` shares these out over
    machines; `cmd_run` picks its own by the same lines, and a test holds the two to the same problems for
    every option that bears on them."""
    from .problems import names, select
    exp = experiment.load(args.experiment)
    count = exp.problems if args.problems is None else (args.problems or None)
    problems = select(names(args.benchmarks or exp.benchmarks), args.split or exp.split, count)
    return [p for p in problems if not args.only or p.id in args.only]


def cmd_run(args):
    from .problems import names, select
    from .swarm import play
    from .tracking import Run

    exp = experiment.load(args.experiment)
    unknown = [name for name in args.arms or [] if name not in exp.arms]
    if unknown:
        raise SystemExit(f"no arm {', '.join(unknown)} in {exp.name} (arms: {', '.join(exp.arms)})")
    changes = {key: getattr(args, key) for key in ("agents", "steps", "model", "max_tokens", "lines") if getattr(args, key) is not None}
    if args.thinking is not None:
        changes["thinking"] = thinking_budget(args.thinking)
    arms = [replace(exp.arms[name], **changes) for name in (args.arms or exp.arms)]
    for arm in arms:
        if arm.lines * 12 > arm.max_tokens:           # agents write 12 tokens a line: most files of that length would be cut off
            raise SystemExit(f"a file of {arm.lines} lines does not fit in a reply of {arm.max_tokens:,} tokens (agents write 12 "
                             f"tokens a line): give --max-tokens {round(arm.lines * 19.2):,}, the room 300 lines have in 5,760")
    benchmarks = names(args.benchmarks or exp.benchmarks)
    split = args.split or exp.split
    count = exp.problems if args.problems is None else (args.problems or None)
    name = args.name or ("dry" if args.dry_run else "main")
    settings = {"benchmarks": benchmarks, "split": split, "problems": count, "seed": args.seed, "dry_run": args.dry_run,
                **{f"arm:{arm.name}": arm.describe() for arm in arms}}
    problems = select(benchmarks, split, count)             # before the run's folder exists: no data, no run
    if not problems:
        raise SystemExit(f"no {split} problems in {', '.join(benchmarks)} (only aime_2024 and gpqa_diamond have a train split)")
    if args.only:
        missing = [i for i in args.only if i not in {p.id for p in problems}]
        if missing:
            raise SystemExit(f"--only {' '.join(missing)}: not among the {len(problems)} problems this run is about")
        problems = [p for p in problems if p.id in args.only]
    folder = exp.folder / "runs" / name
    fill_new_fields(folder)
    done = {(e["arm"], e["benchmark"], e["problem"]) for e in (Run(folder).read("episodes") if (folder / "config.json").exists() else [])}
    left = sum((arm.name, p.benchmark, p.id) not in done for arm in arms for p in problems)
    if left and not args.dry_run:
        from swarm_engine import under_lock
        under_lock(mem_gb=args.mem_gb)            # re-runs this command under the machine-wide model lock
    run = Run(folder, settings, may_change=("benchmarks", "problems"), may_add=("arm:",))
    run.say(f"{len(problems)} problems x {len(arms)} arms ({', '.join(a.name for a in arms)}); {left} still to play")
    # on a GPU a run is packed into its server's room (packing.py) unless the command line asks for groups (--batch)
    room = packed_room(arms, getattr(args, "open", None)) if left and not args.dry_run and args.batch is None else None
    args.batch, args.desks = side_by_side(arms, args.batch, args.desks) if left and not args.dry_run else (args.batch or 1, args.desks or 12)
    for stream in ("posts", "looks", "transcripts"):        # what a stop left half written is written again, not twice
        run.keep(stream, lambda row: (row["arm"], row["benchmark"], row["problem"]) in done)

    from .sandbox import Python
    python = Python()
    if (why := python.ready()) is not None:
        if not args.dry_run:
            raise SystemExit(f"agents run Python, but there is {why}")
        python = None
    if args.dry_run or not left:                  # nothing left to play: the tables are rebuilt without a model
        from .llm import Scripted
        backend = Scripted(problems, stay=3)      # they stay at their desks a few steps, so that there is something to read
    else:
        from .llm import Engine, Memo
        backend = Engine(Memo(None) if args.no_cache else Memo(), record=lambda row: run.write("engine", row), say=run.say)
        if left:
            run.say(estimate(arms, len(problems)))

    def progress():                               # agents at their own pace: a line as each one stops, and one a minute
        seen = {"replies": 0, "stopped": 0, "said": time.time()}

        def report_reply(episode, seat, stopped):
            seen["replies"] += 1
            seen["stopped"] += stopped
            if stopped:
                run.say("  " + episode.told(seat))
            elif time.time() - seen["said"] >= 60:
                seen["said"] = time.time()
                run.say(f"  ... {seen['replies']} replies taken, {seen['stopped']} agents have stopped")
        return report_reply

    started, played = time.time(), 0
    if room is not None:
        from .llm import Engine
        from .packing import Piece
        pieces = [Piece(arm, p) for arm in arms for p in problems if (arm.name, p.benchmark, p.id) not in done]
        first = backend._engine(arms[0].model_of(0))        # loaded here, once: a server is started now if none is named,
        if getattr(first, "url", None):                     # and the engines of the pieces use that one
            from swarm_engine.vllm import URL
            if not os.environ.get(URL):                     # unset, or set to nothing, which an engine reads as unset
                os.environ[URL] = first.url
        here, made, writing, loading = threading.local(), [], threading.Lock(), threading.Lock()

        def record(row):
            with writing:
                run.write("engine", row)

        def backend_here():
            if not hasattr(here, "backend"):                # a thread's own engine: they share the server and the kept replies
                engine = Engine(backend.memo, record=record, say=lambda line: None)
                with loading:                               # one at a time: each reads the tokenizer's files and asks the server who it is
                    engine._engine(arms[0].model_of(0))
                    made.append(engine)
                here.backend = engine
            return here.backend

        run.say(f"{len(pieces)} pieces, a problem under an arm each, as many at once as the server keeps hold of: {room.most} agents at work at "
                f"most" + (f", counted at {room.tokens:,.0f} tokens of conversation at most" if room.tokens else " (--open)")
                + f"; the server writes {room.side} at a time")
        play_packed(run, pieces, room, backend_here, python, args.seed, args.desks)
        for engine in made:                                 # what the pieces' engines did is the run's
            backend.calls += engine.calls
            backend.generated += engine.generated
            backend.tokens += engine.tokens
            backend.read += engine.read
            backend.spared += engine.spared
        backend.seconds = time.time() - started             # on the clock: the pieces' own seconds overlap
        run.say(f"  the most agents at work at once: {room.widest}")
    else:
        for batch in chunks(problems, args.batch):
            for arm in arms:
                mine = [p for p in batch if (arm.name, p.benchmark, p.id) not in done]
                if not mine:
                    continue
                together = len(mine) * arm.agents if arm.looks is not None else min(args.desks, len(mine) * arm.agents)
                run.say(f"{arm.name}: {', '.join(p.key for p in mine)} ({together} agents at work at once)")
                began = time.time()
                for episode in play(mine, arm, backend, python, args.seed, progress(), args.desks):
                    for row in episode.post_rows():
                        run.write("posts", row)
                    for row in episode.look_rows():
                        run.write("looks", row)
                    for row in episode.call_rows():
                        run.write("transcripts", row)
                    run.write("episodes", episode.row())        # last: its presence is what marks the pair as done
                played += len(mine)
                rate = (time.time() - started) / played
                run.say(f"  {arm.name}: {len(mine)} problems in {(time.time() - began) / 60:.1f} min. {left - played} of {left} left; "
                        f"{rate / 60:.1f} min per (arm, problem), about {(left - played) * rate / 60:.0f} min to go")

    if left and not args.dry_run and backend.generated:
        speeds = json.loads(SPEED.read_text()) if SPEED.exists() else {}
        speeds[arms[0].model_of(0)] = round(backend.tokens / max(backend.seconds, 1e-9), 1)
        SPEED.parent.mkdir(parents=True, exist_ok=True)
        SPEED.write_text(json.dumps(speeds, indent=2) + "\n")
        run.say(f"model: {backend.generated} calls generated, {backend.calls - backend.generated} recalled, "
                f"{backend.tokens:,} tokens in {backend.seconds / 60:.1f} min ({backend.tokens / max(backend.seconds, 1e-9):.0f} a second); "
                f"{backend.read:,} tokens read, {backend.spared:,} not read again")
    if python is not None:
        run.say(f"Python: {python.asked} runs of a file, {python.recalled} recalled")
        python.close()

    wanted = {(p.benchmark, p.id) for p in problems}
    episodes = [e for e in run.read("episodes") if (e["benchmark"], e["problem"]) in wanted]
    summary = report.summary_of(episodes, report.baseline_of(run.config["settings"]))
    run.save("summary", summary)
    run.path("summary.md").write_text(report.tables(summary) + "\n\n" + report.NOTES + " " + report.DESK_NOTES + "\n")
    run.say("\n" + report.tables(summary, more=False) + "\n")
    run.finish()
    if not args.dry_run:
        update_standings(run)


def update_standings(run):
    """CURRENT.md's tables of approaches and runs are written again, now that this run is one of them. The run
    is whole without that, so a failure here is said and does not undo it."""
    from . import standings
    try:
        run.say(standings.write(strict=False))
    except Exception as error:                              # a run folder the tables cannot read: the run itself is saved
        run.say(f"the standings in CURRENT.md were not written ({type(error).__name__}: {error}): uv run lab standings --write")


# ---------------------------------------------------------------- reading

def cmd_show(args):
    run = report.find(args.run)
    if args.trace:
        print(report.trace(run, args.arm, args.problem, args.agent, args.files))
    elif args.problem:
        print(report.problem(run, args.problem, args.arm, args.benchmark, args.thoughts, args.prompts, args.agent))
    elif args.list or args.where:
        print(report.listing(run, args.arm, args.where, args.benchmark))
    else:
        print(report.overview(run, args.shared, args.benchmark, args.arm, args.more))


def cmd_compare(args):
    print(report.compare([report.find(run) for run in args.runs]))


def cmd_plot(args):
    from .figures import pairs, steps
    run = report.find(args.run)
    print(steps(run))
    print(pairs(run))


def cmd_ls(args):
    from . import standings
    print(standings.listing())


def cmd_standings(args):
    from . import standings
    print(standings.write() if args.write else standings.tables(everything=args.all))


def cmd_new(args):
    folder = experiment.new(args.name, args.question)
    print(f"wrote {folder.relative_to(ROOT)}/: edit experiment.py, then `lab run {args.name} --dry-run`")


def cmd_data(args):
    from . import benchmarks
    benchmarks.main()


def cmd_current(args):
    from . import current
    if args.write:
        print(current.write())
    else:
        print(current.table())


def cmd_python(args):
    from .sandbox import Python
    code = Path(args.code).read_text() if Path(args.code).is_file() else args.code
    python = Python(cache=None)
    ran = python.check(code)
    python.close()
    print(f"{ran.status} ({ran.seconds:.1f}s)\n\n{ran.told()}")
    sys.exit(0 if ran.ok else 1)


def downloaded(name: str) -> bool:
    """Whether a model's weights are in this machine's Hugging Face cache: a real file, not a link to a missing one."""
    import os
    hub = Path(os.environ.get("HF_HOME") or Path.home() / ".cache/huggingface") / "hub"
    return any(f.exists() and f.stat().st_size > 2**27
               for f in (hub / ("models--" + name.replace("/", "--"))).glob("snapshots/*/model*.safetensors"))


def doctor_gpu(ok) -> bool:
    """What a machine with a GPU needs to run a model: the GPU, vLLM in the version this was held against, and
    (not needed beforehand) the model's files."""
    from swarm_engine import KNOWN
    from swarm_engine.vllm import gpu
    from swarm_engine.vllm_server import VERSION, capacity, driver, find
    card, program = gpu(), find()
    good = ok(bool(card), f"a GPU: {card['name']}, {card['memory_gb']:g} GiB, driver {driver()}" if card else "a GPU (nvidia-smi names none)",
              "a bf16 model needs one")
    has = ""
    if program is not None:
        has = subprocess.run([str(Path(program).parent / "python"), "-c", "from importlib.metadata import version; print(version('vllm'))"],
                             capture_output=True, text=True).stdout.strip()
    good &= ok(has.split("+")[0] == VERSION, f"vLLM {VERSION} is installed" + (f" (found {has} at {program})" if has else ""),
               "uv run swarm-vllm install")
    for alias in ("9B-bf16", "4B-bf16"):
        room = capacity(alias)
        ok(downloaded(KNOWN[alias].repo), f"model {alias} ({KNOWN[alias].repo}) is downloaded"
           + (f": this GPU has room to write {room} conversations side by side" if room else ""),
           f"the engine downloads it on first use (about {KNOWN[alias].weights_gb + 1.3:.0f} GB)")
    return good


def cmd_doctor(args):
    """Everything a run needs, checked without loading a model."""
    from swarm_engine import available_gb
    from .sandbox import Python

    def ok(found: bool, what: str, fix: str = ""):
        print(f"{'ok  ' if found else 'MISS'}  {what}" + (f"\n      -> {fix}" if not found and fix else ""))
        return found

    good, mac = True, sys.platform == "darwin"
    if mac:
        for alias, name in (("9B", "mlx-community/Qwen3.5-9B-4bit"), ("4B", "mlx-community/Qwen3.5-4B-4bit")):
            found = ok(downloaded(name), f"model {alias} ({name}) is downloaded", "the engine downloads it on first use (about 5 GB)")
            good &= found or alias != "9B"
    else:
        good &= doctor_gpu(ok)
    good &= ok((BENCHMARKS / "problems").exists() and len(list((BENCHMARKS / "problems").glob("*.jsonl"))) == 11,
               "benchmarks are built (data/benchmarks/problems)", "lab data")
    python = Python(cache=None)
    why = python.ready()
    good &= ok(why is None, "there is a sandbox for agents' Python" + (f": {why}" if why else ""))
    if why is None:
        ran = python.check("import numpy, sympy\nprint(sympy.factorint(42))")
        good &= ok(ran.ok and ran.output == "{2: 1, 3: 1, 7: 1}\n", f"Python runs a file in its sandbox ({ran.seconds:.1f}s, {ran.status})")
        leaks = python.leaks()
        good &= ok(not leaks, "that sandbox refuses files, the network, other programs and signals"
                   + (f": but a file could {'; '.join(leaks)}" if leaks else ""))
    python.close()
    holder = subprocess.run(["pgrep", "-fl", "swarm_engine.ml_run|scripts/ml_run.py"], capture_output=True, text=True).stdout.strip()
    ok(not holder, "no model job is running (the machine lock is free)" + (f": {holder[:120]}" if holder else ""),
       "a new run will wait in line behind it")
    free = available_gb()
    if mac:
        ok(free >= 12, f"{free:.0f} GB of memory available (a run waits for 12; a swarm run is given 28)", "close something large")
        battery = subprocess.run(["pmset", "-g", "batt"], capture_output=True, text=True).stdout
        ok("AC Power" in battery, "on mains power", "plug in before a long run")
    else:
        ok(free >= 12, f"{free:.0f} GB of memory available")
    disk = shutil.disk_usage(ROOT).free / 2**30
    ok(disk > 20, f"{disk:.0f} GB of disk free")
    sys.exit(0 if good else 1)


# ---------------------------------------------------------------- the command line

def parser() -> argparse.ArgumentParser:
    """The `lab` command line. `lab cloud` reads a `lab run` command with it too, so that it takes one as `lab run` does."""
    parser = argparse.ArgumentParser(prog="lab", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)

    run = commands.add_parser("run", help="run an experiment's arms on its problems")
    run.add_argument("experiment")
    run.add_argument("--name", help="this run's folder under the experiment's runs/ (default: main, or dry for --dry-run)")
    run.add_argument("--arms", nargs="+", help="only these arms (default: all of the experiment's)")
    run.add_argument("--benchmarks", nargs="+", help="benchmarks or suites (math, logic, all) instead of the experiment's")
    run.add_argument("--split", choices=["train", "test"])
    run.add_argument("--problems", type=int, metavar="N", help="problems per benchmark, the first N of a fixed order (0: all)")
    run.add_argument("--only", nargs="+", metavar="ID", help="of those problems, play only these now (by id)")
    run.add_argument("--seed", type=int, default=0, help="a new seed is a new, independent draw of every reply")
    run.add_argument("--batch", type=int, help="problems played side by side, a group at a time (results are saved per group). "
                     "Default: 1 on the Mac. On a GPU a run is not played in groups unless this is given: each problem "
                     "under each arm begins as soon as the server has room for its agents")
    run.add_argument("--open", type=at_least_one, metavar="N", help="on a GPU, without --batch: the most agents at work at once "
                     "(default: as many as its server keeps hold of, counted by how long their conversations get)")
    run.add_argument("--dry-run", action="store_true", help="scripted stand-ins instead of a model: no lock, seconds")
    run.add_argument("--no-cache", action="store_true", help="generate every reply afresh and keep none")
    swarm = run.add_argument_group("change every arm (for a pilot; give the run its own --name)")
    swarm.add_argument("--agents", type=int)
    swarm.add_argument("--steps", type=int)
    swarm.add_argument("--model")
    swarm.add_argument("--thinking", metavar="TOKENS", help="a number, 0 for none, or 'none' for no limit")
    swarm.add_argument("--max-tokens", type=int)
    swarm.add_argument("--lines", type=int, help="how long an agent's file may be (300). A file needs --max-tokens to hold "
                       "it: 19.2 tokens a line, as 300 lines have in 5,760. Runs before 2026-10-12 are of --steps 12 "
                       "--lines 80 --max-tokens 1536 unless they say otherwise")
    machine = run.add_argument_group("this machine (not part of a run's identity)")
    machine.add_argument("--mem-gb", type=float, default=20, help="memory budget for the model, of this laptop's 48 GB (a swarm run: 28). "
                         "A GPU's memory is shared out by its server, not by this")
    machine.add_argument("--desks", type=int, help="agents at work at once under an arm in which nobody reads anybody: the rest begin as "
                         "these stop (default: 12 on the Mac; on a GPU, what its server has room for). An arm with looks opens "
                         "every agent of its problems at once")
    run.set_defaults(go=cmd_run)

    show = commands.add_parser("show", help="read a run")
    show.add_argument("run", help="experiment/run, or a run's folder")
    show.add_argument("--more", action="store_true", help="also: agents right after each step, what they did with their tools, the cost")
    show.add_argument("--shared", action="store_true", help="the tables on only the problems every arm has played")
    show.add_argument("--list", action="store_true", help="one line per (arm, problem)")
    show.add_argument("--where", choices=sorted(report.WHERE), help="with --list: only these")
    show.add_argument("--problem", metavar="ID", help="one problem, step by step")
    show.add_argument("--arm")
    show.add_argument("--benchmark")
    show.add_argument("--agent", type=int, help="with --problem or --trace: only this agent")
    show.add_argument("--thoughts", action="store_true", help="with --problem: each agent's private thinking and what its tools said")
    show.add_argument("--prompts", action="store_true", help="with --problem: what each call was shown")
    show.add_argument("--trace", action="store_true", help="every agent, a line a step: tools, what came of them, files read, the answer held")
    show.add_argument("--files", action="store_true", help="with --trace: the file that printed each agent's answer")
    show.set_defaults(go=cmd_show)

    compare = commands.add_parser("compare", help="arms of several runs on the problems they share")
    compare.add_argument("runs", nargs="+")
    compare.set_defaults(go=cmd_compare)

    plot = commands.add_parser("plot", help="write a run's figures: agents right and answers held after each step, and how the pairs of a problem's agents ended")
    plot.add_argument("run")
    plot.set_defaults(go=cmd_plot)

    commands.add_parser("ls", help="every experiment and run, finished or not").set_defaults(go=cmd_ls)

    standings = commands.add_parser("standings", help="every approach's numbers, added up over its runs, and every finished run")
    standings.add_argument("--all", action="store_true", help="also what was run only under earlier versions and left behind")
    standings.add_argument("--write", action="store_true", help="write the tables into CURRENT.md")
    standings.set_defaults(go=cmd_standings)

    new = commands.add_parser("new", help="start an experiment from the template")
    new.add_argument("name")
    new.add_argument("question", nargs="?", default="")
    new.set_defaults(go=cmd_new)

    current = commands.add_parser("current", help="what the baseline and the swarm are now, from the code")
    current.add_argument("--write", action="store_true", help="write it into CURRENT.md")
    current.set_defaults(go=cmd_current)

    commands.add_parser("data", help="build the benchmarks").set_defaults(go=cmd_data)
    commands.add_parser("doctor", help="check this machine is ready").set_defaults(go=cmd_doctor)

    python = commands.add_parser("python", help="run Python the way an agent's file is run, and print what the agent is told")
    python.add_argument("code", help="Python code, or a file of it")
    python.set_defaults(go=cmd_python)

    from . import cloud
    cloud.add_commands(commands)
    return parser


def main():
    args = parser().parse_args()
    args.go(args)


if __name__ == "__main__":
    main()
