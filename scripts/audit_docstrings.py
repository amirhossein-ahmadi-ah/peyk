"""Fail when public API documentation is missing or contains generator placeholders."""
from __future__ import annotations
import ast
import pathlib
import re
import sys
ROOT = pathlib.Path(__file__).resolve().parents[1] / "src" / "peyk"
PATTERNS = ("Parameter of type", "Execute the ``", "See the method signature", "None explicitly raised", "Perform `..`", "extracted verbatim from the legacy", "Implement the Rubika client method")
STOP = {"Returns:", "Raises:", "Examples:", "Yields:", "Attributes:"}
fail: list[str] = []
count = 0
class Visitor(ast.NodeVisitor):
    def __init__(self, path: pathlib.Path) -> None:
        self.path=path; self.class_depth=0; self.function_depth=0
    def visit_ClassDef(self,n:ast.ClassDef)->None:
        global count
        if not n.name.startswith("_"):
            count += 1; self.check(n)
        self.class_depth += 1
        for child in n.body: self.visit(child)
        self.class_depth -= 1
    def visit_FunctionDef(self,n:ast.FunctionDef)->None:
        global count
        if self.function_depth: return
        if not n.name.startswith("_"):
            count += 1; self.check(n)
        self.function_depth += 1
        for child in n.body: self.visit(child)
        self.function_depth -= 1
    def visit_AsyncFunctionDef(self,n:ast.AsyncFunctionDef)->None:
        global count
        if self.function_depth: return
        if not n.name.startswith("_"):
            count += 1; self.check(n)
        self.function_depth += 1
        for child in n.body: self.visit(child)
        self.function_depth -= 1
    def check(self,n:ast.AST)->None:
        doc=ast.get_docstring(n)
        if not doc:
            fail.append(f"{self.path}:{getattr(n,'lineno',0)}:{getattr(n,'name','<symbol>')}: missing docstring"); return
        for pat in PATTERNS:
            if pat in doc: fail.append(f"{self.path}:{getattr(n,'lineno',0)}:{getattr(n,'name','<symbol>')}: placeholder {pat!r}")
        lines=doc.splitlines()
        try:i=next(i for i,x in enumerate(lines) if x.strip()=="Args:")+1
        except StopIteration:return
        while i<len(lines) and lines[i].strip() not in STOP:
            m=re.match(r'^\s{4}([*\w][\w*]*):\s*(.*)$',lines[i])
            if m and not m.group(2).strip(): fail.append(f"{self.path}:{getattr(n,'lineno',0)}:{getattr(n,'name','<symbol>')}: Args entry without description")
            i+=1
for p in sorted(ROOT.rglob("*.py")):
    try: Visitor(p).visit(ast.parse(p.read_text(encoding="utf-8"),filename=str(p)))
    except SyntaxError as e: fail.append(f"{p}: syntax error: {e}")
print(f"Scanned {len(list(ROOT.rglob('*.py')))} Python modules and {count} public classes/functions/methods.")
if fail:
    print(f"FAIL: {len(fail)} documentation issues."); print("\n".join(fail)); raise SystemExit(1)
print("PASS: public docstring coverage and placeholder audit.")
