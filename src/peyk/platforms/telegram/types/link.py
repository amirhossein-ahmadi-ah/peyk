from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class Link:
    """Represents an HTTP link.

Attributes:
    url: URL of the link"""
    url: str

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Link']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(url=data.get('url', ''))
