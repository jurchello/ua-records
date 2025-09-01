from __future__ import annotations
from typing import Any, Dict, Tuple

from gramps.gen.lib import TableObject

from repositories.base_object_repository import BaseObjectRepository


class TableObjectRepository(BaseObjectRepository):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_change_display(self, obj: TableObject) -> str:
        return obj.get_change_display()

    def get_change_time(self, obj: TableObject) -> int:
        return obj.get_change_time()

    def get_handle(self, obj: TableObject) -> str:
        return obj.get_handle()

    def set_change_time(self, obj: TableObject, change: int) -> None:
        obj.set_change_time(change)

    def set_handle(self, obj: TableObject, handle: str) -> None:
        obj.set_handle(handle)

    def serialize(self, obj: TableObject) -> Tuple[Any, ...]:
        return obj.serialize()

    def unserialize(self, obj: TableObject, data: Tuple[Any, ...]) -> None:
        obj.unserialize(data)

    def get_schema(self) -> Dict[str, Any]:
        return TableObject.get_schema()

    def get_secondary_fields(self) -> Dict[str, Any]:
        return TableObject.get_secondary_fields()