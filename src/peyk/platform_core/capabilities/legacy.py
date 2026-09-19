"""Compatibility projection for the pre-R0 capability dataclass."""
from __future__ import annotations
from peyk.platform_core.contracts import PlatformCapabilities
from . import Feature, get_capabilities

def legacy_capabilities(platform: str) -> PlatformCapabilities:
    """Build the legacy nine-field capability object from the audited registry."""
    caps = get_capabilities(platform)
    modes = ["Markdown", "MarkdownV2", "HTML"] if platform == "telegram" else []
    return PlatformCapabilities(
        platform=platform,
        supports_topics=caps.supports(Feature.FORUM_TOPICS),
        supports_scheduled_messages=False,
        update_delivery="both" if caps.get(Feature.POLLING).level.value != "none" and caps.get(Feature.WEBHOOK).level.value != "none" else "polling",
        supported_parse_modes=modes,
        callback_data_max_bytes=caps.limit("callback_data_max_bytes") if isinstance(caps.limit("callback_data_max_bytes"), int) else None,
        supports_payments=caps.supports(Feature.PAYMENTS),
        supports_admin_detection=platform in {"telegram", "bale"},
        supports_chat_member_status_updates=platform == "telegram",
    )
