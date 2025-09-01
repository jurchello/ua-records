from __future__ import annotations
from typing import Any, List, Dict, Optional, Tuple
from gramps.gen.lib import PlaceRef
from repositories.ref_base_repository import RefBaseRepository
from repositories.date_base_repository import DateBaseRepository
from repositories.secondary_object_repository import SecondaryObjectRepository

class PlaceRefRepository(
    RefBaseRepository, 
    DateBaseRepository, 
    SecondaryObjectRepository
):
    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_citation_child_list(self, obj: PlaceRef) -> List[Any]:
        return obj.get_citation_child_list()

    def get_handle_referents(self, obj: PlaceRef) -> List[Any]:
        return obj.get_handle_referents()

    def get_note_child_list(self, obj: PlaceRef) -> List[Any]:
        return obj.get_note_child_list()

    def get_referenced_handles(self, obj: PlaceRef) -> List[Tuple[str, Optional[str]]]:
        return obj.get_referenced_handles()

    def get_schema(self) -> Dict[str, Any]:
        return PlaceRef.get_schema()

    def get_text_data_child_list(self, obj: PlaceRef) -> List[Any]:
        return obj.get_text_data_child_list()

    def get_text_data_list(self, obj: PlaceRef) -> List[str]:
        return obj.get_text_data_list()

    def is_equivalent(self, obj: PlaceRef, other: PlaceRef) -> int:
        return obj.is_equivalent(other)

    def serialize(self, obj: PlaceRef) -> Tuple[Any, ...]:
        return obj.serialize()

    def unserialize(self, obj: PlaceRef, data: Tuple[Any, ...]) -> None:
        obj.unserialize(data)