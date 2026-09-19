from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class UniqueGiftSymbol:
    """This object describes the symbol shown on the pattern of a unique gift.

Attributes:
    name: Name of the symbol
    sticker: The sticker that represents the unique gift
    rarity_per_mille: The number of unique gifts that receive this model for every 1000 gifts upgraded"""
    name: str = ''
    rarity_per_milles: int = 0
    star_count: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['UniqueGiftSymbol']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['UniqueGiftSymbol']``).\n        "
        if data is None:
            return None
        return cls(name=data.get('name', ''), rarity_per_milles=data.get('rarity_per_milles', 0), star_count=data.get('star_count', 0))
