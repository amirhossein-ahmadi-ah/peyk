"""Model parsing tests for Rubika, validated against the official docs."""

from __future__ import annotations

from peyk.platforms.rubika.models import (
    AuxData,
    Bot,
    BotCommand,
    Button,
    ButtonCalendar,
    ButtonCalendarTypeEnum,
    ButtonSelection,
    ButtonStringPicker,
    ButtonTextbox,
    Chat,
    ContactMessage,
    File,
    GetUpdatesResult,
    InlineMessage,
    Keypad,
    KeypadRow,
    Location,
    Message,
    Metadata,
    MetadataPart,
    MetadataTypeEnum,
    Poll,
    PollStatus,
    Sticker,
    Update,
)


# -- Leaf types --------------------------------------------------------------


def test_file_from_dict() -> None:
    f = File.from_dict({"file_id": "f1", "file_name": "a.pdf", "size": "1024"})
    assert f == File(file_id="f1", file_name="a.pdf", size="1024")


def test_file_from_dict_none() -> None:
    assert File.from_dict(None) is None


def test_location_from_dict_string_coords() -> None:
    loc = Location.from_dict({"latitude": "35.7", "longitude": "51.4"})
    assert loc is not None
    assert loc.latitude == "35.7"
    assert loc.longitude == "51.4"


# -- Chat / Bot --------------------------------------------------------------


def test_chat_from_dict_bare() -> None:
    chat = Chat.from_dict(
        {"chat_id": "c1", "chat_type": "Group", "title": "Team"}
    )
    assert chat is not None
    assert chat.chat_id == "c1"
    assert chat.chat_type == "Group"
    assert chat.title == "Team"


def test_chat_from_dict_wrapped_in_chat_key() -> None:
    """The API wraps getChat's response in {"chat": {...}}."""
    chat = Chat.from_dict(
        {"chat": {"chat_id": "c2", "chat_type": "User", "first_name": "Ali"}}
    )
    assert chat is not None
    assert chat.chat_id == "c2"
    assert chat.first_name == "Ali"


def test_bot_from_dict_wrapped() -> None:
    bot = Bot.from_dict(
        {"bot": {"bot_id": "b1", "bot_title": "MyBot", "username": "my_bot"}}
    )
    assert bot is not None
    assert bot.bot_id == "b1"
    assert bot.bot_title == "MyBot"
    assert bot.username == "my_bot"


def test_bot_avatar_parsing() -> None:
    bot = Bot.from_dict(
        {
            "bot": {
                "bot_id": "b1",
                "bot_title": "X",
                "avatar": {"file_id": "av1", "file_name": "a.jpg"},
            }
        }
    )
    assert bot is not None
    assert bot.avatar is not None
    assert bot.avatar.file_id == "av1"


# -- BotCommand ---------------------------------------------------------------


def test_bot_command_roundtrip() -> None:
    cmd = BotCommand(command="start", description="Start")
    assert cmd.to_dict() == {"command": "start", "description": "Start"}


# -- AuxData ------------------------------------------------------------------


def test_aux_data_with_button_id() -> None:
    aux = AuxData.from_dict({"start_id": None, "button_id": "100"})
    assert aux is not None
    assert aux.button_id == "100"
    assert aux.start_id is None


def test_aux_data_with_start_id() -> None:
    aux = AuxData.from_dict({"start_id": "s1", "button_id": None})
    assert aux is not None
    assert aux.start_id == "s1"


# -- Metadata -----------------------------------------------------------------


def test_metadata_part_bold_roundtrip() -> None:
    part = MetadataPart(type=MetadataTypeEnum.BOLD, from_index=0, length=16)
    assert part.to_dict() == {"type": "Bold", "from_index": 0, "length": 16}


def test_metadata_part_link_includes_url() -> None:
    part = MetadataPart(
        type=MetadataTypeEnum.LINK, from_index=0, length=5, link_url="https://x.com"
    )
    d = part.to_dict()
    assert d["link_url"] == "https://x.com"


def test_metadata_part_mention_includes_user_id() -> None:
    part = MetadataPart(
        type=MetadataTypeEnum.MENTION_TEXT,
        from_index=5,
        length=11,
        mention_text_user_id="u1",
    )
    d = part.to_dict()
    assert d["mention_text_user_id"] == "u1"


