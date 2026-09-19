from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class UserProfileAudios:
    """This object represents the audios displayed on a user's profile.

Attributes:
    total_count: Total number of profile audios for the target user
    audios: Requested profile audios"""
    total_count: int = 0
    audios: Optional[List[Audio]] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['UserProfileAudios']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['UserProfileAudios']``).\n        "
        if data is None:
            return None
        return cls(total_count=data.get('total_count', 0), audios=[Audio.from_dict(a) for a in data.get('audios', [])] if data.get('audios') else None)
