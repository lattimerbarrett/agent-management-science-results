"""Hold the vLLM engine against a live server, and time it: `swarm-vllm check` (on a machine with a GPU).

    swarm-vllm check --model 9B-bf16 --out results/<day>-<gpu>/check-9B-bf16.json

tests/test_vllm.py holds vllm.py against a stand-in that does what vLLM's source says it does. This asks the real
thing, and fails if it answers otherwise:

    the tokenizer     the server cuts text into the tokens this engine's tokenizer does
    a thought         closes by itself on an easy question, and is closed by the engine at its budget on a hard one,
                      with an answer after it either way
    a tool call       comes back as the model's own text, as the caller parses it
    the same call     with the same seed is the same reply; with another seed it is another
    a conversation    is taken up from what the server kept of it: of the later prompts of a conversation that goes
                      on as agents' do (the reply, then what a tool said), the server held more than half when
                      they arrived. Its prompts are thousands of tokens long, since a server may keep what it has
                      read only in large blocks, and each call is counted by what its first request found.

and reports, without failing on them: whether a call comes out the same alone and among other calls (a seed fixes
the draws, not the numbers they are drawn from), how much the answer's request of a call had to read again of
what the thought's request had just read and written, and how many tokens a second the server writes with 8, 32
and 128 calls in flight, for single calls and for conversations of four calls that grow.

It is the first thing to run on a new kind of GPU, after a change to vllm.py, and after a new vLLM.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

from .settings import Sampling, trial_seed

EASY = ["What is 17 + 26? Reply with the number only.", "Is 91 a prime number? Reply yes or no.",
        "A rectangle is 6 by 9. What is its area? Reply with the number only.",
        "How many letters are in the word 'consensus'? Reply with the number only."]
EASY_ANSWERS = ["43", "no", "54", "9"]
HARD = ("A drawer holds 7 red, 5 blue and 4 green socks. Socks are drawn one at a time without replacement until two of "
        "the same colour have been drawn in a row. Find the probability that this happens on exactly the fourth draw, as a "
        "fraction in lowest terms.")
SYSTEM = "You are one player on a team answering a problem. Reply briefly."
TOOL = {"type": "function", "function": {"name": "write_file", "description": "Create work.py, or replace the whole of it.",
        "parameters": {"type": "object", "properties": {"content": {"type": "string", "description": "The whole file."}},
                       "required": ["content"]}}}
GREEDY = Sampling(temperature=0, top_k=0, top_p=1, presence_penalty=0)
TABLE = "\n".join(f"{n} squared is {n * n} and {n} cubed is {n ** 3}." for n in range(1, 161))      # some 3,000 tokens
PRINTED = "It ran with no errors. It printed:\n" + "\n".join(f"case {n}: {n * n}" for n in range(60))       # some 500


def long(player: int) -> str:
    """A prompt of a few thousand tokens that is one player's alone from near its start."""
    return f"Player {player + 1}. {HARD}\n\nA table that is of no use for it:\n{TABLE}"


def went_on(history: dict, i: int, opening: str, reply, calls: int, said: str, seed: int):
    """How a conversation of the check goes on, as an agent's at a desk does: the reply as the model wrote it, its
    thought with it, then what a tool said. Returns the next call, or None after `calls` of them."""
    history.setdefault(i, [{"role": "system", "content": SYSTEM}, {"role": "user", "content": opening}])
    history[i] += [{"role": "assistant", "content": reply.text, "reasoning_content": reply.reasoning}, {"role": "tool", "content": said}]
    return (history[i], trial_seed(seed, i, len(history[i]))) if len(history[i]) < 2 + 2 * calls else None      # an opening of two, two a call


def used_gb() -> float | None:
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"], capture_output=True,
                             text=True, timeout=20).stdout.split()
        return round(int(out[0]) / 1024, 1)
    except (OSError, subprocess.SubprocessError, ValueError, IndexError):
        return None


