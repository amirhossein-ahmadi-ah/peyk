from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class WebhookInfo:
    """Describes the current status of a webhook.

Attributes:
    url: Webhook URL, may be empty if webhook is not set up
    has_custom_certificate: True, if a custom certificate was provided for webhook certificate checks
    pending_update_count: Number of updates awaiting delivery
    ip_address: Currently used webhook IP address
    last_error_date: Unix time for the most recent error that happened when trying to deliver an update via webhook
    last_error_message: Error message in human-readable format for the most recent error that happened when trying to deliver an update via webhook
    last_synchronization_error_date: Unix time of the most recent error that happened when trying to synchronize available updates with Telegram datacenters
    max_connections: The maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery
    allowed_updates: A list of update types the bot is subscribed to. Defaults to all update types except chat_member, message_reaction, and message_reaction_count."""
    url: str
    has_custom_certificate: Optional[bool] = None
    pending_update_count: Optional[int] = None
    ip_address: Optional[str] = None
    last_error_date: Optional[int] = None
    last_error_message: Optional[str] = None
    last_synchronization_error_date: Optional[int] = None
    max_connections: Optional[int] = None
    allowed_updates: Optional[List[str]] = field(default=None)

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['WebhookInfo']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(url=data.get('url', ''), has_custom_certificate=data.get('has_custom_certificate'), pending_update_count=data.get('pending_update_count'), ip_address=data.get('ip_address'), last_error_date=data.get('last_error_date'), last_error_message=data.get('last_error_message'), last_synchronization_error_date=data.get('last_synchronization_error_date'), max_connections=data.get('max_connections'), allowed_updates=data.get('allowed_updates'))
