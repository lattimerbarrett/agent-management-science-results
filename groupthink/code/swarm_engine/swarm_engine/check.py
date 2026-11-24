"""Check mechanics and report numerical sensitivity; this is not a proof-quality benchmark.

    swarm-check --model 4B --out results/<new-run>/check-4B.json

Greedy trajectories are compared with an independent, unbatched generate_step
reference. Divergent paths are teacher-forced through the reference at EVERY
sampled token, so an early near-tie cannot hide a later large discrepancy.
Differences within --max-greedy-gap are reported as numerical deviations, never
as equality. --strict requires exact trajectories, including the mixed-row probe.
"""
import argparse
from concurrent.futures import Future
import json
import math
from pathlib import Path
import sys
import threading
import time

from .machine import under_lock

QUESTIONS = [
    "What is 17 + 26? Reply with the number only.",
    "Is 91 a prime number? Reply yes or no.",
    "A train leaves at 9:40 and arrives at 11:05. How many minutes is the trip? Reply with the number only.",
    "Which is larger, 3/7 or 5/12? Reply with the fraction only.",
    "How many letters are in the word 'consensus'? Reply with the number only.",
    "If all bloops are razzies and all razzies are lazzies, are all bloops lazzies? Reply yes or no.",
    "What is the next number: 2, 6, 12, 20, 30, ? Reply with the number only.",
    "A rectangle is 6 by 9. What is its area? Reply with the number only.",
]
SYSTEM = "You are one player on a team answering a problem. Reply briefly."
REASON = "Counting the admissible cases after removing the overcounted ones gives this value."


def shared_round(n: int) -> list[tuple[str, str]]:
    """What a broadcast round looks like: everyone's reports first, then the few lines that are one player's own."""
    reports = "\n".join(f'- Player {k + 1}: {{"answer":"{40 + k}","reason":"{REASON}"}}' for k in range(24))
    block = f"Problem:\n{QUESTIONS[0]}\n\nCurrent reports from all players:\n{reports}\n\n"
    return [(SYSTEM, f"{block}You are Player {k + 1}. Reply with your answer as a number only.") for k in range(n)]


MAX_GREEDY_GAP = 0.25   # explicit diagnostic tolerance, NOT an exact tie or an accuracy guarantee


def plain(engine, context: list[int], thinking: int, max_tokens: int) -> tuple[list[int], list[int], list, list]:
    """One call the plain way, always taking the likeliest token: (thought tokens, answer tokens), and for each
    of the two a trace of its three likeliest tokens and their log-probabilities at every step."""
    import mlx.core as mx
    from mlx_lm.generate import generate_step

    def run(tokens: list[int], limit: int, stops: list[int]) -> tuple[list[int], list[dict[int, float]], bool]:
        out, trace, stopped = [], [], False
        generator = generate_step(mx.array(tokens), engine.model, max_tokens=limit,
            sampler=lambda logprobs: mx.argmax(logprobs, axis=-1),
            logits_processors=[lambda _tokens, logits: logits.astype(mx.float32)])
        try:
            for token, logprobs in generator:
                likeliest = mx.argsort(logprobs)[-3:].tolist() + [token]
                trace.append({t: float(logprobs[t]) for t in likeliest})
                out.append(token)
                if token in stops:
                    stopped = True
                    break
        finally:
            generator.close()
        return out, trace, stopped

    thought, thought_trace = [], []
    if thinking > 0:
        tokens, thought_trace, stopped = run(context, thinking, [engine.end_of_turn, engine.close])
        if stopped and tokens[-1] == engine.close:
            thought = tokens
        elif stopped:
            return tokens, [], thought_trace, []
        else:
            thought = tokens + engine._out_of_time
    answer, answer_trace, _ = run(context + thought, max_tokens, [engine.end_of_turn])
    return thought, answer, thought_trace, answer_trace


