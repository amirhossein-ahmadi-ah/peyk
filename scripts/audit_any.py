"""Audit public typing hazards and enforce a checked-in ratchet baseline.

The audit deliberately measures only source files under ``src/peyk``. The
baseline is a per-module snapshot so existing debt can be reduced incrementally
without allowing a module to regress or a new module to introduce debt.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "peyk"
BASELINE = ROOT / "scripts" / "any_baseline.json"
ALLOWLIST = ROOT / "scripts" / "any_allowlist.json"


class Counts(dict[str, int]):
    """Per-module counts emitted by the audit."""


def _is_public(name: str) -> bool:
    return not name.startswith("_")


def _annotation_has_any(node: ast.AST | None) -> bool:
    return any(isinstance(item, ast.Name) and item.id == "Any" for item in ast.walk(node)) if node else False


def _is_bare_dict(node: ast.AST | None) -> bool:
    return isinstance(node, ast.Name) and node.id == "dict"


def _audit_module(path: Path) -> Counts:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    counts = Counts(any=0, bare_dict=0, unannotated_parameters=0, unannotated_returns=0)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if _is_public(node.name):
                arguments: Iterable[ast.arg] = (
                    *node.args.posonlyargs,
                    *node.args.args,
                    *node.args.kwonlyargs,
                )
                for argument in arguments:
                    if argument.arg not in {"self", "cls"} and argument.annotation is None:
                        counts["unannotated_parameters"] += 1
                if node.args.vararg is not None and node.args.vararg.annotation is None:
                    counts["unannotated_parameters"] += 1
                if node.args.kwarg is not None and node.args.kwarg.annotation is None:
                    counts["unannotated_parameters"] += 1
                if node.returns is None:
                    counts["unannotated_returns"] += 1

            for argument in (
                *node.args.posonlyargs,
                *node.args.args,
                *node.args.kwonlyargs,
            ):
                if argument.arg != "raw" and _annotation_has_any(argument.annotation):
                    counts["any"] += 1
                if _is_bare_dict(argument.annotation):
                    counts["bare_dict"] += 1
            if node.args.vararg is not None:
                if node.args.vararg.arg != "raw" and _annotation_has_any(node.args.vararg.annotation):
                    counts["any"] += 1
                if _is_bare_dict(node.args.vararg.annotation):
                    counts["bare_dict"] += 1
            if node.args.kwarg is not None:
                if node.args.kwarg.arg != "raw" and _annotation_has_any(node.args.kwarg.annotation):
                    counts["any"] += 1
                if _is_bare_dict(node.args.kwarg.annotation):
                    counts["bare_dict"] += 1
            if _annotation_has_any(node.returns):
                counts["any"] += 1
            if _is_bare_dict(node.returns):
                counts["bare_dict"] += 1
        elif isinstance(node, ast.AnnAssign):
            is_raw = isinstance(node.target, ast.Name) and node.target.id == "raw"
            if not is_raw and _annotation_has_any(node.annotation):
                counts["any"] += 1
            if _is_bare_dict(node.annotation):
                counts["bare_dict"] += 1

    return counts


def audit() -> dict[str, Counts]:
    modules: dict[str, Counts] = {}
    for path in sorted(SRC.rglob("*.py")):
        relative = path.relative_to(SRC).with_suffix("")
        module = "peyk." + ".".join(relative.parts)
        modules[module] = _audit_module(path)
    return modules


def _load_baseline() -> dict[str, Counts]:
    if not BASELINE.exists():
        return {}
    raw = json.loads(BASELINE.read_text(encoding="utf-8"))
    return {module: Counts(values) for module, values in raw.items()}


def _print_table(current: dict[str, Counts]) -> None:
    headers = ("module", "Any", "bare dict", "unannotated params", "unannotated returns")
    print(" | ".join(headers))
    print("-+-".join("-" * len(header) for header in headers))
    for module, counts in current.items():
        print(
            f"{module} | {counts['any']} | {counts['bare_dict']} | "
            f"{counts['unannotated_parameters']} | {counts['unannotated_returns']}"
        )


def main() -> int:
    current = audit()
    baseline = _load_baseline()
    allowlist = json.loads(ALLOWLIST.read_text(encoding="utf-8")) if ALLOWLIST.exists() else []
    failures: list[str] = []

    for module, counts in current.items():
        previous = baseline.get(module)
        if previous is None:
            if sum(counts.values()) > 0:
                failures.append(f"new module has typing debt: {module}")
            continue
        for key, value in counts.items():
            if value > previous.get(key, 0):
                failures.append(
                    f"{module}: {key} increased from {previous.get(key, 0)} to {value}"
                )

    if allowlist:
        print("\nAny allow-list entries:")
        for entry in allowlist: print(f"- {entry}")
    for module, counts in current.items():
        if counts["any"] > 0 and module not in {str(e.get("module")) for e in allowlist if isinstance(e, dict)}:
            failures.append(f"public Any is not allow-listed: {module}")
    _print_table(current)
    if failures:
        print("\nTyping ratchet failures:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
