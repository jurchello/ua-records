from __future__ import annotations
from typing import Any, List, Tuple
from gramps.gen.lib.reporef import RepoRef
from repositories.secondary_object_repository import SecondaryObjectRepository
from repositories.privacy_base_repository import PrivacyBaseRepository
from repositories.note_base_repository import NoteBaseRepository
from repositories.ref_base_repository import RefBaseRepository

class RepoRefRepository(
    SecondaryObjectRepository,
    PrivacyBaseRepository,
    NoteBaseRepository,
    RefBaseRepository,
):
    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_call_number(self, obj) -> str:
        return obj.get_call_number()

    def get_media_type(self, obj) -> Any:
        return obj.get_media_type()

    def get_referenced_handles(self, obj) -> List[Tuple[str, str]]:
        return obj.get_referenced_handles()

    @classmethod
    def get_schema(cls) -> dict:
        return RepoRef.get_schema()

    def get_text_data_list(self, obj) -> List[Any]:
        return obj.get_text_data_list()

    def is_equivalent(self, obj, other) -> int:
        return obj.is_equivalent(other)

    def merge(self, obj, acquisition) -> None:
        obj.merge(acquisition)

    def serialize(self, obj) -> Any:
        return obj.serialize()

    def set_call_number(self, obj, number: str) -> None:
        obj.set_call_number(number)

    def set_media_type(self, obj, media_type: Any) -> None:
        obj.set_media_type(media_type)

    def unserialize(self, obj, data: Any) -> None:
        obj.unserialize(data)

    def call_number(self, obj) -> str:
        try:
            return obj.call_number
        except AttributeError:
            return obj.get_call_number()

    def media_type(self, obj) -> Any:
        try:
            return obj.media_type
        except AttributeError:
            return obj.get_media_type()