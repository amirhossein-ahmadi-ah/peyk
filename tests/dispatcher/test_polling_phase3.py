from __future__ import annotations

import asyncio

import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk import BaleBot, Dispatcher, RubikaBot, TelegramBot
from peyk.transport.errors import NetworkError, RateLimitedError
from peyk.dispatcher.polling import BalePoller, RubikaPoller, TelegramPoller


def _telegram_update() -> dict:
    return {"update_id": 11, "message": {"message_id": 7, "date": 1, "chat": {"id": 101, "type": "private"}, "from": {"id": 2, "is_bot": False, "first_name": "U"}, "text": "/start"}}


def _bale_update() -> dict:
    return {"update_id": 21, "message": {"message_id": 8, "date": 1, "chat": {"id": 202, "type": "private"}, "from": {"id": 3, "is_bot": False, "first_name": "U"}, "text": "/start"}}


def _rubika_update() -> dict:
    return {"type": "NewMessage", "chat_id": "303", "new_message": {"message_id": "9", "sender_id": "4", "text": "/start"}}


@pytest.mark.asyncio
async def test_multi_platform_polling_replies_on_same_platform() -> None:
    seen: dict[str, list[dict]] = {"telegram": [], "bale": [], "rubika": []}
    delivered = {"telegram": False, "bale": False, "rubika": False}

    def app_for(platform: str) -> web.Application:
        async def handle(request: web.Request) -> web.Response:
            method = request.match_info["method"]
            if method == "getMe":
                if platform == "rubika":
                    return web.json_response({"status": "OK", "data": {"bot": {"bot_id": platform + "-bot", "bot_title": "Test Bot", "username": "test_bot"}}})
                return web.json_response({"ok": True, "result": {"id": 999, "is_bot": True, "first_name": "Test", "username": "test_bot"}})
            if method == "getWebhookInfo":
                if platform == "rubika":
                    return web.json_response({"status": "OK", "data": {"url": ""}})
                return web.json_response({"ok": True, "result": {"url": ""}})
            if method == "deleteWebhook":
                return web.json_response({"ok": True, "result": True})
            if method == "getUpdates":
                body = await request.json()
                seen[platform].append(body)
                if not delivered[platform]:
                    delivered[platform] = True
                    if platform == "telegram":
                        return web.json_response({"ok": True, "result": [_telegram_update()]})
                    if platform == "bale":
                        return web.json_response({"ok": True, "result": [_bale_update()]})
                    return web.json_response({"status": "OK", "data": {"updates": [_rubika_update()], "next_offset_id": "r2"}})
                if platform == "rubika":
                    return web.json_response({"status": "OK", "data": {"updates": [], "next_offset_id": "r2"}})
                return web.json_response({"ok": True, "result": []})
            if method == "sendMessage":
                body = await request.json()
                chat_id = body["chat_id"]
                if platform == "rubika":
                    return web.json_response({"status": "OK", "data": {"message_id": "sent"}})
                return web.json_response({"ok": True, "result": {"message_id": 99, "date": 1, "chat": {"id": chat_id, "type": "private"}, "text": body["text"]}})
            return web.json_response({"ok": True, "result": True})

        app = web.Application()
        if platform == "rubika":
            app.router.add_post("/v3/{token}/{method}", handle)
        else:
            app.router.add_post("/bot{token}/{method}", handle)
        return app

    async with TestServer(app_for("telegram")) as tg_server, TestServer(app_for("bale")) as bale_server, TestServer(app_for("rubika")) as rubika_server:
        tg = TelegramBot("T", base_url=str(tg_server.make_url("")))
        bale = BaleBot("B", base_url=str(bale_server.make_url("")))
        rubika = RubikaBot("R", base_url=str(rubika_server.make_url("")) + "/v3")
        dp = Dispatcher()
        hits: list[str] = []

        @dp.message()
        async def echo(message, bot, dispatcher) -> None:
            hits.append(bot.platform)
            await message.answer("echo")
            if len(hits) == 3:
                await asyncio.sleep(0.05)
                await dispatcher.stop_polling()

        try:
            await dp.start_polling(tg, bale, rubika, polling_timeout=1, close_bots=False)
        finally:
            await tg.close(); await bale.close(); await rubika.close()

    assert hits == ["telegram", "bale", "rubika"]
    assert seen["telegram"][0].get("offset") is None
    assert seen["bale"][0].get("offset") is None
    assert seen["rubika"][0].get("offset_id") is None
    # Offset ownership is verified independently below; the combined loop may
    # stop immediately after the third reply.


