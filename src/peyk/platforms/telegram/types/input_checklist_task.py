from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputChecklistTask:
    """Describes a task to add to a checklist.

Attributes:
    id: Unique identifier of the task; must be positive and unique among all task identifiers currently present in the checklist
    text: Text of the task; 1-100 characters after entities parsing
    parse_mode: Mode for parsing entities in the text. See formatting options for more details.
    text_entities: List of special entities that appear in the text, which can be specified instead of parse_mode. Currently, only bold, italic, underline, strikethrough, spoiler, custom_emoji, and date_time entities are allowed."""
    text: str
    parse_mode: Optional[str] = None
    text_entities: Optional[List[MessageEntity]] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'text': self.text}
        if self.parse_mode is not None:
            body['parse_mode'] = self.parse_mode
        if self.text_entities is not None:
            body['text_entities'] = [e.to_dict() for e in self.text_entities]
        return body
