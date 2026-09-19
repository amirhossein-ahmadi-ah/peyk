from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms._telegram_like import TelegramLikeClient
from peyk.platforms.bale.client import BaleClient
from peyk.platforms.telegram.client import TelegramClient
from peyk.transport import Session


@dataclass(frozen=True)
class FakeFile:
    file_id: str

    @classmethod
    def from_dict(cls, value: Any) -> "FakeFile":
        return cls(file_id=value["file_id"])


class FakeClient(TelegramLikeClient):
    base_url = "http://unused"
    _error_class = Exception
    user_model = FakeFile
    webhook_info_model = FakeFile
    file_model = FakeFile


def test_shared_get_file_is_generic() -> None:
    async def run() -> None:
        client = FakeClient("token")
        calls = []

        async def fake_call(method_name: str, **kwargs: Any) -> Any:
            calls.append((method_name, kwargs))
            return {"file_id": "abc"}

        client._call = fake_call  # type: ignore[method-assign]
        result = await client.get_file("abc")
        assert result == FakeFile("abc")
        assert calls == [("getFile", {"json_body": {"file_id": "abc"}})]
        await client.close()

    asyncio.run(run())


def test_shared_media_builder_routes_string_and_upload() -> None:
    string_kwargs = FakeClient._build_media_request_kwargs(
        "photo", "file-id", json_fields={"chat_id": 7}, default_filename="photo.jpg"
    )
    assert string_kwargs == {
        "json_body": {"chat_id": 7, "photo": "file-id"}
    }

    upload_kwargs = FakeClient._build_media_request_kwargs(
        "photo", b"abc", json_fields={"chat_id": 7}, default_filename="photo.jpg"
    )
    assert upload_kwargs["data"] == {"chat_id": "7"}
    assert upload_kwargs["files"]["photo"].filename == "photo.jpg"


_MEDIA_REQUESTS: list[dict[str, str]] = []


async def _media_server(request: web.Request) -> web.Response:
    data = await request.post()
    uploaded = data["photo"]
    body = {
        "method": request.path.rsplit("/", 1)[-1],
        "chat_id": data["chat_id"],
        "photo_filename": uploaded.filename,
        "photo_bytes": uploaded.file.read().decode(),
    }
    _MEDIA_REQUESTS.append(body)
    return web.json_response({
        "ok": True,
        "result": {
            "message_id": 1,
            "date": 1,
            "chat": {"id": 7, "type": "private"},
            "photo": [],
            "_test": body,
        },
    })


def test_bale_real_subclass_uses_shared_multipart_path() -> None:
    async def run() -> None:
        app = web.Application()
        app.router.add_post("/botTOKEN/sendPhoto", _media_server)
        async with TestServer(app) as server:
            session = Session()
            client = BaleClient("TOKEN", session=session, base_url=str(server.make_url("" )).rstrip("/"))
            _MEDIA_REQUESTS.clear()
            result = await client.send_photo(7, b"bale-bytes")
            assert result.message_id == 1
            assert _MEDIA_REQUESTS[-1]["chat_id"] == "7"
            assert _MEDIA_REQUESTS[-1]["photo_bytes"] == "bale-bytes"
            assert _MEDIA_REQUESTS[-1]["photo_filename"] == "photo.jpg"
            await client.close()
            await session.close()

    asyncio.run(run())


def test_telegram_real_subclass_uses_shared_multipart_path() -> None:
    async def run() -> None:
        app = web.Application()
        app.router.add_post("/botTOKEN/sendPhoto", _media_server)
        async with TestServer(app) as server:
            session = Session()
            client = TelegramClient("TOKEN", session=session, base_url=str(server.make_url("" )).rstrip("/"))
            _MEDIA_REQUESTS.clear()
            result = await client.send_photo(7, b"telegram-bytes")
            assert result.message_id == 1
            assert _MEDIA_REQUESTS[-1]["chat_id"] == "7"
            assert _MEDIA_REQUESTS[-1]["photo_bytes"] == "telegram-bytes"
            assert _MEDIA_REQUESTS[-1]["photo_filename"] == "photo.jpg"
            await client.close()
            await session.close()

    asyncio.run(run())
