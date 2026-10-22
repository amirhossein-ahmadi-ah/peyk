"""Tests for peyk.ratelimit (stdlib-only, real clock with tiny windows)."""
from __future__ import annotations

import asyncio
import time

import pytest

from peyk.ratelimit import (
    RateLimitConfig,
    RateLimiter,
    RateLimitQueueFull,
    RateLimitWaitTimeout,
    Rule,
    resolve_rate_limiter,
)


def _cfg(**kw):
    base = dict(group=Rule(3, 0.2), private=None, global_=None, is_private=lambda _c: False)
    base.update(kw)
    return RateLimitConfig(**base)


async def _timed(limiter, method, chat):
    await limiter.acquire(method, chat)
    return time.monotonic()


async def test_under_limit_is_immediate():
    lim = RateLimiter(_cfg())
    t0 = time.monotonic()
    for _ in range(3):
        await lim.acquire("sendMessage", -100)
    assert time.monotonic() - t0 < 0.05
    assert lim.stats()["immediate"] == 3 and lim.pending == 0


async def test_over_limit_waits_for_window():
    lim = RateLimiter(_cfg())
    t0 = time.monotonic()
    times = [await _timed(lim, "sendMessage", -100) for _ in range(4)]
    assert times[2] - t0 < 0.05
    assert times[3] - t0 >= 0.19  # 4th must wait for the first slot to expire


async def test_fifo_order_and_chat_isolation():
    lim = RateLimiter(_cfg())
    order = []

    async def send(i, chat):
        await lim.acquire("sendMessage", chat)
        order.append(i)

    await asyncio.gather(*(send(i, -1) for i in range(8)), send("other", -2))
    assert order.index("other") <= 3  # other chat is not blocked by chat -1
    assert [x for x in order if x != "other"] == list(range(8))


async def test_window_is_never_exceeded_under_load():
    rule = Rule(50, 0.1)
    lim = RateLimiter(_cfg(group=rule))
    stamps = []

    async def one():
        await lim.acquire("sendMessage", -7)
        stamps.append(time.monotonic())

    await asyncio.gather(*(one() for _ in range(1500)))
    stamps.sort()
    assert len(stamps) == 1500
    for i in range(len(stamps) - rule.max_calls):
        assert stamps[i + rule.max_calls] - stamps[i] >= rule.period - 0.005


async def test_uncounted_methods_and_disabled_pass_through():
    lim = RateLimiter(_cfg(group=Rule(1, 5.0)))
    for _ in range(5):
        await asyncio.wait_for(lim.acquire("getMe", -1), 0.1)
        await asyncio.wait_for(lim.acquire("editMessageText", -1), 0.1)
    lim2 = RateLimiter(_cfg(group=Rule(1, 5.0), enabled=False))
    for _ in range(5):
        await asyncio.wait_for(lim2.acquire("sendMessage", -1), 0.1)
    lim.enabled = False  # runtime toggle
    for _ in range(5):
        await asyncio.wait_for(lim.acquire("sendMessage", -1), 0.1)


async def test_global_window_spans_chats():
    lim = RateLimiter(_cfg(group=None, global_=Rule(5, 0.2)))
    t0 = time.monotonic()
    await asyncio.gather(*(lim.acquire("sendMessage", -i) for i in range(1, 11)))
    assert time.monotonic() - t0 >= 0.19


async def test_many_chats_share_one_global_timer():
    lim = RateLimiter(_cfg(group=Rule(5, 0.1), global_=Rule(100, 0.1)))
    t0 = time.monotonic()
    await asyncio.gather(*(lim.acquire("sendMessage", -i) for i in range(1, 1001)))
    elapsed = time.monotonic() - t0
    assert 0.8 <= elapsed < 2.0  # 1000/100 = 10 windows of 0.1s
    assert lim.pending == 0


async def test_penalize_pauses_chat_only():
    lim = RateLimiter(_cfg(group=Rule(100, 1.0)))
    await lim.acquire("sendMessage", -1)  # binds the loop
    lim.penalize(-1, 0.3)
    t0 = time.monotonic()
    await lim.acquire("sendMessage", -2)
    assert time.monotonic() - t0 < 0.05
    await lim.acquire("sendMessage", -1)
    assert time.monotonic() - t0 >= 0.29


