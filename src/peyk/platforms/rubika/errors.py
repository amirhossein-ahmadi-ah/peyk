"""Rubika application-level API errors.

Rubika returns HTTP 200 for every call -- including failures. The
failure is encoded in the JSON body as a string ``status`` field:

    {"status": "OK",    "data": {...}}
    {"status": "error", "error_code": "...", "error_message": "..."}

``error_code`` is a **string** identifier, not an integer. This is the
main structural difference from Bale/Telegram and the reason a
separate ``RubikaAPIError`` exists.

Confirmed from the official docs at rubika.ir/botapi.
"""
from __future__ import annotations
from typing import Any, Optional
from peyk.transport.errors import TransportError

class RubikaAPIError(TransportError):
    """Raised when a Rubika response has ``status != "OK"``."""

    def __init__(self, message: str, *, error_code: str, error_message: str, raw: Optional[dict]=None) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.error_message = error_message
        self.raw = raw

def error_for_envelope(envelope: dict) -> RubikaAPIError:
    """Performs the error for envelope operation for the Rubika client.

Args:
    envelope: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
    "Build a ``RubikaAPIError`` from an error envelope.\n    \n        Does NOT auto-map any error_code to ``RateLimitedError`` -- the\n        official docs don't document a rate-limit code or a numeric\n        retry hint.\n        \n    \n    Args:\n        envelope: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``RubikaAPIError``).\n    "
    error_code = str(envelope.get('error_code', '')) or 'UNKNOWN'
    error_message = envelope.get('error_message') or 'unknown Rubika error'
    return RubikaAPIError(f'Rubika API error {error_code}: {error_message}', error_code=error_code, error_message=error_message, raw=envelope)
