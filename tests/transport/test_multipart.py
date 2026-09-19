from __future__ import annotations

import base64
import io

import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.transport import FilePayload, Session


async def _multipart_echo(request: web.Request) -> web.Response:
    """Parse the multipart body server-side and report exactly what it saw.

    Round-tripping through the server (rather than only inspecting the
    client-built `FormData`) is the point here: a subtle encoding bug in
    `build_multipart_body`/`aiohttp`'s writer would still show up as a
    client-side "looks fine" object but fail to parse correctly here.
    """
    reader = await request.multipart()
    result: dict = {"fields": {}, "files": {}}
    async for part in reader:
        if part.filename:
            content = await part.read(decode=False)
            result["files"][part.name] = {
                "filename": part.filename,
                "content_type": part.headers.get("Content-Type"),
                "content_b64": base64.b64encode(content).decode("ascii"),
            }
        else:
            result["fields"][part.name] = await part.text()
    return web.json_response(result)


def _make_app() -> web.Application:
    app = web.Application()
    app.router.add_post("/upload", _multipart_echo)
    return app


@pytest.mark.asyncio
async def test_multipart_bytes_payload_parsed_correctly_by_server() -> None:
    original = b"\x89PNG-fake-bytes-not-a-real-png"

    app = _make_app()
    async with TestServer(app) as server:
        async with Session() as session:
            resp = await session.request(
                "POST",
                str(server.make_url("/upload")),
                data={"caption": "a photo", "chat_id": "42"},
                files={
                    "photo": FilePayload(
                        content=original,
                        filename="photo.png",
                        content_type="image/png",
                    )
                },
            )

            assert resp.status == 200
            parsed = resp.json
            assert parsed["fields"] == {"caption": "a photo", "chat_id": "42"}

            file_part = parsed["files"]["photo"]
            assert file_part["filename"] == "photo.png"
            assert file_part["content_type"] == "image/png"
            assert base64.b64decode(file_part["content_b64"]) == original


@pytest.mark.asyncio
async def test_multipart_stream_payload_read_and_sent_correctly() -> None:
    # Big enough to exercise more than a single internal read chunk.
    original = b"streamed video bytes " * 5000
    stream = io.BytesIO(original)

    app = _make_app()
    async with TestServer(app) as server:
        async with Session() as session:
            resp = await session.request(
                "POST",
                str(server.make_url("/upload")),
                files={
                    "video": FilePayload(
                        content=stream,
                        filename="clip.mp4",
                        content_type="video/mp4",
                    )
                },
            )

            assert resp.status == 200
            file_part = resp.json["files"]["video"]
            assert file_part["filename"] == "clip.mp4"
            assert file_part["content_type"] == "video/mp4"
            assert base64.b64decode(file_part["content_b64"]) == original


@pytest.mark.asyncio
async def test_multipart_fields_and_multiple_files_together() -> None:
    app = _make_app()
    async with TestServer(app) as server:
        async with Session() as session:
            resp = await session.request(
                "POST",
                str(server.make_url("/upload")),
                data={"note": "two files"},
                files={
                    "first": FilePayload(content=b"AAA", filename="a.bin"),
                    "second": FilePayload(content=io.BytesIO(b"BBB"), filename="b.bin"),
                },
            )

            assert resp.status == 200
            parsed = resp.json
            assert parsed["fields"] == {"note": "two files"}
            assert base64.b64decode(parsed["files"]["first"]["content_b64"]) == b"AAA"
            assert base64.b64decode(parsed["files"]["second"]["content_b64"]) == b"BBB"


@pytest.mark.asyncio
async def test_files_and_json_body_together_raises_value_error() -> None:
    async with Session() as session:
        with pytest.raises(ValueError):
            await session.request(
                "POST",
                "http://127.0.0.1:1/unused",
                json_body={"x": 1},
                files={"f": FilePayload(content=b"x", filename="f.bin")},
            )
