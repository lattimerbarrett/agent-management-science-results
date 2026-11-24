# llm.py
"""One model call per agent turn: the request, its retries, and what it cost.

Every call streams (`beta.messages.stream` + `get_final_message`), so a long adaptive-thinking turn never runs
into an HTTP timeout, and goes through the beta namespace for the turn-scoped system notices agents get each
turn (`clear_at`, see agent.py). Apart from `messages`, the request is identical on every turn of every agent of
an arm (same system prompt, same tools), so the prompt cache covers everything before the newest turn: the
top-level `cache_control` moves the breakpoint forward as the conversation grows. The TTL is 1 hour because a
step waits for its slowest agent (a long Python run, a long think), and a 5-minute entry would often expire.
A tool declared deferred (submit_answer before answers open, submit.declared) is added by a message in the
conversation (`tool_addition`, under the tool-changes beta), so the tools stay the same too. Idea tracking (`fork`,
ideas.py) sends the same request with one more message, so it reads the same cache.

Thinking is adaptive with `display: "summarized"`: the summaries cost nothing extra and make the logs readable
(Sonnet 5.5 otherwise returns empty thinking blocks, including the notes it writes between tool calls).

Refusal fallback (`fallbacks`) is off by default: a server-side fallback answers with another model, which would
mix a second model into a measurement of this one. Refusals are retried and logged instead (agent.py).

`OpenAILLM` makes the same calls to an OpenAI model (`--provider openai`), through its Responses API, on the same
conversation (`responses_input` says how it is sent there).
"""

import json
import threading
import time
from contextlib import nullcontext
from dataclasses import dataclass, field
from types import SimpleNamespace

import anthropic
import openai
from anthropic.types.beta import BetaMessage, BetaTextBlock, BetaThinkingBlock, BetaToolUseBlock, BetaUsage
from openai.types.responses import ResponseUsage
from tenacity import Retrying, retry_if_exception, stop_after_attempt, wait_random_exponential

CLEAR_AT_BETA = "mid-conversation-system-clear-at-2026-08-21"
TOOL_CHANGES_BETA = "mid-conversation-tool-changes-2026-07-01"
FALLBACK_BETA = "server-side-fallback-2026-07-01"

# $ per million tokens of each kind usage_dict counts. OpenAI's: its standard tier, for requests of up to 272K input
# tokens (developers.openai.com/api/docs/pricing, read 2026-10-27); a cache write there lasts 30 minutes.
PRICES = {
    "claude-sonnet-5-5": {"input": 2.00, "output": 10.00, "cache_write_5m": 2.50, "cache_write_1h": 4.00, "cache_read": 0.20},
    "claude-opus-5-5": {"input": 4.00, "output": 20.00, "cache_write_5m": 5.00, "cache_write_1h": 8.00, "cache_read": 0.20},
    "claude-haiku-5-5": {"input": 0.10, "output": 0.50, "cache_write_5m": 0.125, "cache_write_1h": 0.20, "cache_read": 0.01},
    "gpt-6.1-sol": {"input": 2.00, "output": 10.00, "cache_write_30m": 2.50, "cache_read": 0.10},
}  # fmt: skip
# Models that cost more for a request above some number of input tokens: (that number, the prices then).
LONG_CONTEXT = {
    "gpt-6.1-sol": (272_000, {"input": 4.00, "output": 15.00, "cache_write_30m": 5.00, "cache_read": 0.20}),
}


