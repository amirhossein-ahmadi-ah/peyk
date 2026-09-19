from __future__ import annotations

from peyk.platforms.bale.models import (
    Animation,
    Audio,
    CallbackQuery,
    Chat,
    ChatMember,
    ChatMemberAdministrator,
    ChatMemberMember,
    ChatMemberOwner,
    ChatMemberRestricted,
    ChatPhoto,
    Contact,
    CopyTextButton,
    Document,
    File,
    Invoice,
    LabeledPrice,
    Location,
    Message,
    MessageEntity,
    MessageId,
    PhotoSize,
    PreCheckoutQuery,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ResponseParameters,
    Sticker,
    StickerSet,
    SuccessfulPayment,
    Transaction,
    Update,
    User,
    Video,
    Voice,
    WebAppData,
    WebAppInfo,
    WebhookInfo,
)


def test_user_from_dict_parses_real_field_names() -> None:
    raw = {
        "id": 111,
        "is_bot": False,
        "first_name": "Sara",
        "last_name": "Ahmadi",
        "username": "sara_a",
        "language_code": "fa",
    }
    user = User.from_dict(raw)
    assert user == User(
        id=111,
        is_bot=False,
        first_name="Sara",
        last_name="Ahmadi",
        username="sara_a",
        language_code="fa",
    )


def test_user_from_dict_defaults_optional_fields() -> None:
    user = User.from_dict({"id": 1, "first_name": "Bot"})
    assert user.is_bot is False
    assert user.last_name is None
    assert user.username is None
    assert user.language_code is None


def test_user_from_dict_none_is_none() -> None:
    assert User.from_dict(None) is None


def test_chat_from_dict_parses_real_field_names() -> None:
    raw = {
        "id": 555,
        "type": "group",
        "title": "Test Group",
        "username": None,
        "first_name": None,
        "last_name": None,
        "photo": {
            "small_file_id": "abc",
            "small_file_unique_id": "abc_u",
            "big_file_id": "def",
            "big_file_unique_id": "def_u",
        },
    }
    chat = Chat.from_dict(raw)
    assert chat == Chat(
        id=555,
        type="group",
        title="Test Group",
        username=None,
        first_name=None,
        last_name=None,
        photo=ChatPhoto(
            small_file_id="abc",
            small_file_unique_id="abc_u",
            big_file_id="def",
            big_file_unique_id="def_u",
        ),
    )


def test_chat_from_dict_with_no_photo() -> None:
    chat = Chat.from_dict({"id": 1, "type": "private"})
    assert chat.photo is None


def test_chat_from_dict_parses_chat_full_info_fields() -> None:
    """ChatFullInfo fields (bio, description, invite_link, linked_chat_id)
    are now part of the Chat model since getChat returns them."""
    raw = {
        "id": 555,
        "type": "private",
        "bio": "About me",
        "invite_link": "https://bale.ai/join/abc",
        "linked_chat_id": "123456",
    }
    chat = Chat.from_dict(raw)
    assert chat.bio == "About me"
    assert chat.invite_link == "https://bale.ai/join/abc"
    assert chat.linked_chat_id == "123456"


def test_message_from_dict_maps_from_to_from_underscore() -> None:
    """The raw Bale field is `from`; the model exposes it as `from_`."""
    raw = {
        "message_id": 42,
        "from": {"id": 7, "is_bot": False, "first_name": "Ali"},
        "date": 1690000000,
        "chat": {"id": 8, "type": "private"},
        "text": "hi",
    }
    message = Message.from_dict(raw)
    assert message.message_id == 42
    assert message.from_ == User(id=7, is_bot=False, first_name="Ali")
    assert message.chat == Chat(id=8, type="private")
    assert message.text == "hi"
    assert message.reply_to_message is None
    assert "from_" in Message.__dataclass_fields__
    assert "from" not in Message.__dataclass_fields__


def test_message_from_dict_parses_nested_reply_to_message() -> None:
    raw = {
        "message_id": 2,
        "from": {"id": 1, "is_bot": False, "first_name": "A"},
        "chat": {"id": 1, "type": "private"},
        "reply_to_message": {
            "message_id": 1,
            "from": {"id": 1, "is_bot": False, "first_name": "A"},
            "chat": {"id": 1, "type": "private"},
            "text": "original",
        },
    }
    message = Message.from_dict(raw)
    assert message.reply_to_message.message_id == 1
    assert message.reply_to_message.text == "original"


