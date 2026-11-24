"""Run a swarm of agents on one local model: on this Mac through MLX, on a GPU through vLLM. See README.md.

    from swarm_engine import Engine, under_lock      # the engine this kind of machine has
    from swarm_engine import backend                 # the engine that runs a given model: backend("9B-bf16")
"""
import sys

from .machine import available_gb, guard, locked, require_lock, under_lock
from .models import KNOWN, backend_of
from .settings import Sampling, trial_seed

__all__ = ["Engine", "Reply", "MODELS", "KNOWN", "Sampling", "trial_seed", "backend", "backend_of", "under_lock", "require_lock",
           "locked", "available_gb", "guard"]


def backend(model: str = "4B", **settings):
    """The engine that runs `model`: MLX's on a Mac (engine.py), vLLM's on a GPU (vllm.py). models.py says which
    for the names it knows. Both take the same calls (`generate`, `converse`) and hand back the same replies."""
    if backend_of(model) == "vllm":
        from .vllm import Engine as OnGPU
        return OnGPU(model, **settings)
    from .engine import Engine as OnMac
    return OnMac(model, **settings)


def __getattr__(name: str):
    """An engine imports its model library (MLX, which only a process under the machine lock should load on a
    Mac): load it when asked for. On a Mac these are the MLX engine's own, as they always were; anywhere else
    there is no MLX, and they are the vLLM engine's."""
    if name in ("Engine", "Reply", "MODELS"):
        if sys.platform == "darwin":
            from . import engine
            return getattr(engine, name)
        if name == "Engine":
            from .vllm import Engine
            return Engine
        from . import common, models
        return common.Reply if name == "Reply" else models.MODELS
    raise AttributeError(name)
