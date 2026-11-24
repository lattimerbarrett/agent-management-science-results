"""A Slack channel for a group of agents: messages, threads and tags (@name), with unread counts.

One SlackHub (SQLite) is shared by the group; each agent gets its own Slack view, the ToolSet you give that agent.
The harness binds the agent's name to its view, so an agent posts only as itself. Delivery is immediate (no logical
clock, unlike comms.py): the agents run on their own, not in steps. A person can post too (`hub.post(HUMAN, ...)`).

There is one channel (CHANNEL). A message is either in the channel (thread NULL) or a reply in the thread of a channel
message. An agent "is in" a thread it started, replied in, or was tagged in. `@name` tags that agent and `@channel` tags
everyone; a tag is a row in `tags`. Like comms.py, every message an agent is shown is recorded in `seen`.

Usage:
    hub = SlackHub(["agent_1", "agent_2"], db_path="slack.db", on_post=callback)
    box = Toolbox(Scratchpad(...), hub.agent("agent_1"))
    notice = hub.agent("agent_1").unread_notice()   # "" when nothing is unread
    hub.agent("agent_1").wakes(after_id)            # tags and replies in its threads since after_id

Tables:
    messages(id, sender, thread, body, created)     # thread: id of the channel message it replies to, or NULL
    tags(message_id, agent)
    seen(agent, message_id, created)
"""

import difflib
import json
import re
import sqlite3
import threading
import time

from toolkit import ToolSet

CHANNEL = "#proof"
HUMAN = "lead"  # the person's name on the channel
EVERYONE = "channel"  # @channel tags everyone
SCHEMA = """
CREATE TABLE IF NOT EXISTS messages (
    id      INTEGER PRIMARY KEY,
    sender  TEXT NOT NULL,
    thread  INTEGER REFERENCES messages(id),
    body    TEXT NOT NULL,
    created REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS tags (
    message_id INTEGER NOT NULL REFERENCES messages(id),
    agent      TEXT NOT NULL,
    PRIMARY KEY (message_id, agent)
);
CREATE TABLE IF NOT EXISTS seen (
    agent      TEXT NOT NULL,
    message_id INTEGER NOT NULL REFERENCES messages(id),
    created    REAL NOT NULL,
    PRIMARY KEY (agent, message_id)
);
CREATE INDEX IF NOT EXISTS messages_thread ON messages (thread);
"""
NAME_RE = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")
TAG_RE = re.compile(r"(?<![\w@])@([A-Za-z0-9_.-]+)")
UNSEEN = "NOT EXISTS (SELECT 1 FROM seen s WHERE s.agent = :me AND s.message_id = m.id)"
# the threads :me is in: started, replied in, or tagged in
MY_THREADS = ("SELECT id FROM messages WHERE thread IS NULL AND sender = :me "
              "UNION SELECT thread FROM messages WHERE thread IS NOT NULL AND sender = :me "
              "UNION SELECT COALESCE(x.thread, x.id) FROM messages x JOIN tags t ON t.message_id = x.id "
              "WHERE t.agent = :me")  # fmt: skip
TAGGED = "EXISTS (SELECT 1 FROM tags t WHERE t.message_id = m.id AND t.agent = :me)"
IN_MY_THREAD = f"(m.thread IS NOT NULL AND m.thread IN ({MY_THREADS}))"


