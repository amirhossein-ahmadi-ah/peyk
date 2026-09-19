"""Tests for `TelegramClient` inline mode (Phase T9).

Fake `aiohttp.test_utils` server, zero real network. Covers
`answer_inline_query` (mixed non-cached + cached results, button,
optionals), `save_prepared_inline_message`, `InputMessageContent`
text/location variants inside an article, `ChosenInlineResult` parsing
from an `Update` payload, and `InlineQuery` parsing with `location`
both present and absent.
"""

from __future__ import annotations

from typing import Any, Callable, Dict

import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms.telegram.client import TelegramClient
from peyk.platforms.telegram.models import (
    ChosenInlineResult,
    InlineQuery,
    InlineQueryResultArticle,
    InlineQueryResultCachedAudio,
    InlineQueryResultCachedDocument,
    InlineQueryResultCachedGif,
    InlineQueryResultCachedMpeg4Gif,
    InlineQueryResultCachedPhoto,
    InlineQueryResultCachedSticker,
    InlineQueryResultCachedVideo,
    InlineQueryResultCachedVoice,
    InlineQueryResultContact,
    InlineQueryResultDocument,
    InlineQueryResultGame,
    InlineQueryResultGif,
    InlineQueryResultLocation,
    InlineQueryResultMpeg4Gif,
    InlineQueryResultPhoto,
    InlineQueryResultVenue,
    InlineQueryResultVideo,
    InlineQueryResultVoice,
    InlineQueryResultAudio,
    InlineQueryResultsButton,
    InputContactMessageContent,
    InputInvoiceMessageContent,
    InputLocationMessageContent,
    InputTextMessageContent,
    InputVenueMessageContent,
    LabeledPrice,
    Location,
    PreparedInlineMessage,
    Update,
)
from peyk.transport import RetryPolicy

TOKEN = "12345:TEST-TOKEN"

