from __future__ import annotations

from typing import Any, List, Tuple


from repositories.repository_core import RepositoryCore


class RefBaseRepository(RepositoryCore):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_reference_handle(self, obj) -> str:
        return obj.get_reference_handle()

    def get_referenced_handles(self, obj) -> List[Tuple[str, str]]:
        return obj.get_referenced_handles()

    def serialize(self, obj) -> Any:
        return obj.serialize()

    def set_reference_handle(self, obj, handle: str) -> None:
        obj.set_reference_handle(handle)

    def unserialize(self, obj, data: Any) -> None:
        obj.unserialize(data)

    def reference_handle(self, obj) -> str:
        try:
            return obj.reference_handle
        except AttributeError:
            return obj.get_reference_handle()