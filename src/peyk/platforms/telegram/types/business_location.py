from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BusinessLocation:
    """Contains information about the location of a Telegram Business account.

Attributes:
    address: Address of the business
    location: Location of the business"""
    address: str
    location: Optional[Location] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BusinessLocation']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BusinessLocation']``).\n        "
        if data is None:
            return None
        return cls(address=_parse_api_value('String', data.get('address')), location=_parse_api_value('Location', data.get('location')))
