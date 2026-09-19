"""M3 contract tests for shared core/text methods."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import orjson
import pytest
import pytest_asyncio
from aiohttp import web

from peyk.platforms._telegram_like import TelegramLikeClient
from peyk.platforms.bale.client import BaleClient
from peyk.platforms.bale.models import User as BaleUser
from peyk.platforms.bale.models import WebhookInfo as BaleWebhookInfo
from peyk.platforms.telegram.client import TelegramClient
from peyk.platforms.telegram.models import User as TelegramUser
from peyk.platforms.telegram.models import WebhookInfo as TelegramWebhookInfo


@dataclass
class FakeUser:
    value: dict

    @classmethod
    def from_dict(cls, data):
        return cls(data)


@dataclass
class FakeWebhookInfo:
    value: dict

    @classmethod
    def from_dict(cls, data):
        return cls(data)


class FakeClient(TelegramLikeClient):
    base_url = "PLACEHOLDER"
    _error_class = RuntimeError
    user_model = FakeUser
    webhook_info_model = FakeWebhookInfo


class Server:
    def __init__(self) -> None:
        self.requests: list[Dict[str, Any]] = []
        self.responses: Dict[str, Any] = {}
        self.app = web.Application()
        self.app.router.add_post("/bot{token}/{method}", self.handle)

    async def handle(self, request: web.Request) -> web.Response:
        raw = await request.read()
        body = orjson.loads(raw) if raw else {}
        method = request.match_info["method"]
        self.requests.append({"method": method, "body": body})
        return web.json_response(self.responses.get(method, {"ok": True, "result": None}))


@pytest_asyncio.fixture
async def server():
    api = Server()
    runner = web.AppRunner(api.app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    port = site._server.sockets[0].getsockname()[1]
    try:
        yield api, f"http://127.0.0.1:{port}"
    finally:
        await runner.cleanup()


@pytest.mark.asyncio
async def test_shared_core_methods_work_on_fake_subclass(server):
    api, base_url = server
    FakeClient.base_url = base_url
    client = FakeClient("TOKEN")
    try:
        api.responses["getMe"] = {"ok": True, "result": {"id": 1}}
        api.responses["getWebhookInfo"] = {
            "ok": True,
            "result": {"url": "https://example.test/hook"},
        }
        api.responses["deleteMessage"] = {"ok": True, "result": True}

        assert (await client.get_me()).value == {"id": 1}
        assert (await client.get_webhook_info()).value == {
            "url": "https://example.test/hook"
        }
        assert await client.delete_message(123, 7) is True
    finally:
        await client.close()

    assert [r["method"] for r in api.requests] == [
        "getMe",
        "getWebhookInfo",
        "deleteMessage",
    ]
    assert api.requests[-1]["body"] == {"chat_id": 123, "message_id": 7}


@pytest.mark.parametrize(
    ("client_cls", "user_model", "webhook_model", "user_result", "webhook_result"),
    [
        (BaleClient, BaleUser, BaleWebhookInfo, {"id": 11, "is_bot": True, "first_name": "Bale"}, {"url": "https://bale.test/hook"}),
        (TelegramClient, TelegramUser, TelegramWebhookInfo, {"id": 22, "is_bot": True, "first_name": "Telegram"}, {"url": "https://telegram.test/hook", "pending_update_count": 2}),
    ],
)
@pytest.mark.asyncio
async def test_real_clients_use_the_same_inherited_core_path(
    server, client_cls, user_model, webhook_model, user_result, webhook_result
):
    api, base_url = server
    api.responses["getMe"] = {"ok": True, "result": user_result}
    api.responses["getWebhookInfo"] = {"ok": True, "result": webhook_result}
    api.responses["deleteMessage"] = {"ok": True, "result": True}

    client = client_cls("TOKEN", base_url=base_url)
    try:
        me = await client.get_me()
        info = await client.get_webhook_info()
        deleted = await client.delete_message(200, 5)
    finally:
        await client.close()

    assert isinstance(me, user_model)
    assert isinstance(info, webhook_model)
    assert deleted is True
    assert [r["method"] for r in api.requests] == [
        "getMe",
        "getWebhookInfo",
        "deleteMessage",
    ]
    assert api.requests[2]["body"] == {"chat_id": 200, "message_id": 5}


def test_migrated_methods_are_inherited_not_shadowed():
    for method in ("get_me", "get_webhook_info", "delete_message"):
        assert getattr(BaleClient, method) is getattr(TelegramLikeClient, method)
        assert getattr(TelegramClient, method) is getattr(TelegramLikeClient, method)
