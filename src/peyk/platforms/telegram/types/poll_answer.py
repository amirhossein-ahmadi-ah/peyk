from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .chat import Chat
from .user import User

@dataclass
class PollAnswer:
    """This object represents an answer of a user in a non-anonymous poll.

Attributes:
    poll_id: Unique poll identifier
    option_ids: 0-based identifiers of chosen answer options. May be empty if the vote was retracted.
    option_persistent_ids: Persistent identifiers of the chosen answer options. May be empty if the vote was retracted.
    voter_chat: The chat that changed the answer to the poll, if the voter is anonymous
    user: The user that changed the answer to the poll, if the voter isn't anonymous"""
    poll_id: str
    voter_chat: Optional[Chat] = None
    user: Optional[User] = None
    option_ids: Optional[List[int]] = None
    option_persistent_ids: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PollAnswer']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(poll_id=data.get('poll_id', ''), voter_chat=Chat.from_dict(data.get('voter_chat')), user=User.from_dict(data.get('user')), option_ids=data.get('option_ids'), option_persistent_ids=data.get('option_persistent_ids'))