def usage_dict(u) -> dict:
    """Token counts of one response, flat: input (uncached), cache writes by TTL, cache reads, output, thinking.
    OpenAI's input_tokens include what was read from the cache and what was written to it; here input is the rest."""
    if isinstance(u, ResponseUsage):
        read, written = u.input_tokens_details.cached_tokens or 0, u.input_tokens_details.cache_write_tokens or 0
        return {"input": u.input_tokens - read - written, "cache_write_30m": written, "cache_read": read,
                "output": u.output_tokens, "thinking": u.output_tokens_details.reasoning_tokens or 0}  # fmt: skip
    cc = getattr(u, "cache_creation", None)
    w5 = getattr(cc, "ephemeral_5m_input_tokens", None) if cc else None
    w1 = getattr(cc, "ephemeral_1h_input_tokens", None) if cc else None
    if w5 is None and w1 is None:  # no breakdown: count every write as 5-minute
        w5, w1 = u.cache_creation_input_tokens or 0, 0
    details = getattr(u, "output_tokens_details", None)
    return {
        "input": u.input_tokens or 0,
        "cache_write_5m": w5 or 0,
        "cache_write_1h": w1 or 0,
        "cache_read": u.cache_read_input_tokens or 0,
        "output": u.output_tokens or 0,
        "thinking": getattr(details, "thinking_tokens", 0) or 0,
    }


def prompt_tokens(usage: dict) -> int:
    """All the input of one response (usage_dict): uncached, written to the cache and read from it."""
    return sum(n for kind, n in usage.items() if kind == "input" or kind.startswith("cache_"))


def cost(model, usage: dict) -> float:
    """Dollars for one response's usage (usage_dict). 0 for a model with no price listed."""
    prices = PRICES.get(model, {})
    if model in LONG_CONTEXT and prompt_tokens(usage) > LONG_CONTEXT[model][0]:
        prices = LONG_CONTEXT[model][1]
    return sum(usage.get(kind, 0) * price for kind, price in prices.items()) / 1e6


class Unfinished(Exception):
    """An OpenAI response that failed on the server, or a stream that ended without a response: tried again."""


def retryable(e) -> bool:
    """Rate limits, overload, server errors and dropped connections are retried; anything else is a bug."""
    if isinstance(e, (anthropic.APIConnectionError, openai.APIConnectionError, Unfinished)):
        return True
    if isinstance(e, anthropic.APIStatusError):
        kind = getattr(e, "type", None)
        return e.status_code in (408, 409, 429) or e.status_code >= 500 or kind in (
            "overloaded_error",
            "api_error",
            "rate_limit_error",
        )
    if isinstance(e, openai.APIStatusError):  # but no credit left is not worth waiting for
        return (e.status_code in (408, 409, 429) or e.status_code >= 500) and e.code != "insufficient_quota"
    return isinstance(e, openai.APIError)  # an error event in the middle of a stream: the server's


@dataclass(frozen=True)
class Reply:
    message: BetaMessage
    request_id: str | None
    seconds: float
    attempts: int


