from __future__ import annotations

import asyncio
import re

import pytest

from peyk import Bot, Dispatcher
from peyk.fsm import (
    FSMContext,
    FSMStrategy,
    MemoryStorage,
    SimpleEventIsolation,
    State,
    StatesGroup,
    StorageKey,
    build_storage_key,
)
from peyk.filters import StateFilter
from peyk.platform_core.contracts import IncomingCallbackQuery, IncomingMessage
from peyk.types import User


class Form(StatesGroup):
    name = State()
    age = State()

    class Address(StatesGroup):
        city = State()


def event(chat_id: int | str, user_id: int | str) -> IncomingMessage:
    return IncomingMessage(chat_id=chat_id, sender_id=user_id, text="x")


def bot(platform: str, bot_id: int | str) -> Bot[object]:
    value = Bot("token", platform=platform)
    value._me = User(id=bot_id, is_bot=True, first_name="bot")
    return value


@pytest.mark.asyncio
async def test_storage_key_isolated_by_platform_and_bot() -> None:
    storage = MemoryStorage()
    tg_a = FSMContext(storage, StorageKey("telegram", 10, 1, 2))
    tg_b = FSMContext(storage, StorageKey("telegram", 11, 1, 2))
    bale = FSMContext(storage, StorageKey("bale", 10, 1, 2))
    await tg_a.set_state(Form.name)
    assert await tg_b.get_state() is None
    assert await bale.get_state() is None
    assert await tg_a.get_state() == "Form:name"


@pytest.mark.parametrize(
    ("strategy", "chat_id", "user_id", "expected"),
    [
        (FSMStrategy.USER_IN_CHAT, 10, 20, (10, 20)),
        (FSMStrategy.CHAT, 10, 20, (10, None)),
        (FSMStrategy.GLOBAL_USER, 10, 20, (None, 20)),
    ],
)
def test_all_fsm_strategies(strategy, chat_id, user_id, expected) -> None:
    key = build_storage_key(event(chat_id, user_id), platform="telegram", bot_id=99, strategy=strategy)
    assert (key.chat_id, key.user_id) == expected


def test_nested_states_group_metadata() -> None:
    assert Form.__states__ == (Form.name, Form.age)
    assert Form.Address.__all_states__ == (Form.Address.city,)
    assert Form.__all_states__ == (Form.name, Form.age, Form.Address.city)
    assert Form.Address.city.state == "Form.Address:city"


@pytest.mark.asyncio
async def test_state_filter_reads_raw_state_without_storage() -> None:
    event_value = event(1, 2)
    assert await StateFilter(Form.name)(event_value, raw_state="Form:name") is True
    assert await StateFilter(Form)(event_value, raw_state="Form:age") is True
    assert await StateFilter(None)(event_value, raw_state=None) is True
    assert await StateFilter(re.compile(r"Form:.*"))(event_value, raw_state="Form:age") is True


@pytest.mark.asyncio
async def test_dispatcher_injects_state_and_raw_state() -> None:
    dispatcher = Dispatcher(storage=MemoryStorage())
    tg = bot("telegram", 123)
    seen: list[str | None] = []

    @dispatcher.message(StateFilter(Form.name))
    async def handler(message, state: FSMContext, raw_state: str | None) -> None:
        seen.append(raw_state)
        await state.set_state(Form.age)

    message = event(1, 2)
    key = build_storage_key(message, platform="telegram", bot_id=123)
    await dispatcher.storage.set_state(key, "Form:name")
    await dispatcher.propagate_event(message, bot=tg, dispatcher=dispatcher)
    assert seen == ["Form:name"]
    assert await dispatcher.storage.get_state(key) == "Form:age"


@pytest.mark.asyncio
async def test_callback_and_message_share_user_in_chat_key() -> None:
    storage = MemoryStorage()
    message = event(55, 77)
    callback = IncomingCallbackQuery(from_user_id=77, chat_id=55, data="ok")
    message_key = build_storage_key(message, platform="telegram", bot_id=1)
    callback_key = build_storage_key(callback, platform="telegram", bot_id=1)
    assert message_key == callback_key
    await FSMContext(storage, message_key).set_state(Form.name)
    assert await FSMContext(storage, callback_key).get_state() == "Form:name"


@pytest.mark.asyncio
async def test_simple_event_isolation_serializes_same_key_not_different_keys() -> None:
    isolation = SimpleEventIsolation()
    same = StorageKey("telegram", 1, 10, 20)
    other = StorageKey("telegram", 1, 10, 21)
    active: dict[StorageKey, int] = {same: 0, other: 0}
    peaks: dict[StorageKey, int] = {same: 0, other: 0}

    async def run(key: StorageKey) -> None:
        async with isolation.lock(key):
            active[key] += 1
            peaks[key] = max(peaks[key], active[key])
            await asyncio.sleep(0.02)
            active[key] -= 1

    await asyncio.gather(run(same), run(same), run(other))
    assert peaks[same] == 1
    assert peaks[other] == 1
    await isolation.close()


@pytest.mark.asyncio
async def test_legacy_context_constructor_still_works() -> None:
    storage = MemoryStorage()
    legacy_event = event(10, 20)
    with pytest.deprecated_call():
        context = FSMContext(legacy_event, storage)
    await context.set_state(Form.name)
    assert await context.get_state() == "Form:name"
