from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import List, Tuple

import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.transport import (
    HTTPStatusError,
    RetryPolicy,
    Session,
    TimeoutError_,
    run_with_retry,
)
from peyk.transport.logging_hook import StdlibTransportLogger, get_default_logger


@dataclass
class RecordingLogger:
    """Test double `TransportLogger` that just records every call it gets."""

    requests: List[Tuple[str, str]] = field(default_factory=list)
    retries: List[Tuple[int, Exception]] = field(default_factory=list)
    failures: List[Exception] = field(default_factory=list)

    def log_request(self, method: str, url: str) -> None:
        self.requests.append((method, url))

    def log_retry(self, attempt: int, exception: Exception) -> None:
        self.retries.append((attempt, exception))

    def log_failure(self, exception: Exception) -> None:
        self.failures.append(exception)


async def _ok(request: web.Request) -> web.Response:
    return web.Response(text="ok")


def _make_ok_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/ok", _ok)
    return app


@pytest.mark.asyncio
async def test_request_logs_each_attempt_with_method_and_url() -> None:
    app = _make_ok_app()
    logger = RecordingLogger()

    async with TestServer(app) as server:
        async with Session(logger=logger) as session:
            url = str(server.make_url("/ok"))
            await session.request("GET", url)
            await session.request("GET", url)

            assert logger.requests == [("GET", url), ("GET", url)]


@pytest.mark.asyncio
async def test_retry_logs_retry_per_attempt_and_no_failure_on_eventual_success() -> None:
    # Extends A1's "429 with Retry-After" scenario (test_retry.py) with
    # logging assertions, rather than only checking behavior in isolation.
    calls = {"count": 0}

    async def handler(request: web.Request) -> web.Response:
        calls["count"] += 1
        if calls["count"] < 3:
            return web.Response(status=429, headers={"Retry-After": "0.01"})
        return web.Response(text="ok")

    app = web.Application()
    app.router.add_get("/flaky", handler)
    logger = RecordingLogger()

    async with TestServer(app) as server:
        async with Session(logger=logger) as session:
            policy = RetryPolicy(max_attempts=5, base_backoff_seconds=0.01)

            async def op():
                return await session.request("GET", str(server.make_url("/flaky")))

            resp = await run_with_retry(op, policy, logger=logger)

            assert resp.status == 200
            assert calls["count"] == 3
            # Two 429s before the success that ends the loop.
            assert [attempt for attempt, _ in logger.retries] == [1, 2]
            assert logger.failures == []
            # request() logged all three attempts too.
            assert len(logger.requests) == 3


@pytest.mark.asyncio
async def test_retry_logs_failure_once_retries_exhausted() -> None:
    # Extends A1's "timeout retried then raises" scenario with logging.
    async def handler(request: web.Request) -> web.Response:
        await asyncio.sleep(0.3)
        return web.Response(text="too slow")

    app = web.Application()
    app.router.add_get("/slow", handler)
    logger = RecordingLogger()

    async with TestServer(app) as server:
        async with Session(logger=logger) as session:
            policy = RetryPolicy(max_attempts=3, base_backoff_seconds=0.01)

            async def op():
                return await session.request(
                    "GET", str(server.make_url("/slow")), timeout=0.05
                )

            with pytest.raises(TimeoutError_):
                await run_with_retry(op, policy, logger=logger)

            assert len(logger.retries) == 2  # retried after attempts 1 and 2
            assert len(logger.failures) == 1
            assert isinstance(logger.failures[0], TimeoutError_)


@pytest.mark.asyncio
async def test_retry_logs_failure_immediately_for_non_retryable_error() -> None:
    # Extends A1's "HTTPStatusError never retried" scenario with logging.
    calls = {"count": 0}

    async def handler(request: web.Request) -> web.Response:
        calls["count"] += 1
        return web.Response(status=403)

    app = web.Application()
    app.router.add_get("/forbidden", handler)
    logger = RecordingLogger()

    async with TestServer(app) as server:
        async with Session(logger=logger) as session:
            policy = RetryPolicy(max_attempts=3, base_backoff_seconds=0.01)

            async def op():
                return await session.request("GET", str(server.make_url("/forbidden")))

            with pytest.raises(HTTPStatusError):
                await run_with_retry(op, policy, logger=logger)

            assert calls["count"] == 1
            assert logger.retries == []
            assert len(logger.failures) == 1
            assert isinstance(logger.failures[0], HTTPStatusError)


@pytest.mark.asyncio
async def test_no_logger_passed_uses_default_without_error() -> None:
    # Mirrors how A1's existing tests call Session()/run_with_retry() with
    # no logger argument at all -- must keep working unmodified.
    app = _make_ok_app()
    async with TestServer(app) as server:
        async with Session() as session:
            policy = RetryPolicy(max_attempts=2, base_backoff_seconds=0.01)

            async def op():
                return await session.request("GET", str(server.make_url("/ok")))

            resp = await run_with_retry(op, policy)
            assert resp.status == 200


def test_default_logger_is_stdlib_backed_singleton() -> None:
    logger1 = get_default_logger()
    logger2 = get_default_logger()
    assert logger1 is logger2
    assert isinstance(logger1, StdlibTransportLogger)
