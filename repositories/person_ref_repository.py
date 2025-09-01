from __future__ import annotations
from typing import Any, List, Tuple
from gramps.gen.lib.personref import PersonRef
from repositories.secondary_object_repository import SecondaryObjectRepository
from repositories.privacy_base_repository import PrivacyBaseRepository
from repositories.citation_base_repository import CitationBaseRepository
from repositories.note_base_repository import NoteBaseRepository
from repositories.ref_base_repository import RefBaseRepository

class PersonRefRepository(
    SecondaryObjectRepository,
    PrivacyBaseRepository,
    CitationBaseRepository,
    NoteBaseRepository,
    RefBaseRepository,
):
    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_handle_referents(self, obj: PersonRef) -> List[Any]:
        return obj.get_handle_referents()

    def get_note_child_list(self, obj: PersonRef) -> List[Any]:
        return obj.get_note_child_list()

    def get_referenced_handles(self, obj: PersonRef) -> List[Tuple[str, str]]:
        return obj.get_referenced_handles()

    def get_relation(self, obj: PersonRef) -> Any:
        return obj.get_relation()

    @classmethod
    def get_schema(cls) -> dict:
        return PersonRef.get_schema()

    def get_text_data_child_list(self, obj: PersonRef) -> List[Any]:
        return obj.get_text_data_child_list()

    def get_text_data_list(self, obj: PersonRef) -> List[Any]:
        return obj.get_text_data_list()

    def is_equivalent(self, obj: PersonRef, other: PersonRef) -> int:
        return obj.is_equivalent(other)

    def merge(self, obj: PersonRef, acquisition: PersonRef) -> None:
        obj.merge(acquisition)

    def serialize(self, obj: PersonRef) -> Any:
        return obj.serialize()

    def set_relation(self, obj: PersonRef, rel: Any) -> None:
        obj.set_relation(rel)

    def unserialize(self, obj: PersonRef, data: Any) -> None:
        obj.unserialize(data)

    def relation(self, obj: PersonRef) -> Any:
        try:
            return obj.relation
        except AttributeError:
            return obj.get_relation()