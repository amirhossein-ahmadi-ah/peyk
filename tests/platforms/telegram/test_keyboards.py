"""Tests for `TelegramClient` keyboards & callback queries (Phase T7).

Fake `aiohttp.test_utils` server, zero real network. Covers
`answer_callback_query` (happy path + variants), keyboard-type
integration with `send_message` (regression-style: the types must work
on earlier-phase methods, not just standalone), `CallbackQuery`
parsing in both shapes, and the `callback_data` byte-limit validator.
"""

from __future__ import annotations

from typing import Any, Callable, Dict

import orjson
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms.telegram.client import (
    TelegramClient,
    build_inline_keyboard_button,
)
from peyk.platforms.telegram.models import (
    CallbackQuery,
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUsers,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    validate_callback_data,
)
from peyk.transport import RetryPolicy

TOKEN = "12345:TEST-TOKEN"

SAMPLE_CHAT_RAW = {"id": 200, "type": "private", "first_name": "U"}

SAMPLE_USER_RAW = {"id": 100, "is_bot": False, "first_name": "TestUser"}


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


# -- answer_callback_query -------------------------------------------------

async def test_answer_callback_query_minimal(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("answerCallbackQuery", lambda body: True)
    client = _client_for(test_server, server)

    assert await client.answer_callback_query("query-id-1") is True

    (call,) = server.calls_for("answerCallbackQuery")
    assert call["body"] == {"callback_query_id": "query-id-1"}


async def test_answer_callback_query_alert_variant(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("answerCallbackQuery", lambda body: True)
    client = _client_for(test_server, server)

    assert (
        await client.answer_callback_query(
            "query-id-2", text="Done!", show_alert=True, cache_time=60
        )
        is True
    )

    (call,) = server.calls_for("answerCallbackQuery")
    assert call["body"] == {
        "callback_query_id": "query-id-2",
        "text": "Done!",
        "show_alert": True,
        "cache_time": 60,
    }


async def test_answer_callback_query_url_variant(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("answerCallbackQuery", lambda body: True)
    client = _client_for(test_server, server)

    assert (
        await client.answer_callback_query(
            "query-id-3", url="https://t.me/example_bot?start=XYZ"
        )
        is True
    )

    (call,) = server.calls_for("answerCallbackQuery")
    assert call["body"]["url"] == "https://t.me/example_bot?start=XYZ"
    assert "text" not in call["body"]


# -- keyboard integration with send_message (regression-style) -------------

async def test_send_message_with_inline_keyboard(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("sendMessage", lambda body: _sample_message_raw(7))
    client = _client_for(test_server, server)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Yes", callback_data="vote:yes"
                ),
                InlineKeyboardButton(
                    text="Docs", url="https://core.telegram.org/bots/api"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Copy", callback_data="copy:1"
                )
            ],
        ]
    )

    msg = await client.send_message(200, "Pick one", reply_markup=markup)
    assert isinstance(msg, Message)
    assert msg.message_id == 7

    (call,) = server.calls_for("sendMessage")
    assert call["body"]["reply_markup"] == {
        "inline_keyboard": [
            [
                {"text": "Yes", "callback_data": "vote:yes"},
                {
                    "text": "Docs",
                    "url": "https://core.telegram.org/bots/api",
                },
            ],
            [{"text": "Copy", "callback_data": "copy:1"}],
        ]
    }


async def test_send_message_with_reply_keyboard(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("sendMessage", lambda body: _sample_message_raw(8))
    client = _client_for(test_server, server)

    markup = ReplyKeyboardMarkup(
        keyboard=[
            ["plain shorthand", KeyboardButton(text="Share", request_contact=True)],
            [
                KeyboardButton(
                    text="Pick user",
                    request_users=KeyboardButtonRequestUsers(
                        request_id=42, max_quantity=3
                    ),
                ),
                KeyboardButton(
                    text="Pick chat",
                    request_chat=KeyboardButtonRequestChat(
                        request_id=43, chat_is_channel=False
                    ),
                ),
                KeyboardButton(
                    text="Quiz",
                    request_poll=KeyboardButtonPollType(type="quiz"),
                ),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Choose…",
        selective=True,
    )

    await client.send_message(200, "Keyboard:", reply_markup=markup)

    (call,) = server.calls_for("sendMessage")
    sent = call["body"]["reply_markup"]
    assert sent["keyboard"][0] == [
        {"text": "plain shorthand"},
        {"text": "Share", "request_contact": True},
    ]
    assert sent["keyboard"][1][1] == {
        "text": "Pick chat",
        "request_chat": {"request_id": 43, "chat_is_channel": False},
    }
    assert sent["resize_keyboard"] is True
    assert sent["one_time_keyboard"] is True
    assert sent["input_field_placeholder"] == "Choose…"
    assert sent["selective"] is True


async def test_send_message_with_remove_and_force_reply(
    fake_server,
) -> None:
    server, test_server = fake_server
    server.set_response("sendMessage", lambda body: _sample_message_raw(9))
    client = _client_for(test_server, server)

    await client.send_message(
        200, "gone", reply_markup=ReplyKeyboardRemove(selective=True)
    )
    await client.send_message(
        200,
        "reply!",
        reply_markup=ForceReply(input_field_placeholder="Answer…"),
    )

    calls = server.calls_for("sendMessage")
    assert calls[0]["body"]["reply_markup"] == {
        "remove_keyboard": True,
        "selective": True,
    }
    assert calls[1]["body"]["reply_markup"] == {
        "force_reply": True,
        "input_field_placeholder": "Answer…",
    }


async def test_send_message_rejects_overlong_callback_data(
    fake_server,
) -> None:
    server, test_server = fake_server
    server.set_response("sendMessage", lambda body: _sample_message_raw(1))
    client = _client_for(test_server, server)

    bad = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="x", callback_data="y" * 65)]
        ]
    )
    with pytest.raises(ValueError):
        await client.send_message(200, "nope", reply_markup=bad)
    assert server.calls_for("sendMessage") == []


