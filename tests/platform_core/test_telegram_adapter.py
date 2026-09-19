from peyk.platform_core.adapters.telegram import TELEGRAM_CAPABILITIES, normalize_callback, normalize_chat_member, normalize_message, normalize_pre_checkout_query, normalize_shipping_query, normalize_update
from peyk.platform_core.contracts import IncomingCallbackQuery, IncomingChatMemberStatusUpdate, IncomingMessage, IncomingPreCheckoutQuery, IncomingShippingQuery
from peyk.platforms.telegram.models import Chat, ChatMemberMember, ChatMemberOwner, ChatMemberUpdated, CallbackQuery, Message, PreCheckoutQuery, ShippingQuery, Update, User


def _user(uid: int) -> User:
    return User(id=uid, is_bot=False, first_name="User")


def test_message_normalization_and_raw_identity() -> None:
    raw = Message(message_id=10, date=100, chat=Chat(id=20, type="group"), from_=_user(30), text="hello", new_chat_members=[_user(40)])
    normalized = normalize_message(raw)
    assert isinstance(normalized, IncomingMessage)
    assert normalized.message_id == 10
    assert normalized.chat_id == 20
    assert normalized.sender_id == 30
    assert normalized.new_chat_members == [40]
    assert normalized.left_chat_member is None
    assert normalized.successful_payment is None
    assert normalized.raw is raw


def test_optional_fields_stay_none_when_not_populatable_in_payload() -> None:
    raw = Message(message_id=10, date=100, chat=Chat(id=20, type="group"), text="hello")
    normalized = normalize_message(raw)
    assert normalized.sender_id is None
    assert normalized.reply_to_message_id is None
    assert normalized.media is None
    assert normalized.new_chat_members is None
    assert normalized.left_chat_member is None
    assert normalized.successful_payment is None


def test_callback_data_maps_to_common_data_field() -> None:
    raw = CallbackQuery(id="cb", from_=_user(30), message=Message(message_id=10, date=1, chat=Chat(id=20, type="private")), data="approve")
    normalized = normalize_callback(raw)
    assert isinstance(normalized, IncomingCallbackQuery)
    assert normalized.data == "approve"
    assert normalized.id == "cb"
    assert normalized.chat_id == 20
    assert normalized.message_id == 10
    assert normalized.raw is raw


def test_chat_member_status_normalization() -> None:
    raw = ChatMemberUpdated(
        chat=Chat(id=20, type="group"), from_=_user(30), date=99,
        old_chat_member=ChatMemberMember(status="member", user=_user(40)),
        new_chat_member=ChatMemberOwner(status="creator", user=_user(40)),
    )
    normalized = normalize_chat_member(raw)
    assert isinstance(normalized, IncomingChatMemberStatusUpdate)
    assert normalized.chat_id == 20
    assert normalized.actor_id == 30
    assert normalized.target_user_id == 40
    assert normalized.old_status == "member"
    assert normalized.new_status == "creator"
    assert normalized.raw is raw


def test_pre_checkout_and_shipping_queries() -> None:
    pre = PreCheckoutQuery(id="pc", from_=_user(30), currency="USD", total_amount=500, invoice_payload="p")
    shipping = ShippingQuery(id="sq", from_=_user(30), invoice_payload="p", shipping_address={"country_code": "AZ"})
    p = normalize_pre_checkout_query(pre)
    s = normalize_shipping_query(shipping)
    assert isinstance(p, IncomingPreCheckoutQuery)
    assert p.from_user_id == 30 and p.total_amount == 500 and p.raw is pre
    assert isinstance(s, IncomingShippingQuery)
    assert s.from_user_id == 30 and s.shipping_address == {"country_code": "AZ"} and s.raw is shipping


def test_telegram_capabilities_regression() -> None:
    assert TELEGRAM_CAPABILITIES.supports_topics is True
    assert TELEGRAM_CAPABILITIES.supports_scheduled_messages is False
    assert TELEGRAM_CAPABILITIES.update_delivery == "both"
    assert TELEGRAM_CAPABILITIES.supported_parse_modes == ["Markdown", "MarkdownV2", "HTML"]
    assert TELEGRAM_CAPABILITIES.callback_data_max_bytes == 64
    assert TELEGRAM_CAPABILITIES.supports_payments is True
    assert TELEGRAM_CAPABILITIES.supports_admin_detection is True
    assert TELEGRAM_CAPABILITIES.supports_chat_member_status_updates is True


def test_update_dispatches_message_callback_and_member() -> None:
    msg = Message(message_id=1, date=1, chat=Chat(id=2, type="private"), text="x")
    assert isinstance(normalize_update(Update(update_id=1, message=msg)), IncomingMessage)
    cb = CallbackQuery(id="c", data="x")
    assert isinstance(normalize_update(Update(update_id=2, callback_query=cb)), IncomingCallbackQuery)
    cm = ChatMemberUpdated(chat=Chat(id=2, type="group"), new_chat_member=ChatMemberMember(status="member", user=_user(3)))
    assert isinstance(normalize_update(Update(update_id=3, my_chat_member=cm)), IncomingChatMemberStatusUpdate)


def test_telegram_platform_unique_update_uses_raw_escape_hatch() -> None:
    raw = Update(update_id=99, poll={"id": "poll-1"})
    assert normalize_update(raw) is raw
