from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class Gifts:
    """This object represent a list of gifts.

Attributes:
    gifts: The list of gifts"""
    gifts: List[Gift]

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Gifts']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Gifts']``).\n        "
        if data is None:
            return None
        return cls(gifts=_parse_api_value('Array of Gift', data.get('gifts')))
