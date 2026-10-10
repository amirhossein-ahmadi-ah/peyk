from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional
from .poll_option import PollOption

@dataclass
class Poll:
    """Represent a Bale poll (undocumented, but present in the live API).

A poll arrives either inside ``Message.poll`` or on its own as the ``poll``
field of an ``Update``. The field set mirrors what the server sends."""
    id: Any = None
    question: str = ''
    options: Optional[List[PollOption]] = None
    total_voter_count: int = 0
    is_closed: bool = False
    is_anonymous: bool = True
    type: str = ''
    allows_multiple_answers: bool = False
    allows_revoting: bool = False
    members_only: bool = False

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Poll']:
        """Parse raw Bale data into ``Poll``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[Poll]: Parsed object or ``None``."""
        if data is None:
            return None
        return cls(id=data.get('id'), question=data.get('question', ''), options=PollOption.list_from_result(data.get('options')), total_voter_count=data.get('total_voter_count', 0), is_closed=data.get('is_closed', False), is_anonymous=data.get('is_anonymous', True), type=data.get('type', ''), allows_multiple_answers=data.get('allows_multiple_answers', False), allows_revoting=data.get('allows_revoting', False), members_only=data.get('members_only', False))
