from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputRichBlockSectionHeading:
    """A section heading, corresponding to the HTML tags , , , , , or .

Attributes:
    type: Type of the block, always 'heading'
    text: Text of the block
    size: Relative size of the text font; 1-6, 1 is the largest, 6 is the smallest"""
    text: str = ''

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'text': self.text}
