from __future__ import annotations

from typing import Any, Iterator, List, Optional, Tuple

from gramps.gen.lib import Event

from repositories.attribute_base_repository import AttributeBaseRepository
from repositories.citation_base_repository import CitationBaseRepository
from repositories.date_base_repository import DateBaseRepository
from repositories.media_base_repository import MediaBaseRepository
from repositories.note_base_repository import NoteBaseRepository
from repositories.place_base_repository import PlaceBaseRepository
from repositories.primary_object_repository import PrimaryObjectRepository
from gramps.gen.lib.eventtype import EventType


class EventRepository(
    CitationBaseRepository,
    NoteBaseRepository,
    MediaBaseRepository,
    AttributeBaseRepository,
    DateBaseRepository,
    PlaceBaseRepository,
    PrimaryObjectRepository,
):
    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def are_equal(self, obj, other) -> bool:
        return obj.are_equal(other)

    def get_citation_child_list(self, obj) -> List[Any]:
        return obj.get_citation_child_list()

    def get_description(self, obj) -> str:
        return obj.get_description()

    def get_handle_referents(self, obj) -> List[Any]:
        return obj.get_handle_referents()

    def get_note_child_list(self, obj) -> List[Any]:
        return obj.get_note_child_list()

    def get_referenced_handles(self, obj) -> List[Tuple[str, str]]:
        return obj.get_referenced_handles()

    @classmethod
    def get_schema(cls) -> dict:
        return Event.get_schema()

    def get_text_data_child_list(self, obj) -> List[Any]:
        return obj.get_text_data_child_list()

    def get_text_data_list(self, obj) -> List[Any]:
        return obj.get_text_data_list()

    def get_type(self, obj) -> EventType:
        return obj.get_type()

    def is_empty(self, obj) -> bool:
        return obj.is_empty()

    def merge(self, obj, acquisition) -> None:
        obj.merge(acquisition)

    def serialize(self, obj, no_text_date: bool = False) -> Tuple[Any, ...]:
        return obj.serialize(no_text_date=no_text_date)

    def set_description(self, obj, description: str) -> None:
        obj.set_description(description)

    def set_type(self, obj, the_type: Tuple[int, str]) -> None:
        obj.set_type(the_type)

    def unserialize(self, obj, data: Tuple[Any, ...]) -> None:
        obj.unserialize(data)

    def description(self, obj) -> str:
        try:
            return obj.description
        except AttributeError:
            return obj.get_description()

    def type(self, obj) -> EventType:
        try:
            return obj.type
        except AttributeError:
            return obj.get_type()

