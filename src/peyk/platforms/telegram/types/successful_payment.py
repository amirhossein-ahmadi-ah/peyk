from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class SuccessfulPayment:
    """This object contains basic information about a successful payment. Note that if the buyer initiates a chargeback with the relevant payment provider following this transaction, the funds may be debited from your balance. This is outside of Telegram's control.

Attributes:
    currency: Three-letter ISO 4217 currency code, or 'XTR' for payments in Telegram Stars
    total_amount: Total price in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).
    invoice_payload: Bot-specified invoice payload
    telegram_payment_charge_id: Telegram payment identifier
    provider_payment_charge_id: Provider payment identifier
    subscription_expiration_date: Expiration date of the subscription, in Unix time; for recurring payments only
    is_recurring: True, if the payment is a recurring payment for a subscription
    is_first_recurring: True, if the payment is the first payment for a subscription
    shipping_option_id: Identifier of the shipping option chosen by the user
    order_info: Order information provided by the user"""
    currency: str
    total_amount: int
    invoice_payload: str
    telegram_payment_charge_id: str
    provider_payment_charge_id: str
    subscription_expiration_date: Optional[int] = None
    is_recurring: Optional[bool] = None
    is_first_recurring: Optional[bool] = None
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['SuccessfulPayment']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['SuccessfulPayment']``).\n        "
        if data is None:
            return None
        return cls(currency=_parse_api_value('String', data.get('currency')), total_amount=_parse_api_value('Integer', data.get('total_amount')), invoice_payload=_parse_api_value('String', data.get('invoice_payload')), telegram_payment_charge_id=_parse_api_value('String', data.get('telegram_payment_charge_id')), provider_payment_charge_id=_parse_api_value('String', data.get('provider_payment_charge_id')), subscription_expiration_date=_parse_api_value('Integer', data.get('subscription_expiration_date')), is_recurring=_parse_api_value('True', data.get('is_recurring')), is_first_recurring=_parse_api_value('True', data.get('is_first_recurring')), shipping_option_id=_parse_api_value('String', data.get('shipping_option_id')), order_info=_parse_api_value('OrderInfo', data.get('order_info')))
