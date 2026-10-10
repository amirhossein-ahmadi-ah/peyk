from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class PollOption:
    """Represent one option of a Bale poll.

The Bale documentation does not describe polls, but the live API returns
them; the field set mirrors what the server sends (``persistent_id`` is the
stable option identifier, unlike the option's position)."""
    persistent_id: str = ''
    text: str = ''
    voter_count: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PollOption']:
        """Parse raw Bale data into ``PollOption``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[PollOption]: Parsed object or ``None``."""
        if data is None:
            return None
        return cls(persistent_id=data.get('persistent_id', ''), text=data.get('text', ''), voter_count=data.get('voter_count', 0))

    @classmethod
    def list_from_result(cls, data: Optional[List[dict]]) -> Optional[List['PollOption']]:
        """Parse a raw option list; ``None`` stays ``None``."""
        if data is None:
            return None
        return [cls.from_dict(item) for item in data]
