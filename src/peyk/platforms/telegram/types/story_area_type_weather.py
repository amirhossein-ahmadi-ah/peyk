from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class StoryAreaTypeWeather:
    """Describes a story area containing weather information. Currently, a story can have up to 3 weather areas.

Attributes:
    type: Type of the area, always 'weather'
    temperature: Temperature, in degree Celsius
    emoji: Emoji representing the weather
    background_color: A color of the area background in the ARGB format"""
    temperature: float
    emoji: str
    background_color: int
    type: str = 'weather'

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['StoryAreaTypeWeather']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['StoryAreaTypeWeather']``).\n        "
        if data is None:
            return None
        return cls(temperature=_parse_api_value('Float', data.get('temperature')), emoji=_parse_api_value('String', data.get('emoji')), background_color=_parse_api_value('Integer', data.get('background_color')), type=_parse_api_value('String', data.get('type')))
