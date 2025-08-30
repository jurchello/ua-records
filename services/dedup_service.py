from __future__ import annotations

from typing import Any, Callable, Dict, Tuple

VH_PREFIX = "VH:"


def dedup_virtuals(
    after: Dict[Tuple[str, str], Dict[str, Any]],
    finder: Callable[[str, Dict[str, Any]], str | None],
) -> tuple[Dict[Tuple[str, str], Dict[str, Any]], Dict[str, str]]:
    """Try to replace some VH oids by existing H handles using `finder(kind, data)->handle|None`.
    Returns (updated_after, vh_to_h_map).
    """
    out: Dict[Tuple[str, str], Dict[str, Any]] = {}
    vh_to_h: Dict[str, str] = {}
    for (kind, oid), data in after.items():
        if oid.startswith(VH_PREFIX):
            h = finder(kind, data)
            if h:
                vh_to_h[oid] = h
                out[(kind, h)] = data
            else:
                out[(kind, oid)] = data
        else:
            out[(kind, oid)] = data
    return out, vh_to_h
