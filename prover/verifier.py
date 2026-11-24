"""The verifier: the archive's stopping condition since 2026-11-06 (in place of REPORT + MANAGER), and the stop bench's
`verify` system (stop_systems.py), where it decided all 39 items right on two runs.

Two stages:
1. The gate (CONTRACT, DEFINITE, RESULT). Once per problem, from the question alone, the form a complete answer takes;
   then whether the answer a team was told has that form. A hedge (bounds, "unknown", a conditional) can't pass,
   however well proved. An answer that has the form is asked about once more (RESULT, since 2026-11-23): is it the
   result itself, or a procedure for finding it (the problem's definition turned into a calculation left to be carried
   out)? A procedure can't pass either: before, two archives ended on one, soundly proved (p1024, p1028).
2. The verifier (VERIFY): an agent of the swarms' model, at effort high, with the whole record of the team: its
   workspace, each agent's folder, its whole channel, each agent's last reply and whole transcript rendered as text
   (record/). It reruns the team's code in the Sandbox, the record read-only, and gives a verdict: sound, gap, false
   or unfinished; and whether the team itself acknowledged a gap in its final proof.
Stop iff the answer is definite, the verdict is sound and the team acknowledged no gap.

A record is a swarm's folder (Record): agents/<name>/conversation.json (earlier parts conversation.<i>.json), slack.jsonl,
workspace/. stop_bench.Item has the same methods.

A team that was not told an answer (swarm_untold.py) is verified on the answer it ended with (VERIFY_UNTOLD).

A lone agent's record (swarm_play.Swarm `solo`, the individual baseline) has no channel and no workspace: channel.md
then holds what the agent wrote each time it stopped and what its lead answered, and the task says so (VERIFY_SOLO,
VERIFY_UNTOLD_SOLO: only the sentences that describe the record change, the steps and verdicts are VERIFY's).
"""

import json
import re
from dataclasses import replace
from pathlib import Path

from replies import parse

CONTRACT = """Below is a math problem. Before anyone works on it, state what a complete answer to its question must be: the form it takes (for example a single integer, a closed formula in the problem's parameters, yes or no, an explicit object), so that a reader can tell whether a proposed answer settles the question.

A range, bounds, "unknown", "not determined", an answer conditional on a conjecture, or an answer for only some cases does not settle a question that asks for one value or one formula, unless the question itself asks for bounds, allows several cases, or asks whether something is determined.

<problem>
{problem}
</problem>

Reply with one JSON object, in a ```json block, and nothing else: {{"form": "<what a complete answer is, in a sentence or two>", "not_enough": "<what kinds of answer would not settle it>"}}."""

DEFINITE = """Below is a math problem, the form a complete answer to it takes, and a proposed answer. Decide whether the proposed answer, as stated, has that form: whether, if it were true, it would settle the question. Judge only its form: the answer comes alone, its proof is checked elsewhere, so ignore whatever the form says about justification, and don't ask whether it is true.

<problem>
{problem}
</problem>

A complete answer: {form}
Not enough: {not_enough}

The proposed answer: {answer}

Reply with one JSON object, in a ```json block, and nothing else: {{"definite": true or false, "reason": "<briefly, why>"}}."""

RESULT = """Below is a math problem and an answer someone proposes to it. Suppose the answer is true and has been fully proved. Decide whether it is what the problem set out to find: would the person who posed the problem accept it as the answer, or would they say that the problem is still to be solved? Don't ask whether the answer is true. The answer must be the result itself, not a procedure for finding it. If the proposed answer just turns the problem's own definition into a calculation and leaves that calculation for the reader to carry out, then the problem has not been solved. That is true even if the calculation is correct, finishes in a finite number of steps, and is written as one formula.

<problem>
{problem}
</problem>

The proposed answer: {answer}

Reply with one JSON object, in a ```json block, and nothing else: {{"accepted": true or false, "reason": "<briefly, why>"}}, where "accepted" is true if the person who posed the problem would accept it as the answer."""


