"""Tests for Telegram T1 models: deep parsing, unions, updates, webhook."""

from __future__ import annotations

from peyk.platforms.telegram.errors import ResponseParameters
from peyk.platforms.telegram.models import (
    Chat,
    ChatFullInfo,
    ExternalReplyInfo,
    InaccessibleMessage,
    Message,
    MessageEntity,
    MessageId,
    ReplyParameters,
    TextQuote,
    Update,
    User,
    WebhookInfo,
    parse_maybe_inaccessible_message,
)

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


def _sample_message_raw(message_id: int = 1) -> dict:
    return {
        "message_id": message_id,
        "date": 1690000000,
        "chat": SAMPLE_CHAT_RAW,
        "from": SAMPLE_USER_RAW,
        "text": "hello",
    }


def test_user_parses_all_fields() -> None:
    user = User.from_dict(
        {
            "id": 1,
            "is_bot": False,
            "first_name": "Sara",
            "last_name": "Ahmadi",
            "username": "sara_a",
            "language_code": "fa",
            "is_premium": True,
            "can_join_groups": True,
            "can_read_all_group_messages": False,
            "supports_inline_queries": True,
        }
    )
    assert user.id == 1
    assert user.is_bot is False
    assert user.first_name == "Sara"
    assert user.last_name == "Ahmadi"
    assert user.username == "sara_a"
    assert user.language_code == "fa"
    assert user.is_premium is True
    assert user.can_join_groups is True
    assert user.supports_inline_queries is True


def test_user_defaults_and_none() -> None:
    user = User.from_dict({"id": 1, "first_name": "Bot"})
    assert user.is_bot is False
    assert user.last_name is None
    assert User.from_dict(None) is None


def test_chat_and_full_info() -> None:
    chat = Chat.from_dict({"id": 5, "type": "supergroup", "title": "G"})
    assert chat.type == "supergroup"
    assert chat.title == "G"
    assert chat.is_forum is None

    full = ChatFullInfo.from_dict(
        {
            "id": 5,
            "type": "supergroup",
            "title": "G",
            "description": "desc",
            "invite_link": "https://t.me/+x",
            "pinned_message": _sample_message_raw(9),
            "slow_mode_delay": 10,
            "sticker_set_name": "set",
        }
    )
    assert full.description == "desc"
    assert full.invite_link == "https://t.me/+x"
    assert isinstance(full.pinned_message, Message)
    assert full.pinned_message.message_id == 9
    assert full.slow_mode_delay == 10


def test_message_deep_parsing_reply_and_entities() -> None:
    raw = _sample_message_raw(11)
    raw["entities"] = [
        {"type": "bold", "offset": 0, "length": 5},
        {
            "type": "text_mention",
            "offset": 6,
            "length": 4,
            "user": {"id": 7, "is_bot": False, "first_name": "X"},
        },
    ]
    raw["reply_to_message"] = {
        "message_id": 10,
        "date": 1689999999,
        "chat": SAMPLE_CHAT_RAW,
        "from": {"id": 7, "is_bot": False, "first_name": "X"},
        "text": "original",
    }
    raw["quote"] = {"text": "orig", "position": 0}
    raw["external_reply"] = {
        "chat": SAMPLE_CHAT_RAW,
        "message_id": 3,
        "quote": {"text": "q"},
    }

    msg = Message.from_dict(raw)
    assert msg.message_id == 11
    assert msg.from_.id == 100
    assert msg.chat.id == 200
    assert msg.entities[0] == MessageEntity(type="bold", offset=0, length=5)
    assert msg.entities[1].user.first_name == "X"
    # Nested reply proves recursive parsing, not just flat fields.
    assert isinstance(msg.reply_to_message, Message)
    assert msg.reply_to_message.message_id == 10
    assert msg.reply_to_message.text == "original"
    assert msg.reply_to_message.from_.id == 7
    assert isinstance(msg.quote, TextQuote)
    assert msg.quote.text == "orig"
    assert isinstance(msg.external_reply, ExternalReplyInfo)
    assert msg.external_reply.message_id == 3
    assert msg.external_reply.quote.text == "q"


def test_message_new_chat_members_and_service_fields() -> None:
    raw = _sample_message_raw(12)
    raw["new_chat_members"] = [
        {"id": 21, "is_bot": False, "first_name": "A"},
        {"id": 22, "is_bot": True, "first_name": "B"},
    ]
    raw["left_chat_member"] = {"id": 23, "is_bot": False, "first_name": "C"}
    raw["new_chat_title"] = "New title"
    raw["migrate_to_chat_id"] = 999
    msg = Message.from_dict(raw)
    assert [u.id for u in msg.new_chat_members] == [21, 22]
    assert msg.left_chat_member.first_name == "C"
    assert msg.new_chat_title == "New title"
    assert msg.migrate_to_chat_id == 999


def test_maybe_inaccessible_both_branches() -> None:
    normal = parse_maybe_inaccessible_message(_sample_message_raw(1))
    assert isinstance(normal, Message)
    assert not isinstance(normal, InaccessibleMessage)

    inaccessible = parse_maybe_inaccessible_message(
        {"message_id": 2, "date": 0, "chat": SAMPLE_CHAT_RAW}
    )
    assert isinstance(inaccessible, InaccessibleMessage)
    assert inaccessible.message_id == 2
    assert inaccessible.date == 0
    assert inaccessible.chat.id == 200

    assert parse_maybe_inaccessible_message(None) is None


def test_message_id_and_reply_parameters() -> None:
    assert MessageId.from_dict({"message_id": 42}).message_id == 42
    rp = ReplyParameters.from_dict(
        {
            "message_id": 5,
            "quote": "hi",
            "quote_entities": [{"type": "italic", "offset": 0, "length": 2}],
        }
    )
    assert rp.message_id == 5
    assert rp.quote == "hi"
    assert rp.quote_entities[0].type == "italic"


def test_update_parses_message_variants() -> None:
    upd = Update.from_dict(
        {"update_id": 1, "message": _sample_message_raw(1)}
    )
    assert upd.update_id == 1
    assert upd.message.text == "hello"
    assert upd.edited_message is None

    upd2 = Update.from_dict(
        {
            "update_id": 2,
            "channel_post": _sample_message_raw(3),
            "edited_channel_post": _sample_message_raw(4),
        }
    )
    assert upd2.channel_post.message_id == 3
    assert upd2.edited_channel_post.message_id == 4

    assert Update.list_from_result([]) == []


def test_webhook_info_and_response_parameters() -> None:
    info = WebhookInfo.from_dict(
        {
            "url": "https://example.com/hook",
            "has_custom_certificate": False,
            "pending_update_count": 3,
            "ip_address": "1.2.3.4",
            "last_error_message": "boom",
            "max_connections": 40,
            "allowed_updates": ["message", "callback_query"],
        }
    )
    assert info.url == "https://example.com/hook"
    assert info.pending_update_count == 3
    assert info.ip_address == "1.2.3.4"
    assert info.allowed_updates == ["message", "callback_query"]

    params = ResponseParameters.from_dict(
        {"migrate_to_chat_id": 11, "retry_after": 30}
    )
    assert params.migrate_to_chat_id == 11
    assert params.retry_after == 30
    assert ResponseParameters.from_dict(None) is None
