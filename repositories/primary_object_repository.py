from __future__ import annotations

from typing import Any, List, Tuple, Union

from gramps.gen.lib import PrimaryObject

from repositories.basic_primary_object_repository import BasicPrimaryObjectRepository


class PrimaryObjectRepository(BasicPrimaryObjectRepository):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def has_handle_reference(self, obj, classname: str, handle: str) -> bool:
        return obj.has_handle_reference(classname, handle)

    def remove_handle_references(self, obj, classname: str, handle_list: List[str]) -> None:
        obj.remove_handle_references(classname, handle_list)

    def replace_handle_reference(self, obj, classname: str, old_handle: str, new_handle: str) -> None:
        obj.replace_handle_reference(classname, old_handle, new_handle)

    def serialize(self, obj) -> Union[Tuple[Any, ...], None]:
        return obj.serialize()

    def unserialize(self, obj, data: Tuple[Any, ...]) -> None:
        obj.unserialize(data)
