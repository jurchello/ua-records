from __future__ import annotations

from typing import Any, List, Optional, Tuple

from gramps.gen.lib import Citation

from repositories.attribute_base_repository import AttributeBaseRepository
from repositories.citation_base_repository import CitationBaseRepository
from repositories.media_base_repository import MediaBaseRepository
from repositories.note_base_repository import NoteBaseRepository
from repositories.primary_object_repository import PrimaryObjectRepository

class CitationRepository(
    CitationBaseRepository,
    AttributeBaseRepository,
    PrimaryObjectRepository,
    MediaBaseRepository,
    NoteBaseRepository,
):
    CONF_HIGH = 3 
    CONF_LOW = 1 
    CONF_NORMAL = 2 
    CONF_VERY_HIGH = 4 
    CONF_VERY_LOW = 0

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_citation_child_list(self, obj) -> List[Any]:
        return obj.get_citation_child_list()

    def get_confidence_level(self, obj) -> int:
        return obj.get_confidence_level()

    def set_confidence_level(self, obj, val: int) -> None:
        obj.set_confidence_level(val)

    def get_handle_referents(self, obj) -> List[Any]:
        return obj.get_handle_referents()

    def get_note_child_list(self, obj) -> List[Any]:
        return obj.get_note_child_list()

    def get_page(self, obj) -> str:
        return obj.get_page()

    def set_page(self, obj, page: str) -> None:
        obj.set_page(page)

    def get_reference_handle(self, obj) -> Optional[str]:
        return obj.get_reference_handle()

    def set_reference_handle(self, obj, val: str) -> None:
        obj.set_reference_handle(val)

    def get_referenced_handles(self, obj) -> List[Tuple[str, str]]:
        return obj.get_referenced_handles()

    def get_text_data_child_list(self, obj) -> List[Any]:
        return obj.get_text_data_child_list()

    def get_text_data_list(self, obj) -> List[str]:
        return obj.get_text_data_list()

    def merge(self, obj, acquisition) -> None:
        obj.merge(acquisition)

    def serialize(self, obj, no_text_date: bool = False) -> Tuple[Any, ...]:
        return obj.serialize(no_text_date=no_text_date)

    def unserialize(self, obj, data: Tuple[Any, ...]) -> None:
        obj.unserialize(data)
