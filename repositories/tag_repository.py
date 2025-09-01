from __future__ import annotations
from typing import Any, List, Dict, Tuple
from gramps.gen.lib import Tag
from repositories.table_object_repository import TableObjectRepository

class TagRepository(TableObjectRepository):
    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def are_equal(self, obj: Tag, other: Tag) -> bool:
        return obj.are_equal(other)

    def get_color(self, obj: Tag) -> str:
        return obj.get_color()

    def get_name(self, obj: Tag) -> str:
        return obj.get_name()

    def get_priority(self, obj: Tag) -> int:
        return obj.get_priority()

    def get_schema(self) -> Dict[str, Any]:
        return Tag.get_schema()

    def get_text_data_list(self, obj: Tag) -> List[str]:
        return obj.get_text_data_list()

    def is_empty(self, obj: Tag) -> bool:
        return obj.is_empty()

    def serialize(self, obj: Tag) -> Tuple[Any, ...]:
        return obj.serialize()

    def set_color(self, obj: Tag, color: str) -> None:
        obj.set_color(color)

    def set_name(self, obj: Tag, name: str) -> None:
        obj.set_name(name)

    def set_priority(self, obj: Tag, priority: int) -> None:
        obj.set_priority(priority)

    def unserialize(self, obj: Tag, data: Tuple[Any, ...]) -> None:
        obj.unserialize(data)