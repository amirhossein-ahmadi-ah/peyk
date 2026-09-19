from __future__ import annotations
from dataclasses import dataclass, field
from typing import Generic, TypeVar
T = TypeVar('T')

@dataclass
class MediaGroupBuilder(Generic[T]):
    """Collect media items for a platform-supported media group."""
    items: list[T] = field(default_factory=list)

    def add(self, media: T) -> 'MediaGroupBuilder[T]':
        """Performs the add operation for the utility client.

Args:
    media: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        self.items.append(media)
        return self

    def build(self) -> list[T]:
        """Performs the build operation for the utility client.

Returns:
    Result produced by the utility operation."""
        return list(self.items)

    def __len__(self) -> int:
        return len(self.items)
