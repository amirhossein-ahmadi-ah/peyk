from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BotSubscriptionUpdated:
    """This object contains information about changes to a user payment subscription toward the current bot.

Attributes:
    user: User who subscribed for payments toward the bot
    invoice_payload: Bot-specified invoice payload
    state: The new state of the subscription. Currently, it can be one of 'canceled' if the user canceled the subscription, 'active' if the user re-enabled a previously canceled subscription, or 'failed' if payment for the subscription failed."""
    user: User
    invoice_payload: str
    state: str

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BotSubscriptionUpdated']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BotSubscriptionUpdated']``).\n        "
        if data is None:
            return None
        return cls(user=_parse_api_value('User', data.get('user')), invoice_payload=_parse_api_value('String', data.get('invoice_payload')), state=_parse_api_value('String', data.get('state')))
