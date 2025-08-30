from __future__ import annotations

from typing import Any, Dict, List, Tuple


def deep_diff(a: Any, b: Any, *, id_keys: Tuple[str, ...] = ("handle", "id", "gid")) -> Dict[str, Any]:
    if a == b:
        return {}

    if isinstance(a, dict) and isinstance(b, dict):
        out: Dict[str, Any] = {}
        keys = set(a.keys()) | set(b.keys())
        for k in sorted(keys):
            d = deep_diff(a.get(k), b.get(k), id_keys=id_keys)
            if d:
                out[k] = d
        return out

    if isinstance(a, list) and isinstance(b, list):
        if all(not isinstance(x, (dict, list)) for x in a + b):
            sa, sb = set(map(str, a)), set(map(str, b))
            diff: Dict[str, Any] = {}
            rem, add = sorted(sa - sb), sorted(sb - sa)
            if rem:
                diff["removed"] = rem
            if add:
                diff["added"] = add
            return diff or {}

        def to_map(lst: List[Any]):
            m, rest = {}, []
            for it in lst:
                if isinstance(it, dict):
                    key = next((it.get(k) for k in id_keys if it.get(k) is not None), None)
                    if key is not None:
                        m[str(key)] = it
                        continue
                rest.append(it)
            return m, rest

        ma, ra = to_map(a)
        mb, rb = to_map(b)

        map_diff: Dict[str, Any] = {}
        rem = [ma[k] for k in ma.keys() - mb.keys()]
        add = [mb[k] for k in mb.keys() - ma.keys()]
        if rem:
            map_diff["removed"] = rem
        if add:
            map_diff["added"] = add

        chg: Dict[str, Any] = {}
        for k in sorted(ma.keys() & mb.keys()):
            d = deep_diff(ma[k], mb[k], id_keys=id_keys)
            if d:
                chg[k] = d
        if chg:
            map_diff["changed"] = chg

        if ra or rb:
            sa, sb = set(map(str, ra)), set(map(str, rb))
            only_a = sorted(sa - sb)
            only_b = sorted(sb - sa)
            if only_a:
                map_diff.setdefault("removed", []).extend(only_a)
            if only_b:
                map_diff.setdefault("added", []).extend(only_b)

        return map_diff or {}

    return {"from": a, "to": b}
