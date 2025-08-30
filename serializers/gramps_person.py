from __future__ import annotations

from typing import Any, Dict, List


def _safe(obj: Any, name: str, default=None):
    f = getattr(obj, name, None)
    if callable(f):
        try:
            return f()
        except Exception:
            return default
    return f if f is not None else default


def _norm_str(x: Any) -> str:
    return "" if x is None else str(x)


def _serialize_name(n: Any) -> Dict[str, Any]:
    if n is None:
        return {"first_name": "", "type": "", "surnames": []}
    first = _norm_str(_safe(n, "get_first_name", ""))
    type_ = _norm_str(_safe(n, "get_type", ""))
    surnames: List[Dict[str, str]] = []
    get_surname_list = getattr(n, "get_surname_list", None)
    if callable(get_surname_list):
        for s in get_surname_list() or []:
            surnames.append(
                {
                    "text": _norm_str(_safe(s, "get_surname", "")),
                    "type": _norm_str(_safe(s, "get_origintype", "")),
                }
            )
    else:
        sn = _norm_str(_safe(n, "get_surname", ""))
        if sn:
            surnames.append({"text": sn, "type": ""})
    surnames.sort(key=lambda x: (x["text"], x["type"]))
    return {"first_name": first, "type": type_, "surnames": surnames}


def serialize_person(p: Any) -> Dict[str, Any]:
    pn = _safe(p, "get_primary_name", None)
    alt = _safe(p, "get_alternate_names", []) or []
    alt_list = [_serialize_name(n) for n in alt]
    alt_list.sort(
        key=lambda x: (
            x["surnames"][0]["text"] if x["surnames"] else "",
            x["first_name"],
            x["type"],
        )
    )
    evrefs = []
    for r in _safe(p, "get_event_ref_list", []) or []:
        evrefs.append(
            {
                "event": _norm_str(_safe(r, "get_reference_handle", "")),
                "role": _norm_str(_safe(r, "get_role", "")),
            }
        )
    evrefs.sort(key=lambda x: (x["event"], x["role"]))
    tags = [{"tag": _norm_str(t)} for t in (_safe(p, "get_tag_list", []) or [])]
    tags.sort(key=lambda x: x["tag"])
    refs = []
    for a in _safe(p, "get_person_ref_list", []) or []:
        refs.append(
            {
                "type": _norm_str(_safe(a, "get_relation", "")),
                "person": _norm_str(_safe(a, "get_reference_handle", "")),
                "citations": [_norm_str(c) for c in (_safe(a, "get_citation_list", []) or [])],
            }
        )
    refs.sort(key=lambda x: (x["type"], x["person"]))
    notes = [{"note": _norm_str(nh)} for nh in (_safe(p, "get_note_list", []) or [])]
    fams = [{"family": _norm_str(fh)} for fh in (_safe(p, "get_family_handle_list", []) or [])]
    return {
        "gid": _norm_str(_safe(p, "get_gramps_id", "")),
        "gender": _norm_str(_safe(p, "get_gender", "")),
        "primary_name": _serialize_name(pn),
        "alt_names": alt_list,
        "event_refs": evrefs,
        "tags": tags,
        "refs": refs,
        "notes": notes,
        "families": sorted(fams, key=lambda x: x["family"]),
    }
