from __future__ import annotations

from typing import Any, List


def set_if(obj: Any, attr: str, value) -> None:
    setter = getattr(obj, f"set_{attr}", None)
    if callable(setter):
        setter(value)


def ensure_list(obj: Any, attr: str) -> List[Any]:
    getter = getattr(obj, f"get_{attr}", None)
    current = getter() if callable(getter) else None
    if current is None:
        current = []
        setter = getattr(obj, f"set_{attr}", None)
        if callable(setter):
            setter(current)
    return current
