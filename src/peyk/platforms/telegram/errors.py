"""Telegram application-level API errors.

Every Telegram Bot API response is a JSON envelope with an ``ok`` flag.
On ``ok: false`` Telegram still returns a plain HTTP 200 -- the failure
is encoded in the JSON body (``description`` + ``error_code`` + optional
``parameters``), not in the HTTP status line. That makes it an
*application*-level failure, distinct from ``peyk.transport``'s
transport-level errors (``HTTPStatusError``, ``NetworkError``,
``TimeoutError_``, ``RateLimitedError``), which are raised from
transport-level facts only (connection failures, timeouts, non-2xx
status codes).

``TelegramAPIError`` subclasses ``peyk.transport.errors.TransportError``
so it can still be caught alongside transport errors by callers that
want a single "something about this Telegram call failed" catch-all --
but it is deliberately **not** included in
``peyk.transport.retry.DEFAULT_RETRYABLE``, and ``TelegramClient`` never
passes it through ``run_with_retry`` in the first place (see
``client.py``): a ``run_with_retry``-wrapped call to
``Session.request()`` already returns successfully (HTTP 200, valid
JSON) before ``TelegramClient`` ever looks at the ``ok`` flag, so the
retry layer never even sees a ``TelegramAPIError`` to (correctly)
decline to retry.

Rate-limit decision (see ``docs/decisions.md``): when the ``ok: false``
envelope carries ``parameters.retry_after``, that is Telegram's
rate-limit signal (Telegram does not use a generic HTTP 429 for this).
In that case ``TelegramClient._call`` raises ``RateLimitedError`` (from
``peyk.transport``) with ``retry_after_seconds`` set, instead of
``TelegramAPIError``. The raise still happens *after* ``run_with_retry``
has returned, so it is **not** auto-retried by ``_call`` -- the caller
sees a retryable-typed signal and decides when to retry.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from peyk.transport.errors import RateLimitedError, TransportError

@dataclass
class ResponseParameters:
    """Telegram's ``ResponseParameters`` error-hint object.

    Only the fields Telegram documents on this object are modelled:
    ``migrate_to_chat_id`` (group migrated to a supergroup) and
    ``retry_after`` (rate-limit wait hint, seconds).
    """
    migrate_to_chat_id: Optional[int] = None
    retry_after: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ResponseParameters']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ResponseParameters']``).\n        "
        if data is None:
            return None
        return cls(migrate_to_chat_id=data.get('migrate_to_chat_id'), retry_after=data.get('retry_after'))

class TelegramAPIError(TransportError):
    """Raised when a Telegram API response has ``ok: false`` (no rate hint).

    Attributes:
        error_code: Telegram's ``error_code`` integer from the response body.
        description: Telegram's human-readable ``description`` string.
        parameters: The optional ``parameters`` object Telegram sometimes
            includes alongside an error (a ``ResponseParameters`` when the
            raw dict parses, else the raw value). ``None`` when absent.
            Note: when the parameters carry ``retry_after``,
            ``TelegramClient`` raises ``RateLimitedError`` instead of this
            class -- so a ``TelegramAPIError`` observed in practice never
            carries a retry hint (see module docstring).
    """

    def __init__(self, message: str, *, error_code: int, description: str, parameters: Optional[ResponseParameters]=None) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.description = description
        self.parameters = parameters

def error_for_envelope(method_name: str, *, error_code: int, description: str, parameters: Optional[dict]) -> TransportError:
    """Provides the error for envelope operation for the Telegram integration.

Args:
    method_name: Value used by this operation.
    error_code: Value used by this operation.
    description: Value used by this operation.
    parameters: Value used by this operation.

Returns:
    Result produced by the operation."""
    "Build the right exception for an ``ok: false`` envelope.\n    \n        Returns a ``RateLimitedError`` when ``parameters`` carries\n        ``retry_after`` (Telegram's rate-limit signal), else a\n        ``TelegramAPIError``. Single place for the decision so ``client.py``\n        and tests share it.\n        \n    \n    Args:\n        method_name: Value of the declared parameter type.\n        error_code: Value of the declared parameter type.\n        description: Value of the declared parameter type.\n        parameters: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``TransportError``).\n    "
    parsed = ResponseParameters.from_dict(parameters)
    retry_after = parsed.retry_after if parsed is not None else None
    if retry_after is not None:
        return RateLimitedError(description or f'{method_name} rate limited', retry_after_seconds=float(retry_after))
    return TelegramAPIError(description or f'{method_name} failed', error_code=error_code, description=description, parameters=parsed)
