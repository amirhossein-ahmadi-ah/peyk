"""Tests for T16: Web Apps / Mini Apps.

Uses the same FakeTelegramServer pattern from test_client.py.
"""

from __future__ import annotations

from typing import Any, Callable, Dict

import orjson
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms.telegram.client import TelegramClient
from peyk.platforms.telegram.models import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    MenuButtonWebApp,
    Message,
    SentWebAppMessage,
    WebAppData,
    WebAppInfo,
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
# T16 client method tests
# ---------------------------------------------------------------------------


async def test_answer_web_app_query(fake_server) -> None:
    """Happy path: answerWebAppQuery sends correct payload with InlineQueryResult."""
    server, test_server = fake_server
    server.set_response(
        "answerWebAppQuery",
        lambda body: {"inline_message_id": "inline-msg-123"},
    )

    client = _client_for(test_server, server)
    try:
        result = await client.answer_web_app_query(
            web_app_query_id="wapp-q-1",
            result=InlineQueryResultArticle(
                id="art-1",
                title="Test Article",
                input_message_content=InputTextMessageContent(
                    message_text="Hello from Web App!"
                ),
            ),
        )
    finally:
        await client.close()

    assert isinstance(result, SentWebAppMessage)
    assert result.inline_message_id == "inline-msg-123"

    calls = server.calls_for("answerWebAppQuery")
    assert len(calls) == 1
    body = calls[0]["body"]
    assert body["web_app_query_id"] == "wapp-q-1"
    assert body["result"]["type"] == "article"
    assert body["result"]["id"] == "art-1"
    assert body["result"]["title"] == "Test Article"
    assert body["result"]["input_message_content"]["message_text"] == "Hello from Web App!"


async def test_answer_web_app_query_with_mapping(fake_server) -> None:
    """answerWebAppQuery accepts raw mapping result."""
    server, test_server = fake_server
    server.set_response(
        "answerWebAppQuery",
        lambda body: {"inline_message_id": "inline-msg-456"},
    )

    client = _client_for(test_server, server)
    try:
        result = await client.answer_web_app_query(
            web_app_query_id="wapp-q-2",
            result={"type": "article", "id": "x", "title": "Y", "input_message_content": {"message_text": "raw"}},
        )
    finally:
        await client.close()

    assert isinstance(result, SentWebAppMessage)
    assert result.inline_message_id == "inline-msg-456"


# ---------------------------------------------------------------------------
# Cross-phase integration tests (T7/T8 forward-reference resolution)
# ---------------------------------------------------------------------------


def test_inline_keyboard_button_web_app_serialization() -> None:
    """InlineKeyboardButton.web_app (T7) correctly serializes a real WebAppInfo instance."""
    web_app = WebAppInfo(url="https://my-mini-app.example.com")
    button = InlineKeyboardButton(text="Open App", web_app=web_app)
    result = button.to_dict()

    assert result["text"] == "Open App"
    assert "web_app" in result
    assert result["web_app"]["url"] == "https://my-mini-app.example.com"


def test_inline_keyboard_button_web_app_none() -> None:
    """InlineKeyboardButton without web_app does not include web_app key."""
    button = InlineKeyboardButton(text="Regular", callback_data="cb")
    result = button.to_dict()
    assert "web_app" not in result


def test_menu_button_web_app_serialization() -> None:
    """MenuButtonWebApp.web_app (T8) correctly serializes a real WebAppInfo instance."""
    web_app = WebAppInfo(url="https://menu-mini-app.example.com")
    menu_button = MenuButtonWebApp(text="Menu App", web_app=web_app)
    result = menu_button.to_dict()

    assert result["type"] == "web_app"
    assert result["text"] == "Menu App"
    assert "web_app" in result
    assert result["web_app"]["url"] == "https://menu-mini-app.example.com"


def test_inline_keyboard_markup_with_web_app_button() -> None:
    """InlineKeyboardMarkup containing a WebAppInfo button serializes correctly."""
    web_app = WebAppInfo(url="https://example.com/app")
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Launch", web_app=web_app)]
        ]
    )
    result = markup.to_dict()

    assert len(result["inline_keyboard"]) == 1
    row = result["inline_keyboard"][0]
    assert len(row) == 1
    assert row[0]["text"] == "Launch"
    assert row[0]["web_app"]["url"] == "https://example.com/app"


# ---------------------------------------------------------------------------
# WebAppData parsing from fake Message payload
# ---------------------------------------------------------------------------


def test_web_app_data_parsing() -> None:
    """WebAppData model parses correctly."""
    raw = {
        "data": "user_data_payload",
        "button_text": "Submit",
    }
    result = WebAppData.from_dict(raw)
    assert result is not None
    assert result.data == "user_data_payload"
    assert result.button_text == "Submit"


def test_web_app_data_none() -> None:
    """WebAppData handles None input."""
    assert WebAppData.from_dict(None) is None


def test_web_app_data_defaults() -> None:
    """WebAppData uses correct defaults for missing fields."""
    raw = {"data": "test"}
    result = WebAppData.from_dict(raw)
    assert result is not None
    assert result.data == "test"
    assert result.button_text == ""


def test_message_with_web_app_data() -> None:
    """Message model correctly parses web_app_data."""
    msg_raw = _sample_message_raw(1)
    msg_raw["web_app_data"] = {
        "data": "button_clicked",
        "button_text": "Press Me",
    }

    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.web_app_data is not None
    assert result.web_app_data.data == "button_clicked"
    assert result.web_app_data.button_text == "Press Me"


def test_message_without_web_app_data() -> None:
    """Message model works when web_app_data is absent."""
    msg_raw = _sample_message_raw(1)
    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.web_app_data is None


# ---------------------------------------------------------------------------
# SentWebAppMessage parsing
# ---------------------------------------------------------------------------


def test_sent_web_app_message_parsing() -> None:
    """SentWebAppMessage parses correctly."""
    raw = {"inline_message_id": "sent-inline-123"}
    result = SentWebAppMessage.from_dict(raw)
    assert result is not None
    assert result.inline_message_id == "sent-inline-123"


def test_sent_web_app_message_none() -> None:
    """SentWebAppMessage handles None input."""
    assert SentWebAppMessage.from_dict(None) is None


def test_sent_web_app_message_defaults() -> None:
    """SentWebAppMessage uses correct defaults."""
    raw = {}
    result = SentWebAppMessage.from_dict(raw)
    assert result is not None
    assert result.inline_message_id is None


# ---------------------------------------------------------------------------
# WebAppInfo edge cases
# ---------------------------------------------------------------------------


def test_web_app_info_empty_url() -> None:
    """WebAppInfo accepts empty URL."""
    info = WebAppInfo(url="")
    assert info.url == ""
    assert info.to_dict() == {"url": ""}


def test_web_app_info_from_dict() -> None:
    """WebAppInfo.from_dict parses correctly."""
    raw = {"url": "https://test.com"}
    result = WebAppInfo.from_dict(raw)
    assert result is not None
    assert result.url == "https://test.com"


def test_web_app_info_none() -> None:
    """WebAppInfo handles None input."""
    assert WebAppInfo.from_dict(None) is None
