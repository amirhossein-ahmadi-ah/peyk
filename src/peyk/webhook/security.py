from __future__ import annotations

import hmac
import ipaddress
from collections.abc import Mapping, Sequence
from typing import Final

TELEGRAM_OFFICIAL_NETWORKS: Final[tuple[str, ...]] = (
    "149.154.160.0/20",
    "91.108.4.0/22",
)


def constant_time_compare(a: str | None, b: str | None) -> bool:
    """Compare two non-empty strings without ordinary early-exit timing."""
    if not a or not b:
        return False
    return hmac.compare_digest(a, b)


def verify_telegram_secret_header(headers: Mapping[str, str], secret_token: str) -> bool:
    """Validate Telegram's documented webhook secret header."""
    return constant_time_compare(headers.get("X-Telegram-Bot-Api-Secret-Token"), secret_token)


class IPFilter:
    """Allow webhook requests only when their source IP is in configured networks.

    ``trust_forwarded_for`` is deliberately opt-in. When disabled, only the
    transport peer address is considered, so an untrusted client cannot choose
    its own address through ``X-Forwarded-For``.
    """

    def __init__(self, networks: Sequence[str], *, trust_forwarded_for: bool = False) -> None:
        self._networks = tuple(ipaddress.ip_network(value, strict=False) for value in networks)
        self.trust_forwarded_for = trust_forwarded_for

    def allows(self, peer_ip: str, headers: Mapping[str, str]) -> bool:
        """Return whether the request source belongs to an allowed network."""
        candidate = peer_ip
        if self.trust_forwarded_for:
            forwarded = headers.get("X-Forwarded-For", "").split(",", 1)[0].strip()
            if forwarded:
                candidate = forwarded
        try:
            address = ipaddress.ip_address(candidate)
        except ValueError:
            return False
        return any(address in network for network in self._networks)