def test_message_from_dict_parses_new_message_fields() -> None:
    """Message now parses sender_chat, media_group_id, entities,
    caption_entities, and web_app_data."""
    raw = {
        "message_id": 42,
        "chat": {"id": 1, "type": "group"},
        "text": "hello",
        "sender_chat": {"id": 2, "type": "channel", "title": "Admin"},
        "media_group_id": "album_123",
        "entities": [{"type": "bot_command", "offset": 0, "length": 6}],
        "caption_entities": [{"type": "mention", "offset": 0, "length": 5}],
        "web_app_data": {"data": "from_mini_app"},
    }
    message = Message.from_dict(raw)
    assert message.sender_chat == Chat(id=2, type="channel", title="Admin")
    assert message.media_group_id == "album_123"
    assert message.entities == [MessageEntity(type="bot_command", offset=0, length=6)]
    assert message.caption_entities == [
        MessageEntity(type="mention", offset=0, length=5)
    ]
    assert message.web_app_data == WebAppData(data="from_mini_app")


def test_callback_query_from_dict_maps_from_to_from_underscore() -> None:
    raw = {
        "id": "cbq1",
        "from": {"id": 9, "is_bot": False, "first_name": "B"},
        "message": {
            "message_id": 3,
            "from": {"id": 9, "is_bot": False, "first_name": "B"},
            "chat": {"id": 9, "type": "private"},
        },
        "data": "action:confirm",
    }
    callback_query = CallbackQuery.from_dict(raw)
    assert callback_query.id == "cbq1"
    assert callback_query.from_ == User(id=9, is_bot=False, first_name="B")
    assert callback_query.data == "action:confirm"
    assert callback_query.message.message_id == 3


def test_update_from_dict_parses_message_update() -> None:
    raw = {
        "update_id": 100,
        "message": {
            "message_id": 5,
            "from": {"id": 1, "is_bot": False, "first_name": "A"},
            "chat": {"id": 1, "type": "private"},
            "text": "/start",
        },
    }
    update = Update.from_dict(raw)
    assert update.update_id == 100
    assert update.message.text == "/start"
    assert update.edited_message is None
    assert update.callback_query is None
    assert update.pre_checkout_query is None


def test_update_from_dict_parses_callback_query_update() -> None:
    raw = {
        "update_id": 101,
        "callback_query": {
            "id": "cbq2",
            "from": {"id": 2, "is_bot": False, "first_name": "C"},
            "message": {
                "message_id": 6,
                "from": {"id": 2, "is_bot": False, "first_name": "C"},
                "chat": {"id": 2, "type": "private"},
            },
            "data": "x",
        },
    }
    update = Update.from_dict(raw)
    assert update.message is None
    assert update.callback_query.id == "cbq2"
    assert update.callback_query.data == "x"


def test_update_from_dict_parses_pre_checkout_query_update() -> None:
    """PreCheckoutQuery is now a documented update variant."""
    raw = {
        "update_id": 102,
        "pre_checkout_query": {
            "id": "pcq_1",
            "from": {"id": 3, "is_bot": False, "first_name": "D"},
            "currency": "IRR",
            "total_amount": 50000,
            "invoice_payload": "payload_123",
        },
    }
    update = Update.from_dict(raw)
    assert update.message is None
    assert update.callback_query is None
    assert update.pre_checkout_query is not None
    assert update.pre_checkout_query.id == "pcq_1"
    assert update.pre_checkout_query.total_amount == 50000
    assert update.pre_checkout_query.invoice_payload == "payload_123"
    assert update.pre_checkout_query.from_ == User(
        id=3, is_bot=False, first_name="D"
    )


def test_update_list_from_result_parses_array_and_handles_none() -> None:
    assert Update.list_from_result(None) == []
    raw_list = [{"update_id": 1}, {"update_id": 2}]
    updates = Update.list_from_result(raw_list)
    assert [u.update_id for u in updates] == [1, 2]


# -- Newly added response types (full docs.bale.ai type coverage) ------------------


def test_photo_size_from_dict() -> None:
    raw = {"file_id": "f1", "file_unique_id": "u1", "width": 90, "height": 90}
    assert PhotoSize.from_dict(raw) == PhotoSize(
        file_id="f1", file_unique_id="u1", width=90, height=90
    )