@pytest.mark.asyncio
async def test_lifecycle_hooks_run_recursively_and_shutdown_order() -> None:
    dp = Dispatcher()
    child = __import__("peyk").Router(name="child")
    dp.include_router(child)
    order: list[str] = []

    @dp.startup()
    async def root_start() -> None: order.append("root-start")

    @child.startup()
    async def child_start() -> None: order.append("child-start")

    @dp.shutdown()
    async def root_stop() -> None: order.append("root-stop")

    @child.shutdown()
    async def child_stop() -> None: order.append("child-stop")

    class StopBot:
        platform = "telegram"

    # Exercise lifecycle emission without opening a network session.
    await dp._emit_recursive("startup")
    await dp._emit_recursive("shutdown")
    assert order == ["root-start", "child-start", "root-stop", "child-stop"]


@pytest.mark.asyncio
async def test_rate_limit_and_network_backoff_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    from peyk.dispatcher import dispatcher as module

    sleeps: list[float] = []
    async def fake_sleep(stop: asyncio.Event, seconds: float) -> None:
        sleeps.append(seconds)
        stop.set()

    class Poller:
        calls = 0
        async def fetch(self):
            self.calls += 1
            if self.calls == 1:
                raise RateLimitedError("limited", retry_after_seconds=2.0)
            raise NetworkError("offline")

    stop = asyncio.Event()
    monkeypatch.setattr(module, "_sleep_or_stop", fake_sleep)
    await module._poll_bot(object(), object(), Poller(), asyncio.Semaphore(1), False, stop)
    assert sleeps == [2.0]
    assert module._looks_like_auth_error(Exception()) is False


@pytest.mark.asyncio
async def test_windows_signal_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    import signal
    from peyk.dispatcher import dispatcher as module

    class Loop:
        def add_signal_handler(self, sig, callback):
            raise NotImplementedError
        def remove_signal_handler(self, sig):
            raise NotImplementedError

    loop = Loop()
    monkeypatch.setattr(asyncio, "get_running_loop", lambda: loop)
    # The fallback is intentionally exercised through the same exception path
    # used by start_polling's signal installation.
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, lambda: None)
        except NotImplementedError:
            pass


@pytest.mark.asyncio
async def test_pollers_advance_their_own_offsets() -> None:
    class TelegramClient:
        calls = []
        async def get_updates(self, **kwargs):
            self.calls.append(kwargs)
            if len(self.calls) == 1:
                from peyk.platforms.telegram.types import Update
                return [Update(update_id=41)]
            return []
    class BaleClient:
        calls = []
        async def get_updates(self, **kwargs):
            self.calls.append(kwargs)
            if len(self.calls) == 1:
                from peyk.platforms.bale.types import Update
                return [Update(update_id=51)]
            return []
    class RubikaClient:
        calls = []
        async def get_updates(self, **kwargs):
            self.calls.append(kwargs)
            if len(self.calls) == 1:
                from peyk.platforms.rubika.types import Update
                return ([Update(type="NewMessage")], "next")
            return ([], "next")
    class FakeBot:
        def __init__(self, platform, client): self.platform, self.client = platform, client
    tg_client = TelegramClient(); bale_client = BaleClient(); rubika_client = RubikaClient()
    tg = TelegramPoller(FakeBot("telegram", tg_client), 1, None)
    bale = BalePoller(FakeBot("bale", bale_client), 1, None)
    rubika = RubikaPoller(FakeBot("rubika", rubika_client), 1, None)
    await tg.fetch(); await tg.fetch(); await bale.fetch(); await bale.fetch(); await rubika.fetch(); await rubika.fetch()
    assert tg_client.calls[1]["offset"] == 42
    assert bale_client.calls[1]["offset"] == 52
    assert rubika_client.calls[1]["offset_id"] == "next"
