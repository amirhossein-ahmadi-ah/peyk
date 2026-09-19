from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class StarTransaction:
    """Describes a Telegram Star transaction. Note that if the buyer initiates a chargeback with the payment provider from whom they acquired Stars (e.g., Apple, Google) following this transaction, the refunded Stars will be deducted from the bot's balance. This is outside of Telegram's control.

Attributes:
    id: Unique identifier of the transaction. Coincides with the identifier of the original transaction for refund transactions. Coincides with SuccessfulPayment.telegram_payment_charge_id for successful incoming payments from users.
    amount: Integer amount of Telegram Stars transferred by the transaction
    date: Date the transaction was created in Unix time
    nanostar_amount: The number of 1/1000000000 shares of Telegram Stars transferred by the transaction; from 0 to 999999999
    source: Source of an incoming transaction (e.g., a user purchasing goods or services, Fragment refunding a failed withdrawal). Only for incoming transactions.
    receiver: Receiver of an outgoing transaction (e.g., a user for a purchase refund, Fragment for a withdrawal). Only for outgoing transactions."""
    id: str
    amount: int
    date: int
    nanostar_amount: Optional[int] = None
    source: Optional[TransactionPartner] = None
    receiver: Optional[TransactionPartner] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['StarTransaction']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['StarTransaction']``).\n        "
        if data is None:
            return None
        return cls(id=_parse_api_value('String', data.get('id')), amount=_parse_api_value('Integer', data.get('amount')), date=_parse_api_value('Integer', data.get('date')), nanostar_amount=_parse_api_value('Integer', data.get('nanostar_amount')), source=_parse_api_value('TransactionPartner', data.get('source')), receiver=_parse_api_value('TransactionPartner', data.get('receiver')))
