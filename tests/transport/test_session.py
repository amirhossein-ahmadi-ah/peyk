from __future__ import annotations

import orjson
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.transport import Session


async def _echo(request: web.Request) -> web.Response:
    payload = await request.read()
    return web.Response(body=payload, content_type="application/json")


def _make_app() -> web.Application:
    app = web.Application()
    app.router.add_route("*", "/echo", _echo)
    return app


@pytest.mark.asyncio
async def test_successful_json_response_round_trips() -> None:
    app = _make_app()
    async with TestServer(app) as server:
        async with Session() as session:
            resp = await session.request(
                "POST",
                str(server.make_url("/echo")),
                json_body={"hello": "world", "n": 1},
            )

            assert resp.status == 200
            assert resp.json == {"hello": "world", "n": 1}
            assert orjson.loads(resp.body) == {"hello": "world", "n": 1}


@pytest.mark.asyncio
async def test_session_reuses_same_connector_across_requests() -> None:
    app = _make_app()
    async with TestServer(app) as server:
        async with Session() as session:
            connector_before = session.connector

            await session.request("GET", str(server.make_url("/echo")))
            await session.request("GET", str(server.make_url("/echo")))
            await session.request("GET", str(server.make_url("/echo")))

            connector_after = session.connector

            # Same connector object across every call -- request() must not
            # build a new ClientSession/TCPConnector per call.
            assert connector_before is connector_after
            assert session._session.connector is connector_before


@pytest.mark.asyncio
async def test_data_without_files_is_form_urlencoded() -> None:
    app = _make_app()
    async with TestServer(app) as server:
        async with Session() as session:
            resp = await session.request(
                "POST", str(server.make_url("/echo")), data={"a": "1", "b": "x y"}
            )
    assert resp.body == b"a=1&b=x+y"
