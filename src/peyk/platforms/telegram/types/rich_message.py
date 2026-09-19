from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichMessage:
    """Rich formatted message.

Attributes:
    blocks: Content of the message
    is_rtl: True, if the rich message must be shown right-to-left"""
    text: str = ''
    blocks: Optional[object] = None
    is_rtl: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['RichMessage']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['RichMessage']``).\n        "
        if data is None:
            return None
        return cls(text=data.get('text', ''), blocks=data.get('blocks'), is_rtl=data.get('is_rtl'))