async def test_penalize_without_retry_after_uses_default():
    lim = RateLimiter(_cfg(group=Rule(100, 1.0), default_penalty=0.2))
    await lim.acquire("sendMessage", -1)
    lim.penalize(-1, None)
    t0 = time.monotonic()
    await lim.acquire("sendMessage", -1)
    assert time.monotonic() - t0 >= 0.19


async def test_chat_id_forms_are_the_same_chat():
    lim = RateLimiter(_cfg(group=Rule(1, 0.2)))
    await lim.acquire("sendMessage", "-100123")
    t0 = time.monotonic()
    await lim.acquire("sendMessage", -100123)
    assert time.monotonic() - t0 >= 0.19


async def test_cancellation_releases_pending_and_keeps_order():
    lim = RateLimiter(_cfg(group=Rule(1, 0.3)))
    await lim.acquire("sendMessage", -1)
    a = asyncio.ensure_future(lim.acquire("sendMessage", -1))
    b = asyncio.ensure_future(lim.acquire("sendMessage", -1))
    await asyncio.sleep(0.01)
    assert lim.pending == 2
    a.cancel()
    with pytest.raises(asyncio.CancelledError):
        await a
    assert lim.pending == 1
    await asyncio.wait_for(b, 1.0)
    assert lim.pending == 0


async def test_queue_full_raises_immediately():
    lim = RateLimiter(_cfg(group=Rule(1, 5.0), max_pending=2, max_wait=None))
    await lim.acquire("sendMessage", -1)
    waiters = [asyncio.ensure_future(lim.acquire("sendMessage", -1)) for _ in range(2)]
    await asyncio.sleep(0.01)
    with pytest.raises(RateLimitQueueFull):
        await lim.acquire("sendMessage", -1)
    for w in waiters:
        w.cancel()
    await asyncio.gather(*waiters, return_exceptions=True)
    assert lim.pending == 0


async def test_max_wait_times_out():
    lim = RateLimiter(_cfg(group=Rule(1, 5.0), max_wait=0.2))
    await lim.acquire("sendMessage", -1)
    t0 = time.monotonic()
    with pytest.raises(RateLimitWaitTimeout):
        await lim.acquire("sendMessage", -1)
    assert 0.19 <= time.monotonic() - t0 < 0.6
    assert lim.pending == 0 and lim.stats()["timeouts"] == 1


async def test_weighted_method_consumes_more_slots():
    lim = RateLimiter(_cfg(group=Rule(4, 0.2), weights={"sendMediaGroup": 3}))
    await lim.acquire("sendMediaGroup", -1)
    t0 = time.monotonic()
    await lim.acquire("sendMessage", -1)
    assert time.monotonic() - t0 < 0.05
    await lim.acquire("sendMessage", -1)  # 3 + 1 used, needs expiry
    assert time.monotonic() - t0 >= 0.19


async def test_idle_chats_are_garbage_collected():
    lim = RateLimiter(_cfg(group=Rule(1, 0.05)))
    for i in range(1, 200):
        await lim.acquire("sendMessage", -i)
    assert lim.stats()["chats"] >= 199
    await asyncio.sleep(0.1)
    lim._next_gc = 0.0
    await lim.acquire("sendMessage", -9999)
    assert lim.stats()["chats"] <= 2


def test_presets_and_resolve():
    bale = RateLimitConfig.bale()
    assert bale.group == Rule(20, 60.0, 0.75) and bale.is_private(5) is False
    tg = RateLimitConfig.telegram()
    assert tg.private.max_calls == 3 and tg.global_.max_calls == 30
    assert tg.is_private(5) and not tg.is_private(-5)
    assert resolve_rate_limiter(False) is None and resolve_rate_limiter(None) is None
    assert isinstance(resolve_rate_limiter(True, RateLimitConfig.bale), RateLimiter)
    lim = RateLimiter()
    assert resolve_rate_limiter(lim) is lim
    assert resolve_rate_limiter(RateLimitConfig.disabled()).enabled is False
    with pytest.raises(ValueError):
        Rule(0, 1.0)
