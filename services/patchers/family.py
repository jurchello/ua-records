from __future__ import annotations

from typing import Any, Dict


def build_family(data: Dict[str, Any]) -> Any:
    return data.get("_obj_factory", lambda: {})()


def patch_family(_obj: Any, _data: Dict[str, Any]) -> None:
    # TODO: implement mapping of spouses/event_refs/etc. to a real Gramps Family object
    # Example ideas:
    # - set_father_handle / set_mother_handle based on spouses list
    # - maintain event references list for marriage event
    pass
