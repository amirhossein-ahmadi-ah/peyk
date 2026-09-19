from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChecklistTasksAdded:
    """Describes a service message about tasks added to a checklist.

Attributes:
    tasks: List of tasks added to the checklist
    checklist_message: Message containing the checklist to which the tasks were added. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply."""
    checklist_message: Optional[Message] = None
    tasks: Optional[List[ChecklistTask]] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChecklistTasksAdded']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ChecklistTasksAdded']``).\n        "
        if data is None:
            return None
        return cls(checklist_message=Message.from_dict(data.get('checklist_message')), tasks=[ChecklistTask.from_dict(t) for t in data.get('tasks', [])] if data.get('tasks') else None)
