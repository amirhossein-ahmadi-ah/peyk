from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichBlockList:
    """A list of blocks, corresponding to the HTML tag  or  with multiple nested tags .

Attributes:
    type: Type of the block, always 'list'
    items: Items of the list"""
    items: Optional[List[object]] = None

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(items=data.get('items')) if data else None
