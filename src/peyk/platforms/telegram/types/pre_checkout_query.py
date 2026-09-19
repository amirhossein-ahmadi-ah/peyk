from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class PreCheckoutQuery:
    """This object contains information about an incoming pre-checkout query.

Attributes:
    id: Unique query identifier
    from: User who sent the query
    currency: Three-letter ISO 4217 currency code, or 'XTR' for payments in Telegram Stars
    total_amount: Total price in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).
    invoice_payload: Bot-specified invoice payload
    shipping_option_id: Identifier of the shipping option chosen by the user
    order_info: Order information provided by the user"""
    id: str
    from_: User
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PreCheckoutQuery']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['PreCheckoutQuery']``).\n        "
        if data is None:
            return None
        return cls(id=_parse_api_value('String', data.get('id')), from_=_parse_api_value('User', data.get('from')), currency=_parse_api_value('String', data.get('currency')), total_amount=_parse_api_value('Integer', data.get('total_amount')), invoice_payload=_parse_api_value('String', data.get('invoice_payload')), shipping_option_id=_parse_api_value('String', data.get('shipping_option_id')), order_info=_parse_api_value('OrderInfo', data.get('order_info')))
