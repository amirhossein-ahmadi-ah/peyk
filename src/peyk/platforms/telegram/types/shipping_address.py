from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ShippingAddress:
    """This object represents a shipping address.

Attributes:
    country_code: Two-letter ISO 3166-1 alpha-2 country code
    state: State, if applicable
    city: City
    street_line1: First line for the address
    street_line2: Second line for the address
    post_code: Address post code"""
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ShippingAddress']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ShippingAddress']``).\n        "
        if data is None:
            return None
        return cls(country_code=_parse_api_value('String', data.get('country_code')), state=_parse_api_value('String', data.get('state')), city=_parse_api_value('String', data.get('city')), street_line1=_parse_api_value('String', data.get('street_line1')), street_line2=_parse_api_value('String', data.get('street_line2')), post_code=_parse_api_value('String', data.get('post_code')))