@dataclass(frozen=True)
class LLM:
    client: anthropic.Anthropic
    model: str
    system: str
    tools: list[dict]
    max_tokens: int
    effort: str
    cache_ttl: str = "1h"
    fallbacks: bool = False
    gate: threading.Semaphore | None = field(default=None, compare=False)  # caps calls in flight
    attempts: int = 8  # tries per call for retryable errors, on top of the SDK's own retries

    def create(self, messages) -> Reply:
        cache = {"type": "ephemeral", "ttl": self.cache_ttl}
        return self.send(self.request(messages, self.max_tokens, cache_control=cache))

    def fork(self, messages, question, max_tokens, after=()) -> Reply:
        """Ask `question` of a copy of a conversation that ends in a user turn (ideas.py), in a system message after
        it; `messages` isn't changed. The request is the conversation's own but for that message, and its one
        breakpoint is the end of that user turn: where the conversation's next call caches up to, since the turn
        notice after it can't be cached. No automatic breakpoint, which would write the question to the cache.
        `after`: messages that follow the question in the copy (a reply to it and a question on, vs.py)."""
        return self.send(self.forked(messages, question, max_tokens, after))

    def forked(self, messages, question, max_tokens, after=()) -> dict:
        """The request `fork` sends."""
        last = messages[-1]
        assert last["role"] == "user", "a fork starts after a user turn"
        content = last["content"]
        if isinstance(content, str):
            content = [{"type": "text", "text": content}]
        marked = {**content[-1], "cache_control": {"type": "ephemeral", "ttl": self.cache_ttl}}
        forked = [*messages[:-1], {**last, "content": [*content[:-1], marked]}, {"role": "system", "content": question},
                  *after]  # fmt: skip
        return self.request(forked, max_tokens)

    def request(self, messages, max_tokens, **cache) -> dict:
        """What a call sends: the keyword arguments of `beta.messages.stream`."""
        betas = [CLEAR_AT_BETA] + ([FALLBACK_BETA] if self.fallbacks else [])
        if any(t.get("defer_loading") for t in self.tools):
            betas.append(TOOL_CHANGES_BETA)
        extra = {"fallbacks": "default"} if self.fallbacks else {}
        return dict(model=self.model, system=self.system, tools=self.tools, max_tokens=max_tokens, messages=messages,
                    thinking={"type": "adaptive", "display": "summarized"}, output_config={"effort": self.effort},
                    betas=betas, **cache, **extra)  # fmt: skip

    def send(self, request) -> Reply:
        """Make a call (`request`), retrying what can be retried."""
        started = time.monotonic()
        retrying = Retrying(
            retry=retry_if_exception(retryable),
            wait=wait_random_exponential(multiplier=4, max=180),
            stop=stop_after_attempt(self.attempts),
            reraise=True,
        )
        for attempt in retrying:
            with attempt:
                with self.gate or nullcontext():
                    with self.client.beta.messages.stream(**request) as stream:
                        message = stream.get_final_message()
                        rid = stream.request_id
                return Reply(message, rid, time.monotonic() - started, attempt.retry_state.attempt_number)


# ---- OpenAI ----------------------------------------------------------------

OPENAI_TIMEOUT = 1800.0  # seconds without a byte from a stream before it counts as dropped: a long reasoning is quiet


def openai_client():
    return openai.OpenAI(max_retries=3, timeout=OPENAI_TIMEOUT)


@dataclass(frozen=True)
class OpenAILLM:
    """LLM's calls, to an OpenAI model through its Responses API: the same conversation (agent.py's, in Claude's
    message format), sent as `responses_input` converts it, and the reply read back as a Claude message (`OpenAIReply`),
    so that agent.py, ideas.py and vs.py work unchanged.

    Every reasoning item goes back with the turn it came in (`reasoning.context` "all_turns", as Claude's thinking
    blocks do) and nothing is stored at OpenAI (`store` false): its reasoning travels encrypted in each item, as Claude's
    does in a thinking block's signature. Summaries of it (`summary` "auto") make the logs readable, as Claude's do.

    The prompt cache needs nothing set: OpenAI writes an entry at the end of the request's last user message or last
    group of tool results, never at a developer message after them (developers.openai.com/api/docs/guides/prompt-caching).
    So an agent's call caches its conversation up to the end of its last turn's tool results, the turn notice after
    them left out, and a fork (the question after the same results) reads that entry and writes none (checked
    2026-10-27). An entry lasts 30 minutes at least, and a write costs 1.25 times uncached input."""

    client: openai.OpenAI
    model: str
    system: str
    tools: list[dict]  # as agent.py's toolbox has them (tools.yaml): converted for each request
    max_tokens: int
    effort: str
    gate: threading.Semaphore | None = field(default=None, compare=False)  # caps calls in flight
    attempts: int = 8  # tries per call for retryable errors, on top of the SDK's own retries

    def create(self, messages) -> Reply:
        return self.send(self.request(messages, self.max_tokens))

    def fork(self, messages, question, max_tokens, after=()) -> Reply:
        """LLM.fork: `question` asked of a copy of a conversation that ends in a user turn, in a developer message after
        it. `after`: messages that follow the question in the copy."""
        return self.send(self.forked(messages, question, max_tokens, after))

    def forked(self, messages, question, max_tokens, after=()) -> dict:
        assert messages[-1]["role"] == "user", "a fork starts after a user turn"
        return self.request([*messages, {"role": "system", "content": question}, *after], max_tokens)

    def request(self, messages, max_tokens) -> dict:
        """What a call sends: the keyword arguments of `responses.create` (send streams it)."""
        tools, items = responses_input(messages, self.tools)
        return dict(model=self.model, instructions=self.system, tools=tools, input=items, max_output_tokens=max_tokens,
                    reasoning={"effort": self.effort, "summary": "auto", "context": "all_turns"}, store=False)  # fmt: skip

    def send(self, request) -> Reply:
        """Make a call (`request`), retrying what can be retried. A prompt OpenAI flags (invalid_prompt) is a refusal."""
        started = time.monotonic()
        retrying = Retrying(
            retry=retry_if_exception(retryable),
            wait=wait_random_exponential(multiplier=4, max=180),
            stop=stop_after_attempt(self.attempts),
            reraise=True,
        )
        for attempt in retrying:
            with attempt:
                tries = attempt.retry_state.attempt_number
                with self.gate or nullcontext():
                    try:
                        with self.client.responses.create(**request, stream=True) as events:
                            rid = events.response.headers.get("x-request-id")
                            response = final(events)
                    except openai.BadRequestError as e:
                        if e.code != "invalid_prompt":
                            raise
                        return Reply(refused("invalid_prompt", e.message), e.request_id, time.monotonic() - started, tries)
                if response.status == "failed":
                    if response.error and response.error.code == "invalid_prompt":
                        return Reply(refused("invalid_prompt", response.error.message), rid, time.monotonic() - started,
                                     tries)  # fmt: skip
                    raise Unfinished(f"response {response.id} failed: {response.error}")
                return Reply(as_reply(response), rid, time.monotonic() - started, tries)