class SlackHub:
    """The channel of one group of agents. Safe to use from several threads."""

    def __init__(self, agents, db_path=":memory:", max_chars=6000, on_post=None):
        self.agents = list(agents)
        reserved = {"you", HUMAN, EVERYONE}
        bad = [a for a in self.agents if not isinstance(a, str) or not NAME_RE.match(a) or a.lower() in reserved]
        if bad:
            raise ValueError(f"Invalid agent names {bad}: letters, digits, _ . - only, and none of {sorted(reserved)}")
        if len({a.lower() for a in self.agents}) != len(self.agents):
            raise ValueError("Agent names must be unique (case-insensitively)")
        self.max_chars = max_chars
        self.on_post = on_post  # called with each new message (as `row`), outside the lock
        self.lock = threading.RLock()
        self.db = sqlite3.connect(db_path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)
        self._views = {}

    def agent(self, name):
        if name not in self.agents:
            raise KeyError(f"Unknown agent {name!r}")
        if name not in self._views:
            self._views[name] = Slack(self, name)
        return self._views[name]

    def tags_in(self, body, sender):
        """The agents `body` tags (@name, case-insensitively; @channel: all of them), the sender left out, and the
        @names that match no one."""
        tagged, unknown = [], []
        for raw in TAG_RE.findall(body):
            raw = raw.rstrip(".")
            if raw.lower() == EVERYONE:
                tagged += self.agents
                continue
            match = [a for a in self.agents if a.lower() == raw.lower()]
            if match:
                tagged += match
            elif raw.lower() not in ("you", HUMAN):
                unknown.append(raw)
        return [a for a in dict.fromkeys(tagged) if a != sender], unknown

    def post(self, sender, body, thread=None):
        """Write a message as `sender` (an agent or HUMAN). Returns (row, tagged, unknown tags) or raises ValueError."""
        if not isinstance(body, str) or not body.strip():
            raise ValueError("the message is empty")
        if len(body) > self.max_chars:
            raise ValueError(f"the message is {len(body)} characters; the limit is {self.max_chars}")
        with self.lock, self.db:
            root = None
            if thread is not None:
                parent = self.db.execute("SELECT * FROM messages WHERE id = ?", (thread,)).fetchone()
                if parent is None:
                    raise ValueError(f"there is no message #{thread}")
                root = parent["thread"] or parent["id"]  # a reply to a reply joins the same thread
            tagged, unknown = self.tags_in(body, sender)
            mid = self.db.execute("INSERT INTO messages (sender, thread, body, created) VALUES (?, ?, ?, ?)",
                                  (sender, root, body, time.time())).lastrowid  # fmt: skip
            self.db.executemany("INSERT INTO tags (message_id, agent) VALUES (?, ?)", [(mid, a) for a in tagged])
            if sender in self.agents:
                self.agent(sender)._mark_seen([mid])
            row = self.row(mid)
        if self.on_post:
            self.on_post(row)
        return row, tagged, unknown

    def row(self, mid):
        """A message as a dict: id, sender, thread, body, created, tags."""
        with self.lock:
            r = self.db.execute("SELECT * FROM messages WHERE id = ?", (mid,)).fetchone()
            tags = [t[0] for t in self.db.execute("SELECT agent FROM tags WHERE message_id = ?", (mid,))]
        return {**dict(r), "tags": tags}

    def dump(self):
        """Every message, oldest first, as rows (`row`)."""
        with self.lock:
            ids = [r[0] for r in self.db.execute("SELECT id FROM messages ORDER BY id")]
        return [self.row(i) for i in ids]

    def export(self, path):
        path.write_text("".join(json.dumps(r) + "\n" for r in self.dump()))

    def close(self):
        with self.lock:
            self.db.close()