def text_of(content):
    return content if isinstance(content, str) else "".join(b.get("text", "") for b in content if isinstance(b, dict))


class Record:
    """A swarm's folder, as the verifier reads it."""

    def __init__(self, folder):
        self.path = Path(folder)
        f = self.path / "settings.json"
        self.solo = bool(json.loads(f.read_text()).get("solo")) if f.exists() else False  # a lone agent's run

    def rows(self):
        f = self.path / "slack.jsonl"
        return [json.loads(l) for l in f.read_text().splitlines() if l.strip()] if f.exists() else []

    def channel(self):
        return "\n\n".join(f"#{r['id']} {r['sender']}" + (f" (in thread #{r['thread']})" if r.get("thread") else "")
                           + f": {r['body']}" for r in self.rows())  # fmt: skip

    def agents(self):
        return sorted(p.name for p in (self.path / "agents").iterdir() if p.is_dir())

    def conversation(self, agent):
        folder = self.path / "agents" / agent
        parts = sorted(folder.glob("conversation.*.json"), key=lambda p: int(p.name.split(".")[1]))
        msgs = []
        for p in [*parts, folder / "conversation.json"]:
            if p.exists():
                msgs += json.loads(p.read_text())["messages"]
        return msgs

    def final(self, agent):
        f = self.path / "agents" / agent / "conversation.json"
        msgs = json.loads(f.read_text())["messages"] if f.exists() else []
        return next((text_of([b for b in m["content"] if b.get("type") == "text"]) for m in reversed(msgs)
                     if m["role"] == "assistant" and any(b.get("type") == "text" and b.get("text")
                                                         for b in m["content"])), "")  # fmt: skip

    def workspace(self):
        return self.path / "workspace"


VERIFY_SYSTEM = "You are a careful research mathematician who referees claimed proofs, including their code."

VERIFY = """<problem>
{problem}
</problem>

A complete answer to this problem: {form}

A team of {n} agents was told that the answer is {answer} and asked to prove it{halves}, writing Python that checks every step. Their run ended: {reason}. The answer they were told may be wrong: teams told a wrong answer sometimes stop at bounds or partial results, and sometimes claim a proof anyway. You decide whether this team proved {answer}: whether a search for the answer can stop here and report {answer} as proved.

Their whole record is in your folder, read-only:
- record/prompt.md: what the team was told.
- record/channel.md: their Slack channel (#proof), every post in order.
- record/finals.md: each agent's last reply, often its write-up.
- record/transcripts/<agent>.md: each agent's whole run: its reasoning summaries, its messages, every file it wrote and ran, and what each run printed.
- workspace/: the folder the team shared, as they left it (code, data, certificates, write-ups).
- agents/<agent>/: each agent's own folder (its scratchpad.py and files).

Your tools: list_files, read_file, grep, write_file (files of your own folder; not inside record/, workspace/ or agents/), and run_python, which runs a Python file of your folder in a sandbox with the team's libraries (NumPy, SciPy, SymPy, mpmath, NetworkX, Sage via passagemath, ...), no network, up to {run_seconds} s a run. A run can read workspace/ and agents/ but not change them: to rerun a team's script that writes files, copy it into your folder and change where it writes. Its working directory is your folder, so `sys.path.insert(0, "workspace")` imports the team's shared code.

Do this:
1. Find what the team claims at the end: a complete proof of {answer}, or less (bounds, a partial result, a reduction, a result conditional on something unproved, or no conclusion). Start from record/finals.md and the end of record/channel.md.
2. If they claim a complete proof, reconstruct the final proof and find its decisive steps: those that force {answer} rather than another answer. Check each:
   - an argument written out: check it yourself;
   - a computation: read the code and check that it computes what the step needs (the right objects, the right field or precision, nothing assumed that is to be shown); rerun it, or its decisive part, when that is feasible, rather than trusting the reported output;
   - a cited result: whether it is a precise statement whose hypotheses hold here. Your recollection of the literature is no better evidence than the team's: a citation that was questioned in the record and settled only by agents recalling or agreeing is not settled.
3. Find whether the team itself acknowledged a gap in the final proof: a step it said it could not verify, a citation it could not pin down or whose hypotheses it was unsure hold here, a result left conditional, an objection to a step of the final proof answered by agreement rather than by evidence. Read the end of the channel and the last replies, and follow every objection to a step of the final proof through the channel and the transcripts. Doubts about routes the final proof doesn't use don't count, nor do early doubts that the final proof settles by its own steps.

Then call give_verdict:
- sound: a complete proof of {answer}, perhaps with gaps a competent reader fills routinely (a standard estimate, a routine check, a citation that applies as stated);
- gap: they claim a complete proof, but a substantive step is missing, only asserted, left conditional on an unproved claim, or rests on a computation that doesn't establish what the step needs;
- false: a step of the claimed proof is wrong;
- unfinished: they don't claim a complete proof of {answer}.

You have about {responses} responses; spend them on the decisive steps."""

