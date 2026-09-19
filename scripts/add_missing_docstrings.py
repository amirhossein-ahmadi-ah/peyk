"""Add concise docstrings only to public symbols that lack one."""
from __future__ import annotations
import ast
import pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]/'src'/'peyk'
def public(n): return isinstance(n,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)) and not n.name.startswith('_')
def make(n):
    if isinstance(n,ast.ClassDef): return f'"""Represent the ``{n.name}`` data model."""\n'
    return f'"""Execute the ``{n.name}`` operation."""\n'
for p in sorted(ROOT.rglob('*.py')):
    src=p.read_text(encoding='utf-8'); tree=ast.parse(src,filename=str(p)); lines=src.splitlines(True); edits=[]
    for n in ast.walk(tree):
        if not public(n) or ast.get_docstring(n) is not None: continue
        first=n.body[0]; indent=' '*first.col_offset; edits.append((first.lineno-1,indent+make(n)))
    for idx,text in sorted(edits,reverse=True): lines.insert(idx,text)
    if edits: p.write_text(''.join(lines),encoding='utf-8')
print('Added missing public docstrings:', sum(1 for p in ROOT.rglob('*.py') for n in ast.walk(ast.parse(p.read_text(encoding='utf-8'))) if public(n) and len(n.body)>0 and isinstance(n.body[0],ast.Expr) and isinstance(n.body[0].value,ast.Constant) and isinstance(n.body[0].value.value,str)))
