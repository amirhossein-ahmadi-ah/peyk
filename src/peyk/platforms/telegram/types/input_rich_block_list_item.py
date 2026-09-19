from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputRichBlockListItem:
    """An item of a list to be sent.

Attributes:
    blocks: The content of the item
    has_checkbox: Pass True if the item has a checkbox
    is_checked: Pass True if the item has a checked checkbox
    value: For ordered lists, the numeric value of the item label
    type: For ordered lists, the type of the item label; must be one of 'a' for lowercase letters, 'A' for uppercase letters, 'i' for lowercase Roman numerals, 'I' for uppercase Roman numerals, or '1' for decimal numbers"""
    text: str = ''
    parse_mode: Optional[str] = None
    text_entities: Optional[List[MessageEntity]] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'text': self.text}
        if self.parse_mode is not None:
            body['parse_mode'] = self.parse_mode
        if self.text_entities is not None:
            body['text_entities'] = [e.to_dict() for e in self.text_entities]
        return body
