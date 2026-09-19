"""Tests for T18: Final Completeness Sweep.

Tests for the methods and types added during the T18 completeness audit.
"""

from __future__ import annotations

from typing import Any, Callable, Dict

import orjson
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms.telegram.client import TelegramClient
from peyk.platforms.telegram.models import (
    BotSubscriptionUpdated,
    Message,
    Update,
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
        self.app.router.add_route("POST", "/bot{token}/{method}", self._handle)

    def set_response(
        self, method_name: str, result_builder: Callable[[Any], Any]
    ) -> None:
        self.responses[method_name] = result_builder

    def set_raw_envelope(self, method_name: str, envelope: Any) -> None:
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
    return TelegramClient(
        TOKEN,
        base_url=base_url,
        retry_policy=RetryPolicy(max_attempts=3, base_backoff_seconds=0.001),
    )


# ---------------------------------------------------------------------------
# T18 client method tests
# ---------------------------------------------------------------------------


async def test_answer_guest_query(fake_server) -> None:
    """answerGuestQuery sends correct payload."""
    server, test_server = fake_server
    server.set_response(
        "answerGuestQuery",
        lambda body: {"chat_id": 200, "message_id": 42},
    )

    client = _client_for(test_server, server)
    try:
        result = await client.answer_guest_query(
            guest_query_id="gq-123",
            result={"type": "article", "id": "1", "title": "Test", "input_message_content": {"message_text": "Hello"}},
        )
    finally:
        await client.close()

    assert result is not None
    calls = server.calls_for("answerGuestQuery")
    assert len(calls) == 1
    assert calls[0]["body"]["guest_query_id"] == "gq-123"


async def test_delete_all_message_reactions(fake_server) -> None:
    """deleteAllMessageReactions sends correct payload."""
    server, test_server = fake_server
    server.set_response("deleteAllMessageReactions", lambda body: True)

    client = _client_for(test_server, server)
    try:
        ok = await client.delete_all_message_reactions(chat_id=200, message_id=10)
    finally:
        await client.close()

    assert ok is True
    calls = server.calls_for("deleteAllMessageReactions")
    assert len(calls) == 1
    assert calls[0]["body"]["chat_id"] == 200
    assert calls[0]["body"]["message_id"] == 10


async def test_delete_message_reaction(fake_server) -> None:
    """deleteMessageReaction sends correct payload."""
    server, test_server = fake_server
    server.set_response("deleteMessageReaction", lambda body: True)

    client = _client_for(test_server, server)
    try:
        ok = await client.delete_message_reaction(chat_id=200, message_id=10)
    finally:
        await client.close()

    assert ok is True
    calls = server.calls_for("deleteMessageReaction")
    assert len(calls) == 1


async def test_delete_ephemeral_message(fake_server) -> None:
    """deleteEphemeralMessage sends correct payload."""
    server, test_server = fake_server
    server.set_response("deleteEphemeralMessage", lambda body: True)

    client = _client_for(test_server, server)
    try:
        ok = await client.delete_ephemeral_message(chat_id=200, ephemeral_message_id=555)
    finally:
        await client.close()

    assert ok is True
    calls = server.calls_for("deleteEphemeralMessage")
    assert len(calls) == 1
    assert calls[0]["body"]["ephemeral_message_id"] == 555


async def test_edit_ephemeral_message_text(fake_server) -> None:
    """editEphemeralMessageText sends correct payload."""
    server, test_server = fake_server
    server.set_response("editEphemeralMessageText", lambda body: _sample_message_raw(42))

    client = _client_for(test_server, server)
    try:
        result = await client.edit_ephemeral_message_text(
            chat_id=200, ephemeral_message_id=555, text="Updated text"
        )
    finally:
        await client.close()

    assert result.message_id == 42
    calls = server.calls_for("editEphemeralMessageText")
    assert len(calls) == 1
    assert calls[0]["body"]["text"] == "Updated text"


async def test_edit_ephemeral_message_media(fake_server) -> None:
    """editEphemeralMessageMedia sends correct payload."""
    server, test_server = fake_server
    server.set_response("editEphemeralMessageMedia", lambda body: _sample_message_raw(43))

    client = _client_for(test_server, server)
    try:
        result = await client.edit_ephemeral_message_media(
            chat_id=200, ephemeral_message_id=555, media={"type": "photo", "media": "file_id"}
        )
    finally:
        await client.close()

    assert result.message_id == 43


async def test_edit_ephemeral_message_caption(fake_server) -> None:
    """editEphemeralMessageCaption sends correct payload."""
    server, test_server = fake_server
    server.set_response("editEphemeralMessageCaption", lambda body: _sample_message_raw(44))

    client = _client_for(test_server, server)
    try:
        result = await client.edit_ephemeral_message_caption(
            chat_id=200, ephemeral_message_id=555, caption="New caption"
        )
    finally:
        await client.close()

    assert result.message_id == 44


async def test_edit_ephemeral_message_reply_markup(fake_server) -> None:
    """editEphemeralMessageReplyMarkup sends correct payload."""
    server, test_server = fake_server
    server.set_response("editEphemeralMessageReplyMarkup", lambda body: True)

    client = _client_for(test_server, server)
    try:
        ok = await client.edit_ephemeral_message_reply_markup(
            chat_id=200, ephemeral_message_id=555, reply_markup={"inline_keyboard": []}
        )
    finally:
        await client.close()

    assert ok is True


async def test_send_message_draft(fake_server) -> None:
    """sendMessageDraft sends correct payload."""
    server, test_server = fake_server
    server.set_response("sendMessageDraft", lambda body: _sample_message_raw(50))

    client = _client_for(test_server, server)
    try:
        result = await client.send_message_draft(chat_id=200, text="Draft text")
    finally:
        await client.close()

    assert result.message_id == 50


async def test_send_rich_message_draft(fake_server) -> None:
    """sendRichMessageDraft sends correct payload."""
    server, test_server = fake_server
    server.set_response("sendRichMessageDraft", lambda body: _sample_message_raw(51))

    client = _client_for(test_server, server)
    try:
        result = await client.send_rich_message_draft(chat_id=200, text="Draft rich")
    finally:
        await client.close()

    assert result.message_id == 51


async def test_answer_chat_join_request_query(fake_server) -> None:
    """answerChatJoinRequestQuery sends correct payload."""
    server, test_server = fake_server
    server.set_response("answerChatJoinRequestQuery", lambda body: True)

    client = _client_for(test_server, server)
    try:
        ok = await client.answer_chat_join_request_query(
            chat_id=200, user_id=300, query_id="qr-1"
        )
    finally:
        await client.close()

    assert ok is True


async def test_send_chat_join_request_web_app(fake_server) -> None:
    """sendChatJoinRequestWebApp sends correct payload."""
    server, test_server = fake_server
    server.set_response("sendChatJoinRequestWebApp", lambda body: True)

    client = _client_for(test_server, server)
    try:
        ok = await client.send_chat_join_request_web_app(
            chat_id=200, user_id=300, query_id="qr-1"
        )
    finally:
        await client.close()

    assert ok is True


async def test_get_managed_bot_access_settings(fake_server) -> None:
    """getManagedBotAccessSettings sends correct payload."""
    server, test_server = fake_server
    server.set_response("getManagedBotAccessSettings", lambda body: {"can_send_messages": True})

    client = _client_for(test_server, server)
    try:
        result = await client.get_managed_bot_access_settings(chat_id=200)
    finally:
        await client.close()

    assert result is not None


async def test_set_managed_bot_access_settings(fake_server) -> None:
    """setManagedBotAccessSettings sends correct payload."""
    server, test_server = fake_server
    server.set_response("setManagedBotAccessSettings", lambda body: True)

    client = _client_for(test_server, server)
    try:
        ok = await client.set_managed_bot_access_settings(chat_id=200)
    finally:
        await client.close()

    assert ok is True


async def test_get_user_personal_chat_messages(fake_server) -> None:
    """getUserPersonalChatMessages sends correct payload."""
    server, test_server = fake_server
    server.set_response("getUserPersonalChatMessages", lambda body: {"total_count": 0})

    client = _client_for(test_server, server)
    try:
        result = await client.get_user_personal_chat_messages(user_id=100)
    finally:
        await client.close()

    assert result is not None


# ---------------------------------------------------------------------------
# T18 model tests: Update.subscription field
# ---------------------------------------------------------------------------


def test_update_subscription_field() -> None:
    """Update parses subscription field."""
    raw = {
        "update_id": 1,
        "subscription": {"subscription": {"is_premium": True}},
    }
    result = Update.from_dict(raw)
    assert result is not None
    assert result.subscription is not None
    assert result.subscription.subscription is not None


def test_update_subscription_none() -> None:
    """Update handles absent subscription."""
    raw = {"update_id": 2}
    result = Update.from_dict(raw)
    assert result is not None
    assert result.subscription is None


# ---------------------------------------------------------------------------
# T18 model tests: Message new fields
# ---------------------------------------------------------------------------


def test_message_sender_tag() -> None:
    """Message parses sender_tag field."""
    msg_raw = _sample_message_raw(1)
    msg_raw["sender_tag"] = "admin"
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.sender_tag == "admin"


def test_message_edit_date() -> None:
    """Message parses edit_date field."""
    msg_raw = _sample_message_raw(1)
    msg_raw["edit_date"] = 1690005000
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.edit_date == 1690005000


def test_message_has_protected_content() -> None:
    """Message parses has_protected_content field."""
    msg_raw = _sample_message_raw(1)
    msg_raw["has_protected_content"] = True
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.has_protected_content is True


def test_message_is_from_offline() -> None:
    """Message parses is_from_offline field."""
    msg_raw = _sample_message_raw(1)
    msg_raw["is_from_offline"] = True
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.is_from_offline is True


def test_message_is_paid_post() -> None:
    """Message parses is_paid_post field."""
    msg_raw = _sample_message_raw(1)
    msg_raw["is_paid_post"] = True
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.is_paid_post is True


def test_message_media_group_id() -> None:
    """Message parses media_group_id field."""
    msg_raw = _sample_message_raw(1)
    msg_raw["media_group_id"] = "group-123"
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.media_group_id == "group-123"


def test_message_direct_messages_topic_passthrough() -> None:
    """Message preserves direct_messages_topic as passthrough."""
    msg_raw = _sample_message_raw(1)
    msg_raw["direct_messages_topic"] = {"id": 1, "title": "DM"}
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.direct_messages_topic is not None
    assert result.direct_messages_topic["id"] == 1


def test_message_chat_owner_left_passthrough() -> None:
    """Message preserves chat_owner_left as passthrough."""
    msg_raw = _sample_message_raw(1)
    msg_raw["chat_owner_left"] = {"from": SAMPLE_USER_RAW}
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.chat_owner_left is not None


def test_message_chat_owner_changed_passthrough() -> None:
    """Message preserves chat_owner_changed as passthrough."""
    msg_raw = _sample_message_raw(1)
    msg_raw["chat_owner_changed"] = {"from": SAMPLE_USER_RAW}
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.chat_owner_changed is not None


# ---------------------------------------------------------------------------
# BotSubscriptionUpdated model tests
# ---------------------------------------------------------------------------


def test_bot_subscription_updated_parsing() -> None:
    """BotSubscriptionUpdated parses correctly."""
    raw = {"subscription": {"is_premium": True}}
    result = BotSubscriptionUpdated.from_dict(raw)
    assert result is not None
    assert result.subscription is not None


def test_bot_subscription_updated_none() -> None:
    """BotSubscriptionUpdated handles None."""
    assert BotSubscriptionUpdated.from_dict(None) is None


def test_bot_subscription_updated_defaults() -> None:
    """BotSubscriptionUpdated uses correct defaults."""
    result = BotSubscriptionUpdated.from_dict({})
    assert result is not None
    assert result.subscription is None
