"""Outbound rate limiting for Telegram-shaped bot clients (Bale, Telegram).

The limiter sits in front of the HTTP call and delays a request until the
platform would accept it, so bots stop hitting ``429 Too Many Requests``
instead of reacting to it afterwards.

Design (all single-process, pure ``asyncio``, stdlib only):

* One sliding window per chat (``Rule``: *max_calls* per *period*) plus an
  optional bot-wide window. A request is granted only when every window that
  applies to it has room.
* Hot path is O(1): when there is room, ``acquire`` takes a slot and returns
  without creating a future, a task or a timer.
* When there is no room the request parks in a per-chat FIFO queue (one
  ``Future`` per waiter, no tasks). Each chat has at most one timer. Chats
  blocked by the bot-wide window share a single timer instead of waking
  individually, so thousands of waiting chats cost O(released) per refill.
* ``penalize`` pauses a chat (or the whole bot) when the server still answers
  429, using the server's ``retry_after``.
* Memory is bounded by ``max_pending`` / ``max_pending_per_chat``; idle chat
  state is garbage-collected.

Public names: :class:`Rule`, :class:`RateLimitConfig`, :class:`RateLimiter`,
:class:`RateLimitQueueFull`, :class:`RateLimitWaitTimeout`.
"""
from __future__ import annotations

import asyncio
from collections import deque
from dataclasses import dataclass, field
from typing import (
    Callable,
    Deque,
    Dict,
    FrozenSet,
    Hashable,
    Mapping,
    Optional,
    Union,
)

from .transport.errors import TransportError

ChatId = Union[int, str]

__all__ = [
    "Rule",
    "RateLimitConfig",
    "RateLimiter",
    "RateLimitError",
    "RateLimitQueueFull",
    "RateLimitWaitTimeout",
    "DEFAULT_SEND_METHODS",
    "resolve_rate_limiter",
]

#: API methods that count against per-chat send limits.
DEFAULT_SEND_METHODS: FrozenSet[str] = frozenset(
    {
        "sendMessage",
        "sendPhoto",
        "sendDocument",
        "sendVideo",
        "sendAudio",
        "sendVoice",
        "sendAnimation",
        "sendVideoNote",
        "sendSticker",
        "sendLocation",
        "sendVenue",
        "sendContact",
        "sendPoll",
        "sendDice",
        "sendInvoice",
        "sendMediaGroup",
        "sendPaidMedia",
        "sendGame",
        "forwardMessage",
        "forwardMessages",
        "copyMessage",
        "copyMessages",
    }
)

# Slack added to every wake-up so a timer firing a hair early never loops.
_EPSILON = 0.001


class RateLimitError(TransportError):
    """Base class for errors raised by the local rate limiter."""


class RateLimitQueueFull(RateLimitError):
    """Too many requests are already waiting (``max_pending`` reached)."""


class RateLimitWaitTimeout(RateLimitError):
    """A request waited longer than ``max_wait`` for a free slot."""


@dataclass(frozen=True)
class Rule:
    """``max_calls`` requests per ``period`` seconds.

    ``padding`` widens the window a little. The server starts counting when a
    request *arrives*, we count when it is *sent*; padding absorbs that
    network jitter so the server never sees a burst we did not intend.
    """

    max_calls: int
    period: float
    padding: float = 0.0

    def __post_init__(self) -> None:
        if self.max_calls < 1:
            raise ValueError("Rule.max_calls must be >= 1")
        if self.period <= 0:
            raise ValueError("Rule.period must be > 0")
        if self.padding < 0:
            raise ValueError("Rule.padding must be >= 0")


def _default_is_private(chat_id: ChatId) -> bool:
    return isinstance(chat_id, int) and chat_id > 0


def _never_private(chat_id: ChatId) -> bool:
    return False


