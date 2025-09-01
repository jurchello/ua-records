from __future__ import annotations

from typing import Any, Dict, List, Tuple

from gramps.gen.lib import ChildRef

from repositories.citation_base_repository import CitationBaseRepository
from repositories.note_base_repository import NoteBaseRepository
from repositories.privacy_base_repository import PrivacyBaseRepository
from repositories.ref_base_repository import RefBaseRepository
from repositories.secondary_object_repository import SecondaryObjectRepository



class ChildRefRepository(
    SecondaryObjectRepository, 
    PrivacyBaseRepository, 
    CitationBaseRepository, 
    NoteBaseRepository, 
    RefBaseRepository
):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_father_relation(self, obj: ChildRef) -> Any:
        return obj.get_father_relation()

    def get_mother_relation(self, obj: ChildRef) -> Any:
        return obj.get_mother_relation()

    def set_father_relation(self, obj: ChildRef, frel: Any) -> None:
        obj.set_father_relation(frel)

    def set_mother_relation(self, obj: ChildRef, rel: Any) -> None:
        obj.set_mother_relation(rel)

    def get_handle_referents(self, obj: ChildRef) -> List[Any]:
        return obj.get_handle_referents()

    def get_note_child_list(self, obj: ChildRef) -> List[Any]:
        return obj.get_note_child_list()

    def get_referenced_handles(self, obj: ChildRef) -> List[Tuple[str, str]]:
        return obj.get_referenced_handles()

    def get_text_data_child_list(self, obj: ChildRef) -> List[Any]:
        return obj.get_text_data_child_list()

    def get_text_data_list(self, obj: ChildRef) -> List[Any]:
        return obj.get_text_data_list()

    def is_equivalent(self, obj: ChildRef, other: ChildRef) -> int:
        return obj.is_equivalent(other)

    def merge(self, obj: ChildRef, acquisition: ChildRef) -> None:
        obj.merge(acquisition)

    def serialize(self, obj: ChildRef) -> Tuple[Any, ...]:
        return obj.serialize()

    def unserialize(self, obj: ChildRef, data: Tuple[Any, ...]) -> None:
        obj.unserialize(data)

    def get_schema(self) -> Dict[str, Any]:
        return ChildRef.get_schema()
