from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from .media_input import MediaInput

@dataclass(frozen=True)
class InputMediaPhoto:
    """Represent an outgoing Bale ``InputMediaPhoto`` item."""
    media: MediaInput
    caption: Optional[str] = None
