"""Tests for the Soroush Plus (Splus) platform.

Splus is Telegram-shaped, so these tests focus on what is Splus-specific: the
base URL, the confirmed method surface, the request-field translation, the
capability declarations and the wiring into ``Bot``/``Dispatcher``.  A fake
``Session`` is injected, so no network and no ``aiohttp`` server is needed.
"""
from __future__ import annotations

import json
from typing import Any, Mapping, Optional

import pytest

from peyk import Bot, Dispatcher, Feature, SplusBot
from peyk.bot.base import Bot as BaseBot
from peyk.keyboard import InlineButton, InlineKeyboard
from peyk.keyboard.ir import ButtonStyle
from peyk.platform_core.adapters import SPLUS_CAPABILITIES
from peyk.platform_core.capabilities import SupportLevel, get_capabilities
from peyk.platform_core.errors import UnsupportedFeatureError
from peyk.platforms.splus import BASE_URL, SPLUS_METHODS, SPLUS_UPDATE_TYPES, SplusAPIError, SplusClient
from peyk.platforms.telegram.errors import TelegramAPIError
from peyk.platforms.telegram.types import Update
from peyk.transport.session import TransportResponse
from peyk.webhook.registrars import SplusWebhookRegistrar, WebhookOptions, registrar_for

TOKEN = "123:ABC"
USER = {"id": 1, "is_bot": True, "first_name": "Bot", "username": "bot"}
CHAT = {"id": 10, "type": "private", "first_name": "U"}
MESSAGE = {"message_id": 5, "date": 1, "chat": CHAT, "from": {"id": 20, "is_bot": False, "first_name": "U"}, "text": "hi"}


class FakeSession:
    """Records requests and answers with a canned Telegram-shaped envelope."""

    def __init__(self, results: Optional[Mapping[str, Any]] = None) -> None:
        self.results = dict(results or {})
        self.calls: list[dict[str, Any]] = []

    async def request(self, method: str, url: str, *, params: Any = None, json_body: Any = None, data: Any = None, files: Any = None, timeout: Any = None) -> TransportResponse:
        self.calls.append({"method": method, "url": url, "json": json_body, "data": data, "files": files})
        name = url.rsplit("/", 1)[-1]
        result = self.results.get(name, MESSAGE if name.startswith(("send", "edit", "copy", "forward")) else True)
        if name == "getMe":
            result = USER
        return TransportResponse(status=200, json={"ok": True, "result": result}, body=b"{}", headers={})

    async def close(self) -> None:
        return None


def _bot(session: Optional[FakeSession] = None, **kwargs: Any) -> SplusBot:
    return SplusBot(TOKEN, session=session or FakeSession(), **kwargs)


# --------------------------------------------------------------------- client

async def test_url_and_error_types() -> None:
    session = FakeSession()
    client = SplusClient(TOKEN, session)
    me = await client.get_me()
    assert session.calls[0]["url"] == f"{BASE_URL}/bot{TOKEN}/getMe" == "https://api.splus.ir/bot123:ABC/getMe"
    assert me.username == "bot"
    assert issubclass(SplusAPIError, TelegramAPIError)
    assert client._error_class is SplusAPIError


async def test_error_envelope_raises_splus_error() -> None:
    class Failing(FakeSession):
        async def request(self, *a: Any, **k: Any) -> TransportResponse:
            return TransportResponse(status=200, json={"ok": False, "error_code": 400, "description": "bad"}, body=b"{}", headers={})

    with pytest.raises(SplusAPIError) as info:
        await SplusClient(TOKEN, Failing()).get_me()
    assert info.value.error_code == 400


def test_client_exposes_only_confirmed_methods() -> None:
    for name in SPLUS_METHODS:
        assert callable(getattr(SplusClient, name)), name
    for name in ("send_poll", "send_invoice", "ban_chat_member", "send_venue", "answer_inline_query", "create_forum_topic"):
        assert not hasattr(SplusClient, name), name


async def test_reply_and_preview_fields_are_translated() -> None:
    session = FakeSession()
    client = SplusClient(TOKEN, session)
    await client.send_message(10, "hi", reply_parameters={"message_id": 7, "allow_sending_without_reply": True}, link_preview_options={"is_disabled": True})
    body = session.calls[0]["json"]
    assert body["reply_to_message_id"] == 7
    assert body["allow_sending_without_reply"] is True
    assert body["disable_web_page_preview"] is True
    assert "reply_parameters" not in body and "link_preview_options" not in body