def greedy_path_gap(engine, context, reply) -> float:
    """Audit all sampled tokens on the engine's actual path, including after divergence."""
    import mlx.core as mx
    from mlx_lm.models.cache import make_prompt_cache
    cache = make_prompt_cache(engine.model)
    for at in range(0, len(context), 512):
        logits = engine.model(mx.array(context[at:at + 512])[None], cache=cache)[:, -1, :].astype(mx.float32)
        mx.eval(logits, [c.state for c in cache])
    gaps = []
    injected = set(reply.injected_positions)
    for i, token in enumerate(reply.output_tokens):
        if i not in injected:
            gaps.append(float(mx.max(logits) - logits[0, token]))
        if i + 1 < len(reply.output_tokens):
            logits = engine.model(mx.array([[token]]), cache=cache)[:, -1, :].astype(mx.float32)
            mx.eval(logits)
    return max(gaps, default=0.0)


def against_plain(engine, ask, reply, thinking: int, max_tokens: int, tolerance=MAX_GREEDY_GAP) -> tuple[str, float]:
    context = engine.encode(ask, thinking=thinking > 0)
    thought, answer, _, _ = plain(engine, context, thinking, max_tokens)
    if (reply.thought_tokens or []) == thought and reply.tokens == answer:
        return "same", 0.0
    gap = greedy_path_gap(engine, context, reply)
    return ("numerical_deviation" if gap <= tolerance else "differs"), gap


