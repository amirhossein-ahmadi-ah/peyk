from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class WebhookInfo:
    """Current webhook status.

    Per docs.bale.ai, `WebhookInfo` only carries `url` -- unlike Telegram's
    richer type, Bale does not document `has_custom_certificate` or
    `pending_update_count`.
    """
    url: str

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['WebhookInfo']:
        """Parse raw Bale data into ``WebhookInfo``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[WebhookInfo]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(url=data.get('url', ''))
