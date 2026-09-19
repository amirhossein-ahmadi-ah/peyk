"""Typing-ratchet checks for the source audit and static reveal tests."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_any_audit_ratchet() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "audit_any.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "module | Any | bare dict | unannotated params | unannotated returns" in result.stdout


def test_mypy_reveal_types() -> None:
    if importlib.util.find_spec("mypy") is None:
        pytest.skip("mypy is not installed in this environment")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "mypy", "tests/typing/test_reveal_types.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        pytest.skip("mypy is not installed in this environment")
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
