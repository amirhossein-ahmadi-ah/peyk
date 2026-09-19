"""Tests for `BaleClient`.

Uses `aiohttp.test_utils` to run a local fake server that speaks the real
Bale response shape (`ok`/`result`/`description`/`error_code`) -- zero
real network calls, same approach as Phase A's transport tests. The fake
server records the last request it saw (method name, JSON body or parsed
multipart fields/files, HTTP method) so tests can assert on request shape,
not just on the parsed model coming back.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional

import orjson
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms.bale.client import (
    BaleClient,
    InputMediaPhoto,
    InputMediaVideo,
)
from peyk.platforms.bale.errors import BaleAPIError
from peyk.platforms.bale.models import (
    Chat,
    ChatMember,
    ChatMemberAdministrator,
    File,
    Message,
    Update,
    User,
    WebhookInfo,
)
from peyk.transport import FilePayload, RetryPolicy
from peyk.transport.errors import HTTPStatusError

TOKEN = "12345:TEST-TOKEN"

SAMPLE_USER_RAW = {
    "id": 100,
    "is_bot": True,
    "first_name": "TestBot",
    "last_name": None,
    "username": "test_bot",
    "language_code": None,
}

SAMPLE_CHAT_RAW = {
    "id": 200,
    "type": "private",
    "title": None,
    "username": "someone",
    "first_name": "Some",
    "last_name": "One",
    "photo": None,
}


def _sample_message_raw(message_id: int = 1) -> Dict[str, Any]:
    return {
        "message_id": message_id,
        "from": SAMPLE_USER_RAW,
        "date": 1690000000,
        "chat": SAMPLE_CHAT_RAW,
        "reply_to_message": None,
        "text": "hello",
        "caption": None,
        "photo": None,
        "document": None,
        "sticker": None,
        "reply_markup": None,
    }


class FakeBaleServer:
    """A minimal aiohttp app that mimics `tapi.bale.ai`'s routing/response shape.

    `responses` maps a Bale method name to a callable that receives the
    parsed request (JSON dict, or `{"fields": ..., "files": ...}` for a
    multipart request) and returns the raw dict to send back as the `ok`
    envelope's `result` (or the whole envelope dict if `raw_envelope` is
    used -- see `set_raw_response`).
    """

    def __init__(self) -> None:
        self.responses: Dict[str, Callable[[Any], Any]] = {}
        self.raw_envelopes: Dict[str, Any] = {}
        self.request_log: list[Dict[str, Any]] = []
        self.app = web.Application()
        self.app.router.add_route("GET", "/bot{token}/{method}", self._handle)
        self.app.router.add_route("POST", "/bot{token}/{method}", self._handle)

    def set_response(self, method_name: str, result_builder: Callable[[Any], Any]) -> None:
        self.responses[method_name] = result_builder

    def set_raw_envelope(self, method_name: str, envelope: Any) -> None:
        """Bypass the ok:true wrapping entirely -- for ok:false tests."""
        self.raw_envelopes[method_name] = envelope

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
                    content = await part.read(decode=False)
                    files[part.name] = {
                        "filename": part.filename,
                        "content_type": part.headers.get("Content-Type"),
                        "content": content,
                    }
                else:
                    fields[part.name] = await part.text()
            parsed_body: Any = {"fields": fields, "files": files}
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
    server = FakeBaleServer()
    async with TestServer(server.app) as test_server:
        base_url = str(test_server.make_url("")).rstrip("/")
        yield server, base_url


@pytest.fixture
async def client(fake_server):
    server, base_url = fake_server
    bale_client = BaleClient(TOKEN, base_url=base_url)
    yield bale_client, server
    await bale_client.close()


# -- Bot info -----------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_me(client) -> None:
    bale_client, server = client
    server.set_response("getMe", lambda body: SAMPLE_USER_RAW)

    user = await bale_client.get_me()

    assert user == User.from_dict(SAMPLE_USER_RAW)
    call = server.calls_for("getMe")[0]
    assert call["token"] == TOKEN
    assert call["http_method"] == "POST"


# -- Messages -------------------------------------------------------------------


@pytest.mark.asyncio
async def test_send_message(client) -> None:
    bale_client, server = client
    server.set_response("sendMessage", lambda body: _sample_message_raw())

    message = await bale_client.send_message(200, "hello", reply_to_message_id=9)

    assert message == Message.from_dict(_sample_message_raw())
    call = server.calls_for("sendMessage")[0]
    assert call["body"] == {
        "chat_id": 200,
        "text": "hello",
        "reply_to_message_id": 9,
    }


@pytest.mark.asyncio
async def test_edit_message_text(client) -> None:
    bale_client, server = client
    server.set_response(
        "editMessageText", lambda body: _sample_message_raw(message_id=5)
    )

    message = await bale_client.edit_message_text(200, 5, "updated text")

    assert message.message_id == 5
    call = server.calls_for("editMessageText")[0]
    assert call["body"] == {"chat_id": 200, "message_id": 5, "text": "updated text"}


@pytest.mark.asyncio
async def test_edit_message_caption(client) -> None:
    bale_client, server = client
    server.set_response(
        "editMessageCaption", lambda body: _sample_message_raw(message_id=5)
    )

    message = await bale_client.edit_message_caption(200, 5, caption="new caption")

    assert message.message_id == 5
    call = server.calls_for("editMessageCaption")[0]
    assert call["body"] == {
        "chat_id": 200,
        "message_id": 5,
        "caption": "new caption",
    }


@pytest.mark.asyncio
async def test_edit_message_reply_markup(client) -> None:
    bale_client, server = client
    server.set_response(
        "editMessageReplyMarkup", lambda body: _sample_message_raw(message_id=5)
    )

    reply_markup = {"inline_keyboard": [[{"text": "Ok", "callback_data": "ok"}]]}
    message = await bale_client.edit_message_reply_markup(
        200, 5, reply_markup=reply_markup
    )

    assert message.message_id == 5
    call = server.calls_for("editMessageReplyMarkup")[0]
    assert call["body"] == {"chat_id": 200, "message_id": 5, "reply_markup": reply_markup}


@pytest.mark.asyncio
async def test_delete_message(client) -> None:
    bale_client, server = client
    server.set_response("deleteMessage", lambda body: True)

    result = await bale_client.delete_message(200, 5)

    assert result is True
    call = server.calls_for("deleteMessage")[0]
    assert call["body"] == {"chat_id": 200, "message_id": 5}


@pytest.mark.asyncio
async def test_forward_message(client) -> None:
    bale_client, server = client
    server.set_response(
        "forwardMessage", lambda body: _sample_message_raw(message_id=7)
    )

    message = await bale_client.forward_message(200, 300, 5)

    assert message.message_id == 7
    call = server.calls_for("forwardMessage")[0]
    assert call["body"] == {"chat_id": 200, "from_chat_id": 300, "message_id": 5}


@pytest.mark.asyncio
async def test_copy_message(client) -> None:
    bale_client, server = client
    server.set_response("copyMessage", lambda body: {"message_id": 42})

    result = await bale_client.copy_message(200, 300, 5)

    assert result == {"message_id": 42}
    call = server.calls_for("copyMessage")[0]
    assert call["body"] == {"chat_id": 200, "from_chat_id": 300, "message_id": 5}


# -- Chat / member management ---------------------------------------------------


@pytest.mark.asyncio
async def test_ban_chat_member(client) -> None:
    bale_client, server = client
    server.set_response("banChatMember", lambda body: True)

    result = await bale_client.ban_chat_member(200, 7)

    assert result is True
    assert server.calls_for("banChatMember")[0]["body"] == {
        "chat_id": 200,
        "user_id": 7,
    }


@pytest.mark.asyncio
async def test_unban_chat_member(client) -> None:
    bale_client, server = client
    server.set_response("unbanChatMember", lambda body: True)

    result = await bale_client.unban_chat_member(200, 7)

    assert result is True
    assert server.calls_for("unbanChatMember")[0]["body"] == {
        "chat_id": 200,
        "user_id": 7,
    }


@pytest.mark.asyncio
async def test_pin_chat_message(client) -> None:
    bale_client, server = client
    server.set_response("pinChatMessage", lambda body: True)

    result = await bale_client.pin_chat_message(200, 5)

    assert result is True
    assert server.calls_for("pinChatMessage")[0]["body"] == {
        "chat_id": 200,
        "message_id": 5,
    }


@pytest.mark.asyncio
async def test_unpin_chat_message(client) -> None:
    bale_client, server = client
    server.set_response("unpinChatMessage", lambda body: True)

    result = await bale_client.unpin_chat_message(200, 5)

    assert result is True
    assert server.calls_for("unpinChatMessage")[0]["body"] == {
        "chat_id": 200,
        "message_id": 5,
    }


@pytest.mark.asyncio
async def test_leave_chat(client) -> None:
    bale_client, server = client
    server.set_response("leaveChat", lambda body: True)

    result = await bale_client.leave_chat(200)

    assert result is True
    assert server.calls_for("leaveChat")[0]["body"] == {"chat_id": 200}


@pytest.mark.asyncio
async def test_get_chat(client) -> None:
    bale_client, server = client
    server.set_response("getChat", lambda body: SAMPLE_CHAT_RAW)

    chat = await bale_client.get_chat(200)

    assert chat == Chat.from_dict(SAMPLE_CHAT_RAW)
    assert server.calls_for("getChat")[0]["body"] == {"chat_id": 200}


@pytest.mark.asyncio
async def test_get_chat_administrators(client) -> None:
    bale_client, server = client
    raw_admins = [
        {
            "status": "administrator",
            "user": {"id": 2, "is_bot": False, "first_name": "Admin"},
            "can_delete_messages": True,
            "can_manage_video_chats": True,
            "can_restrict_members": False,
            "can_promote_members": False,
            "can_change_info": True,
            "can_invite_users": True,
            "can_post_stories": True,
            "can_post_messages": True,
            "can_edit_messages": False,
            "can_pin_messages": True,
        },
        {
            "status": "member",
            "user": {"id": 3, "is_bot": False, "first_name": "User"},
        },
    ]
    server.set_response("getChatAdministrators", lambda body: raw_admins)

    result = await bale_client.get_chat_administrators(200)

    assert len(result) == 2
    assert isinstance(result[0], ChatMemberAdministrator)
    assert isinstance(result[1], ChatMember)
    assert result[0].can_delete_messages is True
    assert result[1].user.first_name == "User"
    assert server.calls_for("getChatAdministrators")[0]["body"] == {"chat_id": 200}


@pytest.mark.asyncio
async def test_get_chat_member_returns_chat_member(client) -> None:
    bale_client, server = client
    raw = {
        "status": "administrator",
        "user": {"id": 2, "is_bot": False, "first_name": "Admin"},
        "can_delete_messages": True,
    }
    server.set_response("getChatMember", lambda body: raw)

    result = await bale_client.get_chat_member(200, 100)

    assert isinstance(result, ChatMemberAdministrator)
    assert result.can_delete_messages is True
    assert result.user == User(id=2, is_bot=False, first_name="Admin")
    assert server.calls_for("getChatMember")[0]["body"] == {
        "chat_id": 200,
        "user_id": 100,
    }


@pytest.mark.asyncio
async def test_get_chat_members_count(client) -> None:
    bale_client, server = client
    server.set_response("getChatMembersCount", lambda body: 42)

    result = await bale_client.get_chat_members_count(200)

    assert result == 42
    assert isinstance(result, int)
    assert server.calls_for("getChatMembersCount")[0]["body"] == {"chat_id": 200}


@pytest.mark.asyncio
async def test_create_chat_invite_link(client) -> None:
    bale_client, server = client
    server.set_response(
        "createChatInviteLink",
        lambda body: {"invite_link": "https://bale.ai/invite/abc"},
    )

    result = await bale_client.create_chat_invite_link(200)

    assert result == {"invite_link": "https://bale.ai/invite/abc"}
    assert server.calls_for("createChatInviteLink")[0]["body"] == {"chat_id": 200}


@pytest.mark.asyncio
async def test_revoke_chat_invite_link(client) -> None:
    bale_client, server = client
    server.set_response(
        "revokeChatInviteLink",
        lambda body: {"invite_link": "https://bale.ai/invite/abc", "is_revoked": True},
    )

    result = await bale_client.revoke_chat_invite_link(
        200, "https://bale.ai/invite/abc"
    )

    assert result["is_revoked"] is True
    assert server.calls_for("revokeChatInviteLink")[0]["body"] == {
        "chat_id": 200,
        "invite_link": "https://bale.ai/invite/abc",
    }


# -- Media: three distinct parameter shapes ---------------------------------------


@pytest.mark.asyncio
async def test_send_photo_with_file_id_string_sends_json_not_multipart(client) -> None:
    bale_client, server = client
    server.set_response("sendPhoto", lambda body: _sample_message_raw())

    message = await bale_client.send_photo(200, "AgACAgQAAxk...existing_file_id")

    assert message == Message.from_dict(_sample_message_raw())
    call = server.calls_for("sendPhoto")[0]
    assert call["body"] == {
        "chat_id": 200,
        "photo": "AgACAgQAAxk...existing_file_id",
    }


@pytest.mark.asyncio
async def test_send_photo_with_url_string_sends_json_not_multipart(client) -> None:
    bale_client, server = client
    server.set_response("sendPhoto", lambda body: _sample_message_raw())

    await bale_client.send_photo(
        200, "https://example.com/photo.jpg", caption="a caption"
    )

    call = server.calls_for("sendPhoto")[0]
    assert call["body"] == {
        "chat_id": 200,
        "photo": "https://example.com/photo.jpg",
        "caption": "a caption",
    }


@pytest.mark.asyncio
async def test_send_photo_uploads_raw_bytes_as_multipart(client) -> None:
    bale_client, server = client
    server.set_response("sendPhoto", lambda body: _sample_message_raw())

    raw_bytes = b"\x89PNG-fake-bytes-not-a-real-png"
    await bale_client.send_photo(200, raw_bytes, caption="uploaded")

    call = server.calls_for("sendPhoto")[0]
    assert call["body"]["fields"] == {"chat_id": "200", "caption": "uploaded"}
    uploaded_file = call["body"]["files"]["photo"]
    assert uploaded_file["content"] == raw_bytes
    assert uploaded_file["filename"] == "photo.jpg"


@pytest.mark.asyncio
async def test_send_document_uploads_streamed_file_as_multipart(client) -> None:
    import io

    bale_client, server = client
    server.set_response("sendDocument", lambda body: _sample_message_raw())

    stream_content = b"streamed document content, not read eagerly by us"
    stream = io.BytesIO(stream_content)
    payload = FilePayload(content=stream, filename="report.txt", content_type="text/plain")

    await bale_client.send_document(200, payload)

    call = server.calls_for("sendDocument")[0]
    uploaded_file = call["body"]["files"]["document"]
    assert uploaded_file["content"] == stream_content
    assert uploaded_file["filename"] == "report.txt"
    assert uploaded_file["content_type"] == "text/plain"


# -- Updates / webhook --------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_updates_request_shape_and_parsing(client) -> None:
    bale_client, server = client
    raw_updates = [
        {"update_id": 1, "message": _sample_message_raw(message_id=1)},
        {"update_id": 2, "message": _sample_message_raw(message_id=2)},
    ]
    server.set_response("getUpdates", lambda body: raw_updates)

    updates = await bale_client.get_updates(offset=5, limit=10, timeout=30)

    assert [u.update_id for u in updates] == [1, 2]
    assert isinstance(updates[0], Update)
    call = server.calls_for("getUpdates")[0]
    assert call["body"] == {"offset": 5, "limit": 10, "timeout": 30}


@pytest.mark.asyncio
async def test_get_updates_with_no_args_sends_empty_body(client) -> None:
    bale_client, server = client
    server.set_response("getUpdates", lambda body: [])

    updates = await bale_client.get_updates()

    assert updates == []
    call = server.calls_for("getUpdates")[0]
    assert call["body"] == {}


@pytest.mark.asyncio
async def test_set_webhook_request_shape(client) -> None:
    bale_client, server = client
    server.set_response("setWebhook", lambda body: True)

    result = await bale_client.set_webhook("https://example.com/webhook")

    assert result is True
    call = server.calls_for("setWebhook")[0]
    assert call["body"] == {"url": "https://example.com/webhook"}


@pytest.mark.asyncio
async def test_delete_webhook(client) -> None:
    bale_client, server = client
    server.set_response("deleteWebhook", lambda body: True)

    result = await bale_client.delete_webhook()

    assert result is True
    call = server.calls_for("deleteWebhook")[0]
    assert call["body"] == {}


@pytest.mark.asyncio
async def test_get_webhook_info(client) -> None:
    bale_client, server = client
    server.set_response(
        "getWebhookInfo",
        lambda body: {"url": "https://example.com/webhook"},
    )

    result = await bale_client.get_webhook_info()

    assert isinstance(result, WebhookInfo)
    assert result.url == "https://example.com/webhook"


# -- Bot lifecycle: logout / close_bot -----------------------------------------------


@pytest.mark.asyncio
async def test_logout(client) -> None:
    bale_client, server = client
    server.set_response("logout", lambda body: True)

    result = await bale_client.logout()

    assert result is True
    assert server.calls_for("logout")[0]["body"] == {}


@pytest.mark.asyncio
async def test_close_bot(client) -> None:
    """`close_bot()` wraps the API's `close` method, not this client's own `close()`."""
    bale_client, server = client
    server.set_response("close", lambda body: True)

    result = await bale_client.close_bot()

    assert result is True
    assert server.calls_for("close")[0]["body"] == {}


# -- Remaining send* media methods ----------------------------------------------------


@pytest.mark.asyncio
async def test_send_audio_with_file_id(client) -> None:
    bale_client, server = client
    server.set_response("sendAudio", lambda body: _sample_message_raw())

    await bale_client.send_audio(200, "existing_audio_file_id", caption="a song")

    call = server.calls_for("sendAudio")[0]
    assert call["body"] == {
        "chat_id": 200,
        "audio": "existing_audio_file_id",
        "caption": "a song",
    }


@pytest.mark.asyncio
async def test_send_audio_uploads_bytes_with_reply_markup(client) -> None:
    bale_client, server = client
    server.set_response("sendAudio", lambda body: _sample_message_raw())

    raw_bytes = b"fake-mp3-bytes"
    reply_markup = {"inline_keyboard": [[{"text": "Ok", "callback_data": "ok"}]]}
    await bale_client.send_audio(
        200, raw_bytes, reply_to_message_id=9, reply_markup=reply_markup
    )

    call = server.calls_for("sendAudio")[0]
    assert call["body"]["fields"]["chat_id"] == "200"
    assert call["body"]["fields"]["reply_to_message_id"] == "9"
    assert orjson.loads(call["body"]["fields"]["reply_markup"]) == reply_markup
    assert call["body"]["files"]["audio"]["content"] == raw_bytes


@pytest.mark.asyncio
async def test_send_video_with_url(client) -> None:
    bale_client, server = client
    server.set_response("sendVideo", lambda body: _sample_message_raw())

    await bale_client.send_video(200, "https://example.com/video.mp4")

    call = server.calls_for("sendVideo")[0]
    assert call["body"] == {"chat_id": 200, "video": "https://example.com/video.mp4"}


@pytest.mark.asyncio
async def test_send_animation_uploads_stream(client) -> None:
    import io

    bale_client, server = client
    server.set_response("sendAnimation", lambda body: _sample_message_raw())

    content = b"gif-bytes"
    stream = io.BytesIO(content)
    await bale_client.send_animation(200, FilePayload(content=stream, filename="a.gif"))

    call = server.calls_for("sendAnimation")[0]
    assert call["body"]["files"]["animation"]["content"] == content
    assert call["body"]["files"]["animation"]["filename"] == "a.gif"


@pytest.mark.asyncio
async def test_send_voice_with_file_id(client) -> None:
    bale_client, server = client
    server.set_response("sendVoice", lambda body: _sample_message_raw())

    await bale_client.send_voice(200, "existing_voice_file_id")

    call = server.calls_for("sendVoice")[0]
    assert call["body"] == {"chat_id": 200, "voice": "existing_voice_file_id"}


@pytest.mark.asyncio
async def test_send_chat_action(client) -> None:
    bale_client, server = client
    server.set_response("sendChatAction", lambda body: True)

    result = await bale_client.send_chat_action(200, "typing")

    assert result is True
    assert server.calls_for("sendChatAction")[0]["body"] == {
        "chat_id": 200,
        "action": "typing",
    }


@pytest.mark.asyncio
async def test_answer_callback_query(client) -> None:
    bale_client, server = client
    server.set_response("answerCallbackQuery", lambda body: True)

    result = await bale_client.answer_callback_query(
        "cbq_123", text="Done!", show_alert=False
    )

    assert result is True
    call = server.calls_for("answerCallbackQuery")[0]
    assert call["body"] == {
        "callback_query_id": "cbq_123",
        "text": "Done!",
        "show_alert": False,
    }


@pytest.mark.asyncio
async def test_ask_review(client) -> None:
    bale_client, server = client
    server.set_response("askReview", lambda body: True)

    result = await bale_client.ask_review(user_id=42, delay_seconds=60)

    assert result is True
    assert server.calls_for("askReview")[0]["body"] == {
        "user_id": 42,
        "delay_seconds": 60,
    }


@pytest.mark.asyncio
async def test_send_media_group_all_file_ids_sends_json(client) -> None:
    bale_client, server = client
    server.set_response(
        "sendMediaGroup",
        lambda body: [_sample_message_raw(1), _sample_message_raw(2)],
    )

    messages = await bale_client.send_media_group(
        200,
        [
            InputMediaPhoto(media="photo_file_id", caption="first"),
            InputMediaVideo(media="video_file_id", duration=30),
        ],
    )

    assert len(messages) == 2
    call = server.calls_for("sendMediaGroup")[0]
    assert call["body"] == {
        "chat_id": 200,
        "media": [
            {"type": "photo", "media": "photo_file_id", "caption": "first"},
            {"type": "video", "media": "video_file_id", "duration": 30},
        ],
    }


@pytest.mark.asyncio
async def test_send_media_group_with_upload_switches_to_multipart(client) -> None:
    bale_client, server = client
    server.set_response("sendMediaGroup", lambda body: [_sample_message_raw(1)])

    raw_bytes = b"raw-photo-bytes"
    await bale_client.send_media_group(
        200,
        [InputMediaPhoto(media=raw_bytes, caption="uploaded")],
        reply_to_message_id=3,
    )

    call = server.calls_for("sendMediaGroup")[0]
    fields = call["body"]["fields"]
    assert fields["chat_id"] == "200"
    assert fields["reply_to_message_id"] == "3"
    media_field = orjson.loads(fields["media"])
    assert media_field == [
        {"type": "photo", "media": "attach://file0", "caption": "uploaded"}
    ]
    assert call["body"]["files"]["file0"]["content"] == raw_bytes


@pytest.mark.asyncio
async def test_send_location(client) -> None:
    bale_client, server = client
    server.set_response("sendLocation", lambda body: _sample_message_raw())

    await bale_client.send_location(200, 35.7, 51.4, horizontal_accuracy=10.0)

    call = server.calls_for("sendLocation")[0]
    assert call["body"] == {
        "chat_id": 200,
        "latitude": 35.7,
        "longitude": 51.4,
        "horizontal_accuracy": 10.0,
    }


@pytest.mark.asyncio
async def test_send_contact(client) -> None:
    bale_client, server = client
    server.set_response("sendContact", lambda body: _sample_message_raw())

    await bale_client.send_contact(200, "+989120000000", "Sara", last_name="Ahmadi")

    call = server.calls_for("sendContact")[0]
    assert call["body"] == {
        "chat_id": 200,
        "phone_number": "+989120000000",
        "first_name": "Sara",
        "last_name": "Ahmadi",
    }


@pytest.mark.asyncio
async def test_get_file(client) -> None:
    bale_client, server = client
    server.set_response(
        "getFile",
        lambda body: {
            "file_id": "abc",
            "file_unique_id": "u1",
            "file_size": 1024,
            "file_path": "documents/file_1.pdf",
        },
    )

    result = await bale_client.get_file("abc")

    assert isinstance(result, File)
    assert result.file_path == "documents/file_1.pdf"
    assert server.calls_for("getFile")[0]["body"] == {"file_id": "abc"}


# -- Chat administration: promote/photo/title/description/invite -------------------


@pytest.mark.asyncio
async def test_promote_chat_member(client) -> None:
    bale_client, server = client
    server.set_response("promoteChatMember", lambda body: True)

    result = await bale_client.promote_chat_member(
        200, 7, can_delete_messages=True, can_invite_users=False
    )

    assert result is True
    assert server.calls_for("promoteChatMember")[0]["body"] == {
        "chat_id": 200,
        "user_id": 7,
        "can_delete_messages": True,
        "can_invite_users": False,
    }


@pytest.mark.asyncio
async def test_set_chat_photo_is_always_multipart(client) -> None:
    bale_client, server = client
    server.set_response("setChatPhoto", lambda body: True)

    raw_bytes = b"new-chat-photo-bytes"
    result = await bale_client.set_chat_photo(200, raw_bytes)

    assert result is True
    call = server.calls_for("setChatPhoto")[0]
    assert call["body"]["fields"] == {"chat_id": "200"}
    assert call["body"]["files"]["photo"]["content"] == raw_bytes


@pytest.mark.asyncio
async def test_delete_chat_photo(client) -> None:
    bale_client, server = client
    server.set_response("deleteChatPhoto", lambda body: True)

    result = await bale_client.delete_chat_photo(200)

    assert result is True
    assert server.calls_for("deleteChatPhoto")[0]["body"] == {"chat_id": 200}


@pytest.mark.asyncio
async def test_set_chat_title(client) -> None:
    bale_client, server = client
    server.set_response("setChatTitle", lambda body: True)

    result = await bale_client.set_chat_title(200, "New Title")

    assert result is True
    assert server.calls_for("setChatTitle")[0]["body"] == {
        "chat_id": 200,
        "title": "New Title",
    }


@pytest.mark.asyncio
async def test_set_chat_description(client) -> None:
    bale_client, server = client
    server.set_response("setChatDescription", lambda body: True)

    result = await bale_client.set_chat_description(200, "New description")

    assert result is True
    assert server.calls_for("setChatDescription")[0]["body"] == {
        "chat_id": 200,
        "description": "New description",
    }


@pytest.mark.asyncio
async def test_unpin_all_chat_messages(client) -> None:
    bale_client, server = client
    server.set_response("unpinAllChatMessages", lambda body: True)

    result = await bale_client.unpin_all_chat_messages(200)

    assert result is True
    assert server.calls_for("unpinAllChatMessages")[0]["body"] == {"chat_id": 200}


@pytest.mark.asyncio
async def test_export_chat_invite_link(client) -> None:
    bale_client, server = client
    server.set_response("exportChatInviteLink", lambda body: "https://bale.ai/join/xyz")

    result = await bale_client.export_chat_invite_link(200)

    assert result == "https://bale.ai/join/xyz"
    assert server.calls_for("exportChatInviteLink")[0]["body"] == {"chat_id": 200}


# -- Stickers --------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_upload_sticker_file(client) -> None:
    bale_client, server = client
    server.set_response(
        "uploadStickerFile",
        lambda body: {"file_id": "sfid", "file_unique_id": "sfuid"},
    )

    raw_bytes = b"webp-bytes"
    result = await bale_client.upload_sticker_file(100, raw_bytes)

    assert isinstance(result, File)
    assert result.file_id == "sfid"
    call = server.calls_for("uploadStickerFile")[0]
    assert call["body"]["fields"] == {"user_id": "100"}
    assert call["body"]["files"]["sticker"]["content"] == raw_bytes


@pytest.mark.asyncio
async def test_create_new_sticker_set(client) -> None:
    bale_client, server = client
    server.set_response("createNewStickerSet", lambda body: True)

    stickers = [{"sticker": "attach://sticker0", "emoji_list": ["\U0001F600"]}]
    result = await bale_client.create_new_sticker_set(
        100, "pack_by_mybot", "My Pack", stickers
    )

    assert result is True
    assert server.calls_for("createNewStickerSet")[0]["body"] == {
        "user_id": 100,
        "name": "pack_by_mybot",
        "title": "My Pack",
        "sticker": stickers,
    }


@pytest.mark.asyncio
async def test_add_sticker_to_set(client) -> None:
    bale_client, server = client
    server.set_response("addStickerToSet", lambda body: True)

    sticker = {"sticker": "attach://sticker0", "emoji_list": ["\U0001F600"]}
    result = await bale_client.add_sticker_to_set(100, "pack_by_mybot", sticker)

    assert result is True
    assert server.calls_for("addStickerToSet")[0]["body"] == {
        "user_id": 100,
        "name": "pack_by_mybot",
        "sticker": sticker,
    }


# -- Payments ----------------------------------------------------------------------


@pytest.mark.asyncio
async def test_send_invoice(client) -> None:
    bale_client, server = client
    server.set_response("sendInvoice", lambda body: _sample_message_raw())

    prices = [{"label": "Item", "amount": 10000}]
    message = await bale_client.send_invoice(
        200,
        "Product",
        "A great product",
        "internal-payload-123",
        "1234-5678-9012-3456",
        prices,
        photo_url="https://example.com/product.png",
    )

    assert isinstance(message, Message)
    call = server.calls_for("sendInvoice")[0]
    assert call["body"] == {
        "chat_id": 200,
        "title": "Product",
        "description": "A great product",
        "payload": "internal-payload-123",
        "provider_token": "1234-5678-9012-3456",
        "prices": prices,
        "photo_url": "https://example.com/product.png",
    }


@pytest.mark.asyncio
async def test_create_invoice_link(client) -> None:
    bale_client, server = client
    server.set_response(
        "createInvoiceLink",
        lambda body: "inv_link_abc123",
    )

    prices = [{"label": "Item", "amount": 10000}]
    result = await bale_client.create_invoice_link(
        "Product",
        "A great product",
        "internal-payload-123",
        "1234-5678-9012-3456",
        prices,
    )

    assert result == "inv_link_abc123"
    call = server.calls_for("createInvoiceLink")[0]
    assert call["body"] == {
        "title": "Product",
        "description": "A great product",
        "payload": "internal-payload-123",
        "provider_token": "1234-5678-9012-3456",
        "prices": prices,
    }


@pytest.mark.asyncio
async def test_answer_pre_checkout_query(client) -> None:
    bale_client, server = client
    server.set_response("answerPreCheckoutQuery", lambda body: True)

    result = await bale_client.answer_pre_checkout_query("pcq_123", ok=True)

    assert result is True
    assert server.calls_for("answerPreCheckoutQuery")[0]["body"] == {
        "pre_checkout_query_id": "pcq_123",
        "ok": True,
    }


@pytest.mark.asyncio
async def test_answer_pre_checkout_query_decline(client) -> None:
    bale_client, server = client
    server.set_response("answerPreCheckoutQuery", lambda body: True)

    result = await bale_client.answer_pre_checkout_query(
        "pcq_123", ok=False, error_message="Not available"
    )

    assert result is True
    assert server.calls_for("answerPreCheckoutQuery")[0]["body"] == {
        "pre_checkout_query_id": "pcq_123",
        "ok": False,
        "error_message": "Not available",
    }


@pytest.mark.asyncio
async def test_inquire_transaction(client) -> None:
    bale_client, server = client
    server.set_response(
        "inquireTransaction",
        lambda body: {
            "id": "txn_1",
            "status": "paid",
            "userID": 42,
            "amount": 50000,
            "createdAt": 1690000000,
        },
    )

    result = await bale_client.inquire_transaction("txn_1")

    assert result.id == "txn_1"
    assert result.status == "paid"
    assert result.userID == 42
    assert server.calls_for("inquireTransaction")[0]["body"] == {"transaction_id": "txn_1"}


# -- ok:false -> BaleAPIError, and never retried ------------------------------------


@pytest.mark.asyncio
async def test_ok_false_raises_bale_api_error_with_code_and_description(client) -> None:
    bale_client, server = client
    server.set_raw_envelope(
        "sendMessage",
        {
            "ok": False,
            "error_code": 403,
            "description": "Forbidden: bot was blocked by the user",
        },
    )

    with pytest.raises(BaleAPIError) as exc_info:
        await bale_client.send_message(200, "hello")

    assert exc_info.value.error_code == 403
    assert exc_info.value.description == "Forbidden: bot was blocked by the user"


@pytest.mark.asyncio
async def test_ok_false_is_not_retried(fake_server) -> None:
    """An application-level Bale error must not trigger the transport retry policy.

    `run_with_retry`'s default retryable set is transport-only
    (NetworkError/TimeoutError_/RateLimitedError); a 200 response with
    `ok: false` never even raises one of those, so this should hit the
    fake server exactly once no matter how many retry attempts the
    policy allows for.
    """
    server, base_url = fake_server
    server.set_raw_envelope(
        "sendMessage",
        {"ok": False, "error_code": 400, "description": "Bad Request: chat not found"},
    )
    bale_client = BaleClient(
        TOKEN, base_url=base_url, retry_policy=RetryPolicy(max_attempts=5)
    )

    with pytest.raises(BaleAPIError):
        await bale_client.send_message(200, "hello")

    assert server.call_count == 1
    await bale_client.close()


@pytest.mark.asyncio
async def test_bale_api_error_is_distinct_from_transport_http_status_error(
    client,
) -> None:
    """A `BaleAPIError` must never be confused with `HTTPStatusError`.

    They represent different failure classes (application-level `ok:
    false` on a 200, vs. a genuine non-2xx transport response) and must
    stay distinguishable to callers -- e.g. a caller catching
    `HTTPStatusError` specifically should NOT accidentally catch this.
    """
    bale_client, server = client
    server.set_raw_envelope(
        "sendMessage", {"ok": False, "error_code": 400, "description": "bad request"}
    )

    with pytest.raises(BaleAPIError) as exc_info:
        await bale_client.send_message(200, "hello")

    assert not isinstance(exc_info.value, HTTPStatusError)
