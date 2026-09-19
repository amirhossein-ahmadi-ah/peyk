"""T5 tagged union for Telegram chat-member responses."""
from typing import Optional, Union
from .chat_member_administrator import ChatMemberAdministrator
from .chat_member_banned import ChatMemberBanned
from .chat_member_left import ChatMemberLeft
from .chat_member_member import ChatMemberMember
from .chat_member_owner import ChatMemberOwner
from .chat_member_restricted import ChatMemberRestricted
ChatMember = Union[ChatMemberOwner, ChatMemberAdministrator, ChatMemberMember, ChatMemberRestricted, ChatMemberLeft, ChatMemberBanned]
_CHAT_MEMBER_TYPES = {'creator': ChatMemberOwner, 'administrator': ChatMemberAdministrator, 'member': ChatMemberMember, 'restricted': ChatMemberRestricted, 'left': ChatMemberLeft, 'kicked': ChatMemberBanned}

def parse_chat_member(data: Optional[dict]) -> Optional[ChatMember]:
    """Provides the parse chat member operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
    'Parse a Telegram ``ChatMember`` tagged by its ``status`` field.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional[ChatMember]``).\n        \n    \n    Raises:\n        ValueError: Raised when the operation cannot complete.\n    '
    if data is None:
        return None
    cls = _CHAT_MEMBER_TYPES.get(data.get('status', ''))
    if cls is None:
        raise ValueError(f"unknown ChatMember status: {data.get('status')!r}")
    return cls.from_dict(data)
