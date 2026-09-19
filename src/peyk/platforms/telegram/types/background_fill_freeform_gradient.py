from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BackgroundFillFreeformGradient:
    """The background is a freeform gradient that rotates after every message in the chat.

Attributes:
    type: Type of the background fill, always 'freeform_gradient'
    colors: A list of the 3 or 4 base colors that are used to generate the freeform gradient in the RGB24 format"""
    type: str = 'freeform_gradient'
    colors: Optional[List[int]] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BackgroundFillFreeformGradient']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BackgroundFillFreeformGradient']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'freeform_gradient'), colors=data.get('colors'))
