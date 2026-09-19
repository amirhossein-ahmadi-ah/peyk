from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputProfilePhotoStatic:
    """A static profile photo in the .JPG format.

Attributes:
    type: Type of the profile photo, must be static
    photo: The static profile photo. Profile photos can't be reused and can only be uploaded as a new file, so you can pass 'attach://' if the photo was uploaded using multipart/form-data under . More information on Sending Files"""
    photo: object
    type: str = 'static'

    def to_dict(self, photo_ref: str) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Args:
    photo_ref: Value used by this operation.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Args:\n            photo_ref: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'type': 'static', 'photo': photo_ref}
