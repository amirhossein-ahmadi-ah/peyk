from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ProximityAlertTriggered:
    """This object represents the content of a service message, sent whenever a user in the chat triggers a proximity alert set by another user.

Attributes:
    traveler: User that triggered the alert
    watcher: User that set the alert
    distance: The distance between the users"""
    traveler: Optional[User] = None
    watcher: Optional[User] = None
    distance: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ProximityAlertTriggered']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ProximityAlertTriggered']``).\n        "
        if data is None:
            return None
        return cls(traveler=User.from_dict(data.get('traveler')), watcher=User.from_dict(data.get('watcher')), distance=data.get('distance', 0))
