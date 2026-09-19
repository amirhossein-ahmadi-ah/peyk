"""Tests for `TelegramClient` (Phase T1).

Uses `aiohttp.test_utils` to run a local fake server that speaks the
real Telegram response shape (`ok`/`result`/`description`/`error_code`)
-- zero real network calls, same approach as the Bale client tests. The
fake server records the last requests it saw (method name, JSON body,
HTTP method) so tests can assert on request shape, not just on the
parsed model coming back.
"""

from __future__ import annotations

from typing import Any, Callable, Dict

import orjson
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms.telegram.client import TelegramClient
from peyk.platforms.telegram.errors import TelegramAPIError
from peyk.transport import RetryPolicy
from peyk.transport.errors import RateLimitedError

TOKEN = "12345:TEST-TOKEN"

SAMPLE_USER_RAW = {
    "id": 100,
    "is_bot": True,
    "first_name": "TestBot",
    "username": "test_bot",
}

SAMPLE_CHAT_RAW = {
    "id": 200,
    "type": "private",
    "first_name": "Some",
    "last_name": "One",
    "username": "someone",
}


def _sample_message_raw(message_id: int = 1) -> Dict[str, Any]:
    return {
        "message_id": message_id,
        "date": 1690000000,
        "chat": SAMPLE_CHAT_RAW,
        "from": SAMPLE_USER_RAW,
        "text": "hello",
    }


class FakeTelegramServer:
    """A minimal aiohttp app mimicking `api.telegram.org` routing/shape."""

    def __init__(self) -> None:
        self.responses: Dict[str, Callable[[Any], Any]] = {}
        self.raw_envelopes: Dict[str, Any] = {}
        self.request_log: list[Dict[str, Any]] = []
        self.app = web.Application()
        self.app.router.add_route("*", "/bot{token}/{method}", self._handle)

    def set_response(
        self, method_name: str, result_builder: Callable[[Any], Any]
    ) -> None:
        self.responses[method_name] = result_builder

    def set_raw_envelope(self, method_name: str, envelope: Any) -> None:
        """Bypass the ok:true wrapping entirely -- for ok:false tests."""
        self.raw_envelopes[method_name] = envelope

    async def _handle(self, request: web.Request) -> web.Response:
        method_name = request.match_info["method"]
        token = request.match_info["token"]

        raw = await request.read()
        parsed_body: Any = orjson.loads(raw) if raw else {}

        self.request_log.append(
            {
                "method_name": method_name,
                "token": token,
                "http_method": request.method,
                "body": parsed_body,
            }
        )

        if method_name in self.raw_envelopes:
            return web.json_response(self.raw_envelopes[method_name])

        builder = self.responses.get(method_name)
        result = builder(parsed_body) if builder else None
        return web.json_response({"ok": True, "result": result})

    @property
    def call_count(self) -> int:
        return len(self.request_log)

    def calls_for(self, method_name: str) -> list[Dict[str, Any]]:
        return [c for c in self.request_log if c["method_name"] == method_name]


@pytest.fixture
async def fake_server():
    server = FakeTelegramServer()
    async with TestServer(server.app) as test_server:
        yield server, test_server


def _client_for(
    test_server: TestServer, server: FakeTelegramServer
) -> TelegramClient:
    base_url = str(test_server.make_url("")).rstrip("/")
    # No backoff delay so any accidental retry would still fail fast
    # via call_count assertions rather than slow tests.
    return TelegramClient(
        TOKEN,
        base_url=base_url,
        retry_policy=RetryPolicy(max_attempts=3, base_backoff_seconds=0.001),
    )


