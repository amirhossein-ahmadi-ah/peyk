"""A single, reused `aiohttp.ClientSession` behind a generic request() call.

Performance choices here (tuned `TCPConnector`, `orjson` for JSON) are
generic, documented `aiohttp`/Python practices — not copied from any
specific library's source. See docs/decisions.md for the reasoning behind
the specific connector values and for the "techniques, not code" note.
"""
from __future__ import annotations
import asyncio
from dataclasses import dataclass
from types import TracebackType
from typing import Any, Mapping, Optional, Type
import aiohttp
import orjson
from .errors import HTTPStatusError, NetworkError, RateLimitedError, TimeoutError_
from .logging_hook import TransportLogger, get_default_logger
from .multipart import FilePayload, build_multipart_body
DEFAULT_LIMIT = 100
DEFAULT_LIMIT_PER_HOST = 30
DEFAULT_KEEPALIVE_TIMEOUT = 30.0
DEFAULT_TTL_DNS_CACHE = 300

@dataclass(frozen=True)
class TransportResponse:
    """The result of a successful (2xx) transport-level request.

    Attributes:
        status: HTTP status code.
        json: Parsed body via `orjson`, if the response's Content-Type
            indicated JSON and the body parsed successfully. `None`
            otherwise.
        body: Raw response body bytes, always populated.
        headers: Response headers as a plain mapping.
    """
    status: int
    json: Optional[object]
    body: bytes
    headers: Mapping[str, str]

def _orjson_dumps(obj: object) -> str:
    return orjson.dumps(obj).decode('utf-8')

def _parse_retry_after(value: Optional[str]) -> Optional[float]:
    """Parse a `Retry-After` header value as a plain number of seconds.

    Only the delta-seconds form is handled (e.g. `"120"`). The HTTP-date
    form is intentionally not parsed here — platform-specific error
    handling, including any richer Retry-After interpretation, belongs to
    future per-platform adapters, not this generic transport layer.
    """
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None

class Session:
    """Wraps one reused `aiohttp.ClientSession` backed by a tuned connector."""

    def __init__(self, *, limit: int=DEFAULT_LIMIT, limit_per_host: int=DEFAULT_LIMIT_PER_HOST, keepalive_timeout: float=DEFAULT_KEEPALIVE_TIMEOUT, ttl_dns_cache: int=DEFAULT_TTL_DNS_CACHE, logger: Optional[TransportLogger]=None) -> None:
        connector = aiohttp.TCPConnector(limit=limit, limit_per_host=limit_per_host, keepalive_timeout=keepalive_timeout, ttl_dns_cache=ttl_dns_cache)
        self._session = aiohttp.ClientSession(connector=connector, json_serialize=_orjson_dumps)
        self._logger: TransportLogger = logger or get_default_logger()

    @property
    def connector(self) -> aiohttp.BaseConnector:
        """The underlying connector, exposed so reuse can be asserted in tests.
        
        Returns:
            The operation result (``aiohttp.BaseConnector``).
        """
        return self._session.connector

    async def request(self, method: str, url: str, *, params: Optional[Mapping[str, object]]=None, json_body: Optional[object]=None, data: Optional[object]=None, files: Optional[Mapping[str, FilePayload]]=None, timeout: Optional[float]=None) -> TransportResponse:
        """Performs the request operation for the transport client.

Args:
    method: Value used by this operation.
    url: Target URL.
    params: Value used by this operation.
    json_body: Value used by this operation.
    data: Value used by this operation.
    files: Value used by this operation.
    timeout: Maximum time to wait for the operation.

Returns:
    Result produced by the transport operation."""
        'Issue a request and return a `TransportResponse`.\n        \n                `files` (added in Phase A2) builds a `multipart/form-data` body:\n                pass plain string fields via `data` (as a mapping) alongside\n                `files`, keyed by their multipart field names. `files` and\n                `json_body` cannot be combined. File payloads may be raw `bytes`\n                or a file-like/stream object — streams are not read into memory\n                here, see `multipart.py`.\n        \n                Raises:\n                    NetworkError: on connection-level failure.\n                    TimeoutError_: if the request exceeds `timeout`.\n                    RateLimitedError: on HTTP 429.\n                    HTTPStatusError: on any other non-2xx status.\n                    ValueError: if both `files` and `json_body` are given.\n                \n        \n        Args:\n            method: Value of the declared parameter type.\n            url: Value of the declared parameter type.\n            params: Value of the declared parameter type.\n            json_body: Value of the declared parameter type.\n            data: Value of the declared parameter type.\n            files: Value of the declared parameter type.\n            timeout: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``TransportResponse``).\n        '
        self._logger.log_request(method, url)
        request_body: Optional[object] = data
        if files:
            if json_body is not None:
                raise ValueError('request() cannot take both json_body and files')
            fields = data if isinstance(data, Mapping) else None
            request_body = build_multipart_body(fields, files)
        client_timeout = aiohttp.ClientTimeout(total=timeout) if timeout is not None else None
        try:
            async with self._session.request(method, url, params=params, json=json_body, data=request_body if json_body is None else None, timeout=client_timeout) as resp:
                body = await resp.read()
                if resp.status == 429:
                    retry_after = _parse_retry_after(resp.headers.get('Retry-After'))
                    raise RateLimitedError(f'Rate limited by {url}', retry_after_seconds=retry_after)
                if not 200 <= resp.status < 300:
                    raise HTTPStatusError(f'HTTP {resp.status} for {url}', status_code=resp.status, body=body)
                parsed_json = None
                content_type = resp.headers.get('Content-Type', '')
                if 'json' in content_type and body:
                    try:
                        parsed_json = orjson.loads(body)
                    except orjson.JSONDecodeError:
                        parsed_json = None
                return TransportResponse(status=resp.status, json=parsed_json, body=body, headers=dict(resp.headers))
        except (RateLimitedError, HTTPStatusError):
            raise
        except (asyncio.TimeoutError, aiohttp.ServerTimeoutError) as exc:
            raise TimeoutError_(f'Request to {url} timed out') from exc
        except aiohttp.ClientConnectionError as exc:
            raise NetworkError(f'Connection failed for {url}: {exc}') from exc
        except aiohttp.ClientError as exc:
            raise NetworkError(f'Network error for {url}: {exc}') from exc

    async def close(self) -> None:
        """Performs the close operation for the transport client."""
        'Performs the close operation.\n\nArgs:\n    None.\n\nReturns:\n    None.\n\nRaises:\n    \n'
        await self._session.close()

    async def __aenter__(self) -> 'Session':
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]], exc: Optional[BaseException], tb: Optional[TracebackType]) -> None:
        await self.close()
