from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class PollOptionAdded:
    """Describes a service message about an option added to a poll.

Attributes:
    option_persistent_id: Unique identifier of the added option
    option_text: Option text
    poll_message: Message containing the poll to which the option was added, if known. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply.
    option_text_entities: Special entities that appear in the option_text"""
    option: Optional[PollOption] = None
    voter_count: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PollOptionAdded']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['PollOptionAdded']``).\n        "
        if data is None:
            return None
        return cls(option=PollOption.from_dict(data.get('option')), voter_count=data.get('voter_count', 0))
