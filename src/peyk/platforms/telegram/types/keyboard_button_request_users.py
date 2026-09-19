from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class KeyboardButtonRequestUsers:
    """This object defines the criteria used to request suitable users. Information about the selected users will be shared with the bot when the corresponding button is pressed.

Attributes:
    request_id: Signed 32-bit identifier of the request that will be received back in the UsersShared object. Must be unique within the message.
    user_is_bot: Pass True to request bots, pass False to request regular users. If not specified, no additional restrictions are applied.
    user_is_premium: Pass True to request premium users, pass False to request non-premium users. If not specified, no additional restrictions are applied.
    max_quantity: The maximum number of users to be selected; 1-10. Defaults to 1.
    request_name: Pass True to request the users' first and last names
    request_username: Pass True to request the users' usernames
    request_photo: Pass True to request the users' photos"""
    request_id: int = 0
    user_is_bot: Optional[bool] = None
    user_is_premium: Optional[bool] = None
    max_quantity: Optional[int] = None
    request_name: Optional[bool] = None
    request_username: Optional[bool] = None
    request_photo: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['KeyboardButtonRequestUsers']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['KeyboardButtonRequestUsers']``).\n        "
        if data is None:
            return None
        return cls(request_id=data.get('request_id', 0), user_is_bot=data.get('user_is_bot'), user_is_premium=data.get('user_is_premium'), max_quantity=data.get('max_quantity'), request_name=data.get('request_name'), request_username=data.get('request_username'), request_photo=data.get('request_photo'))

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'request_id': self.request_id}
        if self.user_is_bot is not None:
            body['user_is_bot'] = self.user_is_bot
        if self.user_is_premium is not None:
            body['user_is_premium'] = self.user_is_premium
        if self.max_quantity is not None:
            body['max_quantity'] = self.max_quantity
        if self.request_name is not None:
            body['request_name'] = self.request_name
        if self.request_username is not None:
            body['request_username'] = self.request_username
        if self.request_photo is not None:
            body['request_photo'] = self.request_photo
        return body
