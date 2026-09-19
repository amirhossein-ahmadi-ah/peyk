from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputMediaLink:
    """Represents an HTTP link to be sent.

Attributes:
    type: Type of the media, must be link
    url: HTTP URL of the link"""
    url: str

    def to_dict(self) -> Dict[str, object]:
        """Serialize this type to the Telegram API request shape.

Returns:
    A JSON-compatible mapping representing this value."""
        return {'type': 'link', 'url': self.url}
