from __future__ import annotations
from typing import List, Any
from gramps.gen.lib import MediaBase

from repositories.base_repository import BaseRepository


class MediaBaseRepository(BaseRepository):
    
    def get_media_list(self, obj: MediaBase) -> List[Any]:
        return obj.get_media_list()
    
    def add_media_reference(self, obj: MediaBase, media_ref: Any) -> None:
        obj.add_media_reference(media_ref)
    
    def has_media_reference(self, obj: MediaBase, obj_handle: str) -> bool:
        return obj.has_media_reference(obj_handle)
    
    def remove_media_references(self, obj: MediaBase, obj_handle_list: List[str]) -> None:
        obj.remove_media_references(obj_handle_list)
    
    def replace_media_references(self, obj: MediaBase, old_handle: str, new_handle: str) -> None:
        obj.replace_media_references(old_handle, new_handle)
    
    def set_media_list(self, obj: MediaBase, media_list: List[Any]) -> None:
        obj.set_media_list(media_list)