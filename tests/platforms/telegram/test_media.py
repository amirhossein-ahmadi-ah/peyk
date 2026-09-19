"""Tests for `TelegramClient` media methods (Phase T3).

Fake `aiohttp.test_utils` server, zero real network. The fake server
parses multipart bodies server-side (fields + files), so the upload
case asserts on what the server actually received -- not just on what
the client claims it sent.
"""

from __future__ import annotations

from typing import Any, Callable, Dict

import orjson
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms.telegram.client import TelegramClient
from peyk.platforms.telegram.models import (
    Animation,
    Audio,
    Document,
    File,
    InputMediaAnimation,
    InputMediaDocument,
    InputMediaLivePhoto,
    InputMediaPhoto,
    InputMediaVideo,
    LivePhoto,
    Message,
    PhotoSize,
    Video,
    VideoNote,
    Voice,
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
    "type": "private",
    "first_name": "Some",
    "last_name": "One",
    "username": "someone",
}


def _sample_message_raw(message_id: int = 1, **extra: Any) -> Dict[str, Any]:
    base: Dict[str, Any] = {
        "message_id": message_id,
        "date": 1690000000,
        "chat": SAMPLE_CHAT_RAW,
        "from": SAMPLE_USER_RAW,
    }
    base.update(extra)
    return base


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
                "multipart": True,
                "fields": fields,
                "files": files,
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


async def test_send_photo_file_id(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "sendPhoto",
        lambda body: _sample_message_raw(
            1,
            photo=[{"file_id": "pid", "file_unique_id": "puid",
                    "width": 100, "height": 100}],
            caption="nice",
        ),
    )
    client = _client_for(test_server)
    try:
        msg = await client.send_photo(200, "FILE_ID_1", caption="nice")
    finally:
        await client.close()
    assert isinstance(msg, Message)
    assert msg.photo[0] == PhotoSize("pid", "puid", 100, 100, None)
    assert msg.caption == "nice"
    assert server.calls_for("sendPhoto")[0]["body"] == {
        "chat_id": 200, "photo": "FILE_ID_1", "caption": "nice",
    }


