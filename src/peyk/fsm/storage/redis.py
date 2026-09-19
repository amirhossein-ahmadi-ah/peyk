"""Optional Redis-backed FSM storage."""
from __future__ import annotations
import json
from collections.abc import Mapping
from typing import Protocol
from .base import BaseStorage, DefaultKeyBuilder, FSMData, KeyBuilder, StorageKey, coerce_storage_key

class AsyncRedisClient(Protocol):
    """Minimal async Redis surface required by :class:`RedisStorage`."""

    async def get(self, key: str) -> str | bytes | None:
        """Performs the get operation for the FSM client.

Args:
    key: Value used by this operation.

Returns:
    Result produced by the FSM operation."""
        ...

    async def set(self, key: str, value: str, *, ex: int | float | None=None) -> object:
        """Performs the set operation for the FSM client.

Args:
    key: Value used by this operation.
    value: Value used by this operation.
    ex: Value used by this operation.

Returns:
    Result produced by the FSM operation."""
        ...

    async def delete(self, key: str) -> object:
        """Performs the delete operation for the FSM client.

Args:
    key: Value used by this operation.

Returns:
    Result produced by the FSM operation."""
        ...

    async def aclose(self) -> None:
        """Performs the aclose operation for the FSM client."""
        ...

class RedisStorage(BaseStorage):
    """Persist FSM state/data in Redis with independent optional TTLs."""

    def __init__(self, redis: AsyncRedisClient | None=None, *, state_ttl: int | float | None=None, data_ttl: int | float | None=None, key_builder: KeyBuilder | None=None, url: str | None=None, prefix: str | None=None) -> None:
        builder = key_builder or DefaultKeyBuilder(prefix=prefix or 'peyk')
        super().__init__(key_builder=builder)
        if redis is None:
            if url is None:
                raise ValueError('provide redis or url')
            try:
                from redis.asyncio import Redis
            except ImportError as exc:
                raise RuntimeError("RedisStorage requires 'peyk[fsm-redis]'") from exc
            redis = Redis.from_url(url, decode_responses=True)
        self.redis = redis
        self.state_ttl = state_ttl
        self.data_ttl = data_ttl

    def _key(self, key: StorageKey | str, part: str) -> str:
        return self.key_builder.build(coerce_storage_key(key), part)

    @staticmethod
    def _decode(value: str | bytes | None) -> str | None:
        if value is None:
            return None
        return value.decode() if isinstance(value, bytes) else value

    async def get_state(self, key: StorageKey | str) -> str | None:
        """Return a stored state string, if present."""
        return self._decode(await self.redis.get(self._key(key, 'state')))

    async def set_state(self, key: StorageKey | str, state: str | None) -> None:
        """Set or clear state, applying ``state_ttl`` when configured."""
        redis_key = self._key(key, 'state')
        if state is None:
            await self.redis.delete(redis_key)
        elif self.state_ttl is None:
            await self.redis.set(redis_key, state)
        else:
            await self.redis.set(redis_key, state, ex=self.state_ttl)

    async def get_data(self, key: StorageKey | str) -> FSMData:
        """Decode JSON conversation data from Redis."""
        value = self._decode(await self.redis.get(self._key(key, 'data')))
        if value is None:
            return {}
        decoded = json.loads(value)
        return dict(decoded) if isinstance(decoded, dict) else {}

    async def set_data(self, key: StorageKey | str, data: Mapping[str, object]) -> None:
        """Replace JSON conversation data and apply ``data_ttl``."""
        payload = json.dumps(dict(data), ensure_ascii=False, separators=(',', ':'))
        redis_key = self._key(key, 'data')
        if self.data_ttl is None:
            await self.redis.set(redis_key, payload)
        else:
            await self.redis.set(redis_key, payload, ex=self.data_ttl)

    async def update_data(self, key: StorageKey | str, data: Mapping[str, object] | None=None, **kwargs: object) -> FSMData:
        """Read, merge and persist conversation data."""
        current = await self.get_data(key)
        if data is not None:
            current.update(data)
        current.update(kwargs)
        await self.set_data(key, current)
        return current

    async def close(self) -> None:
        """Close the underlying Redis client when supported."""
        await self.redis.aclose()
