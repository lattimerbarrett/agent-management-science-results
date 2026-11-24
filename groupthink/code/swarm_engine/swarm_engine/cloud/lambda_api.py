"""Lambda's cloud API, as far as a job needs it: which GPUs are free, launch one, look at it, terminate it.

    api = Lambda(key)
    free = api.free(["gpu_1x_h100_pcie", "gpu_1x_a100"])     # [(type, region, cents an hour)], in the order asked for
    machine = api.launch("gpu_1x_a10", "us-west-1", ssh_key="swarm-myserver", name="swarm-ab12cd-trial")
    api.status(machine)                                      # "booting", "active", ...; None: its list does not have it
    api.terminate(machine)

From its published description (the OpenAPI file at https://docs.lambda.ai/api/cloud/spec.json, version 1.10.0,
read on 2026-10-11): requests are JSON over HTTPS with the key as a Bearer token; an answer is {"data": ...} or
{"error": {"code", "message", "suggestion"}}; anything is limited to one request a second and a launch to one in
twelve seconds. A launch has no way of being asked twice safely, so a job names its machine and looks for that
name before it launches again (`named`).
"""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request

BASE = "https://cloud.lambda.ai/api/v1"
NO_CAPACITY = "instance-operations/launch/insufficient-capacity"
NO_SUCH = "global/object-does-not-exist"
GONE = ("terminated", "terminating", "preempted")       # of an instance's `status`: it is no longer anybody's to use


class Refused(Exception):
    """The API said no: `code` is its own name for why (match on that, as its description asks), `status` the HTTP status."""

    def __init__(self, code: str, message: str, status: int = 0):
        super().__init__(f"{code}: {message}")
        self.code, self.message, self.status = code, message, status


class Lambda:
    def __init__(self, key: str, base: str = BASE, pause: float = 1.1, send=None):
        """`pause` is the least time between two requests (the API allows one a second). `send(request, timeout)`
        stands in for the network in tests."""
        self.key, self.base, self.pause = key.strip(), base.rstrip("/"), pause
        if not re.fullmatch(r"[\x21-\x7e]+", self.key):         # it goes into a header, whole: anything else would be quoted
            raise ValueError("the Lambda API key is one word of plain characters, and what was given is not")   # in the error
        self.send = send or (lambda request, timeout: urllib.request.urlopen(request, timeout=timeout))
        self.last = self.last_launch = 0.0

    def ask(self, method: str, path: str, body: dict | None = None, tries: int = 5) -> dict | list:
        """One request, asked again when the API says it is asked too often or does not answer."""
        problem = None
        for attempt in range(tries):
            wait = self.last + self.pause - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            self.last = time.monotonic()
            request = urllib.request.Request(f"{self.base}{path}", method=method, data=json.dumps(body).encode() if body is not None else None,
                                             headers={"Authorization": f"Bearer {self.key}", "Accept": "application/json",
                                                      "Content-Type": "application/json", "User-Agent": "swarm-engine-cloud"})
            try:
                with self.send(request, 60) as answer:
                    return json.loads(answer.read().decode() or "{}").get("data", {})
            except urllib.error.HTTPError as refused:
                try:
                    error = json.loads(refused.read().decode()).get("error", {})
                except (ValueError, AttributeError):
                    error = {}
                code = error.get("code") or f"http/{refused.code}"
                if refused.code == 429 or refused.code >= 500:              # asked too often, or its own trouble: ask again
                    problem = Refused(code, error.get("message", ""), refused.code)
                    try:
                        wait = float(refused.headers.get("Retry-After") or 0)
                    except ValueError:                                       # given as a date
                        wait = 0.0
                    time.sleep(min(wait or 5.0 * (attempt + 1), 60.0) * (self.pause > 0))
                    continue
                raise Refused(code, " ".join(filter(None, [error.get("message"), error.get("suggestion")])), refused.code) from None
            except (urllib.error.URLError, TimeoutError, ConnectionError) as error:      # no network for a moment
                problem = error
                time.sleep(5.0 * (attempt + 1) * (self.pause > 0))
        raise ConnectionError(f"Lambda's API did not answer {method} {path} in {tries} tries ({problem})")

    # ---- what there is
    def types(self) -> dict:
        """Every kind of machine: {name: {"instance_type": {..., "price_cents_per_hour"}, "regions_with_capacity_available": [...]}}."""
        return self.ask("GET", "/instance-types")

    def free(self, wanted: list[str], regions: list[str] | None = None) -> list[tuple[str, str, int]]:
        """Where a machine of one of the `wanted` kinds can be had now: (kind, region, cents an hour), the kinds in
        the order they were asked for. `regions` keeps it to those."""
        types, out = self.types(), []
        for name in wanted:
            entry = types.get(name)
            if entry is None:
                raise Refused("unknown-instance-type", f"Lambda has no machine called {name} (it has {', '.join(sorted(types))})")
            for region in entry.get("regions_with_capacity_available", []):
                if regions is None or region["name"] in regions:
                    out.append((name, region["name"], entry["instance_type"]["price_cents_per_hour"]))
        return out

    def instances(self) -> list[dict]:
        """Every machine the account has. An answer that is not that list (a page from something in between) is
        an error here, never an account without machines: what is not in this list is taken to be gone."""
        listed = self.ask("GET", "/instances")
        if not isinstance(listed, list) or not all(isinstance(each, dict) for each in listed):
            raise Refused("unexpected-answer", "the list of machines came back as something else")
        return listed

    def status(self, machine: str) -> str | None:
        """What Lambda says of a machine: its `status`, or None when its list of machines does not have it. Read
        off the list, asked and answered, and off nothing else."""
        return next((i.get("status") or "unknown" for i in self.instances() if i.get("id") == machine), None)

    def named(self, name: str) -> list[dict]:
        """Every machine that carries a name and is still somebody's."""
        return [i for i in self.instances() if i.get("name") == name and i.get("status") not in GONE]

    # ---- launching and giving back
    def launch(self, kind: str, region: str, ssh_key: str, name: str, image: str | None = None) -> str:
        """Launch one machine and return its id. `Refused` with code `NO_CAPACITY` when it was taken meanwhile."""
        wait = self.last_launch + 12.5 * (self.pause > 0) - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        self.last_launch = time.monotonic()
        body = {"region_name": region, "instance_type_name": kind, "ssh_key_names": [ssh_key], "name": name[:64]}
        if image:
            body["image"] = {"family": image}
        made = self.ask("POST", "/instance-operations/launch", body, tries=1)
        return made["instance_ids"][0]

    def terminate(self, machine: str) -> None:
        """Give a machine back. Billing stops with this and with nothing else. Lambda saying, in its own words,
        that it has no such machine is fine; anything else that is not a yes is an error."""
        try:
            self.ask("POST", "/instance-operations/terminate", {"instance_ids": [machine]})
        except Refused as refused:
            if refused.code != NO_SUCH:
                raise

    # ---- ssh keys
    def ssh_keys(self) -> list[dict]:
        return self.ask("GET", "/ssh-keys")

    def add_ssh_key(self, name: str, public_key: str) -> None:
        """Make sure the account has this public key under this name."""
        mine = public_key.split()[:2]
        for key in self.ssh_keys():
            if key.get("name") == name:
                if key.get("public_key", "").split()[:2] != mine:
                    raise Refused("ssh-key-differs", f"Lambda has another key under the name {name}: delete it there, or name this one otherwise")
                return
        self.ask("POST", "/ssh-keys", {"name": name, "public_key": public_key.strip()})
