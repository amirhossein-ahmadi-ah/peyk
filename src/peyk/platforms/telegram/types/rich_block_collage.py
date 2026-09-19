from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichBlockCollage:
    """A collage, corresponding to the custom HTML tag .

Attributes:
    type: Type of the block, always 'collage'
    blocks: Elements of the collage
    caption: Caption of the block"""
    items: Optional[List[object]] = None

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(items=data.get('items')) if data else None
