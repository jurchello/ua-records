from __future__ import annotations
from typing import Any, Dict
from .apply_helpers import set_if

def build_event(data: Dict[str,Any]) -> Any:
    return data.get("_obj_factory", lambda: {})()

def patch_event(obj: Any, data: Dict[str,Any]) -> None:
    if "type" in data:
        set_if(obj, "type", data["type"])
    # Map date/place/description as needed in your environment.