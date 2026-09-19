from __future__ import annotations

from typing import Any, Optional

def _to_str(value: object) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return str(value)

def _to_int(value: object) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

def _to_float(value: object) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

def _unwrap(data: object, key: str) -> object:
    """Extract ``data[key]`` if present, else return ``data`` unchanged."""
    if isinstance(data, dict) and key in data:
        return data[key]
    return data
