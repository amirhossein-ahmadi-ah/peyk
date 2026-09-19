from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputRichBlockAnchor:
    """A block with an anchor, corresponding to the HTML tag  with the attribute name.

Attributes:
    type: Type of the block, always 'anchor'
    name: The name of the anchor"""
    name: str = ''
    text: str = ''

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'name': self.name, 'text': self.text}
