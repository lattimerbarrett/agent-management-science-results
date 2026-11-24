"""The models this was measured on, by the names an experiment gives them, and what runs each.

    "4B", "9B"              Qwen3.5 at 4 bits (mlx-community's conversion), on this Mac through MLX: engine.py
    "4B-bf16", "9B-bf16"    Qwen3.5 as Qwen released it, in bfloat16, on a GPU through vLLM: vllm.py

The two families are different builds of the same model, and an experiment should treat them as two models: a
number made with one is not held against a number made with the other. They do share their chat template and
their tokenizer (results/2026-10-11-gpu/tokenizer_parity.txt: 4,498 texts of a real run and 800 chat prompts cut
into the same tokens by both), so the same messages are the same prompt on either.

Every name is pinned to a commit of its Hugging Face repository. Nothing here imports a model library.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Model:
    repo: str                 # its Hugging Face repository
    revision: str             # the commit it is pinned to
    backend: str              # "mlx" or "vllm"
    weights_gb: float = 0.0   # for vLLM: what its weights take of a GPU's memory, in GiB (the MLX engine reads this
                              # off the loaded model instead)
    dtype: str = ""           # for vLLM: the precision it is served in


# The weight files of the two bf16 repositories are 17.98 and 8.68 GiB (the Hugging Face API, 2026-10-11). Served
# for text alone, the vision tower (0.9 and 0.7 GB) and the head for speculative decoding (0.5 and 0.2 GB) are
# not loaded: those four sizes are summed from the files' headers and have not been checked on a GPU.
KNOWN = {
    "4B": Model("mlx-community/Qwen3.5-4B-4bit", "0e7ffd5c629ef7719d4cbc04069232580bfa9d9c", "mlx"),
    "9B": Model("mlx-community/Qwen3.5-9B-4bit", "8b2b98c00a6b4d291155e4890773ca8f769aee53", "mlx"),
    "4B-bf16": Model("Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a", "vllm", 7.8, "bfloat16"),
    "9B-bf16": Model("Qwen/Qwen3.5-9B", "c202236235762e1c871ad0ccb60c8ee5ba337b9a", "vllm", 16.7, "bfloat16"),
}

# As engine.py has them, for the MLX names (held equal by a test), and the same for every name.
MODELS = {name: model.repo for name, model in KNOWN.items()}
REVISIONS = {name: model.revision for name, model in KNOWN.items()}


def backend_of(model: str) -> str:
    """Which backend runs a model: "mlx" or "vllm". A name this file knows says so itself. Any other name (a
    folder, another Hugging Face repository) goes to SWARM_BACKEND if that is set, and otherwise to the backend
    this kind of machine has: MLX on a Mac, vLLM anywhere else."""
    if model in KNOWN:
        return KNOWN[model].backend
    chosen = os.environ.get("SWARM_BACKEND", "").strip().lower()
    if chosen:
        if chosen not in ("mlx", "vllm"):
            raise ValueError(f"SWARM_BACKEND is {chosen!r}: it is mlx or vllm")
        return chosen
    return "mlx" if sys.platform == "darwin" else "vllm"
