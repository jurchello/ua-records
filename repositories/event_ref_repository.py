from __future__ import annotations
from typing import Any, List, Tuple

from gramps.gen.lib import EventRef
from repositories.attribute_base_repository import AttributeBaseRepository
from repositories.indirect_citation_base_repository import IndirectCitationBaseRepository
from repositories.note_base_repository import NoteBaseRepository
from repositories.privacy_base_repository import PrivacyBaseRepository
from repositories.ref_base_repository import RefBaseRepository
from repositories.secondary_object_repository import SecondaryObjectRepository


class EventRefRepository(
    PrivacyBaseRepository, 
    NoteBaseRepository, 
    AttributeBaseRepository, 
    RefBaseRepository, 
    IndirectCitationBaseRepository, 
    SecondaryObjectRepository
):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_citation_child_list(self, obj) -> List[Any]:
        return obj.get_citation_child_list()

    def get_handle_referents(self, obj) -> List[Any]:
        return obj.get_handle_referents()

    def get_note_child_list(self, obj) -> List[Any]:
        return obj.get_note_child_list()

    def get_referenced_handles(self, obj) -> List[Tuple[str, str]]:
        return obj.get_referenced_handles()

    def get_role(self, obj) -> Any:
        return obj.get_role()

    @classmethod
    def get_schema(cls) -> dict:
        return EventRef.get_schema()

    def get_text_data_child_list(self, obj) -> List[Any]:
        return obj.get_text_data_child_list()

    def get_text_data_list(self, obj) -> List[Any]:
        return obj.get_text_data_list()

    def is_equivalent(self, obj, other) -> int:
        return obj.is_equivalent(other)

    def merge(self, obj, acquisition) -> None:
        obj.merge(acquisition)

    def serialize(self, obj) -> Any:
        return obj.serialize()

    def set_role(self, obj, role: Any) -> None:
        obj.set_role(role)

    def unserialize(self, obj, data: Any) -> None:
        obj.unserialize(data)

    def role(self, obj) -> Any:
        try:
            return obj.role
        except AttributeError:
            return obj.get_role()