def main(args) -> int:
    import httpx

    from . import backend
    from .common import OUT_OF_TIME
    from .vllm_server import VERSION

    def say(line: str):
        print(f"[swarm-vllm check] {line}", file=sys.stderr, flush=True)

    engine = backend(args.model, say=say)
    found: dict = {"model": args.model, "engine": engine.describe(), "checks": {}, "notes": {}, "timing": []}
    failed: list[str] = []

    def check(name: str, held: bool, **what):
        found["checks"][name] = {"held": bool(held), **what}
        say(f"{'ok  ' if held else 'FAIL'}  {name}" + (f": {json.dumps(what)[:300]}" if what and not held else ""))
        if not held:
            failed.append(name)

    try:
        found["notes"]["vllm"] = engine.vllm_version
        check("the server is the pinned vLLM", (engine.vllm_version or "").split("+")[0] == VERSION, has=engine.vllm_version, pinned=VERSION)

        # ---- the tokenizer
        texts = [engine.tokenizer.apply_chat_template([{"role": "system", "content": SYSTEM}, {"role": "user", "content": HARD}],
                                                      add_generation_prompt=True, enable_thinking=True, tokenize=False, tools=[TOOL]),
                 "x**2 + y**2 == z**2\n\n    return [i for i in range(10)]  # naïve café √2 ≈ 1.41421356… 数学",
                 "<tool_call>\n<function=write_file>\n<parameter=content>\nprint('ANSWER:', 42)\n</parameter>\n</function>\n</tool_call>"]
        same = []
        for text in texts:
            cut = httpx.post(f"{engine.url}/tokenize", json={"model": engine.served, "prompt": text, "add_special_tokens": False}, timeout=60.0)
            same.append(cut.status_code == 200 and cut.json().get("tokens") == engine.encode_text(text))
        check("the server cuts text into the tokens this engine does", all(same), same=same)

        # ---- a thought, closed by itself and at its budget
        easy = engine.generate([(SYSTEM, q) for q in EASY], [trial_seed(1, k) for k in range(len(EASY))], thinking=None,
                               max_tokens=64, max_total_tokens=4096, sampling=GREEDY)
        right = [answer in reply.text.lower() for reply, answer in zip(easy, EASY_ANSWERS)]
        check("an easy question is thought through, the thought closed by the model, and answered",
              all(r.finish_reason == "stop" and r.finished_thinking for r in easy) and sum(right) >= 3,
              finish=[r.finish_reason for r in easy], closed=[r.finished_thinking for r in easy], texts=[r.text[:60] for r in easy])
        (cut,) = engine.generate([(SYSTEM, HARD)], [trial_seed(2, 0)], thinking=48, max_tokens=64, sampling=GREEDY)
        words = len(engine._out_of_time)                          # an answer that runs into its limit gets one end of turn more
        check("a thought still open at its budget is closed with the engine's words, and answered",
              cut.finished_thinking is False and cut.reasoning.endswith(OUT_OF_TIME.split("</think>")[0])
              and len(cut.thought_tokens or ()) == 48 + words and cut.injected_tokens == words + (cut.finish_reason == "answer_limit")
              and bool(cut.text) and cut.finish_reason in ("stop", "answer_limit"),
              finish=cut.finish_reason, thought_tokens=len(cut.thought_tokens or ()), injected=cut.injected_tokens, text=cut.text[:80])
        (direct,) = engine.generate([(SYSTEM, EASY[0])], [trial_seed(2, 1)], thinking=0, max_tokens=32, sampling=GREEDY)
        check("with thinking off the answer comes at once", direct.thought_tokens is None and "43" in direct.text and direct.finish_reason == "stop",
              text=direct.text[:60])

        # ---- a tool call
        (called,) = engine.generate([("You write Python files. Reply with one call to write_file.", "Write a file that prints 6 * 7.")],
                                    [trial_seed(3, 0)], thinking=256, max_tokens=256, sampling=Sampling.coding(), tools=[TOOL])
        check("a tool call comes back as the model's own text", "<function=write_file>" in called.text and "<parameter=content>" in called.text,
              text=called.text[:200])

        # ---- the same call
        ask, policy = [(SYSTEM, HARD)], dict(thinking=96, max_tokens=96, sampling=Sampling.coding(), thought_sampling=Sampling())
        (one,), (again,), (other,) = (engine.generate(ask, [seed], **policy) for seed in (7, 7, 8))
        check("the same seed and the same call are the same reply", one.output_tokens == again.output_tokens)
        check("another seed is another reply", one.output_tokens != other.output_tokens)
        crowd = engine.generate(ask + [(SYSTEM, q) for q in EASY * 4], [7] + [trial_seed(4, k) for k in range(16)], **policy)
        found["notes"]["a call comes out the same alone and among 16 others"] = crowd[0].output_tokens == one.output_tokens
        say(f"note  a call among 16 others is {'the same' if crowd[0].output_tokens == one.output_tokens else 'NOT the same'} reply as alone "
            "(a seed fixes the draws, not the numbers: arms are paired through the cache)")

        # ---- a conversation that carries on
        history: dict[int, list] = {}
        engine.converse([(SYSTEM, long(i)) for i in range(2)], [trial_seed(5, 0), trial_seed(5, 1)],
                        lambda i, reply: went_on(history, i, long(i), reply, 3, PRINTED, 5), thinking=128, max_tokens=128,
                        sampling=Sampling.coding(), thought_sampling=Sampling(), tools=[TOOL])
        calls, seen = engine.last_run["calls"], set()
        later = [c for c in calls if c["conversation"] in seen or seen.add(c["conversation"])]      # all but each one's first
        share = sum(c["carried_tokens"] for c in later) / max(sum(c["prompt_tokens"] for c in later), 1)
        check("a conversation is taken up from what the server kept of it", len(calls) == 6 and len(later) == 4 and share > 0.5,
              calls=[[c["conversation"], c["prompt_tokens"], c["carried_tokens"]] for c in calls], share_not_read_again=round(share, 2))
        found["notes"]["of a conversation's later prompts, the share the server did not read again"] = round(share, 2)
        again = engine.last_run["usage"]["answer_read_tokens"] / max(len(calls), 1)
        found["notes"]["tokens a call's answer request read again, of what its thought request had read and written"] = round(again)
        say(f"note  the answer's request of a call read {again:.0f} tokens again (its thought was at most 128, its prompt thousands)")

        # ---- timing
        for width in args.widths:
            engine.width = width
            started = time.perf_counter()
            replies = engine.generate([(SYSTEM, f"{HARD} (Player {k + 1})") for k in range(width)], [trial_seed(6, k) for k in range(width)],
                                      thinking=256, max_tokens=256, sampling=Sampling.coding(), thought_sampling=Sampling())
            seconds = time.perf_counter() - started
            written = sum(len(r.output_tokens) for r in replies)
            row = {"round": "single calls", "in_flight": width, "calls": width, "seconds": round(seconds, 1), "written": written,
                   "tokens_per_s": round(written / seconds), "gpu_used_gb": used_gb()}
            found["timing"].append(row)
            say(f"time  {row}")
            talks: dict[int, list] = {}
            started = time.perf_counter()
            engine.converse([(SYSTEM, f"Player {k + 1}. {HARD}") for k in range(width)], [trial_seed(7, k) for k in range(width)],
                            lambda i, reply: went_on(talks, i, f"Player {i + 1}. {HARD}", reply, 4, PRINTED, 7),
                            thinking=256, max_tokens=256, sampling=Sampling.coding(), thought_sampling=Sampling(), workers=8, tools=[TOOL])
            seconds, usage = time.perf_counter() - started, engine.last_run["usage"]
            written = usage["output_tokens"]
            row = {"round": "conversations of four calls", "in_flight": width, "calls": len(engine.last_run["calls"]),
                   "seconds": round(seconds, 1), "written": written, "tokens_per_s": round(written / seconds), "read": usage["read_tokens"],
                   "not_read_again": usage["spared_tokens"], "read_again_for_answers": usage["answer_read_tokens"], "gpu_used_gb": used_gb()}
            found["timing"].append(row)
            say(f"time  {row}")
    finally:
        engine.close_server()
    found["failed"] = failed
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(found, indent=2) + "\n")
        say(f"wrote {args.out}")
    say("every check held" if not failed else f"{len(failed)} checks failed: {'; '.join(failed)}")
    return 1 if failed else 0
