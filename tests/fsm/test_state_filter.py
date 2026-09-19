from dataclasses import dataclass, field

import pytest

from peyk.dispatcher import Router
from peyk.platform_core.contracts import IncomingMessage
from peyk.dispatcher.filters import StateFilter
from peyk.fsm import FSMContext, MemoryStorage, State, StatesGroup


class States(StatesGroup):
    waiting = State()


@dataclass
class RawBale:
    pass
RawBale.__module__ = "peyk.platforms.bale.models"

@dataclass(frozen=True)
class Event(IncomingMessage):
    raw: object = field(default_factory=RawBale)


@pytest.mark.asyncio
async def test_state_filter_only_fires_in_selected_state():
    storage = MemoryStorage()
    router = Router()
    seen = []

    @router.message(StateFilter(States.waiting, storage))
    async def handler(event):
        seen.append(event.text)

    event = Event(chat_id=1, sender_id=2, text="before")
    assert await router.propagate_event(event) is not None

    await FSMContext(event, storage).set_state(States.waiting)
    await router.propagate_event(Event(chat_id=1, sender_id=2, text="during"))
    await router.propagate_event(Event(chat_id=1, sender_id=2, text="during-2"))
    assert seen == ["during", "during-2"]

    await FSMContext(event, storage).set_state(None)
    await router.propagate_event(Event(chat_id=1, sender_id=2, text="after"))
    assert seen == ["during", "during-2"]


@pytest.mark.asyncio
async def test_conversations_are_isolated_and_platform_aware():
    storage = MemoryStorage()

    bale = Event(chat_id=100, sender_id=200, raw=RawBale())
    bale_same = Event(chat_id=100, sender_id=200, raw=RawBale())
    await FSMContext(bale, storage).set_state(States.waiting)
    assert await FSMContext(bale_same, storage).get_state() == "States:waiting"

    class RawTelegram: pass
    RawTelegram.__module__ = "peyk.platforms.telegram.models"
    telegram = Event(100, 200, raw=RawTelegram())
    assert await FSMContext(telegram, storage).get_state() is None

    other_user = Event(chat_id=100, sender_id=201, raw=RawBale())
    assert await FSMContext(other_user, storage).get_state() is None
