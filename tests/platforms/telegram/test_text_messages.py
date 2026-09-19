"""Tests for `TelegramClient` text-message methods (Phase T2).

Fake `aiohttp.test_utils` server, zero real network -- same pattern as
the T1 client tests. One happy-path test per method (request shape +
response parsing), both `edit_message_text` targeting variants, and
multi-element lists for the plural batch methods.
"""

from __future__ import annotations

from typing import Any, Callable, Dict

import orjson
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms.telegram.client import TelegramClient
from peyk.platforms.telegram.models import (
    LinkPreviewOptions,
    Message,
    MessageEntity,
    MessageId,
    ReplyParameters,
)
from peyk.transport import RetryPolicy

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


def _sample_message_raw(message_id: int = 1, text: str = "hello") -> Dict[str, Any]:
    return {
        "message_id": message_id,
        "date": 1690000000,
        "chat": SAMPLE_CHAT_RAW,
        "from": SAMPLE_USER_RAW,
        "text": text,
    }


class FakeTelegramServer:
    def __init__(self) -> None:
        self.responses: Dict[str, Callable[[Any], Any]] = {}
        self.request_log: list[Dict[str, Any]] = []
        self.app = web.Application()
        self.app.router.add_route("*", "/bot{token}/{method}", self._handle)

    def set_response(
        self, method_name: str, result_builder: Callable[[Any], Any]
    ) -> None:
        self.responses[method_name] = result_builder

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
        builder = self.responses.get(method_name)
        result = builder(parsed_body) if builder else None
        return web.json_response({"ok": True, "result": result})

    def calls_for(self, method_name: str) -> list[Dict[str, Any]]:
        return [c for c in self.request_log if c["method_name"] == method_name]


@pytest.fixture
async def fake_server():
    server = FakeTelegramServer()
    async with TestServer(server.app) as test_server:
        yield server, test_server


def _client_for(test_server: TestServer) -> TelegramClient:
    base_url = str(test_server.make_url("")).rstrip("/")
    return TelegramClient(
        TOKEN,
        base_url=base_url,
        retry_policy=RetryPolicy(max_attempts=3, base_backoff_seconds=0.001),
    )


