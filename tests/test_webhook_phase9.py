from __future__ import annotations

import asyncio
import ssl

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from peyk.webhook.processor import WebhookProcessor
from peyk.webhook.security import IPFilter, constant_time_compare, verify_telegram_secret_header
from peyk.webhook.aiohttp_server import SimpleRequestHandler


class FakeBot:
    def __init__(self, platform: str) -> None:
        self.platform = platform
        self.calls: list[object] = []


class FakeDispatcher:
    def __init__(self) -> None:
        self.events: list[object] = []
        self.started = asyncio.Event()

    async def feed_raw_update(self, bot: FakeBot, update: object) -> None:
        self.events.append(update)
        self.started.set()


@pytest.mark.asyncio
async def test_telegram_header_and_background_processing() -> None:
    dispatcher = FakeDispatcher()
    bot = FakeBot("telegram")
    processor = WebhookProcessor(dispatcher, secret="secret")
    good = await processor.handle(bot, b'{"update_id": 1}', {"X-Telegram-Bot-Api-Secret-Token": "secret"})
    bad = await processor.handle(bot, b'{"update_id": 2}', {"X-Telegram-Bot-Api-Secret-Token": "wrong"})
    assert good.status == 200
    assert bad.status == 404
    await asyncio.wait_for(dispatcher.started.wait(), 1)
    await processor.shutdown()
    assert dispatcher.events[0].update_id == 1


@pytest.mark.asyncio
async def test_malformed_and_oversize() -> None:
    dispatcher = FakeDispatcher()
    bot = FakeBot("bale")
    processor = WebhookProcessor(dispatcher, max_body_size=8)
    assert (await processor.handle(bot, b"not-json", {})).status == 400
    assert (await processor.handle(bot, b"{}xxxxxxxx", {})).status == 413


@pytest.mark.asyncio
async def test_path_secret_and_ip_filter() -> None:
    dispatcher = FakeDispatcher()
    bot = FakeBot("bale")
    app = web.Application()
    handler = SimpleRequestHandler(dispatcher, bot, "/hook/bale/abc", "unused")
    app.router.add_route("POST", "/hook/bale/abc", handler)
    server = TestServer(app)
    client = TestClient(server)
    await client.start_server()
    try:
        assert (await client.post("/hook/bale/wrong", data=b"{}" )).status == 404
        assert (await client.post("/hook/bale/abc", data=b"{\"update_id\":1}" )).status == 200
    finally:
        await handler.shutdown()
        await client.close()


def test_security_helpers_and_forwarded_for() -> None:
    assert constant_time_compare("abc", "abc")
    assert not constant_time_compare("abc", "abd")
    assert verify_telegram_secret_header({"X-Telegram-Bot-Api-Secret-Token": "abc"}, "abc")
    assert not verify_telegram_secret_header({}, "abc")
    filt = IPFilter(["10.0.0.0/8"])
    assert filt.allows("10.1.2.3", {"X-Forwarded-For": "192.0.2.1"})
    assert not filt.allows("192.0.2.1", {})
    trusted = IPFilter(["10.0.0.0/8"], trust_forwarded_for=True)
    assert trusted.allows("192.0.2.1", {"X-Forwarded-For": "10.1.2.3"})


def test_rubika_security_shim() -> None:
    from peyk.platforms.rubika.webhook_security import constant_time_compare as legacy_compare
    assert legacy_compare("x", "x")

@pytest.mark.asyncio
async def test_registrars_send_audited_platform_urls() -> None:
    from peyk.webhook.registrars import BaleWebhookRegistrar, RubikaWebhookRegistrar, TelegramWebhookRegistrar, WebhookOptions

    class Client:
        def __init__(self) -> None:
            self.calls: list[tuple[str, object]] = []
        async def set_webhook(self, url: str, **kwargs: object) -> bool:
            self.calls.append(("set_webhook", (url, kwargs)))
            return True
        async def delete_webhook(self, **kwargs: object) -> bool:
            self.calls.append(("delete_webhook", kwargs))
            return True
        async def update_bot_endpoints(self, url: str, type: str) -> bool:
            self.calls.append(("update_bot_endpoints", (url, type)))
            return True

    class BotLike:
        def __init__(self, platform: str, client: Client) -> None:
            self.platform = platform
            self.client = client
        def supports(self, feature: object) -> bool:
            return True

    tg_client, bale_client, rubika_client = Client(), Client(), Client()
    tg = BotLike("telegram", tg_client)
    bale = BotLike("bale", bale_client)
    rubika = BotLike("rubika", rubika_client)
    options = WebhookOptions(allowed_updates=["message"], drop_pending_updates=True, max_connections=7)
    await TelegramWebhookRegistrar().install(tg, "https://x/tg/s", "s", options)
    await BaleWebhookRegistrar().install(bale, "https://x/bale/s", "s", WebhookOptions())
    registrar = RubikaWebhookRegistrar()
    await registrar.install(rubika, "https://x/rubika/s", "s", WebhookOptions())
    await registrar.install_inline(rubika, "https://x/rubika/s/inline")
    assert tg_client.calls[0][0] == "set_webhook"
    assert tg_client.calls[0][1][0] == "https://x/tg/s"
    assert tg_client.calls[0][1][1]["secret_token"] == "s"
    assert bale_client.calls == [("set_webhook", ("https://x/bale/s", {}))]
    assert rubika_client.calls == [
        ("update_bot_endpoints", ("https://x/rubika/s", "ReceiveUpdate")),
        ("update_bot_endpoints", ("https://x/rubika/s/inline", "ReceiveInlineMessage")),
    ]
