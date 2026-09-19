"""Tests for `TelegramClient` sticker methods (Phase T10).

Fake `aiohttp.test_utils` server, zero real network. Covers all sticker
methods: send_sticker, get_sticker_set, get_custom_emoji_stickers,
upload_sticker_file, create_new_sticker_set, add_sticker_to_set,
set_sticker_position_in_set, delete_sticker_from_set,
replace_sticker_in_set, set_sticker_emoji_list, set_sticker_keywords,
set_sticker_mask_position, set_sticker_set_title,
set_sticker_set_thumbnail, set_custom_emoji_sticker_set_thumbnail,
delete_sticker_set. Also verifies Sticker parsing for all three type
values and multipart upload correctness.
"""

from __future__ import annotations

from typing import Any, Callable, Dict

import orjson
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms.telegram.client import TelegramClient
from peyk.platforms.telegram.models import (
    File,
    InputSticker,
    MaskPosition,
    Message,
    PhotoSize,
    Sticker,
    StickerSet,
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


# ---------------------------------------------------------------------------
# send_sticker
# ---------------------------------------------------------------------------


async def test_send_sticker_file_id(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "sendSticker",
        lambda body: _sample_message_raw(1),
    )
    client = _client_for(test_server)
    try:
        msg = await client.send_sticker(200, "STICKER_FILE_ID")
    finally:
        await client.close()
    assert isinstance(msg, Message)
    assert server.calls_for("sendSticker")[0]["body"] == {
        "chat_id": 200,
        "sticker": "STICKER_FILE_ID",
    }


async def test_send_sticker_upload_bytes(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("sendSticker", lambda body: _sample_message_raw(1))
    client = _client_for(test_server)
    try:
        await client.send_sticker(
            200, b"WEBP-binary", emoji="🔥",
            disable_notification=True,
        )
    finally:
        await client.close()
    body = server.calls_for("sendSticker")[0]["body"]
    assert body["multipart"] is True
    assert body["fields"]["chat_id"] == "200"
    assert body["fields"]["emoji"] == "🔥"
    assert body["fields"]["disable_notification"] == "True"
    assert body["files"]["sticker"]["content"] == b"WEBP-binary"
    assert body["files"]["sticker"]["filename"] == "sticker.webp"


# ---------------------------------------------------------------------------
# get_sticker_set
# ---------------------------------------------------------------------------


async def test_get_sticker_set(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "getStickerSet",
        lambda body: {
            "name": "my_set_by_bot",
            "title": "My Set",
            "sticker_type": "regular",
            "is_animated": False,
            "is_video": False,
            "stickers": [
                {
                    "file_id": "s1",
                    "file_unique_id": "s1u",
                    "type": "regular",
                    "width": 512,
                    "height": 512,
                    "is_animated": False,
                    "is_video": False,
                }
            ],
        },
    )
    client = _client_for(test_server)
    try:
        result = await client.get_sticker_set("my_set_by_bot")
    finally:
        await client.close()
    assert isinstance(result, StickerSet)
    assert result.name == "my_set_by_bot"
    assert result.title == "My Set"
    assert result.sticker_type == "regular"
    assert len(result.stickers) == 1
    assert result.stickers[0].file_id == "s1"


# ---------------------------------------------------------------------------
# get_custom_emoji_stickers
# ---------------------------------------------------------------------------


async def test_get_custom_emoji_stickers(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "getCustomEmojiStickers",
        lambda body: [
            {
                "file_id": "ce1",
                "file_unique_id": "ce1u",
                "type": "custom_emoji",
                "width": 512,
                "height": 512,
                "is_animated": False,
                "is_video": False,
                "custom_emoji_id": "12345",
            }
        ],
    )
    client = _client_for(test_server)
    try:
        result = await client.get_custom_emoji_stickers(["12345"])
    finally:
        await client.close()
    assert len(result) == 1
    assert result[0].type == "custom_emoji"
    assert result[0].custom_emoji_id == "12345"


# ---------------------------------------------------------------------------
# upload_sticker_file
# ---------------------------------------------------------------------------


async def test_upload_sticker_file_upload(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "uploadStickerFile",
        lambda body: {"file_id": "new_sticker", "file_unique_id": "nsu"},
    )
    client = _client_for(test_server)
    try:
        result = await client.upload_sticker_file(
            100, b"WEBP-data", "static"
        )
    finally:
        await client.close()
    assert isinstance(result, File)
    body = server.calls_for("uploadStickerFile")[0]["body"]
    assert body["multipart"] is True
    assert body["fields"]["user_id"] == "100"
    assert body["fields"]["sticker_format"] == "static"
    assert body["files"]["sticker"]["content"] == b"WEBP-data"


# ---------------------------------------------------------------------------
# create_new_sticker_set
# ---------------------------------------------------------------------------


async def test_create_new_sticker_set_json(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("createNewStickerSet", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.create_new_sticker_set(
            100,
            "my_set_by_bot",
            "My Set",
            [
                InputSticker(
                    sticker="FILE_ID_1",
                    format="static",
                    emoji_list=["😀"],
                )
            ],
        )
    finally:
        await client.close()
    assert result is True
    body = server.calls_for("createNewStickerSet")[0]["body"]
    assert body["user_id"] == 100
    assert body["name"] == "my_set_by_bot"
    assert body["title"] == "My Set"
    assert body["stickers"][0]["sticker"] == "FILE_ID_1"
    assert body["stickers"][0]["format"] == "static"
    assert body["stickers"][0]["emoji_list"] == ["😀"]


async def test_create_new_sticker_set_upload(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("createNewStickerSet", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.create_new_sticker_set(
            100,
            "my_set_by_bot",
            "My Set",
            [
                InputSticker(
                    sticker=b"WEBP-binary",
                    format="static",
                    emoji_list=["😀"],
                )
            ],
        )
    finally:
        await client.close()
    assert result is True
    body = server.calls_for("createNewStickerSet")[0]["body"]
    assert body["multipart"] is True
    assert body["fields"]["user_id"] == "100"
    assert body["fields"]["name"] == "my_set_by_bot"
    assert body["fields"]["title"] == "My Set"
    # The sticker part should be an attach:// reference
    stickers = orjson.loads(body["fields"]["stickers"])
    assert stickers[0]["sticker"].startswith("attach://")
    assert body["files"]["file0_sticker"]["content"] == b"WEBP-binary"


# ---------------------------------------------------------------------------
# add_sticker_to_set
# ---------------------------------------------------------------------------


async def test_add_sticker_to_set_json(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("addStickerToSet", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.add_sticker_to_set(
            100,
            "my_set_by_bot",
            InputSticker(
                sticker="FILE_ID_2",
                format="static",
                emoji_list=["😎"],
            ),
        )
    finally:
        await client.close()
    assert result is True
    body = server.calls_for("addStickerToSet")[0]["body"]
    assert body["user_id"] == 100
    assert body["name"] == "my_set_by_bot"
    assert body["sticker"]["sticker"] == "FILE_ID_2"


async def test_add_sticker_to_set_upload(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("addStickerToSet", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.add_sticker_to_set(
            100,
            "my_set_by_bot",
            InputSticker(
                sticker=b"WEBP-data",
                format="static",
                emoji_list=["😎"],
            ),
        )
    finally:
        await client.close()
    assert result is True
    body = server.calls_for("addStickerToSet")[0]["body"]
    assert body["multipart"] is True
    sticker = orjson.loads(body["fields"]["sticker"])
    assert sticker["sticker"].startswith("attach://")
    assert body["files"]["file0_sticker"]["content"] == b"WEBP-data"


# ---------------------------------------------------------------------------
# set_sticker_position_in_set
# ---------------------------------------------------------------------------


async def test_set_sticker_position_in_set(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setStickerPositionInSet", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.set_sticker_position_in_set("STICKER_ID", 3)
    finally:
        await client.close()
    assert result is True
    assert server.calls_for("setStickerPositionInSet")[0]["body"] == {
        "sticker": "STICKER_ID",
        "position": 3,
    }


# ---------------------------------------------------------------------------
# delete_sticker_from_set
# ---------------------------------------------------------------------------


async def test_delete_sticker_from_set(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("deleteStickerFromSet", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.delete_sticker_from_set("STICKER_ID")
    finally:
        await client.close()
    assert result is True
    assert server.calls_for("deleteStickerFromSet")[0]["body"] == {
        "sticker": "STICKER_ID",
    }


# ---------------------------------------------------------------------------
# replace_sticker_in_set
# ---------------------------------------------------------------------------


async def test_replace_sticker_in_set_json(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("replaceStickerInSet", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.replace_sticker_in_set(
            100,
            "my_set_by_bot",
            "OLD_STICKER_ID",
            InputSticker(
                sticker="NEW_FILE_ID",
                format="static",
                emoji_list=["✨"],
            ),
        )
    finally:
        await client.close()
    assert result is True
    body = server.calls_for("replaceStickerInSet")[0]["body"]
    assert body["user_id"] == 100
    assert body["name"] == "my_set_by_bot"
    assert body["old_sticker"] == "OLD_STICKER_ID"
    assert body["sticker"]["sticker"] == "NEW_FILE_ID"
    assert body["sticker"]["emoji_list"] == ["✨"]


async def test_replace_sticker_in_set_upload(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("replaceStickerInSet", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.replace_sticker_in_set(
            100,
            "my_set_by_bot",
            "OLD_STICKER_ID",
            InputSticker(
                sticker=b"NEW_WEBP",
                format="static",
                emoji_list=["✨"],
            ),
        )
    finally:
        await client.close()
    assert result is True
    body = server.calls_for("replaceStickerInSet")[0]["body"]
    assert body["multipart"] is True
    assert body["fields"]["old_sticker"] == "OLD_STICKER_ID"
    sticker = orjson.loads(body["fields"]["sticker"])
    assert sticker["sticker"].startswith("attach://")
    assert body["files"]["file0_sticker"]["content"] == b"NEW_WEBP"


# ---------------------------------------------------------------------------
# set_sticker_emoji_list
# ---------------------------------------------------------------------------


async def test_set_sticker_emoji_list(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setStickerEmojiList", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.set_sticker_emoji_list(
            "STICKER_ID", ["😀", "😃"]
        )
    finally:
        await client.close()
    assert result is True
    assert server.calls_for("setStickerEmojiList")[0]["body"] == {
        "sticker": "STICKER_ID",
        "emoji_list": ["😀", "😃"],
    }


# ---------------------------------------------------------------------------
# set_sticker_keywords
# ---------------------------------------------------------------------------


async def test_set_sticker_keywords(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setStickerKeywords", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.set_sticker_keywords(
            "STICKER_ID", ["funny", "lol"]
        )
    finally:
        await client.close()
    assert result is True
    assert server.calls_for("setStickerKeywords")[0]["body"] == {
        "sticker": "STICKER_ID",
        "keywords": ["funny", "lol"],
    }


# ---------------------------------------------------------------------------
# set_sticker_mask_position
# ---------------------------------------------------------------------------


async def test_set_sticker_mask_position(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setStickerMaskPosition", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.set_sticker_mask_position(
            "STICKER_ID",
            MaskPosition(point="eyes", x_shift=0.0, y_shift=0.2, scale=1.5),
        )
    finally:
        await client.close()
    assert result is True
    body = server.calls_for("setStickerMaskPosition")[0]["body"]
    assert body["sticker"] == "STICKER_ID"
    assert body["mask_position"]["point"] == "eyes"
    assert body["mask_position"]["scale"] == 1.5


# ---------------------------------------------------------------------------
# set_sticker_set_title
# ---------------------------------------------------------------------------


async def test_set_sticker_set_title(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setStickerSetTitle", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.set_sticker_set_title(
            "my_set_by_bot", "New Title"
        )
    finally:
        await client.close()
    assert result is True
    assert server.calls_for("setStickerSetTitle")[0]["body"] == {
        "name": "my_set_by_bot",
        "title": "New Title",
    }


# ---------------------------------------------------------------------------
# set_sticker_set_thumbnail
# ---------------------------------------------------------------------------


async def test_set_sticker_set_thumbnail_json(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setStickerSetThumbnail", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.set_sticker_set_thumbnail(
            "my_set_by_bot", 100, thumbnail="THUMB_FILE_ID", format="static"
        )
    finally:
        await client.close()
    assert result is True
    body = server.calls_for("setStickerSetThumbnail")[0]["body"]
    assert body["name"] == "my_set_by_bot"
    assert body["user_id"] == 100
    assert body["thumbnail"] == "THUMB_FILE_ID"
    assert body["format"] == "static"


async def test_set_sticker_set_thumbnail_upload(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setStickerSetThumbnail", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.set_sticker_set_thumbnail(
            "my_set_by_bot", 100, thumbnail=b"PNG_DATA", format="static"
        )
    finally:
        await client.close()
    assert result is True
    body = server.calls_for("setStickerSetThumbnail")[0]["body"]
    assert body["multipart"] is True
    assert body["fields"]["name"] == "my_set_by_bot"
    assert body["fields"]["user_id"] == "100"
    assert body["fields"]["format"] == "static"
    assert body["files"]["thumbnail"]["content"] == b"PNG_DATA"


# ---------------------------------------------------------------------------
# set_custom_emoji_sticker_set_thumbnail
# ---------------------------------------------------------------------------


async def test_set_custom_emoji_sticker_set_thumbnail(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setCustomEmojiStickerSetThumbnail", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.set_custom_emoji_sticker_set_thumbnail(
            "my_set_by_bot", "12345"
        )
    finally:
        await client.close()
    assert result is True
    assert server.calls_for("setCustomEmojiStickerSetThumbnail")[0]["body"] == {
        "name": "my_set_by_bot",
        "custom_emoji_id": "12345",
    }


# ---------------------------------------------------------------------------
# delete_sticker_set
# ---------------------------------------------------------------------------


async def test_delete_sticker_set(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("deleteStickerSet", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.delete_sticker_set("my_set_by_bot")
    finally:
        await client.close()
    assert result is True
    assert server.calls_for("deleteStickerSet")[0]["body"] == {
        "name": "my_set_by_bot",
    }


# ---------------------------------------------------------------------------
# Sticker parsing for all three type values
# ---------------------------------------------------------------------------


def test_sticker_type_regular() -> None:
    """Regular sticker: has emoji, set_name, no mask_position/custom_emoji_id."""
    sticker = Sticker.from_dict({
        "file_id": "s1",
        "file_unique_id": "s1u",
        "type": "regular",
        "width": 512,
        "height": 512,
        "is_animated": False,
        "is_video": False,
        "emoji": "😀",
        "set_name": "my_set_by_bot",
        "file_size": 10240,
    })
    assert sticker is not None
    assert sticker.type == "regular"
    assert sticker.emoji == "😀"
    assert sticker.set_name == "my_set_by_bot"
    assert sticker.mask_position is None
    assert sticker.custom_emoji_id is None
    assert sticker.file_size == 10240


def test_sticker_type_mask() -> None:
    """Mask sticker: has mask_position, no emoji/custom_emoji_id."""
    sticker = Sticker.from_dict({
        "file_id": "s2",
        "file_unique_id": "s2u",
        "type": "mask",
        "width": 512,
        "height": 512,
        "is_animated": False,
        "is_video": False,
        "mask_position": {
            "point": "eyes",
            "x_shift": 0.0,
            "y_shift": 0.2,
            "scale": 1.5,
        },
    })
    assert sticker is not None
    assert sticker.type == "mask"
    assert sticker.mask_position is not None
    assert sticker.mask_position.point == "eyes"
    assert sticker.mask_position.scale == 1.5
    assert sticker.emoji is None
    assert sticker.custom_emoji_id is None


def test_sticker_type_custom_emoji() -> None:
    """Custom emoji sticker: has custom_emoji_id, no emoji/mask_position."""
    sticker = Sticker.from_dict({
        "file_id": "s3",
        "file_unique_id": "s3u",
        "type": "custom_emoji",
        "width": 512,
        "height": 512,
        "is_animated": False,
        "is_video": False,
        "custom_emoji_id": "12345",
        "needs_repainting": True,
    })
    assert sticker is not None
    assert sticker.type == "custom_emoji"
    assert sticker.custom_emoji_id == "12345"
    assert sticker.needs_repainting is True
    assert sticker.emoji is None
    assert sticker.mask_position is None


def test_sticker_with_thumbnail() -> None:
    """Sticker with thumbnail parses PhotoSize correctly."""
    sticker = Sticker.from_dict({
        "file_id": "s4",
        "file_unique_id": "s4u",
        "type": "regular",
        "width": 512,
        "height": 512,
        "is_animated": False,
        "is_video": False,
        "thumbnail": {
            "file_id": "t1",
            "file_unique_id": "t1u",
            "width": 100,
            "height": 100,
            "file_size": 2048,
        },
    })
    assert sticker is not None
    assert sticker.thumbnail is not None
    assert sticker.thumbnail.file_id == "t1"
    assert sticker.thumbnail.width == 100


def test_sticker_list_from() -> None:
    """Sticker.list_from parses a list of stickers."""
    stickers = Sticker.list_from([
        {
            "file_id": "s1",
            "file_unique_id": "s1u",
            "type": "regular",
            "width": 512,
            "height": 512,
            "is_animated": False,
            "is_video": False,
        },
        {
            "file_id": "s2",
            "file_unique_id": "s2u",
            "type": "custom_emoji",
            "width": 512,
            "height": 512,
            "is_animated": False,
            "is_video": False,
            "custom_emoji_id": "999",
        },
    ])
    assert stickers is not None
    assert len(stickers) == 2
    assert stickers[0].type == "regular"
    assert stickers[1].type == "custom_emoji"


# ---------------------------------------------------------------------------
# MaskPosition
# ---------------------------------------------------------------------------


def test_mask_position_roundtrip() -> None:
    """MaskPosition to_dict/from_dict roundtrip."""
    mp = MaskPosition(point="forehead", x_shift=0.1, y_shift=0.2, scale=1.0)
    d = mp.to_dict()
    assert d == {"point": "forehead", "x_shift": 0.1, "y_shift": 0.2, "scale": 1.0}
    mp2 = MaskPosition.from_dict(d)
    assert mp2 is not None
    assert mp2.point == "forehead"
    assert mp2.x_shift == 0.1


# ---------------------------------------------------------------------------
# InputSticker
# ---------------------------------------------------------------------------


def test_input_sticker_to_dict_with_file_id() -> None:
    """InputSticker.to_dict with a file_id string."""
    s = InputSticker(
        sticker="FILE_ID_1",
        format="static",
        emoji_list=["😀", "😃"],
    )
    d = s.to_dict("FILE_ID_1")
    assert d == {
        "sticker": "FILE_ID_1",
        "format": "static",
        "emoji_list": ["😀", "😃"],
    }


def test_input_sticker_to_dict_with_mask_position() -> None:
    """InputSticker.to_dict includes mask_position when present."""
    s = InputSticker(
        sticker="FILE_ID_1",
        format="static",
        emoji_list=["😷"],
        mask_position=MaskPosition(
            point="eyes", x_shift=0.0, y_shift=0.2, scale=1.5
        ),
    )
    d = s.to_dict("FILE_ID_1")
    assert d["mask_position"]["point"] == "eyes"
    assert d["mask_position"]["scale"] == 1.5


def test_input_sticker_to_dict_with_keywords() -> None:
    """InputSticker.to_dict includes keywords when present."""
    s = InputSticker(
        sticker="FILE_ID_1",
        format="static",
        emoji_list=["😀"],
        keywords=["funny", "lol"],
    )
    d = s.to_dict("FILE_ID_1")
    assert d["keywords"] == ["funny", "lol"]


# ---------------------------------------------------------------------------
# StickerSet
# ---------------------------------------------------------------------------


def test_sticker_set_from_dict() -> None:
    """StickerSet.from_dict parses stickers and metadata."""
    ss = StickerSet.from_dict({
        "name": "my_set_by_bot",
        "title": "My Set",
        "sticker_type": "regular",
        "is_animated": False,
        "is_video": False,
        "stickers": [
            {
                "file_id": "s1",
                "file_unique_id": "s1u",
                "type": "regular",
                "width": 512,
                "height": 512,
                "is_animated": False,
                "is_video": False,
            }
        ],
    })
    assert ss is not None
    assert ss.name == "my_set_by_bot"
    assert ss.title == "My Set"
    assert ss.sticker_type == "regular"
    assert len(ss.stickers) == 1
    assert ss.stickers[0].file_id == "s1"
