from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

@dataclass
class FlatRow:
    section: str          # "new" | "modified" | "deleted"
    kind: str
    handle: str
    path: str             # dotted path (with [id] for list items)
    before: str
    after: str
    status: int           # 0 same, 1 removed, 2 added, 3 changed

def _to_scalar(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v,(str,int,float,bool)):
        return str(v)
    return str(v)

def _flatten(obj: Any, prefix: str="", id_keys: Tuple[str,...]=("handle","id","gid")) -> Dict[str,str]:
    out: Dict[str,str] = {}
    if isinstance(obj, dict):
        for k in sorted(obj.keys()):
            nk = f"{prefix}.{k}" if prefix else k
            sub = _flatten(obj[k], nk, id_keys)
            if sub:
                out.update(sub)
            else:
                out[nk] = _to_scalar(obj[k])
        return out
    if isinstance(obj, list):
        keyed, scalar = {}, []
        for it in obj:
            if isinstance(it, dict):
                key = next((str(it.get(k)) for k in id_keys if it.get(k) is not None), None)
                if key is not None:
                    keyed[key] = it
                    continue
            scalar.append(_to_scalar(it))
        for key in sorted(keyed.keys()):
            nk = f"{prefix}[{key}]"
            out.update(_flatten(keyed[key], nk, id_keys))
        if scalar:
            for idx, val in enumerate(sorted(scalar)):
                nk = f"{prefix}[{idx}]"
                out[nk] = val
        return out
    out[prefix] = _to_scalar(obj)
    return out

def _rows_for_item(section: str, kind: str, handle: str, before: Dict[str,Any], after: Dict[str,Any]) -> List[FlatRow]:
    a = _flatten(before)
    b = _flatten(after)
    keys = sorted(set(a.keys())|set(b.keys()))
    rows: List[FlatRow] = []
    for k in keys:
        va = a.get(k,"")
        vb = b.get(k,"")
        status = 0 if va==vb else (1 if va and not vb else (2 if vb and not va else 3))
        rows.append(FlatRow(section,kind,handle,k,va,vb,status))
    return rows

def flatten_preview(preview: Dict[str,List[Dict[str,Any]]]) -> List[FlatRow]:
    rows: List[FlatRow] = []
    for sec in ("new","modified","deleted"):
        for item in preview.get(sec,[]):
            kind = item["kind"]
            handle = item["handle"]
            before = item.get("before",{}) or {}
            after = item.get("after",{}) or {}
            rows.extend(_rows_for_item(sec,kind,handle,before,after))
    return rows