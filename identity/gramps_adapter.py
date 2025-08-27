from __future__ import annotations
from typing import Any, Callable, Dict
from identity.identity_map import CommitAdapter

class GrampsAdapter(CommitAdapter):
    def __init__(self, add_map: Dict[str, Callable[[Any], str]], commit_map: Dict[str, Callable[[Any], None]]) -> None:
        self.add_map = add_map
        self.commit_map = commit_map
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