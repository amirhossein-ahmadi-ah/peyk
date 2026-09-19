"""Storage contracts and key builders for the dispatcher FSM."""
from __future__ import annotations
import warnings
from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol, runtime_checkable
Identifier = int | str
FSMData = dict[str, object]

@dataclass(frozen=True, slots=True)
class StorageKey:
    """Identify one FSM namespace without embedding a bot token.

    ``platform`` is deliberately part of the identity so equal numeric IDs on
    Telegram and Bale cannot share state. ``bot_id`` isolates two bots on the
    same platform.
    """
    platform: str
    bot_id: Identifier
    chat_id: Identifier | None
    user_id: Identifier | None
    destiny: str = 'default'

@runtime_checkable
class KeyBuilder(Protocol):
    """Build backend keys from a :class:`StorageKey`."""

    def build(self, key: StorageKey, part: str | None=None) -> str:
        """Performs the build operation for the FSM client.

Args:
    key: Value used by this operation.
    part: Value used by this operation.

Returns:
    Result produced by the FSM operation."""
        ...

@dataclass(frozen=True, slots=True)
class DefaultKeyBuilder:
    """Build aiogram-shaped FSM keys with platform and bot namespaces.

    The default is equivalent to aiogram's ``with_bot_id=True`` plus the
    additional platform segment required by Peyk's multi-platform contract.
    """
    prefix: str = 'peyk'
    separator: str = ':'
    with_bot_id: bool = True
    with_destiny: bool = True

    def build(self, key: StorageKey, part: str | None=None) -> str:
        """Performs the build operation for the FSM client.

Args:
    key: Value used by this operation.
    part: Value used by this operation.

Returns:
    Result produced by the FSM operation."""
        if not key.platform:
            raise ValueError('StorageKey.platform must not be empty')
        if key.destiny != 'default' and (not self.with_destiny):
            raise ValueError('destiny is disabled by this key builder')
        parts = [self.prefix, key.platform]
        if self.with_bot_id:
            parts.append(str(key.bot_id))
        if key.chat_id is not None:
            parts.append(str(key.chat_id))
        if key.user_id is not None:
            parts.append(str(key.user_id))
        if self.with_destiny:
            parts.append(key.destiny)
        if part is not None:
            parts.append(part)
        return self.separator.join(parts)

def coerce_storage_key(key: StorageKey | str) -> StorageKey:
    """Convert a legacy string key while preserving old storage tests.

    New dispatcher code always passes :class:`StorageKey`; string keys are a
    deprecated compatibility escape hatch and cannot provide bot isolation.
    """
    if isinstance(key, StorageKey):
        return key
    warnings.warn('String FSM storage keys are deprecated; use StorageKey.', DeprecationWarning, stacklevel=3)
    return StorageKey(platform='legacy', bot_id='legacy', chat_id=key, user_id=None)

class BaseStorage(ABC):
    """Abstract asynchronous FSM storage keyed by :class:`StorageKey`."""

    def __init__(self, *, key_builder: KeyBuilder | None=None) -> None:
        self.key_builder = key_builder or DefaultKeyBuilder()

    @abstractmethod
    async def get_state(self, key: StorageKey | str) -> str | None:
        """Retrieves state from the FSM API.

Args:
    key: Value used by this operation.

Returns:
    Result produced by the FSM operation."""
        ...

    @abstractmethod
    async def set_state(self, key: StorageKey | str, state: str | None) -> None:
        """Updates state through the FSM API.

Args:
    key: Value used by this operation.
    state: Value used by this operation."""
        ...

    @abstractmethod
    async def get_data(self, key: StorageKey | str) -> FSMData:
        """Retrieves data from the FSM API.

Args:
    key: Value used by this operation.

Returns:
    Result produced by the FSM operation."""
        ...

    @abstractmethod
    async def set_data(self, key: StorageKey | str, data: Mapping[str, object]) -> None:
        """Updates data through the FSM API.

Args:
    key: Value used by this operation.
    data: Value used by this operation."""
        ...

    @abstractmethod
    async def update_data(self, key: StorageKey | str, data: Mapping[str, object] | None=None, **kwargs: object) -> FSMData:
        """Performs the update data operation for the FSM client.

Args:
    key: Value used by this operation.
    data: Value used by this operation.

Returns:
    Result produced by the FSM operation."""
        ...

    @abstractmethod
    async def close(self) -> None:
        """Performs the close operation for the FSM client."""
        ...

