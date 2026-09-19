from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class MessageReactionUpdated:
    """This object represents a change of a reaction on a message performed by a user.

Attributes:
    chat: The chat containing the message the user reacted to
    message_id: Unique identifier of the message inside the chat
    date: Date of the change in Unix time
    old_reaction: Previous list of reaction types that were set by the user
    new_reaction: New list of reaction types that have been set by the user
    user: The user that changed the reaction, if the user isn't anonymous
    actor_chat: The chat on behalf of which the reaction was changed, if the user is anonymous"""
    chat: Chat
    message_id: int
    date: int
    old_reaction: Optional[List[ReactionType]] = None
    new_reaction: Optional[List[ReactionType]] = None
    user: Optional[User] = None
    actor_chat: Optional[Chat] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['MessageReactionUpdated']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['MessageReactionUpdated']``).\n        "
        if data is None:
            return None
        return cls(chat=Chat.from_dict(data.get('chat', {})), message_id=data.get('message_id', 0), date=data.get('date', 0), old_reaction=[parse_reaction_type(r) for r in data.get('old_reaction', [])] if data.get('old_reaction') else None, new_reaction=[parse_reaction_type(r) for r in data.get('new_reaction', [])] if data.get('new_reaction') else None, user=User.from_dict(data.get('user')), actor_chat=Chat.from_dict(data.get('actor_chat')))