def same(a, b) -> bool:
    return (a.thought_tokens or []) == (b.thought_tokens or []) and a.tokens == b.tokens


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", default="4B")
    parser.add_argument("--out", type=Path, help="write machine-readable results (must not already exist)")
    parser.add_argument("--strict", action="store_true", help="fail on any token trajectory difference")
    parser.add_argument("--max-greedy-gap", type=float, default=MAX_GREEDY_GAP,
                        help="maximum teacher-forced logit gap, in nats, for a numerical deviation")
    args = parser.parse_args()
    if args.max_greedy_gap < 0 or not math.isfinite(args.max_greedy_gap):
        parser.error("--max-greedy-gap must be finite and nonnegative")
    if args.out and args.out.exists():
        parser.error("--out already exists; choose a new result path")
    under_lock()
    from .engine import Engine
    from .settings import Sampling

    engine = Engine(args.model)
    print(f"{engine.name}: {engine.describe()}", flush=True)
    failures = 0
    records = []

    def report(name: str, good: int, total: int, detail: str = ""):
        nonlocal failures
        failures += good != total
        records.append({"check": name, "passed": good, "total": total, "detail": detail})
        print(f"{'ok  ' if good == total else 'FAIL'} {name}: {good}/{total}{' ' + detail if detail else ''}", flush=True)

    def report_against_plain(name: str, asks, replies, thinking: int, max_tokens: int, detail: str = ""):
        verdicts = [against_plain(engine, a, r, thinking, max_tokens, args.max_greedy_gap) for a, r in zip(asks, replies)]
        exact = sum(v == "same" for v, _ in verdicts)
        deviations = sum(v == "numerical_deviation" for v, _ in verdicts)
        good = exact if args.strict else exact + deviations
        report(name, good, len(verdicts),
               f"{exact} exact, {deviations} numerical deviations; full-path max gap={max(g for _, g in verdicts):.4f} nats; {detail}")

    greedy = {"sampling": Sampling(temperature=0, top_k=0, top_p=1, presence_penalty=0)}

    asks = [(SYSTEM, q) for q in QUESTIONS]

    # 1. Thought into answer in one pass, one call at a time (so nothing but the one pass differs from plain),
    #    then side by side. Short budgets cut thoughts off; the long one lets an easy question's thought close
    #    by itself, so both ways of ending a thought are covered.
    for budget, limit in ((48, 24), (900, 24)):
        subset = asks if budget < 100 else asks[:4]
        alone = [engine.generate([a], thinking=budget, max_tokens=limit, share=False, **greedy)[0] for a in subset]
        closed = sum(bool(r.finished_thinking) for r in alone)
        report_against_plain(f"thought into answer in one pass (budget {budget})", subset, alone, budget, limit,
                             f"{closed} thoughts closed by themselves, {len(subset) - closed} cut off")
        started = time.perf_counter()
        together = engine.generate(subset, thinking=budget, max_tokens=limit, share=False, **greedy)
        report_against_plain(f"the same calls side by side (budget {budget})", subset, together, budget, limit,
                             f"{time.perf_counter() - started:.1f}s")

    # 2. Answering directly (no thinking), side by side.
    report_against_plain("side by side, answering directly", asks, engine.generate(asks, thinking=0, max_tokens=24, share=False, **greedy), 0, 24)

    # 3. A shared start read once.
    round_ = shared_round(8)
    before = engine.spared_tokens
    together = engine.generate(round_, thinking=40, max_tokens=16, **greedy)
    report_against_plain("shared start read once", round_, together, 40, 16,
                         f"{engine.spared_tokens - before} tokens not read again")

    # 4. Identical prompts (every player's first answer): read once, and still one independent draw per seed.
    first = engine.generate([asks[2]] * 8, seeds=list(range(8)), thinking=40, max_tokens=16)
    again = engine.generate([asks[2]] * 8, seeds=list(range(8)), thinking=40, max_tokens=16)
    report("the same seeds repeat themselves", sum(same(a, b) for a, b in zip(first, again)), 8)
    distinct = len({tuple(r.thought_tokens) for r in first})
    report("different seeds think differently", min(distinct, 2), 2, f"({distinct} distinct thoughts of 8)")

    # 5. A sampled call says the same thing alone as in a crowd.
    crowd = engine.generate(asks, seeds=[100 + k for k in range(len(asks))], thinking=40, max_tokens=16)
    alone = [engine.generate([a], seeds=[100 + k], thinking=40, max_tokens=16)[0] for k, a in enumerate(asks)]
    exact = sum(same(a, b) for a, b in zip(crowd, alone))
    if args.strict:
        report("sampled alone vs batch", exact, len(asks))
    else:
        records.append({"check": "sampled alone vs batch", "exact": exact, "total": len(asks), "diagnostic_only": True})
        print(f"info sampled alone vs batch: {exact}/{len(asks)} exact (diagnostic, not equality guarantee)", flush=True)

    # Conversations carried on, each at its own pace: every call has to be the call `generate` would make of the
    # same prompt, whether it went on from what was kept or was read again. A tool's word follows each reply, so
    # that the chat template keeps the thought and the next prompt begins with what the model read and wrote.
    for budget in (900, 48):                             # thoughts that close themselves, and thoughts that are cut
        talks = [[{"role": "system", "content": SYSTEM}, {"role": "user", "content": q}] for q in QUESTIONS[:4]]
        asked, heard = [], []

        def respond(i, reply):
            asked.append(list(talks[i]))
            heard.append(reply)
            if len([m for m in talks[i] if m["role"] == "assistant"]) == 2:
                return None
            talks[i] += [{"role": "assistant", "content": reply.text, "reasoning_content": reply.reasoning},
                         {"role": "tool", "content": "Noted. Now check it once more and reply with your final answer only."}]
            return list(talks[i]), 300 + i
        before = engine.spared_tokens
        engine.converse([list(talk) for talk in talks], [300 + i for i in range(4)], respond, thinking=budget, max_tokens=24, **greedy)
        run = engine.last_run
        report_against_plain(f"conversations carried on (budget {budget})", asked, heard, budget, 24,
                             f"{len(heard)} calls, {engine.spared_tokens - before} tokens not read again, "
                             f"{run['read_again']} prompts read again, {run['widest']} side by side")
        records[-1]["carried"] = [call["carried_tokens"] for call in run["calls"]]

    # A conversation that waits for another, and one whose first reply the caller already has: what is written
    # is still what `generate` would make of the same prompts, and nothing is written for the reply that is known.
    talks = [[{"role": "system", "content": SYSTEM}, {"role": "user", "content": q}] for q in QUESTIONS[:3]]
    had = engine.generate([list(talks[2])], seeds=[302], thinking=900, max_tokens=24, **greedy)[0]
    asked, heard, order, gate, later, state = [], [], [], threading.Lock(), Future(), {"ended": False, "next": None}

    def respond(i, reply):
        with gate:
            order.append(i)
            if reply is not had:
                asked.append(list(talks[i]))
                heard.append(reply)
            if len([m for m in talks[i] if m["role"] == "assistant"]) == 1:      # that was its second reply
                if i == 0:
                    state["ended"] = True
                    if state["next"] is not None:
                        later.set_result(state["next"])              # conversation 1 may go on now
                return None
            talks[i] += [{"role": "assistant", "content": reply.text, "reasoning_content": reply.reasoning},
                         {"role": "tool", "content": "Noted. Now check it once more and reply with your final answer only."}]
            if i == 1 and not state["ended"]:
                state["next"] = (list(talks[1]), 301)
                return later                                         # it waits until conversation 0 has ended
            return list(talks[i]), 300 + i
    engine.converse([list(talk) for talk in talks], [300, 301, 302], respond, thinking=900, max_tokens=24,
                    known=lambda i: had if i == 2 and len(talks[2]) == 2 else None, **greedy)
    run = engine.last_run
    waited = state["next"] is not None
    report_against_plain("a conversation that waits for another, and a reply that was known", asked, heard, 900, 24,
                         f"{len(heard)} calls written, {run['known']} known; conversation 1 "
                         f"{'waited for conversation 0 to end' if waited else 'did not have to wait'}")
    report("a known reply is not written again, and a wait ends when it should",
           int(run["known"] == 1 and len(run["calls"]) == 5 and order.count(1) == 2 and
               (not waited or order.index(1, order.index(1) + 1) > max(k for k, i in enumerate(order) if i == 0))), 1)

    # Natural mode must neither inject a bridge nor manufacture an answer at its cap.
    capped = engine.generate([asks[0]], seeds=[5], max_total_tokens=1)[0]
    report("natural cap preserves unfinished thought", int(capped.finish_reason == "total_limit" and
        capped.injected_tokens == 0 and len(capped.output_tokens) == 1 and not capped.text), 1)

    # More requests than the prefill batch, multiple shared prefixes, unequal histories.
    mixed = [("Group " + str(i // 15) + ". " + "Background: triangles have three sides. " * (8 + i // 15),
              f"Agent {i}. " + "Ignore this filler. " * (i % 7) + QUESTIONS[0]) for i in range(50)]
    seeds = list(range(500, 550))
    options = dict(thinking=32, max_tokens=16, seeds=seeds)
    shared = engine.generate(mixed, **options)
    run_metadata = engine.last_run
    unshared = engine.generate(mixed, share=False, **options)
    engine.width = 7
    narrow = engine.generate(mixed, **options)
    engine.width = 100
    for label, replies in (("sharing", unshared), ("width", narrow)):
        exact = sum(same(a, b) for a, b in zip(shared, replies))
        accuracy = sum(r.text.strip() == "43" for r in replies)
        records.append({"check": "mixed rows " + label, "exact": exact, "total": 50,
                        "correct_arithmetic_answers": accuracy, "diagnostic_only": not args.strict})
        print(f"info mixed rows {label}: {exact}/50 exact; {accuracy}/50 correct arithmetic answers", flush=True)
        if args.strict:
            failures += exact != 50
    report("emitted token accounting", sum(len(r.output_tokens) == r.sampled_tokens + r.injected_tokens
        and len(r.injected_positions) == r.injected_tokens for r in shared + unshared + narrow), 150)
    fresh = engine.generate([asks[0]], thinking=0, max_tokens=8)[0]
    replay = engine.generate([asks[0]], seeds=[fresh.seed], thinking=0, max_tokens=8)[0]
    report("fresh seed can be replayed", int(same(fresh, replay)), 1)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("x") as f:
            json.dump({"engine": engine.describe(), "strict": args.strict,
                       "max_greedy_gap": args.max_greedy_gap, "failures": failures,
                       "checks": records, "mixed_run": run_metadata}, f, indent=2)
            f.write("\n")

    print(f"{engine.calls} calls, {engine.new_tokens} tokens written, {engine.read_tokens} read, "
          f"{engine.spared_tokens} not read again", flush=True)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
