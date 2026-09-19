from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class CopyTextButton:
    """An inline button that copies the specified text."""
    text: str

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['CopyTextButton']:
        """Parse raw Bale data into ``CopyTextButton``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[CopyTextButton]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(text=data.get('text', ''))