@dataclass(frozen=True)
class RateLimitConfig:
    """Tunable behaviour of a :class:`RateLimiter`.

    Attributes:
        enabled: Master switch. Can also be flipped at runtime via
            ``RateLimiter.enabled``.
        group: Per-chat rule for groups/channels (and for every chat when
            ``is_private`` says no). ``None`` = unlimited.
        private: Per-chat rule for private chats. ``None`` = unlimited.
        global_: Bot-wide rule across all chats. ``None`` = unlimited.
        methods: API methods that consume slots; everything else passes
            through untouched.
        weights: Slots consumed per method (default 1), e.g. for media
            groups.
        is_private: Decides which per-chat rule applies to a chat id.
        max_wait: Longest a request may wait for a slot, in seconds. On
            expiry ``RateLimitWaitTimeout`` is raised. ``None`` = forever.
        max_pending: Cap on queued requests across all chats; beyond it
            ``RateLimitQueueFull`` is raised immediately (back-pressure).
        max_pending_per_chat: Same cap for a single chat.
        retry_on_429: When the server still answers 429 (JSON envelope or
            HTTP), retry through the client's retry policy after pausing.
        default_penalty: Pause applied on a 429 that carries no
            ``retry_after``.
    """

    enabled: bool = True
    group: Optional[Rule] = Rule(20, 60.0, 0.75)
    private: Optional[Rule] = None
    global_: Optional[Rule] = None
    methods: FrozenSet[str] = DEFAULT_SEND_METHODS
    weights: Mapping[str, int] = field(default_factory=dict)
    is_private: Callable[[ChatId], bool] = _default_is_private
    max_wait: Optional[float] = 300.0
    max_pending: int = 100_000
    max_pending_per_chat: int = 20_000
    retry_on_429: bool = True
    default_penalty: float = 3.0

    @classmethod
    def bale(cls, **overrides: object) -> "RateLimitConfig":
        """Bale: 20 messages/minute per group or channel per bot.

        The rule is applied to *every* chat (Bale's chat-id conventions for
        groups are not relied on); pass ``is_private=...`` and ``private=...``
        to exempt private chats.
        """
        base: Dict[str, object] = {
            "group": Rule(20, 60.0, 0.75),
            "private": None,
            "is_private": _never_private,
        }
        base.update(overrides)
        return cls(**base)  # type: ignore[arg-type]

    @classmethod
    def telegram(cls, **overrides: object) -> "RateLimitConfig":
        """Telegram: ~20/min per group, ~1/s per private chat (burst 3), ~30/s overall."""
        base: Dict[str, object] = {
            "group": Rule(20, 60.0, 0.75),
            "private": Rule(3, 3.0, 0.05),  # ~1/s sustained, bursts of 3 allowed
            "global_": Rule(30, 1.0, 0.05),
        }
        base.update(overrides)
        return cls(**base)  # type: ignore[arg-type]

    @classmethod
    def disabled(cls) -> "RateLimitConfig":
        """A config whose limiter lets everything through."""
        return cls(enabled=False)


class _Window:
    """Sliding window over monotonic timestamps."""

    __slots__ = ("max_calls", "span", "hits")

    def __init__(self, rule: Rule) -> None:
        self.max_calls = rule.max_calls
        self.span = rule.period + rule.padding
        self.hits: Deque[float] = deque()

    def wait_time(self, now: float, weight: int) -> float:
        if weight > self.max_calls:
            weight = self.max_calls
        hits = self.hits
        cutoff = now - self.span
        while hits and hits[0] <= cutoff:
            hits.popleft()
        over = len(hits) + weight - self.max_calls
        if over <= 0:
            return 0.0
        return hits[over - 1] + self.span - now

    def take(self, now: float, weight: int) -> None:
        if weight > self.max_calls:
            weight = self.max_calls
        if weight == 1:
            self.hits.append(now)
        else:
            self.hits.extend([now] * weight)

    def idle(self, now: float) -> bool:
        hits = self.hits
        cutoff = now - self.span
        while hits and hits[0] <= cutoff:
            hits.popleft()
        return not hits


class _Waiter:
    __slots__ = ("fut", "weight", "deadline", "counted")

    def __init__(self, fut: "asyncio.Future[None]", weight: int, deadline: Optional[float]) -> None:
        self.fut = fut
        self.weight = weight
        self.deadline = deadline
        # True while this waiter is included in ``RateLimiter._pending``.
        self.counted = True