# For a team that was not told an answer (swarm_untold.py): VERIFY with the sentences on what the team was told
# replaced; `answer` is then the answer the team ended with, as its record was read (swarm_untold.ANSWER_ASK).
TOLD = "A team of {n} agents was told that the answer is {answer} and asked to prove it{halves}, writing Python that checks every step. Their run ended: {reason}. The answer they were told may be wrong: teams told a wrong answer sometimes stop at bounds or partial results, and sometimes claim a proof anyway."
UNTOLD = "A team of {n} agents was asked to find the answer, which they were not told, and to prove it, writing Python that checks every step. Their run ended: {reason}. Read from their record, the answer they ended with is {answer}. It may be wrong, and they may not have proved it: teams sometimes stop at bounds or partial results, and sometimes claim a proof of a wrong answer anyway."
VERIFY_UNTOLD = VERIFY.replace(TOLD, UNTOLD)
assert VERIFY_UNTOLD != VERIFY


def reworded(text, pairs):
    for old, new in pairs:
        assert old in text, f"not in the prompt: {old!r}"
        text = text.replace(old, new)
    return text


# For a lone agent's record (Record.solo): what was asked of whom, and what the record holds. The steps and the
# verdicts stay VERIFY's, with "the team" read as that agent.
ONE = ' Below, "the team" is this one agent: it had no partners, no Slack channel and no shared workspace.'
TOLD_SOLO = ("One agent, working alone, was told that the answer is {answer} and asked to prove it{halves}, writing Python that "
             "checks every step. Its run ended: {reason}. The answer it was told may be wrong: agents told a wrong answer "
             "sometimes stop at bounds or partial results, and sometimes claim a proof anyway.") + ONE  # fmt: skip
UNTOLD_SOLO = ("One agent, working alone, was asked to find the answer, which it was not told, and to prove it, writing Python "
               "that checks every step. Its run ended: {reason}. Read from its record, the answer it ended with is {answer}. "
               "It may be wrong, and it may not have proved it: agents sometimes stop at bounds or partial results, and "
               "sometimes claim a proof of a wrong answer anyway.") + ONE  # fmt: skip
RECORD_SOLO = [
    ("- record/channel.md: their Slack channel (#proof), every post in order.",
     "- record/channel.md: what the agent wrote each time it stopped (often its write-up), and what its lead answered "
     "(a nudge, when it stopped short), in order."),
    ("- record/finals.md: each agent's last reply, often its write-up.", "- record/finals.md: the agent's last reply."),
    ("- workspace/: the folder the team shared, as they left it (code, data, certificates, write-ups).\n", ""),
    ("- agents/<agent>/: each agent's own folder (its scratchpad.py and files).",
     "- agents/<agent>/: the agent's folder, as it left it (its scratchpad.py and the files its runs wrote: code, data, "
     "certificates, write-ups)."),
    ("(files of your own folder; not inside record/, workspace/ or agents/)", "(files of your own folder; not inside record/ or agents/)"),
    ("A run can read workspace/ and agents/ but not change them:", "A run can read agents/ but not change it:"),
    ("so `sys.path.insert(0, \"workspace\")` imports the team's shared code.",
     "so `sys.path.insert(0, \"agents/<agent>\")` imports the agent's code."),
]  # fmt: skip
VERIFY_SOLO = reworded(VERIFY, [(TOLD, TOLD_SOLO), *RECORD_SOLO])
VERIFY_UNTOLD_SOLO = reworded(VERIFY, [(TOLD, UNTOLD_SOLO), *RECORD_SOLO])

