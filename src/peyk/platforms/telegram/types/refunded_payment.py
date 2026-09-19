from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RefundedPayment:
    """This object contains basic information about a refunded payment.

Attributes:
    currency: Three-letter ISO 4217 currency code, or 'XTR' for payments in Telegram Stars. Currently, always 'XTR'.
    total_amount: Total refunded price in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45, total_amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).
    invoice_payload: Bot-specified invoice payload
    telegram_payment_charge_id: Telegram payment identifier
    provider_payment_charge_id: Provider payment identifier"""
    currency: str
    total_amount: int
    invoice_payload: str
    telegram_payment_charge_id: str
    provider_payment_charge_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['RefundedPayment']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['RefundedPayment']``).\n        "
        if data is None:
            return None
        return cls(currency=_parse_api_value('String', data.get('currency')), total_amount=_parse_api_value('Integer', data.get('total_amount')), invoice_payload=_parse_api_value('String', data.get('invoice_payload')), telegram_payment_charge_id=_parse_api_value('String', data.get('telegram_payment_charge_id')), provider_payment_charge_id=_parse_api_value('String', data.get('provider_payment_charge_id')))
