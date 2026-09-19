"""Isolated contract tests for the M2 TelegramLikeClient skeleton."""

from __future__ import annotations

from io import BytesIO
from typing import Any, Dict, Optional

import orjson
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms._telegram_like import TelegramLikeClient
from peyk.transport import FilePayload
from peyk.transport.errors import RateLimitedError
from peyk.transport.errors import TransportError


class FakeAPIError(TransportError):
    def __init__(
        self,
        message: str,
        *,
        error_code: int,
        description: str,
        parameters: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.description = description
        self.parameters = parameters


class FakeClient(TelegramLikeClient):
    base_url = "PLACEHOLDER"
    _error_class = FakeAPIError

    def _extract_retry_hint(self, response: Any) -> Optional[float]:
        parameters = response.get("parameters")
        retry_after = parameters.get("retry_after") if isinstance(parameters, dict) else None
        return float(retry_after) if retry_after is not None else None


class FakeServer:
    def __init__(self) -> None:
        self.requests: list[Dict[str, Any]] = []
        self.responses: Dict[str, Any] = {}
        self.app = web.Application()
        self.app.router.add_post("/bot{token}/{method}", self.handle)

    async def handle(self, request: web.Request) -> web.Response:
        content_type = request.headers.get("Content-Type", "")
        if "multipart/form-data" in content_type:
            reader = await request.multipart()
            fields: Dict[str, str] = {}
            files: Dict[str, Dict[str, Any]] = {}
            async for part in reader:
                if part.filename:
                    files[part.name] = {
                        "filename": part.filename,
                        "content_type": part.headers.get("Content-Type"),
                        "content": await part.read(decode=False),
                    }
                else:
                    fields[part.name] = await part.text()
            body: Any = {"fields": fields, "files": files}
        else:
            raw = await request.read()
            body = orjson.loads(raw) if raw else {}
        method = request.match_info["method"]
        self.requests.append({"method": method, "body": body})
        return web.json_response(self.responses.get(method, {"ok": True, "result": None}))


@pytest.fixture
async def fake_server():
    server = FakeServer()
    async with TestServer(server.app) as test_server:
        yield server, str(test_server.make_url("")).rstrip("/")


@pytest.fixture
async def client(fake_server):
    server, base_url = fake_server
    FakeClient.base_url = base_url
    client = FakeClient("TOKEN")
    yield client, server
    await client.close()


@pytest.mark.asyncio
async def test_call_success_and_failure(client):
    api, server = client
    server.responses["okMethod"] = {"ok": True, "result": {"answer": 42}}
    assert await api._call("okMethod", json_body={"x": 1}) == {"answer": 42}

    server.responses["badMethod"] = {
        "ok": False,
        "error_code": 400,
        "description": "bad request",
    }
    with pytest.raises(FakeAPIError) as exc_info:
        await api._call("badMethod")
    assert exc_info.value.error_code == 400
    assert exc_info.value.description == "bad request"
    assert server.requests[-1]["method"] == "badMethod"


@pytest.mark.asyncio
async def test_call_extracts_platform_retry_hint_without_retrying(client):
    api, server = client
    server.responses["limited"] = {
        "ok": False,
        "error_code": 429,
        "description": "Too Many Requests",
        "parameters": {"retry_after": 7},
    }
    with pytest.raises(RateLimitedError) as exc_info:
        await api._call("limited")
    assert exc_info.value.retry_after_seconds == 7.0
    assert len(server.requests) == 1


@pytest.mark.asyncio
async def test_media_dispatch_json_and_multipart(client):
    api, server = client
    server.responses["media"] = {"ok": True, "result": "ok"}

    kwargs = api._media_request_kwargs(
        "photo",
        "file-id-or-url",
        json_fields={"chat_id": 123, "caption": "hello"},
        default_filename="photo.jpg",
    )
    assert kwargs["json_body"] == {
        "chat_id": 123,
        "caption": "hello",
        "photo": "file-id-or-url",
    }
    assert "files" not in kwargs
    await api._call("media", **kwargs)
    assert server.requests[-1]["body"] == kwargs["json_body"]

    stream = BytesIO(b"payload")
    kwargs = api._media_request_kwargs(
        "photo",
        stream,
        json_fields={"chat_id": 123, "reply_markup": {"inline": True}},
        default_filename="photo.jpg",
    )
    assert kwargs["data"]["reply_markup"] == '{"inline":true}'
    assert kwargs["files"]["photo"].content is stream
    await api._call("media", **kwargs)
    multipart = server.requests[-1]["body"]
    assert multipart["fields"]["chat_id"] == "123"
    assert multipart["fields"]["reply_markup"] == '{"inline":true}'
    assert multipart["files"]["photo"]["filename"] == "photo.jpg"
    assert multipart["files"]["photo"]["content"] == b"payload"

    payload = FilePayload(b"bytes", "custom.bin", "application/octet-stream")
    assert api._as_file_payload(payload, default_filename="ignored") is payload


@pytest.mark.asyncio
async def test_validate_callback_data_uses_utf8_bytes(client):
    api, _ = client
    api.validate_callback_data("a")
    api.validate_callback_data("ی" * 32)
    with pytest.raises(ValueError):
        api.validate_callback_data("")
    with pytest.raises(ValueError):
        api.validate_callback_data("a" * 65)
    with pytest.raises(ValueError):
        api.validate_callback_data("ی" * 33)
