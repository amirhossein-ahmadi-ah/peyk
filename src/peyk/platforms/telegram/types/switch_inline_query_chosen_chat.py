from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class SwitchInlineQueryChosenChat:
    """This object represents an inline button that switches the current user to inline mode in a chosen chat, with an optional default inline query.

Attributes:
    query: The default inline query to be inserted in the input field. If left empty, only the bot's username will be inserted.
    allow_user_chats: True, if private chats with users can be chosen
    allow_bot_chats: True, if private chats with bots can be chosen
    allow_group_chats: True, if group and supergroup chats can be chosen
    allow_channel_chats: True, if channel chats can be chosen"""
    query: Optional[str] = None
    allow_user_chats: Optional[bool] = None
    allow_bot_chats: Optional[bool] = None
    allow_group_chats: Optional[bool] = None
    allow_channel_chats: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['SwitchInlineQueryChosenChat']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['SwitchInlineQueryChosenChat']``).\n        "
        if data is None:
            return None
        return cls(query=data.get('query'), allow_user_chats=data.get('allow_user_chats'), allow_bot_chats=data.get('allow_bot_chats'), allow_group_chats=data.get('allow_group_chats'), allow_channel_chats=data.get('allow_channel_chats'))

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {}
        if self.query is not None:
            body['query'] = self.query
        if self.allow_user_chats is not None:
            body['allow_user_chats'] = self.allow_user_chats
        if self.allow_bot_chats is not None:
            body['allow_bot_chats'] = self.allow_bot_chats
        if self.allow_group_chats is not None:
            body['allow_group_chats'] = self.allow_group_chats
        if self.allow_channel_chats is not None:
            body['allow_channel_chats'] = self.allow_channel_chats
        return body
