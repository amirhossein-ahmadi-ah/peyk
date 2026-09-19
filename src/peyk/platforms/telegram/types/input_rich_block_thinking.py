from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputRichBlockThinking:
    """A block with a 'Thinking…' placeholder, corresponding to the custom HTML tag . The block may be used only in sendRichMessageDraft, therefore it can't be received in messages. See https://t.me/addemoji/AIActions for examples of custom emoji that are recommended for usage in the block.

Attributes:
    type: Type of the block, always 'thinking'
    text: Text of the block. See https://t.me/addemoji/AIActions for examples of custom emoji that are recommended for usage in the block."""
    text: str = ''

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'text': self.text}
