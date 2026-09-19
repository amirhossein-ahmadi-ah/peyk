from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class TransactionPartnerUser:
    """Describes a transaction with a user.

Attributes:
    type: Type of the transaction partner, always 'user'
    transaction_type: Type of the transaction, currently one of 'invoice_payment' for payments via invoices, 'paid_media_payment' for payments for paid media, 'gift_purchase' for gifts sent by the bot, 'premium_purchase' for Telegram Premium subscriptions gifted by the bot, 'business_account_transfer' for direct transfers from managed business accounts
    user: Information about the user
    affiliate: Information about the affiliate that received a commission via this transaction. Can be available only for 'invoice_payment' and 'paid_media_payment' transactions.
    invoice_payload: Bot-specified invoice payload. Can be available only for 'invoice_payment' transactions.
    subscription_period: The duration of the paid subscription. Can be available only for 'invoice_payment' transactions.
    paid_media: Information about the paid media bought by the user; for 'paid_media_payment' transactions only
    paid_media_payload: Bot-specified paid media payload. Can be available only for 'paid_media_payment' transactions.
    gift: The gift sent to the user by the bot; for 'gift_purchase' transactions only
    premium_subscription_duration: Number of months the gifted Telegram Premium subscription will be active for; for 'premium_purchase' transactions only"""
    transaction_type: str
    user: User
    type: str = 'user'
    affiliate: Optional[AffiliateInfo] = None
    invoice_payload: Optional[str] = None
    subscription_period: Optional[int] = None
    paid_media: Optional[List[PaidMedia]] = None
    paid_media_payload: Optional[str] = None
    gift: Optional[Gift] = None
    premium_subscription_duration: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['TransactionPartnerUser']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['TransactionPartnerUser']``).\n        "
        if data is None:
            return None
        return cls(transaction_type=_parse_api_value('String', data.get('transaction_type')), user=_parse_api_value('User', data.get('user')), type=_parse_api_value('String', data.get('type')), affiliate=_parse_api_value('AffiliateInfo', data.get('affiliate')), invoice_payload=_parse_api_value('String', data.get('invoice_payload')), subscription_period=_parse_api_value('Integer', data.get('subscription_period')), paid_media=_parse_api_value('Array of PaidMedia', data.get('paid_media')), paid_media_payload=_parse_api_value('String', data.get('paid_media_payload')), gift=_parse_api_value('Gift', data.get('gift')), premium_subscription_duration=_parse_api_value('Integer', data.get('premium_subscription_duration')))
