from __future__ import annotations
from typing import Any, Dict
from .apply_helpers import set_if

def build_person(data: Dict[str,Any]) -> Any:
    # Replace with factory constructing a real Gramps Person.
    # For tests you can provide data["_obj_factory"] that returns a dummy object.
    return data.get("_obj_factory", lambda: {})()

def patch_person(obj: Any, data: Dict[str,Any]) -> None:
    # Map JSON fields to your real Gramps setters
    if "gender" in data:
        set_if(obj, "gender", data["gender"])
    # Extend with name handling, event refs, etc.