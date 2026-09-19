from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class Birthdate:
    """Describes the birthdate of a user.

Attributes:
    day: Day of the user's birth; 1-31
    month: Month of the user's birth; 1-12
    year: Year of the user's birth"""
    day: int
    month: int
    year: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Birthdate']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Birthdate']``).\n        "
        if data is None:
            return None
        return cls(day=data['day'], month=data['month'], year=data.get('year'))