def test_message_from_dict_parses_media_and_extra_fields() -> None:
    raw = {
        "message_id": 10,
        "from": {"id": 1, "is_bot": False, "first_name": "A"},
        "chat": {"id": 1, "type": "group"},
        "forward_from": {"id": 2, "is_bot": False, "first_name": "B"},
        "forward_from_message_id": 3,
        "forward_date": 1690000000,
        "edit_date": 1690000500,
        "animation": {
            "file_id": "anim1",
            "file_unique_id": "animu1",
            "width": 100,
            "height": 100,
            "duration": 5,
        },
        "audio": {"file_id": "aud1", "file_unique_id": "audu1", "duration": 120},
        "document": {"file_id": "doc1", "file_unique_id": "docu1", "file_name": "a.pdf"},
        "photo": [
            {"file_id": "p1", "file_unique_id": "pu1", "width": 90, "height": 90}
        ],
        "sticker": {
            "file_id": "st1",
            "file_unique_id": "stu1",
            "type": "regular",
            "width": 512,
            "height": 512,
        },
        "video": {"file_id": "v1", "file_unique_id": "vu1", "width": 640, "height": 480, "duration": 30},
        "voice": {"file_id": "vo1", "file_unique_id": "vou1"},
        "contact": {"phone_number": "+98912", "first_name": "Sara"},
        "location": {"longitude": 51.4, "latitude": 35.7},
        "new_chat_members": [{"id": 5, "is_bot": False, "first_name": "New"}],
        "left_chat_member": {"id": 6, "is_bot": False, "first_name": "Left"},
        "invoice": {"title": "T", "description": "D", "total_amount": 1000},
        "successful_payment": {
            "currency": "IRR",
            "total_amount": 50000,
            "invoice_payload": "p",
            "telegram_payment_charge_id": "tpc_1",
            "provider_payment_charge_id": "ppc_1",
        },
    }
    message = Message.from_dict(raw)

    assert message.forward_from == User(id=2, is_bot=False, first_name="B")
    assert message.forward_from_message_id == 3
    assert message.forward_date == 1690000000
    assert message.edit_date == 1690000500
    assert message.animation == Animation(
        file_id="anim1", file_unique_id="animu1", width=100, height=100, duration=5
    )
    assert message.audio == Audio(file_id="aud1", file_unique_id="audu1", duration=120)
    assert message.document == Document(
        file_id="doc1", file_unique_id="docu1", file_name="a.pdf"
    )
    assert message.photo == [
        PhotoSize(file_id="p1", file_unique_id="pu1", width=90, height=90)
    ]
    assert message.sticker == Sticker(
        file_id="st1", file_unique_id="stu1", type="regular", width=512, height=512
    )
    assert message.video == Video(
        file_id="v1", file_unique_id="vu1", width=640, height=480, duration=30
    )
    assert message.voice == Voice(file_id="vo1", file_unique_id="vou1")
    assert message.contact == Contact(phone_number="+98912", first_name="Sara")
    assert message.location == Location(longitude=51.4, latitude=35.7)
    assert message.new_chat_members == [User(id=5, is_bot=False, first_name="New")]
    assert message.left_chat_member == User(id=6, is_bot=False, first_name="Left")
    assert message.invoice == Invoice(title="T", description="D", total_amount=1000)
    assert message.successful_payment == SuccessfulPayment(
        currency="IRR",
        total_amount=50000,
        invoice_payload="p",
        telegram_payment_charge_id="tpc_1",
        provider_payment_charge_id="ppc_1",
    )


def test_message_list_from_result_for_media_group() -> None:
    raw_list = [
        {"message_id": 1, "chat": {"id": 1, "type": "private"}},
        {"message_id": 2, "chat": {"id": 1, "type": "private"}},
    ]
    messages = Message.list_from_result(raw_list)
    assert [m.message_id for m in messages] == [1, 2]
    assert Message.list_from_result(None) == []


def test_file_from_dict() -> None:
    raw = {"file_id": "f1", "file_unique_id": "u1", "file_size": 2048, "file_path": "docs/x.pdf"}
    assert File.from_dict(raw) == File(
        file_id="f1", file_unique_id="u1", file_size=2048, file_path="docs/x.pdf"
    )


def test_webhook_info_from_dict() -> None:
    """Per docs.bale.ai, WebhookInfo only has `url`."""
    raw = {"url": "https://example.com/webhook"}
    info = WebhookInfo.from_dict(raw)
    assert info == WebhookInfo(url="https://example.com/webhook")


def test_webhook_info_from_dict_empty_url() -> None:
    """When using getUpdates, the url field is empty."""
    raw = {"url": ""}
    info = WebhookInfo.from_dict(raw)
    assert info == WebhookInfo(url="")


