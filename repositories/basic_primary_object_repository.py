from __future__ import annotations
from typing import Any, List, Optional

from gramps.gen.lib.primaryobj import BasicPrimaryObject

from repositories.privacy_base_repository import PrivacyBaseRepository
from repositories.table_object_repository import TableObjectRepository
from repositories.tag_base_repository import TagBaseRepository


class BasicPrimaryObjectRepository(
    TableObjectRepository, 
    PrivacyBaseRepository,
    TagBaseRepository,
):
    
    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_gramps_id(self, obj) -> Optional[str]:
        return obj.get_gramps_id()

    def set_gramps_id(self, obj, gramps_id: str) -> None:
        obj.set_gramps_id(gramps_id)

    def has_citation_reference(self, obj, handle: str) -> bool:
        return obj.has_citation_reference(handle)

    def has_handle_reference(self, obj, classname: str, handle: str) -> bool:
        return obj.has_handle_reference(classname, handle)

    def has_media_reference(self, obj, handle: str) -> bool:
        return obj.has_media_reference(handle)

    def remove_citation_references(self, obj, handle_list: List[str]) -> None:
        obj.remove_citation_references(handle_list)

    def remove_handle_references(self, obj, classname: str, handle_list: List[str]) -> None:
        obj.remove_handle_references(classname, handle_list)

    def remove_media_references(self, obj, handle_list: List[str]) -> None:
        obj.remove_media_references(handle_list)

    def replace_citation_references(self, obj, old_handle: str, new_handle: str) -> None:
        obj.replace_citation_references(old_handle, new_handle)

    def replace_handle_reference(self, obj, classname: str, old_handle: str, new_handle: str) -> None:
        obj.replace_handle_reference(classname, old_handle, new_handle)

    def replace_media_references(self, obj, old_handle: str, new_handle: str) -> None:
        obj.replace_media_references(old_handle, new_handle)

    def serialize(self, obj) -> Any:
        return obj.serialize()

    def unserialize(self, obj, data: Any) -> None:
        obj.unserialize(data)
