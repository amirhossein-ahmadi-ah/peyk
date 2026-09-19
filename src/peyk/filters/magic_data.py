from __future__ import annotations

from collections.abc import Mapping, Iterator
from .base import BaseFilter


class _DependencyData(Mapping[str, object]):
    """Expose dispatcher dependency data through both attributes and keys."""

    def __init__(self, data: Mapping[str, object]) -> None:
        self._data = dict(data)

    def __getitem__(self, key: str) -> object:
        return self._data[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __getattr__(self, name: str) -> object:
        try:
            return self._data[name]
        except KeyError as exc:
            raise AttributeError(name) from exc


class MagicData(BaseFilter):
    """Evaluate a magic filter against dispatcher dependency data."""

    def __init__(self, magic: object) -> None:
        self.magic = magic

    async def __call__(self, event: object, **data: object) -> bool | dict[str, object]:
        # ``F.value`` is an attribute lookup, while ``F["value"]`` is a key
        # lookup.  The proxy intentionally supports both so MagicData behaves
        # consistently regardless of how the dependency is expressed.
        context = _DependencyData(data)
        resolver = getattr(self.magic, "resolve", None)
        if resolver is not None:
            result = resolver(context)
        elif callable(self.magic):
            result = self.magic(context)
        else:
            result = self.magic
        if hasattr(result, "__await__"):
            result = await result
        return bool(result)