def test_metadata_roundtrip() -> None:
    md = Metadata(
        meta_data_parts=[
            MetadataPart(type="Bold", from_index=0, length=4),
            MetadataPart(type="Italic", from_index=5, length=3),
        ]
    )
    d = md.to_dict()
    assert len(d["meta_data_parts"]) == 2


# -- Buttons ------------------------------------------------------------------


def test_simple_button_to_dict() -> None:
    btn = Button(id="b1", type="Simple", button_text="OK")
    assert btn.to_dict() == {
        "id": "b1",
        "type": "Simple",
        "button_text": "OK",
    }


def test_calendar_button_to_dict() -> None:
    btn = Button(
        id="c1",
        type="Calendar",
        button_text="Pick",
        button_calendar=ButtonCalendar(
            type=ButtonCalendarTypeEnum.DATE_PERSIAN,
            min_year="1300",
            max_year="1450",
            title="Select date",
        ),
    )
    d = btn.to_dict()
    assert d["type"] == "Calendar"
    assert d["button_calendar"]["type"] == "DatePersian"
    assert d["button_calendar"]["min_year"] == "1300"


def test_string_picker_button_to_dict() -> None:
    btn = Button(
        id="sp1",
        type="StringPicker",
        button_text="Pick",
        button_string_picker=ButtonStringPicker(items=["A", "B", "C"]),
    )
    d = btn.to_dict()
    assert d["button_string_picker"]["items"] == ["A", "B", "C"]


def test_textbox_button_to_dict() -> None:
    btn = Button(
        id="tb1",
        type="Textbox",
        button_text="Enter",
        button_textbox=ButtonTextbox(
            type_line="SingleLine",
            type_keypad="Number",
            place_holder="0",
        ),
    )
    d = btn.to_dict()
    assert d["button_textbox"]["type_line"] == "SingleLine"
    assert d["button_textbox"]["type_keypad"] == "Number"


def test_selection_button_roundtrip() -> None:
    btn = Button(
        id="sel1",
        type="Selection",
        button_text="Choose",
        button_selection=ButtonSelection(
            selection_id="s1",
            search_type="Local",
            get_type="Local",
            items=[],
            is_multi_selection=True,
            columns_count="2",
            title="Pick",
        ),
    )
    d = btn.to_dict()
    assert d["button_selection"]["selection_id"] == "s1"
    assert d["button_selection"]["is_multi_selection"] is True


def test_button_from_dict_dispatch_by_nested_key() -> None:
    raw = {
        "id": "c1",
        "type": "Calendar",
        "button_text": "Pick",
        "button_calendar": {
            "type": "DateGregorian",
            "min_year": "2000",
            "max_year": "2100",
            "title": "Date",
        },
    }
    btn = Button.from_dict(raw)
    assert btn is not None
    assert btn.type == "Calendar"
    assert btn.button_calendar is not None
    assert btn.button_calendar.type == "DateGregorian"


# -- Keypad -------------------------------------------------------------------


