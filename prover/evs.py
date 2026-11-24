"""Counterfactual verbalized sampling (CFVS; "EVS" in this code, for its earlier name, epistemic verbalized sampling):
the question that gives an explorer its options, and how its reply is read.

evs.md asks an agent for n counterfactuals (statements that run against what it now believes), each with a
probability, and under each one k approaches it could take next if the counterfactual were true, each with a
probability. `counterfactuals` reads the reply and `flatten` lists every approach with its counterfactual: an
explorer's options (prover_archive.Archive.options). A rollout is told its option's counterfactual as a verified
result and its approach (VERIFIED); once it is a parent, that message becomes RELABEL.
"""

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = (ROOT / "evs.md").read_text()
MAX_TOKENS = 24000  # per reply, thinking included
# What a rollout is told before its step: its option's counterfactual as a verified result, then the approach.
# {no_answer} is NO_ANSWER_STEP.
VERIFIED = ("The following has been established; it is a verified result, not a guess, and your work must be consistent "
            "with it: {counterfactual}\n"
            "Anything you concluded earlier that contradicts it is wrong. Take this approach: {approach}{no_answer}")
NO_ANSWER_STEP = "\nDo not give a final answer until you have seen what it gives."
# What that message becomes before the next step, once the agent is a parent: a counterfactual given as a verified
# result stayed in the context of every later step, and the agent, asked for statements that run against what it
# believes, stopped questioning it.
RELABEL = "In your last step you worked under this assumption: {counterfactual}\nYou took this approach: {approach}"


def weight(raw, percent=False):
    """A verbalized probability as a number in [0, 1], or None if it isn't one: "25%" (and, with `percent`, 25) is
    0.25, and values outside [0, 1] are clipped."""
    if isinstance(raw, str):
        text = raw.strip()
        percent = percent or text.endswith("%")
        try:
            raw = float(text.removesuffix("%"))
        except ValueError:
            return None
    if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not math.isfinite(raw):
        return None
    return min(max(raw / 100 if percent else raw, 0.0), 1.0)


def approaches(reply, percent=False):
    """The approaches of one parsed reply ({"responses": [{"text", "probability" or "confidence"}]}), each as {"text",
    "p_raw", "w"}, w its weight (`weight`, None without one); None if the reply has no list of them."""
    items = reply.get("responses") if isinstance(reply, dict) else None
    if not isinstance(items, list):
        return None
    out = []
    for it in items:
        it = {"text": it} if isinstance(it, str) else it
        if not isinstance(it, dict):
            continue
        text = next((it[k] for k in ("text", "response", "approach") if isinstance(it.get(k), str)), "").strip()
        if text:
            raw = next((it[k] for k in ("probability", "confidence") if k in it), None)
            out.append({"text": text, "p_raw": raw, "w": weight(raw, percent)})
    return out


def normalize(found):
    """`found` (approaches) with `p`, each one's weight over their sum; uniform when any weight is missing or they sum
    to 0 (Sequence)."""
    weights = [a["w"] for a in found]
    total = 0.0 if None in weights else sum(weights)
    return [{**a, "p": a["w"] / total if total else 1 / len(found)} for a in found]


def counterfactuals(reply):
    """The counterfactuals of one parsed reply ({"counterfactuals": [{"text", "probability", "responses"}]}), each as
    {"text", "p_raw", "w", "p", "responses"}: w its weight (`weight`), p normalized over them (`normalize`), and its
    approaches (`approaches`, normalized over them); one without approaches is left out. None if the reply has no list
    of them."""
    items = reply.get("counterfactuals") if isinstance(reply, dict) else None
    if not isinstance(items, list):
        return None
    out = []
    for it in items:
        if not isinstance(it, dict):
            continue
        text = next((it[k] for k in ("text", "counterfactual") if isinstance(it.get(k), str)), "").strip()
        if text and (found := approaches(it)):
            raw = next((it[k] for k in ("probability", "confidence") if k in it), None)
            out.append({"text": text, "p_raw": raw, "w": weight(raw), "responses": normalize(found)})
    return normalize(out)


def flatten(cfs):
    """Every counterfactual's approaches in one list, each with its branch (c<i>b<j>: approach j of counterfactual i),
    its counterfactual's text and p (cf_p), p_given (its p among its counterfactual's) and p, cf_p times p_given."""
    return [{**a, "branch": f"c{i}b{j}", "counterfactual": c["text"], "cf_p": c["p"], "p_given": a["p"],
             "p": c["p"] * a["p"]} for i, c in enumerate(cfs) for j, a in enumerate(c["responses"])]  # fmt: skip