def final(events):
    """The response a stream of Responses API events ends with (completed, incomplete or failed). When its last event
    leaves the output out, it is the items each `response.output_item.done` event gave, as the SDK's stream helper
    does (which won't return a response that didn't complete)."""
    done, last = {}, None
    for event in events:
        if event.type == "response.output_item.done":
            done[event.output_index] = event.item
        elif event.type in ("response.completed", "response.incomplete", "response.failed"):
            last = event.response
    if last is None:
        raise Unfinished("the stream ended without a response")
    if last.output is None:
        last = last.model_copy(update={"output": [done[i] for i in sorted(done)]})
    return last


@dataclass(frozen=True)
class Part:
    """An output item of an OpenAI response, as the Claude content block agent.py reads: "thinking" (a reasoning item,
    its summary as `thinking`), "text" (a message, its text) or "tool_use" (a function call, its call_id as `id` and its
    arguments as `input`: parsed, or the string if they aren't JSON, which the toolbox then rejects). `item` is the
    item as it came, which to_dict keeps so that it goes back to OpenAI unchanged (responses_input)."""

    type: str
    item: dict
    thinking: str = ""
    text: str = ""
    id: str = ""
    name: str = ""
    input: object = None

    def to_dict(self) -> dict:
        own = {"thinking": ["thinking"], "text": ["text"], "tool_use": ["id", "name", "input"]}[self.type]
        return {"type": self.type, **{k: getattr(self, k) for k in own}, "openai": self.item}


@dataclass(frozen=True)
class OpenAIReply:
    """An OpenAI response, as the Claude message agent.py, ideas.py and vs.py read: content blocks (Part), a stop reason
    (end_turn, tool_use, max_tokens or refusal), usage (usage_dict reads it) and, for a refusal, its category and
    explanation."""

    content: list[Part]
    stop_reason: str
    usage: ResponseUsage
    stop_details: SimpleNamespace | None = None
    id: str | None = None


NO_USAGE = ResponseUsage(input_tokens=0, input_tokens_details={"cached_tokens": 0, "cache_write_tokens": 0},
                         output_tokens=0, output_tokens_details={"reasoning_tokens": 0}, total_tokens=0)  # fmt: skip


