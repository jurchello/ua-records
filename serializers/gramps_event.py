from __future__ import annotations
from typing import Any, Dict, List

def _norm_str(x: Any) -> str:
    return "" if x is None else str(x)

def _normalize_date(d: Any) -> Dict[str, Any]:
    if d is None:
        return {"text":"","yyyy":None,"mm":None,"dd":None,"mod":"","qual":"","cal":"","span":{}}
    span = {}
    gs = getattr(d,"get_start_date",None)
    ge = getattr(d,"get_stop_date",None)
    if callable(gs) and callable(ge):
        s = gs()
        e = ge()
        span = {
            "start": {"yyyy":s[2] if s and len(s) > 2 else None,"mm":s[1] if s and len(s) > 1 else None,"dd":s[0] if s and len(s) > 0 else None} if s else {},
            "end":   {"yyyy":e[2] if e and len(e) > 2 else None,"mm":e[1] if e and len(e) > 1 else None,"dd":e[0] if e and len(e) > 0 else None} if e else {},
        }
    return {
        "text":_norm_str(getattr(d,"get_text",lambda:"")()),
        "yyyy":getattr(d,"get_year",lambda:None)(),
        "mm":getattr(d,"get_month",lambda:None)(),
        "dd":getattr(d,"get_day",lambda:None)(),
        "mod":_norm_str(getattr(d,"get_modifier",lambda:"")()),
        "qual":_norm_str(getattr(d,"get_quality",lambda:"")()),
        "cal":_norm_str(getattr(d,"get_calendar",lambda:"")()),
        "span":span,
    }

def serialize_event(e: Any) -> Dict[str, Any]:
    d = getattr(e,"get_date_object",lambda:None)()
    place_h = getattr(e,"get_place_handle",lambda:None)()
    citations = [_norm_str(ch) for ch in (getattr(e,"get_citation_list",lambda:[])() or [])]
    attrs = []
    for a in (getattr(e,"get_attribute_list",lambda:[])() or []):
        attrs.append({"type":_norm_str(getattr(a,"get_type",lambda:"")()),"value":_norm_str(getattr(a,"get_value",lambda:"")())})
    return {
        "gid":_norm_str(getattr(e,"get_gramps_id",lambda:"")()),
        "type":_norm_str(getattr(e,"get_type",lambda:"")()),
        "date":_normalize_date(d),
        "place":{"place":_norm_str(place_h)} if place_h else {},
        "description":_norm_str(getattr(e,"get_description",lambda:"")()),
        "citations":sorted(citations),
        "attributes":sorted(attrs,key=lambda x:(x["type"],x["value"])),
    }