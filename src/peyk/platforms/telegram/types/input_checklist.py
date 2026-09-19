from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputChecklist:
    """Describes a checklist to create.

Attributes:
    title: Title of the checklist; 1-255 characters after entities parsing
    tasks: List of 1-30 tasks in the checklist
    parse_mode: Mode for parsing entities in the title. See formatting options for more details.
    title_entities: List of special entities that appear in the title, which can be specified instead of parse_mode. Currently, only bold, italic, underline, strikethrough, spoiler, custom_emoji, and date_time entities are allowed.
    others_can_add_tasks: Pass True if other users can add tasks to the checklist
    others_can_mark_tasks_as_done: Pass True if other users can mark tasks as done or not done in the checklist"""
    title: str
    tasks: List[InputChecklistTask]
    others_can_add_tasks: Optional[bool] = None
    others_can_mark_tasks_as_done: Optional[bool] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'title': self.title, 'tasks': [t.to_dict() for t in self.tasks]}
        if self.others_can_add_tasks is not None:
            body['others_can_add_tasks'] = self.others_can_add_tasks
        if self.others_can_mark_tasks_as_done is not None:
            body['others_can_mark_tasks_as_done'] = self.others_can_mark_tasks_as_done
        return body