SAMPLE_USER_RAW = {
    "id": 100,
    "is_bot": False,
    "first_name": "Some",
    "username": "someone",
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


def _article_with_text() -> InlineQueryResultArticle:
    return InlineQueryResultArticle(
        id="a1",
        title="Hello",
        input_message_content=InputTextMessageContent(
            message_text="Hello *world*",
            parse_mode="Markdown",
        ),
        description="A greeting",
        url="https://example.com/hello",
    )


def _cached_photo() -> InlineQueryResultCachedPhoto:
    return InlineQueryResultCachedPhoto(
        id="c1",
        photo_file_id="FILEID123",
        title="Cached pic",
        caption="look",
    )


async def test_answer_inline_query_mixed_results(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("answerInlineQuery", lambda body: True)
    client = _client_for(test_server)
    try:
        ok = await client.answer_inline_query(
            "qid-1",
            [_article_with_text(), _cached_photo()],
            cache_time=60,
            is_personal=True,
            next_offset="page2",
            button=InlineQueryResultsButton(
                text="More", start_parameter="deep-link_1"
            ),
        )
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("answerInlineQuery")[0]["body"]
    assert body == {
        "inline_query_id": "qid-1",
        "results": [
            {
                "type": "article",
                "id": "a1",
                "title": "Hello",
                "input_message_content": {
                    "message_text": "Hello *world*",
                    "parse_mode": "Markdown",
                },
                "url": "https://example.com/hello",
                "description": "A greeting",
            },
            {
                "type": "photo",
                "id": "c1",
                "photo_file_id": "FILEID123",
                "title": "Cached pic",
                "caption": "look",
            },
        ],
        "cache_time": 60,
        "is_personal": True,
        "next_offset": "page2",
        "button": {"text": "More", "start_parameter": "deep-link_1"},
    }


async def test_answer_inline_query_minimal_and_raw_mapping(
    fake_server,
) -> None:
    server, test_server = fake_server
    server.set_response("answerInlineQuery", lambda body: True)
    client = _client_for(test_server)
    try:
        ok = await client.answer_inline_query(
            "qid-2",
            [{"type": "game", "id": "g1", "game_short_name": "chess"}],
        )
    finally:
        await client.close()
    assert ok is True
    body = server.calls_for("answerInlineQuery")[0]["body"]
    assert body == {
        "inline_query_id": "qid-2",
        "results": [
            {"type": "game", "id": "g1", "game_short_name": "chess"}
        ],
    }


async def test_save_prepared_inline_message(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "savePreparedInlineMessage",
        lambda body: {"id": "prep-1", "expiration_date": 1893456000},
    )
    client = _client_for(test_server)
    try:
        prepared = await client.save_prepared_inline_message(
            100,
            _cached_photo(),
            allow_user_chats=True,
            allow_group_chats=True,
        )
    finally:
        await client.close()
    assert prepared == PreparedInlineMessage(
        id="prep-1", expiration_date=1893456000
    )
    body = server.calls_for("savePreparedInlineMessage")[0]["body"]
    assert body == {
        "user_id": 100,
        "result": {
            "type": "photo",
            "id": "c1",
            "photo_file_id": "FILEID123",
            "title": "Cached pic",
            "caption": "look",
        },
        "allow_user_chats": True,
        "allow_group_chats": True,
    }


def test_input_text_and_location_content_in_article() -> None:
    text_article = InlineQueryResultArticle(
        id="t1",
        title="Text",
        input_message_content=InputTextMessageContent(
            message_text="hi",
            entities=[
                {"type": "bold", "offset": 0, "length": 2},
            ],
        ),
    )
    assert text_article.to_dict()["input_message_content"] == {
        "message_text": "hi",
        "entities": [{"type": "bold", "offset": 0, "length": 2}],
    }

    loc_article = InlineQueryResultArticle(
        id="l1",
        title="Spot",
        input_message_content=InputLocationMessageContent(
            latitude=35.7,
            longitude=51.4,
            live_period=900,
        ),
    )
    assert loc_article.to_dict()["input_message_content"] == {
        "latitude": 35.7,
        "longitude": 51.4,
        "live_period": 900,
    }


def test_input_venue_contact_invoice_shapes() -> None:
    venue = InputVenueMessageContent(
        latitude=35.7,
        longitude=51.4,
        title="Hall",
        address="1 Main St",
        foursquare_id="fsq1",
    )
    assert venue.to_dict() == {
        "latitude": 35.7,
        "longitude": 51.4,
        "title": "Hall",
        "address": "1 Main St",
        "foursquare_id": "fsq1",
    }

    contact = InputContactMessageContent(
        phone_number="+989121234567", first_name="Some"
    )
    assert contact.to_dict() == {
        "phone_number": "+989121234567",
        "first_name": "Some",
    }

    invoice = InputInvoiceMessageContent(
        title="Widget",
        description="A fine widget",
        payload="inv-1",
        currency="USD",
        prices=[LabeledPrice(label="Widget", amount=199)],
        need_name=True,
    )
    assert invoice.to_dict() == {
        "title": "Widget",
        "description": "A fine widget",
        "payload": "inv-1",
        "currency": "USD",
        "prices": [{"label": "Widget", "amount": 199}],
        "need_name": True,
    }


async def test_chosen_inline_result_parsing_from_update(
    fake_server,
) -> None:
    server, test_server = fake_server
    raw_chosen = {
        "result_id": "c1",
        "from": SAMPLE_USER_RAW,
        "location": {"latitude": 35.7, "longitude": 51.4},
        "inline_message_id": "im-1",
        "query": "pic",
    }
    server.set_response(
        "getUpdates", lambda body: [{"update_id": 7, **{"chosen_inline_result": raw_chosen}}],
    )
    client = _client_for(test_server)
    try:
        updates = await client.get_updates()
    finally:
        await client.close()
    assert len(updates) == 1
    chosen = updates[0].chosen_inline_result
    assert isinstance(chosen, ChosenInlineResult)
    assert chosen.result_id == "c1"
    assert chosen.from_ is not None and chosen.from_.id == 100
    assert chosen.location == Location(35.7, 51.4, None, None, None, None)
    assert chosen.inline_message_id == "im-1"
    assert chosen.query == "pic"


async def test_inline_query_parsing_location_present_and_absent(
    fake_server,
) -> None:
    server, test_server = fake_server
    with_loc = {
        "id": "q1",
        "from": SAMPLE_USER_RAW,
        "query": "cafe",
        "offset": "",
        "chat_type": "private",
        "location": {
            "latitude": 35.7,
            "longitude": 51.4,
            "horizontal_accuracy": 50.0,
        },
    }
    without_loc = {
        "id": "q2",
        "from": SAMPLE_USER_RAW,
        "query": "news",
        "offset": "10",
    }
    server.set_response(
        "getUpdates",
        lambda body: [
            {"update_id": 8, "inline_query": with_loc},
            {"update_id": 9, "inline_query": without_loc},
        ],
    )
    client = _client_for(test_server)
    try:
        updates = await client.get_updates()
    finally:
        await client.close()
    first = updates[0].inline_query
    assert isinstance(first, InlineQuery)
    assert first.id == "q1"
    assert first.query == "cafe"
    assert first.chat_type == "private"
    assert first.location == Location(35.7, 51.4, 50.0, None, None, None)

    second = updates[1].inline_query
    assert isinstance(second, InlineQuery)
    assert second.id == "q2"
    assert second.offset == "10"
    assert second.chat_type is None
    assert second.location is None


def test_results_button_requires_exactly_one_optional() -> None:
    button = InlineQueryResultsButton(
        text="Connect", start_parameter="connect_1"
    )
    assert button.to_dict() == {
        "text": "Connect",
        "start_parameter": "connect_1",
    }
    import pytest as _pytest

    with _pytest.raises(ValueError):
        InlineQueryResultsButton(text="Bad")
    with _pytest.raises(ValueError):
        InlineQueryResultsButton(
            text="Bad",
            web_app={"url": "https://example.com"},
            start_parameter="x",
        )


def test_all_result_subtype_tags_serialize() -> None:
    cases = [
        (
            InlineQueryResultPhoto(
                id="1", photo_url="https://e.com/p.jpg",
                thumbnail_url="https://e.com/t.jpg",
            ),
            {"type": "photo", "photo_url": "https://e.com/p.jpg"},
        ),
        (
            InlineQueryResultGif(
                id="1", gif_url="https://e.com/a.gif",
                thumbnail_url="https://e.com/t.jpg",
            ),
            {"type": "gif", "gif_url": "https://e.com/a.gif"},
        ),
        (
            InlineQueryResultMpeg4Gif(
                id="1", mpeg4_url="https://e.com/a.mp4",
                thumbnail_url="https://e.com/t.jpg",
            ),
            {"type": "mpeg4_gif", "mpeg4_url": "https://e.com/a.mp4"},
        ),
        (
            InlineQueryResultVideo(
                id="1", video_url="https://e.com/v.mp4",
                mime_type="video/mp4",
                thumbnail_url="https://e.com/t.jpg", title="V",
            ),
            {"type": "video", "mime_type": "video/mp4", "title": "V"},
        ),
        (
            InlineQueryResultAudio(
                id="1", audio_url="https://e.com/a.mp3", title="A"
            ),
            {"type": "audio", "title": "A"},
        ),
        (
            InlineQueryResultVoice(
                id="1", voice_url="https://e.com/v.ogg", title="V"
            ),
            {"type": "voice", "title": "V"},
        ),
        (
            InlineQueryResultDocument(
                id="1", title="D", document_url="https://e.com/d.pdf",
                mime_type="application/pdf",
            ),
            {"type": "document", "mime_type": "application/pdf"},
        ),
        (
            InlineQueryResultLocation(
                id="1", latitude=1.0, longitude=2.0, title="L"
            ),
            {"type": "location", "latitude": 1.0, "longitude": 2.0},
        ),
        (
            InlineQueryResultVenue(
                id="1", latitude=1.0, longitude=2.0,
                title="V", address="Addr",
            ),
            {"type": "venue", "address": "Addr"},
        ),
        (
            InlineQueryResultContact(
                id="1", phone_number="+1", first_name="A"
            ),
            {"type": "contact", "phone_number": "+1"},
        ),
        (
            InlineQueryResultGame(id="1", game_short_name="chess"),
            {"type": "game", "game_short_name": "chess"},
        ),
        (
            InlineQueryResultCachedGif(id="1", gif_file_id="GIFID"),
            {"type": "gif", "gif_file_id": "GIFID"},
        ),
        (
            InlineQueryResultCachedMpeg4Gif(id="1", mpeg4_file_id="M4ID"),
            {"type": "mpeg4_gif", "mpeg4_file_id": "M4ID"},
        ),
        (
            InlineQueryResultCachedSticker(id="1", sticker_file_id="STID"),
            {"type": "sticker", "sticker_file_id": "STID"},
        ),
        (
            InlineQueryResultCachedDocument(
                id="1", title="D", document_file_id="DOCID"
            ),
            {"type": "document", "document_file_id": "DOCID"},
        ),
        (
            InlineQueryResultCachedVideo(
                id="1", video_file_id="VID", title="V"
            ),
            {"type": "video", "video_file_id": "VID"},
        ),
        (
            InlineQueryResultCachedVoice(
                id="1", voice_file_id="VOI", title="V"
            ),
            {"type": "voice", "voice_file_id": "VOI"},
        ),
        (
            InlineQueryResultCachedAudio(id="1", audio_file_id="AUD"),
            {"type": "audio", "audio_file_id": "AUD"},
        ),
    ]
    for result, expected in cases:
        body = result.to_dict()
        for key, value in expected.items():
            assert body[key] == value, result


def test_update_without_inline_fields_stays_none() -> None:
    update = Update.from_dict({"update_id": 42})
    assert update.inline_query is None
    assert update.chosen_inline_result is None
