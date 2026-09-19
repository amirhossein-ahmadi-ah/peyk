from dataclasses import dataclass

import pytest

from peyk.fsm import FSMContext, MemoryStorage, State, StatesGroup


class PanelStates(StatesGroup):
    waiting_for_lock_value = State()
    waiting_for_name = State()


@dataclass
class RawTelegram:
    pass

RawTelegram.__module__ = "peyk.platforms.telegram.models"


@dataclass
class Event:
    chat_id: int
    sender_id: int
    raw: object


@pytest.mark.asyncio
async def test_context_get_set_update():
    storage = MemoryStorage()
    context = FSMContext(Event(10, 20, RawTelegram()), storage)
    assert await context.get_state() is None
    assert await context.get_data() == {}

    await context.set_state(PanelStates.waiting_for_lock_value)
    await context.update_data(lock_key="emoji", value=3)

    assert await context.get_state() == "PanelStates:waiting_for_lock_value"
    assert await context.get_data() == {"lock_key": "emoji", "value": 3}

    await context.clear()
    assert await context.get_state() is None
    assert await context.get_data() == {}


class FakeRedis:
    def __init__(self):
        self.values = {}
    async def get(self, key): return self.values.get(key)
    async def set(self, key, value): self.values[key] = value
    async def delete(self, key): self.values.pop(key, None)
    async def aclose(self): self.values.clear()


@pytest.mark.asyncio
async def test_context_against_redis_backend():
    from peyk.fsm.storage.redis import RedisStorage
    storage = RedisStorage(FakeRedis(), prefix="context-test")
    context = FSMContext(Event(30, 40, raw=RawTelegram()), storage)
    await context.set_state(PanelStates.waiting_for_name)
    await context.update_data(name="Amir")
    assert await context.get_state() == "PanelStates:waiting_for_name"
    assert await context.get_data() == {"name": "Amir"}
    await storage.close()
