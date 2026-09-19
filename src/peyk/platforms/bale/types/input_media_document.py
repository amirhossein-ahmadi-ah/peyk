from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from .media_input import MediaInput

@dataclass(frozen=True)
class InputMediaDocument:
    """Represent an outgoing Bale ``InputMediaDocument`` item."""
    media: MediaInput
    caption: Optional[str] = None
