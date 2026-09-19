from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class UniqueGiftBackdrop:
    """This object describes the backdrop of a unique gift.

Attributes:
    name: Name of the backdrop
    colors: Colors of the backdrop
    rarity_per_mille: The number of unique gifts that receive this backdrop for every 1000 gifts upgraded"""
    name: str = ''
    colors: Optional[UniqueGiftBackdropColors] = None
    rarity_per_milles: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['UniqueGiftBackdrop']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['UniqueGiftBackdrop']``).\n        "
        if data is None:
            return None
        return cls(name=data.get('name', ''), colors=UniqueGiftBackdropColors.from_dict(data.get('colors')), rarity_per_milles=data.get('rarity_per_milles', 0))
