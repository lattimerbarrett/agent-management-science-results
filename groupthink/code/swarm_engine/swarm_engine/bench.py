"""How fast is a round of 50 agents on this machine? (Loads models; about five minutes, fifteen with --full.)

    swarm-bench                       # both models, written to results/<today>/
    swarm-bench --models 4B --full    # also one full-length round: 50 agents thinking up to 2,048 tokens each

Three rounds, each as the engine would really run it (thinking on, the thought closed at its budget, then a
short answer):

  first answers   every agent gets the same problem: one prompt, read once, 50 or 100 thoughts side by side
  shared context  every agent reads the problem and all 50 reports, then a few lines of its own: once with the
                  shared part read once, once with every agent reading it
  full round      (--full) 50 agents, a 2,048-token thinking budget and a 250-token answer
"""
import argparse
import json
import platform
import time
from importlib.metadata import version
from pathlib import Path

from .machine import budget_gb, under_lock

SYSTEM = ("You must output only valid JSON. No extra keys, no markdown, and no text outside the JSON object.\n"
          "You are one player on a team answering a problem.\nFollow the exact output schema given in the user message.")
SCHEMA = 'Output JSON exactly:\n{"answer":"<your answer>","reason":"<one sentence>"}'
PROBLEM = ("A drawer holds 7 red, 5 blue and 4 green socks. Socks are drawn one at a time without replacement "
           "until two of the same colour have been drawn in a row. Find the probability that this happens on "
           "exactly the fourth draw, as a fraction in lowest terms.")
REASON = ("Setting up the recurrence and counting the admissible configurations modulo the symmetry gives this "
          "value after subtracting the overcounted boundary cases.")


def first_answers(n: int) -> list[tuple[str, str]]:
    user = ("All players are working on the same problem.\nYou work on it alone; the other players see only what "
            f"you report.\n\nProblem:\n{PROBLEM}\n\n{SCHEMA}")
    return [(SYSTEM, user)] * n


def shared_context(n: int) -> list[tuple[str, str]]:
    reports = "\n".join(f'- Player {k + 1}: {{"answer":"{100 + 7 * k}/429","reason":"{REASON}"}}' for k in range(50))
    shared = (f"All players are working on the same problem.\n\nProblem:\n{PROBLEM}\n\n"
              f"Current reports from all players:\n{reports}\n\n")
    return [(SYSTEM, f"{shared}You are Player {k + 1}. Your previous answers (oldest -> newest): "
                     f'["{100 + 7 * k}/429"]\n\n{SCHEMA}') for k in range(n)]


def measure(engine, prompts, **settings) -> dict:
    import mlx.core as mx

    mx.clear_cache()
    mx.reset_peak_memory()
    before = (engine.new_tokens, engine.read_tokens, engine.spared_tokens)
    started = time.perf_counter()
    replies = engine.generate(prompts, **settings)
    seconds = time.perf_counter() - started
    written, read, spared = (now - then for now, then in zip((engine.new_tokens, engine.read_tokens, engine.spared_tokens), before))
    return {"calls": len(prompts), "side_by_side": engine.groups, "seconds": round(seconds, 1), "written": written,
            "sampled": sum(r.sampled_tokens for r in replies), "injected": sum(r.injected_tokens for r in replies),
            "read": read, "not_read_again": spared, "tokens_per_s": round(written / seconds),
            "thoughts_cut_off": sum(r.finished_thinking is False for r in replies),
            "answers_cut_off": sum(r.finish_reason in ("answer_limit", "total_limit") for r in replies),
            "run": engine.last_run,
            "prompt_tokens": len(engine.encode(prompts[0], thinking=True)),
            "peak_gb": round(mx.get_peak_memory() / 2**30, 1)}


def table(rows: list[dict]) -> str:
    lines = ["| model | round | agents | side by side | seconds | tokens written | tokens/s | peak memory |",
             "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        beside = " + ".join(str(g) for g in r["side_by_side"])
        lines.append(f"| {r['model']} | {r['round']} | {r['calls']} | {beside} | {r['seconds']} | {r['written']:,} | "
                     f"{r['tokens_per_s']} | {r['peak_gb']} GB |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--models", nargs="+", default=["4B", "9B"])
    parser.add_argument("--full", action="store_true", help="also one full-length round (2,048-token thoughts)")
    parser.add_argument("--name", default=time.strftime("%Y-%m-%d"), help="folder under --out for the results")
    parser.add_argument("--out", default="results")
    parser.add_argument("--mem-gb", type=float, default=20, help="memory budget for the job, of this laptop's 48 GB")
    args = parser.parse_args()
    under_lock(mem_gb=args.mem_gb)
    import mlx.core as mx

    from .engine import Engine

    folder = Path(args.out) / args.name
    folder.mkdir(parents=True, exist_ok=True)
    if any((folder / name).exists() for name in ("bench.json", "bench.md", "bench.jsonl")):
        parser.error("benchmark files already exist; choose a new --name")
    rows: list[dict] = []
    for model in args.models:
        engine = Engine(model)
        print(f"{engine.name}: {engine.describe()}", flush=True)
        engine.generate(first_answers(2), thinking=8, max_tokens=4)                      # warm up
        rounds = [("first answers", first_answers(50), {"thinking": 384, "max_tokens": 32}),
                  ("first answers", first_answers(100), {"thinking": 384, "max_tokens": 32}),
                  ("shared context, read once", shared_context(50), {"thinking": 64, "max_tokens": 32}),
                  ("shared context, each agent reads it", shared_context(50), {"thinking": 64, "max_tokens": 32, "share": False})]
        if args.full:
            rounds.append(("full round (2,048-token thoughts)", first_answers(50), {"thinking": 2048, "max_tokens": 250}))
        for name, prompts, settings in rounds:
            row = {"model": model, "round": name,
                   **measure(engine, prompts, seeds=list(range(len(prompts))), **settings), "settings": settings}
            rows.append(row)
            with (folder / "bench.jsonl").open("a") as f:
                f.write(json.dumps(row) + "\n")
            print(json.dumps(row), flush=True)
        del engine
        mx.clear_cache()
    about = {"when": time.strftime("%Y-%m-%d %H:%M"), "machine": mx.device_info().get("device_name"),
             "macos": platform.mac_ver()[0], "mlx": version("mlx"), "mlx_lm": version("mlx-lm"),
             "budget_gb": budget_gb(), "full": args.full}
    (folder / "bench.json").write_text(json.dumps({"about": about, "rows": rows}, indent=2) + "\n")
    (folder / "bench.md").write_text(table(rows) + "\n")
    print("\n" + table(rows) + f"\n\nwritten to {folder}/", flush=True)


if __name__ == "__main__":
    main()
