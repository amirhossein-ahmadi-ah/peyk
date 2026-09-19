"""Tests for ``RubikaClient`` (validated against official docs)."""

from __future__ import annotations

import base64
from typing import Any, Callable, Dict

import orjson
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms.rubika.client import RubikaClient
from peyk.platforms.rubika.errors import RubikaAPIError
from peyk.platforms.rubika.models import (
    Bot,
    BotCommand,
    Button,
    Chat,
    ChatKeypadTypeEnum,
    FileTypeEnum,
    Keypad,
    KeypadRow,
    Message,
    Metadata,
    MetadataPart,
    UpdateEndpointTypeEnum,
)
from peyk.transport import RetryPolicy

TOKEN = "TEST-TOKEN"


class FakeRubikaServer:
    def __init__(self) -> None:
        self.responses: Dict[str, Callable[[Any], Any]] = {}
        self.raw_envelopes: Dict[str, Any] = {}
        self.request_log: list[Dict[str, Any]] = []
        self.upload_responses: Dict[str, Any] = {}
        self.app = web.Application()
        self.app.router.add_route("POST", "/v3/{token}/{method}", self._handle)
        self.app.router.add_route("POST", "/upload/{upload_id}", self._handle_upload)

    def set_response(self, name: str, builder: Callable[[Any], Any]) -> None:
        self.responses[name] = builder

    def set_raw_envelope(self, name: str, envelope: Any) -> None:
        self.raw_envelopes[name] = envelope

    async def _handle(self, request: web.Request) -> web.Response:
        method = request.match_info["method"]
        raw = await request.read()
        body: Any = orjson.loads(raw) if raw else {}
        self.request_log.append({"method": method, "body": body})
        if method in self.raw_envelopes:
            return web.json_response(self.raw_envelopes[method])
        builder = self.responses.get(method)
        result = builder(body) if builder else None
        return web.json_response({"status": "OK", "data": result})

    async def _handle_upload(self, request: web.Request) -> web.Response:
        reader = await request.multipart()
        file_bytes = b""
        async for part in reader:
            if part.name == "file":
                file_bytes = await part.read(decode=False)
        self.request_log.append({"method": "_UPLOAD", "bytes_len": len(file_bytes)})
        return web.json_response({"file_id": "uploaded_file_id_123"})

    def calls_for(self, name: str) -> list[Dict[str, Any]]:
        return [c for c in self.request_log if c["method"] == name]


@pytest.fixture
async def fake_server():
    server = FakeRubikaServer()
    async with TestServer(server.app) as ts:
        base_url = str(ts.make_url("")).rstrip("/") + "/v3"
        upload_base = str(ts.make_url("")).rstrip("/") + "/upload"
        yield server, base_url, upload_base


def _client(base_url: str) -> RubikaClient:
    return RubikaClient(
        TOKEN,
        base_url=base_url,
        retry_policy=RetryPolicy(max_attempts=3, base_backoff_seconds=0.001),
    )


# -- getMe -------------------------------------------------------------------


