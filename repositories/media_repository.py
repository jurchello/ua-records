from __future__ import annotations
from typing import Any, List, Tuple
from gramps.gen.lib.media import Media
from repositories.citation_base_repository import CitationBaseRepository
from repositories.note_base_repository import NoteBaseRepository
from repositories.date_base_repository import DateBaseRepository
from repositories.attribute_base_repository import AttributeBaseRepository
from repositories.primary_object_repository import PrimaryObjectRepository

class MediaRepository(
    CitationBaseRepository,
    NoteBaseRepository,
    DateBaseRepository,
    AttributeBaseRepository,
    PrimaryObjectRepository,
):
    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_checksum(self, obj: Media) -> str:
        return obj.get_checksum()

    def get_citation_child_list(self, obj: Media) -> List[Any]:
        return obj.get_citation_child_list()

    def get_description(self, obj: Media) -> str:
        return obj.get_description()

    def get_handle_referents(self, obj: Media) -> List[Any]:
        return obj.get_handle_referents()

    def get_mime_type(self, obj: Media) -> str:
        return obj.get_mime_type()

    def get_note_child_list(self, obj: Media) -> List[Any]:
        return obj.get_note_child_list()

    def get_path(self, obj: Media) -> str:
        return obj.get_path()

    def get_referenced_handles(self, obj: Media) -> List[Tuple[str, str]]:
        return obj.get_referenced_handles()

    @classmethod
    def get_schema(cls) -> dict:
        return Media.get_schema()

    def get_text_data_child_list(self, obj: Media) -> List[Any]:
        return obj.get_text_data_child_list()

    def get_text_data_list(self, obj: Media) -> List[Any]:
        return obj.get_text_data_list()

    def merge(self, obj: Media, acquisition: Media) -> None:
        obj.merge(acquisition)

    def serialize(self, obj: Media, no_text_date: bool = False) -> Tuple[Any, ...]:
        return obj.serialize(no_text_date=no_text_date)

    def set_checksum(self, obj: Media, text: str) -> None:
        obj.set_checksum(text)

    def set_description(self, obj: Media, text: str) -> None:
        obj.set_description(text)

    def set_mime_type(self, obj: Media, mime_type: str) -> None:
        obj.set_mime_type(mime_type)

    def set_path(self, obj: Media, path: str) -> None:
        obj.set_path(path)

    def unserialize(self, obj: Media, data: Tuple[Any, ...]) -> None:
        obj.unserialize(data)

    def description(self, obj: Media) -> str:
        try:
            return obj.description
        except AttributeError:
            return obj.get_description()

    def mime_type(self, obj: Media) -> str:
        try:
            return obj.mime_type
        except AttributeError:
            return obj.get_mime_type()

    def path(self, obj: Media) -> str:
        try:
            return obj.path
        except AttributeError:
            return obj.get_path()