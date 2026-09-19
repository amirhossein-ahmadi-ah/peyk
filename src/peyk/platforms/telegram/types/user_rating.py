from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class UserRating:
    """This object describes the rating of a user based on their Telegram Star spendings.

Attributes:
    level: Current level of the user, indicating their reliability when purchasing digital goods and services. A higher level suggests a more trustworthy customer; a negative level is likely reason for concern.
    rating: Numerical value of the user's rating; the higher the rating, the better
    current_level_rating: The rating value required to get the current level
    next_level_rating: The rating value required to get to the next level; omitted if the maximum level was reached"""
    rating: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['UserRating']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['UserRating']``).\n        "
        if data is None:
            return None
        return cls(rating=data.get('rating', 0))
