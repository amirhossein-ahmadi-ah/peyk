"""In-process FSM storage."""
from __future__ import annotations

import asyncio
from copy import deepcopy
from collections.abc import Mapping

from .base import BaseStorage, DefaultKeyBuilder, FSMData, KeyBuilder, StorageKey, coerce_storage_key


class MemoryStorage(BaseStorage):
    """Store FSM state and data in process memory."""

    def __init__(self, *, key_builder: KeyBuilder | None = None) -> None:
        super().__init__(key_builder=key_builder or DefaultKeyBuilder())
        self._states: dict[str, str] = {}
        self._data: dict[str, FSMData] = {}
        self._lock = asyncio.Lock()
        self._closed = False

    def _key(self, key: StorageKey | str, part: str) -> str:
        return self.key_builder.build(coerce_storage_key(key), part)

    async def get_state(self, key: StorageKey | str) -> str | None:
        """Return the stored state for ``key``."""
        async with self._lock:
            return self._states.get(self._key(key, "state"))

    async def set_state(self, key: StorageKey | str, state: str | None) -> None:
        """Set or clear the stored state."""
        async with self._lock:
            storage_key = self._key(key, "state")
            if state is None:
                self._states.pop(storage_key, None)
            else:
                self._states[storage_key] = state

    async def get_data(self, key: StorageKey | str) -> FSMData:
        """Return a defensive copy of conversation data."""
        async with self._lock:
            return deepcopy(self._data.get(self._key(key, "data"), {}))

    async def set_data(self, key: StorageKey | str, data: Mapping[str, object]) -> None:
        """Replace conversation data with a defensive copy."""
        async with self._lock:
            self._data[self._key(key, "data")] = deepcopy(dict(data))

    async def update_data(
        self,
        key: StorageKey | str,
        data: Mapping[str, object] | None = None,
        **kwargs: object,
    ) -> FSMData:
        """Merge mapping and keyword values into conversation data."""
        async with self._lock:
            storage_key = self._key(key, "data")
            current = self._data.setdefault(storage_key, {})
            if data is not None:
                current.update(data)
            current.update(kwargs)
            return deepcopy(current)

    async def close(self) -> None:
        """Release in-memory data and mark the backend closed."""
        async with self._lock:
            self._states.clear()
            self._data.clear()
            self._closed = True