def refused(category, explanation, usage=NO_USAGE, response_id=None) -> OpenAIReply:
    return OpenAIReply([], "refusal", usage, SimpleNamespace(category=category, explanation=explanation), response_id)


def as_reply(response) -> OpenAIReply:
    """A Responses API response as a Claude message (OpenAIReply). A refusal: a refusal part in a message, or the content
    filter stopping the response."""
    parts, refusals = [], []
    for item in response.output:
        raw = item.model_dump(mode="json", by_alias=True, exclude_none=True)
        if item.type == "reasoning":
            parts.append(Part("thinking", raw, thinking="\n\n".join(s.text for s in item.summary)))
        elif item.type == "message":
            refusals += [c.refusal for c in item.content if c.type == "refusal"]
            parts.append(Part("text", raw, text="".join(c.text for c in item.content if c.type == "output_text")))
        elif item.type == "function_call":
            try:
                args = json.loads(item.arguments) if item.arguments.strip() else {}
            except ValueError:
                args = item.arguments
            parts.append(Part("tool_use", raw, id=item.call_id, name=item.name, input=args))
        else:
            raise ValueError(f"an output item of type {item.type}: the harness gives the model only functions")
    usage = response.usage or NO_USAGE
    reason = response.incomplete_details.reason if response.incomplete_details else None
    if refusals or reason == "content_filter":
        return refused("refusal" if refusals else reason, "\n".join(refusals) or None, usage, response.id)
    if response.status == "incomplete":
        stop = "max_tokens" if reason == "max_output_tokens" else reason
    else:
        stop = "tool_use" if any(p.type == "tool_use" for p in parts) else "end_turn"
    return OpenAIReply(parts, stop, usage, None, response.id)


def function(tool) -> dict:
    """A harness tool (tools.yaml: name, description, input_schema) as an OpenAI function."""
    return {"type": "function", "name": tool["name"], "description": tool["description"],
            "parameters": tool["input_schema"], "strict": False}  # fmt: skip


def responses_input(messages, tools) -> tuple[list[dict], list[dict]]:
    """A conversation in agent.py's message format (Claude's), and the harness's tools, as the Responses API takes
    them: (tools, input items).

    - What the model wrote goes back as the output items it came as (Part.to_dict keeps them), reasoning items
      included, in order. A text block that never came from OpenAI (agent.py's "(cut off)") is an assistant message.
    - A user message is a user message; tool results are function call outputs, an error's text after "Error: " (OpenAI
      has no error flag); a system message (a turn notice, the ideas question) is a developer message.
    - A deferred tool (`defer_loading`: submit_answer before answers open, submit.declared) is left out of `tools`, and
      the system message that adds it (submit.OPEN) becomes an `additional_tools` item: the tools, and so the cache of
      everything before that turn, stay as they were, and the model isn't shown the tool before then.
    The turn notices stay in the conversation: Claude's `clear_at` has no form at OpenAI, and the model reasoned after
    them. So the input only grows, and the request for each turn begins with the request for the turn before."""
    by_name = {t["name"]: t for t in tools}
    items = []
    for m in messages:
        blocks = m["content"] if isinstance(m["content"], list) else [{"type": "text", "text": m["content"]}]
        for b in blocks:
            if m["role"] == "assistant":
                if "openai" in b:
                    items.append(b["openai"])
                elif b["type"] == "text":
                    items.append({"role": "assistant", "content": b["text"]})
                elif b["type"] == "tool_use":
                    items.append({"type": "function_call", "call_id": b["id"], "name": b["name"],
                                  "arguments": json.dumps(b["input"])})  # fmt: skip
                else:
                    raise ValueError(f"no OpenAI form for a {b['type']} block that didn't come from OpenAI")
            elif b["type"] == "tool_result":
                c = b["content"] if isinstance(b["content"], str) else "".join(x.get("text", "") for x in b["content"])
                items.append({"type": "function_call_output", "call_id": b["tool_use_id"],
                              "output": f"Error: {c}" if b.get("is_error") else c})  # fmt: skip
            elif b["type"] == "text":
                items.append({"role": "developer" if m["role"] == "system" else "user", "content": b["text"]})
            elif b["type"] == "tool_addition":
                items.append({"type": "additional_tools", "role": "developer",
                              "tools": [function(by_name[b["tool"]["name"]])]})  # fmt: skip
            else:
                raise ValueError(f"no OpenAI form for a {b['type']} block")
    return [function(t) for t in tools if not t.get("defer_loading")], items