async def test_get_me_request_shape_and_parsing(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("getMe", lambda body: SAMPLE_USER_RAW)

    client = _client_for(test_server, server)
    try:
        me = await client.get_me()
    finally:
        await client.close()

    assert me.id == 100
    assert me.is_bot is True
    assert me.username == "test_bot"

    calls = server.calls_for("getMe")
    assert len(calls) == 1
    assert calls[0]["http_method"] == "POST"
    assert calls[0]["token"] == TOKEN


async def test_get_updates_parses_deep_message(fake_server) -> None:
    server, test_server = fake_server

    def _result(body: Any) -> Any:
        assert body.get("offset") == 10
        assert body.get("limit") == 5
        assert body.get("timeout") == 30
        inner = _sample_message_raw(11)
        inner["entities"] = [{"type": "bold", "offset": 0, "length": 5}]
        inner["reply_to_message"] = {
            "message_id": 10,
            "date": 1689999999,
            "chat": SAMPLE_CHAT_RAW,
            "from": {"id": 7, "is_bot": False, "first_name": "X"},
            "text": "original",
        }
        return [{"update_id": 9001, "message": inner}]

    server.set_response("getUpdates", _result)

    client = _client_for(test_server, server)
    try:
        updates = await client.get_updates(offset=10, limit=5, timeout=30)
    finally:
        await client.close()

    assert len(updates) == 1
    assert updates[0].update_id == 9001
    msg = updates[0].message
    assert msg.message_id == 11
    assert msg.entities[0].type == "bold"
    assert msg.reply_to_message.message_id == 10
    assert msg.reply_to_message.text == "original"


async def test_get_updates_default_body_is_empty_object(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("getUpdates", lambda body: [])

    client = _client_for(test_server, server)
    try:
        updates = await client.get_updates()
    finally:
        await client.close()

    assert updates == []
    assert server.calls_for("getUpdates")[0]["body"] == {}


async def test_set_webhook_request_shape(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setWebhook", lambda body: True)

    client = _client_for(test_server, server)
    try:
        ok = await client.set_webhook(
            "https://example.com/hook", max_connections=40
        )
    finally:
        await client.close()

    assert ok is True
    body = server.calls_for("setWebhook")[0]["body"]
    assert body["url"] == "https://example.com/hook"
    assert body["max_connections"] == 40


async def test_delete_webhook_request_shape(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("deleteWebhook", lambda body: True)

    client = _client_for(test_server, server)
    try:
        ok = await client.delete_webhook(drop_pending_updates=True)
    finally:
        await client.close()

    assert ok is True
    body = server.calls_for("deleteWebhook")[0]["body"]
    assert body["drop_pending_updates"] is True


async def test_get_webhook_info_parsing(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "getWebhookInfo",
        lambda body: {
            "url": "https://example.com/hook",
            "has_custom_certificate": False,
            "pending_update_count": 3,
            "max_connections": 40,
        },
    )

    client = _client_for(test_server, server)
    try:
        info = await client.get_webhook_info()
    finally:
        await client.close()

    assert info.url == "https://example.com/hook"
    assert info.pending_update_count == 3
    assert info.max_connections == 40


async def test_ok_false_without_retry_after_raises_api_error_no_retry(
    fake_server,
) -> None:
    server, test_server = fake_server
    server.set_raw_envelope(
        "getMe",
        {"ok": False, "error_code": 401, "description": "Unauthorized"},
    )

    client = _client_for(test_server, server)
    try:
        with pytest.raises(TelegramAPIError) as exc_info:
            await client.get_me()
    finally:
        await client.close()

    assert exc_info.value.error_code == 401
    assert exc_info.value.description == "Unauthorized"
    # Plain application errors are never retried.
    assert server.call_count == 1


async def test_ok_false_with_retry_after_raises_rate_limited_no_retry(
    fake_server,
) -> None:
    server, test_server = fake_server
    server.set_raw_envelope(
        "getMe",
        {
            "ok": False,
            "error_code": 429,
            "description": "Too Many Requests: retry after 30",
            "parameters": {"retry_after": 30},
        },
    )

    client = _client_for(test_server, server)
    try:
        with pytest.raises(RateLimitedError) as exc_info:
            await client.get_me()
    finally:
        await client.close()

    assert exc_info.value.retry_after_seconds == 30.0
    # Raised post-retry (like TelegramAPIError): visible as a
    # retryable-typed signal, but _call does not auto-retry it.
    assert server.call_count == 1
