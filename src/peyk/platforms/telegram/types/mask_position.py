from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class MaskPosition:
    """This object describes the position on faces where a mask should be placed by default.

Attributes:
    point: The part of the face relative to which the mask should be placed. One of 'forehead', 'eyes', 'mouth', or 'chin'.
    x_shift: Shift by X-axis measured in widths of the mask scaled to the face size, from left to right. For example, choosing -1.0 will place mask just to the left of the default mask position.
    y_shift: Shift by Y-axis measured in heights of the mask scaled to the face size, from top to bottom. For example, 1.0 will place the mask just below the default mask position.
    scale: Mask scaling coefficient. For example, 2.0 means double size."""
    point: str
    x_shift: float
    y_shift: float
    scale: float

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['MaskPosition']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['MaskPosition']``).\n        "
        if data is None:
            return None
        return cls(point=data.get('point', ''), x_shift=data.get('x_shift', 0.0), y_shift=data.get('y_shift', 0.0), scale=data.get('scale', 0.0))

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'point': self.point, 'x_shift': self.x_shift, 'y_shift': self.y_shift, 'scale': self.scale}
