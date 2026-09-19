from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class CallbackQuery:
    """This object represents an incoming callback query from a callback button in an inline keyboard. If the button that originated the query was attached to a message sent by the bot, the field message will be present. If the button was attached to a message sent via the bot (in inline mode), the field inline_message_id will be present. Exactly one of the fields data or game_short_name will be present.
NOTE: After the user presses a callback button, Telegram clients will display a progress bar until you call answerCallbackQuery. It is, therefore, necessary to react by calling answerCallbackQuery even if no notification to the user is needed (e.g., without specifying any of the optional parameters).

Attributes:
    id: Unique identifier for this query
    from: Sender
    chat_instance: Global identifier, uniquely corresponding to the chat to which the message with the callback button was sent. Useful for high scores in games.
    message: Message sent by the bot with the callback button that originated the query
    inline_message_id: Identifier of the message sent via the bot in inline mode, that originated the query
    data: Data associated with the callback button. Be aware that the message originated the query can contain no callback buttons with this data.
    game_short_name: Short name of a Game to be returned, serves as the unique identifier for the game"""
    id: str = ''
    from_: Optional[User] = None
    message: Optional[MaybeInaccessibleMessage] = None
    inline_message_id: Optional[str] = None
    chat_instance: Optional[str] = None
    data: Optional[str] = None
    game_short_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['CallbackQuery']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['CallbackQuery']``).\n        "
        if data is None:
            return None
        return cls(id=data.get('id', ''), from_=User.from_dict(data.get('from')), message=parse_maybe_inaccessible_message(data.get('message')), inline_message_id=data.get('inline_message_id'), chat_instance=data.get('chat_instance'), data=data.get('data'), game_short_name=data.get('game_short_name'))
