from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChecklistTask:
    """Describes a task in a checklist.

Attributes:
    id: Unique identifier of the task
    text: Text of the task
    text_entities: Special entities that appear in the task text
    completed_by_user: User that completed the task; omitted if the task wasn't completed by a user
    completed_by_chat: Chat that completed the task; omitted if the task wasn't completed by a chat
    completion_date: Point in time (Unix timestamp) when the task was completed; 0 if the task wasn't completed"""
    id: int = 0
    text: str = ''
    text_entities: Optional[List[MessageEntity]] = None
    completed_by_user: Optional[User] = None
    completion_date: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChecklistTask']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ChecklistTask']``).\n        "
        if data is None:
            return None
        return cls(id=data.get('id', 0), text=data.get('text', ''), text_entities=MessageEntity.list_from(data.get('text_entities')), completed_by_user=User.from_dict(data.get('completed_by_user')), completion_date=data.get('completion_date'))
