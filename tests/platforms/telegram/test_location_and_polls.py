"""Tests for `TelegramClient` location/poll/dice methods (Phase T4).

Fake `aiohttp.test_utils` server, zero real network. Covers one
happy path per method, regular + quiz polls, and the newer poll
fields (`media`, `members_only`, `country_codes`) with
confirmed-working examples.
"""

from __future__ import annotations

from typing import Any, Callable, Dict

import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms.telegram.client import TelegramClient
from peyk.platforms.telegram.models import (
    Contact,
    Dice,
    InputMediaLink,
    InputMediaLocation,
    InputMediaPhoto,
    InputPollOption,
    Location,
    Message,
    Poll,
    PollMedia,
    Venue,
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


def _sample_poll_raw() -> Dict[str, Any]:
    return {
        "id": "poll1",
        "question": "Best?",
        "options": [
            {"text": "A", "voter_count": 3},
            {"text": "B", "voter_count": 5},
        ],
        "total_voter_count": 8,
        "is_closed": False,
        "is_anonymous": True,
        "type": "regular",
        "allows_multiple_answers": False,
        "allows_revoting": True,
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
        import orjson

        method_name = request.match_info["method"]
        token = request.match_info["token"]
        raw = await request.read()
        parsed_body: Any = orjson.loads(raw) if raw else {}
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


async def test_send_location(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "sendLocation",
        lambda body: _sample_message_raw(
            1, location={"latitude": 35.7, "longitude": 51.4,
                         "live_period": 900},
        ),
    )
    client = _client_for(test_server)
    try:
        msg = await client.send_location(200, 35.7, 51.4, live_period=900)
    finally:
        await client.close()
    assert msg.location == Location(35.7, 51.4, None, 900, None, None)
    assert server.calls_for("sendLocation")[0]["body"] == {
        "chat_id": 200, "latitude": 35.7, "longitude": 51.4,
        "live_period": 900,
    }


async def test_edit_and_stop_live_location(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "editMessageLiveLocation",
        lambda body: _sample_message_raw(
            2, location={"latitude": 35.8, "longitude": 51.5},
        ),
    )
    server.set_response(
        "stopMessageLiveLocation",
        lambda body: True
        if "inline_message_id" in body
        else _sample_message_raw(2),
    )
    client = _client_for(test_server)
    try:
        edited = await client.edit_message_live_location(
            35.8, 51.5, chat_id=200, message_id=2, heading=90
        )
        assert isinstance(edited, Message)
        assert edited.location.latitude == 35.8
        stopped = await client.stop_message_live_location(
            inline_message_id="ABC"
        )
        assert stopped is True
    finally:
        await client.close()
    assert server.calls_for("editMessageLiveLocation")[0]["body"] == {
        "chat_id": 200, "message_id": 2,
        "latitude": 35.8, "longitude": 51.5, "heading": 90,
    }
    assert server.calls_for("stopMessageLiveLocation")[0]["body"] == {
        "inline_message_id": "ABC",
    }


async def test_send_venue(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "sendVenue",
        lambda body: _sample_message_raw(
            3, venue={"location": {"latitude": 35.7, "longitude": 51.4},
                      "title": "Cafe", "address": "Street 1",
                      "foursquare_id": "fsq1"},
        ),
    )
    client = _client_for(test_server)
    try:
        msg = await client.send_venue(
            200, 35.7, 51.4, "Cafe", "Street 1", foursquare_id="fsq1"
        )
    finally:
        await client.close()
    assert isinstance(msg.venue, Venue)
    assert msg.venue.title == "Cafe"
    assert msg.venue.location.latitude == 35.7
    assert msg.venue.foursquare_id == "fsq1"
    assert server.calls_for("sendVenue")[0]["body"]["address"] == "Street 1"


async def test_send_contact(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "sendContact",
        lambda body: _sample_message_raw(
            4, contact={"phone_number": "+123", "first_name": "A",
                        "last_name": "B", "vcard": "VC"},
        ),
    )
    client = _client_for(test_server)
    try:
        msg = await client.send_contact(
            200, "+123", "A", last_name="B", vcard="VC"
        )
    finally:
        await client.close()
    assert msg.contact == Contact("+123", "A", "B", None, "VC")
    assert server.calls_for("sendContact")[0]["body"] == {
        "chat_id": 200, "phone_number": "+123", "first_name": "A",
        "last_name": "B", "vcard": "VC",
    }


async def test_send_regular_poll(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "sendPoll", lambda body: _sample_message_raw(5, poll=_sample_poll_raw())
    )
    client = _client_for(test_server)
    try:
        msg = await client.send_poll(
            200, "Best?", ["A", "B"],
            is_anonymous=False, allows_multiple_answers=True,
        )
    finally:
        await client.close()
    assert isinstance(msg.poll, Poll)
    assert msg.poll.question == "Best?"
    assert [o.text for o in msg.poll.options] == ["A", "B"]
    assert msg.poll.total_voter_count == 8
    body = server.calls_for("sendPoll")[0]["body"]
    assert body["options"] == [{"text": "A"}, {"text": "B"}]
    assert body["is_anonymous"] is False
    assert body["allows_multiple_answers"] is True


async def test_send_quiz_poll(fake_server) -> None:
    server, test_server = fake_server

    def _result(body: Any) -> Any:
        assert body["type"] == "quiz"
        assert body["correct_option_ids"] == [1]
        assert body["explanation"] == "Because."
        assert body["open_period"] == 60
        raw = _sample_poll_raw()
        raw.update({"type": "quiz", "correct_option_ids": [1],
                    "explanation": "Because."})
        return _sample_message_raw(6, poll=raw)

    server.set_response("sendPoll", _result)
    client = _client_for(test_server)
    try:
        msg = await client.send_poll(
            200, "Best?", ["A", "B"], type="quiz",
            correct_option_ids=[1], explanation="Because.", open_period=60,
        )
    finally:
        await client.close()
    assert msg.poll.type == "quiz"
    assert msg.poll.correct_option_ids == [1]
    assert msg.poll.explanation == "Because."


async def test_send_poll_newer_fields(fake_server) -> None:
    server, test_server = fake_server

    def _result(body: Any) -> Any:
        assert body["members_only"] is True
        assert body["country_codes"] == ["US", "FT"]
        assert body["media"] == {"type": "photo", "media": "PHOTO_ID"}
        assert body["explanation_media"] == {
            "type": "location", "latitude": 1.0, "longitude": 2.0,
        }
        assert body["options"][0]["media"] == {
            "type": "link", "url": "https://example.com",
        }
        assert body["question_entities"] == [
            {"type": "bold", "offset": 0, "length": 4}
        ]
        raw = _sample_poll_raw()
        raw.update({"members_only": True, "country_codes": ["US", "FT"]})
        return _sample_message_raw(7, poll=raw)

    server.set_response("sendPoll", _result)
    client = _client_for(test_server)
    try:
        msg = await client.send_poll(
            200, "Best?", [InputPollOption(
                "A", media=InputMediaLink("https://example.com"))],
            members_only=True,
            country_codes=["US", "FT"],
            media=InputMediaPhoto("PHOTO_ID"),
            explanation_media=InputMediaLocation(1.0, 2.0),
            question_entities=[
                {"type": "bold", "offset": 0, "length": 4}
            ],
        )
    finally:
        await client.close()
    assert msg.poll.members_only is True
    assert msg.poll.country_codes == ["US", "FT"]


async def test_poll_option_upload_media_rejected() -> None:
    with pytest.raises(ValueError):
        InputPollOption("A", media=InputMediaPhoto(b"BYTES")).to_dict()


async def test_stop_poll(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("stopPoll", lambda body: _sample_poll_raw())
    client = _client_for(test_server)
    try:
        poll = await client.stop_poll(200, 5)
    finally:
        await client.close()
    assert isinstance(poll, Poll)
    assert poll.id == "poll1"
    assert server.calls_for("stopPoll")[0]["body"] == {
        "chat_id": 200, "message_id": 5,
    }


async def test_send_dice(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "sendDice",
        lambda body: _sample_message_raw(
            8, dice={"emoji": "🎲", "value": 4},
        ),
    )
    client = _client_for(test_server)
    try:
        msg = await client.send_dice(200, emoji="🎲")
    finally:
        await client.close()
    assert msg.dice == Dice("🎲", 4)
    assert server.calls_for("sendDice")[0]["body"] == {
        "chat_id": 200, "emoji": "🎲",
    }


async def test_poll_media_parsing() -> None:
    media = PollMedia.from_dict(
        {"link": {"url": "https://example.com"},
         "location": {"latitude": 1.0, "longitude": 2.0}}
    )
    assert media.link.url == "https://example.com"
    assert media.location.latitude == 1.0
    assert media.photo is None
    assert PollMedia.from_dict(None) is None
