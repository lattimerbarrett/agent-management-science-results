"""One streamed model response for the playgrounds (serve.py, swarm_play.py): every delta passed on as it comes."""

import json
import random
import time

import openai

from llm import Unfinished, as_reply, final, refused, retryable

NO_CALLS = "You ended your turn without calling a tool."  # agent.NO_CALLS
CUT_OFF = ("Your last response was cut off because it reached the output limit, and its tool calls (if any) were not "
           "run. Keep each response shorter: write long code to the scratchpad in smaller steps.")  # agent.CUT_OFF


def code(name, args):
    """What a call wrote, as text: the file for write/run, the change for an edit, the answer for a submission."""
    if name == "edit_scratchpad":
        old, new = (args.get(k, "").splitlines() for k in ("old_string", "new_string"))
        return "\n".join([f"- {x}" for x in old] + [f"+ {x}" for x in new])
    if name == "submit_answer":
        return args.get("answer", "")
    return args.get("content", "")


def longer_runs(tools, seconds):
    """`tools` with run_scratchpad's timeout allowed up to `seconds`, as the model is shown it (set
    scratchpad.MAX_SECONDS to match, which is what a run is held to)."""
    out = []
    for t in tools:
        if t["name"] == "run_scratchpad":
            t = json.loads(json.dumps(t))
            ts = t["input_schema"]["properties"]["timeout_seconds"]
            old = ts["maximum"]
            ts["maximum"] = seconds
            ts["description"] = ts["description"].replace(f"at most {old}", f"at most {seconds}")
        out.append(t)
    return out


def shown(name, args):
    """What the page shows of a call as it is made: `code`, and a Slack message's text."""
    if name == "slack_post":
        return args.get("text", "") + (f"\n\n(in thread #{args['thread']})" if args.get("thread") is not None else "")
    if name == "slack_read":
        return json.dumps(args) if args else ""
    return code(name, args)


def respond(llm, messages, n, emit, stop):
    """Response `n` to `messages`, streamed: its deltas go to `emit` (think, say, call, args, called, note) as they come.
    Raises InterruptedError when `stop` is set. Returns the reply (llm.as_reply), a refusal for a prompt OpenAI flags.
    Retried as OpenAILLM.send retries (rate limits, overload, dropped streams: `llm.attempts` tries, random exponential
    waits of up to 3 minutes), so that several swarms at once ride out rate limits instead of losing agents."""
    request = llm.request(messages, llm.max_tokens)

    def forward(events):
        for e in events:
            if stop.is_set():
                raise InterruptedError
            t = e.type
            if t == "response.output_item.added" and e.item.type == "function_call":
                emit(k="call", id=e.item.id, name=e.item.name)
            elif t == "response.reasoning_summary_part.added":
                emit(k="think", text="\n\n")
            elif t == "response.reasoning_summary_text.delta":
                emit(k="think", text=e.delta)
            elif t == "response.output_text.delta":
                emit(k="say", text=e.delta)
            elif t == "response.function_call_arguments.delta":
                emit(k="args", id=e.item_id, text=e.delta)
            elif t == "response.output_item.done" and e.item.type == "function_call":
                try:
                    args = json.loads(e.item.arguments or "{}")
                except ValueError:
                    args = {}
                emit(k="called", id=e.item.id, call_id=e.item.call_id, name=e.item.name,
                     code=shown(e.item.name, args if isinstance(args, dict) else {}))  # fmt: skip
            yield e

    for attempt in range(1, llm.attempts + 1):
        try:
            with llm.client.responses.create(**request, stream=True) as events:
                response = final(forward(events))
            if response.status == "failed":
                if response.error and response.error.code == "invalid_prompt":
                    return refused("invalid_prompt", response.error.message)
                raise Unfinished(f"response {response.id} failed: {response.error}")
            return as_reply(response)
        except InterruptedError:
            raise
        except openai.BadRequestError as e:
            if e.code != "invalid_prompt":
                raise
            return refused("invalid_prompt", e.message)
        except Exception as e:
            if attempt == llm.attempts or not retryable(e):
                raise
            wait = random.uniform(0, min(180, 4 * 2**attempt))  # as tenacity's wait_random_exponential(4, max=180)
            emit(k="note", text=f"response {n} failed ({type(e).__name__}); asking again in {wait:.0f} s")
            for _ in range(int(wait * 10)):  # a Stop doesn't wait out the pause
                if stop.is_set():
                    raise InterruptedError
                time.sleep(0.1)
