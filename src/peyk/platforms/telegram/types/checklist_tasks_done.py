from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChecklistTasksDone:
    """Describes a service message about checklist tasks marked as done or not done.

Attributes:
    checklist_message: Message containing the checklist whose tasks were marked as done or not done. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply.
    marked_as_done_task_ids: Identifiers of the tasks that were marked as done
    marked_as_not_done_task_ids: Identifiers of the tasks that were marked as not done"""
    checklist_message: Optional[Message] = None
    tasks: Optional[List[ChecklistTask]] = None
    completed_tasks: Optional[List[ChecklistTask]] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChecklistTasksDone']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ChecklistTasksDone']``).\n        "
        if data is None:
            return None
        return cls(checklist_message=Message.from_dict(data.get('checklist_message')), tasks=[ChecklistTask.from_dict(t) for t in data.get('tasks', [])] if data.get('tasks') else None, completed_tasks=[ChecklistTask.from_dict(t) for t in data.get('completed_tasks', [])] if data.get('completed_tasks') else None)
