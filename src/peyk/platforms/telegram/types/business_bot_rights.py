from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BusinessBotRights:
    """Represents the rights of a business bot.

Attributes:
    can_reply: True, if the bot can send and edit messages in the private chats that had incoming messages in the last 24 hours
    can_read_messages: True, if the bot can mark incoming private messages as read
    can_delete_sent_messages: True, if the bot can delete messages sent by the bot
    can_delete_all_messages: True, if the bot can delete all private messages in managed chats
    can_edit_name: True, if the bot can edit the first and last name of the business account
    can_edit_bio: True, if the bot can edit the bio of the business account
    can_edit_profile_photo: True, if the bot can edit the profile photo of the business account
    can_edit_username: True, if the bot can edit the username of the business account
    can_change_gift_settings: True, if the bot can change the privacy settings pertaining to gifts for the business account
    can_view_gifts_and_stars: True, if the bot can view gifts and the amount of Telegram Stars owned by the business account
    can_convert_gifts_to_stars: True, if the bot can convert regular gifts owned by the business account to Telegram Stars
    can_transfer_and_upgrade_gifts: True, if the bot can transfer and upgrade gifts owned by the business account
    can_transfer_stars: True, if the bot can transfer Telegram Stars received by the business account to its own account, or use them to upgrade and transfer gifts
    can_manage_stories: True, if the bot can post, edit and delete stories on behalf of the business account
    can_delete_outgoing_messages: True, if the bot can delete messages sent by the bot"""
    can_reply: Optional[bool] = None
    can_delete_outgoing_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_delete_all_messages: Optional[bool] = None
    can_post_stories: Optional[bool] = None
    can_edit_stories: Optional[bool] = None
    can_delete_stories: Optional[bool] = None
    can_read_messages: Optional[bool] = None
    can_change_gift_settings: Optional[bool] = None
    can_transfer_and_upgrade_gifts: Optional[bool] = None
    can_convert_gift_to_stars: Optional[bool] = None
    can_transfer_stars: Optional[bool] = None
    can_manage_connected_bots: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BusinessBotRights']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BusinessBotRights']``).\n        "
        if data is None:
            return None
        return cls(**{f: data.get(f) for f in ('can_reply', 'can_delete_outgoing_messages', 'can_edit_messages', 'can_delete_all_messages', 'can_post_stories', 'can_edit_stories', 'can_delete_stories', 'can_read_messages', 'can_change_gift_settings', 'can_transfer_and_upgrade_gifts', 'can_convert_gift_to_stars', 'can_transfer_stars', 'can_manage_connected_bots')})
