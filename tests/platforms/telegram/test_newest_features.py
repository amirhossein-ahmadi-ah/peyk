"""Tests for T17: Newest Bot API Features (Rich Messages, Communities, Guest Mode).

Uses the same FakeTelegramServer pattern from test_client.py.

Covers:
- RichMessage / InputRichMessage / InputRichMessageContent models
- send_rich_message client method
- Community / CommunityChatAdded / CommunityChatRemoved / CommunityChatJoined models
- SentGuestMessage model
- MessageGenerationStopped model
- New optional fields on Message, Update, ChatFullInfo, User
"""

from __future__ import annotations

from typing import Any, Callable, Dict

import orjson
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms.telegram.client import TelegramClient
from peyk.platforms.telegram.models import (
    Community,
    CommunityChatAdded,
    CommunityChatJoined,
    CommunityChatRemoved,
    InputRichMessage,
    InputRichMessageContent,
    Message,
    MessageGenerationStopped,
    RichMessage,
    SentGuestMessage,
    User,
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
# T17 client method tests: send_rich_message
# ---------------------------------------------------------------------------


async def test_send_rich_message_basic(fake_server) -> None:
    """Happy path: sendRichMessage sends correct payload with text only."""
    server, test_server = fake_server
    server.set_response(
        "sendRichMessage",
        lambda body: _sample_message_raw(42),
    )

    client = _client_for(test_server, server)
    try:
        result = await client.send_rich_message(
            chat_id=200,
            text="Hello rich world!",
        )
    finally:
        await client.close()

    assert result.message_id == 42
    assert result.text == "hello"

    calls = server.calls_for("sendRichMessage")
    assert len(calls) == 1
    body = calls[0]["body"]
    assert body["chat_id"] == 200
    assert body["text"] == "Hello rich world!"


async def test_send_rich_message_with_blocks(fake_server) -> None:
    """sendRichMessage sends blocks and media when provided."""
    server, test_server = fake_server
    server.set_response(
        "sendRichMessage",
        lambda body: _sample_message_raw(43),
    )

    client = _client_for(test_server, server)
    try:
        result = await client.send_rich_message(
            chat_id=200,
            text="Check this out",
            blocks=[{"type": "paragraph", "text": "block content"}],
            media="file_id_123",
        )
    finally:
        await client.close()

    assert result.message_id == 43

    calls = server.calls_for("sendRichMessage")
    assert len(calls) == 1
    body = calls[0]["body"]
    assert body["text"] == "Check this out"
    assert body["blocks"] == [{"type": "paragraph", "text": "block content"}]
    assert body["media"] == "file_id_123"


async def test_send_rich_message_with_parse_mode(fake_server) -> None:
    """sendRichMessage sends parse_mode when provided."""
    server, test_server = fake_server
    server.set_response(
        "sendRichMessage",
        lambda body: _sample_message_raw(44),
    )

    client = _client_for(test_server, server)
    try:
        await client.send_rich_message(
            chat_id=200,
            text="**bold text**",
            parse_mode="Markdown",
        )
    finally:
        await client.close()

    calls = server.calls_for("sendRichMessage")
    assert calls[0]["body"]["parse_mode"] == "Markdown"


# ---------------------------------------------------------------------------
# RichMessage model tests
# ---------------------------------------------------------------------------


def test_rich_message_parsing() -> None:
    """RichMessage model parses correctly."""
    raw = {"text": "Hello rich world!"}
    result = RichMessage.from_dict(raw)
    assert result is not None
    assert result.text == "Hello rich world!"


def test_rich_message_none() -> None:
    """RichMessage handles None input."""
    assert RichMessage.from_dict(None) is None


def test_rich_message_defaults() -> None:
    """RichMessage uses correct defaults."""
    raw = {}
    result = RichMessage.from_dict(raw)
    assert result is not None
    assert result.text == ""


# ---------------------------------------------------------------------------
# InputRichMessage / InputRichMessageContent tests
# ---------------------------------------------------------------------------


def test_input_rich_message_serialization() -> None:
    """InputRichMessage serializes correctly."""
    msg = InputRichMessage(
        text="Rich content",
        parse_mode="HTML",
        blocks=[{"type": "paragraph", "text": "test"}],
        media="file_id",
    )
    result = msg.to_dict()
    assert result["text"] == "Rich content"
    assert result["parse_mode"] == "HTML"
    assert result["blocks"] == [{"type": "paragraph", "text": "test"}]
    assert result["media"] == "file_id"


def test_input_rich_message_minimal() -> None:
    """InputRichMessage serializes with just text."""
    msg = InputRichMessage(text="Minimal")
    result = msg.to_dict()
    assert result["text"] == "Minimal"
    assert "parse_mode" not in result
    assert "blocks" not in result
    assert "media" not in result


def test_input_rich_message_content_with_message() -> None:
    """InputRichMessageContent with InputRichMessage serializes correctly."""
    content = InputRichMessageContent(
        rich_message=InputRichMessage(text="Inner rich")
    )
    result = content.to_dict()
    assert result["text"] == "Inner rich"


def test_input_rich_message_content_empty() -> None:
    """InputRichMessageContent with no message returns empty dict."""
    content = InputRichMessageContent()
    result = content.to_dict()
    assert result == {}


# ---------------------------------------------------------------------------
# Community model tests
# ---------------------------------------------------------------------------


def test_community_parsing() -> None:
    """Community model parses correctly."""
    raw = {
        "id": 42,
        "title": "My Community",
        "bot": SAMPLE_USER_RAW,
    }
    result = Community.from_dict(raw)
    assert result is not None
    assert result.id == 42
    assert result.title == "My Community"
    assert result.bot is not None
    assert result.bot.id == 100
    assert result.bot.first_name == "TestBot"


def test_community_none() -> None:
    """Community handles None input."""
    assert Community.from_dict(None) is None


def test_community_defaults() -> None:
    """Community uses correct defaults."""
    raw = {}
    result = Community.from_dict(raw)
    assert result is not None
    assert result.id == 0
    assert result.title == ""
    assert result.bot is None


def test_community_without_bot() -> None:
    """Community can parse without a bot field."""
    raw = {"id": 99, "title": "Test Community"}
    result = Community.from_dict(raw)
    assert result is not None
    assert result.id == 99
    assert result.title == "Test Community"
    assert result.bot is None


# ---------------------------------------------------------------------------
# CommunityChatAdded / Removed / Joined tests
# ---------------------------------------------------------------------------


def test_community_chat_added_parsing() -> None:
    """CommunityChatAdded parses correctly."""
    raw = {"chat_id": 12345}
    result = CommunityChatAdded.from_dict(raw)
    assert result is not None
    assert result.chat_id == 12345


def test_community_chat_added_none() -> None:
    """CommunityChatAdded handles None."""
    assert CommunityChatAdded.from_dict(None) is None


def test_community_chat_added_defaults() -> None:
    """CommunityChatAdded uses correct defaults."""
    result = CommunityChatAdded.from_dict({})
    assert result is not None
    assert result.chat_id == 0


def test_community_chat_removed_parsing() -> None:
    """CommunityChatRemoved parses correctly."""
    raw = {"chat_id": 67890}
    result = CommunityChatRemoved.from_dict(raw)
    assert result is not None
    assert result.chat_id == 67890


def test_community_chat_removed_none() -> None:
    """CommunityChatRemoved handles None."""
    assert CommunityChatRemoved.from_dict(None) is None


def test_community_chat_joined_parsing() -> None:
    """CommunityChatJoined parses correctly."""
    raw = {"chat_id": 11111}
    result = CommunityChatJoined.from_dict(raw)
    assert result is not None
    assert result.chat_id == 11111


def test_community_chat_joined_none() -> None:
    """CommunityChatJoined handles None."""
    assert CommunityChatJoined.from_dict(None) is None


# ---------------------------------------------------------------------------
# SentGuestMessage tests
# ---------------------------------------------------------------------------


def test_sent_guest_message_parsing() -> None:
    """SentGuestMessage parses correctly."""
    raw = {
        "chat_id": 200,
        "message_id": 999,
    }
    result = SentGuestMessage.from_dict(raw)
    assert result is not None
    assert result.chat_id == 200
    assert result.message_id == 999


def test_sent_guest_message_none() -> None:
    """SentGuestMessage handles None input."""
    assert SentGuestMessage.from_dict(None) is None


def test_sent_guest_message_defaults() -> None:
    """SentGuestMessage uses correct defaults."""
    raw = {}
    result = SentGuestMessage.from_dict(raw)
    assert result is not None
    assert result.chat_id == 0
    assert result.message_id is None


# ---------------------------------------------------------------------------
# MessageGenerationStopped tests
# ---------------------------------------------------------------------------


def test_message_generation_stopped_parsing() -> None:
    """MessageGenerationStopped parses correctly."""
    raw = {
        "chat_id": 200,
        "message_id": 50,
        "message_thread_id": 10,
    }
    result = MessageGenerationStopped.from_dict(raw)
    assert result is not None
    assert result.chat_id == 200
    assert result.message_id == 50
    assert result.message_thread_id == 10


def test_message_generation_stopped_none() -> None:
    """MessageGenerationStopped handles None input."""
    assert MessageGenerationStopped.from_dict(None) is None


def test_message_generation_stopped_defaults() -> None:
    """MessageGenerationStopped uses correct defaults."""
    raw = {}
    result = MessageGenerationStopped.from_dict(raw)
    assert result is not None
    assert result.chat_id == 0
    assert result.message_id is None
    assert result.message_thread_id is None


# ---------------------------------------------------------------------------
# New Message field tests (receiver_user, ephemeral_message_id, guest_*, community_*, etc.)
# ---------------------------------------------------------------------------


def test_message_receiver_user() -> None:
    """Message parses receiver_user field."""
    msg_raw = _sample_message_raw(1)
    msg_raw["receiver_user"] = SAMPLE_USER_RAW
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.receiver_user is not None
    assert result.receiver_user.id == 100


def test_message_ephemeral_message_id() -> None:
    """Message parses ephemeral_message_id field."""
    msg_raw = _sample_message_raw(1)
    msg_raw["ephemeral_message_id"] = 555
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.ephemeral_message_id == 555


def test_message_guest_bot_caller_user() -> None:
    """Message parses guest_bot_caller_user field."""
    msg_raw = _sample_message_raw(1)
    msg_raw["guest_bot_caller_user"] = {"id": 999, "is_bot": False, "first_name": "Guest"}
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.guest_bot_caller_user is not None
    assert result.guest_bot_caller_user.id == 999


def test_message_guest_bot_caller_chat() -> None:
    """Message parses guest_bot_caller_chat field."""
    msg_raw = _sample_message_raw(1)
    msg_raw["guest_bot_caller_chat"] = SAMPLE_CHAT_RAW
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.guest_bot_caller_chat is not None
    assert result.guest_bot_caller_chat.id == 200


def test_message_guest_query_id() -> None:
    """Message parses guest_query_id field."""
    msg_raw = _sample_message_raw(1)
    msg_raw["guest_query_id"] = "gq-12345"
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.guest_query_id == "gq-12345"


def test_message_community_chat_joined() -> None:
    """Message parses community_chat_joined field."""
    msg_raw = _sample_message_raw(1)
    msg_raw["community_chat_joined"] = {"chat_id": 777}
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.community_chat_joined is not None
    assert result.community_chat_joined.chat_id == 777


def test_message_community_chat_added() -> None:
    """Message parses community_chat_added field."""
    msg_raw = _sample_message_raw(1)
    msg_raw["community_chat_added"] = {"chat_id": 888}
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.community_chat_added is not None
    assert result.community_chat_added.chat_id == 888


def test_message_community_chat_removed() -> None:
    """Message parses community_chat_removed field."""
    msg_raw = _sample_message_raw(1)
    msg_raw["community_chat_removed"] = {"chat_id": 999}
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.community_chat_removed is not None
    assert result.community_chat_removed.chat_id == 999


def test_message_rich_message_passthrough() -> None:
    """Message preserves rich_message field as passthrough."""
    msg_raw = _sample_message_raw(1)
    msg_raw["rich_message"] = {"text": "Rich text", "blocks": []}
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.rich_message is not None
    assert result.rich_message["text"] == "Rich text"


def test_message_checklist_passthrough() -> None:
    """Message preserves checklist field as passthrough."""
    msg_raw = _sample_message_raw(1)
    msg_raw["checklist"] = {"title": "My Checklist", "tasks": []}
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.checklist is not None
    assert result.checklist["title"] == "My Checklist"


def test_message_suggested_post_info_passthrough() -> None:
    """Message preserves suggested_post_info field as passthrough."""
    msg_raw = _sample_message_raw(1)
    msg_raw["suggested_post_info"] = {"price": 100, "date": "2026-09-17T12:00:00Z"}
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.suggested_post_info is not None
    assert result.suggested_post_info["price"] == 100


def test_message_paid_star_count() -> None:
    """Message parses paid_star_count field."""
    msg_raw = _sample_message_raw(1)
    msg_raw["paid_star_count"] = 500
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.paid_star_count == 500


# ---------------------------------------------------------------------------
# New Update field tests (guest_message, managed_bot, stopped_message_generation)
# ---------------------------------------------------------------------------


def test_update_guest_message() -> None:
    """Update parses guest_message field."""
    raw = {
        "update_id": 1,
        "guest_message": _sample_message_raw(1),
    }
    from peyk.platforms.telegram.models import Update
    result = Update.from_dict(raw)
    assert result is not None
    assert result.update_id == 1
    assert result.guest_message is not None
    assert result.guest_message.message_id == 1


def test_update_managed_bot_passthrough() -> None:
    """Update preserves managed_bot field as passthrough."""
    raw = {
        "update_id": 2,
        "managed_bot": {"id": "bot-123", "name": "Managed Bot"},
    }
    from peyk.platforms.telegram.models import Update
    result = Update.from_dict(raw)
    assert result is not None
    assert result.managed_bot is not None
    assert result.managed_bot["id"] == "bot-123"


def test_update_stopped_message_generation() -> None:
    """Update parses stopped_message_generation field."""
    raw = {
        "update_id": 3,
        "stopped_message_generation": {
            "chat_id": 200,
            "message_id": 50,
            "message_thread_id": 10,
        },
    }
    from peyk.platforms.telegram.models import Update
    result = Update.from_dict(raw)
    assert result is not None
    assert result.stopped_message_generation is not None
    assert result.stopped_message_generation.chat_id == 200
    assert result.stopped_message_generation.message_id == 50
    assert result.stopped_message_generation.message_thread_id == 10


# ---------------------------------------------------------------------------
# New ChatFullInfo field tests (guard_bot, community)
# ---------------------------------------------------------------------------


def test_chat_full_info_guard_bot() -> None:
    """ChatFullInfo parses guard_bot field."""
    raw = {
        "id": 200,
        "type": "supergroup",
        "title": "Test Group",
        "guard_bot": SAMPLE_USER_RAW,
    }
    from peyk.platforms.telegram.models import ChatFullInfo
    result = ChatFullInfo.from_dict(raw)
    assert result is not None
    assert result.guard_bot is not None
    assert result.guard_bot.id == 100
    assert result.guard_bot.first_name == "TestBot"


def test_chat_full_info_community() -> None:
    """ChatFullInfo parses community field."""
    raw = {
        "id": 200,
        "type": "supergroup",
        "title": "Test Group",
        "community": {"id": 42, "title": "My Community", "bot": SAMPLE_USER_RAW},
    }
    from peyk.platforms.telegram.models import ChatFullInfo
    result = ChatFullInfo.from_dict(raw)
    assert result is not None
    assert result.community is not None
    assert result.community.id == 42
    assert result.community.title == "My Community"
    assert result.community.bot is not None


# ---------------------------------------------------------------------------
# New User field tests (supports_guest_queries, supports_join_request_queries)
# ---------------------------------------------------------------------------


def test_user_supports_guest_queries() -> None:
    """User parses supports_guest_queries field."""
    raw = {**SAMPLE_USER_RAW, "supports_guest_queries": True}
    from peyk.platforms.telegram.models import User
    result = User.from_dict(raw)
    assert result is not None
    assert result.supports_guest_queries is True


def test_user_supports_join_request_queries() -> None:
    """User parses supports_join_request_queries field."""
    raw = {**SAMPLE_USER_RAW, "supports_join_request_queries": False}
    from peyk.platforms.telegram.models import User
    result = User.from_dict(raw)
    assert result is not None
    assert result.supports_join_request_queries is False


def test_user_new_fields_defaults() -> None:
    """User new fields default to None when absent."""
    result = User.from_dict(SAMPLE_USER_RAW)
    assert result is not None
    assert result.supports_guest_queries is None
    assert result.supports_join_request_queries is None
