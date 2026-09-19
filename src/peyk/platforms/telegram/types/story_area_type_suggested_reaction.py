from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class StoryAreaTypeSuggestedReaction:
    """Describes a story area pointing to a suggested reaction. Currently, a story can have up to 5 suggested reaction areas.

Attributes:
    type: Type of the area, always 'suggested_reaction'
    reaction_type: Type of the reaction
    is_dark: Pass True if the reaction area has a dark background
    is_flipped: Pass True if reaction area corner is flipped"""
    reaction_type: ReactionType
    type: str = 'suggested_reaction'
    is_dark: Optional[bool] = None
    is_flipped: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['StoryAreaTypeSuggestedReaction']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['StoryAreaTypeSuggestedReaction']``).\n        "
        if data is None:
            return None
        return cls(reaction_type=_parse_api_value('ReactionType', data.get('reaction_type')), type=_parse_api_value('String', data.get('type')), is_dark=_parse_api_value('Boolean', data.get('is_dark')), is_flipped=_parse_api_value('Boolean', data.get('is_flipped')))
