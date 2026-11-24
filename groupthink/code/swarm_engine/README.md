# swarm_engine, as the run used it

The engine that makes every model call for [`../math_swarm_explore/`](../math_swarm_explore/): on a GPU it starts
a vLLM server and sends it each call with its seed (`swarm_engine/vllm.py`, `vllm_server.py`), and it can rent the
GPU for a job and give it back (`swarm_engine/cloud/`). On a Mac it runs the model through MLX
(`swarm_engine/engine.py`), which this run did not use.

Here are the package and its two dependency files. What is left out, and how this copy differs from the lab's own,
are in the [section's README](../../README.md#code).

This page was written for this repo. The engine's own README is not here.
