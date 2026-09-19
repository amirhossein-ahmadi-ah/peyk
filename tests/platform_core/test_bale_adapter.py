from peyk.platform_core.adapters.bale import BALE_CAPABILITIES, normalize_callback, normalize_message, normalize_pre_checkout_query, normalize_update
from peyk.platform_core.contracts import IncomingCallbackQuery, IncomingMessage, IncomingPreCheckoutQuery
from peyk.platforms.bale.models import CallbackQuery, Chat, Message, PreCheckoutQuery, Update, User


def test_message_normalization_and_raw_identity() -> None:
    sender = User(id=7, is_bot=False, first_name="Ali")
    chat = Chat(id=100, type="group", title="G")
    raw = Message(
        message_id=55, from_=sender, date=123, chat=chat, text="hello",
        reply_to_message=Message(message_id=54, chat=chat, text="old"),
        new_chat_members=[User(id=8, is_bot=False, first_name="N")],
        successful_payment=None,
    )
    normalized = normalize_message(raw)
    assert isinstance(normalized, IncomingMessage)
    assert normalized.chat_id == 100
    assert normalized.sender_id == 7
    assert normalized.text == "hello"
    assert normalized.reply_to_message_id == 54
    assert normalized.new_chat_members == [8]
    assert normalized.successful_payment is None
    assert normalized.raw is raw


def test_callback_data_maps_to_common_data_field() -> None:
    raw_message = Message(message_id=55, chat=Chat(id=100, type="group"), text="x")
    raw = CallbackQuery(id="cb1", from_=User(id=7, is_bot=False, first_name="A"), message=raw_message, data="menu:1")
    normalized = normalize_callback(raw)
    assert isinstance(normalized, IncomingCallbackQuery)
    assert normalized.data == "menu:1"
    assert normalized.id == "cb1"
    assert normalized.chat_id == 100
    assert normalized.raw is raw


def test_bale_pre_checkout_is_normalized() -> None:
    raw = PreCheckoutQuery(id="pc1", from_=User(id=7, is_bot=False, first_name="A"), currency="IRR", total_amount=1200, invoice_payload="p")
    normalized = normalize_pre_checkout_query(raw)
    assert isinstance(normalized, IncomingPreCheckoutQuery)
    assert normalized.id == "pc1"
    assert normalized.from_user_id == 7
    assert normalized.currency == "IRR"
    assert normalized.total_amount == 1200
    assert normalized.invoice_payload == "p"
    assert normalized.raw is raw


def test_bale_has_no_rich_chat_member_status_update() -> None:
    # Bale has ChatMember response models, but no confirmed incoming update
    # kind carrying old/new membership transitions.
    from peyk.platform_core.adapters.bale import normalize_chat_member
    assert normalize_chat_member(object()) is None


def test_bale_capabilities_regression() -> None:
    assert BALE_CAPABILITIES.supports_topics is False
    assert BALE_CAPABILITIES.supports_scheduled_messages is False
    assert BALE_CAPABILITIES.update_delivery == "both"
    assert BALE_CAPABILITIES.callback_data_max_bytes == 64
    assert BALE_CAPABILITIES.supports_payments is True
    assert BALE_CAPABILITIES.supports_admin_detection is True
    assert BALE_CAPABILITIES.supports_chat_member_status_updates is False


def test_bale_update_dispatches_pre_checkout() -> None:
    raw = Update(update_id=1, pre_checkout_query=PreCheckoutQuery(id="pc", currency="IRR", total_amount=1, invoice_payload="x"))
    normalized = normalize_update(raw)
    assert isinstance(normalized, IncomingPreCheckoutQuery)
    assert normalized.raw is raw.pre_checkout_query
