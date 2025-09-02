from __future__ import annotations
from typing import Any, Dict, Tuple


from repositories.base_object_repository import BaseObjectRepository


class TableObjectRepository(BaseObjectRepository):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_change_display(self, obj) -> str:
        return obj.get_change_display()

    def get_change_time(self, obj) -> int:
        return obj.get_change_time()

    def get_handle(self, obj) -> str:
        return obj.get_handle()

    def set_change_time(self, obj, change: int) -> None:
        obj.set_change_time(change)

    def set_handle(self, obj, handle: str) -> None:
        obj.set_handle(handle)

    def serialize(self, obj) -> Tuple[Any, ...]:
        return obj.serialize()

    def unserialize(self, obj, data: Tuple[Any, ...]) -> None:
        obj.unserialize(data)

    def get_schema(self, obj) -> Dict[str, Any]:
        return obj.get_schema()

    def get_secondary_fields(self, obj) -> Dict[str, Any]:
        return obj.get_secondary_fields()