async def test_send_photo_url(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("sendPhoto", lambda body: _sample_message_raw(1))
    client = _client_for(test_server)
    try:
        await client.send_photo(200, "https://example.com/p.jpg")
    finally:
        await client.close()
    assert server.calls_for("sendPhoto")[0]["body"]["photo"] == (
        "https://example.com/p.jpg"
    )


async def test_send_photo_upload_bytes(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("sendPhoto", lambda body: _sample_message_raw(1))
    client = _client_for(test_server)
    try:
        await client.send_photo(
            200, b"\x89PNG-binary", caption="up",
            show_caption_above_media=True, has_spoiler=True,
        )
    finally:
        await client.close()
    body = server.calls_for("sendPhoto")[0]["body"]
    assert body["multipart"] is True
    assert body["fields"]["chat_id"] == "200"
    assert body["fields"]["caption"] == "up"
    assert body["fields"]["show_caption_above_media"] == "True"
    assert body["fields"]["has_spoiler"] == "True"
    assert body["files"]["photo"]["content"] == b"\x89PNG-binary"
    assert body["files"]["photo"]["filename"] == "photo.jpg"


async def test_send_document_all_three_styles(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("sendDocument", lambda body: _sample_message_raw(2))
    client = _client_for(test_server)
    try:
        await client.send_document(200, "DOC_FILE_ID")
        await client.send_document(200, "https://example.com/f.pdf")
        await client.send_document(
            200, b"%PDF-binary", caption="doc",
            disable_content_type_detection=True,
        )
    finally:
        await client.close()
    bodies = [c["body"] for c in server.calls_for("sendDocument")]
    assert bodies[0] == {"chat_id": 200, "document": "DOC_FILE_ID"}
    assert bodies[1]["document"] == "https://example.com/f.pdf"
    assert bodies[2]["multipart"] is True
    assert bodies[2]["fields"]["caption"] == "doc"
    assert bodies[2]["fields"]["disable_content_type_detection"] == "True"
    assert bodies[2]["files"]["document"]["content"] == b"%PDF-binary"


async def test_send_audio_with_metadata(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "sendAudio",
        lambda body: _sample_message_raw(
            3, audio={"file_id": "a", "file_unique_id": "au",
                      "duration": 120, "performer": "P", "title": "T"},
        ),
    )
    client = _client_for(test_server)
    try:
        msg = await client.send_audio(
            200, "AUDIO_ID", duration=120, performer="P", title="T"
        )
    finally:
        await client.close()
    assert msg.audio == Audio("a", "au", 120, "P", "T", None, None, None, None)
    assert server.calls_for("sendAudio")[0]["body"] == {
        "chat_id": 200, "audio": "AUDIO_ID",
        "duration": 120, "performer": "P", "title": "T",
    }


async def test_send_video_upload_with_thumbnail(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("sendVideo", lambda body: _sample_message_raw(4))
    client = _client_for(test_server)
    try:
        await client.send_video(
            200, b"VIDEO", thumbnail=b"THUMB",
            duration=10, width=640, height=480, supports_streaming=True,
        )
    finally:
        await client.close()
    body = server.calls_for("sendVideo")[0]["body"]
    assert body["multipart"] is True
    assert body["files"]["video"]["content"] == b"VIDEO"
    assert body["files"]["thumbnail"]["content"] == b"THUMB"
    assert body["fields"]["duration"] == "10"
    assert body["fields"]["supports_streaming"] == "True"


async def test_send_animation_url(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("sendAnimation", lambda body: _sample_message_raw(5))
    client = _client_for(test_server)
    try:
        await client.send_animation(
            200, "https://example.com/a.gif", has_spoiler=True
        )
    finally:
        await client.close()
    assert server.calls_for("sendAnimation")[0]["body"] == {
        "chat_id": 200, "animation": "https://example.com/a.gif",
        "has_spoiler": True,
    }


async def test_send_voice_and_video_note(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "sendVoice",
        lambda body: _sample_message_raw(
            6, voice={"file_id": "v", "file_unique_id": "vu",
                      "duration": 5},
        ),
    )
    server.set_response("sendVideoNote", lambda body: _sample_message_raw(7))
    client = _client_for(test_server)
    try:
        msg = await client.send_voice(200, b"VOICE", duration=5)
        assert msg.voice == Voice("v", "vu", 5, None, None)
        await client.send_video_note(200, "VN_ID", length=384)
    finally:
        await client.close()
    assert server.calls_for("sendVoice")[0]["body"]["multipart"] is True
    assert server.calls_for("sendVideoNote")[0]["body"] == {
        "chat_id": 200, "video_note": "VN_ID", "length": 384,
    }


async def test_send_live_photo_file_ids_and_upload(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "sendLivePhoto",
        lambda body: _sample_message_raw(
            8, live_photo={"file_id": "lp", "file_unique_id": "lpu",
                           "width": 100, "height": 100, "duration": 3},
        ),
    )
    client = _client_for(test_server)
    try:
        msg = await client.send_live_photo(200, "VIDEO_ID", "PHOTO_ID")
        assert msg.live_photo == LivePhoto(
            "lp", "lpu", 100, 100, 3, None, None, None
        )
        await client.send_live_photo(200, b"VID", b"PIC", caption="live")
    finally:
        await client.close()
    bodies = [c["body"] for c in server.calls_for("sendLivePhoto")]
    assert bodies[0] == {
        "chat_id": 200, "live_photo": "VIDEO_ID", "photo": "PHOTO_ID",
    }
    assert bodies[1]["multipart"] is True
    assert bodies[1]["files"]["live_photo"]["content"] == b"VID"
    assert bodies[1]["files"]["photo"]["content"] == b"PIC"
    assert bodies[1]["fields"]["caption"] == "live"


async def test_send_media_group_mixed(fake_server) -> None:
    server, test_server = fake_server

    def _result(body: Any) -> Any:
        media = orjson.loads(body["fields"]["media"])
        assert [m["type"] for m in media] == ["photo", "photo", "video"]
        assert media[0]["media"] == "attach://file0_media"
        assert media[1]["media"] == "attach://file1_media"
        assert media[1]["caption"] == "second"
        assert media[2]["media"] == "VIDEO_ID"
        return [_sample_message_raw(10), _sample_message_raw(11),
                _sample_message_raw(12)]

    server.set_response("sendMediaGroup", _result)
    client = _client_for(test_server)
    try:
        msgs = await client.send_media_group(
            200,
            [InputMediaPhoto(b"P1"),
             InputMediaPhoto(b"P2", caption="second"),
             InputMediaVideo("VIDEO_ID")],
        )
    finally:
        await client.close()
    assert [m.message_id for m in msgs] == [10, 11, 12]
    body = server.calls_for("sendMediaGroup")[0]["body"]
    assert set(body["files"]) == {"file0_media", "file1_media"}
    assert body["files"]["file0_media"]["content"] == b"P1"


async def test_send_media_group_all_strings_is_json(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "sendMediaGroup",
        lambda body: [_sample_message_raw(20), _sample_message_raw(21)],
    )
    client = _client_for(test_server)
    try:
        msgs = await client.send_media_group(
            200, [InputMediaPhoto("P1"), InputMediaDocument("D1")]
        )
    finally:
        await client.close()
    assert len(msgs) == 2
    body = server.calls_for("sendMediaGroup")[0]["body"]
    assert body == {
        "chat_id": 200,
        "media": [{"type": "photo", "media": "P1"},
                  {"type": "document", "media": "D1"}],
    }


async def test_edit_message_media_and_caption(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "editMessageMedia",
        lambda body: _sample_message_raw(30, caption="new"),
    )
    server.set_response("editMessageCaption", lambda body: True)
    client = _client_for(test_server)
    try:
        edited = await client.edit_message_media(
            InputMediaPhoto("NEW_PHOTO"), chat_id=200, message_id=30
        )
        assert isinstance(edited, Message)
        assert edited.caption == "new"
        inline = await client.edit_message_caption(
            inline_message_id="ABC", caption="cap"
        )
        assert inline is True
    finally:
        await client.close()
    media_body = server.calls_for("editMessageMedia")[0]["body"]
    assert media_body["media"] == {"type": "photo", "media": "NEW_PHOTO"}
    caption_body = server.calls_for("editMessageCaption")[0]["body"]
    assert caption_body == {"inline_message_id": "ABC", "caption": "cap"}


async def test_edit_message_media_inline_upload_rejected() -> None:
    client = TelegramClient("T", base_url="http://127.0.0.1:1")
    try:
        with pytest.raises(ValueError):
            await client.edit_message_media(
                InputMediaPhoto(b"BYTES"), inline_message_id="ABC"
            )
    finally:
        await client.close()


async def test_get_file(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "getFile",
        lambda body: {"file_id": "f", "file_unique_id": "fu",
                      "file_size": 42, "file_path": "photos/f.jpg"},
    )
    client = _client_for(test_server)
    try:
        f = await client.get_file("f")
    finally:
        await client.close()
    assert f == File("f", "fu", 42, "photos/f.jpg")
    assert server.calls_for("getFile")[0]["body"] == {"file_id": "f"}


async def test_media_response_models_parse() -> None:
    doc = Document.from_dict(
        {"file_id": "d", "file_unique_id": "du",
         "file_name": "f.pdf", "mime_type": "application/pdf",
         "thumbnail": {"file_id": "t", "file_unique_id": "tu",
                       "width": 10, "height": 10}}
    )
    assert doc.thumbnail.width == 10
    anim = Animation.from_dict(
        {"file_id": "a", "file_unique_id": "au",
         "width": 100, "height": 100, "duration": 3}
    )
    assert anim.duration == 3
    vn = VideoNote.from_dict(
        {"file_id": "n", "file_unique_id": "nu",
         "length": 384, "duration": 60}
    )
    assert vn.length == 384
    lp_in = InputMediaLivePhoto("VID", "PIC", has_spoiler=True)
    assert lp_in.to_dict("attach://x", "attach://y") == {
        "type": "live_photo", "media": "attach://x",
        "photo": "attach://y", "has_spoiler": True,
    }
    assert InputMediaAnimation("A").to_dict("A")["type"] == "animation"
    assert InputMediaDocument("D").to_dict("D")["type"] == "document"