class _Lane:
    """Per-chat state: its window, FIFO of waiters and at most one timer."""

    __slots__ = ("key", "window", "queue", "timer", "timer_at", "blocked_until", "parked")

    def __init__(self, key: Hashable, window: Optional[_Window]) -> None:
        self.key = key
        self.window = window
        self.queue: Deque[_Waiter] = deque()
        self.timer: Optional[asyncio.TimerHandle] = None
        self.timer_at = 0.0
        self.blocked_until = 0.0
        self.parked = False


def _normalize_chat(chat_id: ChatId) -> ChatId:
    """``"123"`` and ``123`` are the same chat; ``"@name"`` stays a string."""
    if isinstance(chat_id, str):
        s = chat_id.strip()
        body = s[1:] if s[:1] == "-" else s
        if body.isdigit():
            return int(s)
        return s
    return chat_id


class RateLimiter:
    """Asynchronous, per-event-loop rate limiter. See module docstring."""

    def __init__(self, config: Optional[RateLimitConfig] = None) -> None:
        self.config = config or RateLimitConfig()
        self.enabled: bool = self.config.enabled
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._lanes: Dict[Hashable, _Lane] = {}
        self._global: Optional[_Window] = (
            _Window(self.config.global_) if self.config.global_ else None
        )
        self._global_blocked_until = 0.0
        self._parked: Deque[_Lane] = deque()
        self._global_timer: Optional[asyncio.TimerHandle] = None
        self._global_timer_at = 0.0
        self._pending = 0
        self._next_gc = 0.0
        self._stats = {
            "immediate": 0,
            "delayed": 0,
            "rejected": 0,
            "timeouts": 0,
            "penalties": 0,
        }

    # ------------------------------------------------------------------ API

    @property
    def retry_on_429(self) -> bool:
        """Whether the client should retry server-side 429s (see config)."""
        return self.config.retry_on_429

    @property
    def pending(self) -> int:
        """Requests currently waiting for a slot."""
        return self._pending

    def stats(self) -> Dict[str, int]:
        """Counters plus current ``pending`` and ``chats`` (tracked chats)."""
        out = dict(self._stats)
        out["pending"] = self._pending
        out["chats"] = len(self._lanes)
        return out

    async def acquire(
        self, method: str, chat_id: Optional[ChatId] = None, *, weight: Optional[int] = None
    ) -> None:
        """Wait until ``method`` may be sent to ``chat_id``.

        Returns immediately when the limiter is disabled, the method does not
        count, or there is room. Cancelling the caller removes it from the
        queue.

        Raises:
            RateLimitQueueFull: the pending-queue cap was hit.
            RateLimitWaitTimeout: no slot became free within ``max_wait``.
        """
        if not self.enabled:
            return
        cfg = self.config
        if method not in cfg.methods:
            return
        loop = asyncio.get_running_loop()
        if loop is not self._loop:
            self._rebind(loop)
        w = weight if weight is not None else cfg.weights.get(method, 1)
        if w < 1:
            w = 1
        now = loop.time()
        if now >= self._next_gc:
            self._gc(now)

        lane = self._lane_for(chat_id)
        if lane is None:
            lane = self._lane_for_global()
        if not lane.queue:
            delay = self._lane_delay(lane, now, w)
            if delay <= 0:
                if lane.window is not None:
                    lane.window.take(now, w)
                if self._global is not None:
                    self._global.take(now, w)
                self._stats["immediate"] += 1
                return

        # Slow path: queue up.
        if self._pending >= cfg.max_pending or len(lane.queue) >= cfg.max_pending_per_chat:
            self._stats["rejected"] += 1
            raise RateLimitQueueFull(
                f"rate limiter queue is full ({self._pending} pending requests)"
            )
        fut: "asyncio.Future[None]" = loop.create_future()
        deadline = now + cfg.max_wait if cfg.max_wait is not None else None
        waiter = _Waiter(fut, w, deadline)
        lane.queue.append(waiter)
        self._pending += 1
        self._stats["delayed"] += 1
        if len(lane.queue) == 1:
            self._schedule(lane, now)
        try:
            await fut
        except asyncio.CancelledError:
            # The pump discards the cancelled future lazily; release the
            # pending count now unless the pump already did.
            if waiter.counted:
                waiter.counted = False
                self._pending -= 1
            raise

    def penalize(self, chat_id: Optional[ChatId], seconds: Optional[float] = None) -> None:
        """Pause ``chat_id`` (or the whole bot when ``None``) for ``seconds``.

        Call this when the server answered 429; ``seconds`` is its
        ``retry_after`` (``config.default_penalty`` when missing).
        """
        if not self.enabled:
            return
        loop = self._loop
        if loop is None:
            return
        if seconds is None or seconds <= 0:
            seconds = self.config.default_penalty
        until = loop.time() + seconds + _EPSILON
        self._stats["penalties"] += 1
        if chat_id is None:
            if until > self._global_blocked_until:
                self._global_blocked_until = until
            return
        key = _normalize_chat(chat_id)
        lane = self._lanes.get(key)
        if lane is None:
            rule = self._rule_for(key)
            lane = _Lane(key, _Window(rule) if rule is not None else None)
            self._lanes[key] = lane
        if until > lane.blocked_until:
            lane.blocked_until = until

    def reset(self) -> None:
        """Forget all state and fail waiting requests with cancellation."""
        self._rebind(self._loop)

    # ------------------------------------------------------------ internals

    def _rebind(self, loop: Optional[asyncio.AbstractEventLoop]) -> None:
        for lane in self._lanes.values():
            if lane.timer is not None:
                lane.timer.cancel()
            for w in lane.queue:
                if not w.fut.done():
                    w.fut.cancel()
        if self._global_timer is not None:
            self._global_timer.cancel()
        self._lanes.clear()
        self._parked.clear()
        self._global_timer = None
        self._pending = 0
        self._global_blocked_until = 0.0
        self._global = _Window(self.config.global_) if self.config.global_ else None
        self._loop = loop
        self._next_gc = 0.0

    def _rule_for(self, chat_id: ChatId) -> Optional[Rule]:
        cfg = self.config
        return cfg.private if cfg.is_private(chat_id) else cfg.group

    def _lane_for(self, chat_id: Optional[ChatId]) -> Optional[_Lane]:
        """Lane for a chat, or ``None`` when no per-chat rule applies."""
        if chat_id is None:
            return None
        key = _normalize_chat(chat_id)
        lane = self._lanes.get(key)
        if lane is not None:
            return lane
        rule = self._rule_for(key)
        if rule is None:
            return None
        lane = _Lane(key, _Window(rule))
        self._lanes[key] = lane
        return lane

    def _lane_for_global(self) -> _Lane:
        lane = self._lanes.get(_GLOBAL_KEY)
        if lane is None:
            lane = _Lane(_GLOBAL_KEY, None)
            self._lanes[_GLOBAL_KEY] = lane
        return lane

    def _global_delay(self, now: float, weight: int) -> float:
        d = self._global_blocked_until - now
        g = self._global
        if g is not None:
            gd = g.wait_time(now, weight)
            if gd > d:
                d = gd
        return d

    def _lane_delay(self, lane: _Lane, now: float, weight: int) -> float:
        d = lane.blocked_until - now
        win = lane.window
        if win is not None:
            cd = win.wait_time(now, weight)
            if cd > d:
                d = cd
        gd = self._global_delay(now, weight)
        return gd if gd > d else d

    def _schedule(self, lane: _Lane, now: float) -> None:
        """Arm whichever timer will next let ``lane``'s head waiter run."""
        head = lane.queue[0]
        w = head.weight
        own = lane.blocked_until - now
        win = lane.window
        if win is not None:
            cd = win.wait_time(now, w)
            if cd > own:
                own = cd
        gd = self._global_delay(now, w)
        if gd > own and gd > 0:
            # Bottleneck is the bot-wide window: park on the shared timer.
            if not lane.parked:
                lane.parked = True
                self._parked.append(lane)
            self._arm_global(now + gd)
            return
        self._arm_lane(lane, now, own)

    def _arm_lane(self, lane: _Lane, now: float, delay: float) -> None:
        head = lane.queue[0]
        if head.deadline is not None:
            remaining = head.deadline - now
            if remaining < delay:
                delay = remaining
        if delay < 0:
            delay = 0.0
        at = now + delay + _EPSILON
        if lane.timer is not None:
            if lane.timer_at <= at:
                return
            lane.timer.cancel()
        assert self._loop is not None
        lane.timer = self._loop.call_at(at, self._pump_timer, lane)
        lane.timer_at = at

    def _arm_global(self, at: float) -> None:
        at += _EPSILON
        if self._global_timer is not None:
            if self._global_timer_at <= at:
                return
            self._global_timer.cancel()
        assert self._loop is not None
        self._global_timer = self._loop.call_at(at, self._pump_global)
        self._global_timer_at = at

    def _pump_timer(self, lane: _Lane) -> None:
        lane.timer = None
        self._pump(lane, front=False)

    def _pump_global(self) -> None:
        self._global_timer = None
        parked = self._parked
        loop = self._loop
        assert loop is not None
        while parked:
            lane = parked.popleft()
            lane.parked = False
            self._pump(lane, front=True)
            if self._global_delay(loop.time(), 1) > 0:
                break
        if parked and self._global_timer is None:
            now = loop.time()
            self._arm_global(now + max(self._global_delay(now, 1), 0.0))

    def _pump(self, lane: _Lane, *, front: bool) -> None:
        """Serve as many waiters of ``lane`` as the windows allow."""
        loop = self._loop
        assert loop is not None
        now = loop.time()
        q = lane.queue
        glob = self._global
        while q:
            w = q[0]
            fut = w.fut
            if fut.done():
                q.popleft()
                if w.counted:
                    w.counted = False
                    self._pending -= 1
                continue
            delay = self._lane_delay(lane, now, w.weight)
            if delay > 0:
                if w.deadline is not None and now >= w.deadline:
                    q.popleft()
                    w.counted = False
                    self._pending -= 1
                    self._stats["timeouts"] += 1
                    fut.set_exception(
                        RateLimitWaitTimeout(
                            f"waited more than {self.config.max_wait:g}s for a rate-limit slot"
                        )
                    )
                    continue
                self._requeue(lane, now, front)
                return
            if lane.window is not None:
                lane.window.take(now, w.weight)
            if glob is not None:
                glob.take(now, w.weight)
            q.popleft()
            w.counted = False
            self._pending -= 1
            fut.set_result(None)

    def _requeue(self, lane: _Lane, now: float, front: bool) -> None:
        w = lane.queue[0]
        own = lane.blocked_until - now
        win = lane.window
        if win is not None:
            cd = win.wait_time(now, w.weight)
            if cd > own:
                own = cd
        gd = self._global_delay(now, w.weight)
        if gd > own and gd > 0:
            if not lane.parked:
                lane.parked = True
                if front:
                    self._parked.appendleft(lane)
                else:
                    self._parked.append(lane)
            self._arm_global(now + gd)
            return
        self._arm_lane(lane, now, own)

    def _gc(self, now: float) -> None:
        """Drop chats that have been quiet for a full window."""
        self._next_gc = now + 30.0
        dead = [
            key
            for key, lane in self._lanes.items()
            if not lane.queue
            and lane.timer is None
            and not lane.parked
            and lane.blocked_until <= now
            and (lane.window is None or lane.window.idle(now))
        ]
        for key in dead:
            del self._lanes[key]


_GLOBAL_KEY: Hashable = ("__global__",)


def resolve_rate_limiter(
    value: object,
    preset: Optional[Callable[[], RateLimitConfig]] = None,
) -> Optional[RateLimiter]:
    """Turn a user-facing ``rate_limit=`` argument into a limiter (or None).

    * ``RateLimiter`` -> used as is (share one across clients on purpose)
    * ``RateLimitConfig`` -> wrapped in a new limiter
    * ``True`` -> new limiter from the platform ``preset``
    * ``False`` / ``None`` -> no limiter
    """
    if isinstance(value, RateLimiter):
        return value
    if isinstance(value, RateLimitConfig):
        return RateLimiter(value)
    if value is True:
        return RateLimiter(preset() if preset is not None else RateLimitConfig())
    return None
