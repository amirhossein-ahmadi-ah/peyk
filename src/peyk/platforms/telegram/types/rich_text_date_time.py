from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichTextDateTime:
    """Formatted date and time.

Attributes:
    type: Type of the rich text, always 'date_time'
    text: The text
    unix_time: The Unix time associated with the entity
    date_time_format: The string that defines the formatting of the date and time. See date-time entity formatting for more details."""
    text: str = ''
    type: str = 'date_time'

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(text=data.get('text', '')) if data else None