async def test_translation_also_applies_to_multipart_form_fields() -> None:
    session = FakeSession()
    client = SplusClient(TOKEN, session)
    await client.send_photo(10, b"\x89PNG", reply_parameters={"message_id": 9})
    call = session.calls[0]
    assert call["files"] is not None
    assert call["data"]["reply_to_message_id"] == 9
    assert "reply_parameters" not in call["data"]


async def test_get_updates_and_webhook_payloads() -> None:
    session = FakeSession({"getUpdates": [{"update_id": 3, "message": MESSAGE}]})
    client = SplusClient(TOKEN, session)
    updates = await client.get_updates(offset=3, timeout=30)
    assert updates[0].update_id == 3 and updates[0].message.text == "hi"
    assert session.calls[0]["json"] == {"offset": 3, "timeout": 30}
    await client.set_webhook("https://x.test/hook", max_connections=5)
    assert session.calls[1]["json"] == {"url": "https://x.test/hook", "max_connections": 5}


# ------------------------------------------------------------------------ bot

async def test_bot_facade_sends_with_reply_to_message_id() -> None:
    session = FakeSession()
    bot = Bot(TOKEN, platform="splus", session=session)
    assert bot.platform == "splus" and bot.client.__class__ is SplusClient
    message = await bot.send_message(10, "hello", reply_to_message_id=5)
    assert message.text == "hi"
    body = session.calls[0]["json"]
    assert body["chat_id"] == 10 and body["text"] == "hello"
    assert body["reply_to_message_id"] == 5 and "reply_parameters" not in body


async def test_unsupported_features_are_refused_before_any_request() -> None:
    session = FakeSession()
    bot = _bot(session)
    with pytest.raises(UnsupportedFeatureError):
        await bot.send_poll(10, "q?", ["a", "b"])
    with pytest.raises(UnsupportedFeatureError):
        await bot.set_webhook("https://x.test/h", secret_token="s")
    with pytest.raises(UnsupportedFeatureError):
        await bot.ban_chat_member(10, 20)
    assert session.calls == []


async def test_webhook_delegation() -> None:
    session = FakeSession()
    bot = _bot(session)
    assert await bot.set_webhook("https://x.test/h", max_connections=3, drop_pending_updates=True)
    assert session.calls[0]["json"] == {"url": "https://x.test/h", "max_connections": 3, "drop_pending_updates": True}
    assert await bot.delete_webhook()


# --------------------------------------------------------------- capabilities

def test_capability_declarations() -> None:
    caps = get_capabilities("splus")
    assert caps.platform == "splus"
    for feature in (Feature.TEXT, Feature.PHOTO, Feature.EDIT_TEXT, Feature.POLLING, Feature.WEBHOOK, Feature.BOT_COMMANDS):
        assert caps.supports(feature), feature
    for feature in (Feature.POLL, Feature.VENUE, Feature.PAYMENTS, Feature.WEBHOOK_SECRET_HEADER, Feature.MEMBER_STATUS_UPDATES, Feature.TELEGRAM_GAMES):
        assert caps.get(feature).level is SupportLevel.NONE, feature
    # Unconfirmed chat administration stays UNKNOWN (and therefore unsupported).
    assert caps.get(Feature.BAN).level is SupportLevel.UNKNOWN and not caps.supports(Feature.BAN)
    assert caps.limit("callback_data_max_bytes") == 64


def test_legacy_projection() -> None:
    assert SPLUS_CAPABILITIES.platform == "splus"
    assert SPLUS_CAPABILITIES.update_delivery == "both"
    assert SPLUS_CAPABILITIES.supports_topics is False
    assert SPLUS_CAPABILITIES.supports_payments is False
    assert SPLUS_CAPABILITIES.supported_parse_modes == ["Markdown", "MarkdownV2", "HTML"]
    assert SPLUS_CAPABILITIES.callback_data_max_bytes == 64


# --------------------------------------------------------- dispatch + updates

async def test_dispatcher_routes_message_and_callback_updates() -> None:
    bot = _bot()
    dp = Dispatcher()
    seen: list[tuple[str, object]] = []

    @dp.message()
    async def on_message(message: Any) -> None:
        seen.append(("message", message.text))

    @dp.callback_query()
    async def on_callback(query: Any) -> None:
        seen.append(("callback", query.data))

    await dp.feed_raw_update(bot, Update.from_dict({"update_id": 1, "message": MESSAGE}))
    await dp.feed_raw_update(bot, Update.from_dict({"update_id": 2, "callback_query": {"id": "c", "from": {"id": 20, "is_bot": False, "first_name": "U"}, "message": MESSAGE, "data": "go"}}))
    assert seen == [("message", "hi"), ("callback", "go")]


