from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichBlockListItem:
    """An item of a list.

Attributes:
    label: Label of the item
    blocks: The content of the item
    has_checkbox: True, if the item has a checkbox
    is_checked: True, if the item has a checked checkbox
    value: For ordered lists, the numeric value of the item label
    type: For ordered lists, the type of the item label; must be one of 'a' for lowercase letters, 'A' for uppercase letters, 'i' for lowercase Roman numerals, 'I' for uppercase Roman numerals, or '1' for decimal numbers"""
    text: str = ''

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(text=data.get('text', '')) if data else None
