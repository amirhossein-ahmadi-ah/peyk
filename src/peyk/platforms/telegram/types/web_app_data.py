from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class WebAppData:
    """Describes data sent from a Web App to the bot.

Attributes:
    data: The data. Be aware that a bad client can send arbitrary data in this field.
    button_text: Text of the web_app keyboard button from which the Web App was opened. Be aware that a bad client can send arbitrary data in this field."""
    data: str
    button_text: str

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['WebAppData']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['WebAppData']``).\n        "
        if data is None:
            return None
        return cls(data=_parse_api_value('String', data.get('data')), button_text=_parse_api_value('String', data.get('button_text')))
