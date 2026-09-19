from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class UniqueGiftColors:
    """This object contains information about the color scheme for a user's name, message replies and link previews based on a unique gift.

Attributes:
    model_custom_emoji_id: Custom emoji identifier of the unique gift's model
    symbol_custom_emoji_id: Custom emoji identifier of the unique gift's symbol
    light_theme_main_color: Main color used in light themes; RGB format
    light_theme_other_colors: List of 1-3 additional colors used in light themes; RGB format
    dark_theme_main_color: Main color used in dark themes; RGB format
    dark_theme_other_colors: List of 1-3 additional colors used in dark themes; RGB format"""
    center_color: int = 0
    edge_color: int = 0
    symbol_color: int = 0
    text_color: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['UniqueGiftColors']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['UniqueGiftColors']``).\n        "
        if data is None:
            return None
        return cls(center_color=data.get('center_color', 0), edge_color=data.get('edge_color', 0), symbol_color=data.get('symbol_color', 0), text_color=data.get('text_color', 0))