VERIFY_TOOLS = [
    {"name": "list_files", "description": "List the files under a folder of yours (record/, workspace/, agents/, or your own), with sizes, to a depth.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string", "description": "Default '.'."},
                                                       "depth": {"type": "integer", "minimum": 1, "maximum": 6, "description": "Default 2."}}}},
    {"name": "read_file", "description": "Read a text file, its lines numbered. At most 40,000 characters a call: use start_line and end_line for long files.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "start_line": {"type": "integer", "minimum": 1},
                                                       "end_line": {"type": "integer", "minimum": 1}}, "required": ["path"]}},
    {"name": "grep", "description": "Search the text files under a path for a regular expression (Python re, case-insensitive). Returns path:line: text, at most max_matches.",
     "input_schema": {"type": "object", "properties": {"pattern": {"type": "string"}, "path": {"type": "string", "description": "Default '.'."},
                                                       "max_matches": {"type": "integer", "minimum": 1, "maximum": 300, "description": "Default 80."}}, "required": ["pattern"]}},
    {"name": "write_file", "description": "Write a file in your own folder (not inside record/, workspace/ or agents/), replacing it if it exists.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}},
    {"name": "run_python", "description": "Run a Python file of your folder in the sandbox, from your folder, and return its exit code, time, stdout and stderr (long output cut in the middle).",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "timeout_seconds": {"type": "integer", "minimum": 1,
                                                       "description": "Default 300."}}, "required": ["path"]}},
    {"name": "give_verdict", "description": "Your verdict, which ends your review.",
     "input_schema": {"type": "object", "properties": {
         "claimed": {"type": "string", "description": "What the team claims at the end, in a sentence."},
         "verdict": {"type": "string", "enum": ["sound", "gap", "false", "unfinished"]},
         "team_acknowledged_gap": {"type": "boolean", "description": "Whether the team itself acknowledged a gap in the final proof (step 3)."},
         "acknowledged_where": {"type": "string", "description": "Where (post numbers, agent) and what, or empty."},
         "decisive_steps": {"type": "array", "items": {"type": "object", "properties": {
             "step": {"type": "string"}, "basis": {"type": "string", "enum": ["argument", "computation", "citation", "recollection", "missing"]},
             "checked": {"type": "string", "description": "What you did to check it and what you found (reran X: matches; read the argument: holds; ...)."}}}},
         "failing_step": {"type": "string", "description": "The step that fails, or for a sound proof the one you found hardest."},
         "reason": {"type": "string", "description": "Briefly, why."}},
         "required": ["claimed", "verdict", "team_acknowledged_gap", "reason"]}},
]  # fmt: skip

