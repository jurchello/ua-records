from __future__ import annotations
from typing import Any, List, Tuple
from gramps.gen.lib.mediaref import MediaRef
from repositories.secondary_object_repository import SecondaryObjectRepository
from repositories.privacy_base_repository import PrivacyBaseRepository
from repositories.citation_base_repository import CitationBaseRepository
from repositories.note_base_repository import NoteBaseRepository
from repositories.ref_base_repository import RefBaseRepository
from repositories.attribute_base_repository import AttributeBaseRepository

class MediaRefRepository(
    SecondaryObjectRepository,
    PrivacyBaseRepository,
    CitationBaseRepository,
    NoteBaseRepository,
    RefBaseRepository,
    AttributeBaseRepository,
):
    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_citation_child_list(self, obj: MediaRef) -> List[Any]:
        return obj.get_citation_child_list()

    def get_handle_referents(self, obj: MediaRef) -> List[Any]:
        return obj.get_handle_referents()

    def get_note_child_list(self, obj: MediaRef) -> List[Any]:
        return obj.get_note_child_list()

    def get_rectangle(self, obj: MediaRef) -> Any:
        return obj.get_rectangle()

    def get_referenced_handles(self, obj: MediaRef) -> List[Tuple[str, str]]:
        return obj.get_referenced_handles()

    @classmethod
    def get_schema(cls) -> dict:
        return MediaRef.get_schema()

    def get_text_data_child_list(self, obj: MediaRef) -> List[Any]:
        return obj.get_text_data_child_list()

    def is_equivalent(self, obj: MediaRef, other: MediaRef) -> int:
        return obj.is_equivalent(other)

    def merge(self, obj: MediaRef, acquisition: MediaRef) -> None:
        obj.merge(acquisition)

    def serialize(self, obj: MediaRef) -> Any:
        return obj.serialize()

    def set_rectangle(self, obj: MediaRef, coord: Any) -> None:
        obj.set_rectangle(coord)

    def unserialize(self, obj: MediaRef, data: Any) -> None:
        obj.unserialize(data)