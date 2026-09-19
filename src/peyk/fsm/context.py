"""FSM context and event-to-storage-key compatibility helpers."""
from __future__ import annotations

import warnings
from collections.abc import Mapping
from enum import Enum
from typing import overload

from .state import State
from .storage.base import BaseStorage, FSMData, LegacyStorageAdapter, LegacyStringStorage, StorageKey


class FSMStrategy(str, Enum):
    """Select which event identities share one FSM conversation."""

    USER_IN_CHAT = "USER_IN_CHAT"
    CHAT = "CHAT"
    GLOBAL_USER = "GLOBAL_USER"


def _identity(event: object) -> tuple[object | None, object | None]:
    chat_id = getattr(event, "chat_id", None)
    user_id = getattr(event, "sender_id", None)
    if user_id is None:
        user_id = getattr(event, "from_user_id", None)
    if user_id is None:
        user_id = getattr(event, "actor_id", None)
    if user_id is None:
        user_id = getattr(event, "target_user_id", None)
    return chat_id, user_id


def build_storage_key(
    event: object,
    *,
    platform: str,
    bot_id: int | str,
    strategy: str | FSMStrategy = FSMStrategy.USER_IN_CHAT,
    destiny: str = "default",
) -> StorageKey:
    """Build a platform/bot-aware key from a normalized event."""
    chat_id, user_id = _identity(event)
    if strategy == FSMStrategy.USER_IN_CHAT:
        if chat_id is None and user_id is None:
            raise ValueError("normalized event has no conversation identity")
    elif strategy == FSMStrategy.CHAT:
        if chat_id is None:
            raise ValueError("FSMStrategy.CHAT requires chat_id")
        user_id = None
    elif strategy == FSMStrategy.GLOBAL_USER:
        if user_id is None:
            raise ValueError("FSMStrategy.GLOBAL_USER requires user_id")
        chat_id = None
    else:
        raise ValueError(f"unsupported FSM strategy: {strategy}")
    if not isinstance(chat_id, (int, str)) and chat_id is not None:
        raise TypeError("chat_id must be int or str")
    if not isinstance(user_id, (int, str)) and user_id is not None:
        raise TypeError("user_id must be int or str")
    return StorageKey(platform, bot_id, chat_id, user_id, destiny)


def conversation_key(event: object, *, platform: str | None = None, bot_id: int | str | None = None) -> StorageKey:
    """Return a compatibility :class:`StorageKey` for an event.

    The old form inferred the platform from ``event.raw`` and had no bot ID.
    That form is deprecated; dispatcher integrations must pass both values.
    """
    if platform is None or bot_id is None:
        warnings.warn(
            "conversation_key() without platform and bot_id is deprecated; use build_storage_key().",
            DeprecationWarning,
            stacklevel=2,
        )
        raw = getattr(event, "raw", None)
        module = getattr(raw.__class__, "__module__", "") if raw is not None else ""
        platform = next((name for name in ("telegram", "bale", "rubika") if f"peyk.platforms.{name}" in module), "legacy")
        bot_id = "legacy"
    return build_storage_key(event, platform=platform, bot_id=bot_id)


class FSMContext:
    """Read and mutate state/data for one :class:`StorageKey`."""

    @overload
    def __init__(self, storage: BaseStorage, key: StorageKey) -> None: ...

    @overload
    def __init__(self, event: object, storage: BaseStorage | LegacyStringStorage, *, platform: str | None = None, bot_id: int | str | None = None) -> None: ...

    def __init__(
        self,
        first: BaseStorage | object,
        second: StorageKey | BaseStorage | LegacyStringStorage,
        *,
        platform: str | None = None,
        bot_id: int | str | None = None,
    ) -> None:
        if isinstance(first, BaseStorage) and isinstance(second, StorageKey):
            self.storage = first
            self.key = second
            self.event: object | None = None
            return
        if isinstance(second, BaseStorage):
            warnings.warn(
                "FSMContext(event, storage) is deprecated; use FSMContext(storage, key) or FSMContext.for_event().",
                DeprecationWarning,
                stacklevel=2,
            )
            self.event = first
            self.storage = second
            self.key = conversation_key(first, platform=platform, bot_id=bot_id)
            return
        if isinstance(second, LegacyStringStorage):
            warnings.warn(
                "FSMContext with a legacy string-key storage is deprecated; use BaseStorage.",
                DeprecationWarning,
                stacklevel=2,
            )
            self.event = first
            self.storage = LegacyStorageAdapter(second)
            self.key = conversation_key(first, platform=platform, bot_id=bot_id)
            return
        raise TypeError("FSMContext expects (storage, StorageKey)")

    @classmethod
    def for_event(
        cls,
        event: object,
        storage: BaseStorage,
        *,
        platform: str,
        bot_id: int | str,
        strategy: str | FSMStrategy = FSMStrategy.USER_IN_CHAT,
        destiny: str = "default",
    ) -> FSMContext:
        """Create a context for a normalized event using explicit identity data."""
        return cls(storage, build_storage_key(event, platform=platform, bot_id=bot_id, strategy=strategy, destiny=destiny))

    async def get_state(self) -> str | None:
        """Return the current state."""
        return await self.storage.get_state(self.key)

    async def set_state(self, state: State | str | None) -> None:
        """Set or clear the current state."""
        await self.storage.set_state(self.key, None if state is None else state.state if isinstance(state, State) else str(state))

    async def get_data(self) -> FSMData:
        """Return a copy of conversation data."""
        return await self.storage.get_data(self.key)

    async def set_data(self, data: Mapping[str, object]) -> None:
        """Replace conversation data."""
        await self.storage.set_data(self.key, data)

    async def get_value(self, key: str, default: object = None) -> object:
        """Return one data value, or ``default`` when absent."""
        return (await self.get_data()).get(key, default)

    async def update_data(
        self,
        data: Mapping[str, object] | None = None,
        **kwargs: object,
    ) -> FSMData:
        """Merge mapping and keyword values into conversation data."""
        return await self.storage.update_data(self.key, data, **kwargs)

    async def clear(self) -> None:
        """Clear both state and conversation data."""
        await self.storage.set_state(self.key, None)
        await self.storage.set_data(self.key, {})