def test_sticker_set_from_dict() -> None:
    raw = {
        "name": "pack",
        "title": "Pack",
        "stickers": [
            {
                "file_id": "st1",
                "file_unique_id": "stu1",
                "type": "regular",
                "width": 512,
                "height": 512,
            }
        ],
    }
    sticker_set = StickerSet.from_dict(raw)
    assert sticker_set.name == "pack"
    assert len(sticker_set.stickers) == 1
    assert sticker_set.stickers[0].file_id == "st1"


def test_message_id_from_dict() -> None:
    raw = {"message_id": 42}
    message_id = MessageId.from_dict(raw)
    assert message_id == MessageId(message_id=42)


def test_message_entity_from_dict() -> None:
    raw = {"type": "bot_command", "offset": 0, "length": 6}
    entity = MessageEntity.from_dict(raw)
    assert entity == MessageEntity(type="bot_command", offset=0, length=6)


def test_message_entity_list_from_result() -> None:
    raw = [
        {"type": "bot_command", "offset": 0, "length": 6},
        {"type": "mention", "offset": 7, "length": 4},
    ]
    entities = MessageEntity.list_from_result(raw)
    assert entities == [
        MessageEntity(type="bot_command", offset=0, length=6),
        MessageEntity(type="mention", offset=7, length=4),
    ]
    assert MessageEntity.list_from_result(None) is None


def test_labeled_price_from_dict() -> None:
    raw = {"label": "Product", "amount": 10000}
    price = LabeledPrice.from_dict(raw)
    assert price == LabeledPrice(label="Product", amount=10000)


def test_labeled_price_list_from_result() -> None:
    raw = [{"label": "Item1", "amount": 5000}, {"label": "Item2", "amount": 15000}]
    prices = LabeledPrice.list_from_result(raw)
    assert prices == [
        LabeledPrice(label="Item1", amount=5000),
        LabeledPrice(label="Item2", amount=15000),
    ]


def test_response_parameters_from_dict() -> None:
    raw = {"retry_after": 30}
    params = ResponseParameters.from_dict(raw)
    assert params == ResponseParameters(retry_after=30)


def test_response_parameters_from_dict_none() -> None:
    assert ResponseParameters.from_dict(None) is None


def test_invoice_from_dict() -> None:
    raw = {"title": "Product", "description": "A great product", "total_amount": 10000}
    invoice = Invoice.from_dict(raw)
    assert invoice == Invoice(
        title="Product", description="A great product", total_amount=10000
    )


def test_successful_payment_from_dict() -> None:
    raw = {
        "currency": "IRR",
        "total_amount": 50000,
        "invoice_payload": "internal_payload",
        "telegram_payment_charge_id": "charge_123",
        "provider_payment_charge_id": "prov_456",
    }
    payment = SuccessfulPayment.from_dict(raw)
    assert payment == SuccessfulPayment(
        currency="IRR",
        total_amount=50000,
        invoice_payload="internal_payload",
        telegram_payment_charge_id="charge_123",
        provider_payment_charge_id="prov_456",
    )


def test_pre_checkout_query_from_dict() -> None:
    raw = {
        "id": "pcq_1",
        "from": {"id": 3, "is_bot": False, "first_name": "D"},
        "currency": "IRR",
        "total_amount": 50000,
        "invoice_payload": "payload_123",
    }
    query = PreCheckoutQuery.from_dict(raw)
    assert query == PreCheckoutQuery(
        id="pcq_1",
        from_=User(id=3, is_bot=False, first_name="D"),
        currency="IRR",
        total_amount=50000,
        invoice_payload="payload_123",
    )


def test_transaction_from_dict() -> None:
    raw = {
        "id": "txn_1",
        "status": "paid",
        "userID": 42,
        "amount": 50000,
        "createdAt": 1690000000,
    }
    txn = Transaction.from_dict(raw)
    assert txn == Transaction(
        id="txn_1", status="paid", userID=42, amount=50000, createdAt=1690000000
    )


def test_web_app_data_from_dict() -> None:
    raw = {"data": "some_data"}
    data = WebAppData.from_dict(raw)
    assert data == WebAppData(data="some_data")


def test_web_app_info_from_dict() -> None:
    raw = {"url": "https://example.com/miniapp"}
    info = WebAppInfo.from_dict(raw)
    assert info == WebAppInfo(url="https://example.com/miniapp")


def test_copy_text_button_from_dict() -> None:
    raw = {"text": "https://example.com/link"}
    btn = CopyTextButton.from_dict(raw)
    assert btn == CopyTextButton(text="https://example.com/link")


