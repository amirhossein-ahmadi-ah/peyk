"""Transport-level exceptions.

These carry only transport-level facts (connection failure, timeout, HTTP
status, rate-limit hint). No platform-specific error-body parsing happens
here or anywhere in this project — that is deliberately deferred to future
per-platform adapters that sit on top of `peyk`.
"""

from __future__ import annotations

from typing import Optional


class TransportError(Exception):
    """Base class for all errors raised by the transport layer."""


class NetworkError(TransportError):
    """Raised when the underlying connection fails.

    Covers DNS failure, connection refused, connection reset, and other
    transport-level connectivity problems that are not an HTTP response.
    """


class TimeoutError_(TransportError):
    """Raised when a request does not complete within its configured timeout.

    Named with a trailing underscore to avoid shadowing the builtin
    ``TimeoutError``.
    """


class RateLimitedError(TransportError):
    """Raised when the server responds with HTTP 429 (Too Many Requests).

    Attributes:
        retry_after_seconds: The value of the response's ``Retry-After``
            header, parsed to seconds, if present and parseable.
            ``None`` if the header was absent or not parseable as a
            plain number of seconds.
    """

    def __init__(self, message: str, *, retry_after_seconds: Optional[float] = None) -> None:
        super().__init__(message)
        self.retry_after_seconds = retry_after_seconds


class HTTPStatusError(TransportError):
    """Raised for any non-2xx HTTP response other than 429.

    Attributes:
        status_code: The HTTP status code returned by the server.
        body: The raw response body bytes (may be empty).
    """

    def __init__(self, message: str, *, status_code: int, body: bytes) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body