def test_update_types_constant() -> None:
    assert set(SPLUS_UPDATE_TYPES) == {"message", "edited_message", "callback_query"}


async def test_webhook_registrar_has_no_secret_header() -> None:
    session = FakeSession()
    bot = _bot(session)
    registrar = registrar_for(bot)
    assert isinstance(registrar, SplusWebhookRegistrar)
    await registrar.install(bot, "https://x.test/splus/abc", "abc", WebhookOptions(max_connections=4))
    assert session.calls[0]["json"] == {"url": "https://x.test/splus/abc", "max_connections": 4}
    assert "secret_token" not in session.calls[0]["json"]


async def test_webhook_processor_accepts_splus_update_with_path_secret_only() -> None:
    from peyk.webhook.processor import WebhookProcessor

    dp = Dispatcher()
    seen: list[str] = []

    @dp.message()
    async def on_message(message: Any) -> None:
        seen.append(message.text)

    processor = WebhookProcessor(dp, secret="s", handle_in_background=False)
    # No X-Telegram-Bot-Api-Secret-Token header: Splus cannot send one, so it must not be required.
    result = await processor.handle(_bot(), json.dumps({"update_id": 9, "message": MESSAGE}).encode(), {})
    assert result.status == 200
    assert seen == ["hi"]


def test_polling_uses_the_telegram_poller() -> None:
    from peyk.dispatcher.polling import TelegramPoller, make_poller

    assert isinstance(make_poller(_bot(), 30, None), TelegramPoller)


# ------------------------------------------------------------------ keyboards

async def test_inline_keyboard_renders_confirmed_buttons_and_drops_style() -> None:
    session = FakeSession()
    bot = _bot(session)
    markup = InlineKeyboard(inline_keyboard=[[InlineButton("a", callback_data="x", style=ButtonStyle.PRIMARY), InlineButton("b", url="https://x.test")]])
    await bot.send_message(10, "kb", reply_markup=markup)
    row = session.calls[0]["json"]["reply_markup"]["inline_keyboard"][0]
    assert row[0]["callback_data"] == "x" and "style" not in row[0]
    assert row[1]["url"] == "https://x.test"
    markup = InlineKeyboard(inline_keyboard=[[InlineButton("c", copy_text="abc")]])
    with pytest.raises(UnsupportedFeatureError):
        await bot.send_message(10, "kb", reply_markup=markup)


async def test_unconfirmed_button_kind_is_rejected() -> None:
    bot = _bot()
    markup = InlineKeyboard(inline_keyboard=[[InlineButton("pay", pay=True)]])
    with pytest.raises(UnsupportedFeatureError):
        await bot.send_message(10, "kb", reply_markup=markup)


async def test_bound_actions_work_end_to_end_through_the_bot_router() -> None:
    from peyk.keyboard import InlineKeyboardBuilder

    session = FakeSession()
    bot = _bot(session)
    keyboard = InlineKeyboardBuilder().button(text="Say hi", callback_data="hi").as_markup()

    @bot.command("start")
    async def start(message: Any) -> None:
        await message.answer("welcome", reply_markup=keyboard)

    @bot.callback_query()
    async def on_button(query: Any) -> None:
        await query.answer("Hi!")

    dp = Dispatcher()
    dp.include_router(bot.router)
    start_message = dict(MESSAGE, text="/start", entities=[{"type": "bot_command", "offset": 0, "length": 6}])
    await dp.feed_raw_update(bot, Update.from_dict({"update_id": 1, "message": start_message}))
    send = [c for c in session.calls if c["url"].endswith("/sendMessage")][0]
    assert send["json"]["text"] == "welcome"
    assert send["json"]["reply_markup"]["inline_keyboard"][0][0]["callback_data"] == "hi"

    callback = {"id": "cb1", "from": {"id": 20, "is_bot": False, "first_name": "U"}, "message": MESSAGE, "data": "hi"}
    await dp.feed_raw_update(bot, Update.from_dict({"update_id": 2, "callback_query": callback}))
    answer = [c for c in session.calls if c["url"].endswith("/answerCallbackQuery")][0]
    assert answer["json"]["callback_query_id"] == "cb1" and answer["json"]["text"] == "Hi!"
