from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class Checklist:
    """Describes a checklist.

Attributes:
    title: Title of the checklist
    tasks: List of tasks in the checklist
    title_entities: Special entities that appear in the checklist title
    others_can_add_tasks: True, if users other than the creator of the list can add tasks to the list
    others_can_mark_tasks_as_done: True, if users other than the creator of the list can mark tasks as done or not done"""
    title: str = ''
    tasks: Optional[List[ChecklistTask]] = None
    others_can_add_tasks: Optional[bool] = None
    others_can_mark_tasks_as_done: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Checklist']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Checklist']``).\n        "
        if data is None:
            return None
        return cls(title=data.get('title', ''), tasks=[ChecklistTask.from_dict(t) for t in data.get('tasks', [])] if data.get('tasks') else None, others_can_add_tasks=data.get('others_can_add_tasks'), others_can_mark_tasks_as_done=data.get('others_can_mark_tasks_as_done'))