# ---- a scripted stand-in, for dry runs and tests --------------------------


class ScriptedLLM:
    """Plays a fixed little routine with whatever tools it is given, without calling the API: write a script,
    run it, (with comms) post and DM, then submit. For `--dry-run` and tests: it exercises every part of the
    harness except the model. `answer` is what it submits; `model` is only a label."""

    model = "scripted"

    def __init__(self, tools, answer="42", turns_before_submit=4):
        self.tools = tools
        self.names = {t["name"] for t in tools}
        self.answer = answer
        self.turns_before_submit = turns_before_submit
        self._n = 0
        self._lock = threading.Lock()

    def _id(self):
        with self._lock:
            self._n += 1
            return f"toolu_scripted_{self._n:06d}"

    def _use(self, name, **inp):
        return BetaToolUseBlock(type="tool_use", id=self._id(), name=name, input=inp)

    def create(self, messages) -> Reply:
        turn = 1 + sum(m["role"] == "assistant" for m in messages)
        me = next((w for w in messages[0]["content"].split() if w.startswith("agent_")), "agent").rstrip(".")
        talk = "post_to_board" in self.names
        blocks = [BetaThinkingBlock(type="thinking", thinking=f"Scripted turn {turn}.", signature="scripted")]
        if turn == 1:
            code = "import sympy\nprint('scripted', sympy.factorint(2**32 + 1))\n"
            blocks.append(self._use("write_scratchpad", content=code))
            if talk:
                blocks.append(self._use("post_to_board", content=f"{me} here: I will try {self.answer}."))
        elif turn == 2:
            blocks.append(self._use("run_scratchpad", timeout_seconds=30))
            if talk:
                blocks += [self._use("read_board"), self._use("send_dm", to="agent_0", content=f"hi from {me}")]
        elif turn < self.turns_before_submit:
            blocks.append(BetaTextBlock(type="text", text="Thinking it over."))  # a turn with no tool call
        else:
            if talk:
                blocks.append(self._use("read_dms"))
            blocks.append(self._use("submit_answer", answer=self.answer))
        stop = "tool_use" if any(b.type == "tool_use" for b in blocks) else "end_turn"
        usage = BetaUsage(input_tokens=1000, output_tokens=200, cache_read_input_tokens=0, cache_creation_input_tokens=0)
        message = BetaMessage.model_construct(
            id=f"msg_scripted_{turn}", type="message", role="assistant", model=self.model,
            content=blocks, stop_reason=stop, stop_sequence=None, usage=usage,
        )  # fmt: skip
        return Reply(message, None, 0.0, 1)

    def fork(self, messages, question, max_tokens) -> Reply:
        """A reply to ideas.md: one idea in the current approach."""
        turn = sum(m["role"] == "assistant" for m in messages)
        idea = {"statement": f"The answer is {self.answer}.", "confidence": 0.5, "basis": f"scripted, turn {turn}"}
        text = "```json\n" + json.dumps({"approach": [idea]}) + "\n```"
        usage = BetaUsage(input_tokens=50, output_tokens=100, cache_read_input_tokens=1000, cache_creation_input_tokens=0)
        message = BetaMessage.model_construct(
            id=f"msg_scripted_ideas_{turn}", type="message", role="assistant", model=self.model,
            content=[BetaTextBlock(type="text", text=text)], stop_reason="end_turn", stop_sequence=None, usage=usage,
        )  # fmt: skip
        return Reply(message, None, 0.0, 1)
