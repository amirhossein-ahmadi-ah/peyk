import pytest

from peyk.dispatcher.filters import (
    CallbackDataEquals, CallbackDataStartsWith, ChatType, Command, TextContains, TextEquals,
)
from peyk.platform_core.contracts import IncomingCallbackQuery, IncomingMessage

def message(text: str | None, chat_type: str | None = "private") -> IncomingMessage:
    return IncomingMessage(text=text, chat_type=chat_type)

@pytest.mark.asyncio
async def test_command_matches_start_and_optional_bot_username() -> None:
    f = Command("start")
    assert await f(message("/start"))
    assert await f(message("/start hello"))
    assert await f(message("/start@my_bot hello"), bot=object()) is False
    assert not await f(message("hello /start"))
    assert not await f(message("/starting"))

@pytest.mark.asyncio
async def test_text_filters_are_normalized_message_only() -> None:
    assert await TextEquals("hello")(message("hello"))
    assert not await TextEquals("hello")(message("Hello"))
    assert await TextEquals("hello", case_sensitive=False)(message("Hello"))
    assert await TextContains("ell")(message("hello"))
    assert not await TextContains("xyz")(message("hello"))
    assert not await TextEquals("hello")(IncomingCallbackQuery(data="hello"))

@pytest.mark.asyncio
async def test_callback_filters_use_only_normalized_data() -> None:
    event = IncomingCallbackQuery(data="menu:settings")
    assert await CallbackDataEquals("menu:settings")(event)
    assert not await CallbackDataEquals("menu")(event)
    assert await CallbackDataStartsWith("menu:")(event)
    assert not await CallbackDataStartsWith("settings:")(event)
    assert not await CallbackDataStartsWith("menu:")(IncomingCallbackQuery(data=None))

@pytest.mark.asyncio
async def test_chat_type_normalizes_supergroup_to_group() -> None:
    assert await ChatType("private")(message("x", "private"))
    assert await ChatType("group")(message("x", "group"))
    assert await ChatType("group")(message("x", "supergroup"))
    assert not await ChatType("private")(message("x", "group"))
    assert not await ChatType("group")(message("x", None))
