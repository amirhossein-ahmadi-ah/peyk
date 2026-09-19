"""Regressions found by running the shipped examples against a fake Telegram."""
from __future__ import annotations

import logging
import runpy
from pathlib import Path

import pytest

from peyk import Bot, Dispatcher, F, Router
from peyk.fsm.middleware import FSMContextMiddleware
from peyk.fsm import MemoryStorage
from peyk.platforms.telegram.types import Update, User as TelegramUser
from peyk.utils.i18n import I18n, I18nMiddleware

EXAMPLES = Path(__file__).resolve().parents[2] / "examples"
USER = {"id": 5, "is_bot": False, "first_name": "A", "language_code": "fa"}
CHAT = {"id": 5, "type": "private"}


def message_update(text: str) -> Update:
    entities = [{"type": "bot_command", "offset": 0, "length": len(text.split()[0])}] if text.startswith("/") else []
    return Update.from_dict({"update_id": 1, "message": {"message_id": 1, "date": 1, "from": USER, "chat": CHAT, "text": text, "entities": entities}})


class FakeClient:
    """Just enough of the Telegram client for dispatcher tests."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, object]]] = []
        self.dispatcher: Dispatcher | None = None

    async def get_me(self) -> TelegramUser:
        return TelegramUser(id=99, is_bot=True, first_name="B", username="bot")

    async def get_webhook_info(self) -> object:
        return type("Info", (), {"url": ""})()

    async def get_updates(self, **kwargs: object) -> list[Update]:
        self.calls.append(("get_updates", kwargs))
        assert self.dispatcher is not None
        await self.dispatcher.stop_polling()
        return []

    async def send_message(self, chat_id: object, text: str, **kwargs: object) -> object:
        self.calls.append(("send_message", {"text": text}))
        return type("Sent", (), {"message_id": 2, "chat": None, "text": text, "date": 1})()

    async def close(self) -> None:
        return None


def make_bot() -> tuple[Bot, FakeClient]:
    bot = Bot("1:T", platform="telegram")
    client = FakeClient()
    bot._client = client  # type: ignore[assignment]
    return bot, client


@pytest.mark.asyncio
async def test_router_and_dispatcher_have_command_decorator() -> None:
    seen: list[str] = []
    router = Router()
    dispatcher = Dispatcher()

    @router.command("admin", "root")
    async def admin(message) -> None:
        seen.append("admin")

    @dispatcher.command("start")
    async def start(message) -> None:
        seen.append("start")

    dispatcher.include_router(router)
    bot, _ = make_bot()
    for text in ("/start", "/admin", "/root", "/unknown"):
        await dispatcher.feed_raw_update(bot, message_update(text))
    assert seen == ["start", "admin", "admin"]
    with pytest.raises(ValueError):
        router.command()


@pytest.mark.asyncio
async def test_magic_filter_expressions_actually_filter() -> None:
    hits: list[str | None] = []
    router = Router()

    @router.message(F.text == "hi")
    async def only_hi(message) -> None:
        hits.append(message.text)

    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    bot, _ = make_bot()
    for text in ("hi", "nope", "hi"):
        await dispatcher.feed_raw_update(bot, message_update(text))
    assert hits == ["hi", "hi"]


@pytest.mark.asyncio
async def test_fsm_middleware_skips_events_without_identity(caplog: pytest.LogCaptureFixture) -> None:
    bot, _ = make_bot()
    await bot.me()
    middleware = FSMContextMiddleware(MemoryStorage())
    reached: list[bool] = []

    async def handler() -> str:
        reached.append(True)
        return "ok"

    with caplog.at_level(logging.ERROR):
        assert await middleware(handler, object(), {"bot": bot}) == "ok"
    assert reached == [True]
    assert not caplog.records


def test_resolved_update_types_are_explicit_and_include_interactive_updates() -> None:
    dispatcher = Dispatcher()
    types = dispatcher.resolve_used_update_types()
    assert {"message", "callback_query", "inline_query"} <= set(types)
    assert "chat_member" not in types and "message_reaction" not in types

    child = Router()
    child.chat_member_status_update()(lambda event: None)
    child.message_reaction()(lambda event: None)
    dispatcher.include_router(child)
    types = dispatcher.resolve_used_update_types()
    assert "chat_member" in types and "message_reaction" in types
    assert "message_reaction_count" not in types


@pytest.mark.asyncio
async def test_polling_sends_explicit_allowed_updates_for_telegram() -> None:
    bot, client = make_bot()
    dispatcher = Dispatcher()
    client.dispatcher = dispatcher
    await dispatcher.start_polling(bot, handle_signals=False, polling_timeout=1)
    (_, kwargs), = client.calls
    assert "callback_query" in kwargs["allowed_updates"]
    assert "inline_query" in kwargs["allowed_updates"]


@pytest.mark.asyncio
async def test_explicit_allowed_updates_are_not_overridden() -> None:
    bot, client = make_bot()
    dispatcher = Dispatcher()
    client.dispatcher = dispatcher
    await dispatcher.start_polling(bot, handle_signals=False, polling_timeout=1, allowed_updates=["message"])
    assert client.calls[0][1]["allowed_updates"] == ["message"]


@pytest.mark.asyncio
async def test_i18n_uses_the_users_language_and_binds_it_per_event() -> None:
    fixtures = Path(__file__).resolve().parents[1] / "fixtures" / "i18n"
    i18n = I18n(fixtures, default_locale="en")
    middleware = I18nMiddleware(i18n)
    bot, _ = make_bot()
    dispatcher = Dispatcher()
    seen: dict[str, str] = {}

    async def wrap(handler, event, data):
        return await middleware(handler, event, data)

    router = Router()
    router.handler_middleware(wrap)

    @router.command("start")
    async def start(message, gettext, locale) -> None:
        seen["locale"] = locale
        i18n.set_locale("en")  # another update switching the shared locale...
        seen["text"] = gettext("Hello")  # ...must not change this handler's language

    dispatcher.include_router(router)
    await dispatcher.feed_raw_update(bot, message_update("/start"))
    assert seen == {"locale": "fa", "text": "سلام"}


@pytest.mark.parametrize("example", sorted(EXAMPLES.glob("*.py")), ids=lambda path: path.name)
def test_every_example_loads(example: Path) -> None:
    runpy.run_path(str(example), run_name="example_import")
