import pytest

from peyk.dispatcher import Router
from peyk.platforms.telegram.types.update import Update
from peyk.platforms.telegram.types.inline_query import InlineQuery
from peyk.platforms.telegram.types.message import Message as TelegramMessage
from peyk.platforms.telegram.types.chat import Chat
from peyk.platform_core.adapters.telegram import normalize_update
from peyk.platform_core.adapters.bale import normalize_update as normalize_bale_update
from peyk.platform_core.adapters.rubika import normalize_update as normalize_rubika_update
from peyk.platforms.bale.types.update import Update as BaleUpdate
from peyk.platforms.rubika.types.update import Update as RubikaUpdate
from peyk.platforms.rubika.enums import UpdateTypeEnum
from peyk.platforms.rubika.types.message import Message as RubikaMessage


@pytest.mark.asyncio
async def test_telegram_inline_query_observer_receives_native_model():
    router = Router()
    seen = []

    @router.inline_query()
    async def handler(event, bot):
        seen.append((event, bot))
        return True

    raw = Update(update_id=1, inline_query=InlineQuery(id="iq-1", query="hello"))
    marker = object()
    result = await router.propagate_platform_event(raw, platform="telegram", bot=marker)
    assert result is True
    assert isinstance(seen[0][0], InlineQuery)
    assert seen[0][0].id == "iq-1"
    assert seen[0][1] is marker


@pytest.mark.asyncio
async def test_generic_platform_event_receives_native_update():
    router = Router()
    seen = []

    @router.platform_event()
    async def handler(event, bot):
        seen.append((event, bot))
        return True

    raw = Update(update_id=2, inline_query=InlineQuery(id="iq-2"))
    marker = object()
    assert await router.propagate_platform_event(raw, platform="telegram", bot=marker) is True
    assert seen == [(raw, marker)]


def test_neutral_message_update_kind_is_platform_evidence_based():
    bale = BaleUpdate(update_id=1, message=None, edited_message=None)
    assert normalize_bale_update(bale) is bale

    rubika = RubikaUpdate(type=UpdateTypeEnum.UPDATED_MESSAGE, chat_id="c", updated_message=RubikaMessage(message_id="m"))
    event = normalize_rubika_update(rubika)
    assert getattr(event, "update_kind") == "edited_message"
    assert event.is_edited is True


def test_telegram_neutral_message_update_kind():
    raw = Update(update_id=3, edited_message=TelegramMessage(message_id=3, date=1, chat=Chat(id=1, type="private")) )
    event = normalize_update(raw)
    assert event.update_kind == "edited_message"
    assert event.is_edited is True

@pytest.mark.asyncio
async def test_telegram_native_observer_warning_for_non_telegram(caplog):
    from peyk import Dispatcher
    import logging
    dp = Dispatcher()
    @dp.inline_query()
    async def handler(event):
        return True
    class FakeBot:
        platform = "bale"
    with caplog.at_level(logging.WARNING):
        dp._warn_unsupported_observers(FakeBot())
    assert "Telegram-native" in caplog.text
    assert "inline_query" in caplog.text