def test_keypad_roundtrip() -> None:
    kp = Keypad(
        rows=[
            KeypadRow(buttons=[Button(id="b1", type="Simple", button_text="A")]),
            KeypadRow(buttons=[
                Button(id="b2", type="Simple", button_text="B"),
                Button(id="b3", type="Simple", button_text="C"),
            ]),
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )
    d = kp.to_dict()
    assert len(d["rows"]) == 2
    assert d["resize_keyboard"] is True
    assert d["one_time_keyboard"] is False
    # Round-trip
    kp2 = Keypad.from_dict(d)
    assert kp2 is not None
    assert len(kp2.rows) == 2


# -- Message / Update / InlineMessage ----------------------------------------


def test_message_full_parsing() -> None:
    raw = {
        "message_id": "m1",
        "text": "hello",
        "time": "1643122902",
        "is_edited": False,
        "sender_type": "User",
        "sender_id": "u1",
        "aux_data": {"start_id": None, "button_id": "b1"},
        "reply_to_message_id": "m0",
    }
    msg = Message.from_dict(raw)
    assert msg is not None
    assert msg.message_id == "m1"
    assert msg.text == "hello"
    assert msg.time == 1643122902
    assert msg.sender_type == "User"
    assert msg.aux_data is not None and msg.aux_data.button_id == "b1"


def test_message_with_sticker() -> None:
    msg = Message.from_dict(
        {
            "message_id": "m2",
            "sticker": {
                "sticker_id": "s1",
                "file": {"file_id": "f1"},
                "emoji_character": "😀",
            },
        }
    )
    assert msg is not None
    assert isinstance(msg.sticker, Sticker)
    assert msg.sticker.emoji_character == "😀"


def test_message_with_poll() -> None:
    msg = Message.from_dict(
        {
            "message_id": "m3",
            "poll": {
                "question": "Yes?",
                "options": ["yes", "no"],
                "poll_status": {"state": "Open", "total_vote": 10},
            },
        }
    )
    assert msg is not None
    assert isinstance(msg.poll, Poll)
    assert msg.poll.question == "Yes?"
    assert msg.poll.poll_status is not None
    assert msg.poll.poll_status.total_vote == 10


def test_message_with_contact() -> None:
    msg = Message.from_dict(
        {
            "message_id": "m4",
            "contact_message": {
                "phone_number": "+98912",
                "first_name": "Ali",
                "last_name": "R",
            },
        }
    )
    assert msg is not None
    assert isinstance(msg.contact_message, ContactMessage)
    assert msg.contact_message.first_name == "Ali"


def test_update_parsing_new_message() -> None:
    raw = {
        "update": {
            "type": "NewMessage",
            "chat_id": "c1",
            "new_message": {"message_id": "m1", "text": "hi"},
        }
    }
    upd = Update.from_dict(raw)
    assert upd is not None
    assert upd.type == "NewMessage"
    assert upd.chat_id == "c1"
    assert upd.new_message is not None and upd.new_message.text == "hi"


def test_update_parsing_removed_message() -> None:
    upd = Update.from_dict(
        {
            "update": {
                "type": "RemovedMessage",
                "chat_id": "c1",
                "removed_message_id": "m5",
            }
        }
    )
    assert upd is not None
    assert upd.type == "RemovedMessage"
    assert upd.removed_message_id == "m5"


def test_update_with_event_data() -> None:
    upd = Update.from_dict(
        {
            "update": {
                "type": "EventData",
                "chat_id": "c1",
                "event_data": {
                    "type": "BotJoined",
                    "access_list": ["SendMessages"],
                    "join_type": "Admin",
                },
            }
        }
    )
    assert upd is not None
    assert upd.event_data is not None
    assert upd.event_data.type == "BotJoined"
    assert upd.event_data.join_type == "Admin"


def test_inline_message_parsing() -> None:
    raw = {
        "inline_message": {
            "sender_id": "u1",
            "text": "custom",
            "location": None,
            "aux_data": {"start_id": None, "button_id": "b1"},
            "message_id": "m1",
            "chat_id": "c1",
        }
    }
    im = InlineMessage.from_dict(raw)
    assert im is not None
    assert im.sender_id == "u1"
    assert im.chat_id == "c1"
    assert im.aux_data is not None and im.aux_data.button_id == "b1"


# -- GetUpdatesResult --------------------------------------------------------


def test_get_updates_result_from_dict() -> None:
    result = GetUpdatesResult.from_data(
        {
            "updates": [
                {"type": "NewMessage", "chat_id": "c1", "new_message": {"message_id": "m1"}},
            ],
            "next_offset_id": "42",
        }
    )
    assert len(result.updates) == 1
    assert result.next_offset_id == "42"


def test_get_updates_result_from_bare_list() -> None:
    """Some implementations return a bare list; handle both."""
    result = GetUpdatesResult.from_data(
        [{"type": "NewMessage", "chat_id": "c1", "new_message": {"message_id": "m1"}}]
    )
    assert len(result.updates) == 1
    assert result.next_offset_id is None


def test_get_updates_result_none() -> None:
    assert GetUpdatesResult.from_data(None).updates == []


# -- PollStatus ---------------------------------------------------------------


def test_poll_status_defaults() -> None:
    ps = PollStatus.from_dict({})
    assert ps is not None
    assert ps.selection_index == -1


def test_poll_status_full() -> None:
    ps = PollStatus.from_dict(
        {
            "state": "Closed",
            "selection_index": 2,
            "percent_vote_options": [30, 70],
            "total_vote": 100,
            "show_total_votes": True,
        }
    )
    assert ps is not None
    assert ps.state == "Closed"
    assert ps.percent_vote_options == [30, 70]
    assert ps.total_vote == 100