from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BackgroundFillSolid:
    """The background is filled using the selected color.

Attributes:
    type: Type of the background fill, always 'solid'
    color: The color of the background fill in the RGB24 format"""
    type: str = 'solid'
    color: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BackgroundFillSolid']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BackgroundFillSolid']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'solid'), color=data.get('color', 0))