# -- CallbackQuery parsing -------------------------------------------------

def _callback_update_raw(
    *, with_message: bool = True, game: bool = False
) -> Dict[str, Any]:
    query: Dict[str, Any] = {
        "id": "cq-1",
        "from": SAMPLE_USER_RAW,
        "chat_instance": "ci-9",
    }
    if game:
        query["game_short_name"] = "my_game"
    else:
        query["data"] = "vote:yes"
    if with_message:
        query["message"] = _sample_message_raw(11)
    else:
        query["inline_message_id"] = "inline-abc-123"
    return {"update_id": 9001, "callback_query": query}


def test_callback_query_with_message() -> None:
    update = Update.from_dict(_callback_update_raw(with_message=True))
    assert update is not None
    query = update.callback_query
    assert isinstance(query, CallbackQuery)
    assert query.id == "cq-1"
    assert query.data == "vote:yes"
    assert query.game_short_name is None
    assert query.inline_message_id is None
    assert isinstance(query.message, Message)
    assert query.message.message_id == 11
    assert query.from_ is not None and query.from_.id == 100


def test_callback_query_with_inline_message_id() -> None:
    update = Update.from_dict(_callback_update_raw(with_message=False))
    assert update is not None
    query = update.callback_query
    assert isinstance(query, CallbackQuery)
    assert query.message is None
    assert query.inline_message_id == "inline-abc-123"
    assert query.data == "vote:yes"


def test_callback_query_game_short_name() -> None:
    update = Update.from_dict(
        _callback_update_raw(with_message=True, game=True)
    )
    assert update is not None
    query = update.callback_query
    assert isinstance(query, CallbackQuery)
    assert query.game_short_name == "my_game"
    assert query.data is None


def test_message_reply_markup_parses() -> None:
    raw = _sample_message_raw(12)
    raw["reply_markup"] = {
        "inline_keyboard": [[{"text": "Hi", "callback_data": "hi"}]]
    }
    msg = Message.from_dict(raw)
    assert msg is not None
    assert msg.reply_markup is not None
    [[button]] = msg.reply_markup.inline_keyboard
    assert button.text == "Hi"
    assert button.callback_data == "hi"


# -- callback_data validator -----------------------------------------------

def test_validate_callback_data_boundaries() -> None:
    validate_callback_data("a")  # 1 byte: minimum OK
    validate_callback_data("x" * 64)  # exactly 64 bytes: OK
    with pytest.raises(ValueError):
        validate_callback_data("")  # 0 bytes: too short
    with pytest.raises(ValueError):
        validate_callback_data("x" * 65)  # 65 bytes: too long


def test_validate_callback_data_multibyte_utf8() -> None:
    # 'ی' is 2 bytes in UTF-8: 32 of them fit exactly, 33 overflow.
    validate_callback_data("ی" * 32)
    with pytest.raises(ValueError):
        validate_callback_data("ی" * 33)
    # Mixed content counts encoded bytes, not characters.
    with pytest.raises(ValueError):
        validate_callback_data("x" * 63 + "ی")


def test_build_inline_keyboard_button_validates() -> None:
    button = build_inline_keyboard_button("OK", "ok:1")
    assert isinstance(button, InlineKeyboardButton)
    assert button.to_dict() == {"text": "OK", "callback_data": "ok:1"}
    with pytest.raises(ValueError):
        build_inline_keyboard_button("Bad", "z" * 100)
