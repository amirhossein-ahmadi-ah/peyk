from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class AffiliateInfo:
    """Contains information about the affiliate that received a commission via this transaction.

Attributes:
    commission_per_mille: The number of Telegram Stars received by the affiliate for each 1000 Telegram Stars received by the bot from referred users
    amount: Integer amount of Telegram Stars received by the affiliate from the transaction, rounded to 0; can be negative for refunds
    affiliate_user: The bot or the user that received an affiliate commission if it was received by a bot or a user
    affiliate_chat: The chat that received an affiliate commission if it was received by a chat
    nanostar_amount: The number of 1/1000000000 shares of Telegram Stars received by the affiliate; from -999999999 to 999999999; can be negative for refunds"""
    commission_per_mille: int = 0
    amount: int = 0
    nanostar_amount: Optional[int] = None
    currency: str = ''

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['AffiliateInfo']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['AffiliateInfo']``).\n        "
        if data is None:
            return None
        return cls(commission_per_mille=data.get('commission_per_mille', 0), amount=data.get('amount', 0), nanostar_amount=data.get('nanostar_amount'), currency=data.get('currency', ''))
