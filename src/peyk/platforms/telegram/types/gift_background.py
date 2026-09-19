from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class GiftBackground:
    """This object describes the background of a gift.

Attributes:
    center_color: Center color of the background in RGB format
    edge_color: Edge color of the background in RGB format
    text_color: Text color of the background in RGB format"""
    name: str = ''
    center_color: int = 0
    edge_color: int = 0
    symbol_color: int = 0
    text_color: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['GiftBackground']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['GiftBackground']``).\n        "
        if data is None:
            return None
        return cls(name=data.get('name', ''), center_color=data.get('center_color', 0), edge_color=data.get('edge_color', 0), symbol_color=data.get('symbol_color', 0), text_color=data.get('text_color', 0))
