from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputRichBlockSlideshow:
    """A slideshow, corresponding to the custom HTML tag .

Attributes:
    type: Type of the block, always 'slideshow'
    blocks: Elements of the slideshow
    caption: Caption of the block"""
    items: Optional[List[object]] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'items': self.items or []}
