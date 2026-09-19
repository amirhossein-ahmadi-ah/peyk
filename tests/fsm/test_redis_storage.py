import pytest

from peyk.fsm.storage.redis import RedisStorage


class FakeRedis:
    """Minimal async in-memory Redis test double; no external server needed."""

    def __init__(self):
        self.values = {}

    async def get(self, key):
        return self.values.get(key)

    async def set(self, key, value):
        self.values[key] = value
        return True

    async def delete(self, key):
        self.values.pop(key, None)
        return 1

    async def aclose(self):
        self.values.clear()


@pytest.mark.asyncio
async def test_redis_storage_without_real_server():
    storage = RedisStorage(FakeRedis(), prefix="test")
    await storage.set_state("key", "State:test")
    await storage.update_data("key", foo="bar", count=2)
    assert await storage.get_state("key") == "State:test"
    assert await storage.get_data("key") == {"foo": "bar", "count": 2}
    await storage.close()