async def test_send_message_minimal(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("sendMessage", lambda body: _sample_message_raw(1))

    client = _client_for(test_server)
    try:
        msg = await client.send_message(200, "hello")
    finally:
        await client.close()

    assert isinstance(msg, Message)
    assert msg.message_id == 1
    assert msg.text == "hello"
    body = server.calls_for("sendMessage")[0]["body"]
    assert body == {"chat_id": 200, "text": "hello"}


async def test_send_message_full_options(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("sendMessage", lambda body: _sample_message_raw(2))

    client = _client_for(test_server)
    try:
        msg = await client.send_message(
            "@channel",
            "hi *there*",
            message_thread_id=3,
            parse_mode="MarkdownV2",
            entities=[MessageEntity(type="bold", offset=3, length=5)],
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            disable_notification=True,
            protect_content=True,
            reply_parameters=ReplyParameters(message_id=1, quote="hel"),
            reply_markup={"inline_keyboard": []},
        )
    finally:
        await client.close()

    assert msg.message_id == 2
    body = server.calls_for("sendMessage")[0]["body"]
    assert body["chat_id"] == "@channel"
    assert body["message_thread_id"] == 3
    assert body["parse_mode"] == "MarkdownV2"
    assert body["entities"] == [{"type": "bold", "offset": 3, "length": 5}]
    assert body["link_preview_options"] == {"is_disabled": True}
    assert body["disable_notification"] is True
    assert body["protect_content"] is True
    assert body["reply_parameters"] == {"message_id": 1, "quote": "hel"}
    assert body["reply_markup"] == {"inline_keyboard": []}
    assert "reply_to_message_id" not in body


async def test_forward_message(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("forwardMessage", lambda body: _sample_message_raw(5))

    client = _client_for(test_server)
    try:
        msg = await client.forward_message(200, 300, 7, disable_notification=True)
    finally:
        await client.close()

    assert msg.message_id == 5
    body = server.calls_for("forwardMessage")[0]["body"]
    assert body == {
        "chat_id": 200,
        "from_chat_id": 300,
        "message_id": 7,
        "disable_notification": True,
    }


async def test_forward_messages_multi_element(fake_server) -> None:
    server, test_server = fake_server

    def _result(body: Any) -> Any:
        assert body["message_ids"] == [7, 8, 9]
        return [{"message_id": mid} for mid in (101, 102, 103)]

    server.set_response("forwardMessages", _result)

    client = _client_for(test_server)
    try:
        ids = await client.forward_messages(200, 300, [7, 8, 9])
    finally:
        await client.close()

    assert ids == [MessageId(101), MessageId(102), MessageId(103)]
    body = server.calls_for("forwardMessages")[0]["body"]
    assert body["chat_id"] == 200
    assert body["from_chat_id"] == 300


async def test_copy_message(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("copyMessage", lambda body: {"message_id": 55})

    client = _client_for(test_server)
    try:
        mid = await client.copy_message(
            200, 300, 7, caption="new caption", parse_mode="HTML"
        )
    finally:
        await client.close()

    assert mid == MessageId(55)
    body = server.calls_for("copyMessage")[0]["body"]
    assert body["message_id"] == 7
    assert body["caption"] == "new caption"
    assert body["parse_mode"] == "HTML"


async def test_copy_messages_multi_element(fake_server) -> None:
    server, test_server = fake_server

    def _result(body: Any) -> Any:
        assert body["message_ids"] == [7, 8]
        assert body["remove_caption"] is True
        return [{"message_id": 201}, {"message_id": 202}]

    server.set_response("copyMessages", _result)

    client = _client_for(test_server)
    try:
        ids = await client.copy_messages(200, 300, [7, 8], remove_caption=True)
    finally:
        await client.close()

    assert [m.message_id for m in ids] == [201, 202]


async def test_delete_message(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("deleteMessage", lambda body: True)

    client = _client_for(test_server)
    try:
        ok = await client.delete_message(200, 7)
    finally:
        await client.close()

    assert ok is True
    assert server.calls_for("deleteMessage")[0]["body"] == {
        "chat_id": 200,
        "message_id": 7,
    }


async def test_delete_messages_multi_element(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("deleteMessages", lambda body: True)

    client = _client_for(test_server)
    try:
        ok = await client.delete_messages(200, [7, 8, 9])
    finally:
        await client.close()

    assert ok is True
    assert server.calls_for("deleteMessages")[0]["body"] == {
        "chat_id": 200,
        "message_ids": [7, 8, 9],
    }


async def test_edit_message_text_by_chat_and_message_id(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "editMessageText", lambda body: _sample_message_raw(7, "edited")
    )

    client = _client_for(test_server)
    try:
        result = await client.edit_message_text(
            "edited",
            chat_id=200,
            message_id=7,
            parse_mode="HTML",
            reply_markup={"inline_keyboard": []},
        )
    finally:
        await client.close()

    assert isinstance(result, Message)
    assert result.text == "edited"
    body = server.calls_for("editMessageText")[0]["body"]
    assert body["chat_id"] == 200
    assert body["message_id"] == 7
    assert body["text"] == "edited"
    assert body["parse_mode"] == "HTML"


async def test_edit_message_text_by_inline_message_id(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("editMessageText", lambda body: True)

    client = _client_for(test_server)
    try:
        result = await client.edit_message_text(
            "edited inline", inline_message_id="ABC123"
        )
    finally:
        await client.close()

    assert result is True
    body = server.calls_for("editMessageText")[0]["body"]
    assert body == {"text": "edited inline", "inline_message_id": "ABC123"}


async def test_edit_message_text_requires_target() -> None:
    client = TelegramClient(TOKEN, base_url="http://127.0.0.1:1")
    try:
        with pytest.raises(ValueError):
            await client.edit_message_text("x")
        with pytest.raises(ValueError):
            await client.edit_message_reply_markup()
    finally:
        await client.close()


async def test_edit_message_reply_markup_both_variants(fake_server) -> None:
    server, test_server = fake_server
    calls = {"n": 0}

    def _result(body: Any) -> Any:
        calls["n"] += 1
        if calls["n"] == 1:
            return _sample_message_raw(7, "hello")
        return True

    server.set_response("editMessageReplyMarkup", _result)

    client = _client_for(test_server)
    try:
        first = await client.edit_message_reply_markup(
            chat_id=200, message_id=7, reply_markup={"inline_keyboard": []}
        )
        second = await client.edit_message_reply_markup(
            inline_message_id="ABC123", reply_markup={"inline_keyboard": []}
        )
    finally:
        await client.close()

    assert isinstance(first, Message)
    assert second is True
    bodies = [c["body"] for c in server.calls_for("editMessageReplyMarkup")]
    assert bodies[0]["chat_id"] == 200
    assert bodies[0]["message_id"] == 7
    assert bodies[1] == {
        "inline_message_id": "ABC123",
        "reply_markup": {"inline_keyboard": []},
    }


async def test_link_preview_options_round_trip() -> None:
    opts = LinkPreviewOptions(
        is_disabled=False, url="https://example.com", show_above_text=True
    )
    assert LinkPreviewOptions.from_dict(opts.to_dict()) == opts
    assert ReplyParameters.from_dict(
        ReplyParameters(message_id=1).to_dict()
    ) == ReplyParameters(message_id=1)
