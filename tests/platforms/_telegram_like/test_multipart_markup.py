"""Structured form fields (e.g. a rendered inline keyboard) must be sent as JSON.

Uploading bytes switches a media request to multipart. ``reply_markup`` used to be
``str()``-ed there, i.e. the Python ``repr`` of the dataclass was sent, which the
platform cannot parse, so the keyboard silently disappeared.
"""
import json

from peyk.platforms._telegram_like.base_client import TelegramLikeClient
from peyk.platforms.bale.types import InlineKeyboardButton, InlineKeyboardMarkup


def _markup():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="a", url="https://example.com/a")],
            [InlineKeyboardButton(text="b", url="https://example.com/b")],
        ]
    )


def test_upload_serializes_dataclass_reply_markup_as_json():
    kwargs = TelegramLikeClient._build_media_request_kwargs(
        "animation",
        b"GIF89a",
        json_fields={"chat_id": -100, "caption": "hi", "reply_markup": _markup()},
        default_filename="animation.gif",
    )
    fields = kwargs["data"]
    assert fields["chat_id"] == "-100"
    assert fields["caption"] == "hi"
    rows = json.loads(fields["reply_markup"])["inline_keyboard"]
    assert [[b["text"] for b in row] for row in rows] == [["a"], ["b"]]


def test_form_field_value_keeps_plain_values_unchanged():
    f = TelegramLikeClient._form_field_value
    assert f("text") == "text"
    assert f(5) == "5"
    assert json.loads(f({"k": [1, 2]})) == {"k": [1, 2]}
    assert json.loads(f((1, 2))) == [1, 2]
