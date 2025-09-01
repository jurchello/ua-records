from __future__ import annotations
from typing import Any, List, Optional, Tuple
from gramps.gen.lib import Family
from gramps.gen.lib.childref import ChildRef
from gramps.gen.lib.eventref import EventRef
from gramps.gen.lib.familyreltype import FamilyRelType
from repositories.citation_base_repository import CitationBaseRepository
from repositories.note_base_repository import NoteBaseRepository
from repositories.media_base_repository import MediaBaseRepository
from repositories.attribute_base_repository import AttributeBaseRepository
from repositories.primary_object_repository import PrimaryObjectRepository

class FamilyRepository(
    CitationBaseRepository,
    NoteBaseRepository,
    MediaBaseRepository,
    AttributeBaseRepository,
    PrimaryObjectRepository,
):
    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def add_child_ref(self, obj: Family, child_ref: ChildRef) -> None:
        obj.add_child_ref(child_ref)

    def add_event_ref(self, obj: Family, event_ref: EventRef) -> None:
        obj.add_event_ref(event_ref)

    def get_child_ref_list(self, obj: Family) -> List[ChildRef]:
        return obj.get_child_ref_list()

    def get_citation_child_list(self, obj: Family) -> List[Any]:
        return obj.get_citation_child_list()

    def get_event_list(self, obj: Family) -> List[Any]:
        return obj.get_event_list()

    def get_event_ref_list(self, obj: Family) -> List[EventRef]:
        return obj.get_event_ref_list()

    def get_father_handle(self, obj: Family) -> Optional[str]:
        return obj.get_father_handle()

    def get_handle_referents(self, obj: Family) -> List[Any]:
        return obj.get_handle_referents()

    def get_mother_handle(self, obj: Family) -> Optional[str]:
        return obj.get_mother_handle()

    def get_note_child_list(self, obj: Family) -> List[Any]:
        return obj.get_note_child_list()

    def get_referenced_handles(self, obj: Family) -> List[Tuple[str, str]]:
        return obj.get_referenced_handles()

    def get_relationship(self, obj: Family) -> FamilyRelType:
        return obj.get_relationship()

    @classmethod
    def get_schema(cls) -> dict:
        return Family.get_schema()

    def get_text_data_child_list(self, obj: Family) -> List[Any]:
        return obj.get_text_data_child_list()

    def get_text_data_list(self, obj: Family) -> List[Any]:
        return obj.get_text_data_list()

    def merge(self, obj: Family, acquisition: Family) -> None:
        obj.merge(acquisition)

    def remove_child_handle(self, obj: Family, child_handle: str) -> None:
        obj.remove_child_handle(child_handle)

    def remove_child_ref(self, obj: Family, child_ref: ChildRef) -> None:
        obj.remove_child_ref(child_ref)

    def serialize(self, obj: Family) -> Tuple[Any, ...]:
        return obj.serialize()

    def set_child_ref_list(self, obj: Family, child_ref_list: List[ChildRef]) -> None:
        obj.set_child_ref_list(child_ref_list)

    def set_event_ref_list(self, obj: Family, event_ref_list: List[EventRef]) -> None:
        obj.set_event_ref_list(event_ref_list)

    def set_father_handle(self, obj: Family, person_handle: str) -> None:
        obj.set_father_handle(person_handle)

    def set_mother_handle(self, obj: Family, person_handle: str) -> None:
        obj.set_mother_handle(person_handle)

    def set_relationship(self, obj: Family, relationship_type: Tuple[int, str]) -> None:
        obj.set_relationship(relationship_type)

    def unserialize(self, obj: Family, data: Tuple[Any, ...]) -> None:
        obj.unserialize(data)