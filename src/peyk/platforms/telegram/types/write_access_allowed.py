from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class WriteAccessAllowed:
    """This object represents a service message about a user allowing a bot to write messages after adding it to the attachment menu, launching a Web App from a link, or accepting an explicit request from a Web App sent by the method requestWriteAccess.

Attributes:
    from_request: True, if the access was granted after the user accepted an explicit request from a Web App sent by the method requestWriteAccess
    web_app_name: Name of the Web App, if the access was granted when the Web App was launched from a link
    from_attachment_menu: True, if the access was granted when the bot was added to the attachment or side menu"""
    from_request: Optional[bool] = None
    web_app_name: Optional[str] = None
    from_attachment_menu: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['WriteAccessAllowed']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['WriteAccessAllowed']``).\n        "
        if data is None:
            return None
        return cls(from_request=data.get('from_request'), web_app_name=data.get('web_app_name'), from_attachment_menu=data.get('from_attachment_menu'))
