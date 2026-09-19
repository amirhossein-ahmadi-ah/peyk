"""Synchronize Telegram method annotations and documentation from Butcher schema data.

The supplied Butcher schema is the offline source of truth for method names,
parameter descriptions, and type descriptions.  The 10.2 schema currently
stores method return information in prose rather than a structured ``returning``
field, so this script extracts only explicit documented return types and records
ambiguous union cases explicitly.  It never invents a platform capability.
"""
from __future__ import annotations
import argparse, ast, html, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def find_schema(explicit: Path|None)->Path:
    candidates=[explicit] if explicit else []
    candidates += [Path(r"D:\aiogram\.butcher\schema\schema.json"), ROOT.parent/"aiogram"/".butcher"/"schema"/"schema.json"]
    for path in candidates:
        if path and path.is_file(): return path
    raise FileNotFoundError("aiogram .butcher/schema/schema.json was not found")

def plain(value:str)->str:
    value=html.unescape(value or "")
    value=re.sub(r"<br\s*/?>","\n",value,flags=re.I); value=re.sub(r"<[^>]+>","",value)
    value=re.sub(r":(?:code|class|meth):`([^`]+)`",r"\1",value)
    value=re.sub(r"`([^`]+?) <[^>]+>`_",r"\1",value)
    value=re.sub(r"\*\*([^*]+)\*\*",r"\1",value); value=re.sub(r"\*([^*]+)\*",r"\1",value)
    return re.sub(r"\n{3,}","\n\n",value).strip()

def snake(name:str)->str:return re.sub(r"(?<!^)(?=[A-Z])","_",name).lower()

OVERRIDES={
 "getMyCommands":"List[BotCommand]", "getUpdates":"List[Update]", "getUserPersonalChatMessages":"List[Message]",
 "getForumTopicIconStickers":"List[Sticker]", "getCustomEmojiStickers":"List[Sticker]", "getGameHighScores":"List[GameHighScore]",
 "sendMediaGroup":"List[Message]", "copyMessages":"List[MessageId]", "forwardMessages":"List[MessageId]",
 "editMessageText":"Union[Message, bool]", "editMessageCaption":"Union[Message, bool]", "editMessageReplyMarkup":"Union[Message, bool]",
 "editMessageMedia":"Union[Message, bool]", "editMessageLiveLocation":"Union[Message, bool]", "setGameScore":"Union[Message, bool]",
 "stopMessageLiveLocation":"Union[Message, bool]", "answerGuestQuery":"SentGuestMessage", "answerWebAppQuery":"SentWebAppMessage",
}

def infer_return(name:str,desc:str)->str|None:
    if name in OVERRIDES:return OVERRIDES[name]
    d=desc.replace("\n"," ")
    if re.search(r"\bTrue (?:on success|is returned)|Returns True\b",d,re.I):return "bool"
    if re.search(r"\bInteger on success\b",d,re.I):return "int"
    if re.search(r"\bString on success\b|token as String\b|as String on success",d,re.I):return "str"
    for pat in (r"Array of ([A-Za-z][A-Za-z0-9_]*) objects?",r"an Array of ([A-Za-z][A-Za-z0-9_]*)"):
        m=re.search(pat,d,re.I)
        if m:return f"List[{m.group(1)}]"
    m=re.search(r"(?:a|an|the|sent|edited|stopped|created|uploaded|revoked|new)\s+([A-Z][A-Za-z0-9_]*)\s+(?:object\s+)?(?:on success|is returned|object is returned)",d,re.I)
    if m:return m.group(1)
    m=re.search(r"form of (?:a|an)\s+([A-Z][A-Za-z0-9_]*) object",d)
    return m.group(1) if m else None

