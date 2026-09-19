"""FSM event isolation primitives."""
from __future__ import annotations
import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Protocol
from .base import DefaultKeyBuilder, KeyBuilder, StorageKey

class BaseEventIsolation:
    """Serialize handlers that share one :class:`StorageKey`."""

    def lock(self, key: StorageKey) -> AsyncIterator[None]:
        """Return an async context manager for the event lock."""
        raise NotImplementedError

    async def close(self) -> None:
        """Close isolation resources."""

class DisabledEventIsolation(BaseEventIsolation):
    """Do not serialize events."""

    @asynccontextmanager
    async def lock(self, key: StorageKey) -> AsyncIterator[None]:
        """Performs the lock operation for the FSM client.

Args:
    key: Value used by this operation.

Returns:
    Result produced by the FSM operation."""
        yield

@dataclass
class _LockEntry:
    lock: asyncio.Lock
    waiters: int = 0

class SimpleEventIsolation(BaseEventIsolation):
    """Serialize by key and evict idle locks after release."""

    def __init__(self) -> None:
        self._entries: dict[StorageKey, _LockEntry] = {}
        self._entries_lock = asyncio.Lock()

    @asynccontextmanager
    async def lock(self, key: StorageKey) -> AsyncIterator[None]:
        """Performs the lock operation for the FSM client.

Args:
    key: Value used by this operation.

Returns:
    Result produced by the FSM operation."""
        async with self._entries_lock:
            entry = self._entries.get(key)
            if entry is None:
                entry = _LockEntry(asyncio.Lock())
                self._entries[key] = entry
            entry.waiters += 1
        try:
            await entry.lock.acquire()
            yield
        finally:
            entry.lock.release()
            async with self._entries_lock:
                entry.waiters -= 1
                if entry.waiters == 0 and (not entry.lock.locked()) and (self._entries.get(key) is entry):
                    self._entries.pop(key, None)

    async def close(self) -> None:
        """Performs the close operation for the FSM client."""
        async with self._entries_lock:
            self._entries.clear()

class RedisLock(Protocol):
    """RedisLock provides the FSM API surface used by peyk."""

    async def acquire(self) -> bool:
        """Performs the acquire operation for the FSM client.

Returns:
    Result produced by the FSM operation."""
        ...

    async def release(self) -> None:
        """Performs the release operation for the FSM client."""
        ...

class RedisLockClient(Protocol):
    """RedisLockClient provides the FSM API surface used by peyk."""

    def lock(self, name: str, timeout: float | None=None, sleep: float=0.1, blocking: bool=True, blocking_timeout: float | None=None) -> RedisLock:
        """Performs the lock operation for the FSM client.

Args:
    name: Value used by this operation.
    timeout: Maximum time to wait for the operation.
    sleep: Value used by this operation.
    blocking: Value used by this operation.
    blocking_timeout: Value used by this operation.

Returns:
    Result produced by the FSM operation."""
        ...

    async def aclose(self) -> None:
        """Performs the aclose operation for the FSM client."""
        ...

class RedisEventIsolation(BaseEventIsolation):
    """Serialize events using Redis distributed locks."""

    def __init__(self, redis: RedisLockClient, *, key_builder: KeyBuilder | None=None, lock_timeout: float | None=30.0, blocking_timeout: float | None=None) -> None:
        self.redis = redis
        self.key_builder = key_builder or DefaultKeyBuilder()
        self.lock_timeout = lock_timeout
        self.blocking_timeout = blocking_timeout

    @asynccontextmanager
    async def lock(self, key: StorageKey) -> AsyncIterator[None]:
        """Performs the lock operation for the FSM client.

Args:
    key: Value used by this operation.

Returns:
    Result produced by the FSM operation."""
        lock = self.redis.lock(self.key_builder.build(key, 'lock'), timeout=self.lock_timeout, blocking_timeout=self.blocking_timeout)
        acquired = await lock.acquire()
        if not acquired:
            raise TimeoutError('could not acquire Redis FSM event lock')
        try:
            yield
        finally:
            await lock.release()

    async def close(self) -> None:
        """Performs the close operation for the FSM client."""
        close = getattr(self.redis, 'aclose', None)
        if close is not None:
            await close()
