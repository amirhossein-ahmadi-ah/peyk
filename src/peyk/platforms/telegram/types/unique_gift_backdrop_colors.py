from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class UniqueGiftBackdropColors:
    """This object describes the colors of the backdrop of a unique gift.

Attributes:
    center_color: The color in the center of the backdrop in RGB format
    edge_color: The color on the edges of the backdrop in RGB format
    symbol_color: The color to be applied to the symbol in RGB format
    text_color: The color for the text on the backdrop in RGB format"""
    center_color: int = 0
    edge_color: int = 0
    symbol_color: int = 0
    text_color: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['UniqueGiftBackdropColors']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['UniqueGiftBackdropColors']``).\n        "
        if data is None:
            return None
        return cls(center_color=data.get('center_color', 0), edge_color=data.get('edge_color', 0), symbol_color=data.get('symbol_color', 0), text_color=data.get('text_color', 0))
