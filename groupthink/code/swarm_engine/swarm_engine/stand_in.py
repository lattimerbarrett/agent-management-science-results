"""A stand-in for a vLLM server, for tests here and in the repos that use this engine: the few endpoints vllm.py
uses, answered by a model that is a function. No GPU, no model, no network but this machine's own.

    with FakeVLLM(lambda tokens: 7) as server:      # a model that always writes token 7
        engine = stand_in_engine(server.url)

`model(tokens)` is given everything read and written so far and returns the next token. Or `whole(prompt, body)`
returns all the model would write after a prompt, and the server cuts it where a real one would stop. The
server keeps to what vLLM does with a request: it stops on a stop token (the end of turn is reported with no
`stop_reason`, any other with its id) or at `max_tokens`, hands back the token ids it wrote, and says how many
tokens of the prompt it already held: whole blocks that an earlier request read or wrote. How a real server keeps
what it has read is its own affair and differs by model (blocks of 16 of everything, or for a model like Qwen3.5
a coarser grid of what was read as a prompt): `block` and `keeps_written` set which this one does, and nothing
in vllm.py may depend on it. Every request's body is kept in `asked`. Given a `tokenizer`, it cuts text into
tokens at /tokenize as a real server does.

It is what vllm.py was written against, not vLLM: `swarm-vllm check` holds the engine against the real server.
"""
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BLOCK = 16


class FakeVLLM:
    def __init__(self, model=None, name: str = "stand-in", limit: int = 100_000, end_of_turn: int = 9, keeps_stop: bool = False,
                 fail: list | None = None, whole=None, root: str = "/models/stand-in", block: int = BLOCK,
                 keeps_written: bool = True, forgets: bool = False, tokenizer=None, version: str = "stand-in"):
        self.model, self.name, self.limit, self.end_of_turn, self.keeps_stop = model, name, limit, end_of_turn, keeps_stop
        self.whole, self.root, self.block, self.keeps_written, self.forgets = whole, root, block, keeps_written, forgets
        self.tokenizer, self.version = tokenizer, version
        self.delay = 0.0                             # seconds it sits on a request before it answers
        self.cut_as = "length"                       # what it calls a reply that ran into `max_tokens`
        self.fail = list(fail or [])                 # HTTP codes to answer the next requests with, before answering properly
        self.asked: list[dict] = []
        self.held: set[tuple] = set()                # the starts it has read or written, in whole blocks
        self.lock = threading.Lock()
        self.flying = self.widest = 0
        fake = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def send(self, code: int, body: dict):
                data = json.dumps(body).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):
                if self.path == "/health":
                    return self.send(200, {})
                if self.path == "/version":
                    return self.send(200, {"version": fake.version})
                if self.path == "/v1/models":
                    return self.send(200, {"data": [{"id": fake.name, "root": fake.root, "max_model_len": fake.limit}]})
                self.send(404, {"error": "no such path"})

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                if self.path == "/tokenize" and fake.tokenizer is not None:
                    return self.send(200, {"tokens": fake.tokenizer.encode(body["prompt"], add_special_tokens=False)})
                with fake.lock:
                    fake.asked.append(body)
                    failing = fake.fail.pop(0) if fake.fail else None
                    fake.flying += 1
                    fake.widest = max(fake.widest, fake.flying)
                try:
                    if failing:
                        return self.send(failing, {"error": {"message": "the stand-in was told to fail"}})
                    if len(body["prompt"]) + body["max_tokens"] > fake.limit:
                        return self.send(400, {"error": {"message": "This model's maximum context length is exceeded"}})
                    time.sleep(fake.delay)
                    try:
                        answer = fake.complete(body)
                    except Exception as problem:                 # the model that is a function went wrong: said at once
                        return self.send(400, {"error": {"message": f"the stand-in's model went wrong: {type(problem).__name__}: {problem}"}})
                    self.send(200, answer)
                except (BrokenPipeError, ConnectionResetError):      # whoever asked has gone
                    pass
                finally:
                    with fake.lock:
                        fake.flying -= 1

        class Quiet(ThreadingHTTPServer):
            def handle_error(self, request, client_address):     # a caller that hung up is not news
                pass

        self.httpd = Quiet(("127.0.0.1", 0), Handler)
        self.httpd.daemon_threads = True
        self.url = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    def complete(self, body: dict) -> dict:
        prompt, stops, block = list(body["prompt"]), set(body.get("stop_token_ids") or ()), self.block
        with self.lock:
            cached = 0
            while cached + block <= len(prompt) and tuple(prompt[:cached + block]) in self.held:
                cached += block
        tokens, written, reason, stop = list(prompt), [], self.cut_as, None
        script = iter(self.whole(prompt, body)) if self.whole is not None else None
        while len(written) < body["max_tokens"]:
            token = next(script, self.end_of_turn) if script is not None else self.model(tokens)
            tokens.append(token)
            if token == self.end_of_turn or token in stops:
                reason, stop = "stop", (None if token == self.end_of_turn else token)
                if self.keeps_stop:
                    written.append(token)
                break
            written.append(token)
        with self.lock:
            if not self.forgets:
                for end in range(block, len(tokens if self.keeps_written else prompt) + 1, block):
                    self.held.add(tuple(tokens[:end]))
        return {"choices": [{"index": 0, "text": "", "token_ids": written, "finish_reason": reason, "stop_reason": stop}],
                "usage": {"prompt_tokens": len(prompt), "completion_tokens": len(written) + (reason == "stop" and not self.keeps_stop),
                          "prompt_tokens_details": {"cached_tokens": cached}}}

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *_):
        self.httpd.shutdown()
        self.httpd.server_close()


class Tokenizer:
    """A token is a number, and text is numbers with spaces between them."""
    eos_token_id = 9

    def decode(self, tokens):
        return " ".join(str(token) for token in tokens)

    def encode(self, text, add_special_tokens=False):
        return [int(word) for word in text.split()]


def stand_in_engine(url: str, width: int = 64, close: int = 90, out_of_time=(70, 90), name: str = "stand-in",
                    path: str = "/models/stand-in"):
    """A vLLM engine that talks to `url`, with no tokenizer files and nothing downloaded: a prompt is its tokens."""
    import httpx

    from swarm_engine.vllm import Engine
    e = Engine.__new__(Engine)
    e.alias = e.name = name
    e.revision, e.model_path, e.server, e.say = None, path, None, lambda line: None
    e.tokenizer, e.artifact_hashes, e.versions, e._source_hash = Tokenizer(), {}, {}, "source"
    e.end_of_turn, e.close, e._out_of_time, e.end_tokens = Tokenizer.eos_token_id, close, list(out_of_time), {Tokenizer.eos_token_id}
    e.url, e._httpx, e.width, e.stall, e._heard, e.machine = url, httpx, width, 60.0, 0.0, {}
    e.served, e.context_limit, e.vllm_version = e._hello()
    e.encode = lambda prompt, thinking=False, tools=None: list(prompt)
    e.calls = e.new_tokens = e.read_tokens = e.spared_tokens = e.sampled_tokens = e.injected_tokens = e.prompt_tokens = 0
    e.answer_read_tokens = 0
    e.last_run, e.seconds, e.groups = {}, 0.0, []
    return e
