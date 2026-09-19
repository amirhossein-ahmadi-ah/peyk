"""Tests for T15: Chat Boosts & Gifts.

Uses the same FakeTelegramServer pattern from test_client.py.
"""

from __future__ import annotations

from typing import Any, Callable, Dict

import orjson
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms.telegram.client import TelegramClient
from peyk.platforms.telegram.models import (
    ChatBoost,
    ChatBoostRemoved,
    ChatBoostSource,
    ChatBoostSourceGiftCode,
    ChatBoostSourceGiveaway,
    ChatBoostSourcePremium,
    ChatBoostUpdated,
    Gift,
    Gifts,
    Giveaway,
    GiveawayCompleted,
    GiveawayWinners,
    Message,
    OwnedGift,
    OwnedGiftRegular,
    OwnedGiftUnique,
    UniqueGift,
    UserChatBoosts,
    parse_chat_boost_source,
    parse_owned_gift,
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


def _sample_message_raw(message_id: int = 1) -> Dict[str, Any]:
    return {
        "message_id": message_id,
        "date": 1690000000,
        "chat": SAMPLE_CHAT_RAW,
        "from": SAMPLE_USER_RAW,
        "text": "hello",
    }


class FakeTelegramServer:
    """A minimal aiohttp app mimicking `api.telegram.org` routing/shape."""

    def __init__(self) -> None:
        self.responses: Dict[str, Callable[[Any], Any]] = {}
        self.raw_envelopes: Dict[str, Any] = {}
        self.request_log: list[Dict[str, Any]] = []
        self.app = web.Application()
        self.app.router.add_route("POST", "/bot{token}/{method}", self._handle)

    def set_response(
        self, method_name: str, result_builder: Callable[[Any], Any]
    ) -> None:
        self.responses[method_name] = result_builder

    def set_raw_envelope(self, method_name: str, envelope: Any) -> None:
        self.raw_envelopes[method_name] = envelope

    async def _handle(self, request: web.Request) -> web.Response:
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
    server = FakeTelegramServer()
    async with TestServer(server.app) as test_server:
        yield server, test_server


def _client_for(
    test_server: TestServer, server: FakeTelegramServer
) -> TelegramClient:
    base_url = str(test_server.make_url("")).rstrip("/")
    return TelegramClient(
        TOKEN,
        base_url=base_url,
        retry_policy=RetryPolicy(max_attempts=3, base_backoff_seconds=0.001),
    )


# ---------------------------------------------------------------------------
# T15 client method tests
# ---------------------------------------------------------------------------


async def test_get_user_chat_boosts(fake_server) -> None:
    """Happy path: getUserChatBoosts parses boosts with mixed sources."""
    server, test_server = fake_server
    server.set_response(
        "getUserChatBoosts",
        lambda body: {
            "boosts": [
                {
                    "boost_id": "boost-1",
                    "add_date": 1700000000,
                    "expiration_date": 1700003600,
                    "source": {
                        "source": "premium",
                        "user": SAMPLE_USER_RAW,
                    },
                },
                {
                    "boost_id": "boost-2",
                    "add_date": 1700000100,
                    "expiration_date": 1700003700,
                    "source": {
                        "source": "gift_code",
                        "user": {
                            "id": 300,
                            "is_bot": False,
                            "first_name": "Gifter",
                        },
                    },
                },
                {
                    "boost_id": "boost-3",
                    "add_date": 1700000200,
                    "expiration_date": 1700003800,
                    "source": {
                        "source": "giveaway",
                        "giveaway_message_id": 42,
                        "user": {
                            "id": 400,
                            "is_bot": False,
                            "first_name": "Winner",
                        },
                        "is_unclaimed": False,
                        "prize_star_count": 100,
                    },
                },
            ]
        },
    )

    client = _client_for(test_server, server)
    try:
        result = await client.get_user_chat_boosts(
            chat_id=SAMPLE_CHAT_RAW["id"], user_id=SAMPLE_USER_RAW["id"]
        )
    finally:
        await client.close()

    assert isinstance(result, UserChatBoosts)
    assert len(result.boosts) == 3

    # Premium source
    assert result.boosts[0].boost_id == "boost-1"
    assert result.boosts[0].source.source == "premium"
    assert result.boosts[0].source.user.id == 100

    # Gift code source
    assert result.boosts[1].boost_id == "boost-2"
    assert result.boosts[1].source.source == "gift_code"
    assert result.boosts[1].source.user.id == 300

    # Giveaway source
    assert result.boosts[2].boost_id == "boost-3"
    assert result.boosts[2].source.source == "giveaway"
    assert result.boosts[2].source.giveaway_message_id == 42
    assert result.boosts[2].source.is_unclaimed is False
    assert result.boosts[2].source.prize_star_count == 100

    # Request shape
    calls = server.calls_for("getUserChatBoosts")
    assert len(calls) == 1
    assert calls[0]["body"]["chat_id"] == SAMPLE_CHAT_RAW["id"]
    assert calls[0]["body"]["user_id"] == SAMPLE_USER_RAW["id"]


async def test_send_gift(fake_server) -> None:
    """Happy path: sendGift sends correct payload."""
    server, test_server = fake_server
    server.set_response("sendGift", lambda body: True)

    client = _client_for(test_server, server)
    try:
        ok = await client.send_gift(
            user_id=500,
            gift_id="gift-123",
            text="Happy birthday!",
            pay_for_upgrade=True,
        )
    finally:
        await client.close()

    assert ok is True
    calls = server.calls_for("sendGift")
    assert len(calls) == 1
    body = calls[0]["body"]
    assert body["user_id"] == 500
    assert body["gift_id"] == "gift-123"
    assert body["text"] == "Happy birthday!"
    assert body["pay_for_upgrade"] is True


async def test_gift_premium_subscription(fake_server) -> None:
    """Happy path: giftPremiumSubscription sends correct payload."""
    server, test_server = fake_server
    server.set_response("giftPremiumSubscription", lambda body: True)

    client = _client_for(test_server, server)
    try:
        ok = await client.gift_premium_subscription(
            user_id=600,
            month_count=3,
            text="Enjoy your premium!",
        )
    finally:
        await client.close()

    assert ok is True
    calls = server.calls_for("giftPremiumSubscription")
    assert len(calls) == 1
    body = calls[0]["body"]
    assert body["user_id"] == 600
    assert body["month_count"] == 3
    assert body["text"] == "Enjoy your premium!"


async def test_get_available_gifts(fake_server) -> None:
    """Happy path: getAvailableGifts parses list of gifts."""
    server, test_server = fake_server
    server.set_response(
        "getAvailableGifts",
        lambda body: {
            "gifts": [
                {
                    "id": "gift-1",
                    "star_count": 100,
                    "total_count": 1000,
                    "remaining_count": 500,
                    "is_premium": False,
                    "has_colors": True,
                    "unique_gift_variant_count": 5,
                    "personal_total_count": 10,
                    "personal_remaining_count": 5,
                },
                {
                    "id": "gift-2",
                    "star_count": 200,
                    "total_count": 500,
                    "remaining_count": 250,
                    "is_premium": True,
                    "has_colors": False,
                    "unique_gift_variant_count": 3,
                    "personal_total_count": 5,
                    "personal_remaining_count": 2,
                },
            ]
        },
    )

    client = _client_for(test_server, server)
    try:
        result = await client.get_available_gifts()
    finally:
        await client.close()

    assert isinstance(result, Gifts)
    assert len(result.gifts) == 2

    assert result.gifts[0].id == "gift-1"
    assert result.gifts[0].star_count == 100
    assert result.gifts[0].total_count == 1000
    assert result.gifts[0].remaining_count == 500
    assert result.gifts[0].is_premium is False
    assert result.gifts[0].has_colors is True
    assert result.gifts[0].unique_gift_variant_count == 5
    assert result.gifts[0].personal_total_count == 10
    assert result.gifts[0].personal_remaining_count == 5

    assert result.gifts[1].id == "gift-2"
    assert result.gifts[1].star_count == 200
    assert result.gifts[1].is_premium is True

    calls = server.calls_for("getAvailableGifts")
    assert len(calls) == 1


# ---------------------------------------------------------------------------
# ChatBoostSource tagged union parsing
# ---------------------------------------------------------------------------


def test_chat_boost_source_premium_parsing() -> None:
    """ChatBoostSourcePremium parses correctly."""
    raw = {
        "source": "premium",
        "user": SAMPLE_USER_RAW,
    }
    result = parse_chat_boost_source(raw)
    assert isinstance(result, ChatBoostSourcePremium)
    assert result.source == "premium"
    assert result.user.id == 100
    assert result.user.first_name == "TestBot"


def test_chat_boost_source_gift_code_parsing() -> None:
    """ChatBoostSourceGiftCode parses correctly."""
    raw = {
        "source": "gift_code",
        "user": {"id": 200, "is_bot": False, "first_name": "Gifter"},
    }
    result = parse_chat_boost_source(raw)
    assert isinstance(result, ChatBoostSourceGiftCode)
    assert result.source == "gift_code"
    assert result.user.id == 200


def test_chat_boost_source_giveaway_parsing() -> None:
    """ChatBoostSourceGiveaway parses correctly."""
    raw = {
        "source": "giveaway",
        "giveaway_message_id": 99,
        "user": {"id": 300, "is_bot": False, "first_name": "Winner"},
        "is_unclaimed": True,
        "prize_star_count": 50,
    }
    result = parse_chat_boost_source(raw)
    assert isinstance(result, ChatBoostSourceGiveaway)
    assert result.source == "giveaway"
    assert result.giveaway_message_id == 99
    assert result.user.id == 300
    assert result.is_unclaimed is True
    assert result.prize_star_count == 50


def test_chat_boost_source_unknown_returns_none() -> None:
    """Unknown source type returns None."""
    raw = {"source": "unknown_type", "user": SAMPLE_USER_RAW}
    result = parse_chat_boost_source(raw)
    assert result is None


def test_chat_boost_source_none_returns_none() -> None:
    """None input returns None."""
    assert parse_chat_boost_source(None) is None


# ---------------------------------------------------------------------------
# OwnedGift tagged union parsing
# ---------------------------------------------------------------------------


def test_owned_gift_regular_parsing() -> None:
    """OwnedGiftRegular parses correctly."""
    raw = {
        "type": "regular",
        "gift": {
            "id": "gift-1",
            "star_count": 100,
            "total_count": 1000,
            "remaining_count": 500,
        },
        "date": 1700000000,
        "is_private": False,
        "is_saved": True,
    }
    result = parse_owned_gift(raw)
    assert isinstance(result, OwnedGiftRegular)
    assert result.type == "regular"
    assert result.gift.id == "gift-1"
    assert result.gift.star_count == 100
    assert result.date == 1700000000
    assert result.is_private is False
    assert result.is_saved is True


def test_owned_gift_unique_parsing() -> None:
    """OwnedGiftUnique parses correctly."""
    raw = {
        "type": "unique",
        "gift": {
            "id": "ug-1",
            "title": "Golden Glyph",
            "name": "golden_glyph",
            "number": 7,
            "is_premium": True,
            "is_burned": False,
            "is_from_blockchain": True,
            "gift_id": "gift-1",
        },
        "date": 1700000100,
        "is_private": True,
        "is_saved": False,
    }
    result = parse_owned_gift(raw)
    assert isinstance(result, OwnedGiftUnique)
    assert result.type == "unique"
    assert result.gift.id == "ug-1"
    assert result.gift.title == "Golden Glyph"
    assert result.gift.name == "golden_glyph"
    assert result.gift.number == 7
    assert result.gift.is_premium is True
    assert result.gift.is_burned is False
    assert result.gift.is_from_blockchain is True
    assert result.gift.gift_id == "gift-1"
    assert result.date == 1700000100
    assert result.is_private is True
    assert result.is_saved is False


def test_owned_gift_default_is_regular() -> None:
    """Missing type defaults to regular."""
    raw = {
        "gift": {"id": "gift-1", "star_count": 100},
        "date": 1700000000,
    }
    result = parse_owned_gift(raw)
    assert isinstance(result, OwnedGiftRegular)


def test_owned_gift_none_returns_none() -> None:
    """None input returns None."""
    assert parse_owned_gift(None) is None


# ---------------------------------------------------------------------------
# Giveaway / GiveawayWinners parsing from fake Message payload
# ---------------------------------------------------------------------------


def test_giveaway_parsing_from_message() -> None:
    """Giveaway model parses from a message payload."""
    giveaway_raw = {
        "chats": [SAMPLE_CHAT_RAW],
        "winners_selection_date": 1700005000,
        "winner_count": 5,
        "only_new_members": True,
        "has_public_winners": True,
        "prize_description": "Premium subscription",
        "country_codes": ["US", "GB"],
        "prize_star_count": 500,
        "premium_subscription_month_count": 3,
    }
    result = Giveaway.from_dict(giveaway_raw)
    assert result is not None
    assert len(result.chats) == 1
    assert result.chats[0].id == 200
    assert result.winners_selection_date == 1700005000
    assert result.winner_count == 5
    assert result.only_new_members is True
    assert result.has_public_winners is True
    assert result.prize_description == "Premium subscription"
    assert result.country_codes == ["US", "GB"]
    assert result.prize_star_count == 500
    assert result.premium_subscription_month_count == 3


def test_giveaway_winners_parsing_from_message() -> None:
    """GiveawayWinners model parses from a message payload."""
    winners_raw = {
        "giveaway_message_id": 42,
        "winners_selection_date": 1700005000,
        "winner_count": 3,
        "winners": [
            {"id": 101, "is_bot": False, "first_name": "Alice"},
            {"id": 102, "is_bot": False, "first_name": "Bob"},
            {"id": 103, "is_bot": False, "first_name": "Charlie"},
        ],
    }
    result = GiveawayWinners.from_dict(winners_raw)
    assert result is not None
    assert result.giveaway_message_id == 42
    assert result.winners_selection_date == 1700005000
    assert result.winner_count == 3
    assert len(result.winners) == 3
    assert result.winners[0].first_name == "Alice"
    assert result.winners[1].first_name == "Bob"
    assert result.winners[2].first_name == "Charlie"


def test_giveaway_completed_parsing_from_message() -> None:
    """GiveawayCompleted model parses from a message payload."""
    completed_raw = {
        "giveaway_message_id": 42,
        "winner_count": 3,
        "unclaimed_prize_count": 1,
    }
    result = GiveawayCompleted.from_dict(completed_raw)
    assert result is not None
    assert result.giveaway_message_id == 42
    assert result.winner_count == 3
    assert result.unclaimed_prize_count == 1


def test_message_with_giveaway_fields() -> None:
    """Message model preserves giveaway fields as passthroughs."""
    msg_raw = _sample_message_raw(1)
    msg_raw["giveaway"] = {
        "chats": [SAMPLE_CHAT_RAW],
        "winners_selection_date": 1700005000,
        "winner_count": 5,
    }
    msg_raw["giveaway_winners"] = {
        "giveaway_message_id": 1,
        "winners_selection_date": 1700005000,
        "winner_count": 2,
        "winners": [
            {"id": 101, "is_bot": False, "first_name": "Alice"},
            {"id": 102, "is_bot": False, "first_name": "Bob"},
        ],
    }
    msg_raw["giveaway_completed"] = {
        "giveaway_message_id": 1,
        "winner_count": 2,
        "unclaimed_prize_count": 0,
    }

    result = Message.from_dict(msg_raw)
    assert result is not None
    assert result.giveaway is not None
    assert result.giveaway.winner_count == 5
    assert result.giveaway_winners is not None
    assert result.giveaway_winners.winner_count == 2
    assert result.giveaway_completed is not None
    assert result.giveaway_completed.unclaimed_prize_count == 0


# ---------------------------------------------------------------------------
# ChatBoostUpdated / ChatBoostRemoved parsing from fake Update payload
# ---------------------------------------------------------------------------


def test_chat_boost_updated_parsing() -> None:
    """ChatBoostUpdated parses from an update payload."""
    raw = {
        "boost": {
            "boost_id": "boost-1",
            "add_date": 1700000000,
            "expiration_date": 1700003600,
            "source": {
                "source": "premium",
                "user": SAMPLE_USER_RAW,
            },
        }
    }
    result = ChatBoostUpdated.from_dict(raw)
    assert result is not None
    assert result.boost.boost_id == "boost-1"
    assert result.boost.source.source == "premium"
    assert result.boost.source.user.id == 100


def test_chat_boost_removed_parsing() -> None:
    """ChatBoostRemoved parses from an update payload."""
    raw = {
        "boost_id": "boost-1",
        "remove_date": 1700007200,
        "source": {
            "source": "gift_code",
            "user": {"id": 200, "is_bot": False, "first_name": "Gifter"},
        },
    }
    result = ChatBoostRemoved.from_dict(raw)
    assert result is not None
    assert result.boost_id == "boost-1"
    assert result.remove_date == 1700007200
    assert result.source.source == "gift_code"
    assert result.source.user.id == 200


async def test_update_with_chat_boost(fake_server) -> None:
    """Update.chat_boost is preserved as passthrough from getUpdates."""
    server, test_server = fake_server
    server.set_response(
        "getUpdates",
        lambda body: [
            {
                "update_id": 9001,
                "chat_boost": {
                    "boost": {
                        "boost_id": "boost-1",
                        "add_date": 1700000000,
                        "expiration_date": 1700003600,
                        "source": {
                            "source": "premium",
                            "user": SAMPLE_USER_RAW,
                        },
                    }
                },
            }
        ],
    )

    client = _client_for(test_server, server)
    try:
        updates = await client.get_updates()
    finally:
        await client.close()

    assert len(updates) == 1
    assert updates[0].update_id == 9001
    assert updates[0].chat_boost is not None
    assert updates[0].chat_boost.boost.boost_id == "boost-1"


async def test_update_with_removed_chat_boost(fake_server) -> None:
    """Update.removed_chat_boost is preserved as passthrough from getUpdates."""
    server, test_server = fake_server
    server.set_response(
        "getUpdates",
        lambda body: [
            {
                "update_id": 9002,
                "removed_chat_boost": {
                    "boost_id": "boost-2",
                    "remove_date": 1700007200,
                    "source": {
                        "source": "giveaway",
                        "giveaway_message_id": 42,
                        "user": {"id": 300, "is_bot": False, "first_name": "Winner"},
                        "is_unclaimed": False,
                        "prize_star_count": 100,
                    },
                },
            }
        ],
    )

    client = _client_for(test_server, server)
    try:
        updates = await client.get_updates()
    finally:
        await client.close()

    assert len(updates) == 1
    assert updates[0].update_id == 9002
    assert updates[0].removed_chat_boost is not None
    assert updates[0].removed_chat_boost.boost_id == "boost-2"
    assert updates[0].removed_chat_boost.source.source == "giveaway"


# ---------------------------------------------------------------------------
# UniqueGift parsing
# ---------------------------------------------------------------------------


def test_unique_gift_parsing() -> None:
    """UniqueGift model parses correctly."""
    raw = {
        "id": "ug-1",
        "title": "Golden Glyph",
        "name": "golden_glyph",
        "number": 7,
        "is_premium": True,
        "is_burned": False,
        "is_from_blockchain": True,
        "gift_id": "gift-1",
    }
    result = UniqueGift.from_dict(raw)
    assert result is not None
    assert result.id == "ug-1"
    assert result.title == "Golden Glyph"
    assert result.name == "golden_glyph"
    assert result.number == 7
    assert result.is_premium is True
    assert result.is_burned is False
    assert result.is_from_blockchain is True
    assert result.gift_id == "gift-1"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


def test_chat_boost_source_premium_defaults() -> None:
    """ChatBoostSourcePremium uses correct defaults."""
    raw = {"source": "premium"}
    result = parse_chat_boost_source(raw)
    assert isinstance(result, ChatBoostSourcePremium)
    assert result.user is None


def test_chat_boost_source_giveaway_defaults() -> None:
    """ChatBoostSourceGiveaway uses correct defaults."""
    raw = {"source": "giveaway"}
    result = parse_chat_boost_source(raw)
    assert isinstance(result, ChatBoostSourceGiveaway)
    assert result.giveaway_message_id is None
    assert result.user is None
    assert result.is_unclaimed is None
    assert result.prize_star_count is None


def test_gift_defaults() -> None:
    """Gift model uses correct defaults for optional fields."""
    raw = {"id": "gift-1", "star_count": 100}
    result = Gift.from_dict(raw)
    assert result is not None
    assert result.id == "gift-1"
    assert result.star_count == 100
    assert result.total_count is None
    assert result.remaining_count is None
    assert result.is_premium is None
    assert result.has_colors is None


def test_user_chat_boosts_empty() -> None:
    """UserChatBoosts handles empty boosts list."""
    raw = {"boosts": []}
    result = UserChatBoosts.from_dict(raw)
    assert result is not None
    assert result.boosts == []


def test_gifts_empty() -> None:
    """Gifts handles empty gifts list."""
    raw = {"gifts": []}
    result = Gifts.from_dict(raw)
    assert result is not None
    assert result.gifts == []
