from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichBlockAnchor:
    """A block with an anchor, corresponding to the HTML tag  with the attribute name.

Attributes:
    type: Type of the block, always 'anchor'
    name: The name of the anchor"""
    name: str = ''
    text: str = ''

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(name=data.get('name', ''), text=data.get('text', '')) if data else None
