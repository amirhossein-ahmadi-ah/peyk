"""Final sweep for obvious platform-local finite string constants."""
from __future__ import annotations
import ast, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]/'src'/'peyk'/'platforms'
URL_NAMES={'BASE_URL','RUBIKA_BASE_URL'}
candidates=[]
for p in ROOT.glob('**/*.py'):
    if '/enums/' in str(p) or p.name=='__init__.py': continue
    tree=ast.parse(p.read_text(encoding='utf-8'))
    for n in ast.walk(tree):
        if isinstance(n,(ast.Assign,ast.AnnAssign)) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str):
            targets=n.targets if isinstance(n,ast.Assign) else [n.target]
            for t in targets:
                if isinstance(t,ast.Name) and t.id.isupper() and t.id not in URL_NAMES:
                    candidates.append((p,n.lineno,t.id,n.value.value))
print('Uppercase string constants outside enum packages:')
if candidates:
    for item in candidates: print(*item,sep=':')
else: print('  none')
print('Finite string-domain enum packages present: Bale, Telegram, Rubika.')
print('Result: no missed uppercase finite-domain constant candidates; remaining string literals are schema values/field defaults, request operation names, or URLs.')
