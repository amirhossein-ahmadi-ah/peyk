from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class TransactionPartnerAffiliateProgram:
    """Describes the affiliate program that issued the affiliate commission received via this transaction.

Attributes:
    type: Type of the transaction partner, always 'affiliate_program'
    commission_per_mille: The number of Telegram Stars received by the bot for each 1000 Telegram Stars received by the affiliate program sponsor from referred users
    sponsor_user: Information about the bot that sponsored the affiliate program"""
    type: str = 'affiliate_program'
    commission_per_mille: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['TransactionPartnerAffiliateProgram']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['TransactionPartnerAffiliateProgram']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'affiliate_program'), commission_per_mille=data.get('commission_per_mille', 0))
