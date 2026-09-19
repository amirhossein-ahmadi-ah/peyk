"""Tests for `TelegramClient` chat-administration methods (Phase T5).

Fake `aiohttp.test_utils` server, zero real network. One happy-path
test per method (28 methods), tagged-union dispatch over 4 `ChatMember`
subtypes, and request-side serialization of `ChatPermissions` /
administrator rights.
"""

from __future__ import annotations

from typing import Any, Callable, Dict

import orjson
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms.telegram.client import TelegramClient
from peyk.platforms.telegram.models import (
    ChatAdministratorRights,
    ChatFullInfo,
    ChatInviteLink,
    ChatJoinRequest,
    ChatMemberAdministrator,
    ChatMemberBanned,
    ChatMemberLeft,
    ChatMemberMember,
    ChatMemberOwner,
    ChatMemberRestricted,
    ChatMemberUpdated,
    ChatPermissions,
    ChatPhoto,
    parse_chat_member,
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
    "type": "supergroup",
    "title": "Group",
}


def _sample_invite_link_raw() -> Dict[str, Any]:
    return {
        "invite_link": "https://t.me/+abc",
        "creator": SAMPLE_USER_RAW,
        "creates_join_request": False,
        "is_primary": False,
        "is_revoked": False,
        "name": "link1",
        "member_limit": 10,
        "pending_join_request_count": 2,
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
        content_type = request.headers.get("Content-Type", "")
        if "multipart/form-data" in content_type:
            reader = await request.multipart()
            fields: Dict[str, str] = {}
            files: Dict[str, Dict[str, Any]] = {}
            async for part in reader:
                if part.filename:
                    files[part.name] = {
                        "filename": part.filename,
                        "content": await part.read(decode=False),
                    }
                else:
                    fields[part.name] = await part.text()
            parsed_body: Any = {
                "multipart": True, "fields": fields, "files": files,
            }
        else:
            raw = await request.read()
            parsed_body = orjson.loads(raw) if raw else {}
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


def _client_for(test_server: TestServer) -> TelegramClient:
    base_url = str(test_server.make_url("")).rstrip("/")
    return TelegramClient(
        TOKEN,
        base_url=base_url,
        retry_policy=RetryPolicy(max_attempts=3, base_backoff_seconds=0.001),
    )


async def _bool_method(
    fake_server, method: str, call, expected: Dict[str, Any]
) -> None:
    server, test_server = fake_server
    server.set_response(method, lambda body: True)
    client = _client_for(test_server)
    try:
        assert await call(client) is True
    finally:
        await client.close()
    assert server.calls_for(method)[-1]["body"] == expected


async def test_ban_chat_member(fake_server) -> None:
    await _bool_method(
        fake_server, "banChatMember",
        lambda c: c.ban_chat_member(-100, 7, until_date=999,
                                    revoke_messages=True),
        {"chat_id": -100, "user_id": 7, "until_date": 999,
         "revoke_messages": True},
    )


async def test_unban_chat_member(fake_server) -> None:
    await _bool_method(
        fake_server, "unbanChatMember",
        lambda c: c.unban_chat_member(-100, 7, only_if_banned=True),
        {"chat_id": -100, "user_id": 7, "only_if_banned": True},
    )


async def test_restrict_chat_member_serializes_permissions(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("restrictChatMember", lambda body: True)
    client = _client_for(test_server)
    try:
        ok = await client.restrict_chat_member(
            -100, 7,
            ChatPermissions(can_send_messages=False,
                            can_react_to_messages=True),
            until_date=999,
        )
    finally:
        await client.close()
    assert ok is True
    assert server.calls_for("restrictChatMember")[0]["body"] == {
        "chat_id": -100, "user_id": 7,
        "permissions": {"can_send_messages": False,
                        "can_react_to_messages": True},
        "until_date": 999,
    }


async def test_promote_chat_member_serializes_rights(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("promoteChatMember", lambda body: True)
    client = _client_for(test_server)
    try:
        ok = await client.promote_chat_member(
            -100, 7, can_change_info=True, can_invite_users=True,
            can_send_welcome_messages=True, can_manage_tags=True,
        )
    finally:
        await client.close()
    assert ok is True
    assert server.calls_for("promoteChatMember")[0]["body"] == {
        "chat_id": -100, "user_id": 7, "can_change_info": True,
        "can_invite_users": True, "can_send_welcome_messages": True,
        "can_manage_tags": True,
    }


async def test_set_chat_administrator_custom_title(fake_server) -> None:
    await _bool_method(
        fake_server, "setChatAdministratorCustomTitle",
        lambda c: c.set_chat_administrator_custom_title(-100, 7, "boss"),
        {"chat_id": -100, "user_id": 7, "custom_title": "boss"},
    )


async def test_ban_unban_chat_sender_chat(fake_server) -> None:
    await _bool_method(
        fake_server, "banChatSenderChat",
        lambda c: c.ban_chat_sender_chat(-100, -200),
        {"chat_id": -100, "sender_chat_id": -200},
    )
    await _bool_method(
        fake_server, "unbanChatSenderChat",
        lambda c: c.unban_chat_sender_chat(-100, -200),
        {"chat_id": -100, "sender_chat_id": -200},
    )


async def test_set_chat_permissions(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setChatPermissions", lambda body: True)
    client = _client_for(test_server)
    try:
        ok = await client.set_chat_permissions(
            -100, {"can_send_messages": True},
            use_independent_chat_permissions=True,
        )
    finally:
        await client.close()
    assert ok is True
    assert server.calls_for("setChatPermissions")[0]["body"] == {
        "chat_id": -100, "permissions": {"can_send_messages": True},
        "use_independent_chat_permissions": True,
    }


async def test_invite_link_methods(fake_server) -> None:
    server, test_server = fake_server
    for method in ("exportChatInviteLink", "createChatInviteLink",
                   "editChatInviteLink", "revokeChatInviteLink"):
        server.set_response(method, lambda body: _sample_invite_link_raw())
    client = _client_for(test_server)
    try:
        exported = await client.export_chat_invite_link(-100)
        assert isinstance(exported, ChatInviteLink)
        assert exported.invite_link == "https://t.me/+abc"
        assert exported.creator.id == 100
        assert exported.name == "link1"
        created = await client.create_chat_invite_link(
            -100, name="n", member_limit=5, creates_join_request=True
        )
        assert created.member_limit == 10  # server echo, proves parsing
        edited = await client.edit_chat_invite_link(
            -100, "https://t.me/+abc", name="n2"
        )
        assert edited.name == "link1"
        revoked = await client.revoke_chat_invite_link(
            -100, "https://t.me/+abc"
        )
        assert revoked.is_revoked is False
    finally:
        await client.close()
    assert server.calls_for("exportChatInviteLink")[0]["body"] == {
        "chat_id": -100
    }
    assert server.calls_for("createChatInviteLink")[0]["body"] == {
        "chat_id": -100, "name": "n", "member_limit": 5,
        "creates_join_request": True,
    }
    assert server.calls_for("editChatInviteLink")[0]["body"] == {
        "chat_id": -100, "invite_link": "https://t.me/+abc", "name": "n2",
    }
    assert server.calls_for("revokeChatInviteLink")[0]["body"] == {
        "chat_id": -100, "invite_link": "https://t.me/+abc",
    }


async def test_approve_decline_join_request(fake_server) -> None:
    await _bool_method(
        fake_server, "approveChatJoinRequest",
        lambda c: c.approve_chat_join_request(-100, 7),
        {"chat_id": -100, "user_id": 7},
    )
    await _bool_method(
        fake_server, "declineChatJoinRequest",
        lambda c: c.decline_chat_join_request(-100, 7),
        {"chat_id": -100, "user_id": 7},
    )


async def test_set_chat_photo_upload_and_reject_str(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setChatPhoto", lambda body: True)
    client = _client_for(test_server)
    try:
        assert await client.set_chat_photo(-100, b"JPEG") is True
        with pytest.raises(ValueError):
            await client.set_chat_photo(-100, "FILE_ID")
    finally:
        await client.close()
    body = server.calls_for("setChatPhoto")[0]["body"]
    assert body["multipart"] is True
    assert body["fields"] == {"chat_id": "-100"}
    assert body["files"]["photo"]["content"] == b"JPEG"


async def test_delete_chat_photo_title_description(fake_server) -> None:
    await _bool_method(
        fake_server, "deleteChatPhoto",
        lambda c: c.delete_chat_photo(-100), {"chat_id": -100},
    )
    await _bool_method(
        fake_server, "setChatTitle",
        lambda c: c.set_chat_title(-100, "New"),
        {"chat_id": -100, "title": "New"},
    )
    await _bool_method(
        fake_server, "setChatDescription",
        lambda c: c.set_chat_description(-100, description="Desc"),
        {"chat_id": -100, "description": "Desc"},
    )


async def test_pin_unpin_leave(fake_server) -> None:
    await _bool_method(
        fake_server, "pinChatMessage",
        lambda c: c.pin_chat_message(-100, 9, disable_notification=True),
        {"chat_id": -100, "message_id": 9, "disable_notification": True},
    )
    await _bool_method(
        fake_server, "unpinChatMessage",
        lambda c: c.unpin_chat_message(-100, 9),
        {"chat_id": -100, "message_id": 9},
    )
    await _bool_method(
        fake_server, "unpinChatMessage",
        lambda c: c.unpin_chat_message(-100),
        {"chat_id": -100},
    )
    await _bool_method(
        fake_server, "unpinAllChatMessages",
        lambda c: c.unpin_all_chat_messages(-100), {"chat_id": -100},
    )
    await _bool_method(
        fake_server, "leaveChat",
        lambda c: c.leave_chat(-100), {"chat_id": -100},
    )


async def test_get_chat(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "getChat",
        lambda body: {
            "id": -100, "type": "supergroup", "title": "Group",
            "description": "A group",
            "photo": {"small_file_id": "s", "small_file_unique_id": "su",
                      "big_file_id": "b", "big_file_unique_id": "bu"},
            "pinned_message": None,
        },
    )
    client = _client_for(test_server)
    try:
        chat = await client.get_chat(-100)
    finally:
        await client.close()
    assert isinstance(chat, ChatFullInfo)
    assert chat.title == "Group"
    assert chat.photo == ChatPhoto("s", "su", "b", "bu")
    assert server.calls_for("getChat")[0]["body"] == {"chat_id": -100}


async def test_get_chat_administrators_with_return_bots(fake_server) -> None:
    server, test_server = fake_server

    def _result(body: Any) -> Any:
        assert body == {"chat_id": -100, "return_bots": True}
        return [
            {"status": "creator", "user": SAMPLE_USER_RAW,
             "is_anonymous": False},
            {"status": "administrator", "user": SAMPLE_USER_RAW,
             "can_be_edited": True, "can_change_info": True,
             "can_send_welcome_messages": True},
        ]

    server.set_response("getChatAdministrators", _result)
    client = _client_for(test_server)
    try:
        admins = await client.get_chat_administrators(-100, return_bots=True)
    finally:
        await client.close()
    assert isinstance(admins[0], ChatMemberOwner)
    assert isinstance(admins[1], ChatMemberAdministrator)
    assert admins[1].can_send_welcome_messages is True


async def test_get_chat_member_count(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("getChatMemberCount", lambda body: 42)
    client = _client_for(test_server)
    try:
        assert await client.get_chat_member_count(-100) == 42
    finally:
        await client.close()


async def test_get_chat_member_subtypes(fake_server) -> None:
    server, test_server = fake_server
    raws = {
        "administrator": {"status": "administrator",
                          "user": SAMPLE_USER_RAW,
                          "can_be_edited": False,
                          "can_manage_chat": True},
        "member": {"status": "member", "user": SAMPLE_USER_RAW},
        "restricted": {"status": "restricted", "user": SAMPLE_USER_RAW,
                       "is_member": True, "can_send_messages": True,
                       "can_react_to_messages": False,
                       "until_date": 999},
        "kicked": {"status": "kicked", "user": SAMPLE_USER_RAW,
                   "until_date": 0},
    }
    for status, raw in raws.items():
        server.set_response("getChatMember", lambda body, r=raw: r)
        client = _client_for(test_server)
        try:
            member = await client.get_chat_member(-100, 7)
        finally:
            await client.close()
        if status == "administrator":
            assert isinstance(member, ChatMemberAdministrator)
            assert member.can_manage_chat is True
        elif status == "member":
            assert isinstance(member, ChatMemberMember)
        elif status == "restricted":
            assert isinstance(member, ChatMemberRestricted)
            assert member.is_member is True
            assert member.can_react_to_messages is False
        else:
            assert isinstance(member, ChatMemberBanned)
            assert member.until_date == 0


async def test_parse_chat_member_unknown_status() -> None:
    with pytest.raises(ValueError):
        parse_chat_member({"status": "ghost", "user": SAMPLE_USER_RAW})
    assert parse_chat_member(None) is None


async def test_set_delete_chat_sticker_set(fake_server) -> None:
    await _bool_method(
        fake_server, "setChatStickerSet",
        lambda c: c.set_chat_sticker_set(-100, "set_name"),
        {"chat_id": -100, "sticker_set_name": "set_name"},
    )
    await _bool_method(
        fake_server, "deleteChatStickerSet",
        lambda c: c.delete_chat_sticker_set(-100), {"chat_id": -100},
    )


async def test_chat_member_updated_and_join_request_models() -> None:
    updated = ChatMemberUpdated.from_dict(
        {
            "chat": SAMPLE_CHAT_RAW,
            "from": SAMPLE_USER_RAW,
            "date": 1690000000,
            "old_chat_member": {"status": "left",
                                "user": SAMPLE_USER_RAW},
            "new_chat_member": {"status": "member",
                                "user": SAMPLE_USER_RAW},
            "via_join_request": True,
        }
    )
    assert isinstance(updated.old_chat_member, ChatMemberLeft)
    assert isinstance(updated.new_chat_member, ChatMemberMember)
    assert updated.via_join_request is True

    req = ChatJoinRequest.from_dict(
        {
            "chat": SAMPLE_CHAT_RAW,
            "from": SAMPLE_USER_RAW,
            "user_chat_id": 555,
            "date": 1690000000,
            "bio": "hi",
            "invite_link": _sample_invite_link_raw(),
            "query_id": "q1",
        }
    )
    assert req.user_chat_id == 555
    assert req.query_id == "q1"
    assert req.invite_link.name == "link1"

    rights = ChatAdministratorRights.from_dict(
        {"can_manage_chat": True, "can_send_welcome_messages": True}
    )
    assert rights.to_dict() == {"can_manage_chat": True,
                                "can_send_welcome_messages": True}
    perms = ChatPermissions.from_dict({"can_send_messages": True})
    assert perms.to_dict() == {"can_send_messages": True}
