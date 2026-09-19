from __future__ import annotations
from dataclasses import dataclass, field, replace
from peyk.enums import ButtonStyle
from typing import Sequence
from peyk.filters.callback_data import CallbackData

@dataclass(frozen=True)
class InlineButton:
    """Platform-neutral inline button; platform rendering is deferred."""
    text: str
    callback_data: str | CallbackData | None = None
    url: str | None = None
    web_app_url: str | None = None
    web_app: object | None = None
    copy_text: object | None = None
    login_url: object | None = None
    switch_inline_query: str | None = None
    switch_inline_query_current_chat: str | None = None
    switch_inline_query_chosen_chat: object | None = None
    pay: bool | None = None
    style: ButtonStyle | None = None
    icon_custom_emoji_id: str | None = None
    fallback: 'InlineButton | None' = None

    def packed_callback_data(self) -> str | None:
        """Performs the packed callback data operation for the keyboard client.

Returns:
    Result produced by the keyboard operation."""
        value = self.callback_data
        return value.pack() if isinstance(value, CallbackData) else value

@dataclass(frozen=True)
class ReplyButton:
    """Platform-neutral reply-keyboard button."""
    text: str
    request_contact: bool | None = None
    request_location: bool | None = None
    request_poll: object | None = None
    request_users: object | None = None
    request_chat: object | None = None
    web_app_url: str | None = None
    web_app: object | None = None
    style: ButtonStyle | None = None
    icon_custom_emoji_id: str | None = None
    fallback: 'ReplyButton | None' = None

@dataclass(frozen=True)
class InlineKeyboard:
    """Rows of neutral inline buttons."""
    inline_keyboard: tuple[tuple[InlineButton, ...], ...]

@dataclass(frozen=True)
class ReplyKeyboard:
    """Neutral reply keyboard and its presentation options."""
    keyboard: tuple[tuple[ReplyButton, ...], ...]
    resize_keyboard: bool | None = None
    one_time_keyboard: bool | None = None
    input_field_placeholder: str | None = None
    is_persistent: bool | None = None
    selective: bool | None = None

@dataclass(frozen=True)
class KeyboardRemove:
    """Neutral remove-keyboard instruction."""
    selective: bool | None = None

@dataclass(frozen=True)
class ForceReply:
    """Neutral force-reply instruction."""
    input_field_placeholder: str | None = None
    selective: bool | None = None
