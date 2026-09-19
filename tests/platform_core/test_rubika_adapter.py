from peyk.platform_core.adapters.rubika import RUBIKA_CAPABILITIES, normalize_bot_membership, normalize_callback, normalize_chat_member, normalize_deleted, normalize_message, normalize_update
from peyk.platform_core.contracts import IncomingBotMembershipChange, IncomingCallbackQuery, IncomingMessage, IncomingMessageDeleted
from peyk.platforms.rubika.models import AuxData, Event, EventTypeEnum, InlineMessage, Message, Update, UpdateTypeEnum


def test_message_normalization_is_honest_about_missing_chat_and_payment() -> None:
    raw = Message(message_id="m1", text="hello", sender_id="u1", time=123, reply_to_message_id="m0")
    normalized = normalize_message(raw)
    assert isinstance(normalized, IncomingMessage)
    assert normalized.message_id == "m1"
    assert normalized.sender_id == "u1"
    assert normalized.chat_id is None  # Message itself has no chat_id in Rubika.
    assert normalized.reply_to_message_id == "m0"
    assert normalized.new_chat_members is None
    assert normalized.left_chat_member is None
    assert normalized.successful_payment is None
    assert normalized.raw is raw


def test_rubika_update_supplies_chat_id_without_fabricating_it_in_message_model() -> None:
    raw_message = Message(message_id="m1", text="hello", sender_id="u1")
    raw_update = Update(type=UpdateTypeEnum.NEW_MESSAGE, chat_id="c1", new_message=raw_message)
    normalized = normalize_update(raw_update)
    assert isinstance(normalized, IncomingMessage)
    assert normalized.chat_id == "c1"
    assert normalized.raw is raw_message


def test_button_id_maps_to_common_callback_data_field() -> None:
    raw = InlineMessage(sender_id="u1", text="x", message_id="m1", chat_id="c1", aux_data=AuxData(button_id="btn-42"))
    normalized = normalize_callback(raw)
    assert isinstance(normalized, IncomingCallbackQuery)
    assert normalized.id is None
    assert normalized.data == "btn-42"
    assert normalized.from_user_id == "u1"
    assert normalized.chat_id == "c1"
    assert normalized.message_id == "m1"
    assert normalized.raw is raw


def test_rubika_bot_membership_events_are_explicit_and_actor_is_not_invented() -> None:
    joined = Event(type=EventTypeEnum.BOT_JOINED, join_type="Member")
    removed = Event(type=EventTypeEnum.BOT_REMOVED)
    j = normalize_bot_membership(joined, chat_id="c1")
    r = normalize_bot_membership(removed, chat_id="c1")
    assert isinstance(j, IncomingBotMembershipChange)
    assert j.added is True and j.chat_id == "c1" and j.actor_id is None and j.raw is joined
    assert isinstance(r, IncomingBotMembershipChange)
    assert r.added is False and r.actor_id is None and r.raw is removed


def test_rubika_removed_message_is_normalized() -> None:
    raw = Update(type=UpdateTypeEnum.REMOVED_MESSAGE, chat_id="c1", removed_message_id="m9")
    normalized = normalize_deleted(raw)
    assert isinstance(normalized, IncomingMessageDeleted)
    assert normalized.chat_id == "c1"
    assert normalized.message_id == "m9"
    assert normalized.raw is raw


def test_rubika_has_no_rich_chat_member_status_update() -> None:
    assert normalize_chat_member(object()) is None


def test_rubika_capabilities_regression() -> None:
    assert RUBIKA_CAPABILITIES.supports_topics is False
    assert RUBIKA_CAPABILITIES.supports_scheduled_messages is False
    assert RUBIKA_CAPABILITIES.update_delivery == "both"
    assert RUBIKA_CAPABILITIES.supported_parse_modes == []
    assert RUBIKA_CAPABILITIES.callback_data_max_bytes is None
    assert RUBIKA_CAPABILITIES.supports_payments is False
    assert RUBIKA_CAPABILITIES.supports_admin_detection is False
    assert RUBIKA_CAPABILITIES.supports_chat_member_status_updates is False


def test_rubika_event_data_dispatches_bot_membership() -> None:
    raw = Update(type=UpdateTypeEnum.EVENT_DATA, chat_id="c1", event_data=Event(type=EventTypeEnum.BOT_JOINED))
    normalized = normalize_update(raw)
    assert isinstance(normalized, IncomingBotMembershipChange)
    assert normalized.added is True
    assert normalized.raw is raw.event_data


def test_rubika_permissions_change_stays_raw() -> None:
    raw = Update(type=UpdateTypeEnum.EVENT_DATA, chat_id="c1", event_data=Event(type="BotPermissionsChanged"))
    assert normalize_update(raw) is raw