@runtime_checkable
class LegacyStringStorage(Protocol):
    """Protocol for the pre-Phase-8 string-key storage API."""

    async def get_state(self, key: str) -> str | None:
        """Retrieves state from the FSM API.

Args:
    key: Value used by this operation.

Returns:
    Result produced by the FSM operation."""
        ...

    async def set_state(self, key: str, state: str | None) -> None:
        """Updates state through the FSM API.

Args:
    key: Value used by this operation.
    state: Value used by this operation."""
        ...

    async def get_data(self, key: str) -> FSMData:
        """Retrieves data from the FSM API.

Args:
    key: Value used by this operation.

Returns:
    Result produced by the FSM operation."""
        ...

    async def set_data(self, key: str, data: Mapping[str, object]) -> None:
        """Updates data through the FSM API.

Args:
    key: Value used by this operation.
    data: Value used by this operation."""
        ...

    async def update_data(self, key: str, **kwargs: object) -> FSMData:
        """Performs the update data operation for the FSM client.

Args:
    key: Value used by this operation.

Returns:
    Result produced by the FSM operation."""
        ...

    async def close(self) -> None:
        """Performs the close operation for the FSM client."""
        ...

class LegacyStorageAdapter(BaseStorage):
    """Adapt the pre-Phase-8 string-key storage API to ``StorageKey``."""

    def __init__(self, storage: LegacyStringStorage, *, key_builder: KeyBuilder | None=None) -> None:
        warnings.warn('LegacyStorageAdapter is deprecated; implement BaseStorage with StorageKey instead.', DeprecationWarning, stacklevel=2)
        super().__init__(key_builder=key_builder or DefaultKeyBuilder())
        self.storage = storage

    def _legacy_key(self, key: StorageKey | str) -> str:
        if isinstance(key, str):
            return key
        return self.key_builder.build(key)

    async def get_state(self, key: StorageKey | str) -> str | None:
        """Retrieves state from the FSM API.

Args:
    key: Value used by this operation.

Returns:
    Result produced by the FSM operation."""
        return await self.storage.get_state(self._legacy_key(key))

    async def set_state(self, key: StorageKey | str, state: str | None) -> None:
        """Updates state through the FSM API.

Args:
    key: Value used by this operation.
    state: Value used by this operation."""
        await self.storage.set_state(self._legacy_key(key), state)

    async def get_data(self, key: StorageKey | str) -> FSMData:
        """Retrieves data from the FSM API.

Args:
    key: Value used by this operation.

Returns:
    Result produced by the FSM operation."""
        return await self.storage.get_data(self._legacy_key(key))

    async def set_data(self, key: StorageKey | str, data: Mapping[str, object]) -> None:
        """Updates data through the FSM API.

Args:
    key: Value used by this operation.
    data: Value used by this operation."""
        await self.storage.set_data(self._legacy_key(key), data)

    async def update_data(self, key: StorageKey | str, data: Mapping[str, object] | None=None, **kwargs: object) -> FSMData:
        """Performs the update data operation for the FSM client.

Args:
    key: Value used by this operation.
    data: Value used by this operation.

Returns:
    Result produced by the FSM operation."""
        values = dict(data or {})
        values.update(kwargs)
        return await self.storage.update_data(self._legacy_key(key), **values)

    async def close(self) -> None:
        """Performs the close operation for the FSM client."""
        await self.storage.close()
