from __future__ import annotations

import asyncio

import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.transport import (
    HTTPStatusError,
    NetworkError,
    RetryPolicy,
    Session,
    TimeoutError_,
    run_with_retry,
)


def _make_app(handler) -> web.Application:
    app = web.Application()
    app.router.add_get("/x", handler)
    return app


@pytest.mark.asyncio
async def test_timeout_retried_configured_times_then_raises() -> None:
    calls = {"count": 0}

    async def handler(request: web.Request) -> web.Response:
        calls["count"] += 1
        await asyncio.sleep(0.3)
        return web.Response(text="too slow")

    app = _make_app(handler)
    async with TestServer(app) as server:
        async with Session() as session:
            policy = RetryPolicy(max_attempts=3, base_backoff_seconds=0.01)

            async def op():
                return await session.request(
                    "GET", str(server.make_url("/x")), timeout=0.05
                )

            with pytest.raises(TimeoutError_):
                await run_with_retry(op, policy)

            assert calls["count"] == 3


@pytest.mark.asyncio
async def test_connection_refused_retried_correctly(refused_connection_url: str) -> None:
    # Same NetworkError-vs-TimeoutError_ note as in test_errors.py: both
    # represent "could not connect" and both are retryable, so either is
    # an acceptable final exception here -- what matters is the retry
    # count and that it does give up.
    calls = {"count": 0}
    policy = RetryPolicy(max_attempts=3, base_backoff_seconds=0.01)

    async with Session() as session:

        async def op():
            calls["count"] += 1
            return await session.request("GET", refused_connection_url, timeout=2)

        with pytest.raises((NetworkError, TimeoutError_)):
            await run_with_retry(op, policy)

    assert calls["count"] == 3


@pytest.mark.asyncio
async def test_429_retry_honors_retry_after_hint() -> None:
    calls = {"count": 0}

    async def handler(request: web.Request) -> web.Response:
        calls["count"] += 1
        if calls["count"] < 2:
            return web.Response(status=429, headers={"Retry-After": "0.05"})
        return web.Response(status=200, text="ok")

    app = _make_app(handler)
    async with TestServer(app) as server:
        async with Session() as session:
            # base_backoff_seconds is deliberately huge so the test only
            # passes if the 0.05s Retry-After hint was actually used.
            policy = RetryPolicy(max_attempts=3, base_backoff_seconds=5.0)

            async def op():
                return await session.request("GET", str(server.make_url("/x")))

            loop = asyncio.get_event_loop()
            start = loop.time()
            resp = await run_with_retry(op, policy)
            elapsed = loop.time() - start

            assert resp.status == 200
            assert calls["count"] == 2
            assert elapsed < 1.0


@pytest.mark.asyncio
async def test_http_status_error_never_retried() -> None:
    calls = {"count": 0}

    async def handler(request: web.Request) -> web.Response:
        calls["count"] += 1
        return web.Response(status=403)

    app = _make_app(handler)
    async with TestServer(app) as server:
        async with Session() as session:
            policy = RetryPolicy(max_attempts=3, base_backoff_seconds=0.01)

            async def op():
                return await session.request("GET", str(server.make_url("/x")))

            with pytest.raises(HTTPStatusError):
                await run_with_retry(op, policy)

            assert calls["count"] == 1
