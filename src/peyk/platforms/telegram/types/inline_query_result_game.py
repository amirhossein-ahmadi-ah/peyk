from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InlineQueryResultGame:
    """Represents a Game.

Attributes:
    type: Type of the result, must be game
    id: Unique identifier for this result, 1-64 bytes
    game_short_name: Short name of the game
    reply_markup: Inline keyboard attached to the message"""
    id: str
    game_short_name: str
    type: str = 'game'
    reply_markup: Optional[Union[InlineKeyboardMarkup, Mapping[str, object]]] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': self.type, 'id': self.id, 'game_short_name': self.game_short_name}
        markup = _serialize_inline_markup(self.reply_markup)
        if markup is not None:
            body['reply_markup'] = markup
        return body
