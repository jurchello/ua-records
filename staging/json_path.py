from __future__ import annotations
from typing import Any, Dict, List, Tuple
from schema_types import ID_KEYS

def parse_path(path: str) -> List[Tuple[str, str | None]]:
    """Parse dotted paths with optional [key] selectors into segments.
    Returns list of (field, key) where key=None for scalar/obj, or str for keyed list.
    Example: 'primary_name.surnames[Петренко].type' ->
        [('primary_name', None), ('surnames', 'Петренко'), ('type', None)]
    """
    out: List[Tuple[str, str | None]] = []
    i = 0
    cur = ''
    key = None
    while i < len(path):
        c = path[i]
        if c == '.':
            if cur:
                out.append((cur, key))
                cur, key = '', None
            i += 1
            continue
        if c == '[':
            j = path.find(']', i+1)
            if j == -1:
                raise ValueError(f"Unmatched '[' in path: {path}")
            key = path[i+1:j]
            i = j + 1
            continue
        cur += c
        i += 1
    if cur:
        out.append((cur, key))
    return out

def _ensure_keyed_item(lst: List[Any], key: str) -> Dict[str, Any]:
    # find by any of ID_KEYS
    for it in lst:
        if isinstance(it, dict):
            for k in ID_KEYS:
                v = it.get(k)
                if v is not None and str(v) == key:
                    return it
    obj: Dict[str, Any] = {}
    # choose first ID_KEYS name as storage key
    obj[ID_KEYS[0]] = key
    lst.append(obj)
    return obj

def set_at_path(root: Dict[str, Any], path: str, value: Any) -> None:
    segs = parse_path(path)
    cur: Any = root
    for idx, (field, key) in enumerate(segs):
        last = idx == len(segs) - 1
        if key is None:
            if last:
                cur[field] = value
                return
            if field not in cur or not isinstance(cur[field], (dict, list)):
                cur[field] = {}
            cur = cur[field]
        else:
            # ensure list
            if field not in cur or not isinstance(cur[field], list):
                cur[field] = []
            lst: List[Any] = cur[field]
            item = _ensure_keyed_item(lst, key)
            if last:
                # replace whole dict for keyed item if value is dict, else set to scalar key
                if isinstance(value, dict):
                    item.clear()
                    item.update(value)
                else:
                    # store scalar under 'value'
                    item['value'] = value
                return
            cur = item

def delete_object(objs: Dict[str, Dict[str, Any]], oid: str) -> None:
    if oid in objs:
        del objs[oid]