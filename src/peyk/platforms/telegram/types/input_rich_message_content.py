from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputRichMessageContent:
    """Represents the content of a rich message to be sent as the result of an inline query.

Attributes:
    rich_message: The message to be sent"""
    rich_message: Optional[InputRichMessage] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return self.rich_message.to_dict() if self.rich_message is not None else {}

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['InputRichMessageContent']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['InputRichMessageContent']``).\n        "
        if data is None:
            return None
        return cls(rich_message=InputRichMessage.from_dict(data.get('rich_message')) if 'rich_message' in data else InputRichMessage.from_dict(data))
