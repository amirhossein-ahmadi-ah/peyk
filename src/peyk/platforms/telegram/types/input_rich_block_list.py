from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputRichBlockList:
    """A list of blocks, corresponding to the HTML tag  or  with multiple nested tags .

Attributes:
    type: Type of the block, always 'list'
    items: Items of the list"""
    items: Optional[List[object]] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'items': self.items or []}