def sync_method(path:Path,obj:dict)->bool:
    tree=ast.parse(path.read_text(encoding="utf-8")); target=snake(obj["name"]); changed=False
    desc=plain(obj.get("description","")); docs={a.get("name"):plain(a.get("description","")) for a in obj.get("annotations",[]) if a.get("name")}
    ret=infer_return(obj["name"],obj.get("description",""))
    class V(ast.NodeTransformer):
        def visit_AsyncFunctionDef(self,node):
            nonlocal changed
            if node.name==target:
                lines=[desc]
                args=[a for a in [*node.args.posonlyargs,*node.args.args,*node.args.kwonlyargs] if a.arg!="self"]
                if args:
                    lines += ["", "Args:"]+[f"    {a.arg}: {docs.get(a.arg) or 'Value accepted by this operation.'}" for a in args]
                if ret: lines += ["", "Returns:",f"    {ret}: Result returned by Telegram on successful execution."]
                newdoc="\n".join(lines)
                if ast.get_docstring(node,clean=False)!=newdoc: node.body[0]=ast.Expr(value=ast.Constant(value=newdoc)); changed=True
                if ret and ast.unparse(node.returns)!=ret: node.returns=ast.parse(ret,mode="eval").body; changed=True
            return node
    new=V().visit(tree); ast.fix_missing_locations(new)
    if changed:path.write_text(ast.unparse(new)+"\n",encoding="utf-8")
    return changed

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--schema",type=Path); ap.add_argument("--check",action="store_true"); args=ap.parse_args()
    schema=json.loads(find_schema(args.schema).read_text(encoding="utf-8")); methods={}
    for p in (find_schema(args.schema).parent.parent/"methods").glob("*/entity.json"):
        methods[p.parent.name]=json.loads(p.read_text(encoding="utf-8"))["object"]
    changed=0; missing=[]
    for name,obj in sorted(methods.items()):
        path=ROOT/"src/peyk/platforms/telegram/methods"/f"{snake(name)}.py"
        if not path.exists():
            # Some shared Telegram-like methods are intentionally inherited.
            inherited=ROOT/"src/peyk/platforms/_telegram_like/base_client.py"
            text=inherited.read_text(encoding="utf-8") if inherited.exists() else ""
            if re.search(rf"\bdef\s+{re.escape(snake(name))}\b", text): continue
            missing.append(name); continue
        if not args.check and sync_method(path,obj): changed+=1
    # Verify type field names without mutating them.  These are compatibility-sensitive.
    type_mismatches=[]
    project_types=ROOT/"src/peyk/platforms/telegram/types"
    project_fields={}
    for tp in project_types.glob("*.py"):
        try: tree=ast.parse(tp.read_text(encoding="utf-8"))
        except SyntaxError: continue
        for cls in [n for n in tree.body if isinstance(n,ast.ClassDef)]:
            project_fields[cls.name]={n.target.id for n in cls.body if isinstance(n,ast.AnnAssign) and isinstance(n.target,ast.Name)}
    for tp in (find_schema(args.schema).parent.parent/"types").glob("*/entity.json"):
        obj=json.loads(tp.read_text(encoding="utf-8"))["object"]; sf={a["name"] for a in obj.get("annotations",[]) if a.get("name")}
        pf=project_fields.get(obj["name"])
        if pf is not None and sf != pf: type_mismatches.append((obj["name"],sorted(sf-pf),sorted(pf-sf)))
    print(f"Telegram schema API: {schema['api']['version']} ({schema['api']['release_date']})")
    print(f"Schema methods: {len(methods)}; local method modules: {len(list((ROOT/'src/peyk/platforms/telegram/methods').glob('*.py')))}")
    local_public=set()
    for mp in (ROOT/"src/peyk/platforms/telegram/methods").glob("*.py"):
        try: tree=ast.parse(mp.read_text(encoding="utf-8"))
        except SyntaxError: continue
        local_public |= {n.name for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and not n.name.startswith("_")}
    inherited_tree=ast.parse((ROOT/"src/peyk/platforms/_telegram_like/base_client.py").read_text(encoding="utf-8"))
    inherited=set()
    for cls in [n for n in inherited_tree.body if isinstance(n,ast.ClassDef) and n.name == "TelegramLikeClient"]:
        inherited={n.name for n in cls.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and not n.name.startswith("_")}
    extras=sorted((local_public|inherited)-{snake(n) for n in methods})
    print(f"Schema methods missing local implementation: {len(missing)}")
    if missing: print("  "+", ".join(missing))
    print(f"Local/shared public method names not present in schema: {len(extras)}")
    if extras: print("  "+", ".join(extras))
    print(f"Changed files: {changed}")
    print(f"Type field-structure mismatches (reported, not auto-fixed): {len(type_mismatches)}")
    for name,schema_only,local_only in type_mismatches[:20]:
        print(f"  {name}: schema-only={schema_only}; local-only={local_only}")
    if args.check and missing:return 1
    return 0
if __name__=="__main__":raise SystemExit(main())
