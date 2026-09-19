"""Transport layer: session, errors, retry.

Public re-exports so callers can do ``from peyk.transport import Session, ...``
instead of reaching into submodules.
"""

from .errors import (
    HTTPStatusError,
    NetworkError,
    RateLimitedError,
    TimeoutError_,
    TransportError,
)
from .logging_hook import StdlibTransportLogger, TransportLogger, get_default_logger
from .multipart import FilePayload, build_multipart_body
from .retry import RetryPolicy, run_with_retry
from .session import Session, TransportResponse

__all__ = [
    "Session",
    "TransportResponse",
    "TransportError",
    "NetworkError",
    "TimeoutError_",
    "RateLimitedError",
    "HTTPStatusError",
    "RetryPolicy",
    "run_with_retry",
    "FilePayload",
    "build_multipart_body",
    "TransportLogger",
    "StdlibTransportLogger",
    "get_default_logger",
]