class Slack(ToolSet):
    TOOLS_FILE = "tools_slack.yaml"

    def __init__(self, hub, name):
        self.hub, self.name = hub, name

    # ---- for the harness ----------------------------------------------------

    def unread(self):
        """(unread, tagged {sender: n}, replies in my threads): what's waiting for this agent, without marking it."""
        q = f"SELECT m.*, {TAGGED} AS tagged, {IN_MY_THREAD} AS mine FROM messages m WHERE {UNSEEN}"
        with self.hub.lock:
            rows = self.hub.db.execute(q, {"me": self.name}).fetchall()
        tagged = {}
        for r in rows:
            if r["tagged"]:
                tagged[r["sender"]] = tagged.get(r["sender"], 0) + 1
        return len(rows), tagged, sum(1 for r in rows if r["mine"] and not r["tagged"])

    def unread_notice(self):
        """'Slack: 3 unread messages in #proof (agent_2 tagged you in 1; 1 is a reply in a thread you're in). Read them
        with slack_read.', or ''."""
        n, tagged, mine = self.unread()
        if not n:
            return ""
        parts = [f"{', '.join(tagged)} tagged you in {sum(tagged.values())}"] if tagged else []
        if mine:
            parts.append(f"{mine} {'is a reply' if mine == 1 else 'are replies'} in a thread you're in")
        detail = f" ({'; '.join(parts)})" if parts else ""
        return f"Slack: {n} unread message{'s' * (n != 1)} in {CHANNEL}{detail}. Read {'them' if n != 1 else 'it'} with slack_read."

    def wakes(self, after):
        """The unread messages after id `after` that would wake this agent: ones that tag it, and replies in threads
        it is in, as (id, sender, tagged)."""
        q = (f"SELECT m.id, m.sender, {TAGGED} AS tagged FROM messages m WHERE m.id > :after AND m.sender != :me "
             f"AND {UNSEEN} AND ({TAGGED} OR {IN_MY_THREAD}) ORDER BY m.id")  # fmt: skip
        with self.hub.lock:
            return [tuple(r) for r in self.hub.db.execute(q, {"me": self.name, "after": after})]

    def last_id(self):
        with self.hub.lock:
            return self.hub.db.execute("SELECT COALESCE(MAX(id), 0) FROM messages").fetchone()[0]

    # ---- helpers --------------------------------------------------------------

    def _mark_seen(self, ids):
        now = time.time()
        self.hub.db.executemany("INSERT OR IGNORE INTO seen (agent, message_id, created) VALUES (?, ?, ?)",
                                [(self.name, i, now) for i in ids])  # fmt: skip

    def _who(self, name):
        return "you" if name == self.name else name

    def _fmt(self, r, replies=None):
        where = f" (reply in thread #{r['thread']})" if r["thread"] is not None else ""
        tags = [t[0] for t in self.hub.db.execute("SELECT agent FROM tags WHERE message_id = ?", (r["id"],))]
        tag = " [tags you]" if self.name in tags else ""
        count = f"\n({replies} repl{'ies' if replies != 1 else 'y'}: slack_read with thread={r['id']} to see them)" \
            if replies else ""  # fmt: skip
        return f"#{r['id']} {self._who(r['sender'])}{where}{tag}:\n{r['body']}{count}"

    @staticmethod
    def _id(x):
        """12, '12' or '#12' as an int, else None."""
        if isinstance(x, bool):
            return None
        if isinstance(x, int):
            return x
        s = str(x).strip().lstrip("#")
        return int(s) if s.isdigit() else None

    # ---- tools (names match tools_slack.yaml) -----------------------------------

    def slack_post(self, text, thread=None):
        tid = None
        if thread is not None:
            tid = self._id(thread)
            if tid is None:
                return f"Rejected: thread must be a message id (such as 12), not {thread!r}.", True
        try:
            row, tagged, unknown = self.hub.post(self.name, text, tid)
        except ValueError as e:
            return f"Rejected: {e}.", True
        where = f" in thread #{row['thread']}" if row["thread"] is not None else f" in {CHANNEL}"
        out = f"Posted #{row['id']}{where}."
        if tagged:
            out += f" Tagged {', '.join(tagged)}."
        if unknown:
            close = difflib.get_close_matches(unknown[0], self.hub.agents, n=2, cutoff=0.5)
            hint = f" (did you mean {', '.join('@' + c for c in close)}?)" if close else ""
            out += f" No agent is named {', '.join('@' + u for u in unknown)}{hint}; the team is {', '.join(self.hub.agents)}."
        return out, False

    def slack_read(self, thread=None, include_read=False, limit=20):
        limit = max(1, min(int(limit), 100))
        db, me = self.hub.db, {"me": self.name}
        with self.hub.lock, db:
            if thread is not None:
                tid = self._id(thread)
                r = db.execute("SELECT * FROM messages WHERE id = ?", (tid,)).fetchone() if tid is not None else None
                if r is None:
                    return f"Rejected: there is no message #{thread}.", True
                root = r["thread"] or r["id"]
                rows = db.execute("SELECT * FROM messages WHERE id = ? OR thread = ? ORDER BY id", (root, root)).fetchall()
                note = ""
                if len(rows) > limit:  # the first message and the latest replies
                    note = f"\n\n({len(rows) - limit} earlier replies not shown.)"
                    rows = rows[:1] + rows[len(rows) - (limit - 1):] if limit > 1 else rows[:1]
                self._mark_seen([x["id"] for x in rows])
                return f"Thread #{root} in {CHANNEL}:\n\n" + "\n\n".join(self._fmt(x) for x in rows) + note, False

            if include_read:
                rows = db.execute("SELECT * FROM (SELECT * FROM messages WHERE thread IS NULL ORDER BY id DESC LIMIT ?) "
                                  "ORDER BY id", (limit,)).fetchall()  # fmt: skip
                if not rows:
                    return f"({CHANNEL} is empty)", False
                counts = dict(db.execute("SELECT thread, COUNT(*) FROM messages WHERE thread IS NOT NULL GROUP BY thread"))
                self._mark_seen([x["id"] for x in rows])
                return f"Latest in {CHANNEL}:\n\n" + "\n\n".join(self._fmt(x, counts.get(x["id"])) for x in rows), False

            rows = db.execute(f"SELECT * FROM messages m WHERE {UNSEEN} ORDER BY id", me).fetchall()
            if not rows:
                return "(no unread messages)", False
            shown, remaining = rows[:limit], len(rows) - limit
            self._mark_seen([x["id"] for x in shown])
            text = "\n\n".join(self._fmt(x) for x in shown)
            if remaining > 0:
                text += f"\n\n({remaining} more unread; call slack_read again to see them.)"
            return text, False