def test_chat_member_owner_from_dict() -> None:
    raw = {
        "status": "creator",
        "user": {"id": 1, "is_bot": False, "first_name": "Owner"},
    }
    member = ChatMember.from_dict(raw)
    assert isinstance(member, ChatMemberOwner)
    assert member.status == "creator"
    assert member.user == User(id=1, is_bot=False, first_name="Owner")


def test_chat_member_administrator_from_dict() -> None:
    raw = {
        "status": "administrator",
        "user": {"id": 2, "is_bot": False, "first_name": "Admin"},
        "can_delete_messages": True,
        "can_manage_video_chats": True,
        "can_restrict_members": True,
        "can_promote_members": False,
        "can_change_info": True,
        "can_invite_users": True,
        "can_post_stories": True,
        "can_post_messages": True,
        "can_edit_messages": False,
        "can_pin_messages": True,
    }
    member = ChatMember.from_dict(raw)
    assert isinstance(member, ChatMemberAdministrator)
    assert member.can_delete_messages is True
    assert member.can_promote_members is False
    assert member.can_pin_messages is True


def test_chat_member_member_from_dict() -> None:
    raw = {
        "status": "member",
        "user": {"id": 3, "is_bot": False, "first_name": "Member"},
    }
    member = ChatMember.from_dict(raw)
    assert isinstance(member, ChatMemberMember)
    assert member.status == "member"


def test_chat_member_restricted_from_dict() -> None:
    raw = {
        "status": "restricted",
        "user": {"id": 4, "is_bot": False, "first_name": "Restricted"},
        "is_member": True,
        "can_send_messages": False,
        "can_send_audios": False,
        "can_send_documents": False,
        "can_send_photos": False,
        "can_send_videos": False,
        "can_change_info": False,
        "can_invite_users": False,
        "can_pin_messages": False,
    }
    member = ChatMember.from_dict(raw)
    assert isinstance(member, ChatMemberRestricted)
    assert member.can_send_messages is False
    assert member.is_member is True


def test_chat_member_unknown_status_from_dict() -> None:
    """Unknown statuses fall back to base ChatMember."""
    raw = {
        "status": "some_new_status",
        "user": {"id": 5, "is_bot": False, "first_name": "Unknown"},
    }
    member = ChatMember.from_dict(raw)
    assert isinstance(member, ChatMember)
    assert not isinstance(
        member, (ChatMemberOwner, ChatMemberAdministrator, ChatMemberMember, ChatMemberRestricted)
    )
    assert member.status == "some_new_status"


def test_keyboard_button_from_dict() -> None:
    raw = {"text": "Share Contact", "request_contact": True}
    btn = KeyboardButton.from_dict(raw)
    assert btn == KeyboardButton(text="Share Contact", request_contact=True)


def test_keyboard_button_with_web_app() -> None:
    raw = {"text": "Open App", "web_app": {"url": "https://example.com/app"}}
    btn = KeyboardButton.from_dict(raw)
    assert btn == KeyboardButton(
        text="Open App", web_app=WebAppInfo(url="https://example.com/app")
    )


def test_inline_keyboard_button_from_dict() -> None:
    raw = {"text": "Click", "callback_data": "cb1"}
    btn = InlineKeyboardButton.from_dict(raw)
    assert btn == InlineKeyboardButton(text="Click", callback_data="cb1")


def test_inline_keyboard_button_with_copy_text() -> None:
    raw = {"text": "Copy", "copy_text": {"text": "text to copy"}}
    btn = InlineKeyboardButton.from_dict(raw)
    assert btn == InlineKeyboardButton(
        text="Copy", copy_text=CopyTextButton(text="text to copy")
    )


def test_reply_keyboard_markup_from_dict() -> None:
    raw = {"keyboard": [[{"text": "A"}, {"text": "B"}]]}
    markup = ReplyKeyboardMarkup.from_dict(raw)
    assert markup.keyboard[0][0].text == "A"
    assert markup.keyboard[0][1].text == "B"


def test_inline_keyboard_markup_from_dict() -> None:
    raw = {"inline_keyboard": [[{"text": "X", "callback_data": "x"}]]}
    markup = InlineKeyboardMarkup.from_dict(raw)
    assert markup.inline_keyboard[0][0].text == "X"
    assert markup.inline_keyboard[0][0].callback_data == "x"


def test_reply_keyboard_remove_from_dict() -> None:
    raw = {"remove_keyboard": True}
    res = ReplyKeyboardRemove.from_dict(raw)
    assert res == ReplyKeyboardRemove(remove_keyboard=True)
