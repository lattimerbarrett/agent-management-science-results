"""Playing a run so that a GPU's server always has as many conversations as it holds.

cli.py plays a run a group of problems at a time, one arm after another, and waits for a group's last agent
before anything else begins. On the Mac that is what its memory holds. On a GPU it leaves the server with a
handful of conversations for much of the time, because a group lasts as long as its slowest agent however
little is left to write: the first run on an H100 averaged 1,300 tokens a second over its groups, where the
server wrote 3,000 with all its room taken.

Here a run is cut into pieces, a piece being one problem under one arm, and a piece is begun as soon as the
server has room for its agents. Nothing an agent is shown changes:

  - A piece is played as `swarm.play` plays a group of one problem (`play_open`: its lines but for the last):
    all its agents are open from the start, and what one is shown of another goes by the step count.
  - A problem's arms are played in the order the run names them, each after the one before it has ended for
    that problem. So an arm recalls the replies its agents share with an earlier one, as it does when arms are
    played one after another, and an agent is the same agent in every arm until it is first shown something
    the others are not.
  - No more files of agents' Python run at once than under one group (`AFewAtATime`), so that a file's
    thirty seconds are not spent waiting for a processor.

What changes is which problems are being played at the same moment, and agents of two problems never see each
other. `pack` is the order pieces begin in and nothing else; `tests/test_packing.py` plays a run both ways
with scripted agents and finds every agent of every problem the same.
"""
from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

LONGEST = 0.42      # of the most an agent may write in all its turns, what its conversation comes to at its longest,
                    # prompts and replies together. Measured on the Mac's runs of the fifteen problems: 11,900 tokens
                    # alone (this gives 12,900), 15,300 with a look one time in four (16,100), 23,000 with a look
                    # after every step (25,800); nine conversations in ten stay under 1.7 times their mean
HELD = 0.65         # of the sum of what its conversations come to at their longest, what a server holds of the pieces
                    # open at a time: agents stop at different steps, and the ones that began last are still short
FULL = 0.55         # of a server's room, what the open conversations may be counted at. Past it the server no longer
                    # has what it kept of a conversation when that conversation's next call comes, and reads it again
                    # whole. Measured on an H100 with the 9B and twenty agents a problem (2026-10-12, the first packed
                    # run, which opened 184): of the prompt tokens of the pieces begun with 180 agents at work, 70 to
                    # 94% were read again; with 100 to 160 at work, 40 to 60%; with 90 or fewer, 11 to 21%, as much as
                    # in a run played in groups. 90 agents with a look one time in four are counted at 53% of that room
PIECES = 32         # pieces played at once at most: each has a thread and a line to the server of its own


def longest(arm) -> float:
    """What a conversation under `arm` comes to at its longest, in tokens, as the runs so far have had it."""
    each = (8000 if arm.thinking is None else arm.thinking) + arm.max_tokens         # a thought and a reply
    return LONGEST * arm.steps * (1 + (arm.looks.p if arm.looks is not None else 0)) * each


@dataclass(eq=False)
class Piece:
    """One problem under one arm: what `swarm.play` plays as a group of one."""
    arm: object
    problem: object

    @property
    def agents(self) -> int:
        return self.arm.agents

    @property
    def of(self) -> tuple:
        """The problem it is a piece of."""
        return (self.problem.benchmark, self.problem.id)

    def __str__(self) -> str:
        return f"{self.arm.name}: {self.problem.key}"


@dataclass
class Room:
    """What of a server the pieces being played take: every open conversation is counted at what its arm's
    conversations come to (`longest`, of which a server holds `HELD` at a time).

    `tokens` is what the open conversations may be counted at in all (`FULL` of the conversation a server holds:
    `swarm_engine.vllm_server.room`), `side` how many conversations the server writes at a time, `most` the most
    conversations open at once (left out: `side`, since one more than the server writes only waits in line, and
    what the server kept of a conversation that waits is the first thing it lets go of). None of them given:
    everything fits, which is every piece at once."""
    tokens: float | None = None
    side: int | None = None
    most: int | None = None
    open: int = 0                       # conversations open now
    held: float = 0.0                   # tokens of the server they are counted at
    widest: int = 0                     # the most that were open at once
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def __post_init__(self):
        if self.most is None and self.side:
            self.most = self.side

    @staticmethod
    def holds(arm) -> float:
        return HELD * longest(arm)

    def fits(self, piece: Piece) -> bool:
        with self.lock:
            if self.most is not None and self.open + piece.agents > self.most:
                return False
            return self.tokens is None or self.held + piece.agents * self.holds(piece.arm) <= self.tokens

    def take(self, piece: Piece):
        with self.lock:
            self.open += piece.agents
            self.held += piece.agents * self.holds(piece.arm)
            self.widest = max(self.widest, self.open)

    def give(self, arm, agents: int = 1):
        """`agents` conversations under `arm` have ended."""
        with self.lock:
            self.open -= agents
            self.held -= agents * self.holds(arm)


