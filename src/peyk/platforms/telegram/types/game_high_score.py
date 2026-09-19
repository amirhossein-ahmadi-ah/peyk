from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class GameHighScore:
    """This object represents one row of the high scores table for a game.
And that's about all we've got for now.
If you've got any questions, please check out our Bot FAQ

Attributes:
    position: Position in high score table for the game
    user: User
    score: Score"""
    position: int
    user: User
    score: int

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['GameHighScore']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['GameHighScore']``).\n        "
        if data is None:
            return None
        return cls(position=_parse_api_value('Integer', data.get('position')), user=_parse_api_value('User', data.get('user')), score=_parse_api_value('Integer', data.get('score')))
