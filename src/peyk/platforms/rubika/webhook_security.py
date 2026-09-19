"""Backward-compatible import shim for webhook security helpers."""
from __future__ import annotations

import warnings

from peyk.webhook.security import constant_time_compare

warnings.warn(
    "peyk.platforms.rubika.webhook_security.constant_time_compare is deprecated; import from peyk.webhook.security instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["constant_time_compare"]
