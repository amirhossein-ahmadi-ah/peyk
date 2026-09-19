from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class LoginUrl:
    """This object represents a parameter of the inline keyboard button used to automatically authorize a user. Serves as a great replacement for the Telegram Login Widget when the user is coming from Telegram. All the user needs to do is tap/click a button and confirm that they want to log in:
Telegram apps support these buttons as of version 5.7.
Sample bot: @discussbot

Attributes:
    url: An HTTPS URL to be opened with user authorization data added to the query string when the button is pressed. If the user refuses to provide authorization data, the original URL without information about the user will be opened. The data added is the same as described in Receiving authorization data.

NOTE: You must always check the hash of the received data to verify the authentication and the integrity of the data as described in Checking authorization.
    forward_text: New text of the button in forwarded messages
    bot_username: Username of a bot, which will be used for user authorization. See Setting up a bot for more details. If not specified, the current bot's username will be assumed. The url's domain must be the same as the domain linked with the bot. See Linking your domain to the bot for more details.
    request_write_access: Pass True to request the permission for your bot to send messages to the user"""
    url: str = ''
    forward_text: Optional[str] = None
    bot_username: Optional[str] = None
    request_write_access: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['LoginUrl']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['LoginUrl']``).\n        "
        if data is None:
            return None
        return cls(url=data.get('url', ''), forward_text=data.get('forward_text'), bot_username=data.get('bot_username'), request_write_access=data.get('request_write_access'))

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'url': self.url}
        if self.forward_text is not None:
            body['forward_text'] = self.forward_text
        if self.bot_username is not None:
            body['bot_username'] = self.bot_username
        if self.request_write_access is not None:
            body['request_write_access'] = self.request_write_access
        return body
