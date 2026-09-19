"""Bale application-level API errors.

Every Bale response is a JSON envelope with an `ok` flag. On `ok: false`,
Bale still returns a plain HTTP 200 -- the failure is encoded in the JSON
body (`description` + `error_code` + optional `parameters`), not in the
HTTP status line. That makes it an *application*-level failure, distinct
from `peyk.transport`'s transport-level errors (`HTTPStatusError`,
`NetworkError`, `TimeoutError_`, `RateLimitedError`), which are raised
from transport-level facts only (connection failures, timeouts, non-2xx
status codes).

`BaleAPIError` subclasses `peyk.transport.errors.TransportError` so it can
still be caught alongside transport errors by callers that want a single
"something about this Bale call failed" catch-all -- but it is
deliberately **not** included in `peyk.transport.retry.DEFAULT_RETRYABLE`,
and `BaleClient` never passes it through `run_with_retry` in the first
place (see `client.py`): a `run_with_retry`-wrapped call to
`Session.request()` already returns successfully (HTTP 200, valid JSON)
before `BaleClient` ever looks at the `ok` flag, so the retry layer never
even sees a `BaleAPIError` to (correctly) decline to retry.
"""

from __future__ import annotations

from typing import Any, Optional

from peyk.transport.errors import TransportError


class BaleAPIError(TransportError):
    """Raised when a Bale API response has `ok: false`.

    Attributes:
        error_code: Bale's `error_code` integer from the response body.
        description: Bale's human-readable `description` string.
        parameters: The optional `parameters` object Bale sometimes
            includes alongside an error (e.g. retry hints for specific
            error codes). `None` when absent.
    """

    def __init__(
        self,
        message: str,
        *,
        error_code: int,
        description: str,
        parameters: Optional[object] = None,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.description = description
        self.parameters = parameters
