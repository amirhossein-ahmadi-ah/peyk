from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class Game:
    """This object represents a game. Use BotFather to create and edit games, their short names will act as unique identifiers.

Attributes:
    title: Title of the game
    description: Description of the game
    photo: Photo that will be displayed in the game message in chats
    text: Brief description of the game or high scores included in the game message. Can be automatically edited to include current high scores for the game when the bot calls setGameScore, or manually edited using editMessageText. 0-4096 characters.
    text_entities: Special entities that appear in text, such as usernames, URLs, bot commands, etc.
    animation: Animation that will be displayed in the game message in chats. Upload via BotFather."""
    title: str
    description: str
    photo: List[PhotoSize]
    text: Optional[str] = None
    text_entities: Optional[List[MessageEntity]] = None
    animation: Optional[Animation] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Game']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Game']``).\n        "
        if data is None:
            return None
        return cls(title=_parse_api_value('String', data.get('title')), description=_parse_api_value('String', data.get('description')), photo=_parse_api_value('Array of PhotoSize', data.get('photo')), text=_parse_api_value('String', data.get('text')), text_entities=_parse_api_value('Array of MessageEntity', data.get('text_entities')), animation=_parse_api_value('Animation', data.get('animation')))
