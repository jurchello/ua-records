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
        return {"first_name":"","type":"","surnames":[]}
    first = _norm_str(_safe(n,"get_first_name",""))
    type_ = _norm_str(_safe(n,"get_type",""))
    surnames: List[Dict[str,str]] = []
    get_surname_list = getattr(n,"get_surname_list",None)
    if callable(get_surname_list):
        for s in get_surname_list() or []:
            surnames.append({"text":_norm_str(_safe(s,"get_surname","")),"type":_norm_str(_safe(s,"get_origintype",""))})
    else:
        sn = _norm_str(_safe(n,"get_surname",""))
        if sn:
            surnames.append({"text":sn,"type":""})
    surnames.sort(key=lambda x:(x["text"],x["type"]))
    return {"first_name":first,"type":type_,"surnames":surnames}

def serialize_person(p: Any) -> Dict[str, Any]:
    pn = _safe(p,"get_primary_name",None)
    alt = _safe(p,"get_alternate_names",[]) or []
    alt_list = [_serialize_name(n) for n in alt]
    alt_list.sort(key=lambda x:(x["surnames"][0]["text"] if x["surnames"] else "", x["first_name"], x["type"]))
    evrefs = []
    for r in (_safe(p,"get_event_ref_list",[]) or []):
        evrefs.append({"event":_norm_str(_safe(r,"get_reference_handle","")),"role":_norm_str(_safe(r,"get_role",""))})
    evrefs.sort(key=lambda x:(x["event"],x["role"]))
    tags = [{"tag":_norm_str(t)} for t in (_safe(p,"get_tag_list",[]) or [])]
    tags.sort(key=lambda x:x["tag"])
    refs = []
    for a in (_safe(p,"get_person_ref_list",[]) or []):
        refs.append({"type":_norm_str(_safe(a,"get_relation","")),"person":_norm_str(_safe(a,"get_reference_handle","")),"citations":[_norm_str(c) for c in (_safe(a,"get_citation_list",[]) or [])]})
    refs.sort(key=lambda x:(x["type"],x["person"]))
    notes = [{"note":_norm_str(nh)} for nh in (_safe(p,"get_note_list",[]) or [])]
    fams = [{"family":_norm_str(fh)} for fh in (_safe(p,"get_family_handle_list",[]) or [])]
    return {
        "gid":_norm_str(_safe(p,"get_gramps_id","")),
        "gender":_norm_str(_safe(p,"get_gender","")),
        "primary_name":_serialize_name(pn),
        "alt_names":alt_list,
        "event_refs":evrefs,
        "tags":tags,
        "refs":refs,
        "notes":notes,
        "families":sorted(fams,key=lambda x:x["family"]),
    }

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