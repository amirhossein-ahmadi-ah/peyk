from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputProfilePhotoAnimated:
    """An animated profile photo in the MPEG4 format.

Attributes:
    type: Type of the profile photo, must be animated
    animation: The animated profile photo. Profile photos can't be reused and can only be uploaded as a new file, so you can pass 'attach://' if the photo was uploaded using multipart/form-data under . More information on Sending Files
    main_frame_timestamp: Timestamp in seconds of the frame that will be used as the static profile photo. Defaults to 0.0."""
    photo: object
    type: str = 'animated'
    main_frame_timestamp: Optional[float] = None

    def to_dict(self, photo_ref: str) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Args:
    photo_ref: Value used by this operation.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Args:\n            photo_ref: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': 'animated', 'photo': photo_ref}
        if self.main_frame_timestamp is not None:
            body['main_frame_timestamp'] = self.main_frame_timestamp
        return body
