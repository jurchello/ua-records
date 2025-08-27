from __future__ import annotations
from typing import Any, Callable, Dict

class GrampsAdapter:
    """Thin adapter to map kind → concrete add/commit/remove callables."""
    def __init__(
        self,
        add_map: Dict[str, Callable[[Any], str]],
        commit_map: Dict[str, Callable[[Any], None]],
        remove_map: Dict[str, Callable[[str], None]] | None = None
    ) -> None:
        self.add_map = add_map
        self.commit_map = commit_map
        self.remove_map = remove_map or {}

    def add(self, kind: str, obj: Any) -> str:
        fn = self.add_map.get(kind)
        if not fn:
            raise ValueError(f"no add fn for kind={kind}")
        return fn(obj)

    def commit(self, kind: str, obj: Any) -> None:
        fn = self.commit_map.get(kind)
        if not fn:
            raise ValueError(f"no commit fn for kind={kind}")
        fn(obj)

    def remove(self, kind: str, handle: str) -> None:
        fn = self.remove_map.get(kind)
        if not fn:
            raise ValueError(f"no remove fn for kind={kind}")
        fn(handle)