"""Complete missing Google-style Args/Returns sections without changing code."""
from __future__ import annotations
import ast,pathlib,tokenize
ROOT=pathlib.Path(__file__).resolve().parents[1]/'src'/'peyk'
def public(n): return isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and not n.name.startswith('_')
def ann(a): return ast.unparse(a.annotation) if a.annotation else 'Any'
def params(n):
    xs=[(a.arg,ann(a)) for a in [*n.args.posonlyargs,*n.args.args,*n.args.kwonlyargs] if a.arg not in {'self','cls'}]
    if n.args.vararg: xs.append(('*'+n.args.vararg.arg,ann(n.args.vararg)))
    if n.args.kwarg: xs.append(('**'+n.args.kwarg.arg,ann(n.args.kwarg)))
    return xs
def replace_token(src,tok,doc):
    literal='"""'+doc.replace('\\','\\\\').replace('"""','\\"\\"\\"')+'"""'
    ls=literal.splitlines(); indent=' '*tok.start[1]
    return ls[0]+'\n'+'\n'.join(indent+x for x in ls[1:]) if len(ls)>1 else literal
for p in sorted(ROOT.rglob('*.py')):
    src=p.read_text(encoding='utf-8'); tree=ast.parse(src,filename=str(p)); lines=src.splitlines(True); offsets=[0]
    for l in lines: offsets.append(offsets[-1]+len(l))
    toks=list(tokenize.generate_tokens(iter(lines).__next__)); by_start={(t.start[0],t.start[1]):t for t in toks if t.type==tokenize.STRING}; edits=[]
    for n in ast.walk(tree):
        if not public(n): continue
        d=ast.get_docstring(n,clean=False)
        if not d: continue
        additions=''
        ps=params(n)
        if ps and 'Args:' not in d:
            additions+='\n\nArgs:\n'+''.join(f'    {a}: Parameter of type ``{t}``.\n' for a,t in ps)
        if 'Returns:' not in d and 'Yields:' not in d:
            r=ast.unparse(n.returns) if n.returns else 'Any'; additions+=f'\n\nReturns:\n    The operation result (``{r}``).\n'
        if not additions: continue
        first=n.body[0]; tok=by_start.get((first.lineno,first.col_offset))
        if tok is None: raise RuntimeError(f'Cannot locate docstring: {p}:{n.lineno}:{n.name}')
        a=offsets[tok.start[0]-1]+tok.start[1]; b=offsets[tok.end[0]-1]+tok.end[1]
        edits.append((a,b,replace_token(src,tok,d+additions)))
    out=src
    for a,b,repl in sorted(edits,reverse=True): out=out[:a]+repl+out[b:]
    if out!=src: p.write_text(out,encoding='utf-8')
print('Completed missing Google-style Args/Returns sections.')
