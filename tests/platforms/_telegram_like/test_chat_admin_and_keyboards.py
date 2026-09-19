"""M5 contract tests for shared chat-admin and keyboard mechanics."""

from __future__ import annotations

from typing import Any, Dict, Optional

import orjson
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms._telegram_like import TelegramLikeClient
from peyk.platforms.bale.client import BaleClient, build_inline_keyboard_button as build_bale_button
from peyk.platforms.bale.models import Chat, ChatMember, ChatMemberAdministrator
from peyk.platforms.telegram.client import TelegramClient, build_inline_keyboard_button as build_telegram_button
from peyk.platforms.telegram.models import ChatFullInfo, ChatMemberAdministrator as TelegramChatMemberAdministrator, ChatMemberBanned
from peyk.transport.errors import TransportError


class FakeAPIError(TransportError):
    def __init__(self, message: str, *, error_code: int, description: str, parameters: Optional[Any] = None) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.description = description
        self.parameters = parameters


class FakeChat:
    @classmethod
    def from_dict(cls, data):
        return ("chat", data)


def fake_member_parser(data):
    return ("member", data) if data is not None else None


class FakeClient(TelegramLikeClient):
    base_url = "PLACEHOLDER"
    _error_class = FakeAPIError
    chat_model = FakeChat
    chat_member_parser = staticmethod(fake_member_parser)
    chat_member_count_method = "fakeChatMemberCount"


class Server:
    def __init__(self):
        self.requests = []
        self.member_result = {"status": "member", "user": {"id": 7, "is_bot": False, "first_name": "U"}}
        self.app = web.Application()
        self.app.router.add_post("/bot{token}/{method}", self.handle)

    async def handle(self, request):
        raw = await request.read()
        body = orjson.loads(raw) if raw else {}
        method = request.match_info["method"]
        self.requests.append((method, body))
        results = {
            "unbanChatMember": True,
            "unpinAllChatMessages": True,
            "leaveChat": True,
            "getChat": {"id": 10, "type": "group", "title": "demo"},
            "getChatMember": self.member_result,
            "fakeChatMemberCount": 9,
            "getChatMembersCount": 9,
            "getChatMemberCount": 11,
            "setChatTitle": True,
            "deleteChatPhoto": True,
        }
        return web.json_response({"ok": True, "result": results.get(method)})


@pytest.mark.asyncio
async def test_fake_subclass_uses_shared_admin_dispatch(fake_server_unused=None):
    server = Server()
    async with TestServer(server.app) as ts:
        FakeClient.base_url = str(ts.make_url(""))
        client = FakeClient("TOKEN")
        try:
            assert await client.unban_chat_member(1, 2, only_if_banned=True) is True
            assert await client.unpin_all_chat_messages(1) is True
            assert await client.leave_chat(1) is True
            assert await client.get_chat(1) == ("chat", {"id": 10, "type": "group", "title": "demo"})
            assert await client.get_chat_member(1, 2) == ("member", {"status": "member", "user": {"id": 7, "is_bot": False, "first_name": "U"}})
            assert await client._get_chat_member_count(1) == 9
            assert await client.set_chat_title(1, "new") is True
            assert await client.delete_chat_photo(1) is True
        finally:
            await client.close()
    assert server.requests[0] == ("unbanChatMember", {"chat_id": 1, "user_id": 2, "only_if_banned": True})


def test_shared_keyboard_builder_is_platform_neutral():
    assert TelegramLikeClient._build_inline_keyboard_button_payload("OK", "go") == {"text": "OK", "callback_data": "go"}
    with pytest.raises(ValueError):
        TelegramLikeClient._build_inline_keyboard_button_payload("bad", "x" * 65)
    assert build_bale_button("OK", "go") == {"text": "OK", "callback_data": "go"}
    button = build_telegram_button("OK", "go")
    assert button.text == "OK" and button.callback_data == "go"


def test_a_chat_methods_are_inherited_and_b_methods_remain_platform_owned():
    a_methods = {
        "unban_chat_member", "unpin_all_chat_messages", "leave_chat",
        "get_chat", "get_chat_member", "set_chat_title", "delete_chat_photo",
    }
    for cls in (BaleClient, TelegramClient):
        assert all(name not in cls.__dict__ for name in a_methods)
        assert all(getattr(cls, name) is getattr(TelegramLikeClient, name) for name in a_methods)


def test_m1_b_methods_remain_platform_owned():
    for cls in (BaleClient, TelegramClient):
        assert "ban_chat_member" in cls.__dict__
        assert "get_chat_administrators" in cls.__dict__
        assert "pin_chat_message" in cls.__dict__
        assert "answer_callback_query" in cls.__dict__
    assert "promote_chat_member" in TelegramClient.__dict__
    assert "restrict_chat_member" in TelegramClient.__dict__


@pytest.mark.asyncio
async def test_real_bale_subclass_parses_bale_chat_member_shape():
    server = Server()
    async with TestServer(server.app) as ts:
        BaleClient.base_url = str(ts.make_url(""))
        client = BaleClient("TOKEN")
        try:
            member = await client.get_chat_member(1, 7)
            assert isinstance(member, ChatMember)
            assert member.status == "member"
            assert await client.get_chat_members_count(1) == 9
            assert isinstance(await client.get_chat(1), Chat)
        finally:
            await client.close()


@pytest.mark.asyncio
async def test_real_telegram_subclass_parses_tagged_chat_member_shape():
    server = Server()
    async with TestServer(server.app) as ts:
        TelegramClient.base_url = str(ts.make_url(""))
        client = TelegramClient("TOKEN")
        try:
            member = await client.get_chat_member(1, 7)
            assert isinstance(member, TelegramChatMemberAdministrator) is False
            assert member.status == "member"
            assert await client.get_chat_member_count(1) == 11
            assert isinstance(await client.get_chat(1), ChatFullInfo)
        finally:
            await client.close()


@pytest.mark.asyncio
async def test_telegram_kicked_shape_stays_banned_subtype():
    server = Server()
    server.member_result = {
        "status": "kicked",
        "user": {"id": 7, "is_bot": False, "first_name": "U"},
        "until_date": 5,
    }
    async with TestServer(server.app) as ts:
        TelegramClient.base_url = str(ts.make_url(""))
        client = TelegramClient("TOKEN")
        try:
            member = await client.get_chat_member(1, 7)
            assert isinstance(member, ChatMemberBanned)
            assert member.status == "kicked"
        finally:
            await client.close()