VERIFY_RESPONSES = 80
VERIFY_BUDGET = 6.0  # dollars an item
VERIFY_CONTEXT = 250_000  # input tokens past which it is asked for its verdict (below long-context pricing)
VERIFY_RUN_SECONDS = 1200
VERIFY_READ_CHARS = 40_000
VERIFY_OUT_CHARS = 20_000
VERIFY_NUDGE = "Give your verdict now with give_verdict, from what you have checked."
def cut_middle(s, n):
    return s if len(s) <= n else s[: n // 2] + f"\n... ({len(s) - n:,} characters cut) ...\n" + s[-n // 2:]


def render_transcript(item, agent):
    lines, k = [f"# {agent}: the whole run", ""], 0
    for m in item.conversation(agent):
        c = m["content"]
        if isinstance(c, str):
            who = "notice" if m["role"] == "system" else "user message"
            lines += [f"[{who}]", c, ""]
            continue
        if m["role"] == "assistant":
            k += 1
            lines.append(f"## response {k}")
        for b in c:
            t = b.get("type")
            if t == "thinking" and b.get("thinking"):
                lines += ["[reasoning summary]", b["thinking"], ""]
            elif t == "text" and b.get("text"):
                lines += ["[message]", b["text"], ""]
            elif t == "tool_use":
                inp = b.get("input") if isinstance(b.get("input"), dict) else {"input": b.get("input")}
                lines.append(f"[tool call: {b.get('name')}]")
                for key, v in inp.items():
                    v = v if isinstance(v, str) else json.dumps(v)
                    lines += [f"{key}:", "```", v, "```"] if "\n" in v or len(v) > 200 else [f"{key}: {v}"]
                lines.append("")
            elif t == "tool_result":
                out = b["content"] if isinstance(b["content"], str) else text_of(b["content"])
                lines += ["[tool result" + (", error]" if b.get("is_error") else "]"), "```", cut_middle(out, 12_000), "```", ""]
    return "\n".join(lines)


def prepare_box(item, folder):
    """The verifier's folder: record/ rendered, workspace/ and agents/ linked (read-only to its runs)."""
    box = folder / "box"
    rec = box / "record"
    (rec / "transcripts").mkdir(parents=True, exist_ok=True)
    first = item.conversation(item.agents()[0])[0]["content"]
    (rec / "prompt.md").write_text(first if isinstance(first, str) else str(first))
    (rec / "channel.md").write_text(item.channel() or "(nothing posted)")
    (rec / "finals.md").write_text("\n\n".join(f"# {a}: last reply\n\n{item.final(a) or '(none)'}" for a in item.agents()))
    for a in item.agents():
        (rec / "transcripts" / f"{a}.md").write_text(render_transcript(item, a))
    for name, target in (("workspace", item.workspace()), ("agents", item.path / "agents")):
        if name == "workspace" and getattr(item, "solo", False):  # a lone agent has none
            continue
        link = box / name
        if not link.is_symlink():
            target.mkdir(exist_ok=True)
            link.symlink_to(target.resolve(), target_is_directory=True)
    return box


class VerifyTools:
    def __init__(self, item, box, sandbox):
        self.item, self.box, self.sandbox = item, box.resolve(), sandbox
        self.shown = {"agents/": (item.path / "agents").resolve()}  # the team's folders, as they are shown
        if not getattr(item, "solo", False):  # a lone agent has no workspace
            self.shown = {"workspace/": item.workspace().resolve(), **self.shown}
        self.read_roots = [self.box, *self.shown.values()]
        self.runs = 0

    def where(self, path, write=False):
        p = (self.box / (path or ".")).resolve() if not Path(path or ".").is_absolute() else Path(path).resolve()
        if write:
            ok = p.is_relative_to(self.box) and not p.is_relative_to(self.box / "record") and not (self.box / ".home") in p.parents
            if not ok:
                raise ValueError("you can write only files of your own folder (not record/, workspace/ or agents/)")
        elif not any(p == r or p.is_relative_to(r) for r in self.read_roots):
            raise ValueError("outside your folder")
        return p

    def show(self, p):
        for r, name in ((self.box, ""), *((r, name) for name, r in self.shown.items())):
            if p.is_relative_to(r):
                return name + str(p.relative_to(r))
        return str(p)

    def list_files(self, path=".", depth=2):
        base = self.where(path)
        out = []

        def walk(d, level):
            for q in sorted(d.iterdir()):
                if q.name in (".home", "__pycache__") or len(out) > 400:
                    continue
                if q.is_dir():
                    out.append(f"{q.relative_to(base)}/")
                    if level < depth:
                        walk(q, level + 1)
                else:
                    out.append(f"{q.relative_to(base)}  ({q.stat().st_size:,} bytes)")

        walk(base, 1)
        return "\n".join(out[:400]) or "(empty)"

    def read_file(self, path, start_line=1, end_line=None):
        p = self.where(path)
        if p.stat().st_size > 200 * 2**20:
            return f"{path} is {p.stat().st_size:,} bytes: read it with run_python."
        lines = p.read_text(errors="replace").splitlines()
        end = min(end_line or len(lines), len(lines))
        out, n = [], 0
        for i in range(start_line - 1, end):
            s = f"{i + 1}\t{lines[i]}"
            if n + len(s) > VERIFY_READ_CHARS:
                out.append(f"... (stopped at line {i}; {len(lines)} lines in all: read on with start_line={i + 1})")
                break
            out.append(s)
            n += len(s) + 1
        return "\n".join(out) or f"(no lines; {len(lines)} lines in all)"

    def grep(self, pattern, path=".", max_matches=80):
        rx = re.compile(pattern, re.I)
        base = self.where(path)
        files = [base] if base.is_file() else sorted(f for f in base.rglob("*") if f.is_file() and ".home" not in f.parts)
        out = []
        for f in files:
            if f.stat().st_size > 50 * 2**20 or f.suffix in (".pkl", ".npy", ".npz", ".sobj", ".db", ".gz", ".zip"):
                continue
            try:
                text = f.read_text(errors="strict")
            except (UnicodeDecodeError, OSError):
                continue
            for i, line in enumerate(text.splitlines(), 1):
                if rx.search(line):
                    out.append(f"{self.show(f.resolve())}:{i}: {line[:300]}")
                    if len(out) >= max_matches:
                        return "\n".join(out) + f"\n(stopped at {max_matches} matches)"
        return "\n".join(out) or "(no matches)"

    def write_file(self, path, content):
        p = self.where(path, write=True)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        return f"Wrote {self.show(p)} ({len(content):,} characters)."

    def run_python(self, path, timeout_seconds=300):
        p = self.where(path, write=True)
        ran = self.sandbox.run(self.box, str(p.relative_to(self.box)), min(timeout_seconds, VERIFY_RUN_SECONDS),
                                   read_only=self.read_roots[1:])  # fmt: skip
        self.runs += 1
        out = f"status: {ran.status}, exit code {ran.returncode}, {ran.seconds:.1f} s" + (f", at {ran.where}" if ran.where else "")
        return (out + f"\n<stdout>\n{cut_middle(ran.stdout, VERIFY_OUT_CHARS)}\n</stdout>\n"
                f"<stderr>\n{cut_middle(ran.stderr, VERIFY_OUT_CHARS // 2)}\n</stderr>")  # fmt: skip

    def handle(self, block):
        try:
            args = block.input if isinstance(block.input, dict) else {}
            out = getattr(self, block.name)(**args)
            return {"type": "tool_result", "tool_use_id": block.id, "content": out, "is_error": False}
        except Exception as e:
            return {"type": "tool_result", "tool_use_id": block.id, "content": f"{type(e).__name__}: {e}", "is_error": True}


def contract(call, problem):
    """The problem's answer contract: {form, not_enough}. `call(what, user)` is one tool-less call, its text."""
    got = parse(call("contract", CONTRACT.format(problem=problem))) or {}
    if not got.get("form"):
        raise RuntimeError("no answer contract")
    return got


def definite(call, problem, c, answer):
    """Whether `answer` could end a search for the problem's answer: {definite, reason, procedure}. Two questions, the
    second asked only of an answer that passes the first: whether it has the contract's form (DEFINITE), and whether it
    is the result itself and not a procedure for finding it (RESULT). `procedure`: the second turned it away; `reason`
    is then the second's."""
    d = parse(call("definite", DEFINITE.format(problem=problem, form=c["form"], not_enough=c.get("not_enough", ""),
                                               answer=answer))) or {}  # fmt: skip
    if d.get("definite") is not True:
        return {"definite": False, "reason": d.get("reason"), "procedure": False}
    r = parse(call("result", RESULT.format(problem=problem, answer=answer))) or {}
    if r.get("accepted") is True:
        return {"definite": True, "reason": d.get("reason"), "procedure": False}
    return {"definite": False, "reason": r.get("reason"), "procedure": r.get("accepted") is False}


def verify(llm, sandbox, record, folder, problem, form, answer, reason, halves=None, effort="high", emit=None, stop=None,
           told=True):  # a lone agent's record (record.solo) is told so: VERIFY_SOLO, VERIFY_UNTOLD_SOLO
    """The verifier on `record` (Record or stop_bench.Item), working in `folder` (its box and conversation.json kept
    there). `llm`: an OpenAILLM of the swarms' model (its system, tools and effort replaced). Returns {verdict,
    acknowledged, review, responses, runs, cost, stop}. `emit(text)`: a note per response, for a page. `stop`: an Event
    that ends the review early (no verdict, so no stop). `told` False: the team wasn't told `answer`, it ended with
    it (VERIFY_UNTOLD)."""
    from llm import cost, prompt_tokens, usage_dict

    folder = Path(folder)
    box = prepare_box(record, folder)
    tools = VerifyTools(record, box, sandbox)
    llm = replace(llm, system=VERIFY_SYSTEM, tools=VERIFY_TOOLS, max_tokens=64000, effort=effort)
    solo = getattr(record, "solo", False)
    task = {(True, False): VERIFY, (False, False): VERIFY_UNTOLD, (True, True): VERIFY_SOLO,
            (False, True): VERIFY_UNTOLD_SOLO}[bool(told), bool(solo)]  # fmt: skip
    messages = [{"role": "user", "content": task.format(
        problem=problem, form=form, n=len(record.agents()), answer=answer, reason=reason,
        halves=f" (told: {halves})" if halves else "", run_seconds=VERIFY_RUN_SECONDS,
        responses=VERIFY_RESPONSES)}]  # fmt: skip
    spent, verdict, nudged, responses = 0.0, None, 0, 0
    while verdict is None and responses < VERIFY_RESPONSES + 3 and not (stop and stop.is_set()):
        reply = llm.create(messages).message
        responses += 1
        u = usage_dict(reply.usage)
        spent += cost(llm.model, u)
        if reply.stop_reason == "refusal":
            messages.append({"role": "user", "content": "Please go on with the review."})
            continue
        messages.append({"role": "assistant", "content": [b.to_dict() for b in reply.content]})
        results = []
        for b in (b for b in reply.content if b.type == "tool_use"):
            if b.name == "give_verdict" and isinstance(b.input, dict) and b.input.get("verdict"):
                verdict = b.input
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": "Recorded.", "is_error": False})
            else:
                results.append(tools.handle(b))
        if emit:
            emit(f"verifier: response {responses}, " + (", ".join(b.name for b in reply.content if b.type == "tool_use")
                                                       or "no tool call") + f", ${spent:.2f}")  # fmt: skip
        late = responses >= VERIFY_RESPONSES or spent >= VERIFY_BUDGET or prompt_tokens(u) >= VERIFY_CONTEXT
        if results:
            messages.append({"role": "user", "content": results})
            if late and verdict is None:
                messages.append({"role": "system", "content": VERIFY_NUDGE})
                nudged += 1
        elif verdict is None:
            messages.append({"role": "user", "content": VERIFY_NUDGE})
            nudged += 1
        if nudged > 3:
            break
        (folder / "conversation.json").write_text(json.dumps({"messages": messages}))
    v = verdict or {}
    return {"verdict": v.get("verdict"), "acknowledged": v.get("team_acknowledged_gap"), "review": v,
            "responses": responses, "runs": tools.runs, "cost": spent,
            "stop": v.get("verdict") == "sound" and v.get("team_acknowledged_gap") is False}  # fmt: skip
