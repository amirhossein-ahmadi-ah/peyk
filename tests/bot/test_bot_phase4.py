from __future__ import annotations

import asyncio
import inspect

import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer
from typing import assert_type

from peyk import Bot, Dispatcher, Router, run
from peyk.bot.errors import InvalidTokenError
from peyk.types import CallbackQuery, Message


def _tg_update() -> dict[str, object]:
    return {"update_id": 1, "message": {"message_id": 7, "date": 1, "chat": {"id": 10, "type": "private"}, "from": {"id": 20, "is_bot": False, "first_name": "U"}, "text": "/start"}}


def _bale_update() -> dict[str, object]:
    return {"update_id": 1, "message": {"message_id": 7, "chat": {"id": 10, "type": "private"}, "from": {"id": 20, "is_bot": False, "first_name": "U"}, "text": "/start"}}


def _rubika_update() -> dict[str, object]:
    return {"type": "NewMessage", "chat_id": "c1", "new_message": {"message_id": "7", "sender_id": "20", "text": "/start"}}


@pytest.mark.asyncio
@pytest.mark.parametrize("platform", ["telegram", "bale", "rubika"])
async def test_simple_target_end_to_end(platform: str) -> None:
    calls: list[str] = []
    delivered = False

    async def handle(request: web.Request) -> web.Response:
        nonlocal delivered
        method = request.match_info["method"]
        calls.append(method)
        if method == "getMe":
            if platform == "rubika":
                return web.json_response({"status": "OK", "data": {"bot": {"bot_id": "b1", "bot_title": "Bot", "username": "bot"}}})
            return web.json_response({"ok": True, "result": {"id": 1, "is_bot": True, "first_name": "Bot", "username": "bot"}})
        if method == "getWebhookInfo":
            if platform == "rubika":
                return web.json_response({"status": "OK", "data": {"url": ""}})
            return web.json_response({"ok": True, "result": {"url": ""}})
        if method == "deleteWebhook":
            return web.json_response({"ok": True, "result": True})
        if method == "getUpdates":
            if delivered:
                if platform == "rubika":
                    return web.json_response({"status": "OK", "data": {"updates": [], "next_offset_id": "r2"}})
                return web.json_response({"ok": True, "result": []})
            delivered = True
            if platform == "telegram":
                return web.json_response({"ok": True, "result": [_tg_update()]})
            if platform == "bale":
                return web.json_response({"ok": True, "result": [_bale_update()]})
            return web.json_response({"status": "OK", "data": {"updates": [_rubika_update()], "next_offset_id": "r2"}})
        if method == "sendMessage":
            body = await request.json()
            if platform == "rubika":
                return web.json_response({"status": "OK", "data": {"message_id": "sent"}})
            return web.json_response({"ok": True, "result": {"message_id": 8, "date": 1, "chat": {"id": body["chat_id"], "type": "private"}, "text": body["text"]}})
        return web.json_response({"ok": True, "result": True})

    app = web.Application()
    if platform == "rubika":
        app.router.add_post("/v3/{token}/{method}", handle)
    else:
        app.router.add_post("/bot{token}/{method}", handle)

    async with TestServer(app) as server:
        base_url = str(server.make_url("")) + ("/v3" if platform == "rubika" else "")
        bot = Bot("TOKEN", platform=platform, base_url=base_url)
        stopped = False

        @bot.command("start")
        async def start(message: Message, dispatcher: Dispatcher) -> None:
            nonlocal stopped
            await message.answer("Hello!")
            stopped = True
            await dispatcher.stop_polling()

        await bot.run_async(polling_timeout=1)
        assert stopped
        assert "getMe" in calls and "sendMessage" in calls
        await bot.close()


def test_decorators_keep_callable_identity_and_aliases() -> None:
    bot = Bot("T", platform="telegram")

    @bot.command("start", "begin")
    async def handler(message: Message) -> str:
        return "ok"

    assert handler.__name__ == "handler"
    assert len(bot.router._message) == 2
    assert all(item.callback is handler for item in bot.router._message)


def test_callback_exact_and_prefix_filters() -> None:
    bot = Bot("T", platform="telegram")

    @bot.callback("exact")
    async def exact(query: CallbackQuery) -> None:
        pass

    @bot.callback("item:", prefix=True)
    async def prefixed(query: CallbackQuery) -> None:
        pass

    exact_event = CallbackQuery(id="1", data="exact")
    prefix_event = CallbackQuery(id="2", data="item:42")
    assert asyncio.run(bot.router.propagate_event(exact_event)) is None
    assert asyncio.run(bot.router.propagate_event(prefix_event)) is None


def test_startup_shutdown_hooks_and_explicit_dispatcher() -> None:
    bot = Bot("T", platform="telegram")
    router = Router(name="child")
    bot.include_router(router)
    dp = Dispatcher()
    dp.include_router(bot.router)
    order: list[str] = []

    @bot.on_startup
    async def startup() -> None:
        order.append("start")

    @bot.on_shutdown
    async def shutdown() -> None:
        order.append("stop")

    async def exercise() -> None:
        await dp._emit_recursive("startup")
        await dp._emit_recursive("shutdown")

    asyncio.run(exercise())
    assert order == ["start", "stop"]


def test_peyk_run_accepts_multiple_platforms(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[str] = []

    async def fake_run_async(self: Bot[object], **kwargs: object) -> None:
        seen.append(self.platform)

    monkeypatch.setattr(Bot, "run_async", fake_run_async)
    a = Bot("A", platform="telegram")
    b = Bot("B", platform="bale")
    run(a, b)
    assert sorted(seen) == ["bale", "telegram"]


def test_decorated_handler_type_identity() -> None:
    bot = Bot("T", platform="telegram")

    @bot.command("start")
    async def handler(message: Message, value: int) -> str:
        return str(value)

    assert_type(handler, type(handler))
    assert list(inspect.signature(handler).parameters) == ["message", "value"]


@pytest.mark.asyncio
async def test_invalid_token_message() -> None:
    async def handle(request: web.Request) -> web.Response:
        return web.json_response({"ok": False, "error_code": 401, "description": "Unauthorized"})

    app = web.Application()
    app.router.add_post("/bot{token}/{method}", handle)
    async with TestServer(app) as server:
        bot = Bot("bad", platform="telegram", base_url=str(server.make_url("")))
        with pytest.raises(InvalidTokenError, match="Telegram rejected the token"):
            await bot.run_async()
        await bot.close()
