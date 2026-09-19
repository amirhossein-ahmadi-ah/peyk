import asyncio
import pytest

from peyk.dispatcher import Router
from peyk.dispatcher.filters import CallbackDataStartsWith, TextEquals
from peyk.platform_core.adapters.bale import normalize_callback as normalize_bale_callback
from peyk.platform_core.adapters.bale import normalize_message as normalize_bale_message
from peyk.platform_core.adapters.rubika import normalize_callback as normalize_rubika_callback
from peyk.platform_core.adapters.rubika import normalize_message as normalize_rubika_message
from peyk.platform_core.adapters.telegram import normalize_callback as normalize_telegram_callback
from peyk.platform_core.adapters.telegram import normalize_message as normalize_telegram_message
from peyk.platform_core.contracts import IncomingCallbackQuery, IncomingMessage
from peyk.platforms.bale.models import CallbackQuery as BaleCallbackQuery
from peyk.platforms.bale.models import Chat as BaleChat
from peyk.platforms.bale.models import Message as BaleMessage
from peyk.platforms.bale.models import User as BaleUser
from peyk.platforms.rubika.models import AuxData, InlineMessage, Message as RubikaMessage
from peyk.platforms.telegram.models import CallbackQuery as TelegramCallbackQuery
from peyk.platforms.telegram.models import Chat as TelegramChat
from peyk.platforms.telegram.models import Message as TelegramMessage
from peyk.platforms.telegram.models import User as TelegramUser


@pytest.mark.asyncio
async def test_same_router_and_filters_dispatch_identically_across_three_platform_outputs() -> None:
    router = Router()
    seen: list[str] = []

    @router.message(TextEquals("hello"))
    async def message_handler(event: IncomingMessage) -> None:
        seen.append("message")

    @router.callback_query(CallbackDataStartsWith("menu:"))
    async def callback_handler(event: IncomingCallbackQuery) -> None:
        seen.append("callback")

    telegram_message = TelegramMessage(
        message_id=1, date=1, chat=TelegramChat(id=10, type="private"),
        from_=TelegramUser(id=11, is_bot=False, first_name="T"), text="hello",
    )
    bale_message = BaleMessage(
        message_id=1, date=1, chat=BaleChat(id=10, type="private"),
        from_=BaleUser(id=11, is_bot=False, first_name="B"), text="hello",
    )
    rubika_message = RubikaMessage(message_id="1", text="hello", sender_id="11", time=1)

    telegram_callback = TelegramCallbackQuery(
        id="t", from_=TelegramUser(id=11, is_bot=False, first_name="T"), data="menu:open"
    )
    bale_callback = BaleCallbackQuery(
        id="b", from_=BaleUser(id=11, is_bot=False, first_name="B"), data="menu:open"
    )
    rubika_callback = InlineMessage(
        sender_id="11", text="x", message_id="1", chat_id="10",
        aux_data=AuxData(button_id="menu:open"),
    )

    for event in (
        normalize_telegram_message(telegram_message),
        normalize_bale_message(bale_message),
        normalize_rubika_message(rubika_message),
        normalize_telegram_callback(telegram_callback),
        normalize_bale_callback(bale_callback),
        normalize_rubika_callback(rubika_callback),
    ):
        await router.propagate_event(event)

    assert seen == ["message", "message", "message", "callback", "callback", "callback"]


def test_chat_type_filter_uses_normalized_field_not_raw_platform_objects() -> None:
    from peyk.dispatcher.filters import ChatType
    from peyk.platform_core.contracts import IncomingMessage

    assert asyncio.run(ChatType("private")(IncomingMessage(text="x", chat_type="private")))
    assert asyncio.run(ChatType("group")(IncomingMessage(text="x", chat_type="supergroup")))
