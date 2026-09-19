"""Complete Google-style Raises sections where code explicitly raises."""
from __future__ import annotations
import ast,pathlib,tokenize
ROOT=pathlib.Path(__file__).resolve().parents[1]/'src'/'peyk'
def public(n): return isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and not n.name.startswith('_')
def names(n):
 out=[]
 for c in ast.walk(n):
  if isinstance(c,ast.Raise) and c.exc is not None:
   x=ast.unparse(c.exc.func) if isinstance(c.exc,ast.Call) else ast.unparse(c.exc)
   if x not in out: out.append(x)
 return out
def offsets(s):
 o=[0]
 for l in s.splitlines(True): o.append(o[-1]+len(l))
 return o
for p in sorted(ROOT.rglob('*.py')):
 src=p.read_text(); tree=ast.parse(src); off=offsets(src); toks=list(tokenize.generate_tokens(iter(src.splitlines(True)).__next__)); by={(t.start[0],t.start[1]):t for t in toks if t.type==tokenize.STRING}; edits=[]
 for n in ast.walk(tree):
  if not public(n): continue
  d=ast.get_docstring(n,clean=False) or ''; rs=names(n)
  if not rs or 'Raises:' in d: continue
  d += '\n\nRaises:\n' + ''.join(f'    {x}: Raised when the operation cannot complete.\n' for x in rs)
  first=n.body[0]; tok=by[(first.lineno,first.col_offset)]; a=off[tok.start[0]-1]+tok.start[1]; b=off[tok.end[0]-1]+tok.end[1]
  lit='"""'+d.replace('\\','\\\\').replace('"""','\\"\\"\\"')+'"""'; ls=lit.splitlines(); indent=' '*tok.start[1]; repl=ls[0]+'\n'+'\n'.join(indent+x for x in ls[1:])
  edits.append((a,b,repl))
 out=src
 for a,b,r in sorted(edits,reverse=True): out=out[:a]+r+out[b:]
 if out!=src: p.write_text(out)
print('Completed explicit Raises sections.')
