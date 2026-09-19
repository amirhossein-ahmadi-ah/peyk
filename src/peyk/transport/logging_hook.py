"""Minimal transport logging hook.

Not a full logging system — `peyk` is a separate repo from `hazardastan`
and has no access to its richer logger. This is deliberately just a
three-method `Protocol` plus a stdlib-`logging`-backed default, so callers
(including `hazardastan`'s eventual adapter) can supply their own
implementation without `peyk` depending on anything beyond the stdlib.
"""
from __future__ import annotations
import logging
from typing import Optional, Protocol

class TransportLogger(Protocol):
    """Logging hook used by the transport layer.

    The protocol separates request, event, retry, and final-failure logging.
    """

    def log_request(self, method: str, url: str) -> None:
        """Performs the log request operation for the transport client.

Args:
    method: Value used by this operation.
    url: Target URL."""
        'Log one transport request.\n\n        Args:\n            method: HTTP method.\n            url: Request URL.\n\n        Returns:\n            None.\n\n        Raises:\n            \n        '
        ...

    def log_event(self, event: object) -> None:
        """Performs the log event operation for the transport client.

Args:
    event: Value used by this operation."""
        'Log one normalized event.\n\n        Args:\n            event: Event object being dispatched.\n\n        Returns:\n            None.\n\n        Raises:\n            \n        '
        ...

    def log_retry(self, attempt: int, exception: Exception) -> None:
        """Performs the log retry operation for the transport client.

Args:
    attempt: Value used by this operation.
    exception: Value used by this operation."""
        'Log one retry attempt.\n\n        Args:\n            attempt: One-based retry attempt number.\n            exception: Exception that caused the retry.\n\n        Returns:\n            None.\n\n        Raises:\n            \n        '
        ...

    def log_failure(self, exception: Exception) -> None:
        """Performs the log failure operation for the transport client.

Args:
    exception: Value used by this operation."""
        'Log a final transport failure.\n\n        Args:\n            exception: Exception that ended the operation.\n\n        Returns:\n            None.\n\n        Raises:\n            \n        '
        ...

class StdlibTransportLogger:
    """Default `TransportLogger`, backed by `logging.getLogger("peyk.transport")`.

    Requests log at DEBUG (high-volume, opt-in visibility), retries at
    WARNING (worth noticing but expected/handled), failures at ERROR
    (nothing left to retry — the caller now has to deal with it).
    """

    def __init__(self, logger: Optional[logging.Logger]=None) -> None:
        self._logger = logger or logging.getLogger('peyk.transport')

    def log_request(self, method: str, url: str) -> None:
        """Performs the log request operation for the transport client.

Args:
    method: Value used by this operation.
    url: Target URL."""
        'Performs the log_request operation.\n\nArgs:\n    method: str.\n    url: str.\n\nReturns:\n    None.\n\nRaises:\n    \n'
        self._logger.debug('request: %s %s', method, url)

    def log_event(self, event: object) -> None:
        """Performs the log event operation for the transport client.

Args:
    event: Value used by this operation."""
        'Performs the log_event operation.\n\nArgs:\n    event: object.\n\nReturns:\n    None.\n\nRaises:\n    \n'
        from peyk.platform_core.contracts.message import IncomingMessage
        name = 'IncomingMessage' if isinstance(event, IncomingMessage) else type(event).__name__
        self._logger.info('event: %s', name)

    def log_retry(self, attempt: int, exception: Exception) -> None:
        """Performs the log retry operation for the transport client.

Args:
    attempt: Value used by this operation.
    exception: Value used by this operation."""
        'Performs the log_retry operation.\n\nArgs:\n    attempt: int.\n    exception: Exception.\n\nReturns:\n    None.\n\nRaises:\n    \n'
        self._logger.warning('retry: attempt %d failed with %r', attempt, exception)

    def log_failure(self, exception: Exception) -> None:
        """Performs the log failure operation for the transport client.

Args:
    exception: Value used by this operation."""
        'Performs the log_failure operation.\n\nArgs:\n    exception: Exception.\n\nReturns:\n    None.\n\nRaises:\n    \n'
        self._logger.error('failed: %r', exception)
_default_logger: Optional[TransportLogger] = None

def get_default_logger() -> TransportLogger:
    """A shared, lazily-created `StdlibTransportLogger` instance.
    
        Used by `Session` and `run_with_retry` when no `TransportLogger` is
        passed explicitly, so A1's existing call sites (which never pass a
        logger) keep working unmodified.
        
    
    Returns:
        The operation result (``TransportLogger``).
    """
    global _default_logger
    if _default_logger is None:
        _default_logger = StdlibTransportLogger()
    return _default_logger
