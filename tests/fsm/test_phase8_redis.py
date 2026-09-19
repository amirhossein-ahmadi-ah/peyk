from __future__ import annotations

import asyncio

import pytest

fakeredis = pytest.importorskip("fakeredis.aioredis")

from peyk.fsm import RedisStorage, StorageKey


@pytest.mark.asyncio
async def test_redis_storage_ttl_and_key_isolation() -> None:
    redis = fakeredis.FakeRedis(decode_responses=True)
    storage = RedisStorage(redis, state_ttl=1, data_ttl=1)
    key = StorageKey("telegram", 7, 10, 20)
    other = StorageKey("bale", 7, 10, 20)
    await storage.set_state(key, "Form:name")
    await storage.update_data(key, name="Ada")
    assert await storage.get_state(key) == "Form:name"
    assert await storage.get_data(key) == {"name": "Ada"}
    assert await storage.get_state(other) is None
    await asyncio.sleep(1.1)
    assert await storage.get_state(key) is None
    assert await storage.get_data(key) == {}
    await storage.close()
