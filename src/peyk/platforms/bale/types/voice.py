from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class Voice:
    """A voice message.

    Per docs.bale.ai, the `Voice` type only carries `file_id` and
    `file_unique_id` -- unlike Telegram's richer voice type, Bale does
    not document `duration`, `mime_type`, or `file_size` here.
    """
    file_id: str
    file_unique_id: str

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Voice']:
        """Parse raw Bale data into ``Voice``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[Voice]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(file_id=data.get('file_id', ''), file_unique_id=data.get('file_unique_id', ''))
