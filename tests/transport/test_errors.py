from __future__ import annotations

import asyncio

import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.transport import (
    HTTPStatusError,
    NetworkError,
    RateLimitedError,
    Session,
    TimeoutError_,
)


async def _slow(request: web.Request) -> web.Response:
    await asyncio.sleep(0.3)
    return web.Response(text="too slow")


async def _status(request: web.Request) -> web.Response:
    status = int(request.query["code"])
    headers = {}
    retry_after = request.query.get("retry_after")
    if retry_after is not None:
        headers["Retry-After"] = retry_after
    return web.Response(status=status, headers=headers)


def _make_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/slow", _slow)
    app.router.add_get("/status", _status)
    return app


@pytest.mark.asyncio
async def test_timeout_raises_timeout_error() -> None:
    app = _make_app()
    async with TestServer(app) as server:
        async with Session() as session:
            with pytest.raises(TimeoutError_):
                await session.request("GET", str(server.make_url("/slow")), timeout=0.05)


@pytest.mark.asyncio
async def test_connection_refused_raises_retryable_error(refused_connection_url: str) -> None:
    # On most setups this is a fast NetworkError (immediate OS-level
    # refusal). On some Windows environments -- certain antivirus/VPN
    # setups intercept or silently drop connections to unlisted local
    # ports instead of refusing them -- the same "can't connect" condition
    # surfaces as our own TimeoutError_ once the client-side timeout fires.
    # Both are transport-level "could not connect" outcomes and both are
    # retryable (see retry.DEFAULT_RETRYABLE), so either is correct here.
    async with Session() as session:
        with pytest.raises((NetworkError, TimeoutError_)):
            await session.request("GET", refused_connection_url, timeout=2)


@pytest.mark.asyncio
async def test_429_without_retry_after_has_none_hint() -> None:
    app = _make_app()
    async with TestServer(app) as server:
        async with Session() as session:
            with pytest.raises(RateLimitedError) as exc_info:
                await session.request(
                    "GET", str(server.make_url("/status")), params={"code": "429"}
                )
            assert exc_info.value.retry_after_seconds is None


@pytest.mark.asyncio
async def test_429_with_retry_after_parses_hint() -> None:
    app = _make_app()
    async with TestServer(app) as server:
        async with Session() as session:
            with pytest.raises(RateLimitedError) as exc_info:
                await session.request(
                    "GET",
                    str(server.make_url("/status")),
                    params={"code": "429", "retry_after": "7"},
                )
            assert exc_info.value.retry_after_seconds == 7.0


@pytest.mark.asyncio
async def test_403_raises_http_status_error() -> None:
    app = _make_app()
    async with TestServer(app) as server:
        async with Session() as session:
            with pytest.raises(HTTPStatusError) as exc_info:
                await session.request(
                    "GET", str(server.make_url("/status")), params={"code": "403"}
                )
            assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_400_raises_http_status_error() -> None:
    app = _make_app()
    async with TestServer(app) as server:
        async with Session() as session:
            with pytest.raises(HTTPStatusError) as exc_info:
                await session.request(
                    "GET", str(server.make_url("/status")), params={"code": "400"}
                )
            assert exc_info.value.status_code == 400
