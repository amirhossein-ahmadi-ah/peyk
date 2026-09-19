"""Audit source/examples for legacy platform module imports.

Tests and compatibility documentation are allowed to reference legacy paths
because those imports are intentionally preserved by the re-export facades.
Production source and examples should use the restructured namespaces.
"""
from __future__ import annotations
import pathlib,re,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
scan=[ROOT/'src',ROOT/'scripts',ROOT/'docs']
pat=re.compile(r'peyk\.platforms\.(bale|telegram|rubika)\.(models|client)')
allowed_files={ROOT/'docs/STRUCTURAL_REFACTOR_S3_NOTES.md',ROOT/'docs/STRUCTURAL_REFACTOR_S4_NOTES.md',ROOT/'docs/STRUCTURAL_REFACTOR_S5_NOTES.md',ROOT/'docs/STRUCTURAL_REFACTOR_S6_NOTES.md',ROOT/'docs_internal/decisions.md'}
found=[]
for base in scan:
    if not base.exists(): continue
    for p in base.rglob('*'):
        if not p.is_file() or p.suffix in {'.pyc','.html'} or p in allowed_files: continue
        try:s=p.read_text(encoding='utf-8')
        except UnicodeDecodeError:continue
        for i,line in enumerate(s.splitlines(),1):
            if pat.search(line): found.append((p,i,line.strip()))
print(f'Scanned {sum(1 for b in scan if b.exists())} source/example roots.')
if found:
    print('FAIL: unexpected legacy import-path references:')
    for x in found: print(*x,sep=':')
    sys.exit(1)
print('PASS: no unexpected legacy import-path references; compatibility-only references remain intentionally isolated.')
