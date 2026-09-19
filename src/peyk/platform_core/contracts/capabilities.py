"""Capabilities advertised by each platform adapter."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal
UpdateDelivery = Literal['polling', 'webhook_only', 'both']

@dataclass(frozen=True)
class PlatformCapabilities:
    """PlatformCapabilities provides the platform-core API surface used by peyk."""
    'Represents `PlatformCapabilities`.\n\nRaises:\n    \n'
    supports_topics: bool
    supports_scheduled_messages: bool
    update_delivery: UpdateDelivery
    platform: str = 'custom'
    supported_parse_modes: list[str] = field(default_factory=list)
    callback_data_max_bytes: int | None = None
    supports_payments: bool = False
    supports_admin_detection: bool = False
    supports_chat_member_status_updates: bool = False
