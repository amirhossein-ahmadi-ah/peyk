from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichTextBotCommand:
    """A bot command.

Attributes:
    type: Type of the rich text, always 'bot_command'
    text: The text
    bot_command: The bot command"""
    text: str = ''
    type: str = 'bot_command'

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(text=data.get('text', '')) if data else None
