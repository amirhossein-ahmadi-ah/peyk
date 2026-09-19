"""Phase 10C quality gates and deterministic schema sync checks."""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _run(script: str, *args: str) -> None:
    result = subprocess.run([sys.executable, str(ROOT / script), *args], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def _tree_hash(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(path.glob("*.py")):
        digest.update(item.name.encode())
        digest.update(item.read_bytes())
    return digest.hexdigest()


def test_docstring_audit_passes() -> None:
    _run("scripts/audit_docstrings.py")


def test_any_audit_passes() -> None:
    _run("scripts/audit_any.py")


def test_telegram_schema_sync_is_idempotent() -> None:
    methods = ROOT / "src/peyk/platforms/telegram/methods"
    with tempfile.TemporaryDirectory() as temp:
        base = Path(temp) / ".butcher"
        schema_path = base / "schema" / "schema.json"
        method_path = base / "methods" / "getMe" / "entity.json"
        schema_path.parent.mkdir(parents=True)
        method_path.parent.mkdir(parents=True)
        schema_path.write_text(json.dumps({"api": {"version": "test", "release_date": "test"}, "items": []}), encoding="utf-8")
        method_path.write_text(json.dumps({"object": {"name": "getMe", "description": "Returns a User object on success.", "annotations": []}}), encoding="utf-8")
        before = _tree_hash(methods)
        _run("scripts/sync_telegram_from_schema.py", "--schema", str(schema_path))
        middle = _tree_hash(methods)
        _run("scripts/sync_telegram_from_schema.py", "--schema", str(schema_path))
        after = _tree_hash(methods)
    assert middle == after
    assert before == middle
