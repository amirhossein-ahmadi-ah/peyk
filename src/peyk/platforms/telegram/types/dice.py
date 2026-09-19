from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class Dice:
    """This object represents an animated emoji that displays a random value.

Attributes:
    emoji: Emoji on which the dice throw animation is based
    value: Value of the dice, 1-6 for '', '' and '' base emoji, 1-5 for '' and '' base emoji, 1-64 for '' base emoji"""
    emoji: str
    value: int

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Dice']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(emoji=data.get('emoji', ''), value=data.get('value', 0))
