"""Tests for Phase T12 (Telegram Passport), T13 (Games), T14 (Business Accounts).

Fake server, zero real network.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

import orjson
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms.telegram.client import TelegramClient
from peyk.platforms.telegram.models import (
    BusinessConnection,
    BusinessMessagesDeleted,
    EncryptedPassportElement,
    Game,
    GameHighScore,
    InputStoryContentPhoto,
    Message,
    PassportData,
    PassportElementErrorDataField,
    PassportElementErrorFrontSide,
    PassportElementErrorSelfie,
    PassportElementErrorTranslationFiles,
    PassportElementErrorUnspecified,
    PassportFile,
    PhotoSize,
    StarAmount,
    StoryAreaTypeLocation,
    StoryAreaTypeLink,
    Update,
    User,
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
        self.request_log: List[Dict[str, Any]] = []
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

    def calls_for(self, method_name: str) -> List[Dict[str, Any]]:
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
# T12: Telegram Passport
# ---------------------------------------------------------------------------


async def test_set_passport_data_errors(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setPassportDataErrors", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.set_passport_data_errors(
            100,
            [
                PassportElementErrorDataField(
                    type="personal_details",
                    field_name="first_name",
                    data_hash="abc123",
                    message="Invalid name",
                ),
                PassportElementErrorFrontSide(
                    type="passport",
                    file_hash="def456",
                    message="Blurry image",
                ),
                PassportElementErrorSelfie(
                    type="passport",
                    file_hash="ghi789",
                    message="Face not visible",
                ),
            ],
        )
    finally:
        await client.close()
    assert result is True
    body = server.calls_for("setPassportDataErrors")[0]["body"]
    assert body["user_id"] == 100
    assert len(body["errors"]) == 3
    assert body["errors"][0]["source"] == "data"
    assert body["errors"][0]["field_name"] == "first_name"
    assert body["errors"][1]["source"] == "front_side"
    assert body["errors"][2]["source"] == "selfie"


def test_passport_data_in_message() -> None:
    """PassportData parsing from a Message.passport_data payload."""
    msg = Message.from_dict(
        _sample_message_raw(
            1,
            passport_data={
                "data": [
                    {
                        "type": "personal_details",
                        "hash": "hash123",
                        "data": "encrypted_data_here",
                    }
                ],
                "credentials": {
                    "data": "cred_data",
                    "hash": "cred_hash",
                    "secret": "cred_secret",
                },
            },
        )
    )
    assert msg.passport_data is not None
    assert len(msg.passport_data.data) == 1
    assert msg.passport_data.data[0].type == "personal_details"
    assert msg.passport_data.credentials is not None
    assert msg.passport_data.credentials.hash == "cred_hash"


# ---------------------------------------------------------------------------
# T13: Games
# ---------------------------------------------------------------------------


async def test_send_game(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("sendGame", lambda body: _sample_message_raw(1))
    client = _client_for(test_server)
    try:
        msg = await client.send_game(200, "my_game")
    finally:
        await client.close()
    assert isinstance(msg, Message)
    body = server.calls_for("sendGame")[0]["body"]
    assert body["chat_id"] == 200
    assert body["game_short_name"] == "my_game"


async def test_set_game_score(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setGameScore", lambda body: _sample_message_raw(1))
    client = _client_for(test_server)
    try:
        result = await client.set_game_score(
            100,
            score=1500,
            chat_id=200,
            message_id=42,
            force=True,
        )
    finally:
        await client.close()
    assert isinstance(result, Message)
    body = server.calls_for("setGameScore")[0]["body"]
    assert body["user_id"] == 100
    assert body["score"] == 1500
    assert body["chat_id"] == 200
    assert body["message_id"] == 42
    assert body["force"] is True


async def test_get_game_high_scores(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "getGameHighScores",
        lambda body: [
            {"position": 1, "user": SAMPLE_USER_RAW, "score": 5000},
            {"position": 2, "user": SAMPLE_USER_RAW, "score": 4000},
        ],
    )
    client = _client_for(test_server)
    try:
        result = await client.get_game_high_scores(100, chat_id=200, message_id=42)
    finally:
        await client.close()
    assert len(result) == 2
    assert result[0].position == 1
    assert result[0].score == 5000
    assert result[1].position == 2


def test_game_in_message() -> None:
    """Game parsing from a Message.game payload."""
    msg = Message.from_dict(
        _sample_message_raw(
            1,
            game={
                "title": "My Awesome Game",
                "description": "A fun game",
                "photo": [{"file_id": "p1", "file_unique_id": "p1u", "width": 100, "height": 100}],
            },
        )
    )
    assert msg.game is not None
    assert msg.game.title == "My Awesome Game"
    assert msg.game.photo is not None
    assert msg.game.photo[0].file_id == "p1"


# ---------------------------------------------------------------------------
# T14: Business Accounts
# ---------------------------------------------------------------------------


async def test_get_business_connection(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "getBusinessConnection",
        lambda body: {
            "id": "conn_123",
            "user": SAMPLE_USER_RAW,
            "user_chat_id": 200,
            "date": 1700000000,
            "can_reply": True,
            "is_enabled": True,
        },
    )
    client = _client_for(test_server)
    try:
        result = await client.get_business_connection("conn_123")
    finally:
        await client.close()
    assert isinstance(result, BusinessConnection)
    assert result.id == "conn_123"
    assert result.can_reply is True


async def test_get_business_account_star_balance(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "getBusinessAccountStarBalance",
        lambda body: {"amount": 5000, "nanostar_amount": 5000000000},
    )
    client = _client_for(test_server)
    try:
        result = await client.get_business_account_star_balance("conn_123")
    finally:
        await client.close()
    assert isinstance(result, StarAmount)
    assert result.amount == 5000
    assert result.nanostar_amount == 5000000000


async def test_post_story(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("postStory", lambda body: {"id": 1})
    client = _client_for(test_server)
    try:
        result = await client.post_story(
            "conn_123",
            InputStoryContentPhoto(media="photo_file_id"),
            active_period=86400,
            caption="My story",
            areas=[
                StoryAreaTypeLocation(latitude=40.7128, longitude=-74.0060),
                StoryAreaTypeLink(url="https://example.com"),
            ],
        )
    finally:
        await client.close()
    assert result is not None
    body = server.calls_for("postStory")[0]["body"]
    assert body["business_connection_id"] == "conn_123"
    assert body["active_period"] == 86400
    assert body["caption"] == "My story"
    assert len(body["areas"]) == 2


async def test_send_message_with_business_connection_id(fake_server) -> None:
    """Regression test: send_message accepts business_connection_id."""
    server, test_server = fake_server
    server.set_response("sendMessage", lambda body: _sample_message_raw(1))
    client = _client_for(test_server)
    try:
        await client.send_message(
            200,
            "Hello from business",
            business_connection_id="conn_123",
        )
    finally:
        await client.close()
    body = server.calls_for("sendMessage")[0]["body"]
    assert body["business_connection_id"] == "conn_123"


def test_business_connection_in_update() -> None:
    """BusinessConnection parsing from an Update payload."""
    update = Update.from_dict(
        {
            "update_id": 1,
            "business_connection": {
                "id": "conn_123",
                "user": SAMPLE_USER_RAW,
                "user_chat_id": 200,
                "date": 1700000000,
                "can_reply": True,
                "is_enabled": True,
            },
        }
    )
    assert update.business_connection is not None
    assert update.business_connection.id == "conn_123"
