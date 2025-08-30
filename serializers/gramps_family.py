from __future__ import annotations

from typing import Any, Dict


def _norm_str(x: Any) -> str:
    return "" if x is None else str(x)


def serialize_family(f: Any) -> Dict[str, Any]:
    husband = _norm_str(getattr(f, "get_father_handle", lambda: None)() or "")
    wife = _norm_str(getattr(f, "get_mother_handle", lambda: None)() or "")
    spouses = [{"person": h} for h in [husband, wife] if h]
    # event refs
    ev_refs = []
    get_evrefs = getattr(f, "get_event_ref_list", None)
    if callable(get_evrefs):
        for r in get_evrefs() or []:
            ev_refs.append(
                {
                    "event": _norm_str(getattr(r, "get_reference_handle", lambda: "")()),
                    "role": _norm_str(getattr(r, "get_role", lambda: "")()),
                }
            )
    ev_refs.sort(key=lambda x: (x["event"], x["role"]))
    return {
        "gid": _norm_str(getattr(f, "get_gramps_id", lambda: "")()),
        "spouses": spouses,
        "event_refs": ev_refs,
    }
