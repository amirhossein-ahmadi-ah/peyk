"""Tests for `TelegramClient` forum topic methods (Phase T6).

Fake `aiohttp.test_utils` server, zero real network -- same pattern
as the T1/T2 client tests. One happy-path test per method, plus a
`Message` parsing test for each of the six topic-related service-message
subtypes, and a regression check that `send_message` passes
`message_thread_id` through correctly.
"""

from __future__ import annotations

from typing import Any, Callable, Dict

import orjson
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms.telegram.client import TelegramClient
from peyk.platforms.telegram.models import (
    ForumTopic,
    ForumTopicClosed,
    ForumTopicCreated,
    ForumTopicEdited,
    ForumTopicReopened,
    GeneralForumTopicHidden,
    GeneralForumTopicUnhidden,
    Message,
)
from peyk.transport import RetryPolicy

TOKEN = "12345:TEST-TOKEN"

SAMPLE_CHAT_RAW = {
    "id": 200,
    "type": "supergroup",
    "title": "TestForum",
    "is_forum": True,
}

SAMPLE_USER_RAW = {
    "id": 100,
    "is_bot": False,
    "first_name": "TestUser",
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


def _client_for(
    test_server: TestServer, server: FakeTelegramServer
) -> TelegramClient:
    base_url = str(test_server.make_url("")).rstrip("/")
    return TelegramClient(
        TOKEN,
        base_url=base_url,
        retry_policy=RetryPolicy(max_attempts=3, base_backoff_seconds=0.001),
    )


# -- Happy-path tests, one per method --------------------------------

async def test_create_forum_topic(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "createForumTopic",
        lambda body: {
            "message_thread_id": body["message_thread_id"] if "message_thread_id" in body else 42,
            "name": body["name"],
            "icon_color": body.get("icon_color"),
            "icon_custom_emoji_id": body.get("icon_custom_emoji_id"),
        },
    )
    client = _client_for(test_server, server)
    try:
        topic = await client.create_forum_topic(200, "New Topic", icon_color=6)
    finally:
        await client.close()
    assert isinstance(topic, ForumTopic)
    assert topic.name == "New Topic"
    assert topic.icon_color == 6
    body = server.calls_for("createForumTopic")[0]["body"]
    assert body["chat_id"] == 200
    assert body["name"] == "New Topic"
    assert body["icon_color"] == 6


async def test_edit_forum_topic(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "editForumTopic",
        lambda body: {
            "message_thread_id": body["message_thread_id"],
            "name": body.get("name", "Edited"),
        },
    )
    client = _client_for(test_server, server)
    try:
        topic = await client.edit_forum_topic(200, 42, name="Edited Topic")
    finally:
        await client.close()
    assert isinstance(topic, ForumTopic)
    assert topic.message_thread_id == 42
    body = server.calls_for("editForumTopic")[0]["body"]
    assert body["chat_id"] == 200
    assert body["message_thread_id"] == 42
    assert body["name"] == "Edited Topic"


async def test_close_forum_topic(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("closeForumTopic", lambda body: True)
    client = _client_for(test_server, server)
    try:
        ok = await client.close_forum_topic(200, 42)
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("closeForumTopic")[0]["body"]
    assert body == {"chat_id": 200, "message_thread_id": 42}


async def test_reopen_forum_topic(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("reopenForumTopic", lambda body: True)
    client = _client_for(test_server, server)
    try:
        ok = await client.reopen_forum_topic(200, 42)
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("reopenForumTopic")[0]["body"]
    assert body == {"chat_id": 200, "message_thread_id": 42}


async def test_delete_forum_topic(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("deleteForumTopic", lambda body: True)
    client = _client_for(test_server, server)
    try:
        ok = await client.delete_forum_topic(200, 42)
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("deleteForumTopic")[0]["body"]
    assert body == {"chat_id": 200, "message_thread_id": 42}


async def test_unpin_all_forum_topic_messages(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("unpinAllForumTopicMessages", lambda body: True)
    client = _client_for(test_server, server)
    try:
        ok = await client.unpin_all_forum_topic_messages(200, 42)
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("unpinAllForumTopicMessages")[0]["body"]
    assert body == {"chat_id": 200, "message_thread_id": 42}


async def test_edit_general_forum_topic(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("editGeneralForumTopic", lambda body: True)
    client = _client_for(test_server, server)
    try:
        ok = await client.edit_general_forum_topic(200, "General Topic")
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("editGeneralForumTopic")[0]["body"]
    assert body == {"chat_id": 200, "name": "General Topic"}


async def test_close_general_forum_topic(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("closeGeneralForumTopic", lambda body: True)
    client = _client_for(test_server, server)
    try:
        ok = await client.close_general_forum_topic(200)
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("closeGeneralForumTopic")[0]["body"]
    assert body == {"chat_id": 200}


async def test_reopen_general_forum_topic(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("reopenGeneralForumTopic", lambda body: True)
    client = _client_for(test_server, server)
    try:
        ok = await client.reopen_general_forum_topic(200)
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("reopenGeneralForumTopic")[0]["body"]
    assert body == {"chat_id": 200}


async def test_hide_general_forum_topic(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("hideGeneralForumTopic", lambda body: True)
    client = _client_for(test_server, server)
    try:
        ok = await client.hide_general_forum_topic(200)
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("hideGeneralForumTopic")[0]["body"]
    assert body == {"chat_id": 200}


async def test_unhide_general_forum_topic(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("unhideGeneralForumTopic", lambda body: True)
    client = _client_for(test_server, server)
    try:
        ok = await client.unhide_general_forum_topic(200)
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("unhideGeneralForumTopic")[0]["body"]
    assert body == {"chat_id": 200}


async def test_unpin_all_general_forum_topic_messages(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("unpinAllGeneralForumTopicMessages", lambda body: True)
    client = _client_for(test_server, server)
    try:
        ok = await client.unpin_all_general_forum_topic_messages(200)
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("unpinAllGeneralForumTopicMessages")[0]["body"]
    assert body == {"chat_id": 200}


async def test_get_forum_topic_icon_stickers(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "getForumTopicIconStickers",
        lambda body: [{"file_id": "sticker1", "file_unique_id": "u1"}],
    )
    client = _client_for(test_server, server)
    try:
        stickers = await client.get_forum_topic_icon_stickers()
    finally:
        await client.close()
    assert len(stickers) == 1
    assert stickers[0].file_id == "sticker1"


# -- Message parsing tests for service-message subtypes -----------

def _make_service_message(subtype: str, body: Dict[str, Any]) -> Dict[str, Any]:
    msg = _sample_message_raw(99)
    msg["chat"] = SAMPLE_CHAT_RAW
    msg["from"] = SAMPLE_USER_RAW
    msg[subtype] = body
    return msg


def _parse_service_message(subtype: str, body: Dict[str, Any]) -> Message:
    return Message.from_dict(_make_service_message(subtype, body))


def test_message_parses_forum_topic_created() -> None:
    msg = _parse_service_message(
        "forum_topic_created",
        {
            "name": "New Topic",
            "icon_color": 7,
            "icon_custom_emoji_id": "emoji123",
            "is_name_implicit": True,
        },
    )
    assert isinstance(msg.forum_topic_created, ForumTopicCreated)
    assert msg.forum_topic_created.name == "New Topic"
    assert msg.forum_topic_created.icon_color == 7
    assert msg.forum_topic_created.is_name_implicit is True
    assert msg.forum_topic_created.icon_custom_emoji_id == "emoji123"
    assert msg.forum_topic_closed is None
    assert msg.general_forum_topic_hidden is None


def test_message_parses_forum_topic_closed() -> None:
    msg = _parse_service_message("forum_topic_closed", {})
    assert isinstance(msg.forum_topic_closed, ForumTopicClosed)
    assert msg.forum_topic_created is None
    assert msg.forum_topic_edited is None


def test_message_parses_forum_topic_edited() -> None:
    msg = _parse_service_message(
        "forum_topic_edited", {"name": "Renamed", "icon_custom_emoji_id": "emoji9"}
    )
    assert isinstance(msg.forum_topic_edited, ForumTopicEdited)
    assert msg.forum_topic_edited.name == "Renamed"
    assert msg.forum_topic_edited.icon_custom_emoji_id == "emoji9"
    assert msg.forum_topic_reopened is None


def test_message_parses_forum_topic_reopened() -> None:
    msg = _parse_service_message("forum_topic_reopened", {})
    assert isinstance(msg.forum_topic_reopened, ForumTopicReopened)
    assert msg.forum_topic_closed is None
    assert msg.general_forum_topic_hidden is None


def test_message_parses_general_forum_topic_hidden() -> None:
    msg = _parse_service_message("general_forum_topic_hidden", {})
    assert isinstance(msg.general_forum_topic_hidden, GeneralForumTopicHidden)
    assert msg.forum_topic_created is None
    assert msg.forum_topic_closed is None
    assert msg.general_forum_topic_unhidden is None


def test_message_parses_general_forum_topic_unhidden() -> None:
    msg = _parse_service_message("general_forum_topic_unhidden", {})
    assert isinstance(msg.general_forum_topic_unhidden, GeneralForumTopicUnhidden)
    assert msg.general_forum_topic_hidden is None
    assert msg.forum_topic_created is None
    assert msg.forum_topic_reopened is None


# -- Regression check: send_message with message_thread_id ---------

async def test_send_message_includes_message_thread_id(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("sendMessage", lambda body: _sample_message_raw(1))
    client = _client_for(test_server, server)
    try:
        msg = await client.send_message(200, "hello in topic", message_thread_id=42)
    finally:
        await client.close()
    assert isinstance(msg, Message)
    body = server.calls_for("sendMessage")[0]["body"]
    assert body["message_thread_id"] == 42
    assert body["chat_id"] == 200
    assert body["text"] == "hello in topic"