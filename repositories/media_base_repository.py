from __future__ import annotations

from typing import Any, List

from gramps.gen.lib.mediabase import MediaBase
from gramps.gen.lib.mediaref import MediaRef

from repositories.repository_core import RepositoryCore


class MediaBaseRepository(RepositoryCore):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def add_media_reference(self, obj, media_ref: MediaRef) -> None:
        obj.add_media_reference(media_ref)

    def get_media_list(self, obj) -> List[MediaRef]:
        return obj.get_media_list()

    def has_media_reference(self, obj, obj_handle: str) -> bool:
        return obj.has_media_reference(obj_handle)

    def remove_media_references(self, obj, obj_handle_list: List[str]) -> None:
        obj.remove_media_references(obj_handle_list)

    def replace_media_references(self, obj, old_handle: str, new_handle: str) -> None:
        obj.replace_media_references(old_handle, new_handle)

    def serialize(self, obj) -> Any:
        return obj.serialize()

    def set_media_list(self, obj, media_ref_list: List[MediaRef]) -> None:
        obj.set_media_list(media_ref_list)

    def unserialize(self, obj, data: Any) -> None:
        obj.unserialize(data)

    def media_list(self, obj) -> List[MediaRef]:
        try:
            return obj.media_list
        except AttributeError:
            return obj.get_media_list()
