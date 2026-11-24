"""What every backend shares: what a reply is, and which random stream a call draws from.

Nothing here imports a model library, so it loads on a machine that has no MLX (a GPU server) as on this Mac.

`engine.py`, the MLX backend, was written before there was a second one and has its own copy of each of these.
It is not edited without a `swarm-check`, which needs the model, so the copies stay, and `tests/test_backends.py`
holds them equal: change one and that test says so.
"""
from __future__ import annotations

import zlib
from dataclasses import dataclass, field

import numpy as np

# What Qwen is given when a thought is still open at its budget (from the Qwen3 model card).
OUT_OF_TIME = ("\n\nConsidering the limited time by the user, I have to give the solution based on the thinking "
               "directly now.\n</think>\n\n")

Prompt = str | tuple[str, str] | list[dict]   # a user message, (system, user), or chat messages


@dataclass
class Reply:
    text: str                                 # the answer, without any thinking
    tokens: list[int]                         # the answer's token ids, as written (with its end-of-turn token)
    thought: str = ""                         # what the model thought first, as a person would want to read it
    reasoning: str = ""                       # the thought as the model had it before it when it answered: with the words
                                              # that closed it, when its budget ran out. What a chat passes back as its
                                              # `reasoning_content` if the conversation is to carry on from here
    thought_tokens: list[int] | None = None   # everything between the prompt and the answer, as the model saw it
    finished_thinking: bool | None = None     # False if the thought was closed for it; None if thinking was off
    stopped: bool = True                      # completion ended with a model-sampled EOS
    finish_reason: str = "stop"               # stop, answer_limit, total_limit, end_in_thought
    seed: int | None = None
    prompt_tokens: int = 0
    sampled_tokens: int = 0
    injected_tokens: int = 0                   # forced bridge and any synthetic termination EOS
    injected_positions: list[int] = field(default_factory=list)
    output_tokens: list[int] = field(default_factory=list)  # exact emitted sequence, including forced tokens
    metadata: dict = field(default_factory=dict)


def stream(seed: int, context: list[int]) -> int:
    """Which random stream a call draws from: fixed by who is asking (`seed`) and by exactly what they were
    asked. The same question from the same asker always draws the same numbers, while a different question gets
    fresh randomness (so an agent's successive answers are independent draws)."""
    asked = zlib.crc32(np.asarray(context, dtype=np.int32).tobytes())
    return int(np.random.SeedSequence([seed, asked]).generate_state(1)[0])
