from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChosenInlineResult:
    """Represents a result of an inline query that was chosen by the user and sent to their chat partner.
Note: It is necessary to enable inline feedback via @BotFather in order to receive these objects in updates.

Attributes:
    result_id: The unique identifier for the result that was chosen
    from: The user that chose the result
    query: The query that was used to obtain the result
    location: Sender location, only for bots that require user location
    inline_message_id: Identifier of the sent inline message. Available only if there is an inline keyboard attached to the message. Will be also received in callback queries and can be used to edit the message."""
    result_id: str
    from_: Optional[User] = None
    location: Optional[Location] = None
    inline_message_id: Optional[str] = None
    query: str = ''

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChosenInlineResult']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ChosenInlineResult']``).\n        "
        if data is None:
            return None
        return cls(result_id=data.get('result_id', ''), from_=User.from_dict(data.get('from')), location=Location.from_dict(data.get('location')), inline_message_id=data.get('inline_message_id'), query=data.get('query', ''))
