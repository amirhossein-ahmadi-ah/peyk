from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputRichBlockPreformatted:
    """A preformatted text block, corresponding to the nested HTML tags  and .

Attributes:
    type: Type of the block, always 'pre'
    text: Text of the block
    language: The programming language of the text"""
    text: str = ''
    language: str = ''

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'text': self.text, 'language': self.language}