def play_open(piece: Piece, backend, python=None, seed: int = 0, progress=None, desks: int | None = None):
    """Play one piece as `swarm.play` plays a group of one problem, and hand its episode back before it is
    closed. Closing marks every answer, and the marker (Math-Verify) keeps time with a signal, which only a
    process's main thread may set: a piece is played on a thread of its own, so whoever `pack` hands it to
    (`ended`, on the thread that called `pack`) closes it there. These are `play`'s own lines but for that
    last one, and a test holds the two to the same steps. `desks` is `play`'s: how many agents work at once
    where nobody reads anybody; with looks every agent is open from the start."""
    from .swarm import Workshop, carry_on
    episode = Workshop(piece.problem, piece.arm, seed, python)

    def then(seat: int, reply):
        went_on = episode.step(seat, reply)
        if progress:
            progress(episode, seat, went_on is None)
        return went_on

    carry_on(backend, [episode.call(seat) for seat in range(piece.agents)], then, None if piece.arm.looks is not None else desks)
    return episode


def pack(pieces: list[Piece], play, room: Room | None = None, begun=None, ended=None, at_once: int = PIECES) -> int:
    """Play every piece, and begin each as soon as the pieces before it in the list that are of its problem have
    ended and `room` has room for its agents, `at_once` pieces at a time at most. A piece is always begun when
    nothing else is being played, however large it is: a problem's agents are open together or not at all.

    `play(piece, stopped)` plays one, on a thread of its own, and calls `stopped(who)` as each of its agents
    stops, from whichever thread: the room that agent took is free from then (`who` names the agent, so that
    one told of twice is counted once). `begun(piece)` and `ended(piece, what play returned)` are called on
    this thread, one at a time, so that what a piece made can be written down here without a lock.

    If a piece fails, or `begun` or `ended` does, or this thread is interrupted, no further piece is begun.
    The pieces being played are played out and each is handed to `ended`, so that what they made is written
    down, and then the first failure is raised. (A second interruption is raised at once.) Returns how many
    pieces were played to their end."""
    room = room or Room()
    over: set[int] = set()                                       # the pieces that have ended, by where they stand in the list
    before = [[k for k in range(i) if pieces[k].of == piece.of] for i, piece in enumerate(pieces)]
    waiting, flying, failed = list(range(len(pieces))), {}, []
    woken, broken = threading.Event(), threading.Event()

    def one(i: int):
        piece, counted = pieces[i], threading.Lock()
        left, told = [piece.agents], set()                       # its agents that have not stopped: their room is still taken

        def stopped(who=None):
            with counted:
                if who is not None and who in told:
                    return
                told.add(who)
                given, left[0] = min(left[0], 1), max(left[0] - 1, 0)
            if given:
                room.give(piece.arm, given)
            woken.set()
        try:
            return play(piece, stopped)
        except BaseException:
            broken.set()                                         # before its room is given back: nothing begins on room a failure freed
            raise
        finally:
            with counted:
                rest, left[0] = left[0], 0
            if rest:                                             # a piece that failed, or one whose agents were not all told of
                room.give(piece.arm, rest)
            woken.set()

    def careful(call, *args) -> bool:
        """`begun` or `ended`, called; what it raises is a failure of the run, which is then played to its end."""
        try:
            call(*args)
            return True
        except BaseException as error:
            failed.append(error)
            broken.set()
            return False

    interrupted = 0
    with ThreadPoolExecutor(max_workers=max(1, at_once), thread_name_prefix="piece") as pool:
        while waiting or flying:
            try:
                woken.clear()
                for future in [future for future in flying if future.done()]:
                    i = flying.pop(future)
                    try:
                        made = future.result()
                    except BaseException as error:               # KeyboardInterrupt in a piece is a failure of the run too
                        failed.append(error)
                        continue
                    over.add(i)
                    if ended:                                    # before anything else is begun: a piece that cannot be written
                        careful(ended, pieces[i], made)          # down is a failure, and nothing begins on the room it left
                if not failed:
                    for i in list(waiting):
                        if len(flying) >= max(1, at_once):
                            break
                        if any(k not in over for k in before[i]) or (flying and not room.fits(pieces[i])):
                            continue
                        if broken.is_set():                      # asked after the room: a piece that failed says so before it
                            break                                # gives its room back, so room a failure freed is never taken
                        room.take(pieces[i])
                        waiting.remove(i)
                        if begun and not careful(begun, pieces[i]):
                            room.give(pieces[i].arm, pieces[i].agents)      # it was not begun after all
                            break
                        flying[pool.submit(one, i)] = i
                if not flying:                                   # nothing is being played and nothing may begin: all played, or a failure
                    break
                if not any(future.done() for future in flying):
                    woken.wait(timeout=1.0)
            except BaseException as error:                       # this thread was interrupted: as a failure, once
                interrupted += 1
                failed.append(error)
                broken.set()
                if interrupted > 1:
                    raise
    if failed:
        raise failed[0]
    return len(over)


class AFewAtATime:
    """A sandbox for agents' Python that runs `at_once` files at a time at most, whichever piece asks. Under a
    group there are never more: a file is run by the thread that takes its agent's reply, and a group has
    `llm.WORKERS` of those. Every piece has as many of its own, and a file's thirty seconds are on the clock."""

    def __init__(self, python, at_once: int):
        self.python, self.gate = python, threading.BoundedSemaphore(max(1, at_once))

    def check_many(self, codes: list[str]) -> list:
        with self.gate:
            return self.python.check_many(codes)

    def __getattr__(self, name: str):
        return getattr(self.python, name)
