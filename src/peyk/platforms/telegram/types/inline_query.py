from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from peyk.bot.base import Bot
    from ..models import InlineQueryResult

@dataclass
class InlineQuery:
    """This object represents an incoming inline query. When the user sends an empty query, your bot could return some default or trending results.

Attributes:
    id: Unique identifier for this query
    from: Sender
    query: Text of the query (up to 256 characters)
    offset: Offset of the results to be returned, can be controlled by the bot
    chat_type: Type of the chat from which the inline query was sent. Can be either 'sender' for a private chat with the inline query sender, 'private', 'group', 'supergroup', or 'channel'. The chat type should be always known for requests sent from official clients and most third-party clients, unless the request was sent from a secret chat.
    location: Sender location, only for bots that request user location"""
    id: str
    from_: Optional[User] = None
    query: str = ''
    offset: str = ''
    chat_type: Optional[str] = None
    location: Optional[Location] = None
    bot: Optional['Bot[object]'] = field(default=None, repr=False, compare=False)

    async def answer(self, results: Sequence['InlineQueryResult | Mapping[str, object]'], *, cache_time: int | None=None, is_personal: bool | None=None, next_offset: str | None=None, button: object | None=None) -> bool:
        """Answer this inline query through the bot injected by the dispatcher."""
        if self.bot is None:
            raise RuntimeError('InlineQuery is not bound to a Bot')
        return await self.bot.client.answer_inline_query(self.id, results, cache_time=cache_time, is_personal=is_personal, next_offset=next_offset, button=button)

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['InlineQuery']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['InlineQuery']``).\n        "
        if data is None:
            return None
        return cls(id=data.get('id', ''), from_=User.from_dict(data.get('from')), query=data.get('query', ''), offset=data.get('offset', ''), chat_type=data.get('chat_type'), location=Location.from_dict(data.get('location')))
