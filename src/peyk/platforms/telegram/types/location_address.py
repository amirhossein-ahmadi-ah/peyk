from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class LocationAddress:
    """Describes the physical address of a location.

Attributes:
    country_code: The two-letter ISO 3166-1 alpha-2 country code of the country where the location is located
    state: State of the location
    city: City of the location
    street: Street address of the location"""
    country_code: str
    state: Optional[str] = None
    city: Optional[str] = None
    street_line1: Optional[str] = None
    street_line2: Optional[str] = None
    post_code: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['LocationAddress']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['LocationAddress']``).\n        "
        if data is None:
            return None
        return cls(country_code=data.get('country_code', ''), state=data.get('state'), city=data.get('city'), street_line1=data.get('street_line1'), street_line2=data.get('street_line2'), post_code=data.get('post_code'))
