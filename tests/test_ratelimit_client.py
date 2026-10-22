"""Rate limiter wired into TelegramLikeClient._call (fake session, no network)."""
from __future__ import annotations

import asyncio
import time
from types import SimpleNamespace
from typing import Any, List, Optional

import pytest

from peyk.platforms._telegram_like.base_client import TelegramLikeClient
from peyk.ratelimit import RateLimitConfig, RateLimiter, Rule
from peyk.transport.errors import RateLimitedError
from peyk.transport.retry import RetryPolicy


class _APIError(Exception):
    def __init__(self, message: str, *, error_code: int, description: str, parameters: Any = None) -> None:
        super().__init__(message)
        self.error_code = error_code


class _Client(TelegramLikeClient):
    base_url = "http://fake"
    _error_class = _APIError

    def _extract_retry_hint(self, response: Any) -> Optional[float]:
        params = response.get("parameters")
        value = params.get("retry_after") if isinstance(params, dict) else None
        return float(value) if value is not None else None


class _Session:
    """Records (time, method, chat_id) and replays queued behaviours."""

    def __init__(self) -> None:
        self.calls: List[tuple] = []
        self.script: List[Any] = []  # items: dict envelope or Exception, consumed per call

    async def request(self, method, url, *, json_body=None, data=None, files=None, **_kw):
        chat = (json_body or data or {}).get("chat_id")
        self.calls.append((time.monotonic(), url.rsplit("/", 1)[-1], chat))
        item = self.script.pop(0) if self.script else {"ok": True, "result": 1}
        if isinstance(item, Exception):
            raise item
        return SimpleNamespace(status=200, json=item, body=b"", headers={})


def _client(**cfg):
    session = _Session()
    config = RateLimitConfig(group=Rule(2, 0.2), private=None, is_private=lambda _c: False, **cfg)
    client = _Client("T", session, retry_policy=RetryPolicy(max_attempts=3, base_backoff_seconds=0.01), rate_limit=config)
    return client, session


async def test_sends_are_spaced_per_chat():
    client, session = _client()
    await asyncio.gather(*(client._call("sendMessage", json_body={"chat_id": -1, "text": "x"}) for _ in range(5)))
    times = sorted(t for t, *_ in session.calls)
    assert len(times) == 5
    for i in range(len(times) - 2):
        assert times[i + 2] - times[i] >= 0.19
    assert isinstance(client.rate_limiter, RateLimiter)


async def test_other_methods_and_chats_are_not_delayed():
    client, session = _client()
    t0 = time.monotonic()
    for _ in range(10):
        await client._call("getMe")
        await client._call("editMessageText", json_body={"chat_id": -1})
    await client._call("sendMessage", json_body={"chat_id": -2})
    assert time.monotonic() - t0 < 0.1


async def test_multipart_chat_id_is_extracted():
    client, session = _client()
    await asyncio.gather(*(client._call("sendDocument", data={"chat_id": "-9"}, files={"f": b"x"}) for _ in range(3)))
    times = sorted(t for t, *_ in session.calls)
    assert times[2] - times[0] >= 0.19


async def test_rate_limit_false_disables_and_keeps_old_429_behaviour():
    session = _Session()
    client = _Client("T", session, retry_policy=RetryPolicy(max_attempts=3, base_backoff_seconds=0.01), rate_limit=False)
    assert client.rate_limiter is None
    t0 = time.monotonic()
    await asyncio.gather(*(client._call("sendMessage", json_body={"chat_id": -1}) for _ in range(6)))
    assert time.monotonic() - t0 < 0.1
    session.script = [{"ok": False, "error_code": 429, "description": "slow", "parameters": {"retry_after": 7}}]
    with pytest.raises(RateLimitedError) as exc:
        await client._call("sendMessage", json_body={"chat_id": -1})
    assert exc.value.retry_after_seconds == 7.0


async def test_envelope_429_pauses_then_retries_automatically():
    client, session = _client()
    session.script = [{"ok": False, "error_code": 429, "description": "slow", "parameters": {"retry_after": 0.2}}]
    t0 = time.monotonic()
    assert await client._call("sendMessage", json_body={"chat_id": -1}) == 1
    assert len(session.calls) == 2
    assert session.calls[1][0] - session.calls[0][0] >= 0.19
    # The pause also covers other senders of the same chat, not other chats.
    session.script = [{"ok": False, "error_code": 429, "description": "slow", "parameters": {"retry_after": 0.3}}]
    t1 = time.monotonic()
    first = asyncio.ensure_future(client._call("sendMessage", json_body={"chat_id": -5}))
    await asyncio.sleep(0.02)
    other_chat = time.monotonic()
    await client._call("sendMessage", json_body={"chat_id": -6})
    assert time.monotonic() - other_chat < 0.1
    await first
    assert time.monotonic() - t1 >= 0.29


async def test_http_level_429_also_penalizes_chat():
    client, session = _client()
    session.script = [RateLimitedError("slow", retry_after_seconds=0.25)]
    await client._call("sendMessage", json_body={"chat_id": -3})
    assert len(session.calls) == 2
    assert session.calls[1][0] - session.calls[0][0] >= 0.24


async def test_runtime_toggle():
    client, session = _client()
    client.rate_limiter.enabled = False
    t0 = time.monotonic()
    await asyncio.gather(*(client._call("sendMessage", json_body={"chat_id": -1}) for _ in range(8)))
    assert time.monotonic() - t0 < 0.1
