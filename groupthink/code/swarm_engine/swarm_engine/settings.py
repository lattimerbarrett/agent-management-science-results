"""Serializable decoding settings and reproducible trial seeds (no MLX import)."""
import hashlib
import math
from dataclasses import dataclass


def integer(name: str, value: int, minimum: int = 0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


@dataclass(frozen=True)
class Sampling:
    """Temperature, then top-k, top-p and min-p; penalties use generated tokens.

    These defaults are Qwen3.5's general thinking preset. Use ``Sampling.coding()``
    for its precise-coding preset. The same settings apply throughout a reply.
    Greedy decoding (temperature=0) ignores probability filters, but not penalties.
    """
    temperature: float = 1.0
    top_k: int = 20
    top_p: float = 0.95
    min_p: float = 0.0
    presence_penalty: float = 1.5
    repetition_penalty: float = 1.0

    def __post_init__(self):
        integer("top_k", self.top_k)
        for name in ("temperature", "top_p", "min_p", "presence_penalty", "repetition_penalty"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"{name} must be a finite number")
        if self.temperature < 0 or not 0 < self.top_p <= 1 or not 0 <= self.min_p <= 1:
            raise ValueError("temperature must be >= 0, top_p in (0, 1], min_p in [0, 1]")
        if not -2 <= self.presence_penalty <= 2 or self.repetition_penalty <= 0:
            raise ValueError("presence_penalty must be in [-2, 2], repetition_penalty > 0")

    @classmethod
    def coding(cls):
        return cls(temperature=0.6, presence_penalty=0.0)


def trial_seed(run: int, agent: int, attempt: int = 0) -> int:
    """Stable 64-bit seed for a run, agent and attempt; independent of batch order."""
    for name, value in (("run", run), ("agent", agent), ("attempt", attempt)):
        integer(name, value)
    return int.from_bytes(hashlib.sha256(f"swarm-trial-v1:{run}:{agent}:{attempt}".encode()).digest()[:8], "little")
