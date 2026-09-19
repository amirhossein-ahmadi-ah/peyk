"""Generic retry wrapper for transport operations.

Retries only the exception types explicitly listed in `retryable`.
`HTTPStatusError` is never in the default set and must never be retried:
a non-2xx application-level response is not a transient transport
condition.
"""
from __future__ import annotations
import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable, Optional, Tuple, Type, TypeVar
from .errors import NetworkError, RateLimitedError, TimeoutError_, TransportError
from .logging_hook import TransportLogger, get_default_logger
T = TypeVar('T')
DEFAULT_RETRYABLE: Tuple[Type[TransportError], ...] = (NetworkError, TimeoutError_, RateLimitedError)

@dataclass(frozen=True)
class RetryPolicy:
    """Configuration for `run_with_retry`.

    Attributes:
        max_attempts: Total number of attempts (including the first),
            not the number of retries.
        base_backoff_seconds: Base delay for exponential backoff between
            attempts, used when the raised error doesn't carry its own
            hint (e.g. `RateLimitedError.retry_after_seconds`).
    """
    max_attempts: int = 3
    base_backoff_seconds: float = 0.5

async def run_with_retry(operation: Callable[[], Awaitable[T]], policy: RetryPolicy, retryable: Tuple[Type[TransportError], ...]=DEFAULT_RETRYABLE, logger: Optional[TransportLogger]=None) -> T:
    """Performs the run with retry operation for the transport client.

Args:
    operation: Value used by this operation.
    policy: Value used by this operation.
    retryable: Value used by this operation.
    logger: Value used by this operation.

Returns:
    Result produced by the transport operation."""
    "Run `operation()`, retrying on the exception types in `retryable`.\n    \n        - Only exceptions that are instances of one of `retryable` are retried;\n          anything else (including `HTTPStatusError`) propagates immediately.\n        - When a `RateLimitedError` carries `retry_after_seconds`, that value\n          is used as the delay instead of the exponential backoff.\n        - Backoff between attempts is `base_backoff_seconds * 2 ** (attempt - 1)`\n          for the 1-indexed attempt number, when no explicit hint is present.\n        - After the final attempt, the exception is re-raised rather than\n          swallowed.\n        - `logger` (added in Phase A2) is called once per retry via\n          `log_retry(attempt, exception)`, and exactly once via\n          `log_failure(exception)` when this function gives up — whether that's\n          because retries were exhausted or because the exception wasn't\n          retryable in the first place. Defaults to the shared stdlib-backed\n          logger, so existing callers that never pass `logger` are unaffected.\n        \n    \n    Args:\n        operation: Value of the declared parameter type.\n        policy: Value of the declared parameter type.\n        retryable: Value of the declared parameter type.\n        logger: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``T``).\n\n    Raises:\n        TransportError: Re-raised after retries are exhausted or when the\n            exception is not retryable.\n    "
    logger = logger or get_default_logger()
    attempt = 0
    while True:
        attempt += 1
        try:
            return await operation()
        except retryable as exc:
            if attempt >= policy.max_attempts:
                logger.log_failure(exc)
                raise
            logger.log_retry(attempt, exc)
            if isinstance(exc, RateLimitedError) and exc.retry_after_seconds is not None:
                delay = exc.retry_after_seconds
            else:
                delay = policy.base_backoff_seconds * 2 ** (attempt - 1)
            await asyncio.sleep(delay)
        except Exception as exc:
            logger.log_failure(exc)
            raise