async def test_get_me(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response(
        "getMe",
        lambda body: {"bot": {"bot_id": "b1", "bot_title": "T", "username": "u"}},
    )
    client = _client(base_url)
    try:
        bot = await client.get_me()
    finally:
        await client.close()
    assert isinstance(bot, Bot)
    assert bot.bot_id == "b1"
    assert bot.username == "u"


# -- sendMessage -------------------------------------------------------------


async def test_send_message_minimal(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response("sendMessage", lambda body: {"message_id": "m1"})
    client = _client(base_url)
    try:
        msg = await client.send_message("c1", "hello")
    finally:
        await client.close()
    assert isinstance(msg, Message)
    assert msg.message_id == "m1"
    assert server.calls_for("sendMessage")[0]["body"] == {
        "chat_id": "c1", "text": "hello"
    }


async def test_send_message_with_metadata_and_keypads(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response("sendMessage", lambda body: {"message_id": "m2"})
    client = _client(base_url)
    try:
        md = Metadata(
            meta_data_parts=[MetadataPart(type="Bold", from_index=0, length=4)]
        )
        kp = Keypad(
            rows=[KeypadRow(buttons=[Button(id="b1", type="Simple", button_text="A")])],
            resize_keyboard=True,
        )
        await client.send_message(
            "c1", "Hello!",
            metadata=md,
            inline_keypad=kp,
            reply_to_message_id="m0",
            disable_notification=True,
        )
    finally:
        await client.close()
    body = server.calls_for("sendMessage")[0]["body"]
    assert body["metadata"]["meta_data_parts"][0]["type"] == "Bold"
    assert body["inline_keypad"]["rows"][0]["buttons"][0]["id"] == "b1"
    assert body["reply_to_message_id"] == "m0"
    assert body["disable_notification"] is True


# -- sendPoll / sendLocation / sendContact -----------------------------------


async def test_send_poll(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response("sendPoll", lambda body: {"message_id": "p1"})
    client = _client(base_url)
    try:
        msg = await client.send_poll("c1", "Yes?", ["yes", "no"])
    finally:
        await client.close()
    assert msg.message_id == "p1"
    assert server.calls_for("sendPoll")[0]["body"] == {
        "chat_id": "c1", "question": "Yes?", "options": ["yes", "no"]
    }


async def test_send_location(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response("sendLocation", lambda body: {"message_id": "l1"})
    client = _client(base_url)
    try:
        await client.send_location("c1", "35.7", "51.4")
    finally:
        await client.close()
    body = server.calls_for("sendLocation")[0]["body"]
    assert body == {"chat_id": "c1", "latitude": "35.7", "longitude": "51.4"}


async def test_send_contact(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response("sendContact", lambda body: {"message_id": "ct1"})
    client = _client(base_url)
    try:
        await client.send_contact("c1", "Ali", "R", "+98912")
    finally:
        await client.close()
    body = server.calls_for("sendContact")[0]["body"]
    assert body["first_name"] == "Ali"
    assert body["last_name"] == "R"
    assert body["phone_number"] == "+98912"


# -- getChat -----------------------------------------------------------------


async def test_get_chat(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response(
        "getChat", lambda body: {"chat": {"chat_id": "c1", "chat_type": "Group", "title": "T"}}
    )
    client = _client(base_url)
    try:
        chat = await client.get_chat("c1")
    finally:
        await client.close()
    assert isinstance(chat, Chat)
    assert chat.title == "T"


# -- getUpdates --------------------------------------------------------------


async def test_get_updates_with_offset_and_limit(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response(
        "getUpdates",
        lambda body: {
            "updates": [
                {"type": "NewMessage", "chat_id": "c1", "new_message": {"message_id": "m1"}}
            ],
            "next_offset_id": "10",
        },
    )
    client = _client(base_url)
    try:
        updates, next_id = await client.get_updates(offset_id="5", limit=10)
    finally:
        await client.close()
    assert len(updates) == 1
    assert updates[0].new_message.message_id == "m1"
    assert next_id == "10"
    assert server.calls_for("getUpdates")[0]["body"] == {"offset_id": "5", "limit": 10}


async def test_get_updates_no_args(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response("getUpdates", lambda body: {"updates": [], "next_offset_id": None})
    client = _client(base_url)
    try:
        updates, next_id = await client.get_updates()
    finally:
        await client.close()
    assert updates == []
    assert next_id is None
    assert server.calls_for("getUpdates")[0]["body"] == {}


# -- forwardMessage ----------------------------------------------------------


async def test_forward_message(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response("forwardMessage", lambda body: {"new_message_id": "nm1"})
    client = _client(base_url)
    try:
        new_id = await client.forward_message("from_c", "m1", "to_c")
    finally:
        await client.close()
    assert new_id == "nm1"
    body = server.calls_for("forwardMessage")[0]["body"]
    assert body == {"from_chat_id": "from_c", "message_id": "m1", "to_chat_id": "to_c"}


# -- edit / delete -----------------------------------------------------------


async def test_edit_message_text(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response("editMessageText", lambda body: None)
    client = _client(base_url)
    try:
        ok = await client.edit_message_text("c1", "m1", "new")
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("editMessageText")[0]["body"]
    assert body == {"chat_id": "c1", "message_id": "m1", "text": "new"}


async def test_delete_message(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response("deleteMessage", lambda body: None)
    client = _client(base_url)
    try:
        ok = await client.delete_message("c1", "m1")
    finally:
        await client.close()
    assert ok is True


# -- editMessageKeypad (URL: editInlineKeypad) --------------------------------


async def test_edit_message_keypad(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response("editInlineKeypad", lambda body: None)
    client = _client(base_url)
    try:
        kp = Keypad(
            rows=[KeypadRow(buttons=[Button(id="b1", type="Simple", button_text="X")])]
        )
        ok = await client.edit_message_keypad("c1", "m1", kp)
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("editInlineKeypad")[0]["body"]
    assert body["inline_keypad"]["rows"][0]["buttons"][0]["id"] == "b1"


# -- setCommands -------------------------------------------------------------


async def test_set_commands(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response("setCommands", lambda body: None)
    client = _client(base_url)
    try:
        ok = await client.set_commands(
            [BotCommand(command="start", description="Start")]
        )
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("setCommands")[0]["body"]
    assert body == {"bot_commands": [{"command": "start", "description": "Start"}]}


# -- updateBotEndpoints ------------------------------------------------------


async def test_update_bot_endpoints(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response("updateBotEndpoints", lambda body: None)
    client = _client(base_url)
    try:
        ok = await client.update_bot_endpoints(
            "https://example.com/hook",
            type=UpdateEndpointTypeEnum.RECEIVE_UPDATE,
        )
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("updateBotEndpoints")[0]["body"]
    assert body == {"url": "https://example.com/hook", "type": "ReceiveUpdate"}


# -- editChatKeypad ----------------------------------------------------------


async def test_edit_chat_keypad_new(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response("editChatKeypad", lambda body: None)
    client = _client(base_url)
    try:
        kp = Keypad(
            rows=[KeypadRow(buttons=[Button(id="b1", type="Simple", button_text="A")])]
        )
        ok = await client.edit_chat_keypad("c1", kp, chat_keypad_type=ChatKeypadTypeEnum.NEW)
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("editChatKeypad")[0]["body"]
    assert body["chat_keypad_type"] == "New"
    assert body["chat_keypad"]["rows"][0]["buttons"][0]["id"] == "b1"


async def test_remove_chat_keypad(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response("editChatKeypad", lambda body: None)
    client = _client(base_url)
    try:
        ok = await client.remove_chat_keypad("c1")
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("editChatKeypad")[0]["body"]
    assert body == {"chat_id": "c1", "chat_keypad_type": "Remove"}


# -- getFile / sendFile / upload flow ---------------------------------------


async def test_get_file(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response(
        "getFile", lambda body: {"download_url": "https://cdn.example.com/f1"}
    )
    client = _client(base_url)
    try:
        url = await client.get_file("f1")
    finally:
        await client.close()
    assert url == "https://cdn.example.com/f1"


async def test_send_file(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response("sendFile", lambda body: {"message_id": "fm1"})
    client = _client(base_url)
    try:
        msg = await client.send_file("c1", "fid1", text="caption")
    finally:
        await client.close()
    assert msg.message_id == "fm1"
    body = server.calls_for("sendFile")[0]["body"]
    assert body == {"chat_id": "c1", "file_id": "fid1", "text": "caption"}


async def test_request_send_file(fake_server) -> None:
    server, base_url, upload_base = fake_server
    server.set_response(
        "requestSendFile",
        lambda body: {"upload_url": f"{upload_base}/abc"},
    )
    client = _client(base_url)
    try:
        url = await client.request_send_file(type=FileTypeEnum.IMAGE)
    finally:
        await client.close()
    assert url.endswith("/abc")
    body = server.calls_for("requestSendFile")[0]["body"]
    assert body == {"type": "Image"}


async def test_upload_and_send_file(fake_server) -> None:
    server, base_url, upload_base = fake_server
    server.set_response(
        "requestSendFile",
        lambda body: {"upload_url": f"{upload_base}/xyz"},
    )
    server.set_response("sendFile", lambda body: {"message_id": "final_m1"})
    client = _client(base_url)
    try:
        msg = await client.upload_and_send_file(
            "c1", b"some-bytes",
            file_type=FileTypeEnum.IMAGE,
            filename="p.jpg",
            content_type="image/jpeg",
            text="look",
        )
    finally:
        await client.close()
    assert msg.message_id == "final_m1"
    # Verify the multipart upload saw our bytes
    upload_calls = [c for c in server.request_log if c["method"] == "_UPLOAD"]
    assert len(upload_calls) == 1
    assert upload_calls[0]["bytes_len"] == len(b"some-bytes")
    # And the final sendFile used the returned file_id
    send_body = server.calls_for("sendFile")[0]["body"]
    assert send_body["file_id"] == "uploaded_file_id_123"


# -- ban / unban -------------------------------------------------------------


async def test_ban_chat_member(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response("banChatMember", lambda body: None)
    client = _client(base_url)
    try:
        ok = await client.ban_chat_member("c1", "u42")
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("banChatMember")[0]["body"]
    assert body == {"chat_id": "c1", "user_id": "u42"}


async def test_unban_chat_member(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_response("unbanChatMember", lambda body: None)
    client = _client(base_url)
    try:
        ok = await client.unban_chat_member("c1", "u42")
    finally:
        await client.close()
    assert ok is True


# -- Error envelope ----------------------------------------------------------


async def test_error_envelope_raises_no_retry(fake_server) -> None:
    server, base_url, _ = fake_server
    server.set_raw_envelope(
        "getMe",
        {
            "status": "error",
            "error_code": "INVALID_TOKEN",
            "error_message": "Bad token",
        },
    )
    client = _client(base_url)
    try:
        with pytest.raises(RubikaAPIError) as exc_info:
            await client.get_me()
    finally:
        await client.close()
    assert exc_info.value.error_code == "INVALID_TOKEN"
    assert exc_info.value.error_message == "Bad token"
    # Application errors never retried.
    assert len(server.calls_for("getMe")) == 1