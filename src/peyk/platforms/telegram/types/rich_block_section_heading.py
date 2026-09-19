from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichBlockSectionHeading:
    """A section heading, corresponding to the HTML tags , , , , , or .

Attributes:
    type: Type of the block, always 'heading'
    text: Text of the block
    size: Relative size of the text font; 1-6, 1 is the largest, 6 is the smallest"""
    text: str = ''

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(text=data.get('text', '')) if data else None
