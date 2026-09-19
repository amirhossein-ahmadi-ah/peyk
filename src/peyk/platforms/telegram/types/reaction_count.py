from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ReactionCount:
    """Represents a reaction added to a message along with the number of times it was added.

Attributes:
    type: Type of the reaction
    total_count: Number of times the reaction was added"""
    type: ReactionType
    total_count: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ReactionCount']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ReactionCount']``).\n        "
        if data is None:
            return None
        return cls(type=parse_reaction_type(data.get('type', {})), total_count=data.get('total_count', 0))
