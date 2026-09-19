from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class VideoChatParticipantsInvited:
    """This object represents a service message about new members invited to a video chat.

Attributes:
    users: New members that were invited to the video chat"""
    users: Optional[List[User]] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['VideoChatParticipantsInvited']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['VideoChatParticipantsInvited']``).\n        "
        if data is None:
            return None
        return cls(users=[User.from_dict(u) for u in data.get('users', [])] if data.get('users') else None)
