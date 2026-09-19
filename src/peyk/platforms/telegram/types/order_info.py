from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class OrderInfo:
    """This object represents information about an order.

Attributes:
    name: User name
    phone_number: User's phone number
    email: User email
    shipping_address: User shipping address"""
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    shipping_address: Optional[ShippingAddress] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['OrderInfo']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['OrderInfo']``).\n        "
        if data is None:
            return None
        return cls(name=_parse_api_value('String', data.get('name')), phone_number=_parse_api_value('String', data.get('phone_number')), email=_parse_api_value('String', data.get('email')), shipping_address=_parse_api_value('ShippingAddress', data.get('shipping_address')))
